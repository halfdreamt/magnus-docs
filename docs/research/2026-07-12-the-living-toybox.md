# The Living Toybox — the improvise → normalize loop

**Date:** 2026-07-12
**Status:** Design (Luna-authored; Ryan's direction verbatim: the compendium
"generated, because I want to give it the feeling it can be added to easily,
programmatically... keep expanding the toybox iteratively until it's so big we
need to pick and choose which concepts we allow in a world"; every Luna needs
to "set their 'spells' up extremely easily (on the fly, structured world
changes, created in game often) and those ad hoc spells can be very, very
easily modeled into our greater engine when possible... We don't want any of
our creative energy to go to waste." The griffin is the canonical example:
make a griffin-feeling being in session; afterwards normalize it; new worlds
just have griffins.)
**Related:** luna-protocol.md, luna-compendium.md (the hand-written seed this
work replaces with generation), content-playbook.md (the normalization
pipeline that already exists), spellbook-and-perturbation.md (minting — the
loop's ancestor)

## The loop, named

1. **KNOW** — a generated compendium tells any Luna everything the engine can
   produce, always current, because it is derived from the code's own
   registries.
2. **PLAY** — Luna improvises structured content mid-session with zero
   friction: proto-concepts that RIDE existing machinery.
3. **KEEP** — every improvisation is captured with provenance: what it was,
   what it rode on, every use, every dice roll and cast it touched, the
   session text around it.
4. **NORMALIZE** — after the session, the capture compiles into a playbook
   slice brief; an agent lands it; the concept becomes native; the generated
   compendium picks it up automatically; existing campaigns migrate their
   protos to the real thing.

## L1 — The generated compendium

`stage compendium` renders the toybox from machine-readable sources — the
Theogonus coin registry, BeingKind/WorkKind/SiteKind/EventType tables,
DivineLine, callings, archetype labels, doom types, era machinery, the
spellbook (codified + minted), and each concept's config knobs. Two-layer
document: a small hand-curated cosmology preamble (stable) + the generated
body (never hand-edited).

**The self-maintenance rule (the friction-killer):** prose lives in a
**concept registry** (`tools/compendium/concepts.json` or equivalent — one
entry per concept: table-facing description, spot-it-by, bring-it-by, knobs),
and **`lint_content.py` enforces it**: a new BeingKind/coin/EventType/macro
without a concept entry fails the slice, exactly like a missing chronicle
handler. Adding a tenant automatically means describing it, so the compendium
cannot go stale. Census mode: `stage compendium --world <campaign>` renders
the toybox WITH this world's actual counts (present / absent-but-castable /
absent-needs-knob) — the protocol's census habit becomes one command.

## L2 — The proto kit (spells set up extremely easily)

The insight that makes protos free: **the engine doesn't need to know about
griffins for a griffin to work at the table — it only needs a body to ride.**
- `stage proto <name> --rides <kind> [--fields JSON] [--notes ...]` creates a
  proto-concept: an entity created through the EXISTING bridged machinery
  (`create_being` with the ridden kind, `create --entity-type person/place`,
  or a Work via `bestow`), plus a proto envelope in the campaign
  (`campaign.protos[]`): name, what it rides, the intended texture, and a
  provenance tag every subsequent cast/check/event on it carries. The engine
  sees a beast; the table sees a griffin; `advance` carries it (T5's bridge
  already works — the ridden kind is real).
- Behavior is improvised through the existing verbs — minted macros, notes,
  events, checks — ALL stamped with the proto tag. A proto's whole life is
  queryable: `stage proto show griffin`.
- Protos can also ride nothing (pure-record concepts — a new ritual form, a
  weather, a faction) — record-only, same envelope, same capture.

## L3 — Rigorous session logging (no creative energy wasted)

The session transcript is a first-class artifact:
`campaigns/<name>.sessions/NNN-<date>.md`, appended AS THE TABLE RUNS with
the protocol's own beat blocks (TABLE / SEATS verbatim / DICE / WORLD / LUNA
/ LEVERS) — the same content the DM sees in chat, durably on disk (the seats'
transcripts are NOT durable; the session file is the record). Cross-linked:
gaps, protos, and minted macros reference the session file + beat where they
were born. The protocol gains: writing the beat block to the session file is
part of rendering the beat — not optional, not deferred.

## L4 — The normalization report (the loop's exit ramp)

`stage protos report [--all-campaigns]` compiles each proto into a
**normalization brief**: name, what it rode, every field/note/macro/event it
accumulated, session-text excerpts where it appeared, and a pre-filled
playbook slice skeleton ("BeingKind::Griffin — registry row + control law;
observed behaviors: dens in peaks(cast x3), preys on travelers(events x2),
tamed by a check DC 14(session 2 beat 7)..."). The report is what a build
agent receives; the playbook takes it from there. Minted-macro promotion
(the spellbook report) folds into the same report — macros and protos are
the same loop at different grains.

## L5 — The concept menu (the pick-and-choose future, thin edition)

When the toybox outgrows any single world: `stage new --concepts` presents
the registry as a menu; selections compile to the config overrides that
enable/disable each concept (the registry already knows every concept's
knobs from L1). Coin hands did this for arts; the menu does it for
everything — at the stage layer first (compiling existing knobs), engine-
unified only if play demands it. Not part of the first train if time is
short; the registry makes it cheap later.

## Order

L1 (registry + generator + lint rule) first — it defines the concept
registry everything else references. L2 + L3 parallel behind it (tools/docs,
disjoint). L4 rides L2's envelope. L5 whenever. All tools-layer: no engine
changes, no golden impact, full test-idiom coverage (the 277-test file
grows).
