# Magnus3 Architecture & Logic Assessment

**Date:** 2026-04-08
**Scope:** Full codebase review — architecture, logic correctness, scalability, and roadmap
**Codebase:** ~4,500 LOC C++ core + ~1,000 LOC JavaScript viewer, 24 commits

---

## 1. Architecture Assessment

### 1.1 Overall Verdict: Strong

The top-down rewrite landed on solid foundations:

- **ECS (Flecs v4)** gives us efficient entity storage, relationship graphs, and query-driven iteration without hand-rolling any of it.
- **Event-centric model** (everything-is-an-event with duration + causality) makes the simulation composable — new event types integrate automatically with genealogical tracing via `CausedBy`.
- **Deterministic seeding** (SplitMix64, pure functions of seed + parameters) means byte-identical worlds from the same seed regardless of evaluation order.
- **Config externalization** to JSON (ecology, world, ruler) keeps magic numbers out of code and makes tuning accessible without recompilation.
- **Header-only C++20** minimizes build complexity while keeping the dependency graph flat.

### 1.2 Maintainability

**Good, with one structural concern.**

The source tree is well-organized:

```
src/
  core/         — World wrapper, simulation loop, determinism, time constants
  components/   — POD-like Flecs component definitions
  config/       — Config structs with Glaze reflection
  generation/   — Deterministic generators (world, community, family, person, name)
  systems/      — Simulation systems (ecology)
  cli/          — CLI command implementations
```

The concern: **EcologySystem.hpp has grown to ~1,165 lines** and handles births, marriages, harvests, droughts, famines, fission, leadership selection, and population caching. Each of these is a logically distinct system that happens to run on the same seasonal cadence. This monolith is the first thing that should be split before adding new features (see Section 5).

### 1.3 Extensibility

**Excellent.** The event model was designed for this. Adding a new simulation mechanic (war, trade, migration, plague) follows a repeatable pattern:

1. Define new `EventType` variant
2. Create a new system file in `systems/`
3. Register a Flecs system that fires per-community per-season
4. Create events, modify components, add `CausedBy` links

New events automatically appear in the viewer's event tracks, in JSON exports, and in the causal graph. No existing code needs to change.

### 1.4 Scalability

**Good at current scale, with a known ceiling.**

- The **tick-skip optimization** (only calling `progress()` at season boundaries, not every tick) delivered a 2,800x speedup. A 1,000-year simulation completes in ~40ms.
- **Population caching** with next-death-tick invalidation avoids redundant entity scans.
- **O(1) marriage lookups** via the `MarriedTo` component replaced expensive event scanning.

The ceiling: everything runs single-threaded within one community's season processing. At the current scale (3 regions x 3 communities = 9 communities), this is not a bottleneck. At 100+ communities the per-season work becomes the constraint, and the current pattern of processing communities outside ECS iteration would make parallelization harder. This is not a problem to solve now, but it's worth keeping in mind as world size grows.

**Performance breakdown (profiled):**
- 22% Flecs framework overhead (`progress()` calls)
- 78% ecology logic (births, marriages, harvests, famine, fission)
- ~7.5 us/season/community for ecology logic
- ~2.2 us per `progress()` call

---

## 2. Bugs & Logic Errors

### 2.1 CRITICAL: Seven independent event ID generators

**Locations:**
- `WorldGenerator.hpp:135, 178`
- `PersonGenerator.hpp:188`
- `World.hpp:192`
- `EcologySystem.hpp:699, 1018, 1139`

Each location declares its own `static uint64_t next_event_id = 1;`. These counters are completely independent, meaning event IDs **will collide** across generators. Marriage event #5, person life event #5, and harvest event #5 can all coexist. Any query or lookup by event ID will return wrong results.

**Fix:** Consolidate to a single event ID generator owned by the World/ECS wrapper. Pass it by reference to all generators and systems.

### 2.2 HIGH: Child seed doesn't encode parent identity

**Location:** `EcologySystem.hpp:566-567`

```cpp
uint64_t child_seed = combine_seeds(
    ecology_seed(world_seed), tick, cid.slot, birth_index);
```

The seed is `hash(ecology_seed, tick, community_slot, birth_index)`. Since `birth_index` is sequential across the community, seeds are technically unique within a single run. However, the seed doesn't encode *which parents* produced the child. If community composition changes (different config, different couples end up in the same slot), you get the same child seed from different parents. This is fragile.

**Fix:** Include at least one parent's entity ID or seed in the hash:
```cpp
uint64_t child_seed = combine_seeds(
    ecology_seed(world_seed), tick, cid.slot, parent1_seed, birth_index);
```

### 2.3 HIGH: No incest prevention in marriage pairing

**Location:** `EcologySystem.hpp:670-683`

Singles are shuffled deterministically and paired adjacently. There is no kinship check. Over 1,000 years with small communities of ~12-40 people, sibling and parent-child marriages will inevitably occur.

**Fix options (increasing sophistication):**
1. **Minimum:** Reject pairs that share a `BirthFamily` (prevents sibling marriage)
2. **Better:** Walk `CausedBy` links up to depth N, reject pairs with a common ancestor within N generations
3. **Configurable:** Add `min_kinship_distance` to marriage config (e.g., 3 = no marriages closer than 2nd cousin)

### 2.4 HIGH: Events (drought, famine) don't cause mortality

**Locations:** `EcologySystem.hpp:506-625` (drought), `759-791` (famine)

Drought and famine events are created with severity values but never modify anyone's lifespan or cause deaths. Lifespans are fixed at person generation time (50-80 years, health-modified). This means:

- Population grows monotonically unless births are suppressed by food scarcity
- No famine-driven population crashes (a defining feature of pre-industrial demographics)
- Severity is calculated but has no gameplay consequence

**Fix:** Introduce a mortality system that:
- Applies famine severity as a death chance per person per season
- Targets the oldest and youngest first (historically accurate)
- Shortens remaining lifespan rather than instant-killing (more gradual)

### 2.5 MEDIUM: No infant/child mortality

**Location:** `PersonGenerator.hpp:162-178`

Lifespan is drawn from a uniform distribution [50, 80] years. The minimum floor is 10 years. Historical pre-industrial populations had ~30-40% mortality before age 5. The absence of this creates:

- Unrealistically top-heavy age distributions
- Steady population growth rather than the high-birth/high-death equilibrium of real pre-industrial societies
- Missing a major source of population dynamics and emotional weight

**Fix:** Add age-stratified mortality:
- Year 0-1: ~15% mortality
- Year 1-5: ~15% mortality
- Year 5-15: ~5% mortality
- Survivors: original [50, 80] distribution applies

These rates should be configurable in `ecology.json`.

### 2.6 LOW: Stale `MarriedTo` components on dead spouses

**Location:** `EcologySystem.hpp:248-254`

When a spouse dies, the surviving partner's `MarriedTo` component still points to the dead entity. The `get_spouse()` function handles this correctly (returns null if spouse is dead at current tick), so this doesn't cause logic errors. However:

- Wastes memory at scale
- Could confuse future systems that check `MarriedTo` without also checking liveliness

**Note:** This was a deliberate decision — dead people's marriages should remain visible in the viewer. The current approach is fine as long as all code paths use `get_spouse()` rather than reading `MarriedTo` directly.

### 2.7 LOW: O(n) linear scans in fission spouse collection

**Location:** `EcologySystem.hpp:1058-1059`

When collecting movers during fission, spouse deduplication uses a vector linear scan:
```cpp
for (auto& m : movers) {
    if (m == spouse) { already_moving = true; break; }
}
```

At current family sizes (9-11 people), this is negligible. Would become noticeable only if fission thresholds were raised dramatically.

---

## 3. Data Plausibility

### 3.1 Birth rate: Plausible

The 7% chance per married couple per spring produces ~1.75 births per spring for a community with ~25 couples, or ~7 births/year. For a community of 40-100 people, that's a crude birth rate of ~70-175 per 1,000 — on the high side but within range for a food-surplus pre-industrial society. The food threshold (15 grain/person) acts as a natural brake.

### 3.2 Lifespan distribution: Unrealistic

Uniform [50, 80] is not how human lifespans distribute. Real populations show:
- High infant mortality spike
- Low mortality plateau in young adulthood
- Gradually increasing mortality in middle and old age (Gompertz curve)

The uniform distribution means someone is equally likely to die at 51 as at 79. A simple improvement would be a normal distribution centered around 65 with sigma ~10, plus the infant mortality overlay from Section 2.5.

### 3.3 Marriage age: Acceptable simplification

A flat minimum of 16 for all genders is ahistorical (medieval norms were ~12F/14M) but is a reasonable simplification. Gender-differentiated marriage age could be added later if needed.

### 3.4 Fission triggers: Personality-driven, not economic

Fission occurs when family size exceeds a threshold (default 9), modified by agreeableness/stability. Historical fission was usually driven by land pressure or economic viability, not family harmony. The personality-driven model is speculative but creates interesting emergent behavior (agreeable families stay together longer, producing larger power bases). Worth keeping as-is but potentially supplementing with economic triggers.

### 3.5 Weather/ecology: Functional but one-dimensional

Currently: drought (10% summer), good rain (15% spring), base harvest (150 grain). No floods, plagues, crop disease, locust swarms, or other disaster types. The system is correct for what it models but the event variety is thin.

---

## 4. Feature Roadmap

Ordered by impact and how naturally they fit the existing architecture.

### Tier 1: Fix and Harden (prerequisites for everything else)

| Item | Effort | Description |
|------|--------|-------------|
| Consolidate event IDs | Small | Single generator in World, passed to all systems |
| Harden child seeds | Small | Include parent seed in child seed hash |
| Famine mortality | Small | Apply famine severity as death chance. Severity is already computed |
| Infant mortality | Small | Age-stratified death rates in first 5 years |
| Kinship-aware marriage | Medium | BirthFamily check minimum, CausedBy-walk for deeper kinship |

### Tier 2: Deepen Existing Systems

| Item | Effort | Description |
|------|--------|-------------|
| Lifespan distribution | Small | Replace uniform with normal + infant overlay |
| Disaster variety | Small-Medium | Plague, flood, crop blight as new weather event types |
| Remarriage rules | Small | Configurable mourning period, age-dependent remarriage chance |
| Economic fission triggers | Medium | Fission based on land/food pressure, not just family size |
| Age-dependent fertility | Small | Fertility window (e.g., 16-40) instead of flat rate for all adults |

### Tier 3: New Systems

| Item | Effort | Description |
|------|--------|-------------|
| Inter-community migration | Medium | Families that fission with no room move to neighboring communities |
| Trade/resource sharing | Medium | Communities exchange surplus. Creates interdependence and trade routes |
| Professions/roles | Medium | Farmer, craftsman, priest, warrior. Modifies harvest, events, social standing |
| War/raiding | Medium-High | Community-level conflict driven by scarcity. Causes casualties, resource transfer |
| Cultural drift | High | Name patterns, marriage rules, beliefs evolve independently per community over centuries |
| Multi-region interaction | High | Regions are currently isolated. Connecting them opens diplomacy, alliances, cultural exchange |

### Tier 4: Presentation & Tooling

| Item | Effort | Description |
|------|--------|-------------|
| Test suite (Catch2) | Medium | Unit tests for determinism invariants, edge cases, statistical distributions |
| Viewer: family tree mode | Medium | Dedicated genealogy view (tree layout vs. timeline) |
| Viewer: map mode | High | Spatial view of regions, communities, migration paths |
| Narrative generation | High | Natural-language summaries of notable lives, events, dynasties |

---

## 5. Keeping It Organized

### 5.1 Split EcologySystem before adding features

The current `EcologySystem.hpp` (~1,165 lines) should be decomposed into focused system files:

```
systems/
  PopulationCache.hpp     — Living cache, snapshot building, invalidation
  BirthSystem.hpp         — Birth processing, child generation, trait inheritance
  MarriageSystem.hpp      — Pairing, family transfer, kinship checks
  HarvestSystem.hpp       — Harvest calculation, weather effects, leader bonuses
  FamineSystem.hpp        — Deficit calculation, severity, (future) mortality
  FissionSystem.hpp       — Family splitting, community founding, personality-driven thresholds
  LeadershipSystem.hpp    — Leader selection, caching, recomputation on death
  MortalitySystem.hpp     — (New) Natural death, famine death, infant mortality
  WeatherSystem.hpp       — Drought, rain, (future) floods/plagues
```

Each system:
- Lives in its own file, stays under ~300 lines
- Registers its own Flecs system
- Shares `PopulationSnapshot` and `FoodStores` via components
- Fires per-community per-season on the existing seasonal cadence

This is a pure refactor — no behavior changes, just file boundaries.

### 5.2 New features follow the same pattern

Every new mechanic (war, trade, migration) becomes:
1. A new system file in `systems/`
2. New component(s) in `components/` if needed
3. New config struct + JSON section if tunable
4. New `EventType` variant for its events

The event model, causal graph, and viewer integration come for free.

### 5.3 Consolidate shared utilities

Some patterns are duplicated across systems:
- Event ID generation (7 separate counters — consolidate to World)
- `deterministic_chance()` and `combine_seeds()` — already in `Determinism.hpp`, good
- Population snapshot building — extract to `PopulationCache.hpp`
- Family/community lifespan updates — could move to a shared utility

---

## 6. Current State Summary

**What's working well:**
- Deterministic 1,000-year genealogies in ~40ms
- Complete causal graph from Creator deity down to individual births
- Personality-driven emergent culture (families develop distinct trait profiles over generations)
- Interactive timeline viewer with relationship highlighting
- Clean config externalization — all tuning in JSON

**What needs attention before expanding:**
- Event ID collision (critical bug)
- No death from hardship (population only grows or plateaus, never crashes)
- No kinship checks (incest in small communities)
- EcologySystem monolith (maintainability ceiling)

**What's deferred but healthy to defer:**
- Multi-threading (not needed at current scale)
- Test suite (deferred pending feature stability — reasonable)
- Larger world sizes (architecture supports it, just not exercised yet)
