# The world bible — GM-only

This directory is Campaign 001's narrative web: not a plotted line but a
world, so that future agents spend their time **referencing and connecting**
rather than generating material live at the table.

## What lives here

| File | Contents |
| --- | --- |
| [canon.md](canon.md) | The decision ledger: every optional, ambiguous, or contradictory element in the source books that this campaign has canonized, with citation, ruling, and blast radius. **Check here before ruling on anything the books leave open.** |
| [cast.md](cast.md) | The dramatis personae web: every NPC of campaign relevance, grouped by sphere, with allegiances, wants, secrets, and edges to other cast members. |
| [factions.md](factions.md) | Factions, sects, and networks with their campaign stances and pressure points. |
| [gazetteer.md](gazetteer.md) | Places, from hive floors to subsectors, each with its campaign function and hooks. |
| [weave.md](weave.md) | The metanarrative: the threads that run through everything, how the published campaigns interlock, act structure, and the questions the campaign is about. |

`../insights.md` remains the campaign's founding GM document; this directory
extends it. Where they conflict, the world bible wins and insights.md should
be updated.

## How this was built (and how to extend it)

The method, so any agent can continue it:

1. **Read the sources whole, iteratively.** The five books were read in
   sequence — AdMech GM's Guide and Voll Adventures in full (the GM spine),
   then the core rulebook's sector-and-factions material, the Player's
   Guide's cult-and-sects material, and the Requisition Guide's
   services-and-contacts material. Read in chunks of 1,000–1,500 transcript
   lines; after each chunk, write what matters into these files **before**
   reading on. Reflections written to disk survive; context does not.
2. **Extract webs, not summaries.** For each chunk ask: who is in it (cast),
   what do they want and from whom (edges), what is left open (canon
   candidates), what does it touch elsewhere in the corpus (weave). A fact
   that connects two books is worth ten facts that don't.
3. **Canonize deliberately.** When a book offers options ("the GM may
   decide…", contradictory hints, unresolved mysteries), either rule now in
   canon.md with a citation, or explicitly list it there as OPEN. An
   undocumented ruling is a future contradiction.
4. **Cite everything.** Book + printed page, using the `(scan pN · PDF pN)`
   markers in the transcripts. Corpus routes are in
   `sources/wh40k-imperium-maledictum/retrieval/README.md` (corrected
   routing tables and errata). Body-text search works:
   `grep -in "name" sources/wh40k-imperium-maledictum/*/transcript/*_combined.md`
   or the ForMander browse tool.
5. **Respect the spoiler boundary.** Everything here is GM-only. The
   player-safe projection of this world lives in
   [../../world-primer.md](../../world-primer.md); update it in the same
   pass whenever a fact becomes table-known. Player-facing agents read the
   primer, never this directory (see `../README.md`).
6. **After play, promote.** Session records feed campaign-state.md;
   established facts get folded back here (cast entries updated, threads
   advanced, canon confirmed or amended). The bible describes the world as
   of its `Last updated` stamp — keep the stamps honest.

Abbreviations used throughout: core = Imperium Maledictum core rulebook,
PG = AdMech Player's Guide, GG = AdMech GM's Guide, MRG = Macharian
Requisition Guide, VA = Voll Adventures.
