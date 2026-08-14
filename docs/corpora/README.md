# Private document corpora

Magnus-docs is the local home for user-owned document sources, extraction
artifacts, semantic streams, and retrieval indexes shared by sibling projects.
The private files live beneath the repository's ignored `sources/` directory;
they must not be committed, redistributed, or shipped with a consumer.

## Current layout

- `sources/wh40k-imperium-maledictum/` — Imperium Maledictum core rules,
  Adeptus Mechanicus Player's and GM's Guides, Macharian Requisition Guide,
  and Voll Adventures, including their completed extraction and retrieval
  artifacts.
- `sources/cypher/` — Cypher System and Numenera sources, OCR/transcription
  workspaces, semantic topic folders, indexes, and QA artifacts.

ForMander consumes these corpora locally through ignored compatibility links:

```text
ForMander/sources/wh40k-imperium-maledictum -> Magnus-docs/sources/wh40k-imperium-maledictum
ForMander/sources/cypher                    -> Magnus-docs/sources/cypher
```

The links preserve existing source-relative provenance and retrieval catalogs
without keeping document content in the tabletop application's repository.
A clean checkout may omit the links and private corpus; corpus-dependent tests
must skip in that state rather than downloading or fabricating source text.

## Integrity

Before and after relocation, compare the recursive file count, byte count, and
a path-and-content SHA-256 tree digest. ForMander's corpus verifiers then check
the generated indexes, per-file hashes, bounded topic sizes, and exact source
reassembly through the compatibility links.
