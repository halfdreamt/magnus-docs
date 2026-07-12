# The Tavern Scene — deriving the flavor model

**Date:** 2026-07-11
**Status:** Design (Luna-authored under delegated authority; open questions answered where the scene demanded — flagged ⚖L)
**Related:** `2026-06-27-theogonus-nova.md` (coins, prestige open question), `2026-07-11-directive-disposition-model.md` (gunas, dynamic personality), `Magnus3/docs/design/pantheon.md` (Mercury's sign on discoveries, Mars's directed destruction), `Magnus3/docs/design/stage.md` (what stays authorable)

## Method

Take the target scene whole and decompose it until every noun and verb is
either something the model already generates or a named addition with a
diegetic seat:

> *A group of travelers, of varying professions, sitting in a tavern, when a
> group of undead from the evil city ruled by the necromancer appear.*

Six requirements fall out: **professions · travel and venues · community
relations · combat · necromancy and undead · the evil city.** Each section
below: what exists, what is new, which god and coin it rides, and what the
first slice is. A principle held throughout: **nothing in the scene is
generic.** The engine's one non-negotiable gift is that every person has a
history — every element of the scene should cash that in.

---

## 1 · Professions (classes)

**Exists.** Theogonus already frames this: before community there is exactly
one role (gather); the leader is the first specialist, "the labor whose
product is the organization of other labor." Temperament gives every person a
four-suit affinity blend. Agriculture is reached "through persistent labor
administration."

**New — the Callings coin (Mercury·Zeus, chosen).** Specialization is what
surplus buys: once a community's food margin sustains non-food labor,
individuals take **callings**. A `Calling` component (always-present;
sentinel = the universal gatherer/farmer), assigned at coming-of-age by
temperament affinity, community need, and inheritance pull:

| Suit | Calling family | Fantasy face |
|---|---|---|
| Pentacles (earth) | **Maker** — smith, brewer, builder | the artisan |
| Swords (air) | **Blade** — guard, hunter-of-men, soldier | the fighter |
| Cups (water) | **Keeper** — healer, priest, midwife | the cleric |
| Wands (fire) | **Adept** — lore, craft-secrets, magic | the wizard |

Affinity predisposes, never compels (a cold-dry person *can* become an adept;
the roll is weighted, cat-1, Venus… no — **Zeus arbitrates callings**: order
assigns roles; temperament is the weight). "Class" in play = calling +
renown (below) + temperament. The tavern's "varying professions" is this
coin working.

**⚖L Prestige, answered — the open question from Theogonus.** Prestige is
**the community's memory of witnessed acts**: an event-sourced ledger.
Prestige-bearing events already exist or arrive with this design — surplus
shared, dependents fed, a famine survived *while feeding others*, a raid
repelled, a healing, a discovery shared, an office held well. Each credits
its named participants. Properties:

- **Per-person, event-sourced, decays slowly.** Leader = highest prestige
  (replacing family-authority, as Theogonus intended). Dies with the holder;
  the Family coin makes it heritable — dynastic tyranny, stated mechanically.
- **Scoped by community.** A person's ledger lives where the acts were
  witnessed; elsewhere their prestige travels only as *story* (rumor — Luna's
  medium, chronicle-borne). This one property generates the necromancer:
  **revered at home, a monster abroad** — no alignment flag needed.
- **Renown = prestige within a calling.** The fantasy "level" is just
  standing: the Blade everyone sends for, the Adept whose name is known two
  towns over. No XP; deeds.

**⚖L Groundedness, answered** (the tyranny-drift axis from Theogonus):
groundedness = **earth-affinity × spirit**. Office erodes *spirit* over
tenure (dynamic personality's first live driver — power un-integrates);
low groundedness tips generosity toward neglect. Zeus's steering lever acts
on the erosion rate.

## 2 · Travel and venues (the tavern)

**Exists.** The spatial substrate (regions → areas → tracts → plots),
founding parties that physically relocate, exogamous marriage that already
implies inter-community contact, the unused `LocationLog` component, and the
stage's `create place`.

**New — Roads and Rests (Mercury, chosen).** Mercury owns movement between
communities. **Routes** derive from what already binds towns: founding
lineage (mother→daughter roads), marriage webs (kinship density), adjacency.
People gain **journeys**: temporary location ≠ home (LocationLog finally
writes), taken for reasons the model already has — marriages arranged
abroad, callings that travel (makers to markets, keepers on circuit, blades
for hire), pilgrimage, flight from famine. **Venues** are place-entities that
accrete where routes cross carrying capacity: the tavern (rest + drink =
surplus grain's second life), the market, the shrine. A venue is a child of
its community with a keeper (a calling), patrons (whoever's journeying
through), and its own event feed — which makes it a *scene generator*: the
tavern is mechanically "the set of people from different towns co-located
tonight," which is exactly what an adventure hook needs.

## 3 · Community relations

**Exists** — more than it looks: founding lineage (`CausedBy` between
communities), cross-marriage kinship density, shared famine history, and the
stage's `link` op for authored stances.

**New — Standing between communities (Zeus senses, Mars supplies the
grievances).** A sparse per-pair **Stance** (allied · friendly · wary ·
hostile) *derived, not stored as opinion*: kinship density and lineage pull
toward warmth; **grievance events** push toward hostility — raids suffered,
aid refused in famine, a leader slain, *graves robbed* (§5). Stance is
Zeus-owned (order between polities), recomputed seasonally from the event
record, so it is explainable in play: "why do Persfell and Kondholm hate each
other?" has an answer with dates. The DM's `link` op overrides or seeds
stances at the stage layer — authored grievance is just an authored event.

## 4 · Combat (Mars's content, at last)

**Exists.** Mars as deity + disposition; `EventType::War/Raid/Battle` and
`WarParams` stubs; `Mortality` (gains cause `Violence`); `HealthState` — the
long-flagged placeholder that finally earns its keep; DivineArbiter.

**New — two grains, one owner.**
- **Generation-grain: raids.** Between hostile pairs, Mars arbitrates raids
  (seasonal, disposition-gated: a tamasic Mars lets grievances fester
  unavenged; a rajasic Mars answers every insult). A raid resolves to **named
  outcomes only** — every casualty a person with a chronicle, every survivor
  carrying the grievance forward (feeding §3's stance loop). No faceless
  multitudes: the invariant, now load-bearing in war.
- **Session-grain: the tavern fight.** Personal combat capability =
  calling + renown + temperament + health — a small deterministic resolver
  (Mars's die, seeded) usable by seats and by us at the table, but the
  *default* at session grain is authored resolution: Ryan and Luna adjudicate,
  the stage records outcomes as events with `caused_by: Mars` where his die
  was rolled. Combat is thus playable **today** (authored) and simulable
  tomorrow (resolver), same event vocabulary.
- **Mars's domain signal** (was placeholder 0): **unavenged grievance +
  entrenchment** — the pantheon doc's own spec ("directed destruction aimed
  at disproportion") becoming his weather.

## 5 · Necromancy and the undead

This is where the engine's nature pays out. **The dead are not gone** — every
dead person persists with name, kin, deeds, cause of death, chronicle. The
soul pool (coin 0) is timeless; Saturn reclaims all. Therefore:

**Necromancy is theft from Saturn, delivered by Mercury.** The pantheon doc
already specifies Mercury discharging discoveries that carry a **sign**, with
the lightning-rod image — destructive force grounding out somewhere. 
**Necromancy is the first destructive discovery**: a Mercury discharge that
strikes a person instead of a rod. The struck adept becomes **the
necromancer** — a calling corrupted, not a species. Diegetically complete:
Mercury's fault, Saturn's grievance, one person's story.

**An undead is a *specific* dead person, reanimated.** Not spawned monsters —
a `Reanimated` state referencing the dead person's entity: their name, their
face, their kin. The soul stays in the pool (Saturn holds what is hers); what
walks is the body with the chronicle attached and nobody home. The horror is
**recognition**: the third one through the tavern door is Maren Bratherns,
who died in the famine of year 62, and her granddaughter is at the corner
table. Mechanically: reanimation events target dead persons (recent, local
graves first — hence **grave-raids**, the necromancer's signature raid type,
generating maximal grievance per §3); an undead persists until destroyed
(**the second death** — a `Mortality` cause of its own; Saturn collects at
last, and the family's chronicle closes the wound with a date).

## 6 · The evil city

**No new mechanics.** The evil city is the other five sections composing:
a community whose **leader is the necromancer** (prestige ledger: revered at
home — he feeds them, protects them, his dead legions do the field labor no
living community can match; feared abroad, where only the grave-raids are
witnessed) · **stances hostile** with every neighbor via the grievance loop ·
**raids outbound** carrying named undead · a tamas-dark chronicle. "Evil" is
never a flag — it is a *reputation gradient with receipts*, which means a
party can visit the necromancer's city and find it… orderly. Well-fed.
Grateful. The optimizer-thesis, wearing a black crown.

---

## The scene, replayed in model terms

Travelers (**journeys** on Mercury's **routes**) of varying professions
(**callings** with **renown**) sit in a tavern (**venue** at a route
crossing) when undead (**named reanimated dead**, taken in last season's
**grave-raid**) from the evil city (**necromancer-led community**, **hostile
stance** with receipts) appear (**Mars raid event**, disposition-gated,
casualties by name). Every noun has a chronicle. Nothing is generic.

## Build order (each slice playable; stage-authoring covers everything until its slice lands)

| Slice | Content | Unblocks |
|---|---|---|
| F1 | **Callings + prestige** (component, coming-of-age assignment, prestige ledger + leader-by-prestige, renown) | classes; the Theogonus prestige question closed in code |
| F2 | **Community stance** (derived standing + grievance events) | factions, "why they hate us" |
| F3 | **Mars v1** (raids w/ named outcomes, Violence cause, health live, session resolver, Mars domain signal) | combat both grains |
| F4 | **Necromancy** (signed discovery, necromancer emergence, grave-raids, Reanimated, second death) | the undead, the evil city |
| F5 | **Routes + journeys + venues** (LocationLog live, taverns) | travelers, scene staging |

Everything above is **stage-authorable today** with the six ops (tag a
community's leader `necromancer`, `create` undead persons linked
`was_in_life` → their dead selves, `link` hostile stances, author the raid) —
session zero does not wait on any slice. The slices convert authored flavor
into generated history, one noun at a time.

## Parked

Army-scale war (raids stay party-scale); magic beyond necromancy (the signed-
discovery frame generalizes when wanted); venue economics; undead ecology
(do they eat? — no: they are Saturn's unpaid debt, they cost nothing and
return nothing, which is exactly why a necromancer out-produces the living).
