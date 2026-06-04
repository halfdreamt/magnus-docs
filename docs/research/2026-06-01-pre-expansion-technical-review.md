# Pre-Expansion Technical Review — Cleanup Before the Divine Layers Grow

**Date:** 2026-06-01
**Status:** Review complete — actioning #1 (centralized config) first; remainder backlogged
**Related:** 7-layer architecture (`Magnus3/CLAUDE.md`), divine determinism / model B (`2026-05-28-divine-determinism.md`), DDA / Fertility Restraint + cohesion design (`docs/logs/2026-05-25.md`, Fri–Sun)

## Why this review

Two of seven planned layers are built (Rule/Zeus: leadership + cohesion; Ecology/Venus: food/population/births). Before adding Mars/Mercury/Luna/Sol, take stock of technical debt that will **compound** as the layer count grows. Grounded in a full read of `src/` (systems, core, config, components, generation, cli) and the viewer/export seam, not the logs.

## Headline

The architecture's *design* is sound — single-writer ownership, fixed-phase ordering, model-A→B, the DDA directive pattern. But **almost none of those rules are enforced by structure**; they live in comments and naming discipline, and the cost of *complying* with each rule scales with the number of layers. With 2 of 7 layers built, this is the cheap moment to convert convention into structure — each conversion gets ~3× more expensive per layer added first.

Determinism is intact and not at risk (verified byte-identical repeatedly). None of this is about output stability — per the standing determinism definition these refactors are free to change outputs. It is about whether the rules that *keep* the sim deterministic and auditable survive four more layers.

## Tier 1 — Structural seams that get ~3× harder per layer (do before layer 3)

### 1. Aggregate the configs into one `SimConfig` (HIGHEST LEVERAGE — actioning now)
`EcologyConfig` / `WorldConfig` / `RulerConfig` are threaded by hand as three separate by-value params through ~13 signatures + 4 struct/member declarations. Already painful: the same three configs are passed in **different orders** at different call sites:
- `PersonGenerator::generate_in_family(..., wcfg, cfg, rcfg)` vs `generate_birth(..., cfg, wcfg, rcfg)` vs `WorldGenerator(world, eco, ruler)`.

At 6 configs this is O(configs × call-sites) manual plumbing. **Fix:** one `SimConfig { ecology; world; rule; … }` passed by `const&`. A new layer adds one member and zero new parameters. Call-sites threading the triple today: `World` ctor + members; `register_systems` → both systems; `EcologySystem::register_system` + `SystemState`; `process_season` (already 7+ params); `process_births`; `process_fission`/`perform_fission`; `WorldGenerator` ctor + 3 members; `PersonGenerator::generate_in_family`/`generate_birth`; `cmd_run`/`cmd_generate` (`main.cpp`); `InspectCommand` + members; `ExportCommand` + members.

### 2. Make the tick order explicit
Zeus-before-Venus rests on **which source line the registration call sits on** in `World::register_systems` (both `.kind(flecs::OnUpdate)`, ordered by registration). `RuleSystem.hpp:31-33` hedges ("depends on Flecs merge timing"). **Fix:** explicit Flecs phases (`DependsOn` chain Sol→…→Saturn) or a centralized ordered pipeline + a static assertion. Inserting Mars/Mercury should be a declarative edit, not a line move.

### 3. Build a region→communities index once per season
Four operations each do a global `ecs.each` filtered by region — `process_season`, `cleanup_dead_communities`, exogamy, fission — i.e. **4× O(R×C) per season**. `cleanup_dead_communities` is worst: per-region, and double-refreshes each community's living cache that `process_season` already refreshed (the previously-flagged ~26-30ms). **Fix:** one index built per season, sliced into each consumer. Collapses 4×O(R×C)→1×O(C); reusable by every future per-region layer (Mars raids, Mercury routes).

### 4. Move marriage into Zeus's orchestrator
Marriage is a Rule concern (ruler-deity-arbitrated, `BlessedBy(ruler_deity)`) but **executes inside Venus's `process_season`**, forcing Venus to look up Zeus's deity and thread it around. This is the precedent that metastasizes (next layer piggybacks Venus's loop). Cheap now (RuleSystem already collects communities); sets the "your concern runs in your orchestrator" rule while there are only two orchestrators.

## Tier 2 — Ownership hygiene (keeps single-writer real)

### 5. `CommunityCohesion` (Zeus-owned) is written by Venus
`FissionSystem.hpp:302` and `CommunityGenerator.hpp:69` both `.set<CommunityCohesion>({})`; same for `CarryingCapacity`. Benign today (zero-init), a real bug the moment founding cohesion ≠ 0 or a layer assumes "only Zeus touches this." **Fix:** route component *seeding* through the owning layer, or explicitly codify "creation-time zero-init is exempt from single-writer" in CLAUDE.md.

### 6. The family graph has three writers and no owner
`child_of` / `Parentage` / `MarriedTo` are mutated by Birth, Marriage, *and* Fission across two layers. When Mars (death/displacement) and Mercury (movement) arrive this becomes a 4-way contended write with no arbiter. **Name an owner now** (likely Zeus) and route the others through it.

### 7. The "two-capacities" trap — resolved in computation, live in the consumer
The old bug (CC computed two different ways) *is* resolved by the shared `CarryingCapacity{natural,resultant,overhang}` component. But the consumer choice is the live foot-gun: Fertility Restraint steers toward **resultant** CC, letting population grow into the cohesion-borrowed band — so when a succession erodes cohesion, the directive has *manufactured* the famine-exposed overhang it exists to prevent. **Fix:** make the setpoint target (natural vs resultant) explicit/configurable; record `overhang` in the trace. Goes from theoretical to real once cohesion is dynamic (the Zeus-directive plan).

## Tier 3 — One live bug + correctness traps

### 8. FissionSystem Option-3 defer trap — REAL BUG (confirm empirically before fixing)
New fission-*founded* communities are created via deferred `.set<>()` inside the orchestrator defer scope, then immediately read back: `get<GridPosition>` for plot assignment (`FissionSystem.hpp:412`) and `get_mut<FoodStores>` for the food transfer (`:445`, guarded by `source != target` — exactly the new-community case). Both return null (set still queued) → **new community gets no plot and zero carried food.** Same hazard ConsumptionSystem already solves with `defer_suspend/resume`. Systematically handicaps new communities, biasing the fade-out dynamics the Fertility Restraint sweep tuned against. **Fix:** `defer_suspend/resume` or compute locally before the deferred set.

### 9. Event IDs from file-static locals
Hand-partitioned ranges (1 / 100k / 200k / 10M), never reset between runs, collision-prone as layers add event types. **Fix:** world-scoped counter (singleton component).

### 10. Pairing determinism leans on Flecs table order
Singles/living ordering comes from `community.children()` traversal (archetype order), perturbed by marriage/fission reparenting. Deterministic within a run but fragile. **Fix:** sort by stable person id before order-sensitive pairing.

## Tier 4 — Export/viewer scaling (one root cause, four symptoms)

No single declarative definition of "a per-community time-series layer" shared across the C++ producer, the JSON contract, and the JS consumer:

- **11. `food_history` positional array** grew 3→5→7 columns on an array named "food," kept positional so old readers don't break. Migrate to named fields (or a `columns:[…]` header + positional rows) **now, while 3 readers exist** (ExportCommand, inspect.js, exponator), not at 7.
- **12. Viewer per-layer copy-paste** — paint loop, legend, toggle list, presence test are four parallel hand-synced lists. Replace with one `LAYER_SPECS` descriptor table; a layer becomes one row.
- **13. `DIRECTIVE_DESCRIPTIONS`** is directive prose duplicated C++→JS by hand (the JS comment admits it should be an exported catalog). Export the catalog now, at one directive.
- **14. Event-sourcing doctrine is quietly bending** — `fertility_modifier` is a *reconstruction* (re-derived at export, not the value that gated any roll); `cohesion` is a yearly sample of a season-varying sawtooth (aliasing). Add an explicit "sampled signal, non-authoritative" bucket; sample cohesion at season cadence if the viewer sawtooth claim is to be honest.

## Tier 5 — Tidy-ups (low risk, opportunistic)

- **Dead config:** `world_3region.json`'s `fission` block is silently ignored (WorldConfig has no `fission` member; glaze drops it). The cap is per-region and lives in `ecology.json` — the old "6 alive vs cap 3" mystery was a multi-region world, **not a bug.** Remove the dead block or add unknown-key validation.
- **JSON↔struct default drift:** `cap_base` 60 (C++) vs 40 (JSON) — a 50% difference in the food ceiling; fission thresholds 9↔11 and 12↔3. JSON wins at runtime so the shipped sim is fine, but any default-constructed config (tests, `inspect` without a config file) silently runs a different world. Generate JSON from struct defaults + a round-trip test.
- **Drought** is doc-drift (README + exponator CSV columns reference a mechanic that doesn't exist). Scrub it.
- **Founders'-marriages-on-fission** empty list is a deliberate design choice with a real per-family-event-feed gap — decide it before Narrative/War consume those feeds.
- Delete the dead `Simulation::process_tick` SENSE/DECIDE/RESOLVE stub (`DivineArbiter` is the actual, well-factored model-B nucleus).
- Marriage local/exogamous phases are ~80% duplicated; `too_closely_related` could memoize ancestor sets per pass.
- `World::register_components` is a manual list already drifted (`LeadershipHistory` and others work only via Flecs auto-registration) — make it exhaustive+tested or drop it.

## Recommended sequence

If nothing else: **1 (SimConfig), 2 (explicit ordering), 5/6 (ownership)** are the rules currently propped up by comments — cheapest now, most expensive to retrofit later. **3 (region index)** is the best perf/architecture two-for-one. **8** is the one live correctness bug. **11+12** is one refactor that defuses four compounding viewer problems.

Ordering chosen with Ryan: **#1 (centralized config) first**, then revisit the rest.
