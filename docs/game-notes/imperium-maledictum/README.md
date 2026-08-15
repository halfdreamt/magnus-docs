# Warhammer 40,000 Roleplay: Imperium Maledictum

Imperium Maledictum is a d100 tabletop roleplaying game about a small group of
agents serving a powerful Patron in the Macharian Sector. Investigation,
competing Imperial factions, institutional corruption, dangerous violence,
and the consequences of invoking authority are its central concerns. It is not
the Warhammer 40,000 miniatures wargame.

## Local reference library

The private, ignored corpus is at
`sources/wh40k-imperium-maledictum/`. It contains separate flavor and mechanics
collections for:

- the core rulebook;
- the Adeptus Mechanicus Player's Guide;
- the Adeptus Mechanicus GM's Guide;
- the Macharian Requisition Guide;
- Voll Adventures.

The core book is sufficient to begin. Add the Mechanicus Player's Guide only
when a character or campaign concept calls for its extra options. Treat Voll
Adventures as GM-only material because searches can reveal scenario spoilers.

## Retrieval workflow

The deterministic browser currently lives in the sibling ForMander workspace,
whose tracked manifest points through compatibility links to this corpus. From
the ForMander root:

```sh
.venv/bin/python -m tools.private_corpus browse \
  --manifest config/retrieval/imperium-maledictum.v1.json \
  --query "character creation"
```

This searches metadata only. Add `--include-text` deliberately when source
text is required. A useful workflow is:

1. Browse all ten indexes through the manifest.
2. Prefer a mechanics collection for a rule and a flavor collection for lore.
3. Open only the matched topic file under this repo's `retrieval/` tree.
4. Locate the relevant heading or printed-page marker within that topic.
5. Summarise the result in campaign notes; preserve the source route for later
   verification.

The search vocabulary comes mostly from headings and entry labels, not every
word in the prose. Broad queries can therefore miss a relevant passage or
return a broad topic containing an incidental match. OCR also fragments some
display headings. Search aliases help, but exact rulings still require reading
the routed topic.

## Core source routes

All paths below are beneath
`sources/wh40k-imperium-maledictum/retrieval/`.

| Subject | Route |
| --- | --- |
| Patron creation | `core-mechanics/topics/001.md` and `002.md` |
| Character creation | `core-mechanics/topics/003.md` through `005.md` |
| Skills and talents | `core-mechanics/topics/005.md` and `006.md` |
| Tests | `core-mechanics/topics/011.md` |
| Influence, Superiority, combat turns | `core-mechanics/topics/012.md` |
| Actions, attacks, damage, wounds | `core-mechanics/topics/013.md` |
| Injuries, healing, Fate, corruption | `core-mechanics/topics/014.md` |
| Downtime and GM guidance | `core-mechanics/topics/014.md` through `016.md` |
| Imperium and major factions | `core-flavor/topics/003.md` and `004.md` |
| Macharian Sector and worlds | `core-flavor/topics/004.md` through `009.md` |

## Campaigns

- [Campaign 001](campaign-001/README.md)
