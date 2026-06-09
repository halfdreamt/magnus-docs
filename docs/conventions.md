# Workspace Conventions

## Git commits

- **Approval-first (behavioral — not machine-enforced).** Never run `git commit`
  without first presenting the *exact* proposed commit message and receiving
  explicit approval. No exceptions. This is about showing the message first, which
  a hook can't verify, so it lives here as discipline. (The permission prompt gates
  the commit itself; this rule is the courtesy of showing intent before acting.)
- **Type prefix (hook-enforced).** Every message starts with a type:
  `Feat:`, `Fix:`, `Refactor:`, `Docs:`, `Test:`, `Chore:`, `Perf:`, `Style:`,
  `Build:`, `CI:`, `Revert:`.
- **No AI attribution (hook-enforced).** Never include `Co-Authored-By` lines or the
  `Generated with ...` footer. The intent is no AI credit in the history — mentioning
  Claude/`.claude/` as a *subject* of the work (e.g. "Docs: add Venus agent") is fine.

Enforcement: `~/.claude/hooks/check-commit.ps1` (a `PreToolUse` hook) blocks a
`git commit` whose inline message carries `Co-Authored-By` / `Generated with`, or
that lacks a type prefix. It inspects only the command string, so editor- and
`-F file`-based commits pass through unchecked, and approval-first is never
machine-checkable. To tighten it (e.g. also block the literal word "Claude"), edit
the `$forbidden` list in that script — but note that will reject commits that name
the `.claude/` agent files.

## Weekly log format

- Path: `docs/logs/YYYY-MM-DD.md`, named for **Monday** of that week.
- Log **as work happens** — open the log at the start of a task and append
  throughout, not just at the end.
- Log every action, including knowledge work (research, analysis, brainstorming,
  planning, meetings) — not just commits.
- Entries are nested bullets: top level is the action or topic; sub-bullets carry
  context, reasoning, and what was learned or decided.
- **Chronological** — always append at the end of the day's section; never
  intersperse new entries with earlier work.
- This is the default record for both Ryan and Claude — not a review step, not optional.

## Windows / shell gotchas

- **Absolute paths always.** Use complete absolute Windows paths with drive letters
  for all file operations (e.g. `C:\Users\Ryan\desktop\project\file.cpp`). Prevents
  "file unexpectedly modified" errors during Read/Edit/Write.
- **Don't pipe `curl` straight into `jq`** — Windows pipe encoding breaks jq parsing.
  Write to a temp file first: `curl -s ... -o /tmp/response.json` then
  `jq '.' /tmp/response.json`.
- **jq real path:**
  `C:\Users\Ryan\AppData\Local\Microsoft\WinGet\Packages\jqlang.jq_Microsoft.Winget.Source_8wekyb3d8bbwe\jq.exe`
- When a straightforward command fails with a Windows-specific quirk (encoding, path
  handling, shell differences, tool behavior), record the problem and the workaround
  here so we don't hit it twice.
