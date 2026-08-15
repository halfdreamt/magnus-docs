# NPC briefs — persistent character prompts

One file per recurring NPC. Each brief is a self-contained prompt for a
small subagent (Haiku/Sonnet-class) to play the character in a scene beat,
plus a `State` section the GM updates after each appearance so the
character accumulates history.

Rules:

- A brief contains ONLY what the character knows, feels, and wants — never
  campaign secrets beyond their knowledge, never other characters' secrets,
  never GM plot intentions. Scope leaks here become spoiler leaks at the
  table.
- Player dialogue is passed to NPC agents in the translated in-universe
  register (see ../table-notes.md).
- Subagent output contract (include in every dispatch): dialogue in voice
  (1–2 utterances), physical behaviour (1–2 lines), one internal-reaction
  line for the GM; under ~120 words; no narrating other characters, no
  deciding outcomes, no new scene events.
- After the beat: the GM weaves the return into narration freely (the
  agent's words are raw material, not canon until narrated) and appends
  one line to the brief's State section.
- Major cast (Herazade, the Triumvirs) may eventually warrant Sonnet-class
  agents with fuller briefs; keep those briefs scoped just the same.
