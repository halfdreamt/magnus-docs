# Campaign 001 state

Last updated: 2026-08-14 (canonization pass; Ryan approved concept C, the
Tech-Acquisitor-led Boon package, and delegated remaining decisions)

## Established canon

Nothing has entered play yet. Everything below is accepted preparation,
ratified by Ryan on 2026-08-14, and becomes fiction only as it enters play.

## Table state

| Item | Current state |
| --- | --- |
| Campaign premise | The custody of wonder: Mechanicus technoarcheology from Voll to the Ark, in Lathe Axis-438's sphere (GM arc: `gm/world/weave.md`) |
| Patron | Magos Acquisitor Herazade Vex-Kappa-9 (she/her), Invictus Acquisitor; Boons: Data-Trawler + Tech-Acquisitor + Augmetics Bay + Void Logistician; secret Liabilities recorded GM-side |
| Player character | Adept Vesper Antiphon-6, Grade I Rune-Priest-trained Savant and spirit-speaker; built with open arithmetic in `characters/vesper.md` |
| Starting world | Voll (Hive Rokarth and the Unsea), during the closing years of Explorator Rotation #46 |
| Starting mission | Prelude "Investiture" aboard Recollections of Rust, then "The Forge-Temple of the Tides" (`gm/session-1-investiture.md`) |
| Active factions | Adeptus Mechanicus (Incalcos-6, the Ark), Stilt-fleet Wastelanders, Voll chem-guilds/nobility, with the Vigilites and Inquisition dormant |
| Date in fiction | c. 012.M42, dated in play by rotation leg (canon C1–C2) |
| Party assets | Arvus Lighter "Sacristan's Patience" + retained pilot Podra Vellum-Kite (Patron property, imperfect paperwork) |
| Party Influence | Vesper: +1 Adeptus Mechanicus |
| Superiority | Not in an encounter |
| XP, Fate, Wounds, Corruption | Vesper: 25 XP banked, Fate 3, Wounds 0/13, Corruption 0 |

## Accepted Patron direction

- Faction: Adeptus Mechanicus.
- Duty: Invictus Acquisitor, expressed as a specialist in technoarcheology and
  technological reclamation.
- Motivation: Information.
- Demeanour: Pragmatic mentor.
- Duty Boon: Data-Trawler.
- Mandate: investigate rumours, authenticate discoveries, contain dangerous
  finds, and return lost knowledge to Mechanicus custody.
- Character relationship: the Patron values the prospective novice's curiosity
  and noospheric sensitivity, granting independence but expecting disciplined
  reporting and containment.
- Full design, rationale, and unresolved elements: `patron.md`.

## Play infrastructure

- A dependency-free dice and encounter helper is available at
  `tools/imtool.py`; see `tools/README.md` before use.
- Live encounter JSON belongs in the ignored `runtime/` directory. Promote
  durable consequences to this file and the relevant session record.
- Default to theater of the mind. `table-tools.md` records when a Zone map is
  likely to help and what ForMander can already provide.

## Confirm at the table (small, non-blocking)

- (Settled: Vesper uses he/him. Table convention: out-of-character remarks
  are prefixed `(OOC: ...)`.)

- Content boundaries: default is wonder-forward grimdark with fade-to-black
  on body-horror specifics (canon O6); Ryan can adjust any time.
- When additional player-agents join: pitch slots are prepared
  (`gm/world/weave.md`, multi-player readiness; onboarding in
  `players/README.md`).

## Standing rulings

- Resolve threshold follows core p198 (Superiority ≥ Resolve → Desperate);
  implemented in `imtool.py`; ledgered as canon C8.
- All other optional-source rulings live in `gm/world/canon.md`; check it
  before ruling on anything the books leave open, and append new rulings
  there as they are made in play.
- Solo-PC support levers (allies, healing access, encounter tuning) are
  recorded in `gm/insights.md`; revisit when the party grows.

## Resume pointers

Session records go in `sessions/`; established facts merge back into this
file and the GM world bible (`gm/world/`) per its README method. The first
session's prep is `gm/session-1-investiture.md`.
