# Theogonus Nova — Slice 1: the Coin Reorder

**Date:** 2026-07-11 (overnight, autonomous per Ryan's green light; judgment calls flagged ⚖)
**Status:** Dispatched
**Related:** `docs/research/2026-06-27-theogonus-nova.md` (the spec), `Magnus3/docs/design/technologies.md` (the tree being superseded), `docs/research/2026-07-11-directive-disposition-model.md`

## Scope — what slice 1 does

Re-partition the genesis structure into the Theogonus coins, with the agency
line and staged mortality, keeping the world runnable at every prefix of the
sequence:

| # | Coin | Owner | Agency | Absorbs (current tree) |
|---|---|---|---|---|
| 0 | The World and its People | Saturn | sent | Frame + People-minus-eating (souls with identity; the deathless golden age) |
| 1 | Hunger and Toil | Saturn·Venus | sent | consumption + **starvation mortality** + Gathering + tract yield (the Bearing World retires; the land's yielding is Venus's toil-face) |
| 2 | Death and Birth | Saturn·Venus | sent | **senescence** (retroactive on fire) + birth + Birth Control (Venus's lever rides this coin) |
| 3 | Leadership and Community | Zeus·Venus | **chosen** | Leadership + cohesion + distribution |
| 4 | Marriage and Family | Zeus·Venus | **chosen** | Marriage + rank inheritance |
| 5+ | Crowding/Migration · Agriculture · War | Mercury · (⚖ see below) · Mars | chosen / net-positive | unchanged |

- **Staged mortality is the one real mechanical change.** Starvation death
  gates on coin 1; senescence gates on coin 2. Coin 2 off = no death clock;
  when it fires mid-run, lifespans are assigned deterministically (from person
  seed) to everyone alive at that moment — Saturn's death applied retroactively,
  per the spec.
- **Regroup, don't rename** ⚖: config paths (`ecology.*`, `rule.*`, …) stay
  stable so exponator, serve.py, and the viewer keep working; only the
  technology partition over them changes. Viewer/card sync is deferred to a
  follow-up.
- **Defaults keep all coins on from year 0** ⚖ (the standard world stays rich);
  a new `genesis` config variant staggers the sequence (golden age → hunger →
  death → leadership → family) to prove the walk and give the per-prefix
  verification worlds.
- **Single-tract default** ⚖: 1 region / 1 community / current founder counts
  (~9–12 souls). Pantheon-*sized* seeding (~7) hangs on the ascension design
  and waits with it.

## Deliberately deferred (Ryan's open items — untouched by design)

- **Ascension / emergent pantheon filling** (spec says explicitly "not worked
  out"); gods stay pre-created. **Sol-progenitor / deity sterility** hang on it.
- **Prestige** (the live open question) — leadership keeps its current
  selection mechanics, marked for the prestige rework.
- **Tyranny drift / dynamic personality.**
- **Per-family stockpiles + true pre-community private subsistence**: with coin
  3 off, community mechanics (leader, cohesion, distribution, marriage
  arbitration) are off but food pooling remains — an acknowledged approximation
  ⚖ until the per-family-stocks plan (2026-06-06) lands; coin 3's "full
  inventories, no way to give" texture arrives with it.
- **Luna.**
- ⚖ Agriculture ownership discrepancy flagged, not resolved: Theogonus says
  Venus's (via labor administration); the registry says Mercury. Left as-is.

## Verification contract

Per-prefix worlds on the `genesis` variant (0: souls static, no deaths/births;
+1: starvation possible, no senescence/birth; +2: full demography; +3: leaders/
cohesion; +4: marriages/inheritance); retroactive senescence observed on a
mid-run coin-2 fire; determinism ×2; `validate-config` clean; 1000y soak;
golden baseline re-recorded at the end (trajectories move — greenfield).
