# Divine Disposition — the Guna Data Model for Directives

**Date:** 2026-07-11
**Status:** Design draft — core decisions settled (per-deity moods, discrete states, gradient-driven switching, world + Luna as influences); control-law specifics per deity open
**Related:** DDA / directives (`Magnus3/CLAUDE.md`, `docs/design/pantheon.md`), divine determinism & the cat-1/cat-3 dial (`2026-05-28-divine-determinism.md`), Theogonus Nova (`2026-06-27-theogonus-nova.md`), elements personality rework (`docs/logs/2026-06-22.md`)

## The factoring

A directive today fuses three things into one control law. The disposition model
pulls them apart:

- **Intent** — the standing goal; what the god is *for*. Unchanged from the
  current DDA definition (id, label, goal + mechanism + tradeoff).
- **Disposition** — the guna state, dynamic; how the god currently *is*. New.
  Sits between intent and expression.
- **Repertoire** — the set of expressions the god can act through; what the god
  can *do*. Grows as the simulation gains actuators, without touching the
  disposition model.

The same intent under the same world-error expresses differently by mood:
**sattva** administers (the clean closed-loop law as written — every directive
built so far is sattvic); **tamas** goes dark (administration suspended at
runtime, the world running open-loop on the knobs as last set); **rajas**
escalates (higher gain, harsher instruments — the lions, when lions exist).
Displeasure and instrument are decoupled: Venus can answer the same grievance by
withdrawal or by predation, depending on where her charge has carried her.

## Components

```cpp
enum class Guna : uint8_t { Sattva = 0, Rajas = 1, Tamas = 2 };

// Per-deity. Always-present (seeded at deity creation, mutated in place —
// sentinel rule). Owner/writer: the deity's own layer system.
struct DivineDisposition {
    Guna  mood        = Guna::Sattva;
    float charge      = 0.0f;   // the gradient, [-1, +1]: rajas pole +, tamas pole -
    uint64_t since_tick = 0;    // start of the current mood episode
};

// Per-deity. Owner/writer: Luna, and only Luna — her single write surface,
// read by each deity's disposition update (the existing binding constraint:
// Narrative influences via its own components, never another layer's state).
struct NarrativePressure {
    float push = 0.0f;          // signed, [-1, +1]: + kindles rajas, - deepens tamas,
                                // decay toward 0 releases the god to its own weather
};
```

One signed axis carries the three states: **sattva is the centered band**, rajas
the positive pole, tamas the negative — guna-faithful (sattva *is* equilibrium)
and matches "a value on a gradient determining when the switch is flipped." The
charge is the gradient; the mood is the switch.

## The update (seasonal, deterministic)

Each deity's orchestrator updates its own disposition once per season:

```
charge' = clamp( charge·(1 - decay)
               + world_gain · domain_signal(world)     // the god's own weather
               + luna_gain  · NarrativePressure.push,  // the plot's thumb
               -1, +1 )
```

`domain_signal` is per-deity and deliberately unspecified here — what agitates
Venus (famine deaths? her restraint overridden? sustained CC overshoot?) and
what deadens her (long futility? being unneeded?) is each god's character, the
same class of open question as what generates prestige. The *slots* are fixed;
the *signals* are authored per god.

**Switching with hysteresis.** Enter and exit thresholds differ, so moods are
episodes, not flicker:

- charge ≥ `rajas_enter` (e.g. +0.7) → Rajas; falls back to Sattva only below
  `rajas_exit` (e.g. +0.4). Mirrored negative pair for Tamas.
- `min_episode_seasons` floors an episode's length regardless of charge.
- **The flip is a graded roll, not a hard step.** Within `ramp_width` of a
  threshold, transition probability ramps 0→1, rolled from the deity's RNG
  stream. This is the 2026-05-28 remedy applied at birth rather than
  retrofitted: hard thresholds are exactly the step-function structural
  amplification that made cross-seed outcomes illegible. It also makes the
  transition a **category-1 divine act** — contingent, attributable, an edge in
  the causality graph — rather than clockwork.

**Mood episodes are events.** A transition closes the current episode and opens
a `DispositionShift` event (start tick + duration, Famine-spell pattern), so
episodes land in the export, on the deity's timeline lane in the viewer, and in
any mortal chronicle ("that was the spring Venus darkened"). Mortals never see
the charge — only the expressions — so what a village knows of its gods is
inference from lions and lean years.

## Expression — how mood reaches the levers

The disposition modulates the directive's control law; it never bypasses
single-writer (a god still only bends its own knobs):

| Mood | Expression rule |
|---|---|
| Sattva | The directive's law as written and tuned. |
| Tamas | Administration suspended at runtime — controller gains to zero, knobs frozen as last set. Runtime state, distinct from config `enabled: false` (the player's choice to run open-loop is not the god's torpor). |
| Rajas | The law escalated: gain multiplier, setpoint overshoot, and — once the repertoire holds more than knobs — selection of harsher expressions. |

**Repertoire registry.** Each deity carries a small registry of expressions,
each tagged with the guna it serves. v1 is just the existing knobs re-seated
(Venus: fertility restraint = sattva; suspension = tamas; an overcorrecting
setpoint = rajas). Predation, plague, storm arrive later as rajas entries —
new actuator classes slot in without touching disposition or intent. Every
expression that touches people resolves to named participants (no faceless
multitudes): a lion's kill is `Mortality{cause: Predation, source: Venus}` with
a providence edge.

## Luna

Luna's writes are `NarrativePressure` and nothing else. Her sensing is
dramaturgical — flatness (how long since anything happened to this world),
looming totality (a collapse about to go unwitnessed) — and her actuation is
push: kindle a god toward rajas when the century is flat, soothe toward sattva
before a collapse goes total, let tamas lie when neglect is the story. Her
control law is a directive like any other ("for the plot" is her intent), which
makes her administerable by the same machinery she applies to the others.
Unbuilt in v1: `NarrativePressure` ships as a component defaulted to 0 so the
disposition update reads a real slot from day one; Luna's writer system comes
later.

## Config shape

Per-deity block beside `administration`, same house pattern:

```json
"disposition": {
  "enabled": true,
  "initial_mood": "sattva",
  "charge": { "decay": 0.05, "world_gain": 1.0, "luna_gain": 1.0 },
  "thresholds": {
    "rajas_enter": 0.7, "rajas_exit": 0.4,
    "tamas_enter": -0.7, "tamas_exit": -0.4,
    "ramp_width": 0.1
  },
  "min_episode_seasons": 4,
  "rajas": { "gain_mult": 2.0 }
}
```

All Heaven-scoped. `disposition.enabled: false` pins the god to sattva — the
A/B lever for sweeps, the same house pattern as `administration.enabled`.

## Determinism & audit

- Charge inputs are all deterministic (world state, Luna's component, config);
  the only rolls are ramp transitions, drawn from the deity's own RNG stream in
  a fixed seasonal order. Same build + seed + config → same moods, same
  episodes, same lions.
- Single-writer: each deity writes its own `DivineDisposition`; Luna writes
  `NarrativePressure` only; expressions execute through knobs the deity already
  owns. `DispositionShift` events are emitted by the mood's owner.
- Golden corpus re-records when the model lands — trajectories move, and
  per-build determinism is the only contract.

## Open

- **`domain_signal` per deity** — the character question (Venus's weather vs
  Zeus's vs Mercury's). First to settle, since everything downstream is tuning.
- **Rajas expression selection** when a repertoire holds several rajas entries
  (severity ladder? weighted roll? escalation with episode length?).
- **Deity temperament linkage** — deities are slated to get real `Temperament`
  values (currently exported neutral); whether a god's element/spirit biases its
  thresholds (a hot god enters rajas easily) or stays cosmetic.
- **Luna's own sensing** — the flatness metric, and what "for the plot" measures.
