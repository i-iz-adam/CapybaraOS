# 10 — Glossary

Shared vocabulary. Use these terms exactly in code, UI and docs.

| Term | Meaning |
|---|---|
| **Workspace** | The root of all local state (`~/.capybaraos`). |
| **Project** | A folder on disk bound to chats, terminal/browser state and app links. |
| **Chat** | A conversation in a project. Remembers its engine and model independently of other chats. |
| **Turn** | One user message and all the work that follows it. Unit of snapshots and cost accounting. |
| **Card** | A UI element representing one action (tool call, question, plan, subagent, draft). |
| **Engine** | The program that turns model text into actions (Claude Code, Codex, OpenCode, or our direct API runner). Sometimes called a harness. |
| **Connection** | A configured route to models: subscription, API key, local endpoint, or optional hosted service. Contains accounts, models and tiers. |
| **Tier** | A model slot by job size: High, Medium, Low, Utility, Vision. |
| **Failover** | Moving a turn to another connection when the current one hits a usage limit. |
| **Mode** | How much a chat asks before acting: Ask first, Auto-edit, Plan, All permissions. |
| **Permission gate** | The central component that allows, denies or pauses every tool call. |
| **Approval** | A pending user decision on a tool call or plan. |
| **Review** | The panel where file changes are diffed, commented on, reverted and committed. |
| **Snapshot** | File contents captured before a turn, used by Revert/Rewind. |
| **Rewind** | Restoring files to their state at a previous message. |
| **Steering** | Injecting a correction into a turn that is already running. |
| **Compact** | Summarising earlier context to free context-window space. |
| **Tool** | A callable capability: read, write, edit, bash, glob, grep, web, task, or a connected-app action. |
| **MCP** | Model Context Protocol — the standard way apps expose tools to an agent. Our extension boundary. |
| **Connector** | An MCP server registered as an app, with declared capabilities and permissions. |
| **App** | A first-class panel beside the chat: built-in, connected, or built by the user. |
| **Spotlight** | Automatically opening an app's tab when the agent uses it. |
| **Project app link** | Binding a project to a specific resource (database, deployment, board). |
| **Knowledge page** | A Markdown page in the memory layer describing a decision, problem, workflow or tool. |
| **Knowledge map** | The linked graph view of knowledge pages. |
| **Global memory** | Pages visible to every project (preferences, conventions). |
| **Grounding** | Adding relevant memory pages to a message before it reaches the model. |
| **Automation** | A workflow with a trigger and steps that runs without a user starting it. |
| **Run** | One execution of an automation, with trace, duration and cost. |
| **Sandbox profile** | Restricted / Rules / Full — what an unattended run may do. |
| **Director** | A chat that orchestrates full chats across projects (not in-chat subagents). |
| **Delegate** | A full chat managed by a Director. |
| **Watch** | A short-lived trigger that wakes a Director when a deploy, URL, file or chat changes. |
| **Slice** | A thin, trackable unit of work inside a durable Progress plan. |
| **Checkpoint** | A point in a plan where work stops and waits for the user. |
| **Artifact** | An exported design, document or app shared by link. |
| **Mobile bridge** | The encrypted local service that pairs a phone to the desktop app. |
| **Token** | Both an AI model token (billing/context) and an auth secret. Use `auth token` for the latter in docs. |
| **Perf budget** | The hard idle RAM/CPU/startup targets in `04-tech-stack.md`. |
| **Shell** | The app's chrome and screens built before feature logic: frame, rail, sidebar, workbench, settings, overlays. |
| **Surface** | A top-level screen chosen from the rail (Home, Chats, Customize, Atlas, Inbox, Automations, Director, Design, Settings). |
| **Rail** | The 48 px icon strip for global navigation and pane toggles. |
| **Workbench** | The area right of the sidebar that holds the pane strip. |
| **Pane / Strip** | A tool panel (chat, editor, files, terminal, browser, review, git, app…) / the ordered horizontal list of panes. |
| **Composer** | The message input with mode, model, context and usage controls. |
| **Command palette** | `Ctrl+K` overlay that reaches every action, chat, file and setting. |
| **Screen ID (`S-xx`)** | Stable identifier for a specified screen in `docs/design/`. |
| **Tier (A–D)** | Build priority of a screen: Chrome, Core, Feature shell, Spec-only. |
| **Fixture** | The minimal typed seed data behind the shell; one adapter, size-capped. |
| **ShellPort** | The single interface through which UI reads state and sends intents; implemented by fixtures first, then by the Tauri core. |
| **Mixed theme** | Light app with terminal/editor surfaces pinned dark (`data-surface="dark"`). |
