# CapybaraOS

### Your whole stack. One open workstation.

**CapybaraOS** is an open-source, local-first AI workstation for Windows, macOS and Linux. It brings projects, code, terminal, browser, connected apps, AI agents, automations and persistent memory into one fast desktop environment — with your keys, your data and full control over what the AI is allowed to do.

> **Status: specification phase.** The research, product definition, architecture and roadmap are complete. No runnable build exists yet. Start with [`00-START-HERE.md`](00-START-HERE.md).

---

## The problem

Builders work across editors, terminals, browsers, dashboards, databases, deployment tools, email and scattered AI apps. The tools do not talk to each other, so the person does the integration: handoffs, lost context, slower shipping. AI helps in one tab while the workflow stays fragmented.

A second problem appears when you use these tools all day: they are heavy. CapybaraOS treats **low resource use and responsiveness as first-class requirements**, not polish.

---

## What we are building

| Area | Capability |
|---|---|
| **Workstation** | Many projects open at once; terminal, browser and agent state preserved on switch; worktrees side by side |
| **Chat engine** | Streaming action cards, four permission modes, mid-turn steering, plan cards with approval, subagents, durable multi-step plans |
| **Provider-neutral AI** | Claude / Codex / OpenCode subscriptions, your API keys, local models; per-chat engine; automatic failover when a plan hits its limit |
| **Connected apps** | Gmail, Slack, Calendar, Drive, GitHub, Jira, Supabase, Vercel, databases and more — connected once, used everywhere; MCP for everything else |
| **Persistent memory** | A local, versioned knowledge graph of decisions and solved problems, written as Markdown you own and can undo |
| **Automations** | Routines on schedules, webhooks or app events, running from the tray with a full cost and tool-call trail |
| **Orchestration** | One chat that starts, watches and answers for full agent chats across every project |
| **Design** | Chat-to-prototype, design systems, motion, demos, decks and handoff to code |
| **Voice & mobile** | On-device dictation and voice commands; an encrypted bridge to a phone that stays with you |
| **Safety** | Every file change diffed, reviewable and reversible; every autonomous action audited; secrets in the OS keychain |

Full inventory with stable IDs: [`docs/02-target-features.md`](docs/02-target-features.md).

---

## Design principles

1. **Local-first** — your files, chats and knowledge stay on your machine. No account needed for core use.
2. **Continuity of state** — switching projects never loses a terminal, tab or running task.
3. **Least privilege** — reads auto-run; writes, sends, spends and deploys ask by default.
4. **Reversible by default** — snapshots, Review panel and Rewind on every agent edit.
5. **Provider-neutral** — no model lock-in; subscriptions and keys are yours and billed by their provider.
6. **Open extension surface** — MCP connectors and plugins are first-class.
7. **Light on resources** — built for someone who uses it all day, every day.
8. **Open source** — MIT licensed, no telemetry by default, no training on your data.

---

## Architecture at a glance

```
React renderer  ──IPC──►  Rust core (state, policy, scheduler, store, memory)
                              │
                    engine children · MCP connectors · PTYs · browser tabs
                              │
                    SQLite + local Markdown + OS keychain
```

| Layer | Choice |
|---|---|
| Desktop shell | Tauri 2 — Rust core + system webviews (WebView2 / WKWebView / WebKitGTK) |
| Renderer | TypeScript, React, Vite |
| Core | Rust, Tokio |
| Storage | SQLite (WAL, FTS5, sqlite-vec) + versioned Markdown |
| Extensions | Model Context Protocol + versioned plugin manifest |
| Engines | Official Claude/Codex/OpenCode binaries + OpenAI-compatible API client |
| Platforms | Windows, macOS, Linux; mobile companion later |

Rationale and alternatives: [`docs/04-tech-stack.md`](docs/04-tech-stack.md) · [`docs/adr/`](docs/adr/)

### Performance commitment

Hard budget, enforced in CI: **< 150 MB** core idle RAM, **< 120 MB** renderer RAM, **< 1%** idle CPU, **< 2 s** cold start, **< 25 MB** installer. Details in [`docs/04-tech-stack.md`](docs/04-tech-stack.md).

---

## Documentation

| Document | Contents |
|---|---|
| [`00-START-HERE.md`](00-START-HERE.md) | Orientation, working rules, current status |
| [`01-vision.md`](docs/01-vision.md) | Problem, thesis, principles, positioning, non-goals |
| [`02-target-features.md`](docs/02-target-features.md) | 100+ features with IDs, priority and phase |
| [`03-product-teardown.md`](docs/03-product-teardown.md) | Detailed findings from the reference product |
| [`04-tech-stack.md`](docs/04-tech-stack.md) | Stack decision, alternatives, performance budget |
| [`05-architecture.md`](docs/05-architecture.md) | Components, boundaries, data flows |
| [`06-data-model.md`](docs/06-data-model.md) | Entities, schema, storage layout, retention |
| [`07-security-and-permissions.md`](docs/07-security-and-permissions.md) | Threat model, modes, sandbox, secrets |
| [`08-roadmap.md`](docs/08-roadmap.md) | 11 phases with dependencies and exit criteria |
| [`09-agent-workflow.md`](docs/09-agent-workflow.md) | Multi-agent collaboration contract |
| [`10-glossary.md`](docs/10-glossary.md) | Shared vocabulary |
| [`research/`](research/) | Cited source notes, ledger and 20 reference images |

---

## Roadmap

Phases 0–2 (repo + CI, shell and projects, engines with permissions and review) come first on purpose: the expensive-to-retrofit parts are the event log, provider abstraction, permission gate and undo system. Autonomy is added only on top of a trustworthy core.

See [`docs/08-roadmap.md`](docs/08-roadmap.md) for the full sequence, dependencies and exit criteria.

---

## Contributing

The project is in the specification phase, so documentation, connector design and security review are the highest-leverage contributions right now. Read [`CONTRIBUTING.md`](CONTRIBUTING.md) and the [multi-agent working agreement](docs/09-agent-workflow.md) before opening a PR.

---

## License & attribution

MIT — see [LICENSE](LICENSE).

CapybaraOS is an independent open-source project and is not affiliated with, endorsed by or derived from PandaOS or Pandata. Product research was conducted from publicly available pages and documentation, cited in [`research/source-notes.md`](research/source-notes.md). Reference images are held privately for design study and are not distributed with the software. We do not reuse their code, trademarks, copy or assets.

**No user data is used to train models. No telemetry by default. Your keys stay yours.**
