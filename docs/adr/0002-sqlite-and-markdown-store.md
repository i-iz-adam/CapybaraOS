# 0002 — SQLite plus Markdown as the single local store

- **Status:** proposed
- **Context:** Chats, events, approvals, automations, knowledge pages and indexes all need durable local storage. Knowledge pages must be user-editable, versioned and undoable — a property the reference product achieves with Markdown files on disk [6].
- **Decision:** One SQLite file per workspace for structured state, event log, FTS5 and sqlite-vec embeddings. User-authored knowledge, rules, skills, agents and automation definitions live as Markdown/TOML files on disk; SQLite indexes them. WAL mode, foreign keys, numbered migrations.
- **Consequences:**
  - Good: portable, low-resource, single-file backup; user content remains readable without the app.
  - Bad: two storage models to keep in sync; index rebuild logic needed after external file edits.
- **Alternatives:** Postgres/DuckDB (heavier, non-portable); pure JSON files (poor querying and concurrency); Electron-style LevelDB (opaque to users).

## Sources

[6] https://pandaos.ai/features/atlas
