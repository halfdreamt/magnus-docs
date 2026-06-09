# Per-Family Food Stocks — The Invention of Private Property

**Date:** 2026-06-06
**Status:** Design agreed — ready to plan implementation
**Related:** authority-weighted distribution / Phase B (`docs/logs/2026-06-01.md`, Thu 06/04), Mercury invention model / agriculture (`docs/logs/2026-06-01.md`, Fri 06/05), pre-expansion review #7 setpoint + #8 fission defer bug (`2026-06-01-pre-expansion-technical-review.md`), DDA directive pattern (`Magnus3/CLAUDE.md`)

## Why this exists

This came out of reworking emigration/fission. Founding a new community should require a **resource stake** — so the poor can't muster it and the rich can, producing class-sorted movement. But reviewing the code revealed there is **no per-family resource to gate on**: food lives in one community-level `FoodStores` pool, and the authority-weighted distribution (Phase B) is a *consumption-time triage* with **no memory** — it only decides who eats first during a famine. The rich never accumulate; standing is recomputed each season. That is exactly why persistent class lineages never emerged (the Phase-B caveat).

The fix is to make **food a per-family stock** — an analog to wealth. Disparity moves from "access to a shared pool" to **family income**, and surplus **accumulates** per family. That single change makes class real and heritable, gives founding a real cost, and (via spoilage) generates the *motive* to found. It is the substrate the movement rework needs.

> Scope note: this doc designs the **wealth substrate only**. The consumer feature — crowding-triggered emigration + resource-gated founding + the spatial cost tiers — is the next plan. This unblocks it.

## The model

Disparity lives in **income**; **eating is need-capped**; the difference **banks as family wealth**. One rank-weighted income rule yields both the "egalitarian good times" and "class-stratified bad times" behavior automatically, depending only on harvest size.

1. **Production (unchanged):** `yield = min(community_pop · efficiency, tract.yield_cap · (1 + cohesion_bonus)) · variance`. Total community yield is still community-pop × tract-driven; this design does **not** change how much food exists, only who owns it.
2. **Income split (relocated disparity):** the season's yield is divided into **family incomes**, weighted by family **standing** (= max member authority rank), using the **existing `disparity_steepness` knob** — water-fill toward each family's size-based need (`count · need`) in rank-priority order, blended back toward the egalitarian per-capita share by `(1 − steepness)`. Identical math to today's `ConsumptionSystem` water-fill; only the *location* (production-time, into per-family stocks) and the *persistence* (it banks) change.
   - `steepness = 0` ⇒ egalitarian per-capita income ⇒ regression-safe baseline.
3. **Consumption:** each family eats `need` per living member **from its own stock** (income + carried bank). Surplus **banks**; a deficit draws the bank down, then the family starves.
4. **Spoilage (unchanged mechanism, now per-family):** stocks expire FIFO by shelf-life, per family.

### What emerges (the point)

- **Egalitarian good times.** When the harvest is large, even low-rank families' income clears `need` → everyone eats → the table *looks* egalitarian. The rich simply bank more. Class diverges in **wealth**, not in meals.
- **Class-stratified bad times.** The same rank-weighting pushes low-rank income below `need` in a poor harvest → the underclass starves first. Now with **memory**: a lineage that has been poor for generations has no buffer.
- **Buffers amplify class beyond income.** A deep granary smooths variance; the poor have no shock absorber, so every below-mean variance draw tips them into starvation. The poor are hit twice — lower income *and* fragile. Emergent, not coded.
- **Spoilage brakes hoarding and creates the founding motive.** A rich granary rots at the top faster than it is eaten → a natural ceiling on accumulation → surplus the rich *can't store and can't eat* → the obvious use is to **carry it away and found a new community.** The founding stake becomes the natural sink for un-storable surplus: rank → income → surplus → (spoilage caps it) → invest in expansion.
- **"Can't take food others need" is enforced for free.** You carry *your own* granary; leaving starves no one. Surplus-only emigration falls out automatically (under the old pool, leaving with provisions stole from those who stayed).

## Decisions settled

- **Income weighting:** size-based need (headcount) as the base, **rank as the tilt**, via the existing `disparity_steepness`. Everyone eats — *not* "only laborers are fed" (that is a separate, deferred deal-with-the-devil).
- **Food = wealth** for now. A separate currency (gold) may come later; food works.
- **Dead family → granary splits evenly** among the community's remaining living families.
- **Famine stays a per-community event**, for the same cleanliness reason it was moved off per-individual. Affected people group **by family** (which emerges naturally from per-family starvation); we tag the grouping explicitly. `FamineParams.distribution` already records per-family rations, so the viewer is half-ready.
- **Single-writer / determinism intact:** food stays Venus-owned (relocated community → family); rank stays Zeus-owned and read-only to Venus. The split is deterministic arithmetic.

## Shipped as a Mercury invention (toggleable mid-run)

This is **the invention of private property / storage** — the cleanest deal-with-the-devil yet. Like agriculture, it is a `WorldTech` overlay flag flipped at a trigger by `MercurySystem`, with **both food models living behind the flag**:

- **Before (pooled):** communal `FoodStores`, no class, surplus rots communally, no wealth-driven expansion. (This is also the future "Robin Hood fully on" end state — so the pooled path is not dead weight.)
- **After (private):** family granaries, class crystallizes, the poor die in famines the rich sail through — **but** the society can accumulate, expand, and found new communities on stored wealth.

Flip it at year N and watch class emerge and mortality stratify in the viewer. Blessing and curse in one switch: privatization buys growth and expansion at the price of class and crueler famine.

## Implementation surface (to detail in the impl plan)

- **Components:** move/duplicate `FoodStores` to the **family** level (Venus-owned). Decide whether the community keeps a transient/zero pool or none under the private model.
- **GatheringSystem:** still computes total community yield; a new step splits it into family incomes (the relocated water-fill) and deposits into family stocks.
- **ConsumptionSystem:** each family eats from its own stock; per-family starvation; famine event stays per-community, aggregating family outcomes.
- **Spoilage:** per-family `expire_food`.
- **Fission/founding:** a splitting family carries **its own bank** (no proportional community split) — this *simplifies* fission and makes the **Option-3 defer bug largely evaporate** (the buggy `get_mut<FoodStores>` proportional transfer goes away; plot reads are already statistically inert).
- **WorldTech / MercuryConfig:** new overlay flag (e.g. `private_stores`) + trigger; `cohesion_bonus_scale_mult`/agriculture precedent to follow.
- **Export/viewer:** family stock surfaced in the inspector; famine casualties grouped by family.

## Open / deferred

- **Zeus "Robin Hood" redistribution lever** — a future DDA directive that taxes granaries to feed the starving (turns the cruelty back off). This design deliberately leaves its *absence* visible.
- **Founding stake threshold** and the **crowding-trigger / spatial-cost** mechanics — the next plan (this doc's consumer).
- **Labor-eligibility** ("only workers are fed") — a separate later deal-with-the-devil.
- **Inheritance vs even-split nuance** if a family fissions (the splitting family carries a share of the bank — split rule to confirm in impl).
- **Gold / separate currency** — later.

## Validation

- **Regression:** `steepness = 0` and the invention **off** must reproduce current behavior (byte-identical where the pooled path is unchanged).
- **Behavior shift:** removing communal smoothing will raise deaths and move the population equilibrium — **A/B with the exponator** before choosing defaults; confirm class wealth diverges and famine mortality stratifies by family lineage (the Phase-B signal, now with persistence).
- **Determinism:** two-run byte-identical with the invention on.
