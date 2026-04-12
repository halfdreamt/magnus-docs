# Population Dynamics Under Parameter Sweeps

**Date:** 2026-04-12
**Tool:** `Magnus3/tools/exponator/exponator.py`
**Sim version:** commit `b88e0aa` (ecology cleanup + family tenure + incest tolerance)

## Headline findings

| Dial | Range tested | Effect on mean pop | Verdict |
|---|---|---|---|
| `harvest.base_yield` | 175 → 300 | 55 → 121 | **Highest leverage.** Nearly linear. |
| `birth.chance_per_adult_per_spring` | 0.10 → 0.20 | 68 → 76 | **Weak.** Food threshold gates births; birth rate alone is saturated. |
| `drought.chance_per_summer` | 0.05 → 0.30 | 78 → 54 | **Moderate.** Linear until 0.30, where community deaths begin. |
| `marriage.min_unrelated_generations` | 0 → 3 | 71 → 60 | **Cliff at 3.** 0/1/2 equivalent; 3 causes collapse. |
| `marriage.enable_exogamous` | on / off | 71 → 71 | **Surprisingly neutral** for population but not for community churn. |

Full aggregate table in `tools/exponator/runs/*/summary.csv`.

## Baseline

10 seeds × 1000y at default config:

- **Mean population: 71 ± 2** (across-run average population across food history snapshots)
- Peak pop: 128 ± 17 (varies a lot)
- Final pop: 66 ± 17
- **Year of peak: 366 ± 372** — the system is oscillatory, not monotonic. Peaks happen at random points across the run.
- Living communities at Y1000: 2.9 / 3.0 (1 seed lost a community)
- **60% of marriages are exogamous** — a much larger share than expected
- **Zero community-level fissions** across all 10 seeds — current tuning never produces families large enough to trigger community fission
- ~1100 births / ~1100 deaths / ~1150 marriages per run — throughput is stable across seeds
- ~34 generations deep over 1000 years → ~29-year generational cadence

## Experiment 1 — Harvest yield sweep

| `base_yield` | mean pop | peak | alive/total |
|---|---|---|---|
| 175 | 54.7 | 102 | 2.8/3.0 |
| 200 | 60.2 | 121 | 2.6/3.0 |
| **225** (default) | **71.2** | **129** | **3.0/3.0** |
| 250 | 85.6 | 157 | 3.4/3.4 |
| 275 | 96.3 | 194 | 3.6/3.6 |
| 300 | 120.7 | 220 | 4.4/4.4 |

**Interpretation.** `base_yield` is the single most effective dial. Scaling 175 → 300 (71% increase) produces 55 → 121 mean pop (2.2× increase). Above 250, the system produces enough surplus for community fission to start firing (reflected in total communities climbing above 3.0), which is why we see 3.4–4.4 communities created. Below 225 the system is population-constrained; above 225 it's bounded by structural caps (`max_families_per_community`, fission thresholds).

## Experiment 2 — Birth chance sweep

| `chance_per_adult_per_spring` | mean pop | peak |
|---|---|---|
| 0.10 | 68.4 | 137 |
| 0.12 | 68.0 | 129 |
| **0.15** (default) | **71.2** | **129** |
| 0.18 | 72.8 | 134 |
| 0.20 | 76.2 | 149 |

**Interpretation.** Surprisingly flat. A 2× increase in birth chance produces only ~12% more mean population. The `food_threshold_per_person` ramp in `BirthSystem` caps actual births at the food ceiling regardless of nominal chance — so cranking birth rate without also raising yield doesn't move the needle. Birth chance is a knob for *speed* of reaching equilibrium, not for the equilibrium itself.

## Experiment 3 — Drought chance sweep

| `chance_per_summer` | mean pop | alive/total | extinctions (of 5 seeds) |
|---|---|---|---|
| 0.05 | 77.5 | 3.2/3.4 | 0 |
| **0.10** (default) | **71.2** | **3.0/3.0** | 0 |
| 0.15 | 67.4 | 3.0/3.0 | 0 |
| 0.20 | 65.4 | 3.0/3.2 | 0 |
| 0.30 | 54.1 | 2.6/3.0 | 2 communities lost |

**Interpretation.** Drought is roughly a linear depressant in the 0.05–0.20 range. At 0.30 (one-in-three summers), volatility converts into extinction risk — 2 of 5 seeds lost a community and one seed's population fell to 31. Below 0.20, exogamous marriage rescues struggling communities before they collapse.

## Experiment 4 — Exogamous marriage on vs off

| Config | mean pop | peak | alive/total | cross-comm % |
|---|---|---|---|---|
| Default (exogamy on) | 71.0 | 128 | 2.9/3.0 | 60% |
| `enable_exogamous: false` | 70.9 | 160 | 2.8/3.7 | 4% |

**Interpretation.** The equilibrium population is essentially unchanged (71 vs 70.9). What changes dramatically is **community churn**: disabling exogamy raises total communities over the run from 3.0 to 3.7 while dropping the alive count slightly — so communities are dying *and being replaced* more often. With exogamy, struggling communities get outside marriages to save them; without it, they go extinct and new ones form via fission. Peak pop is actually 25% higher (160 vs 128) without exogamy — isolated communities grow to their local ceiling before collapsing. The 4% cross-community marriages that still occur come from family fission moving people between communities, not from the exogamous-phase pairing.

## Experiment 5 — Incest tolerance sweep

| `min_unrelated_generations` | mean pop | peak | final | alive/total | cross-comm % |
|---|---|---|---|---|---|
| 0 (siblings allowed) | 71.2 | 141 | 78 | 3.0/3.0 | 56% |
| **1** (default — no siblings) | 71.2 | 129 | 72 | 3.0/3.0 | 60% |
| 2 (no first cousins) | 71.9 | 136 | 70 | 3.0/3.0 | 67% |
| 3 (no second cousins) | **60.5** | 116 | **23** | **1.2/3.0** | 74% |

**Interpretation.** Levels 0–2 are essentially equivalent — the system easily finds viable partners within the 2-generation window. Level 3 is catastrophic: **3 of 5 seeds collapsed to 1–2 alive people by year 1000.** In small regional populations (~70 people across 3 communities), everyone becomes related within 3 generations after a few decades. The exogamous-marriage percentage climbs as restriction tightens (56 → 74%), meaning the system tries harder to find unrelated partners, but at level 3 it simply runs out.

**Design implication.** Our default of `min_unrelated_generations = 1` is the right choice. Level 2 is viable if you want a "strict" cultural variant. Level 3 requires much larger populations (more regions or bigger communities) to avoid demographic collapse.

## Answers to the pre-planned questions

**1. What IS the current steady state?**
71 ± 2 people per region (3 communities), ~60% of marriages exogamous, 0 community-level fissions. Stable across 10 seeds.

**2. Which dials are most sensitive / knife-edged?**
Most sensitive: `base_yield` (linear scaling of carrying capacity). Most knife-edged: `min_unrelated_generations` (invisible until 3, then collapse). Moderate: `drought.chance` above 0.20, `max_communities_per_region` if it's ever reached.

**3. What's carrying capacity per tract?**
Observed ~24 people per community at default. Math: `base_yield × fertility × avg_rainfall / consumption = 225 × 1.0 × 1.0 / 3 = 75` grain-equivalents of consumption capacity, supporting ~25 people. Observation matches theory within 4%.

**4. Does exogamous marriage save struggling communities?**
Yes, but not by increasing population — by reducing community churn. With exogamy on, 2.9/3.0 communities stay alive; without, 2.8/3.7 communities cycle through births and deaths.

**5. How deterministic is shape across seeds?**
Peak *timing* varies enormously (stddev 372 years). Peak *magnitude* varies moderately (stddev ~17). Mean pop over the run is the most stable metric (stddev 2 on baseline). For cross-config comparison, use `mean_population`.

**6. Performance floor?**
~270 ms per 1000-year run at default (1 region, 3 communities, ~70 pop). At `yield-300` (4.4 communities, ~120 pop) runs take similar time — the engine is not population-bound at this scale. Batch sweeps of ~30 configs × 5 seeds finish in 40 seconds.

## Candidate "shape" experiments worth running next

With baseline established, the interesting next step is *time-varying* configs:

1. **Golden age** — step yield from 225 → 300 at Y200, revert at Y400. Expect pop surge, then famine wave post-revert.
2. **Climate decay** — decay yield linearly 250 → 175 over 1000 years. Model gradual territorial abandonment.
3. **Plague** — one-off mortality at Y500 killing 40% of each community. Compare recovery times.
4. **Strict era** — start at `incest-1`, transition to `incest-3` at Y300. Observe collapse dynamics.
5. **Malthusian ceiling** — fix `max_communities_per_region = 3` and crank yield to 300. Watch population plateau and volatility rise.

Running these requires either the simulation supporting per-tick config changes or running separate sims and stitching together — both meaningful design choices worth discussing before implementation.

## Notable gaps / questions for the next pass

- **Community-level fission never fires at any tested config.** Either the threshold is mistuned or the mechanic is effectively dead code in the current parameter space. Worth investigating.
- **Year-of-peak variance is huge** (372 year stddev). Understanding what causes a seed to peak at Y90 vs Y964 would illuminate the underlying oscillation dynamics.
- **Famine severity ~0.3–0.4** across all configs — suspiciously narrow. Need to check whether the severity calculation is actually coupled to food state or is mostly cosmetic (the 4/8 review flagged this).
- **`cross_community_marriages` metric relies on birth-family community.** After family fission, someone's "birth family" may have moved; this is a proxy, not exact. Should be fine for aggregate signal.
