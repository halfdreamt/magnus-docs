# The End of the World — engineered ends, and the ages that follow

**Date:** 2026-07-12
**Status:** Design (Luna-authored; Ryan's governing answer to every axis: **"yes, and…" — always configurable**)
**Related:** `2026-07-11-the-wide-world.md` (Works, ruins, the pipeline), `2026-07-11-spellbook-and-perturbation.md` (the epoch chain — the spine Part II rides), `2026-06-27-theogonus-nova.md` (the coins), `2026-07-11-the-map-v2.md` (the ground the ages share)

## The principle: an apocalypse is containment losing

Everything the wide-world built has an immune system attached: Keepers drive
plague to zero, expeditions march on towers, hunts answer dens, reprisals
check raiders. The world survives because containment loops win. So end
states need no new destruction machinery — **they are the thresholds past
which the existing containment loops lose.** Undead-kill-everything is
necromancers emerging faster than expeditions can fell them until the dead
outnumber the living. Every apocalypse is made of events the chronicle
already voices, uncontained.

The proof of concept happened by accident: W6's uncapped raider drift
produced 158 fallen communities a millennium — an emergent end-times,
promptly patched as a bug. The push, precisely: **take the world-death that
exists today only as a bug, and make it authored physics** — legible causes,
named types, a chronicle that knows it is writing an ending.

## Part I — The End

**The doom ledger.** World-pressure metrics, each read off a ledger we
already keep:

| Doom | Metric | Existing ledger |
|---|---|---|
| **The wrong arts** | destructive coin strikes outrunning mitigating ones | TechSign on every Theogonus strike — necromancy and plague compounding with no wards, no healing arts |
| **The wrath concurrence** | simultaneous deep-rajas count across the four | DivineDisposition charge; one angry god is weather, three at once is the end — and the shrine whisper becomes load-bearing in reverse: a world that never built shrines never calmed its gods |
| **The dead outnumber the living** | undead : living ratio | the necromancy loop, unsealed |

**The cascade.** Past a threshold, containment *visibly* fails — and this is
the part the chronicle voices hardest: the last Keeper dying, the expedition
that does not come back, the hunt that becomes a rout. Doom is a slope, not
a switch; mortals fight it all the way down.

**The simplification.** A collapsing population is a shrinking, cheapening
world — the sim gives Ryan's "simplified, smaller state" for free.

**The terminal event.** The world's death is an event like any other, with a
cause and a name: *"The world ended in the year 214 of the Age of Crows,
when the dead outnumbered the living."* Ages get names; endings get causes.
And since everything is determined, the fate-reading omens can read doom —
Keepers whispering the end early is near-free composition.

**The dead world is a product, not a failure screen.** A fully dead export
is ruins everywhere, Works ownerless in the rubble, dragons on their hoards,
undead walking, and a complete chronicle — the richest adventure site the
engine can produce. Which is why Part II follows from Part I rather than
sitting beside it.

**The seals.** All of it config: worlds are **mortal or sealed**, per doom
type. A sealed world is byte-identical to today's immortal behavior — the
A/B gate.

## Part II — The Turning

**The spine exists.** `stage advance` already does replay → perturb →
continue, deterministically, in one file, with per-epoch script hashes and
drift guards. **An era transition is the epoch chain wearing a crown**: run
the age to its end, apply the turning, continue as the next age. One file,
one world, one seed; `world.eras[]` beside `campaign.epochs[]`. The turning
is an engine-authored perturbation — **Saturn's second creation act, over
used ground instead of blank** (the worldgen exemption, generalized).

**The residue function.** The turning's definition: *what does an age leave
behind?* The apocalypse as lossy compression — living complexity in, durable
residue out:

- **The land** — the same map across ages is the payoff: the runes are in
  the pass your caravan uses today.
- **Sites** — every fallen town is already a ruin; across eras they
  **layer**. This earns the Malazan element the map doc extracted and
  couldn't yet honor: ruins of prior civilizations under the present.
- **Works** — provenance crossing ages: "the blade Ferrum, forged by
  Doustcrans in the 88th year of the Second Age." Nothing-from-thin-air
  holds perfectly: every dungeon treasure was really made, by a named hand,
  in a world that really ended.
- **The long-lived linger** — a dragon is ancient *because it remembers the
  last age*; undead do not care that the world ended.
- **Bloodlines** — a carrier line surviving the turning is the
  Six-Eyes-after-centuries moment, now with an apocalypse between.
- **The chronicle becomes legend** — era 1's record is era 2's
  half-remembered history.

**Who follows — the peoples.** All of it, configurable per transition
(⚖ Ryan, with relish): **remnant survivors' descendants** (continuity,
firsthand legend, surviving bloodlines) · **the same race respawned**
(Saturn seeds fresh founders on old ground; everything found is foreign) ·
**a different race entirely** — *era of the Jaghut, era of men; era of
elves, era of men; era of…* No forced order: men need not come last, and
high technology need not follow low. A **Peoples registry**: name, naming
voice, light modifiers (lifespan, fertility, calling affinities) — enough
that a prior age's ruins read as *another people's work*, not merely an
older copy of your own.

**The gods across the turning.** Configurable both ways: Theogonus
**carries** (grudges, dispositions, granted coins remembered — the gods
watched the last world die) or **opens fresh** — a new theogony over the
same substrate. Both in the palette.

**The endings palette.** Fire *and* the quiet fade: the named cataclysm and
the age that simply gutters out, its last town falling to no one in
particular. Both are turnings; both leave residue; the chronicle voices them
differently.

**The hands and the stamps — lost arts.** Theogonus deals each era **a hand
of coins**, and the hand differs: an age of high sorcery, an age of roads
and trade, an age of war-forges — the registry can grow era-flavored
categories so each age has a distinct technological character. Coins gain
**levels** (depth of the art). Every Work and Site is stamped
**(era, coin, level)** at creation — provenance, which we already do. Then
*lost* needs no mechanism at all: **a thing is lost when its stamp falls
outside the current era's hand.** The war-coin-level-3 blade found in a
war-level-1 age is impossible now — not by fiat, but because the art that
made it verifiably is not in the world. The Second Age tower has
architecture the current hand cannot raise; a spell is a Work whose coin no
one holds.

## The waves

| Wave | Content | Gate highlights (playbook full table throughout) |
|---|---|---|
| E1 | **The doom ledger** — the three metrics computed + exported, a viewer doom panel, skim surfacing ("this world is dying") | byte-inert A/B: metrics measure, never steer |
| E2 | **Cascades + the seals** — thresholds, containment-failure dynamics voiced, mortal/sealed config per doom | each end type reachable deterministically on a driven config; a sealed world byte-identical to today |
| E3 | **The terminal event** — world-death event + cause, age naming, the chronicle of the end, the dead-world terminal export, fate-omens doom reads | a world driven to each of the three ends produces a complete, navigable dead export |
| E4 | **The turning spine** — `eras[]`, the engine-authored transition perturbation, residue function v1, remnant/respawn succession (same race) | chain determinism ×2; an era-1-only run byte-identical to a plain run; residue verified item-by-item (ruins layered, Works held over, dragon persists) |
| E5 | **The peoples** — the registry, different-race succession, naming voices, foreignness in chronicle/scene ("Jaghut work, older than the age") | a two-era world where era 2's scene query on an era-1 ruin reads as another people's |
| E6 | **The hands and the stamps** — coin hands per era, levels, (era, coin, level) provenance, lost-art derivation, found-wonder surfacing in skim/scene/chronicle | a found Work verifiably impossible in the finding era; the lost-art list derived, never stored |

E1–E3 are Push A (the End), E4–E6 Push B (the Turning); reorderable within a
push. Session zero stays runnable throughout — every wave only adds. The
train runs on the merged map-v2 world, behind the raider rebalance.

## Parked

Tier-3 prophecy meeting world-death — the self-defeating doom oracle
("foretold ends averted by the foretelling") stays parked with the fixed
point (see the-wide-world.md). At the table, though, the payoff is live from
E2: a campaign can `advance` into its world's dying years and play them.
