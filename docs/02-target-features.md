# 02 — Target Feature Inventory

**Owner:** research session 1 · **Status:** v0.1 · **IDs are stable — never renumber**

Priority key: **P0** = required for first usable release · **P1** = required for parity · **P2** = differentiator · **P3** = later / deferred.

Phase numbers refer to [`08-roadmap.md`](08-roadmap.md).

---

## A. Workspace & projects

| ID | Feature | Priority | Phase |
|---|---|---|---|
| F-01 | Local project = a folder bound to chats, apps, terminal and browser state | P0 | 1 |
| F-02 | Project sidebar with many active projects; instant context switch | P0 | 1 |
| F-03 | Per-chat status: running / needs you / done, visible across all projects | P0 | 1 |
| F-04 | Tool state retention — terminal, browser and open files belong to the chat | P0 | 1 |
| F-05 | Git worktrees — a branch gets its own worktree and its own chat | P1 | 4 |
| F-06 | Project starters/templates with files, rules and dev-server command | P1 | 4 |
| F-07 | Per-project "coding tools" switch (terminal, dev server, credentials, git) | P1 | 4 |
| F-08 | Profiles — sets of settings linked to projects | P2 | 9 |
| F-09 | Shared team workspaces | P3 | 10 |

## B. Chat engine

| ID | Feature | Priority | Phase |
|---|---|---|---|
| F-10 | Streaming chat with action cards (read/write/edit/bash/task/web) | P0 | 1 |
| F-11 | Four modes: Ask first, Auto-edit, Plan, All permissions | P0 | 2 |
| F-12 | Mid-turn steering and message queueing | P1 | 3 |
| F-13 | Context-window ring + `/compact` | P1 | 3 |
| F-14 | Usage/quota ring with per-limit breakdown and reset countdowns | P1 | 5 |
| F-15 | Plan cards with revise/approve cycle and inline comment markup | P1 | 3 |
| F-16 | Progress plans: durable slices (design → build → review) with checkpoints | P2 | 6 |
| F-17 | Subagent cards with nested activity and tool counts | P1 | 3 |
| F-18 | `@` mentions and `/` commands for skills, agents and apps | P1 | 4 |
| F-19 | Attachments: files, images, email, long quotes | P1 | 4 |
| F-20 | Edit a previously sent prompt (drops later turns, with warning) | P2 | 6 |
| F-21 | Generative UI answers (tables, charts, boards, forms) | P2 | 7 |
| F-22 | Inbox: one list of approvals, questions, plans and results across chats | P2 | 6 |
| F-23 | Shareable read-only chat links + copy-link-to-chat | P3 | 9 |

## C. Models & connections

| ID | Feature | Priority | Phase |
|---|---|---|---|
| F-24 | Connection abstraction: Cloud (optional), subscriptions, API keys, local endpoints | P0 | 2 |
| F-25 | Per-chat engine/model; switch mid-chat with conversation carried over | P0 | 2 |
| F-26 | Multiple accounts per provider; choose active account | P1 | 5 |
| F-27 | Usage-limit failover to next connection with usage left | P1 | 5 |
| F-28 | Five model tiers: High / Medium / Low / Utility / Vision | P1 | 2 |
| F-29 | Auto router — pick a model per message from task needs | P2 | 7 |
| F-30 | Per-connection spending caps (day/week/month) and subscription caps | P2 | 7 |
| F-31 | Local model discovery (Ollama, LM Studio, llama.cpp, OpenAI-compatible) | P1 | 5 |
| F-32 | Official subscription CLI binaries launched by us; tokens never read or forwarded | P1 | 5 |
| F-33 | Auto Model Router with tier pinning and per-task overrides | P2 | 7 |

## D. Tools, permissions & review

| ID | Feature | Priority | Phase |
|---|---|---|---|
| F-34 | Tool runtime: file read/write/edit, glob, grep, shell, web, subagent | P0 | 2 |
| F-35 | Permission modes with per-engine behaviour | P0 | 2 |
| F-36 | Auto-approve by category; additional allowed tools; trusted sites | P0 | 2 |
| F-37 | Per-tool Auto / Ask / Off levels | P0 | 2 |
| F-38 | Review panel: every changed file with +/- lines, split/unified diff, line comments | P0 | 2 |
| F-39 | Revert a file; Rewind a chat to a message (snapshots, 30-day retention) | P0 | 2 |
| F-40 | Limited execution environment (filesystem fence + MCP capability tier + network policy) | P0 | 2 |
| F-41 | Unattended automation sandbox: Restricted / Rules / Full | P1 | 6 |
| F-42 | Audit log of approvals, tool calls and policy decisions | P1 | 2 |
| F-43 | Never-train guarantee; secrets redaction before prompts leave the machine | P0 | 2 |

## E. Apps & integrations

| ID | Feature | Priority | Phase |
|---|---|---|---|
| F-44 | Built-in app dock; apps open beside chat; Spotlight opens tab on use | P1 | 4 |
| F-45 | Connect once, use in every project; per-app per-tool permission levels | P1 | 4 |
| F-46 | MCP connectors (third-party servers) with per-project scoping | P1 | 4 |
| F-47 | Build an app by describing it; import a web app from folder or URL | P2 | 7 |
| F-48 | Per-project app links — each project binds to its own DB/deploy/board | P1 | 4 |
| F-49 | Database app — explorer, natural-language SQL, chart results, cost estimates | P1 | 4 |
| F-50 | First connector set (see list below) | P1 | 4 |
| F-51 | Connector SDK + community connector registry | P2 | 8 |
| F-52 | Mobile bridge: encrypted local listener, QR pairing, token rotation | P2 | 8 |
| F-53 | Remote machines / relay transport (optional) | P3 | 10 |

**Connector backlog (order of value, expandable via MCP).** Email & calendar: Gmail, Outlook, Google Calendar, Google Tasks; chat: Slack, Teams, Google Chat, Discord; files & docs: Google Drive, Notion, Microsoft Files; delivery: Vercel, Netlify, GitHub Actions; code: GitHub, GitLab, Bitbucket, Linear, Jira, Asana, Trello; data: Supabase, PostgreSQL, MySQL, SQLite, BigQuery, Snowflake, Redshift; CRM: HubSpot, Salesforce; design: Figma; money: Stripe; plus any OpenAI-compatible endpoint and any MCP server.[7][15][16]

## F. Persistent memory ("Atlas" analogue)

| ID | Feature | Priority | Phase |
|---|---|---|---|
| F-54 | Knowledge pages written from sessions: decisions, problems, workflows, tools | P1 | 5 |
| F-55 | Linked notes + knowledge map (grouped, connected) | P1 | 5 |
| F-56 | Project scope vs Global scope; per-project isolation | P1 | 5 |
| F-57 | Pages stored as versioned Markdown in a managed local folder | P0 | 5 |
| F-58 | User edits are authoritative; agent may append but never overwrite; every change undoable | P1 | 5 |
| F-59 | Review queue for agent-authored changes | P1 | 5 |
| F-60 | "Remember this" inbox command + optional ground-every-message mode | P2 | 5 |
| F-61 | Hybrid retrieval: FTS5 keyword + sqlite-vec embedding, on-device by default | P1 | 5 |

## G. Automations

| ID | Feature | Priority | Phase |
|---|---|---|---|
| F-62 | Describe in chat → generated workflow; visual step builder for edits | P1 | 6 |
| F-63 | Triggers: schedule, cron, webhook, app event, manual | P1 | 6 |
| F-64 | Step types: AI step, full agent session, condition, output, connected-app action | P1 | 6 |
| F-65 | Runs from system tray with no window open; catch-up on wake, or skip | P1 | 6 |
| F-66 | Run history: trigger, duration, cost, every tool call, last 10 runs, notifications | P1 | 6 |
| F-67 | Project-scoped or global automations | P1 | 6 |

## H. Multi-agent orchestration ("Director" analogue)

| ID | Feature | Priority | Phase |
|---|---|---|---|
| F-68 | One chat starts, steers and watches full chats across projects | P2 | 6 |
| F-69 | Map of delegate status: working / waiting / done / error | P2 | 6 |
| F-70 | Delegate questions routed to orchestrator; answers passed through, never guessed | P2 | 6 |
| F-71 | Watches: wake on deploy, URL, file, command or chat change (≤12h) | P3 | 7 |
| F-72 | Nested directors (a project can have its own) | P3 | 7 |

## I. Design app

| ID | Feature | Priority | Phase |
|---|---|---|---|
| F-73 | Chat-to-prototype on a design canvas; clickable, versioned | P2 | 7 |
| F-74 | Design systems: import palette/type from CSS, tokens, PDF or style guide | P2 | 7 |
| F-75 | Motion design timeline with scrub/trim; MP4 export | P3 | 7 |
| F-76 | Product demos: record screen/page, click ripples, zoom, narration | P3 | 7 |
| F-77 | Slide decks from an outline; PPTX / Google Slides export | P3 | 7 |
| F-78 | Handoff to code: frozen HTML, tokens, brief, per-element IDs | P2 | 7 |

## J. Developer environment

| ID | Feature | Priority | Phase |
|---|---|---|---|
| F-79 | Embedded editor with diffs and in-place file open | P0 | 1 |
| F-80 | Persistent PTY terminal per chat; shell selection | P0 | 1 |
| F-81 | Built-in browser with persistent tabs, sign-ins and preview of dev server | P1 | 3 |
| F-82 | Dev-server management (command, port, ready detection) | P1 | 3 |
| F-83 | Git panel: status, stage, diff, commit, message generation | P1 | 3 |
| F-84 | Docker panel | P3 | 9 |
| F-85 | Credentials / `.env` handling with redaction | P1 | 2 |

## K. Voice & mobile

| ID | Feature | Priority | Phase |
|---|---|---|---|
| F-86 | Voice orb: hold-to-talk and hands-free; keyword submit | P2 | 8 |
| F-87 | Local STT by default (whisper.cpp), optional cloud/byo-key | P2 | 8 |
| F-88 | Voice commands: submit, steer, clear, pause, navigate, stop reply | P2 | 8 |
| F-89 | Spoken replies, mini orb, custom dictionary | P3 | 8 |
| F-90 | Mobile companion: chat, approvals, apps, files, directors, voice | P2 | 8 |
| F-91 | Tailscale remote exposure with revocable paired devices | P3 | 8 |

## L. Governance & enterprise (later)

| ID | Feature | Priority | Phase |
|---|---|---|---|
| F-92 | Permission matrix per team; model allowlist; MCP allowlist | P3 | 10 |
| F-93 | Per-team budgets enforced at gateway; hard caps | P3 | 10 |
| F-94 | Versioned policies with rollback; audit + evidence export | P3 | 10 |
| F-95 | Publish skills/agents/starters to teams; required skills | P3 | 10 |
| F-96 | EU-region model pinning; sensitive-data redaction | P3 | 10 |

## M. Platform & quality

| ID | Feature | Priority | Phase |
|---|---|---|---|
| F-97 | Windows, macOS, Linux installers + self-update | P0 | 0 |
| F-98 | System tray with automation execution and quick actions | P1 | 6 |
| F-99 | Performance budget enforced in CI | P0 | 0 |
| F-100 | Telemetry off by default; crash reports opt-in | P0 | 0 |

---

## Cross-cutting requirements

These apply to every feature above, not just one row:

- **Every autonomy feature needs an approval path** before it ships (see `docs/07-security-and-permissions.md`).
- **Every stateful feature persists locally in SQLite** and survives restart.
- **Every long-running feature reports status** to the global "needs you" surface.
- **Every extension uses MCP or the plugin API** — no bespoke one-off integrations in core.
- **Every UI panel must be keyboard-reachable** and respect the performance budget.

## Sources

[7] https://pandaos.ai/apps
[15] https://docs.pandaos.ai/docs/apps/connecting
[16] https://docs.pandaos.ai/docs/apps/database
