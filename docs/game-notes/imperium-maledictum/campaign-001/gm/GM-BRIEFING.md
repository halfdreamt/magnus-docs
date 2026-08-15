# GM briefing — start here

For whoever runs the next session: a fresh agent, a compacted one, or a
human. **Read this file, then only what it points to for the scene in
front of you.** The world bible is deep on purpose; you do not need it all
at once. Ten minutes here should get you to the table.

## 1. Where we are (one paragraph)

Campaign 001, Imperium Maledictum, one player (Ryan) as **Adept Vesper
Antiphon-6** (he/him) — a Grade I Tech-Adept spirit-speaker just
Invested by his new Patron, **Magos Acquisitor Herazade Vex-Kappa-9**,
aboard the Ark Mechanicus *Recollections of Rust*. Session 01 ended with
the Investiture complete: tether installed, first communion clean, oath
sworn, and Herazade walking him down to a lighter bay for his first
mandate. **Session 02 opens at the lighter bay doors.** Then: the Voll
mission, "The Forge-Temple of the Tides."

## 2. Read for Session 02 (in this order, ~10 minutes)

1. [../sessions/session-01.md](../sessions/session-01.md) — what actually
   happened; the "Open threads" and "Established canon" sections matter
   most.
2. [table-notes.md](table-notes.md) — **the table mandates** (verbatim
   translation quotes, checks in the open, PC authorship, no seeds at
   the table, `(OOC: ...)`) and Ryan's style. Non-negotiable; read every
   line of "Conventions."
3. [session-1-investiture.md](session-1-investiture.md) — from "Part 0,
   beat 5" (the lighter and the mandate) through all of "Mission 1."
   That is the session-02 prep.
4. NPC briefs you will need: [npc-briefs/herazade.md](npc-briefs/herazade.md)
   (State section — she is mid-scene),
   [npc-briefs/podra-vellum-kite.md](npc-briefs/podra-vellum-kite.md)
   (the pilot; new), [npc-briefs/muniment.md](npc-briefs/muniment.md),
   [npc-briefs/mission-1-cast.md](npc-briefs/mission-1-cast.md).
5. [world/canon.md](world/canon.md) — skim C11–C17 (patron, PC, and the
   two rules adopted at the table); check the rest only when a ruling
   comes up.

Everything else in `world/` (weave, cast, factions, gazetteer) is
**reference**: consult it when play reaches something, not before.
[insights.md](insights.md) is the founding design memo — background only.

## 3. How to run a beat (the loop)

1. Ryan states intent + why. Translate his dialogue into Mechanicus
   register, **quote the canon line word-for-word**, offer one small
   coaching note when useful, and proceed (sign-off only if you changed
   meaning). Coaching notes so far: Omnissiah spelling; "xenos" not
   "xeno scum"; title-as-honorific ("Magos," "Honoured Overseer"); "the
   Cult Mechanicus" not "the cult"; "the Machine God/He," not "our Lord."
2. If a Test is needed: **declare** Skill/Spec, base value, Difficulty,
   modifiers, stakes — then roll with
   `python3 tools/imtool.py test <target> --difficulty <d> [--advantage N]
   [--sl-modifier N]` from the campaign-001 directory. Show roll, target,
   SL. **Do not show seeds**; record them in the session file's roll
   audit.
3. Recurring NPCs are played by small subagents from their briefs
   (Haiku for routine, Sonnet for Herazade). Dispatch = the brief's
   character block + scene-so-far + Vesper's canon line + the output
   contract (1–3 utterances, 1–2 behaviour lines, one GM-only internal
   line, no narrating the PC, no deciding outcomes). Weave the return
   into narration; you own the prose. **Agent transcripts can expire
   between beats — re-seat from the brief + a scene summary; that is
   what the State sections are for.** Update the State line afterward.
4. Never resolve Vesper's words or actions beyond what Ryan stated. If
   an NPC needs his answer, stop and ask.
5. Log as you go: session file scenes, NPC State lines, canon.md for any
   new ruling, table-notes for any new preference. Commit + push at
   natural breaks (`git add docs && git commit -m "Docs: ..." && git push
   origin main` from the repo root; type-prefixed messages, no AI
   attribution).

## 4. Spoiler boundary (absolute)

Ryan reads: `world-primer.md`, `rules-and-setting-primer.md`,
`campaign-state.md`, `sessions/`, `characters/`, `players/README.md`.
He does **not** read anything under `gm/`, nor the Voll Adventures or
AdMech GM's Guide corpus. Do not quote or paraphrase GM-only material in
player-facing text. When citing sources to him, prefer core/Player's
Guide pages.

## 5. Tone in one line

Wonder first, dread second; the Imperium is the horror, the machines
mostly aren't; mercy is available and priced; horror at full weight when
it earns its place. Ryan likes lore-coaching as a reward, social geometry
over skill gates, and rites to hold onto in hard moments.

## 6. When you end a session

Fill the session file's Mechanical changes / Established canon / Open
threads; update NPC State lines and `campaign-state.md`; add anything
new to canon.md; write the next session's prep (a short file like
session-1-investiture.md, sourced from the corpus — see
`../../README.md` and `sources/wh40k-imperium-maledictum/retrieval/README.md`
for routing); update this briefing's sections 1–2; commit and push.
