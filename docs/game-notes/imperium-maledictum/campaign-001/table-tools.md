# Table and scene-tool assessment

## Recommendation for Campaign 001

Begin in theater of the mind. Imperium Maledictum already measures combat in
abstract Zones, so spoken locations such as “gantry”, “reactor floor”, and
“behind the blast door” carry almost all the information needed for a small
encounter. The local encounter dashboard can remember those Zones, Initiative,
Wounds, Conditions, Resolve, and Superiority.

Add a visual table when spatial relationships become hard to hold in memory:

- roughly five or more relevant Zones;
- multiple routes, floors, or moving groups;
- several barriers, hazards, or sources of cover;
- hidden information whose reveal matters;
- a chase or infiltration where the route itself is the problem.

A map should clarify choices, not turn Zones into five-foot-square movement.
An index card or quick sketch is sufficient before software is.

## What ForMander can provide now

The sibling ForMander project is a deterministic, replayable tabletop scene
host. Its current useful pieces are:

- a rules-neutral `SceneLayout` format and browser/SVG viewers for backgrounds,
  grids, entities, scenery, labels, and interaction markers;
- exact movement- and sight-blocking geometry for authored layouts;
- hosted scenes with separate controller and audience projections;
- a campaign scene ledger with scoped GM, party, public, and seat facts;
- seeded decision records and replay verification;
- an adjudicated-scene pattern where a player states free-form intent, a
  referee specifies the mechanical Test, and the engine rolls afterward.

That means we can author and display a static Zone map in ForMander today if an
encounter benefits from one. It does **not** yet have an Imperium Maledictum
ruleset, live token/door editing, fog of war, an IM character sheet, or native
Wounds/Superiority/Resolve controls. Its existing D&D adjudicated scene is a
useful architectural precedent, not a rules-compatible substitute.

## A useful Imperium Maledictum table surface

If Campaign 001 proves that a shared table would help, the smallest worthwhile
ForMander addition should expose different information to GM and player.

| Concern | Player surface | GM surface |
| --- | --- | --- |
| Intent and Tests | Free-form intent; final Skill, Difficulty, roll, and SL | Choose Skill, Difficulty, Advantage/Disadvantage, and SL modifiers before the seeded roll |
| Zones | Visible Zones, routes, cover, hazards, and known entities | Hidden entities, undiscovered routes, barriers, and reveal controls |
| Combatants | Initiative, current turn, conditions, and broad enemy state | Exact Wounds, Critical Wounds, stat-block limit, Resolve, and notes |
| Group state | Superiority and visible reasons it changed | Exact adjustments, hidden triggers, and NPC Desperate state |
| History | Public rulings and outcomes | Private adjudication plus replayable complete decision stream |

The first implementation should remain an adjudication aid: accept intent,
let the GM frame the Test, roll deterministically, and record the result. Full
attack, Armour, weapon-trait, Critical-table, psychic, and vehicle automation
would create a much larger rules engine and should wait until actual play shows
which portions are repetitive enough to justify it.

## Staged path, if needed

1. **Now:** theater of the mind plus `tools/imtool.py`.
2. **Map only:** author a rules-neutral ForMander `SceneLayout` for a specific
   complex encounter and use its existing viewer.
3. **IM scene shell:** add an Imperium Maledictum kit/ruleset for referee-framed
   d100 Tests, Zone occupants, Initiative, Wounds, Conditions, Superiority, and
   Resolve with private/public projections.
4. **Campaign memory:** connect scene briefs and verified outcomes to
   ForMander's scoped campaign ledger while keeping Magnus campaign notes as
   the human-readable source of campaign continuity.
5. **Selective automation:** implement only the attack or recovery operations
   that play has demonstrated are slow or error-prone.

No ForMander work is required before character creation or the first session.
When the first likely combat location is known, the GM should make a fresh
map/no-map decision based on that encounter rather than committing the entire
campaign to one presentation style.
