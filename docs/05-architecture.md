# 05 — Architecture

**Owner:** research session 1 · **Status:** proposed · **Depends on:** `04-tech-stack.md`

---

## 1. Process and trust boundaries

```
┌─────────────────────────────────────────────────────────────────────┐
│                          USER'S MACHINE                            │
│                                                                     │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │ Tauri app process (Rust, trusted)                             │  │
│  │  ┌───────────┬───────────┬──────────┬──────────┬───────────┐  │  │
│  │  │ cap-core  │ cap-store │ cap-tools│ cap-memory│ cap-apps  │  │  │
│  │  │ event log │ SQLite    │ registry │ indexer   │ runtime   │  │  │
│  │  └─────┬─────┴─────┬─────┴────┬─────┴────┬─────┴─────┬─────┘  │  │
│  │        │           │          │          │           │        │  │
│  │  ┌─────▼───────────▼──────────▼──────────▼───────────▼─────┐  │  │
│  │  │ Permission Gate  ·  Approval Queue  ·  Audit Log       │  │  │
│  │  └───────────────────────────┬─────────────────────────────┘  │  │
│  └──────────────────────────────┼────────────────────────────────┘  │
│                                 │ Tauri IPC (commands + events)    │
│  ┌──────────────────────────────▼────────────────────────────────┐  │
│  │ Renderer (React, untrusted UI logic)                         │  │
│  │  panels: chat · files · review · apps · browser · automation │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                     │
│  ┌──────────────────┐ ┌────────────────┐ ┌───────────────────────┐  │
│  │ Engine children  │ │ MCP connectors │ │ PTY / dev-server procs│  │
│  │ (sandboxed)      │ │ (least priv.)  │ │ (project cwd)         │  │
│  └──────────────────┘ └────────────────┘ └───────────────────────┘  │
│                                                                     │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │ Local state: ~/.capybaraos/  +  <project>/.capybaraos/       │  │
│  └───────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                    │
                    │ opt-in, encrypted, user-controlled
                    ▼
       provider APIs · user-built cloud (later) · mobile bridge · Tailscale
```

**Trust rule:** the renderer never touches the filesystem, secrets or processes directly. Every capability goes through a typed Tauri command that passes the permission gate. Engine children and MCP connectors are treated as untrusted: they receive only the tools and paths their chat's policy allows.

---

## 2. Modules

| Crate | Responsibility | Key interfaces |
|---|---|---|
| `cap-core` | Workspace/project/chat/task state; append-only event log; approvals; scheduler | `EventLog`, `PolicyEngine`, `Scheduler` |
| `cap-store` | SQLite schema, migrations, FTS5 + sqlite-vec, snapshots | `Store`, `SnapshotStore`, `SearchIndex` |
| `cap-engine` | Engine adapters, prompt assembly, `TurnEvent` stream, failover | `Engine`, `TurnHandle`, `ModelRouter` |
| `cap-tools` | Built-in tool registry, MCP client, tool-call execution | `ToolRegistry`, `ToolCall`, `McpClient` |
| `cap-memory` | Session → knowledge pages, versioning, hybrid retrieval | `MemoryWriter`, `KnowledgeMap`, `Retriever` |
| `cap-apps` | App manifests, connector secrets, per-project links, app runtime | `AppRuntime`, `Connector` |
| `cap-pty` | PTY lifecycle, terminal state snapshots | `PtyManager` |
| `cap-browser` | Persistent tabs, profile store, preview detection | `BrowserManager` |
| `cap-sandbox` | Platform fences, network policy, capability tiers | `Sandbox`, `NetworkPolicy` |
| `cap-desktop` | Tauri app, tray, IPC, updater, keychain broker | `commands::*`, `events::*` |

---

## 3. A chat turn, end to end

```
User message ──► renderer ──IPC──► cap-core (append UserMessage event)
                                      │
                          assemble context:
                            project files + rules
                            + memory hits (cap-memory)
                            + connected app tools
                            + attachments
                                      │
                          engine adapter starts turn
                          (sandboxed child process)
                                      │
                    ┌─────────────────┴─────────────────┐
                    │  streamed TurnEvents → UI cards    │
                    └─────────────────┬─────────────────┘
                                      │
                            tool call requested
                                      │
                       ┌──────────────▼──────────────┐
                       │ Permission Gate             │
                       │ mode · category · per-tool  │
                       │ scope · trusted sites       │
                       └──────────────┬──────────────┘
                          auto / ask / deny
                                      │
                       execute (cap-tools / MCP)
                       ├─ snapshot before write
                       ├─ emit ToolResult event
                       └─ append AuditEvent
                                      │
                          final answer → renderer
                          memory writer queued (background)
```

Key properties:
- **Steering** injects a message into the running turn at the next tool boundary; the queued-message count is part of turn state.
- **Failover** replaces the engine adapter mid-turn when a limit event arrives, keeping the event log intact.
- **Rewind** uses per-turn file snapshots; the renderer asks for a diff preview before applying.
- **Nothing is written by the renderer** — it only renders events and sends intents.

---

## 4. Automation runtime

```
Trigger (cron | webhook | app event | manual)
        │
        ▼
Scheduler (tray-resident, no window required)
        │
        ▼
Policy profile: Restricted / Rules / Full
        │
        ▼
Steps: AI → Agent → Condition → App action → Output
        │
        ▼
Result stored + notification + cost/token accounting
```

Catch-up policy is per automation: run once on wake, or skip. Scheduled runs always use the Limited environment. Webhook-triggered runs always use Rules mode. Matches PandaOS's observed model [4].

---

## 5. Memory pipeline

```
Chat turns ──► background observer ──► candidate facts
                                          │
                                   dedupe / link
                                          │
                          Markdown page in <project>/.capybaraos/memory/
                                          │
                          SQLite index: FTS5 + embedding (sqlite-vec)
                                          │
                          Review queue → user edits (authoritative)
                                          │
                          Retrieval: hybrid search → context assembly
```

Global pages live in `~/.capybaraos/memory/global/` and are visible to every project. Version history is kept as append-only diffs so any agent change can be undone individually [6].

---

## 6. Extension points

| Extension | Boundary | Stability |
|---|---|---|
| MCP connector | Stdio / HTTP MCP server, declared capabilities | Stable protocol, versioned |
| Plugin | Manifest + WASM or TS module, UI slots, commands, settings | Versioned API, semver |
| Engine adapter | `Engine` trait in `cap-engine` | Internal, may change |
| Connector SDK | Generated TS/Rust types from manifest schema | Stable from v0.3 |
| Theme | CSS custom properties + token file | Stable |

---

## 7. Failure isolation

| Failure | Behaviour |
|---|---|
| Engine child crashes | Turn card shows error; conversation preserved; retry/restart offered |
| MCP server crashes | Tool marked unavailable; "Not connected" row in Tools menu; other tools unaffected |
| Renderer crash | Tauri restarts webview; state restored from event log |
| Core crash | Event log + snapshots allow recovery; tray shows recovery banner |
| Indexer corruption | Rebuild index from Markdown/files; never destructive |
| Database corruption | Last known-good snapshot + WAL recovery; export tool provided |

---

## 8. Deployment and updates

- Signed installers per platform; update checks run from the tray service, never on the UI thread.
- Release channels: stable / beta / nightly (nightly behind Experimental Features).
- No telemetry by default; crash reports require explicit opt-in.
- All data paths documented in `docs/06-data-model.md` and shown in Settings → Privacy.

---

## Sources

[4] https://pandaos.ai/features/automations
[6] https://pandaos.ai/features/atlas
