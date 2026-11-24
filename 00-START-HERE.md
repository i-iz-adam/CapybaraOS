# CapybaraOS — Start Here

> **Entry point for every agent, contributor and session.** If you only read one file, read this one.

CapybaraOS is an open-source, local-first AI workstation: one desktop application that unifies projects, code, terminal, browser, connected apps, AI agents, automations, and persistent memory across Windows, macOS and Linux. It is an independent re-imagining of the product category demonstrated by [PandaOS](https://www.pandaos.ai/), not a copy of its code, brand or visuals.

**Repository:** <https://github.com/i-iz-adam/CapybaraOS>  
**Status:** Specification complete, **shell designs specified**. Next: build the shell (Phase S).  
**Last updated:** 2026-11-24  

---

## The build strategy in one paragraph

**Shell first.** Every screen (S-01 – S-30, in [`docs/design/`](docs/design/README.md)) is built as a real, themed (light / dark / mixed), keyboard-reachable UI driven by a minimal fixtures adapter **before** any feature logic. Then Phase 1 swaps the fixtures for the real core behind the same `ShellPort` interface, and features land in finished homes. Focus is **design and functionality — not mock-data testing**: fixtures are capped, never tested, and deleted as real data arrives.

---

## Reading order

Read in this order; each document assumes the previous ones.

| # | Document | What it gives you |
|---|---|---|
| 0 | `00-START-HERE.md` | Orientation, rules, current status |
| 1 | [`docs/01-vision.md`](docs/01-vision.md) | Why this exists, principles, positioning, non-goals, design direction |
| 2 | [`docs/design/README.md`](docs/design/README.md) | **Shell-first design index: tiers, session plan, definition of done, fixtures policy, screen status** |
| 3 | [`docs/design/01`…`07`](docs/design/) | Tokens, frame, chat, panes, feature surfaces, settings/dialogs, components & a11y |
| 4 | [`docs/02-target-features.md`](docs/02-target-features.md) | The complete feature inventory with IDs and priorities |
| 5 | [`docs/03-product-teardown.md`](docs/03-product-teardown.md) | Detailed findings from researching PandaOS |
| 6 | [`docs/04-tech-stack.md`](docs/04-tech-stack.md) | Chosen stack, alternatives, performance budget |
| 7 | [`docs/05-architecture.md`](docs/05-architecture.md) | Components, boundaries, data flow, renderer shell architecture |
| 8 | [`docs/06-data-model.md`](docs/06-data-model.md) | Core entities and storage layout |
| 9 | [`docs/07-security-and-permissions.md`](docs/07-security-and-permissions.md) | Sandboxing, approvals, secrets, privacy |
| 10 | [`docs/08-roadmap.md`](docs/08-roadmap.md) | Build order incl. **Phase S**, dependencies, exit criteria |
| 11 | [`docs/09-agent-workflow.md`](docs/09-agent-workflow.md) | **How multiple agents/sessions work together here** (+ shell-phase rules) |
| 12 | [`docs/10-glossary.md`](docs/10-glossary.md) | Shared vocabulary |
| 13 | [`docs/11-windows-dev-setup.md`](docs/11-windows-dev-setup.md) | Windows prerequisites, commands, packaging for the next session |
| — | [`docs/handoff/`](docs/handoff/) | The current next-session prompt |
| — | [`docs/adr/`](docs/adr/) | Decision records (0001–0006) |
| — | [`research/source-notes.md`](research/source-notes.md) | Raw cited research notes |
| — | [`research/reference-images/INDEX.md`](research/reference-images/INDEX.md) | 20 UI reference images (local-only) + which screen each informs |

---

## Rules for working in this repository

1. **One document owner at a time.** Before editing a doc, claim it in `docs/09-agent-workflow.md` → *Active claims*. Append-only sections are also fine; never silently rewrite another session's section.
2. **Read `docs/01-vision.md`, `docs/design/README.md` and `docs/04-tech-stack.md` before writing code.** They contain the constraints that decide architecture and UI.
3. **Cite sources for factual claims about PandaOS.** Use the numbered citation style in `research/source-notes.md` and the ledger at `research/citation-ledger.json`. Do not invent URLs.
4. **Feature IDs (`F-xx`, `P-xx`, `A-xx`) and screen IDs (`S-xx`) are stable.** Never renumber; mark something `DEFERRED` instead.
5. **Decisions go in ADRs.** Create `docs/adr/NNNN-short-title.md` for any reversible-in-principle-but-expensive-in-practice choice. Format: Context / Decision / Consequences / Alternatives.
6. **Small commits, conventional prefixes.** `docs:`, `feat:`, `fix:`, `chore:`, `test:`. One logical change per commit.
7. **Safety before autonomy.** Do not implement a capability that writes files, runs shell commands, spends money or sends messages until the permission/review layer in `docs/07-security-and-permissions.md` exists for it. *(The shell has none of these capabilities.)*
8. **Performance is a feature.** Every PR that adds a background process, an indexer, a watcher or a renderer dependency must state its idle CPU/RAM impact against the budget in `docs/04-tech-stack.md`.
9. **Shell first, tiers in order.** Build screens chrome → core → feature shells. UI reads data only through `ShellPort`. Follow the **fixtures policy** in `docs/design/README.md`: one capped module, no generators or mock servers, never test fixture content, delete as real data arrives.
10. **Tokens only.** No raw colours, spacing or fonts outside `tokens.css`; every screen checked in light and dark.
11. **Timebox, don't polish.** Ship what meets the screen's definition of done, record gaps in the screen status table, and move on.

---

## Current state

- [x] Product research (marketing site, feature pages, public docs, pricing, enterprise)
- [x] Reference image collection (20 images, 4.3 MB)
- [x] Source ledger with 36 registered sources
- [x] Feature inventory and prioritisation (+ F-101–F-112 shell features)
- [x] Tech stack decision + performance budget (+ ADR 0004 plain-CSS tokens, 0006 CodeMirror 6)
- [x] Architecture and data model
- [x] Security model
- [x] Phased roadmap (Phase S inserted)
- [x] **Shell design specification: 30 screens, tokens (light/dark/mixed), components, a11y, shortcuts** *(design session 2, 2026-11-24)*
- [x] Windows dev setup and session hand-off prompt
- [ ] **Phase 0a — repo scaffold** (pnpm workspace, Vite + React + TS, Tauri window) ← *next*
- [ ] **Phase S — build the shell** (sessions 3–7, see `docs/design/README.md`)
- [ ] Phase 0b — CI + perf harness (parallel with Phase S)
- [ ] Phase 1 — wire the shell to the real core
- [ ] First runnable build

---

## Quick facts

| Question | Answer |
|---|---|
| What are we building? | A local-first desktop AI workstation for orchestrating work across projects, apps and agents |
| Which platforms? | Windows, macOS, Linux on day one; mobile companion after Phase 8 |
| What do we build first? | **The shell** — all screens as real themed UI from fixtures (Phase S) |
| Which themes? | Light, dark, system, plus *mixed* (terminal/editor pinned dark) |
| How is styling done? | Plain CSS custom-property tokens + CSS Modules + Radix; no Tailwind (ADR 0004) |
| Why not Electron? | Resource use matters for an all-day app; see `docs/04-tech-stack.md` |
| What is the hardest part? | The permission/review/undo layer — build it first *after* the shell |
| What is the extension point? | MCP-compatible connectors + a first-party plugin API |
| What must never happen? | User data used for training; tokens read or forwarded by the app; silent writes or sends |

---

## Repository map

```
CapybaraOS/
├── README.md                       # Public-facing project README
├── CONTRIBUTING.md                 # Human + agent contribution rules
├── LICENSE                         # MIT
├── 00-START-HERE.md                # This file
├── .gitattributes  .editorconfig   # Line endings / editor settings (Windows-friendly)
├── docs/
│   ├── 01-vision.md … 10-glossary.md
│   ├── 11-windows-dev-setup.md
│   ├── design/                     # Shell-first design spec (S-01…S-30)
│   │   ├── README.md               # Index, tiers, session plan, DoD, fixtures policy, status
│   │   ├── 01…07-*.md
│   │   └── reference/              # tokens.css (canonical) + shell-main.html (visual ref)
│   ├── handoff/                    # Next-session prompt
│   └── adr/                        # Architecture Decision Records 0001–0006
├── research/
│   ├── source-notes.md
│   ├── citation-ledger.json
│   ├── fetch_images.py
│   └── reference-images/           # 20 UI/UX reference images + INDEX.md (images are gitignored)
└── (apps/, packages/, crates/ land here — see docs/04-tech-stack.md §4)
```
