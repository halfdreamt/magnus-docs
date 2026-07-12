# Blooded Lines — divine offspring and inheritable power

**Date:** 2026-07-11
**Status:** Design (Luna-authored; Ryan's revision of deity sterility + his founding
vision for the engine: inheritable powerful abilities — the Six Eyes moment)
**Related:** `2026-07-11-the-wide-world.md` (supersedes its W4/Solblood entry),
`2026-06-27-theogonus-nova.md` (theology revised — noted below),
`Magnus3/docs/design/content-playbook.md`

## The revision (theology, updated by Ryan)

Theogonus held the role-bearing gods sterile, Sol the sole progenitor. Revised:
**the gods can, rarely, father or mother a child.** Sol remains the progenitor
of the *common* line — the wide river of ordinary blood. The other gods' children
are something else: singular, and their blood carries a **domain-marked gift**
that persists in the line. Sol's abundance versus the gods' rarity keeps the
original myth's shape: the rejected stone built the world; the chosen gods each
left only a bloodline, thin as a wick, down the centuries.

## The two-state core: carriers and the manifest

The mechanic that produces "the Six Eyes user is born for the first time in
hundreds of years" is the split between **carrying** and **manifesting**:

- **`DivineBlood { line, potency, expressed }`** — always-present sentinel on
  every person (line=None default). Seeded at a divine conception; inherited
  thereafter.
- **Carriers** are silent. Potency dilutes down generations (child potency =
  max(parents) × decay, PROVISIONAL ~0.85), unnoticed by the world — the
  chronicle does not out them; Luna and the DM can see them (the same
  privileged read as the unwritten future).
- **Expression** rolls once, at birth (cat-1, the god's own stream): chance ∝
  potency × a rarity constant tuned so a full manifestation is a
  **once-in-centuries** event per world. Near-threshold potency can carry a
  line for ten generations of nothing — and then the child opens its eyes.
- **The Manifestation is an event** — world-visible, omen-grade, dated: *"In
  the four-hundred-and-twelfth year, for the first time since the world was
  young, the Open Eye looked out of a child of Kondholm."* The chronicle
  sings; the skim blurb mentions it; the world bends around it (below).

## Divine conception

Rare, seasonal, cat-1 on each god's stream: a god may conceive a child with a
mortal (the child is born normally to their mortal parent — Parentage carries
the mortal side; **providence carries the divine side**, the `CausedBy`
lineage/providence split doing exactly what it was built for). Gating knobs:
overall rarity (once per few centuries per god, PROVISIONAL), and the god's
**disposition colors it** — a rajasic Mars sires in a war camp, a sattvic
Venus blesses a beloved keeper's cradle (mood as flavor-weight, not
requirement). First-generation children start at potency 1.0.

## The four gifts (v1 — one signature per god, all through EXISTING hooks)

| Line | Gift | Engine effect (expression-side, playbook-cheap) |
|---|---|---|
| Venus | **the Evergreen Blood** | a life aura: their community heals faster (Keeper-hook multiplier), births healthier, beasts do not prey there; famine bites last |
| Zeus | **the Crowned Blood** | born sovereign: prestige magnetism (accrual multiplier), cohesion aura on any community they lead; contests collapse before them |
| Mercury | **the Open Eye** | the knowing: technologies fire early where they live (schedule acceleration), discoveries strike NEAR them safely (the living lightning rod), routes open around them |
| Mars | **the Red Hand** | the war-prodigy: combat_power multiplied severalfold; hunts and raids they join tilt hard; they do not die easily (injury resistance) |

A manifest bearer is *one person bending macro trajectories* — leader
selection, raid outcomes, a community's survival curve — which is precisely
"dramatic changes in the world because of it." The dilute gifts of mere
carriers: none in v1 (silence is the point), with a config hook for faint
echoes later.

## The breeding tension (Family coin interplay)

Inheritance makes bloodlines a *strategy*: a family that knows its blood (does
it know? — see open) may marry inward to keep potency, straining the exogamy
and incest constraints — dynasties hoarding a wick of god-blood is exactly the
entrenchment Mars exists to answer, and heritable prestige (the Family curse)
now has a sharper sibling. v1 does not make families act on it; the stage/DM
can (arranged marriages via authored events), and a later slice can give
bloodline-aware matchmaking to ambitious families.

## Session hooks (why Luna loves this)

Carriers are perfect protagonist material: a PC with dormant blood is a
loaded gun the table can fire — the manifestation can BE a session event
(authored, or discovered in the export's future). `stage` should expose
carrier status in the DM/Luna view (never in PC-facing context until
expressed).

## Config sketch

`<domain>.blooded` per god (conception rarity, disposition weights) + a shared
`bloodlines` block (decay, expression rarity constant, gift magnitudes — all
PROVISIONAL). Seated per playbook; new coin **`blooded_lines`** (owner —
⚖L Saturn? conception is sent, not chosen; the gods act but no community opts
in → agency **Sent**, owner the acting pantheon: registry single-owner
convention says pick the deciding deity — Saturn as the frame that permits it,
co-owners documented; open to renaming).

## Verification notes (beyond the playbook's fixed table)

- A manifestation occurring naturally across a multi-seed sweep at the tuned
  rarity (report incidence: aim ~0–2 per 1000y world).
- The world-bend shown: a manifest bearer's community trajectory vs. a
  matched control (Evergreen: famine deaths; Crowned: leader tenure +
  cohesion; Open Eye: tech fire years; Red Hand: raid/hunt record).
- Carrier silence: no chronicle/context leak of unexpressed carriers
  (PC-facing scoping test, same discipline as the unwritten future).
- The Manifestation chronicle quote, rendered, in the report.

## Open

- Do families KNOW their blood (breeding strategy needs knowledge; v1: no —
  the world learns at manifestation).
- Gift list depth per line (one signature each in v1; the table wants more).
- Relationship to ascension (still parked with Theogonus seeding); whether a
  manifest bearer is an ascension candidate when that returns.
- Cross-line unions (two bloods in one child: v1 keeps the stronger line only).
