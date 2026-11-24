# CapybaraOS — Start Here

> **Entry point for every agent, contributor and session.** If you only read one file, read this one.

CapybaraOS is an open-source, local-first AI workstation: one desktop application that unifies projects, code, terminal, browser, connected apps, AI agents, automations, and persistent memory across Windows, macOS and Linux. It is an independent re-imagining of the product category demonstrated by [PandaOS](https://www.pandaos.ai/), not a copy of its code or brand.

**Repository:** <https://github.com/i-iz-adam/CapybaraOS>  
**Status:** Pre-implementation. Research and specification phase complete.  
**Last updated:** 2026-11-24  

---

## Reading order

Read in this order; each document assumes the previous ones.

| # | Document | What it gives you |
|---|---|---|
| 0 | `00-START-HERE.md` | Orientation, rules, current status |
| 1 | [`docs/01-vision.md`](docs/01-vision.md) | Why this exists, principles, positioning, non-goals |
| 2 | [`docs/02-target-features.md`](docs/02-target-features.md) | The complete feature inventory with IDs and priorities |
| 3 | [`docs/03-product-teardown.md`](docs/03-product-teardown.md) | Detailed findings from researching PandaOS |
| 4 | [`docs/04-tech-stack.md`](docs/04-tech-stack.md) | Chosen stack, alternatives, performance budget |
| 5 | [`docs/05-architecture.md`](docs/05-architecture.md) | Components, boundaries, data flow, extension points |
| 6 | [`docs/06-data-model.md`](docs/06-data-model.md) | Core entities and storage layout |
| 7 | [`docs/07-security-and-permissions.md`](docs/07-security-and-permissions.md) | Sandboxing, approvals, secrets, privacy |
| 8 | [`docs/08-roadmap.md`](docs/08-roadmap.md) | Build order, phases, dependencies, exit criteria |
| 9 | [`docs/09-agent-workflow.md`](docs/09-agent-workflow.md) | **How multiple agents/sessions must work together here** |
| 10 | [`docs/10-glossary.md`](docs/10-glossary.md) | Shared vocabulary |
| — | [`research/source-notes.md`](research/source-notes.md) | Raw cited research notes |
| — | [`research/reference-images/INDEX.md`](research/reference-images/INDEX.md) | 20 downloaded UI reference images |

---

## Rules for working in this repository

1. **One document owner at a time.** Before editing a doc, claim it in `docs/09-agent-workflow.md` → *Active claims*. Append-only sections are also fine; never silently rewrite another session's section.
2. **Read `docs/01-vision.md` and `docs/04-tech-stack.md` before writing code.** They contain the constraints that decide architecture.
3. **Cite sources for factual claims about PandaOS.** Use the numbered citation style in `research/source-notes.md` and the ledger at `research/citation-ledger.json`. Do not invent URLs.
4. **Feature IDs are stable.** `F-xx`, `P-xx` and `A-xx` identifiers in `docs/02-target-features.md` are referenced by the roadmap. Never renumber; mark something `DEFERRED` instead.
5. **Decisions go in ADRs.** Create `docs/adr/NNNN-short-title.md` for any reversible-in-principle-but-expensive-in-practice choice. Format: Context / Decision / Consequences / Alternatives.
6. **Small commits, conventional prefixes.** `docs:`, `feat:`, `fix:`, `chore:`, `test:`. One logical change per commit.
7. **Safety before autonomy.** Do not implement a capability that writes files, runs shell commands, spends money or sends messages until the permission/review layer in `docs/07-security-and-permissions.md` exists for it.
8. **Performance is a feature.** Every PR that adds a background process, an indexer, a watcher or a renderer dependency must state its idle CPU/RAM impact against the budget in `docs/04-tech-stack.md`.

---

## Current state

- [x] Product research (marketing site, feature pages, public docs, pricing, enterprise)
- [x] Reference image collection (20 images, 4.3 MB)
- [x] Source ledger with 36 registered sources
- [x] Feature inventory and prioritisation
- [x] Tech stack decision + performance budget
- [x] Architecture and data model
- [x] Security model
- [x] Phased roadmap
- [ ] Repository scaffolding (CI, editor config, license)
- [ ] Phase 0 implementation
- [ ] First runnable build

---

## Quick facts

| Question | Answer |
|---|---|
| What are we building? | A local-first desktop AI workstation for orchestrating work across projects, apps and agents |
| Which platforms? | Windows, macOS, Linux on day one; mobile companion after Phase 8 |
| Why not Electron? | Resource use matters for an all-day app; see `docs/04-tech-stack.md` |
| What is the hardest part? | The permission/review/undo layer — build it first |
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
├── docs/
│   ├── 01-vision.md
│   ├── 02-target-features.md
│   ├── 03-product-teardown.md
│   ├── 04-tech-stack.md
│   ├── 05-architecture.md
│   ├── 06-data-model.md
│   ├── 07-security-and-permissions.md
│   ├── 08-roadmap.md
│   ├── 09-agent-workflow.md
│   ├── 10-glossary.md
│   └── adr/                        # Architecture Decision Records
├── research/
│   ├── source-notes.md
│   ├── citation-ledger.json
│   ├── fetch_images.py
│   └── reference-images/           # 20 UI/UX reference images + INDEX.md
└── (implementation packages land here in Phase 0)
```
