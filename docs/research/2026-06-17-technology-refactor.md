# Technology refactor — the soul-pool reordering

## The turn

Today's sequence is Frame → **Bearing World** → People. That smuggles in an
assumption: to exist is to need to eat, and to fail to eat is to die. The bearing
world comes first because people are modeled as mouths.

Reverse it. **People first.** Existence and identity, communities forming — with
no eating, no death, no birth. A soul pool that simply *is*. "Being and vibing,"
nothing much happening. Hunger, mortality, and reproduction become later
*acquisitions*, not the price of admission. The person is the ground; the ecology
is a thing that happens to it.

This is the humanist motif made structural: the first thing the world contains is
people, before it contains any of the pressures that later optimize them.

## What the soul pool is (tier 1) — Saturn's

A set of person-entities that exist, carry an identity, and group into
communities. Static — almost nothing ticks. This is **Saturn's**, not Venus's:
people don't relate to Venus until they must eat and reproduce. Saturn is their
inherent soul-mother — the Kali who births the soul into being (and later takes it
back). No divine/mortal distinction yet; just souls.

**Present**
- person entities + `PersonIdentity` (name)
- self-identity: gender, orientation (`rule.identity_distribution.*`),
  personality traits
- community membership / grouping

**Absent or dormant** (each returns later as its own technology)
- `FoodStores`, consumption, gathering, starvation — no eating
- `Mortality` — no death of any kind
- aging / lifespan — no time passing for a body
- `BirthSystem` — birth is not yet a coherent concept
- marriage, family-as-lineage, leadership, authority, cohesion, fission/founding
- the divine/mortal distinction itself (see open questions)

## How this decomposes today's "People" tech

Today's People (13 params) bundles existence with the consequences of embodiment.
The soul pool keeps only existence + identity; the rest scatters forward.

| Param | Today | Soul-pool home |
|---|---|---|
| `rule.identity_distribution.*` (5) | People | **People** (soul pool) — self/identity |
| `ecology.sex_distribution.*` (2) | People | **People** — kept as identity for now (Ryan's call) |
| `world.founding.min/max_age_years` (2) | People | **People** generation — inert until Birth & Death makes age matter |
| `ecology.consumption.food_per_person_per_season` | People | **Birth & Death** — the material cost of being incarnate |
| `ecology.starvation.zero_food_death_chance` | People | **Birth & Death** — death-by-lack (Saturn reclaims) |
| `ecology.lifespan.base_min/max_years` (2) | People | **Birth & Death** — death-by-age (Saturn reclaims) |

Result: "People" stops being a mouth-with-a-lifespan and becomes a *soul* —
identity and belonging, nothing else.

## The refined model — eternal Saturn, incarnate Venus

The flip resolves into a clean division of the two earliest deities. **Saturn is
the eternal:** she creates the world, holds the soul pool, and takes the dead back
— womb and tomb, the deathmonger at both thresholds (cf. May). The soul pool,
before birth and death, is Saturn's **golden age**: souls still with the great
mother, the deathless age before mortality. Saturn ruled the golden age, exactly
as the myth has it — the model derives the mythology. **Venus is the incarnate:**
the body, its hungers, and the labor that feeds it. People are Saturn's until they
must eat and reproduce; that need is exactly where Venus enters.

| # | Tier | Owner | What enters |
|---|---|---|---|
| 0 | **Frame** | Saturn | time + space, the world created (unchanged) |
| 1 | **People / the soul pool** | Saturn | souls exist — identity, community; timeless, static |
| 2 | **Birth & Death** | Venus (birth) · Saturn (death) | the first bargain — bodily reproduction + mortality, and **consumption** (the material cost of being incarnate). Both deaths (by lack, by age) are Saturn reclaiming the soul. |
| 3 | **Food Yield** | Venus | the mercy and the labor — drawing sustenance from the earth (gathering, hunting, later agriculture); the land's fertility/yield-cap consolidated here |
| … | Marriage → Leadership → Birth Control → Crowding → Agriculture | Zeus / Mercury | social order, ascension, exchange (as today, downstream) |

Two consolidations fall out:

- **Bearing World + Gathering merge into Food Yield.** The land's latent capacity
  and the act of drawing from it are one Venusian thing — "taking from the earth."
  ("Food Yield" generalizes "Gathering": it spans hunting and, later, agriculture.)
- **People + Wheel split apart.** Existence is Saturn's soul pool; reproduction-
  and-mortality is the Venus/Saturn **Birth & Death** bargain — *"we want more
  people, even if it means we have to die,"* the first devil's bargain. (Rename:
  **"The Wheel" → "Birth & Death"** — "the wheel" reads as the wheel of fortune,
  a different thing.)

The pivotal flavor: **incarnation is a debt.** To take a body — to be born of
Venus — is to need material (coins, food) to sustain it, and to be reclaimable by
Saturn when the material runs out or the time does. Birth, hunger, and death
arrive as one coupled acquisition, not three.

## The model's reach — composable law-states

Each technology is an independent law toggled on its own, so *combinations* the
default sequence never visits become coherently modelable. The layering is
generative, not merely an onboarding order:

- **The golden age** is {Frame, People} with Birth & Death off — souls with the
  great mother, deathless. Saturn's reign.
- **Valhalla / afterlives** — War (a later tech) *without* Birth & Death is endless
  battle with no true death, a hall of the slain. Toggling death under other laws
  lets the afterlife be modeled several ways.

So arbitrary on/off sets aren't bugs to forbid but states to explore. The refactor
should preserve this: keep laws independently toggleable even where the default
genesis order never separates them. (This is the payoff of the binding + toggle
work — every law a real switch.)

## Families, unbaked

From the soul pool forward there are no families — only people in communities, and
a **community is functionally one big family**. "Family" as a lineage/inheritance
unit is a Marriage-tier construct, not a given. And with reproduction owned by
Birth & Death (not gated by marriage), **Marriage is purely Zeus** — a social-order
institution, not a reproductive gate. So the Zeus/Venus seam isn't marriage; it's
**leadership's food bonus** (below).

Also not yet: **wandering.** People are naive — they don't know how to gather, so
they don't know how to spread out either. Migration is a later Mercury gift
(someone must teach them). So a community has no spatial relief valve; it breeds
toward carrying capacity and is stuck there.

## Leadership reconceived — the trap, and the first mortal dial

A community with no migration breeds toward its CC and then has nowhere to put the
surplus. What happens at CC is the question Leadership answers — and the answer is a
trap.

- **Cohesion as average standing.** Before the Leadership technology, the
  community's yield bonus derives from its **average standing** — a flat,
  collective property with no single point of failure.
- **Leadership is the trap.** The technology is the move to a *singular* leader:
  the highest-standing person provides their standing bonus **alone**, replacing the
  average. An efficiency gamble — the best individual beats the average, so yield
  rises — but the bonus now hinges on one fragile, self-interested agent.
  Optimization buys a higher peak and a cliff. (On-thesis: the optimizer is the
  horror.)
- **The first mortal dial — the leader's ration.** The leader controls the food
  (they hold the store; see the spatial question below). In scarcity they *choose*:
  feed self and kin first, or share the burden. This is the live, dynamic version
  of today's static `authority_steepness` — disparity becomes a *decision*, not a
  constant — and it is the Zeus/Venus seam in one act: Zeus's authority deciding
  Venus's distribution.
- **The cycle.** Overshoot CC → scarcity → leader rations selfishly to survive →
  **standing falls** (visible hoarding) → if it falls far enough, ousted (regicide)
  → the singular bonus collapses → famine deepens. The leadership cycle is born from
  one mortal's short-term choice.

## Two agencies — divine and mortal

We've tuned **divine** dials (DDA: a god administering its domain toward a
directive). The leader's ration is the first clear **mortal** dial — bottom-up
agency with consequences. The symmetry is a design axis worth holding: gods
*administer*, mortals *decide*, both tunable and dynamic. Other mortal dials likely
live downstream — whether/whom to marry (Zeus), whether to wander (Mercury), how
hard to labor (Food Yield) — but the leader's famine ration is the sharpest and
earliest.

## Open — the spatial grounding of food, the store, and famine

The crux: *why* can the leader take from the store, and does a store even exist once
famine has started? It depends on why famine happens.

- **Why famine.** With no migration relief, a productive community overshoots CC;
  when a season's yield can't meet need (overshoot, a bad-variance season, or the
  singular bonus collapsing on leader loss), people go unfed.
- **Store vs. flow.** Spoilage already caps hoarding (~2 seasons), so there's no
  deep reserve. Two readings: (a) a **thin granary buffer** the leader controls, or
  (b) **pure seasonal flow** — gather and eat each season, storage itself a later
  acquisition. Under (b) the stockpile question dissolves: famine is simply this
  season's yield short of need, and the leader rations *the harvest*. Leaning (b)
  for the early tiers — it matches spoilage and keeps storage as its own later thing.
- **Spatial access.** Either way, the leader's privilege is *control of the food at
  its gathering/holding point* — leadership is, spatially, control of the commons'
  yield; "taking" is rationing it in their own favor.

Open: what generates an individual's **standing** (trait-derived? earned by
contribution?), since both baseline cohesion (average standing) and leadership (max
standing) now hang on it.

## Emergent divinity — ascension

The mortal/divine split isn't given; it's *earned*, and staggered. "Someone needs
to make a decision" is the flavor under today's leadership; raise it a level and
it's fractal — a great early king dies and **ascends to the Rule deity**, who then
grants authority to later kings. The divine becomes the persisting legacy of a
great mortal: founder-rank and authority-inheritance become the god's gift to its
successors. Venus gets a mortal parallel to keep the shape symmetric — a
**matriarch / priestess** specialist in the community, mirroring the leader, who
ascends to the Ecology deity that administers fertility (the DDA directive,
currently given, becomes *earned*).

So divinity enters as a **technology of ascension**: the first specialists become
the first gods. Until then the genesis sequence is fired by the exogenous creator
(the player), with no in-world god — and the pantheon is filled bottom-up over the
run rather than handed down at gen.

## Parked — to flesh out later

- **Ascension mechanics.** What triggers it (death of a high-authority leader? a
  cohesion/legacy threshold?), what the resulting deity *does* (grant authority,
  run a directive), and — under the always-present-sentinel rule — whether deity
  entities are seeded dormant at gen and *activated* on ascension, never created
  mid-sim.
- **The local Venus parallel.** A matriarch/priestess role mirroring the leader:
  a second specialist slot per community with its own ascension path to Venus, and
  how it relates to the existing leadership/authority machinery.

## Resolved

- **Time stays in the Frame.** Unbaking time is a concept, not a mechanic — a world
  run 1000 years with nothing in it doesn't change whether or not time "exists."
- **Natal sex stays under People** (identity) for now.
- **Initial food → Birth & Death, reconceived as "mana".** The soul's starting
  endowment arrives *with* incarnation (not as a separate Saturn gift) and bridges
  the gap before Food Yield exists — the material to pay the incarnation debt at
  first. Flavor: "mana," and a candidate for distinct mechanics later (e.g.
  doesn't spoil; a finite, once-only endowment). `world.community.initial_food_*`
  → Birth & Death.
- **Venus owns the land's fertility.** `ecology.tract.cap_base` + biome modifiers
  fold into Food Yield (Venus). The earth is Saturn's making; its *yielding* is
  Venus's.
- **Birth split across deities (working seam).** Saturn births the *soul* (into
  the pool); Venus births the *body* (reproduction); death is Saturn's either way.
  The shared Birth & Death tier is Venus (birth-of-body) · Saturn (death + soul).

## Status

Exploratory. Nothing wired. The binding (`src/laws/TechParams.hpp`,
`validate-config`) and the current tree (technologies.md) remain the live spec
until this settles. Changes here are expected to be large (registry reorder, new
tiers, param re-homing, possibly generation-time gating).
