# 03 — Product Teardown: What PandaOS Actually Does

**Owner:** research session 1 · **Status:** findings complete · **Sources:** see ledger

This is the raw "what exists" document. It records observed behaviour from PandaOS's public site and 129-page public documentation so that implementers can build parity without re-researching. Anything we intend to do differently is in `01-vision.md` and `04-tech-stack.md`.

> **Legal/ethical note:** We are re-creating a *capability set*, not copying code, assets, trademarks or UI. All images in `research/reference-images/` are for private reference only and must not be shipped in the product.

---

## 1. Product shape

PandaOS is a desktop-first "local AI workstation" that brings code, tools, external apps and AI agents into one environment.[1] It positions itself as *work orchestration* with a *visual workstation* surface, *system-wide* context, a *global knowledge graph* for memory, and automatic hot-swapping when a plan hits its limit — in contrast to AI app builders (app generation / sandbox / no memory), AI coding editors (code assistant / folder context / RAG), and terminal agents (task execution / session context / manual key swap).[1]

Built-in apps named publicly: Asana, Gmail, Google Calendar, Google Chat, Google Drive, Google Tasks, HubSpot, Jira, Microsoft Files, Microsoft Outlook, Microsoft Teams, Notion, Slack, Supabase, Trello and Vercel — each opening in its own view inside the workspace.[7]

PandaOS's own engineering job posting lists the stack as **TypeScript, Next.js, Node.js and Electron**.[31] That is useful context but not our decision; see `04-tech-stack.md`.

---

## 2. Chat

A chat is where work is requested and watched. Each action — editing a file, running a command, using a connected app — appears as a **card** in the conversation with header, timer, input, output and error state. One message may produce five or six cards.[14]

Per-message choices besides the text:[14]

- **Model** — switchable between messages without a new chat.
- **Mode** — Ask first / Auto-edit / All permissions / Plan.
- **Context** — files, images and email attached to the message.
- **Agent** — optional role with its own model, permissions, skills and apps.
- **App or skill** via `@`, command via `/`.

The **Tools menu** toggles capabilities per chat: image generation, generative UI, agent models, enhanced plans, spotlight and Director. A "Not connected" row appears only when a tool server the chat uses needs attention.[14]

**Two rings:** the *context ring* shows how full the current chat's context window is (`/compact` summarises and continues; a "Context Full" error card offers "Compact and retry"); the *usage ring* shows plan usage across all chats, turning amber past 70% and red past 90%, with a breakdown of session/weekly limits and reset countdowns.[14]

**Steering:** typing while a turn is running gives two actions — Enter queues the message for the next turn; Cmd/Ctrl+Enter *steers* it into the live run, landing at the next tool call. Steering is text-only, capped at 5,000 characters, and unsupported on OpenCode; a late steer is sent as a normal follow-up rather than dropped.[29]

**Plan mode:** reads and researches only; write/command tools are refused while planning. The plan card offers "Yes in a fresh chat with All permissions", "Yes with All permissions", "Yes manually approve edits", or "Tell Panda what to change"; plans support inline comment markup and repeated revision rounds.[26]

**Progress:** enhanced "plans" live outside the chat as durable documents made of *slices*. A slice moves through design → build → review, one chat at a time, with checkpoints that wait for the user; plans can be exported as Markdown or shared at a public URL.[27]

**Subagents** appear as cards with agent kind, activity, timer and tool count; nested subagents appear inside their parent's card.[14] **Rewind** restores files to the state at a sent message (snapshots expire after 30 days; forked chats have no earlier points).[28]

---

## 3. Permissions, sandbox and review

Four modes:[18]

| Mode | Claude Code behaviour |
|---|---|
| All permissions | Every tool runs without asking, including shell |
| Auto-edit | File edits run automatically; shell still asks |
| Plan | Read/research only; proposes a plan before changing anything |
| Ask first | Asks before every file change and every command |

Auto-approve can be enabled by category (file writes, bash execution), which removes prompts for that whole category in every chat — called out with an explicit warning in the docs.[18] Additional allowed tools and trusted sites complete the settings page.

**Connected apps** get three levels: app tools Always ready / When a chat needs them / Off; and per tool **Auto** (reading), **Ask** (sending, deploying) or **Off**.[15] The docs' own guidance is "Auto for reading, Ask for anything that leaves the building."

**Limited Execution Environment:** fences the engine to the project folder plus `~/.pandaos`, each engine's own settings and temp folders. Access presets add Git SSH keys, npm/Node cache, Homebrew, AWS credentials, GPG, Docker config, Python/pip cache and Rust/Cargo. MCP capability tiers are Project-scoped / Read-only / Full; the built-in browser is disabled in a limited chat. Network is Full / Localhost only / Off. Enforcement uses `sandbox-exec` on macOS, bubblewrap on Linux, and a Windows-specific mechanism.[19]

**Review panel:** every changed file with +/− lines, split or unified diff, line comments, per-file "Revert changes", and commit from the Git panel.[28]

**Unattended runs** have three sandbox levels: Restricted (limited set, never asks), Rules (pre-allowed calls only, otherwise pause) and Full.[4]

---

## 4. Connections, engines and failover

A **connection** is one route to models: PandaOS Cloud, Free Mode (pooled free tiers), Claude subscription, OpenAI Codex, OpenCode Go, your API keys, Anthropic Agent SDK, Claude on AWS Bedrock, or local/custom endpoints (Ollama, LM Studio, KoboldCpp, llama.cpp, any OpenAI-compatible address).[22][23]

Each chat remembers its connection; changing one chat never changes the default or other chats; switching mid-conversation carries the thread across without re-sending. **Permissions do not follow the connection** — tool access and execution environment stay put.[23] Each connection has Account / Models / Tiers tabs and can hold multiple accounts.[23]

Five tiers: **High** (deep work), **Medium** (everyday, new-chat default), **Low** (quick), **Utility** (background jobs like titles and commit messages), **Vision** (image reading for a turn when the chat model cannot see).[24]

For subscriptions, PandaOS launches the provider's **official binaries** (Claude Code, Codex, OpenCode); the provider's own login command writes credentials to its own store, and PandaOS states it never receives, reads or forwards the token.[8][23] **Usage-limit failover** moves a turn that hits a limit to the next connection with usage left, in a configured order.[5][23]

---

## 5. Multi-project and worktrees

Several projects stay active in one sidebar; each chat shows running / waiting / done across all projects. Terminal, browser and files opened by a chat stay with that chat when you return.[3] A branch can be given its own **worktree** and its own chat, so two features in one project run side by side without interfering. Cross-project planning and an "In Progress" board are part of the same workspace.[3]

---

## 6. Apps and connectors

Connect once via OAuth or token, then use in every chat. Google and Microsoft apps group under one sign-in; Supabase/Vercel take a generated token; Jira takes email + API token + site URL. Project-scoped apps stay inactive until the project is linked to a resource.[15] Spotlight opens an app's tab beside the chat while the agent works. Apps can be **built by describing them** in chat and imported from a folder or URL; each app declares which accounts, integrations, web access, APIs and folders it may use, and asks in its own chat before using anything else.[7]

**Database app:** BigQuery plus generic SQL (PostgreSQL, MySQL, MariaDB, SQL Server, Azure SQL, SQLite, Redshift, CockroachDB, Oracle). Explorer / Query / History views. Natural-language questions produce SQL and a table or chart; BigQuery queries get a cost estimate and can be held back above a limit. Modes: Safe Mode (structured builder, writes blocked), Direct SQL, No AI Access; AI Data Access toggle; exclusions for databases/schemas/tables.[16]

---

## 7. Atlas (knowledge layer)

Atlas turns sessions into linked **pages** about decisions, problems, workflows and tools. A knowledge map shows all pages grouped and connected. Each page links to pages it touches, carries dates and originating sessions, and is searchable from any project. Work is read in the background and written without user effort; saying "remember" files a note into an Atlas inbox, normally within minutes.[6]

Scope is per-project plus **Global** for things that apply everywhere (e.g. how you write). Pages are stored **on the user's machine as Markdown in a folder PandaOS manages, with every change versioned**. User edits are authoritative: Atlas may add to a page but never rewrites the user's words; agent changes are listed in Review and can each be undone. Every chat can search and read Atlas; mentioning it makes a chat look there first, and "Ground every message" adds matches to each turn.[6]

---

## 8. Automations

Describe a routine in chat, inspect the generated trigger and steps in a visual builder, then let it run. Triggers: **schedule** (hourly, weekday, specific time, cron), **webhook**, **app event**, **manual**. Step types: **AI step**, **Agent** (full autonomous session), **Condition**, **Output** (file/toast/chat), plus any connected app action.[4]

Automations can be project-local or global. Default sandbox is **Rules**; unmatched calls pause and ask; scheduled runs always use Limited. Built-in apps are polled at a configurable interval; webhooks and user-built app events fire immediately. Runs continue in the system tray with no window open; a missed run happens once on wake or is skipped by preference. Each automation keeps its last 10 runs with trigger time, duration, cost and every tool call, and notifies on completion. Events that can trigger runs include Gmail, Calendar, Tasks, Chat, Drive, GitHub, Vercel, Supabase, Trello and database queries.[4]

---

## 9. Director

A Director chat orchestrates **full chats** across projects rather than in-chat subagents. It starts real chats with their own history/tools/project, adopts chats started elsewhere, shows all of them on one status map, routes every question to the orchestrator in one line and passes back the answer it was given (never a guess). A Director sees every project and can run other Directors. It can wake on a schedule, a repeat, or a watch on a deploy, URL, file or another chat — watches and repeats end after at most 12 hours. Voice control is supported.[9]

---

## 10. Design app

Describe an idea in chat and get clickable prototypes, mockups, documents, motion pieces, product demos and slide decks on a design canvas. Motion uses a scrub/trim timeline exported to MP4. Product demos record a page or screen with click ripples, per-click zoom, backdrop and narration. Design systems can be imported from a style guide, CSS, token export or PDF and are reused by both the user and the agent. Slide decks come from an outline with PPTX and Google Slides export. Handoff to code passes frozen HTML, design tokens, the brief and **an ID for every element**.[2]

---

## 11. Voice, mobile and enterprise (observed)

**Voice:** speech-to-text can run on-device (one-time model download), in the cloud, or on the user's key. Hold-to-talk or hands-free; auto-submit on pause or keyword submit ("submit", "steer", "clear dictation", "stop listening", "navigate to …"). Spoken replies optionally summarise aloud while the full answer stays in chat; a mini orb follows the user between screens; a custom dictionary fixes names and terms.[30]

**Mobile:** an encrypted listener on the local network pairs by QR; the phone runs chats, approvals, apps, files/Git, Directors and voice while the computer does the work. Tailscale can expose it remotely. Devices can be individually revoked or all revoked at once.[17]

**Enterprise:** shared workspaces, a governance layer with a permission matrix, approved-model allowlist through a gateway, per-team spend caps, versioned policies with rollback, MCP allowlists, EU-region model pinning, sensitive-data guardrails, one-step offboarding and audit export.[11][12]

---

## 12. Pricing signals (useful for scoping, not for us)

Community tier is free with limited usage, BYO key, Atlas on one project, 5 connected apps and 5 shared artifacts with 7-day retention. Pro tiers add multiple subscriptions with failover, Atlas on all projects, unlimited apps/artifacts, watermark-free exports and a mobile app. Enterprise adds governance. Credits are priced at provider API price + a 10% service fee.[8]

---

## Reference images

20 images were downloaded to `research/reference-images/` covering the interface, multi-project, agent workflows, session-limit bypass, project memory, AI-native dev environment, connected apps, all eight use cases, and five documentation screenshots. See `research/reference-images/INDEX.md` for the mapping and original URLs.

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
[11] https://pandaos.ai/enterprise
[12] https://pandaos.ai/business
[14] https://docs.pandaos.ai/docs/chat/interface
[15] https://docs.pandaos.ai/docs/apps/connecting
[16] https://docs.pandaos.ai/docs/apps/database
[17] https://docs.pandaos.ai/docs/apps/mobile-access
[18] https://docs.pandaos.ai/docs/help/permissions
[19] https://docs.pandaos.ai/docs/help/execution-environment
[22] https://docs.pandaos.ai/docs/get-started/install
[23] https://docs.pandaos.ai/docs/help/connections
[24] https://docs.pandaos.ai/docs/help/models
[26] https://docs.pandaos.ai/docs/chat/plan-mode
[27] https://docs.pandaos.ai/docs/chat/progress
[28] https://docs.pandaos.ai/docs/projects/checking-edits
[29] https://docs.pandaos.ai/docs/chat/steering
[30] https://docs.pandaos.ai/docs/chat/voice
[31] https://www.pandata.de/career/full-stack-developer
