# Luna's Spellbook & the Perturbation — concept-level edits, and Earth informing Heaven

**Date:** 2026-07-11
**Status:** Design (Luna-authored; Ryan's direction — spellbook as codified concept-changes AND future-mechanics source; perturbation un-deferred: "the engine should handle itself")
**Related:** `Magnus3/docs/design/stage.md` (the six primitives — unchanged, still the whole mutation law), `content-playbook.md`, the session/levers reviews (2026-07-11 log)

## Why these are one design

A raw `set` changes a value; a **macro** applies a *concept* — and a concept is
exactly what the engine can be informed of. `event: "the granary burned"` has
no engine meaning; `embitter(Kondholm, Persfell, weight)` knows both its
record shape (the events/links it writes) **and** its engine mutation
(`record_grievance`). The spellbook is therefore the *semantic dictionary* the
perturbation reads. And per Ryan's deeper point: **a macro cast often enough
is a mechanic the engine is missing** — the spellbook's usage ledger is the
gap-log with numbers attached.

## Half one — the Spellbook

- **A macro** = `{name, params, compile(params) → [primitive ops], semantics}`.
  `semantics` is either `record_only` or a named engine perturbation (below).
  **The one-API invariant holds**: casting a macro appends its compiled
  *primitives* to the edit log (auditable, undoable as a unit), with the macro
  name + params as provenance metadata on those ops. The log stays primitives;
  the spellbook is how they were spoken.
- **The codified book, v1** (each with engine semantics): `kill(person, cause,
  tick?)` · `wound(person, amount)` / `heal(person)` · `embitter(commA, commB,
  weight)` / `reconcile(...)` · `bestow(work, person)` · `bind(being, person)`
  / `release(being)` · `exile(person, site?)` · `bless(person, god, rider)` /
  `curse(...)` · `advance(seasons)` (moves now_tick; with the perturbation
  built, optionally *simulates* the gap). Record-only casts render in
  chronicles like any authored material.
- **Minting mid-session**: `stage macro define <name> <params> <op-template>`
  — a new macro is a parameterized template stored in the campaign (or a
  shared `spellbook.json`), castable immediately, `semantics: record_only`
  until someone teaches the engine its meaning. **The usage ledger** counts
  casts per macro across sessions; `stage spellbook report` lists the
  most-cast record-only macros — *these are the engine's next mechanics,
  demonstrated by play.*

## Half two — the Perturbation (Earth informs Heaven)

**The insight that dissolves the deferral: replay is the load.** The engine
regenerates to any tick deterministically and cheaply; at that moment ALL live
state (ledgers, charges, caches, singletons) exists in memory by construction.
No save format, no state import, no reconstruction — the problems that made
this look hard never existed on this path.

**Pipeline** — `world = continue(seed, config, perturbations@T, years)`:
1. Engine runs seed+config to **T = the campaign's now_tick, snapped to a
   season boundary** (the clean phase point).
2. Applies the **perturbation script** — the edit log compiled by the stage
   layer — in edit-log order, through the existing chokepoints: `set` →
   component writes (death-shaped sets route through `kill_person`); `create
   person/place` → the generators (full sentinel sets — the rules hold);
   macro semantics → `record_grievance` / custody / `HealthState` /
   `BeingBinding` / riders; flavor events → injected into the event record at
   their stated ticks (record-only; chronicles keep them).
3. Simulates T → T+N. Every system reacts to the perturbed state — stances
   recompute, prestige accrues, wounds heal, the raid the party provoked
   actually comes. **The engine handles itself. That is the point.**
4. Exports the full 4D history (original + continuation), new checksum.

**Determinism**: the recipe is now `seed + config + [edit-epoch → absorbed at
T1] + [edit-epoch → absorbed at T2] + …` — same chain, same world, always.
CLI shape: `magnus3 continue --perturb <file> --at-tick T --years N`;
stage-side: **`stage advance --years N`** compiles, invokes, re-stamps the
campaign on the new export, and marks absorbed edits (kept in the log for
provenance; `resolve()` skips them — they are IN the export now).

**⚖ Decisions taken (Luna):**
- **All perturbations apply AT the boundary T**, even past-dated ones (the
  record keeps the stated tick; the mechanics land at T). Mid-replay injection
  at the edit's own tick — "the timeline heals," with full knock-ons — is a
  documented v2 option, deliberately not v1: it would rewrite events the table
  already witnessed.
- **`note`/`tag` stay stage-only** (no engine meaning); `link` gains meaning
  only through `embitter`-class macros.
- **Authored ids (`a1…`) are remapped to engine ids at absorption**, mapping
  recorded in the campaign (so later edits referencing them still resolve).

## Hardening this leans on (Ryan's instinct, confirmed)

Nearly everything needed already exists because we built it disciplined:
chokepoints for death/prestige/grievance/custody; generators that mint
complete sentinel sets; season-boundary phase cleanliness; per-build
determinism with golden gates; the campaign as recipe. Genuinely new surface:
the run-pause-perturb-resume mode in `Simulation`/CLI, the perturbation
script format + stage compiler, and absorbed-edit bookkeeping. The rest is
verification.

## Verification contract (both halves)

Spellbook: casts compile to primitives (log auditable, undo-as-unit); ledger
counts; a minted macro round-trips a session. Perturbation: same recipe ×2 →
identical checksum; a null perturbation at T reproduces the unperturbed world
byte-identically after T (the golden test of the pipeline); a `kill` at T
removes the person from all post-T life (no ghost births/marriages — the
hardening test); an `embitter` yields a real StanceShift in the continuation;
a created person marries/works/dies like anyone (no thin-air seams); chronicle
continuity across the boundary (one life, one story, the intervention visible
only as its in-world event). Playbook rows throughout; perf row (replay cost
is the sim cost — already paid).
