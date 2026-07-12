# The Wide World — the content catalog and the pipeline that carries it

**Date:** 2026-07-11
**Status:** Design (Luna-authored under delegated authority; ⚖L marks decisions taken)
**Related:** `2026-07-11-tavern-scene-model.md` (the F-train, all landed), `Magnus3/docs/design/content-playbook.md` (the pipeline — written alongside this), `2026-06-27-theogonus-nova.md` (Sol the progenitor; demigod lines parked)

## The premise

The F-train built a deep but thin stack: callings, prestige, stance, raids,
necromancy, roads, taverns — one of each. Going wide means many of each kind,
and the danger is that every addition costs what a slice cost. So the design
has two halves, and the first is load-bearing:

**Half one: make content cheap.** Three generalizations turn "new thing" from
architecture into data-plus-a-control-law.

**Half two: the catalog** — everything seated diegetically, nothing generic,
every noun with a chronicle.

## Half one — the three generalizations

1. **Beings.** Undead generalize: a Being is any named non-person actor —
   beast, undead, experiment-spawn. Shared shape: kind + name, its existence
   IS its (un)life event, a location/territory, combat presence, a *binding*
   (to a person, a god, a site, or nothing — wild), and a chronicle voice.
   Undead migrate onto the framework (greenfield); every later being kind is
   a registry row + a control law.
2. **Sites.** Venues generalize: a Site is any place with story — tavern,
   wizard tower, shrine, beast den, and **ruin**. Shared shape: place entity,
   parent (community or wilderness tract), founding/abandonment events,
   keeper/inhabitants (persons or beings), a contents/hoard hook.
3. **The signed-discovery table.** Necromancy generalizes: Mercury's
   destructive strikes become a table of corrupted-adept archetypes
   (necromancer · beastcaller · plaguewright · stormcaller …), each with its
   own emissions; mitigating strikes seed the counter-arts (wards, healing
   arts). One emergence machinery, N archetypes.

The interaction glue is already built and does not change: stance/grievance,
prestige, raids, routes/journeys, dispositions, the chronicle, the stage.

## Half two — the catalog (each seated, ordered by session value)

- **Beasts (Venus).** Wilderness ecology on tracts — the Magnus2 fauna
  lineage returns as Beings: wolves/bears/lions tiered by menace, **dragons**
  apex (rare, ancient, site-bound with hoards). Predation threatens
  travelers on roads and communities at the margins; **hunts** are the
  community response (Blade prestige source, Keeper work after). And the
  disposition doc's promise comes due: **a rajasic Venus sends the beasts** —
  her displeasure finally has teeth.
- **Ruins = dungeons, created diegetically** (Ryan: nothing from thin air —
  the bigger the thing, the more so). Three dungeon kinds, all with real
  origins:
  - **Fallen places** — a community dies (famine, raids, fade-out) and its
    site persists as a ruin *whose fall is in the record*; a dead wizard's
    tower becomes one the same way (the site lifecycle is generic).
  - **Natural hollows** — caves seeded at world-gen: Saturn's creation is
    itself a diegetic act, so the world is *made* with hollow places; they
    pre-date people and beasts den in them first.
  - **Inhabitants move in for reasons**: beasts prefer den sites (territory
    selection favors caves/ruins), undead linger where a necromancer fell,
    later perhaps outcasts. Nothing spawns *in* a dungeon; things *arrive*.
  - **Treasure = Works.** The honest hoard needs things that were genuinely
    made: **Works** — rare, named, durable goods a Maker produces at the
    peak of a life ("the blade Ferrum, forged by Doustcrans in year 88"),
    with maker/date/place provenance events, held by families and
    communities, inherited, carried, and *left behind when the place falls*.
    Dragons, later, gather them. Every piece of loot has a maker and a
    history — which makes loot a story hook instead of a number.
  **Every dungeon is a place with a chronicle** — the scene query works on a
  ruin as well as a tavern.
- **Mad wizards and towers (Mercury).** The discovery table plus one social
  mechanic: a struck adept whose home turns on them (prestige collapse at
  home — the scoping already exists) **withdraws** — founds a Tower site in
  the wilderness. Experiments are their periodic emission events per
  archetype: escaped beasts, a plague, walking dead — threat generators
  *with an address*, which is what an adventure needs.
- **Demigods = Sol's line** ⚖L. Theogonus already licenses this: the
  role-bearing gods are sterile; Sol the rejected stone fathers the mortal
  line. So demigods are not divine dalliances — they are **Solblood**: a
  rare heritable spark in one founder line per world (deterministic per
  seed), elevating capability, drawing prestige and divine attention.
  ⚠ The one wave needing Ryan: Sol-as-progenitor isn't seeded in-engine yet
  (Theogonus seeding was deferred), so v1 Solblood marks a founder line
  without the full cosmogony — flag before building.
- **Divine interactivity — expression-side only** (the control-theory weeds
  stay parked). **Omens**: DispositionShift events become visible portents
  Keepers read — chronicle and scene texture, cheap. **Shrines**: a Site
  type, Keeper-kept, where communities address the gods. **Blessings and
  curses**: person-level providence events — emitted by gods at disposition
  extremes at generation, and *authorable by Luna/DM at the table* through
  the existing event op (providence `caused_by` already carries a deity).
- **Community archetypes.** Derived labels, not flags: trade hub (route
  degree), shrine town, martial town, frontier, evil city, ruin — computed
  from calling mix + venues + stance web + history, surfacing in `skim` and
  `scene`. Plus one generation knob: **raider cultures** (a community whose
  economy is raiding — Blade-skewed, raid-prone), a second generated
  antagonist type beside the necromancer.
- **Waiting stubs, taken when cheap:** `Illness` (plaguewright + natural
  outbreaks), `Meeting/Rivalry` (interpersonal arcs — likely post-session-0,
  let play demand them).

## The pipeline (the vital half — see content-playbook.md for the letter)

- **The playbook** (`Magnus3/docs/design/content-playbook.md`): the distilled
  F-train formula every content slice follows — seating, sentinels, hooks,
  export 4D, viewer, chronicle, and the fixed verification table
  (determinism ×2 · coin A/B · no-faceless · soak · golden re-record ·
  chronicle quotes). Agent prompts shrink to "spec + playbook + deltas."
- **The content lint** (`tools/lint_content.py`): static cross-checks that
  kill the drift class we already caught four times — every EventType has an
  export name, a viewer color, a chronicle handler; every coin has a card;
  every config leaf is seated. Runs in every slice's verification, fails
  loud.
- **Golden + validate-config** gate the rest, as they have all day.
- **Cadence:** the F-train pattern per wave — one Opus slice at a time on
  the engine, Sonnet for standalone tooling, commit-per-green-slice.

## Waves

| Wave | Content | Notes |
|---|---|---|
| W0 | **Beings framework + lion proof** · **content lint** · playbook | the repeatability wave; lion = Venus rajas expression + road predation, proving kind #2 lands cheap |
| W1 | **Blooded Lines** (divine offspring, inheritable gifts, the manifestation) | `2026-07-11-blooded-lines.md` — supersedes the Solblood entry; promoted on Ryan's call |
| W2 | **Sites framework + ruins + caves + Works** | dungeons v1, created diegetically (fallen places, creation-seeded hollows, Works as provenanced treasure); venues migrate onto it |
| W3 | **Beasts full** (tiers, dens, hunts, dragons + hoards) | |
| W4 | **Wizard towers** (discovery table, exile, experiments) | |
| W5 | **Omens · shrines · blessings/curses** | divine expression content |
| W6 | **Community archetypes + raider cultures + skim/scene upgrade** | |

Order tuned for session variety early; freely reorderable. Session 0 remains
runnable at any point — every wave only adds toys.

## Parked — generation-time prophecy (the fixed point)

Omens that reference the world's own computed future are achievable by a
two-pass generation — run, harvest notable events, re-run injecting true
foretellings as records; determinism keeps them true — **exactly as long as
omens stay consequence-free**. The moment mortals *react* to prophecy, the
second pass diverges and every foretelling self-invalidates: prophecy becomes
a fixed-point problem, with self-fulfilling and self-defeating oracles as
emergent phenomena — the observer changing the observed, thesis-adjacent.
Deliberately parked (2026-07-11). Built instead: **fate-reading omens** —
category-3 reads of dice already cast (a senescence date, a scheduled
discovery), true by construction, paradox-free, inert by invariant. At the
session layer prophecy needs nothing at all: the unwritten future is the
seer's script, and the perturbation makes averting it real.
