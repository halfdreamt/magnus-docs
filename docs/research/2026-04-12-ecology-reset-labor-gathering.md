# Ecology Reset — Labor + Gathering Model

**Date:** 2026-04-12
**Status:** Design proposal, pending implementation
**Supersedes:** current `HarvestSystem.hpp`, `FamineSystem.hpp`, and drought paths in `WeatherSystem.hpp`

## Background

Reviewed the current harvest/drought/famine pipeline end-to-end. Findings:

- **Famine is cosmetic.** `FamineParams.severity` is computed, stored, and exported, but no downstream system reads it. Nobody dies from famine; droughts only suppress births via the food-per-person threshold.
- **`drought_resilience` leader modifier is dead code.** Computed in `LeadershipSystem.hpp`, never applied anywhere except the inspect printout.
- **Food stores are floored at 0 after any deficit.** Multi-year granary reserves are impossible.
- **Spatial hierarchy (Tract/Plot/Area) is decorative for yield.** Harvest reads a flat regional `soil_fertility`; the per-tract fertility values drive settlement choice but never food output.
- **Grain assumption is baked in everywhere.** Single yield event per autumn, name `FoodStores.grain`, fixed `base_yield` independent of population or location.

The current system is effectively a placeholder. Rather than incrementally patching, we're doing a full reset to a simpler and more extensible model.

## Goals

1. Generalize food — no grain-specific assumption; communities can eventually have different food sources based on biome/area.
2. Couple food production to population through a labor abstraction.
3. Use the spatial hierarchy (tract/area/region) as actual yield inputs.
4. Start minimal: drought and famine removed, to be reintroduced after the new base works.

## Design

### Food abstraction

- Rename `FoodStores.grain` → `FoodStores.food`.
- Single value, no food variants yet.

### Community labor

- `labor = count of living members` in a community.
- Simplest possible — no age weights, personality modifiers, or role distinctions yet.
- Sourced from existing `PopulationSnapshot.alive`; no new stored state.
- Future extensions: exclude children/seniors, weight by health/traits.

### Gathering event (new default food source)

Fires every season, not just autumn. Duration-bounded (one season each), remains queryable in the event stream.

Per-community per-season formula:

```
yield = min(labor × efficiency, tract_cap × area_mod × region_mod) × variance
```

- **Labor-bound regime** (small community): `labor × efficiency < tract_cap × mods` → yield scales with population.
- **Tract-bound regime** (large community): yield plateaus at tract capacity — this is carrying capacity.
- Home tract only for v1. Foraging-radius / adjacent-tract gathering deferred.

### Tract gathering cap

- New `gathering_cap` field on the `Tract` struct.
- Base value set at generation from area type (Forest/Meadow high, Bog/Cliff low), with random jitter.
- Region biome provides a multiplier (Woodland favors gathering, Highland penalizes it).

### Consumption

- Per-season: `pop × food_per_person_per_season` each season.
- Was: all annual consumption debited in winter as a lump.
- Per-season matches the gathering cadence and makes the food curve readable within the year. Sets up for mid-year famine dynamics later.

### Removed (hard delete)

- `FamineSystem.hpp` and all callers
- `WeatherSystem.hpp` summer drought branch (spring rain/recovery also removed for now — no rainfall system at all in v1)
- `DroughtParams`, `FamineParams`, `WeatherParams` structs
- `EventType::Drought`, `EventType::Famine`, `EventType::Weather` enum values
- `drought_resilience` field on `LeaderModifiers` + its config entry
- `famine_reduction` field on `LeaderModifiers` + its config entry (famine is gone)
- `HarvestSystem.hpp` — replaced by `GatheringSystem.hpp`
- `RegionEcology.rainfall`, `.drought_active`, `.drought_start_tick`, `.drought_end_tick`
- `harvest` and `drought` sections in `ecology.json`

### Kept

- Seasonal cadence (Spring/Summer/Autumn/Winter per-community per-season firing)
- Graduated birth threshold
- Leader harvest bonus, **renamed** `harvest_bonus` → `gathering_bonus`. Still driven by conscientiousness.
- Exogamy, marriage, fission, fertility-based settlement
- All spatial hierarchy (Region/Tract/Plot/Area) — now actually used

## Starting parameters

```json
{
  "gathering": {
    "efficiency": 3.5,
    "variance_min": 0.8,
    "variance_max": 1.2
  },
  "tract": {
    "cap_base": 60
  },
  "area_modifiers": {
    "Forest": 1.3, "Grove": 1.2, "Meadow": 1.2,
    "Field": 1.1, "Valley": 1.0,
    "Ridge": 0.8, "Bog": 0.6, "Cliff": 0.5
  },
  "region_modifiers": {
    "Grassland": 1.0, "Woodland": 1.2,
    "Wetland": 1.1, "Highland": 0.8
  },
  "consumption": {
    "food_per_person_per_season": 3
  }
}
```

### Equilibrium sketch (neutral tract, Grassland)

- `tract_cap × area_mod × region_mod = 60 × 1.0 × 1.0 = 60` food/season
- Consumption per person: 3/season
- Carrying capacity ≈ 60 / 3 = 20 people (tract-bound)
- Below ~17 people: labor-bound, `yield = labor × 3.5`. A 10-person community produces 35/season, consumes 30 → slight surplus drives growth.
- Rich area (Forest, Woodland): cap = 60 × 1.3 × 1.2 ≈ 94/season → ~31 people carrying capacity.
- Poor area (Bog, Highland): cap = 60 × 0.6 × 0.8 ≈ 29/season → ~9 people.

Numbers are a starting point. All live in `ecology.json`; tuning is a JSON edit.

## Open questions (not blocking implementation)

1. Labor weighting by age (exclude children and seniors, weight by health). Deferred until base system is stable.
2. Gathering from adjacent tracts — foraging radius. Deferred; interacts with territory/migration design.
3. Food source strategies — Gatherer vs Farmer vs Herder vs Fisher, tied to biome. Grain farming reintroduced here as a specialized alternative. Deferred.
4. Reintroducing drought and famine, now as labor-disrupting events rather than just yield multipliers. Deferred.
5. Mortality from starvation — currently no path from low food to death. Will be part of the famine reintroduction.

## Implementation approach

1. Remove deleted systems + types + config entries (one commit).
2. Rename `FoodStores.grain` → `FoodStores.food`; add `Tract.gathering_cap`; add area/region modifiers to config (one commit).
3. Add `GatheringSystem.hpp`; wire into `EcologySystem.hpp` to fire per-season. Update `LeaderModifiers` (one commit).
4. Switch consumption to per-season (one commit).
5. First 1000y run — compare community counts and mean population against current `baseline` in the exponator. Tune if obviously broken.
