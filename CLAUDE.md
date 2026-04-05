# Desktop Workspace

General starting point for Claude Code sessions. For project-specific context, navigate to the project directory where its own CLAUDE.md will take precedence.

## Rules for Claude Code

### File Operations (Windows)
- Always use complete absolute Windows paths with drive letters for ALL file operations (e.g., `C:\Users\Ryan\desktop\project\file.cs`)
- This prevents "file unexpectedly modified" errors during Read/Edit/Write operations

### Shell Piping (Windows)
- Do not pipe `curl` output directly to `jq` — Windows pipe encoding issues cause jq parse errors
- Instead, write to a temp file first: `curl -s ... -o /tmp/response.json && jq '.' /tmp/response.json`

### Git Commit Rules
- **Never** include "Co-Authored-By" lines or any mention of Claude/AI in commit messages
- **CRITICAL**: Never run `git commit` without first presenting the exact proposed commit message to me and receiving explicit approval. No exceptions.
- Always prefix commit messages with a type: `Feat:`, `Fix:`, `Refactor:`, `Docs:`, `Test:`, `Chore:`, etc.

### Collaboration Style
- **Observe before theorizing.** When investigating an issue, run the code, check the actual state, or test the behavior first — don't read through the codebase looking for answers that a quick test run or inspection would reveal faster. Source code is a last resort for understanding runtime behavior, not the first.
- Keep the process collaborative — present plans and verify assumptions before executing. When referencing specific details (paths, versions, ports), verify against the actual source rather than copying from other documentation.

### Weekly Log (Strict)
- Maintain a weekly log at `docs/logs/YYYY-MM-DD.md` (named for Monday of that week)
- Log **as work happens** — open the log at the start of any task and add entries throughout, not just at the end
- Log every action — including knowledge work like research, analysis, brainstorming, meetings, and planning, not just code commits
- Write entries as nested bullets: top-level is the action or topic, sub-bullets are context, reasoning, and what you learned or decided
- Entries are **chronological** — always append new entries at the end of the day's section, not interspersed with earlier work
- This is the default way both Ryan and Claude keep track of what's happening — not a review step, not optional

### Platform Gotchas
- When encountering unexpected errors running straightforward scripts or commands — especially Windows-specific issues (encoding, path handling, shell differences, tool quirks) — add the problem and workaround to this CLAUDE.md file so we don't hit the same obstacle twice.

## Key Locations

| Path | Description |
|------|-------------|
| `C:\Users\Ryan\desktop\OpusIVSEcosystem\` | Opus ADAS Calibration Ecosystem orchestrator |
| `C:\Users\Ryan\bin\jq.exe` | JSON processing tool |
