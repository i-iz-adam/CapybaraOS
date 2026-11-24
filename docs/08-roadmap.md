# 08 — Roadmap & Build Order

**Owner:** research session 1 (revised by design session 2: Phase S added) · **Status:** proposed · **Depends on:** all of `01`–`07`

---

## 1. Why this order

The strongest temptation in a project like this is to start with the impressive surface: the chat, the beautiful panels, the agent doing twelve things at once. That is exactly backwards. The expensive-to-retrofit parts are **the permission gate, the event log, the snapshot/undo system and the provider abstraction**. If agents can write files before those exist, every later feature inherits an unsafe default. So phases 1–2 are deliberately unglamorous: a working shell, a chat that streams, and safety around file changes. Autonomy is added only on top of that.

Third principle (added): **shell first.** Every surface is designed and built as a real, themed UI from fixtures *before* its logic (Phase S, `docs/design/`, ADR 0005). The shell cannot write, run, spend or send, so this does not weaken the safety-first rule — it just gives features finished homes.

Second principle: **each phase must end with something runnable and testable**. No phase ends in "architecture complete".

---

## 2. Dependency graph

```mermaid
graph LR
  P0[Phase 0a<br/>Repo scaffold] --> PS[Phase S<br/>Shell designs built]
  P0 --> P0b[Phase 0b<br/>CI + perf harness]
  PS --> P1[Phase 1<br/>Wire shell: projects + chat]
  P0b --> P1
  P1 --> P2[Phase 2<br/>Engines + permissions + review]
  P2 --> P3[Phase 3<br/>Tools + browser + terminal]
  P3 --> P4[Phase 4<br/>Apps + MCP + connectors]
  P2 --> P5[Phase 5<br/>Memory + failover]
  P4 --> P6[Phase 6<br/>Automations + orchestration]
  P5 --> P6
  P3 --> P7[Phase 7<br/>Design + generative UI]
  P6 --> P8[Phase 8<br/>Voice + mobile]
  P4 --> P9[Phase 9<br/>Plugins + profiles + polish]
  P8 --> P10[Phase 10<br/>Teams + governance]
```

---

## 3. Phases

### Phase 0 — Foundations (1–2 weeks)

**Goal:** a repo where agents can work safely and where performance is measurable.

> **Split (design session 2):** **0a** = minimal scaffold (pnpm workspace, Vite + React + TS app, Tauri window, lint/format, `.gitattributes`) — needed immediately so Phase S can start. **0b** = CI matrix, `perf.yml`, remaining ADR/repo hygiene — runs in parallel with Phase S and must be green before Phase 1.
- Monorepo scaffolding (pnpm + Cargo workspaces), LICENSE, CONTRIBUTING, codeowners, issue templates.
- CI: build matrix (win/mac/linux), `cargo test`, Vitest, formatting/lint, Playwright smoke.
- `perf.yml`: idle RAM/CPU, cold start, installer size budgets from `04-tech-stack.md`.
- ADRs 0001–0003 (Tauri, SQLite, MCP).
- **Exit:** CI green on all three OSes; perf harness reports numbers; ADRs merged.

### Phase S — Shell designs, built (2–4 weeks, ~5 sessions)

**Goal:** every surface in `docs/design/` exists as a real, themed, keyboard-reachable UI driven by fixtures. No engines, no persistence, no real tools.
- Tokens, light/dark/system + mixed surfaces; `ShellPort` + one fixtures adapter (ADR 0004, 0005).
- **Tier A chrome:** frame, rail, sidebar, pane workbench, command palette, overlay system, settings frame (S-01–S-04, S-23 frame, S-24, S-25).
- **Tier B core:** chat + full card catalogue, composer, model switcher, home, editor, files, terminal, browser, review, git, status surfaces (S-05–S-14, S-30).
- **Tier C shells:** inbox, customize, apps, Atlas, automations, Director, design app, settings pages, onboarding (S-15–S-22, S-29).
- Session breakdown and per-screen definition of done: `docs/design/README.md`.
- **Rules:** fixtures capped and never tested; no feature logic; timebox per session; chrome → core → feature shells.
- **Exit:** all Tier A+B screens built per the definition of done; Tier C reachable with empty + populated states; light/dark/mixed verified; renderer idle RSS < 120 MB and project switch < 150 ms measured on the shell; NVDA smoke pass on Home, Chat, Permissions and the Actions modal.

### Phase 1 — Wire the shell: projects and chat (2–4 weeks)

**Goal:** open the app, add a folder as a project, send a message, see streaming text — by replacing the fixtures adapter with the real core, **without editing components**.
- Tauri tray and native frame wiring; tray-resident core process.
- `cap-store` schema + migrations; `Project`, `Chat`, `Turn`, `Event`; Tauri `ShellPort` adapter (ADR 0005).
- Persist workbench layout per chat; tool-state retention model (F-04); sidebar statuses from real events.
- Real PTY terminal (`portable-pty`) and real file tree/editor read + simple edit behind the existing panes.
- Chat streaming through the event log with a stub echo engine; stop button; mode picker stored (enforced in Phase 2).
- Delete the fixtures each slice replaces, in the same PR.
- **Exit:** 3 projects open simultaneously; terminal state survives switching; perf budget holds.

### Phase 2 — Engines, permissions and review (3–5 weeks) ⚠️ *most important*

**Goal:** an agent can edit a file, and you can see, approve and undo it.
- `cap-engine` adapter trait; one adapter (OpenAI-compatible) with streaming `TurnEvent`s.
- Connection/settings UI for API keys; keychain broker; provider-neutral model list.
- Five model tiers; per-chat engine/model; context ring.
- `cap-sandbox`: filesystem fence, network policy, path validation.
- Permission gate, approval cards, per-tool Auto/Ask/Off, trusted sites, auto-approve categories.
- File snapshots, Review panel with diffs and comments, Revert and Rewind.
- Audit log + Settings → Privacy guarantees.
- **Exit:** an agent edits a file in Auto-edit, the diff appears in Review, and Rewind restores it. Nothing left the machine except provider calls.

### Phase 3 — Tool runtime, browser and dev server (2–4 weeks)
- Built-in tools: read/write/edit/glob/grep/bash/web/task.
- Plan mode with plan cards and revise/approve.
- Mid-turn steering + queue; `/compact`; subagent cards.
- Persistent browser tabs, sign-ins, dev-server preview and ready detection.
- Git panel (status/stage/diff/commit), `.env` redaction.
- **Exit:** "build a small page, start dev server, preview it, commit it" works end to end.

### Phase 4 — Apps, MCP and connectors (3–5 weeks)
- App runtime, dock, Spotlight, per-project app links.
- MCP client with capability tiers and per-tool permission UI.
- First connectors: **Gmail, GitHub, Slack, Google Calendar, Supabase, Vercel**, Database app.
- "Not connected" tool-server status handling.
- **Exit:** ask in chat → Gmail draft appears in the app tab → user approves sending.

### Phase 5 — Memory and provider failover (3–4 weeks)
- Memory writer: sessions → Markdown pages, links, knowledge map.
- FTS5 + sqlite-vec hybrid retrieval; per-project and Global scopes.
- Review queue, user-edit authority, per-change undo.
- Multiple accounts per provider, usage-limit failover, usage ring, caps.
- Local model discovery (Ollama / LM Studio / llama.cpp).
- **Exit:** a decision made in project A is recalled in project B; a simulated limit moves the turn to a second connection without losing history.

### Phase 6 — Automations and orchestration (4–6 weeks)
- Scheduler in tray; triggers (cron, webhook, app event, manual); step builder.
- Sandbox profiles; run history with cost and traces; notifications; missed-run policy.
- Director-style orchestrator: delegate chats, status map, question routing, watches.
- Inbox (approvals/questions/plans/results across all chats).
- **Exit:** a weekday standup automation runs with no window open, and a Director coordinates two delegate chats across projects.

### Phase 7 — Design app and generative UI (4–8 weeks)
- Canvas, prototypes, design systems from tokens/CSS/PDF.
- Handoff to code (frozen HTML, tokens, per-element IDs).
- Generative UI components (table, chart, board, form).
- Motion timeline + MP4 export, product demos, slide decks (lower priority within phase).
- **Exit:** describe a screen, get a clickable prototype, hand it to the build in the same project.

### Phase 8 — Voice and mobile (3–5 weeks)
- Local whisper.cpp STT, voice orb, hold/hands-free, keyword commands, dictionary.
- Optional spoken replies and mini orb.
- Encrypted mobile bridge, QR pairing, device revocation, Tailscale option.
- **Exit:** pair a phone, approve a pending decision from it, dictate a message with on-device STT.

### Phase 9 — Plugins, profiles and polish (3–4 weeks)
- Plugin manifest + SDK, community connector registry, settings/profiles.
- Advanced features: edit-sent-prompt, share-to-web, progress plans, Docker panel.
- Keyboard shortcut audit, accessibility pass, UI performance pass.
- **Exit:** a third-party plugin installs from a manifest and adds a panel + command.

### Phase 10 — Teams and governance (later)
- Organization model, permission matrix, model/MCP allowlists, spend caps, versioned policies, audit export, EU pinning, shared starters/skills.
- **Exit:** an admin publishes a policy and every seat picks it up on next launch.

---

## 4. Ordering rules for agents

1. Never start a phase whose dependencies are not `done` (see `00-START-HERE.md` status list).
2. Within a phase, do **security and storage before UI** when both are present.
3. A feature is not done until it has: tests, docs update, audit hooks, and a perf note.
4. **Phase S precedes Phase 1.** Within Phase S build in tier order (chrome → core → feature shells). Never put feature logic in a shell session; never extend fixtures beyond the cap in `docs/design/README.md`.
5. If a phase is too large, split by *vertical slice* (one connector end to end), not by layer ("all UI, then all backend").
6. Prefer one excellent connector over ten stubs — the MCP boundary makes the rest cheap later.

---

## 5. What to build first if time is short

**Shell:** Tier A chrome plus S-05/S-06 (chat + composer) and S-13 (review) — enough to demonstrate the whole thesis visually. **Then a single vertical slice:** project folder → chat → OpenAI-compatible engine → one file edit → approval card → diff in Review → Rewind → commit. That slice proves the whole thesis. Everything else is a variation on it.
