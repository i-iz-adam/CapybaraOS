# 06 — Data Model & Storage Layout

**Owner:** research session 1 · **Status:** proposed · **Depends on:** `05-architecture.md`

---

## 1. On-disk layout

```
~/.capybaraos/
├── state.sqlite            # event log, chats, tasks, approvals, automations, index
├── state.sqlite-wal
├── config.toml             # user preferences, modes, caps
├── secrets/                # OS keychain handles only — no plaintext tokens
├── memory/global/          # global knowledge pages (Markdown + .meta)
├── connectors/             # connector manifests installed by user
├── plugins/                # installed plugins
├── logs/                   # local rolling logs, opt-in analytics only
└── snapshots/              # per-turn file snapshots (30-day retention)

<project>/.capybaraos/
├── rules.md                # project rules, user-authored, authoritative
├── agents/*.md             # project agents
├── skills/*/SKILL.md       # project skills
├── memory/*.md             # project knowledge pages
├── automations/*.toml      # project automations
└── state.json              # dev-server command, linked app resources, UI state
```

Everything user-editable is Markdown/TOML on disk; SQLite is an index and event log, never the only copy of user knowledge. This mirrors the versioned-local-Markdown approach that makes knowledge pages user-owned and undoable [6].

---

## 2. Core entities

| Entity | Purpose | Notable fields |
|---|---|---|
| `Workspace` | Root container | id, created_at, schema_version |
| `Project` | A folder bound to state | id, path, name, coding_tools, template_id, created_at |
| `Chat` | One conversation in one project | id, project_id, title, engine_id, model_tier, mode, agent_id, status, created_at |
| `Turn` | One user message + its work | id, chat_id, parent_id, started_at, finished_at, token_count, cost, engine_id |
| `Message` | Content in a turn | id, turn_id, role, body, attachments_json, edited_at |
| `Event` | Append-only log of everything that happened | id, turn_id, kind, payload_json, ts, actor |
| `ToolCall` | One tool invocation | id, turn_id, name, input_json, output_json, status, duration_ms |
| `Approval` | A pending or resolved request | id, turn_id, tool_call_id, risk, rationale, decision, decided_at |
| `AuditEntry` | Immutable record of an action/policy decision | id, actor, action, target, policy_id, decision, ts |
| `Connection` | A route to models | id, kind, provider, display_name, is_default, caps_json |
| `ProviderAccount` | One account inside a connection | id, connection_id, label, keychain_handle, active |
| `ToolGrant` | Permission for a tool in a scope | id, scope, tool_name, level (auto/ask/off) |
| `App` | Built-in, connected or user-built app | id, kind, manifest_json, scope (global/per_project) |
| `Connector` | MCP server registration | id, app_id, transport, command_or_url, capabilities_json |
| `ProjectAppLink` | Project → resource binding | id, project_id, app_id, resource_id, credentials_handle |
| `Automation` | A repeatable workflow | id, project_id?, trigger_json, steps_json, sandbox_profile, enabled |
| `AutomationRun` | One execution | id, automation_id, started_at, duration_ms, cost, status, trace_json |
| `MemoryPage` | Index row for a Markdown page | id, project_id?, path, title, kind, version, updated_at |
| `MemoryLink` | Edge between pages | id, from_page, to_page, relation |
| `Snapshot` | File state before a turn | id, turn_id, path, content_before, created_at |
| `Plan` / `Slice` | Durable multi-step work | id, project_id, title, status, slices_json, checkpoints_json |
| `Delegate` | A chat managed by an orchestrator | id, orchestrator_chat_id, chat_id, status, last_update |
| `Artifact` | Shared exported object | id, project_id, kind, path_or_url, expires_at |

---

## 3. Schema sketch (SQLite)

```sql
CREATE TABLE projects (
  id TEXT PRIMARY KEY, path TEXT NOT NULL UNIQUE, name TEXT NOT NULL,
  coding_tools INTEGER NOT NULL DEFAULT 1, template_id TEXT,
  created_at INTEGER NOT NULL
);
CREATE TABLE chats (
  id TEXT PRIMARY KEY, project_id TEXT NOT NULL REFERENCES projects(id),
  title TEXT, engine_id TEXT, model_tier TEXT, mode TEXT NOT NULL DEFAULT 'auto_edit',
  agent_id TEXT, status TEXT NOT NULL, created_at INTEGER NOT NULL
);
CREATE TABLE turns (
  id TEXT PRIMARY KEY, chat_id TEXT NOT NULL REFERENCES chats(id),
  engine_id TEXT, started_at INTEGER, finished_at INTEGER,
  tokens INTEGER DEFAULT 0, cost REAL DEFAULT 0
);
CREATE TABLE events (
  seq INTEGER PRIMARY KEY AUTOINCREMENT, turn_id TEXT NOT NULL,
  kind TEXT NOT NULL, payload TEXT NOT NULL, ts INTEGER NOT NULL, actor TEXT
);
CREATE INDEX idx_events_turn ON events(turn_id, seq);
CREATE TABLE approvals (
  id TEXT PRIMARY KEY, turn_id TEXT NOT NULL, tool_call_id TEXT,
  risk TEXT, rationale TEXT, decision TEXT, decided_at INTEGER
);
CREATE TABLE audit_entries (
  id TEXT PRIMARY KEY, actor TEXT, action TEXT, target TEXT,
  policy_id TEXT, decision TEXT, ts INTEGER NOT NULL
);
CREATE TABLE memory_pages (
  id TEXT PRIMARY KEY, project_id TEXT, path TEXT NOT NULL UNIQUE,
  title TEXT, kind TEXT, version INTEGER DEFAULT 1, updated_at INTEGER
);
CREATE VIRTUAL TABLE memory_fts USING fts5(title, body, content='memory_pages');
CREATE VIRTUAL TABLE memory_vec USING sqlite_vec(vec);
CREATE TABLE automations (
  id TEXT PRIMARY KEY, project_id TEXT, trigger_json TEXT NOT NULL,
  steps_json TEXT NOT NULL, sandbox_profile TEXT DEFAULT 'rules', enabled INTEGER
);
CREATE TABLE snapshots (
  id TEXT PRIMARY KEY, turn_id TEXT NOT NULL, path TEXT NOT NULL,
  content_before BLOB, created_at INTEGER NOT NULL
);
```

`PRAGMA journal_mode=WAL; PRAGMA foreign_keys=ON;` on every connection.

---

## 4. Event kinds

`user_message`, `assistant_delta`, `tool_request`, `tool_result`, `tool_error`, `approval_requested`, `approval_resolved`, `file_snapshot`, `file_changed`, `plan_proposed`, `plan_approved`, `subagent_started`, `subagent_finished`, `engine_switched`, `compacted`, `memory_written`, `automation_fired`, `artifact_created`.

The event log is the source of truth for a chat. Rendering is a projection of it; rewind, replay, share-to-web and crash recovery all read the same stream.

---

## 5. Retention and privacy

| Data | Retention | Location |
|---|---|---|
| Chats and events | Until deleted by user | Local SQLite |
| File snapshots | 30 days | `~/.capybaraos/snapshots/` |
| Automation traces | Last 10 runs by default, configurable | Local SQLite |
| Memory pages | Until deleted; version history kept | Markdown + SQLite index |
| Secrets | OS keychain handles only | OS keychain |
| Telemetry | Not collected by default | — |
| Crash reports | Opt-in only | Local until user sends |

---

## 6. Migration policy

- Migrations are numbered SQL files applied in order at startup; the current version is stored in `PRAGMA user_version`.
- Migrations must be additive where possible; destructive migrations require a backup snapshot first.
- Down-migrations are not supported; users on older builds keep their data via forward-only compatibility.
- Schema changes require an ADR and a test that migrates a fixture database from the previous two versions.

## Sources

[6] https://pandaos.ai/features/atlas
