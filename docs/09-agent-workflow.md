# 09 — Multi-Agent Working Agreement

**Owner:** research session 1 · **Status:** binding for all agents and sessions

This repository will be edited by many agents across many sessions. This file is the contract that keeps those edits from colliding. Read it before touching anything.

---

## 1. Claim a document before you edit it

Add a row to the table below, then edit only what you claimed. Remove your row when you commit.

| Document / area | Claimed by | Session | Started | Status |
|---|---|---|---|---|
| `00-START-HERE.md` | research session 1 | initial | 2026-11-24 | done |
| `docs/01`–`08` | research session 1 | initial | 2026-11-24 | done |
| `research/source-notes.md` | research session 1 | initial | 2026-11-24 | done |
| *(free)* | | | | |

Rules:
- One owner per file at a time. If you need to add to someone's file, append a `### Addition from <session>` section instead of rewriting.
- Never renumber feature IDs (`F-xx`, `P-xx`, `A-xx`). Mark obsolete items `DEFERRED` with a date.
- Never change another document's "Status" field.

---

## 2. Handoff format

When you finish a session, leave a handoff block at the end of the document you worked on:

```markdown
### Handoff — <agent/session name>, <date>
- **Changed:** <files>
- **Decisions:** <decisions made and why>
- **Verified:** <commands run and their results>
- **Open questions:** <anything the next agent must decide>
- **Next suggested task:** <one concrete next step>
```

Also append a one-line summary to `00-START-HERE.md` → *Current state*.

---

## 3. Decision records

Any choice that would be expensive to reverse gets an ADR in `docs/adr/`:

```markdown
# NNNN — Short title
- **Status:** proposed | accepted | superseded by NNNN
- **Context:** what problem, what constraints
- **Decision:** what we will do
- **Consequences:** good and bad, including performance impact
- **Alternatives:** what we rejected and why
```

Number sequentially; never reuse a number. Supersede with a new ADR rather than editing an accepted one.

---

## 4. Commit discipline

```
docs: add permission gate algorithm
feat: scaffold Tauri shell and project store
test: add Rewind snapshot regression test
perf: add idle-memory smoke assertion
chore: pin MCP SDK version
```

One logical change per commit. Always run the relevant test before committing. Never commit secrets, downloaded proprietary assets or generated binaries.

---

## 5. Code rules for agents

1. **Read before write.** Read `01-vision.md`, `04-tech-stack.md`, `07-security-and-permissions.md` and the target file before editing code.
2. **Safety first.** If your feature can write, send, spend or deploy, the permission gate and audit hook ship in the same commit.
3. **No silent defaults that widen access.** Ask is the default for anything outgoing.
4. **No new background threads without a perf note.** State expected idle CPU/RAM in the PR description.
5. **No new top-level dependency without justification.** Prefer existing crates/packages; note bundle-size impact.
6. **MCP for integrations.** Do not hand-roll a connector protocol in core code.
7. **Tests with every feature.** Rust unit test + a Playwright path for anything user-visible.
8. **Markdown on disk for user content.** Never make knowledge or rules SQLite-only.

---

## 6. Conflict resolution

- **Doc conflict:** the later handoff wins only if it cites a source or a decision record; otherwise leave both readings with a `TODO(resolve)` note.
- **Architecture conflict:** open an ADR and mark both options; do not merge code until accepted.
- **Feature priority conflict:** refer to `02-target-features.md` IDs and `08-roadmap.md` phase order.
- **Unsure:** write a comment in the doc and move on. Do not block other work.

---

## 7. New session quick-start prompt

Paste this as the first message of a new agent session:

> Read `00-START-HERE.md`, then `docs/01-vision.md`, `docs/02-target-features.md`, `docs/04-tech-stack.md`, `docs/07-security-and-permissions.md`, `docs/08-roadmap.md`, and this file. Claim the document or feature you will work on in the claims table. Do not touch any other file. Follow the commit convention. Leave a handoff block when done.

---

## 8. Reviewer checklist

- [ ] Changes match the claimed scope only
- [ ] Feature IDs unchanged
- [ ] New claims about PandaOS carry a citation from the ledger
- [ ] Security/audit hooks present for any new capability
- [ ] Perf budget statement present
- [ ] Tests added and passing
- [ ] Docs updated
- [ ] Handoff block written
