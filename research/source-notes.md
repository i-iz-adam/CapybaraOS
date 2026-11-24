# Research Source Notes

**Owner:** research session 1 · **Method:** direct extraction of public marketing pages and public documentation, plus one engineering job posting and one adjacent open-source project for context.  
**Ledger:** `citation-ledger.json` (36 registered sources). Inline `[n]` numbers in the docs refer to this ledger.

---

## 1. Method and caveats

- Every claim in `docs/03-product-teardown.md` came from a fetched page, not memory. Search-result snippets were treated as hints and only used after extraction where possible.
- PandaOS is in beta; its docs were updated 18–20 Nov 2026 and prices may change [8].
- Where a capability was only announced ("coming soon") it is marked as such and excluded from parity requirements.
- The product is private-source. Nothing here was derived from source code; it is behavioural observation only.
- An unrelated open-source project also named "PandaOS" exists on GitHub [36]. It is a fork of Paseo and is **not** the commercial product at pandaos.ai. It is listed only as a potentially useful architectural reference (Electron daemon + Expo client + MCP), not as a source of truth for this product.

---

## 2. Primary sources by area

| Area | Sources |
|---|---|
| Positioning / comparison / use cases | [1] homepage, [10] use cases, [7] apps |
| Design app | [2] |
| Multi-project / worktrees | [3] |
| Automations | [4] |
| Hot-swap / subscriptions | [5], [8] pricing, [23] connections |
| Atlas / memory | [6] |
| Connected apps / DB | [7], [15] connecting, [16] database |
| Director | [9] |
| Chat internals | [14] interface, [26] plan mode, [27] progress, [29] steering, [30] voice |
| Safety / permissions | [18] permissions, [19] execution environment, [28] checking edits |
| Project setup | [20] templates, [21] starters, [22] install |
| Models / tiers | [24] |
| Mobile | [17] |
| Enterprise | [11], [12] business |
| Docs structure (129 pages) | [13], [32]–[35] |
| PandaOS's own stack | [31] job posting: TypeScript, Next.js, Node.js, Electron |
| Adjacent OSS name collision | [36] |

---

## 3. Key extracted facts (condensed)

1. PandaOS positions as work orchestration with system-wide context and a global knowledge graph, versus app builders/editors/terminal agents [1].
2. Built-in apps listed publicly: Asana, Gmail, Google Calendar, Google Chat, Drive, Tasks, HubSpot, Jira, Microsoft Files, Outlook, Teams, Notion, Slack, Supabase, Trello, Vercel [7].
3. Four permission modes with engine-specific behaviour; auto-approving a category removes every prompt in that category [18].
4. Limited environment fences to project + app data + engine config + temp; presets for SSH, npm, Homebrew, AWS, GPG, Docker, Python, Rust; MCP tiers project-scoped/read-only/full; network full/localhost/off [19].
5. Knowledge pages are Markdown in a managed local folder, versioned, with user edits authoritative and agent changes undoable via Review [6].
6. Connections: Cloud, Free Mode, Claude, Codex, OpenCode Go, API keys, Agent SDK, Bedrock, local/custom; five tiers; per-chat engine; permissions don't follow the connection [22][23].
7. Subscription login uses the provider's official binary; PandaOS states it never receives, reads or forwards the token [8][23].
8. Automations: schedule/webhook/app-event/manual triggers; AI/Agent/Condition/Output/app steps; Restricted/Rules/Full; last-10 run history; tray execution; catch-up on wake [4].
9. Director orchestrates full chats across projects, routes questions, and supports watches capped at 12 hours [9].
10. Design app includes clickable prototypes, design systems, motion timeline, product demos, decks and handoff with per-element IDs [2].
11. Voice supports local/cloud/byo-key STT, hold/hands-free, keyword commands and a custom dictionary [30].
12. Mobile uses an opt-in encrypted LAN listener, QR pairing, revocable device tokens and optional Tailscale [17].
13. Enterprise adds a permission matrix, model allowlist gateway, hard spend caps, versioned policies, EU pinning and audit export [11].
14. PandaOS's engineering stack is TypeScript/Next.js/Node.js/Electron [31] — we choose Tauri/Rust for resource reasons (see `docs/04-tech-stack.md`, ADR 0001).

---

## 4. Gaps and unverified items

- Exact desktop UI framework version and internal architecture are not public `[unverified]`.
- The Windows enforcement primitive behind the Limited environment is described only as a platform-specific mechanism in the public docs [19]; we must choose our own and document it.
- Pricing and plan names are beta and may change [8].
- "PandaOS Cloud" gateway location is stated as Frankfurt in the enterprise FAQ [11]; we are not replicating hosted inference.
- No public source code for the commercial product was reviewed.

---

## 5. Reference images

20 images were downloaded from the public site and docs CDN into `reference-images/` (4.3 MB). They are **reference only** and must not be shipped with CapybaraOS. See `reference-images/INDEX.md`.

## Sources

[1] https://www.pandaos.ai
[2] https://pandaos.ai/features/design
[3] https://pandaos.ai/features/multi-project
[4] https://pandaos.ai/features/automations
[5] https://pandaos.ai/features/hot-swap
[6] https://pandaos.ai/features/atlas
[7] https://pandaos.ai/apps
[8] https://pandaos.ai/pricing
[9] https://pandaos.ai/features/director
[10] https://pandaos.ai/use-cases
[11] https://pandaos.ai/enterprise
[12] https://pandaos.ai/business
[13] https://docs.pandaos.ai/docs
[14] https://docs.pandaos.ai/docs/chat/interface
[15] https://docs.pandaos.ai/docs/apps/connecting
[16] https://docs.pandaos.ai/docs/apps/database
[17] https://docs.pandaos.ai/docs/apps/mobile-access
[18] https://docs.pandaos.ai/docs/help/permissions
[19] https://docs.pandaos.ai/docs/help/execution-environment
[20] https://docs.pandaos.ai/docs/projects/templates
[21] https://docs.pandaos.ai/docs/getting-started/creating-a-project
[22] https://docs.pandaos.ai/docs/get-started/install
[23] https://docs.pandaos.ai/docs/help/connections
[24] https://docs.pandaos.ai/docs/help/models
[26] https://docs.pandaos.ai/docs/chat/plan-mode
[27] https://docs.pandaos.ai/docs/chat/progress
[28] https://docs.pandaos.ai/docs/projects/checking-edits
[29] https://docs.pandaos.ai/docs/chat/steering
[30] https://docs.pandaos.ai/docs/chat/voice
[31] https://www.pandata.de/career/full-stack-developer
[32] https://docs.pandaos.ai/docs/get-started/what-is-pandaos
[35] https://docs.pandaos.ai/docs/get-started/first-project
[36] https://github.com/marushan49/pandaos
