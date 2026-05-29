# Divine Determinism — Randomness as a Divine Lever

**Date:** 2026-05-28
**Status:** Design discussion — model agreed, not yet implemented
**Related:** intent/receipt bus (model B, `Simulation.hpp::process_tick` + `Magnus3/CLAUDE.md`), per-woman fertility rewrite (`docs/logs/2026-05-25.md`, Tue), planned drought reintroduction (`2026-04-12-ecology-reset-labor-gathering.md`)

## Premise

All randomness in the simulation is pseudo-randomness seeded from the world seed — so at the level of the application it is already fully deterministic. The proposal: make that fact *diegetic*. Every contingent (in-world "could-have-gone-otherwise") outcome is routed through a divine entity, which becomes both the **arbiter** of the outcome and its **causal source** in the graph.

"Venus has blessed us with a child" stops being lore and becomes a literal edge in the causality graph.

## Two separable ideas

The proposal bundles two moves that are worth keeping distinct, because they deliver different benefits and can ship independently:

1. **Causal/narrative routing.** Every stochastic outcome gets a `CausedBy: deity` edge. Almost free — a tagging change. Can be done without altering any math (keep the current per-pair roll, just attribute the result).
2. **Centralized arbitration.** Instead of each entity independently rolling its own die, entities *apply* (emit an intent) and a single arbiter grants outcomes per an exact rule. This is where precise tuning lives, and it is a genuinely different mechanism.

Flavor benefit comes from (1). Tuning benefit comes from (2). Choose the dose; you don't have to take both at once.

## The real prize: authoring the distribution

"Enforce exactly 15%" undersells centralized arbitration. Independent per-pair Bernoulli rolls give you a fixed *mean*, an *uncontrollable variance*, and *zero correlation* between entities. A central arbiter lets you author all three:

- **Mean** — exact. N eligible applicants × 15% → grant `ceil(0.15·N)`. Because it's a fraction *of applicants*, total births still track population — it is an exact *rate*, not a fixed budget.
- **Variance** — a per-stream dial: `0` = perfectly even (quota), nonzero = authored boom/bust years. Variance becomes something you set, not something the math imposes on you.
- **Correlation** — impossible with independent rolls. A drought rolls *once for a region* and communities draw correlated outcomes (one drought, not 12 independent coin flips). Same machinery enables baby booms (correlated) or birth-spacing (anti-correlated).

The prize is moving from "tune one input and accept whatever distribution falls out" to "author the distribution directly — mean, spread, and spatial/temporal correlation — from one place."

## The deity as a maximally-informed decision function

A deity should be **omniscient in its reads** and **narrow in its writes**:

- **Awareness (reads):** unrestricted. Venus sees diet, age, nutrition, community history — every factor bearing on the choice. More information = better divine decision.
- **Authority (writes):** only its own domain's outcome. Venus writes *who is born*; she does not compute the diet curve or the age window — those are handed to her.

This is the existing **single-writer** principle (which only ever governed writes). It is what keeps a deity from becoming a "god-object": not ignorance, but being *purely a decider* — sees all, decides one kind of thing.

## What is and isn't divine — the determinism taxonomy

Two levels of determinism:

- **Extra-diegetic:** the whole app is a pure function of the seed. Nothing is truly random here; even divine "rolls" are seeded. This is the determinism invariant and never goes away.
- **Diegetic (in-world):** some things are *contingent* (could have gone otherwise — someone chose) and some are *fixed law* (always the same).

The gods own the diegetic-contingent. In the actual sim that splits into **three** categories:

### 1. Divine act — a die is rolled *here*
Contingent; routes through a deity; receives a `providence` edge.
> fertility grants · harvest variance · drought onset · who starves to death · marriage pairing · lifespan-at-birth · where a fission settles · personality at creation

### 2. Natural law — fixed constants and equation *shapes*
Not a choice; the physics of the world. No deity involved, ever.
> food-per-person-per-season (3) · the 64-day year · the *form* `yield = min(labor, land) × variance` · labor efficiency · consumption rules

### 3. Deterministic consequence ("fate") — no die *here*, but inputs trace to past divine acts
Already written, because the gods wrote it upstream.
> a family hitting the fission threshold (pure consequence of births Venus already granted) · leader = oldest in largest family · marriage eligibility · **old-age death simply *arriving*** on the date Venus set at birth

The third category is the philosophically load-bearing one. **Old-age death is not a separate divine act — it is the lifespan Venus rolled at the moment of birth, finally coming due.** The die was cast at the blessing; the death is fate unspooling. The *moment of the roll* is the divine act; everything downstream is consequence.

### The categories are term-level, not system-level
A single equation can weave all three:

```
yield = min(labor × efficiency,  tract_cap)  ×  variance
              └── law (cat 2) ──┘  └─ cat 1, ─┘   └─ cat 1, ─┘
                                  set at creation  rolled each season
```

## Why the taxonomy pays off

1. **It bounds the intent bus — and protects the hot path.** Only **category 1** ever travels through the divine arbitration machinery. Categories 2 and 3 stay plain deterministic engine computation, no deity invoked. That's most of the per-tick work, which answers the performance concern directly: we are *not* routing every calculation through a god, only the genuinely contingent ones.
2. **The cat-1 / cat-3 line is a design dial.** Anything deterministic can be *promoted* to divine if contingency is wanted there. Succession is cat-3 today (mechanical: oldest in largest family); promote it and Zeus *chooses* an heir. Consumption is cat-2 today (flat 3/season); give appetite a roll and it becomes cat-1. The catalog is also a menu of where to inject divine agency next.
3. **It defines what a deity is for.** A deity exists exactly where a domain has category-1 decisions. No randomness in a domain → no arbiter needed. A clean test for whether a future planet-layer earns a deity.

## The causality graph: two edge types

A Venus-blessed child has two causal parents:

- `lineage` — biological parents (descent).
- `providence` — the deity that granted the outcome.

Every person carries both: literally their parents' child, providentially Venus's. The `CausedBy` relation gains a **role/type** so the two graphs can be queried independently ("all of Venus's blessings" vs. "all of X's descendants").

## Fit with existing architecture

- **Intent/receipt bus (model B).** This is the same PROPOSE → RESOLVE → RECEIPT pattern already sketched and deferred "until War/Trade need arbitration." Divine arbitration of randomness is a second, earlier motivation for it. PROPOSE: applicants emit intents. RESOLVE: the deity drains the queue deterministically and grants per the exact rule, drawing from its own RNG stream. RECEIPT: applied/rejected flows back; grants get the `providence` edge.
- **Planet-layer deities.** The organizing rule is *not* "everything goes through Venus." Each layer-deity owns its domain's RNG stream and arbitrates its domain's intents: Venus (Ecology) — fertility, harvest, drought, ecological death; Zeus (Rule) — succession, marriage (marriage is a cultural/order concept, per the per-woman discussion, so its randomness is Zeus's, not Venus's); Mars, Mercury — future.
- **Single-writer.** The deity is the sole writer of its domain's outcomes; all other systems propose and read receipts.
- **Replayable / reseedable gods.** One RNG stream per deity, drawn in deterministic order, is easier to reason about than scattered `hash(seed, ids…)` calls — and it can be replayed, reseeded ("a more generous Venus"), and swept by the exponator (sweep a deity's parameters).

### Determinism cost to keep in mind
Today's guarantee comes from *pure functions* (order-independent). A central arbiter draining a queue is *order-dependent* — who gets the 15% depends on processing order. Determinism is preserved by sorting the queue on a deterministic key (entity id / hashed priority) before granting. The discipline relocates from "pure functions" to "deterministic queue ordering."

## What centralization fixes — and what it doesn't

Centralization is often pitched as "making parameters mean something consistent." That's true for one of the *two* sources of cross-seed inconsistency, and false for the other. Keep them separate:

- **(a) Stochastic noise** — per-trial randomness (independent per-entity Bernoulli, per-community sampling wobble). Centralization + exact rates **fixes this directly.** A rate stops being a mere *expected* value sampled noisily and becomes the realized fraction; rate and spread become independent knobs, so parameter sweeps get a cleaner signal (output changes attribute to the parameter, not to lucky rolls).
- **(b) Structural amplification** — hard step functions (the fission threshold at ≥11 members) and feedback loops turn tiny differences into large divergences via sensitive dependence. Centralization does **not** fix this. *Empirically confirmed 2026-05-28:* routing fertility through Venus at `variance=0` (exact births) still produced 917–1129 persons across 4 seeds — a spread as wide as the per-pair-Bernoulli baseline (635–1262). The macro seed-sensitivity is the step function, not birth noise.

This is the determinism-vs-output-consistency axis: every seed remains perfectly reproducible; (a)/(b) are about cross-seed *legibility*, a different concern.

**The framework is the venue to fix (b) too — by choice, not automatically.** Promote a hard threshold from a cat-3 deterministic consequence to a cat-1 *graded divine roll* (a smooth probability ramp around the threshold instead of a cliff) and the amplification softens. And one RNG stream per deity makes residual variance *attributable* (reseed only Venus to isolate fertility luck from drought luck). So centralization makes rates legible now, and makes the chaos *tameable and analyzable* when you decide to address it.

## Synthesis with the per-woman fertility rewrite

The two redesigns reinforce each other. Under per-woman fertility, the applicant is the *woman*, and her diet/age/nutrition were going to set her *probability*. In a centralized lottery those same factors instead become her **weight in the allocation**: Venus grants N children this year, and the well-fed woman in her prime is likelier to be among the N. Result: exact aggregate control *and* per-woman biological differentiation — strictly more expressive than either redesign alone. The diet→fertility curve sets weight, not an independent coin.

## Inventory of randomness

**Creation-time (the Creator's design of the world — fixed once):**

| Random thing | Current owner | Divine lever |
|---|---|---|
| Tract fertility / yield-cap jitter | generation hash | Venus / creation act |
| Founder ages (18–45) | generation hash | Creator |
| Personality traits | generation hash | Creator / granting deity |
| Names | generation hash | cosmetic |

**Runtime (ongoing providence — what the bus arbitrates):**

| Random thing | Current owner | Divine lever |
|---|---|---|
| Fertility / births | per-pair roll | Venus *(flagship)* |
| Harvest yield variance | per-community roll | Venus |
| Drought / famine onset | emergent only (no live mechanic) | Venus — reintroduce as a regional roll |
| Starvation death (50%/season) | per-person roll | Venus |
| Old-age death | fated at birth (cat 3) | Venus (the lifespan grant) |
| Marriage chance + pairing | per-pair roll + shuffle | **Zeus**, not Venus |
| Fission: who leaves, where settles | personality + seeded pick | open (Venus / Zeus) |

## Dialing the dose

- **Minimal:** one RNG stream per deity + `CausedBy` role tagging. Flavor, auditability, replayable/reseedable gods. All current math unchanged. Pure upside — worth doing unconditionally.
- **Medium:** convert *just fertility* to weighted-lottery arbitration through Venus; everything else stays independent rolls. Proves the pattern on the highest-value case and is the natural home for the per-woman rewrite.
- **Maximal:** full intent/receipt bus; every domain's randomness arbitrated by its layer-deity; regional correlation for drought/harvest. Effectively building model B early.

Recommended path: ship Minimal unconditionally; make **fertility** the first arbiter (Medium), designed with the **same shape** drought will reuse when it returns.

## Open questions

- **Selection rule inside the lottery.** Quota allocation needs a rule for *which* applicants among N get granted: uniform (deterministic shuffle), weighted by nutrition/age (the per-woman synthesis), oldest-first, etc. This is a new design surface that independent rolls never had.
- **Variance dial defaults per stream.** Which streams want zero variance (exact) vs. authored swings? Births vs. drought likely differ.
- **Receipts as narrative hooks.** A repeatedly-denied applicant is a story seed (Luna). Receipts are not just plumbing; they're a place memory/story can attach.

## Parked (explicitly out of scope for now)

- **Personality drift / mid-life re-rolls.** Traits are category-1 (rolled at creation), then cast a lifelong category-3 shadow (fission, exodus, leader bonus). Whether the gods should ever re-roll a living person's traits sits exactly on the cat-1/cat-3 boundary — interesting, but deferred. Current static-trait behavior is accepted as-is.
