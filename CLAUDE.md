# Desktop Workspace

The active project is **Magnus3** — a C++ (flecs ECS) hierarchical
event-simulation engine. Read `C:\Users\Ryan\desktop\Magnus3\CLAUDE.md` before
working in it (the 7-layer "classical planets" architecture, single-writer
ownership, tick ordering, Divine Domain Administration).

## How we work

- **Observe before theorizing.** When investigating, run the code, check actual
  state, or test the behavior first. Source is a last resort for understanding
  runtime behavior, not the first move.
- **Stay collaborative.** Present plans and verify assumptions before executing.
  Verify specifics (paths, versions, ports) against the source, not other docs.
- **Beginner's mind.** Ryan often restarts the design from the very beginning and
  rethinks it anew. This is deliberate, not wasted time — re-deriving from "the world
  is created…" is how he works, and it keeps the result merciful to players. When he
  restarts from the top, follow him from the top; reflect and develop the fresh pass
  rather than rushing to reconcile it with prior state.
- **The weekly log is the default record.** Maintain `docs/logs/YYYY-MM-DD.md`
  (Monday of the week) and log *as work happens* — including research, planning,
  and decisions, not just commits. Format: `docs/conventions.md`.
- **Commits** are type-prefixed and carry no AI attribution. These rules are
  enforced by a hook; full convention in
  `docs/conventions.md`.
- **Windows gotchas** (absolute paths, `curl`/`jq` piping, encoding) live in
  `docs/conventions.md` — check there before fighting a Windows-specific tool
  error, and add new ones there.

## Key Locations

| Path | Description |
|------|-------------|
| `C:\Users\Ryan\desktop\Magnus3\` | Magnus3 simulation engine (C++/flecs). See its own `CLAUDE.md` for architecture. |
| `C:\Users\Ryan\desktop\docs\logs\` | Weekly logs (`YYYY-MM-DD.md`, Monday-of-week) |
| `C:\Users\Ryan\desktop\docs\conventions.md` | Commit rules, weekly-log format, Windows/shell gotchas |
| `jq` (on PATH) | JSON processing tool (winget jqlang.jq). Real exe path + pipe gotcha in `docs/conventions.md`. |
