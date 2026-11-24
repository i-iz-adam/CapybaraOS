# 01 — Vision & Positioning

**Owner:** research session 1 · **Status:** agreed for v0.1 · **Read before:** writing any code

---

## The problem

Modern builders work across editors, terminals, browsers, dashboards, databases, deployment tools, email, scripts and scattered AI apps. Those tools do not talk to each other, so the person does the integration by hand. The result is too many handoffs, lost context and slower shipping — the AI helps in one tab while the workflow stays fragmented.[1]

This is the problem statement PandaOS is built around, and it is the one we adopt. Our addition is that the same problem is worse when you use the app for eight or more hours a day: a workstation that is pleasant for 20 minutes becomes hostile when it consumes half your RAM, wakes a fan, or takes four seconds to switch a panel.

## Product thesis

> CapybaraOS is a **local-first AI workstation**. It gives one AI assistant real, system-wide context — your projects, files, apps, history and decisions — and lets it *do* work across them, while you keep explicit, reviewable control over what it may change.

Three claims are load-bearing:

1. **Context is system-wide, not per-tab.** The assistant knows the project, the terminal state, the browser, the connected apps and the accumulated decisions. PandaOS describes this as the difference between operating a workflow and merely generating an app or writing code.[1]
2. **The work happens in the same place as the tools.** Apps open beside the chat, and the assistant acts inside them; a reply drafted in Gmail or an order looked up in Supabase is visible where you are working.[7]
3. **The machine stays yours.** Local storage, your keys, your subscriptions, no training on your data, and an execution environment that can be fenced to a single project folder.[5][19]

## Design principles

| Principle | What it means in practice |
|---|---|
| **Local-first** | Project data, chats, knowledge pages and secrets live on the user's machine. Cloud features are opt-in adjuncts. |
| **Continuity of state** | Switching projects preserves terminal sessions, browser tabs, running chats and agent state. PandaOS calls this "keep tool state".[3] |
| **Least privilege, then approval** | Every tool defaults to the narrowest scope. Reads auto-run; writes, sends, spends and deploys ask by default. |
| **Reversible by default** | Every file change is captured, diffed, reviewable and rewindable before it is committed.[28] |
| **Provider-neutral** | No lock-in to one model vendor. Chats remember their own engine and can switch mid-conversation with history carried over.[23] |
| **Open extension surface** | MCP-compatible connectors and a plugin API are first-class, not an afterthought. Users can build the app they are missing.[7] |
| **Light on resources** | An all-day app must be quiet: low idle memory, near-zero background CPU, instant panel switches. This is a hard requirement, not a nice-to-have. |
| **Open source, no surveillance** | No telemetry by default, no data training, no opaque cloud dependency for core features. |

## Positioning

PandaOS's own comparison puts it against AI app builders, AI coding editors and terminal agents along five axes: primary job, surface, context, memory and session limits.[1]

| Category | Primary job | Surface | Context | Memory | Session limits |
|---|---|---|---|---|---|
| AI app builders | App generation | Chat/prompt flow | Sandbox only | None | Hard daily caps |
| AI coding editors | Code assistant | Code editor | Folder-level | Vector search (RAG) | Locked out until reset |
| Terminal agents | Coding task execution | CLI/terminal | Session-level | Session-based | Manual key swap |
| **PandaOS** | Work orchestration | Visual workstation | System-wide | Global knowledge graph | Hot-swap to next plan |
| **CapybaraOS (target)** | Work orchestration | Visual workstation | System-wide | Local linked knowledge graph + versioned Markdown | Automatic failover across user-owned providers |

We position against the same four axes and add a fifth: **resource footprint and ownership**. The differentiators we should lead with:

- **Truly open and self-hostable** — no account required for core use.
- **Small and fast** — a native Rust core and system webviews instead of a bundled browser runtime.
- **Batteries-included extensibility** — MCP plus a plugin marketplace from the start.
- **Honest permissions** — a visible, auditable decision log for every autonomous action.

## Target users

| Persona | Today | What CapybaraOS gives them |
|---|---|---|
| **Builder / founder** | Juggles multiple tools, projects and AI workflows | One workspace that runs across projects, with a single place to see what is running or waiting |
| **Developer** | Cursor, Claude Code or custom scripts | A full environment with real files, terminal, browser, DB and review, plus subscription failover |
| **Operator** | Repeats the same reports, checks and messages | Automations that run on a schedule or on app events, with a visible run history |
| **Team / org** | Ten AI tools, ten contracts, no oversight | Shared starters, skills and policies with versioned governance (later phase) |

## Success criteria (north star)

| Metric | Target |
|---|---|
| Time from install to first useful completed task | < 10 minutes |
| Projects active at once without state loss | 10+ |
| Agent actions that run without a user approval (by default) | Read-only tools only |
| User data sent to our infrastructure | Zero in core mode |
| Idle memory footprint | See budget in `docs/04-tech-stack.md` |
| Crash-free sessions | ≥ 99.5% |
| Reversibility | 100% of agent file edits recoverable |

## Non-goals

- Not a general-purpose hosted chat UI. There are enough of those.
- Not a replacement code editor on day one — embed a capable editor, but the unit of work is the *task*, not the file.
- Not a cloud-first product. Cloud is an optional transport, never the source of truth.
- Not a model provider. We orchestrate existing engines and APIs; we do not train or host frontier models.
- Not a brand, logo or UI clone of PandaOS. We are re-creating the *capability set* with our own design and an open license.

## Strategic wedge

Start where the pain is sharpest and the implementation is honest: **a fast, local workstation where an AI agent can work across your projects and apps, with every change reviewable and every key yours.** Memory, orchestration, automation and the design app are force multipliers that come after that core is trustworthy.

## Sources

[1] https://www.pandaos.ai
[3] https://pandaos.ai/features/multi-project
[5] https://pandaos.ai/features/hot-swap
[7] https://pandaos.ai/apps
[19] https://docs.pandaos.ai/docs/help/execution-environment
[23] https://docs.pandaos.ai/docs/help/connections
[28] https://docs.pandaos.ai/docs/projects/checking-edits

### Addition from design session 2 — Design direction

- **Shell first.** Every surface is designed and built as a themed, keyboard-reachable shell before its feature logic exists (see `docs/design/README.md`, ADR 0005).
- **Layout inspired, look our own.** The *pattern* — icon rail → project sidebar → side-by-side panes → composer — is shared with the reference product; palette, tokens, icons, copy and components are original (warm neutrals + moss-teal accent, generic glyphs).
- **Light and dark are equal citizens**, plus a "mixed" option that pins terminal/editor surfaces dark inside a light app (`docs/design/01-principles-and-tokens.md`).
