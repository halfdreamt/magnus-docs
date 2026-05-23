# Rewrite Regression — Sim 3x slower despite similar dynamics

**Date:** 2026-04-13 (investigation), resolved 2026-05-23
**Status:** Root cause identified. Fix designed but not yet committed.
**Context:** Following the labor+gathering rewrite, starvation/famine model, and per-person→embedded-interval redesign, the simulation runs ~3x slower than the pre-rewrite baseline despite producing similar entity counts and fewer events.

## Resolution (2026-05-23)

**Root cause:** Flecs archetype churn from per-person `Starving` and per-community `CurrentFamine` component toggling.

Per 1000y run at default config (3 communities, seed 42):
- ~54,000 Starving add + ~53,000 Starving remove
- ~2,200 CurrentFamine add + ~2,200 CurrentFamine remove
- Each component add/remove moves the entity between Flecs archetype tables. These ops are queued during the system callback's defer scope and flushed *after* the callback returns, inside Flecs's outer pipeline defer scope — which is exactly the "248ms flecs_overhead" measured below (no per-subsystem timer covered it).

**Confirmation experiment:** Replaced both components with process-level `unordered_map`-based side state (entity_id → since_tick for Starving, community_id → famine_event for CurrentFamine) behind a `constexpr bool kUseStarvingComponents` flag. All semantics — interval bookkeeping, death rolls, famine lifecycle, BirthSystem's starvation gate — held identical. Code lives in `src/systems/ConsumptionSystem.hpp`.

Results, default config, 1000y seed 42:

| Metric | Pre-rewrite (`624d74a`) | Current as-shipped | With side-map fix |
|---|---|---|---|
| Sim time | 121ms | 380ms | **163ms** |
| Flecs tables | 3,859 | 6,740 | 4,492 |
| callback_total | — | 142ms | 128ms |
| flecs_overhead | — | 218ms | **35ms** |
| Events | 6,951 | 4,728 | 4,698 |

Side-map cuts sim time by 58%, "flecs_overhead" by 84%, table count by 33%. Residual ~35% regression vs pre-rewrite (121 → 163ms) is the legitimate cost of per-season cadence + plot entities + incest BFS + family tenure components — small and acceptable.

**Why the misattribution of cost.** The original `_cb_t` timer wraps from `defer_begin()` to `defer_end()` inside the system callback. But our nested `defer_end()` only decrements a counter; Flecs's outer pipeline-level defer scope still has the queue. The actual archetype-table moves happen when Flecs flushes that outer scope, *after* our callback returns but *before* `progress()` returns. That's why `tick_total − callback_total` scaled linearly with community-season count even though `progress()` only fires once per tick.

**Scaling sanity check.** 1-community config produces the same number of `progress()` calls but ~1/3 the community-seasons. "flecs_overhead" scaled almost linearly with community-seasons (~15μs/com-season in both configs), not with progress() calls — proving the cost lives in per-community work, not Flecs internal per-tick overhead.

### Behavior delta between variants

The side-map variant emits 4,698 events vs 4,728 with components — a ~0.6% delta. Per-community Y1000 populations also differ (20/23/28 vs 20/30/17 alive). Both are deterministic re-run-to-re-run; the delta comes from Flecs iteration order: in the component path, communities with `CurrentFamine` sit in a different archetype table from those without, so `ecs.each<CommunityIdentity, FoodStores>` visits them in a different order than the side-map path. Different visit order → different `next_event_id` assignment → divergent downstream RNG once entity IDs influence anything. Verified: no overlapping or back-to-back famine spells in either path; macro famine behavior is equivalent.

### Fix options

1. **Adopt side-map as-shipped.** Cheapest; loses determinism continuity with prior saved JSON outputs.
2. **Value-update-only components.** Add `StarvationState{tick}` and `CommunityFamine{event}` to every person/community at creation, never remove — update the value field instead. Archetype membership stays constant → no churn. Preserves current behavior exactly. More structural change, higher implementation cost.
3. **Defer.** Document and live with 380ms. Investigation has the answer; the perf is acceptable for dev workflows.

Recommendation: option 2 if we want to preserve outputs; otherwise option 1.

---

## Original investigation (2026-04-13)

## Measurements

Two commits compared, same seed (42), same year count (1000y), same default config equivalent:

| Metric | Pre-rewrite (`624d74a`) | Current (`2906adb`) | Δ |
|---|---|---|---|
| Sim time | 138ms | 410ms | **+197% (3x)** |
| Entities at end | 1,293 | 1,304 | +0.8% |
| Events at end | 5,659 | 3,425 | -39% |
| People (typical) | ~70 | ~63 | similar |
| Communities (alive Y1000) | 2-3 | 3 | similar |

Same scale of simulation, **fewer** events emitted, but 3x slower. This is not a "more work to do" regression.

## Per-subsystem timing (current state)

Custom instrumentation in `EcologySystem` and `Simulation::run`:

```
EcologyTimings (12,003 community-seasons, 4,001 orch-fires, 410ms total)
  scan=4.7  cache=2.1  leader=5.6  snap=32.9  gather=0.9  consume=20.7
  birth=3.4  marry=1.2  hist=0.2
  exogamy=40.5  cleanup=29.4  fission=4.5  defer_end=0.1
  callback_total=161.6  tick_total=409.8  flecs_overhead=248.1
```

Headline:
- `callback_total` = **162ms** — everything our ecology code does inside the system callback
- `flecs_overhead` = **248ms** — `tick_total - callback_total`, what should be Flecs `progress()` machinery outside our system code

Per-tick "Flecs overhead" cost: 248ms / 4001 ticks ≈ **62μs/tick**.

For comparison, the previous performance log (2026-04-12) recorded Flecs progress overhead as ~2.2μs/tick (commit `624d74a`). **30x increase per tick** if those numbers are directly comparable.

## What's structurally different in the rewrite

| Aspect | Pre-rewrite | Current |
|---|---|---|
| Food production cadence | once/year (Autumn harvest event per community) | every season (silent gathering, no event) |
| Consumption cadence | once/year (Winter lump per community) | every season (per-person allocation loop) |
| Drought / Weather events | Yes (every spring/summer) | Removed |
| Famine events | per-community per winter (~few per run) | per-community per famine spell, with embedded per-person `StarvationInterval`s |
| Per-person `Starving` component | None | Toggle on entry/exit of starvation |
| `CurrentFamine` component on community | None | Toggle on entry/exit of community-level famine |

So we removed Drought/Weather and per-event Harvest, but added per-season per-community work (gather + consume) and per-person Starving toggling.

## A/B test attempts

### 1. Stub the per-person consumption loop entirely
Modified `process_seasonal_consumption` to early-return after computing per-capita allocation, skipping all per-person work (Starving toggling, interval management, death rolls).

**Result:** sim never terminated — populations grew unbounded because food deduction was skipped, leading to entity explosion (3GB memory consumed before kill). Confirms per-person work is load-bearing for the simulation but doesn't isolate the perf cost.

A more careful version of this test would: keep food deduction working, but skip only the `Starving` component add/remove (use a side `unordered_set<entity>` for runtime tracking instead).

## Hypotheses for the 248ms "Flecs overhead"

1. **Component churn from `Starving` toggling.** Each archetype change moves an entity between Flecs internal tables. Even if rare in stable equilibrium, the archetype tables persist and Flecs may scan them on each `progress()` call.
2. **Implicit defer scope work.** Flecs may have its own deferred-operation queue between system fires, applied automatically. Our explicit `defer_end_ms` is 0.1ms, but invisible work in Flecs's outer scope wouldn't show up there.
3. **Measurement artifact.** `tick_total - callback_total` may not actually be "Flecs progress() overhead" in the way I'm interpreting it. Need to verify via Tracy or by a different measurement methodology.
4. **The 2.2μs baseline is stale or measured differently.** That number came from a different commit (`dca84c8`); not a guaranteed apples-to-apples comparison. Today's apples-to-apples test: ran `624d74a` directly → 138ms total sim. If we assume that whole 138ms is the "best case" callback+overhead combined, the regression in *callback work alone* (162ms) already exceeds the pre-rewrite total. So Flecs overhead growth, while real, may not be the full story.

## Open investigation paths

- **Use Tracy properly** (already wired in via `MAGNUS3_TRACY_ENABLED`). Run `magnus3.exe run --profile` with Tracy server attached for true per-zone timing inside Flecs.
- **Disciplined Starving A/B**: replace the component with a runtime `unordered_set<entity>` for the BirthSystem gate; keep food bookkeeping intact; measure delta.
- **Count archetypes / tables**: query Flecs for table count and archetype count at sim end, compare to pre-rewrite.
- **Reduce orchestrator firing frequency**: 4001 progress() calls per 1000y is a known cost. Combining per-season work into one yearly fire would 4x reduce Flecs cost — but loses per-season event granularity (and would re-architect the consumption→birth coupling).
- **Verify on a smaller workload**: e.g. run with just 1 community, see if the regression scales linearly. If not, the regression is dominated by per-season-cadence costs that don't scale with community count.
- **Counter-test on the OLD code path**: confirm the pre-rewrite 138ms isn't achievable with current entity layout by adding per-season firing to the old harvest model and seeing where it lands.

## What also went wrong during this investigation

Spawned multiple parallel `Bash` invocations chasing the same A/B test. The Bash tool auto-backgrounded long-running builds; I tried to read incomplete output, then re-ran, queueing another build behind the first. Net effect: ~10 minutes of wall clock for what should have been a 30-second experiment. Worse: the stubbed sim ran unbounded, leaking 3GB before it was killed.

Lesson: when running build+sim experiments, use a single foreground command, wait for the result, don't re-issue.

## Decision

Documenting and pausing the investigation. The current sim time (410ms) is acceptable for development workflows — sweeps still complete in ~10s, viewer is responsive. The 30x per-tick "Flecs overhead" growth deserves later attention but isn't user-blocking. Next steps when revisiting: start with the disciplined Starving A/B, then Tracy.

(Resumed 2026-05-23 — disciplined Starving A/B was the right call. See **Resolution** section at the top.)
