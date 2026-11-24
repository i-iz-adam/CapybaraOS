# Design — Shell-First Specification

**Owner:** design session 2 · **Status:** v0.1 · **Read before:** writing any UI code

CapybaraOS is built **shell first**: every surface of the app is designed and built as a real, themed, keyboard-reachable UI *before* its feature logic exists. Features are then wired into shells that already have a home, so no later session has to invent layout.

This folder is the single source of truth for how the app looks and is laid out. Behaviour, permissions and storage live in the numbered docs (`../01`–`../10`); this folder says **where it goes and what it looks like**.

> Visual inspiration is the layout *pattern* of PandaOS (icon rail → project sidebar → side-by-side panes → composer). Colours, tokens, icons, copy and components are our own. Never ship, trace or copy reference images (see `research/reference-images/INDEX.md`).

---

## Reading order

| # | File | Contents | Screens |
|---|---|---|---|
| 1 | [`01-principles-and-tokens.md`](01-principles-and-tokens.md) | Principles, light/dark tokens, type, spacing, motion, theme mechanics | — |
| 2 | [`02-frame-and-layout.md`](02-frame-and-layout.md) | Window frame, icon rail, project sidebar, pane workbench | S-01 – S-04 |
| 3 | [`03-chat-and-composer.md`](03-chat-and-composer.md) | Chat view, card catalogue, composer, model switcher, home | S-05 – S-08 |
| 4 | [`04-workbench-panes.md`](04-workbench-panes.md) | Editor, files, terminal, browser, review, git | S-09 – S-14 |
| 5 | [`05-feature-surfaces.md`](05-feature-surfaces.md) | Inbox, customize, apps, Atlas, automations, Director, design app, tray, voice, mobile | S-15 – S-22, S-26 – S-28 |
| 6 | [`06-settings-and-dialogs.md`](06-settings-and-dialogs.md) | Settings shell + pages, command palette, dialogs, first run, status surfaces | S-23 – S-25, S-29, S-30 |
| 7 | [`07-components-and-a11y.md`](07-components-and-a11y.md) | Component inventory, state matrix, shortcuts, accessibility | — |
| — | [`reference/tokens.css`](reference/tokens.css) | The token file — canonical values | — |
| — | [`reference/shell-main.html`](reference/shell-main.html) | Static visual reference of the main shell, light + dark | — |

Screen IDs `S-xx` are **stable** (same rule as feature IDs: never renumber, mark `DEFERRED`).

---

## Build tiers

| Tier | Meaning | Screens |
|---|---|---|
| **A — Chrome** | The frame every other screen lives in. Built first, fully. | S-01, S-02, S-03, S-04, S-23 (frame only), S-24, S-25 |
| **B — Core surfaces** | The daily-driver panes. Fully designed, fixture-driven. | S-05, S-06, S-07, S-08, S-09, S-10, S-11, S-12, S-13, S-14, S-30 |
| **C — Feature shells** | Layout, empty state and one populated state only. No logic. | S-15 – S-22, S-23 pages, S-29 |
| **D — Spec only** | Documented here, built when its phase arrives. | S-26, S-27, S-28 |

## Session plan (shell build)

| Session | Scope | Exit |
|---|---|---|
| **3** | Scaffold (pnpm + Vite + React + TS + Tauri window), tokens, theme switch, `ShellPort` + fixtures, S-01 – S-04, S-24 | Frame renders in light + dark, panes resize/collapse, project switch < 150 ms |
| **4** | S-05 – S-08 (chat, cards, composer, switcher, home) | Every card type renders from fixtures; composer states complete |
| **5** | S-09 – S-14 (editor, files, terminal, browser, review, git) | All panes open side by side; review diff split/unified |
| **6** | S-23, S-25, S-29, S-30 (settings, dialogs, onboarding, status) | Every settings page reachable with correct controls |
| **7** | S-15 – S-22 shells (Tier C) | Each reachable from rail/sidebar/palette with empty + populated state |
| **8+** | Phase 1 wiring (see `../08-roadmap.md`) | — |

Sessions may be merged or split; the *order* is binding (chrome → core → feature shells).

---

## Definition of done for a screen

A screen is **built** only when all of these hold:

1. Matches the regions and states listed in its spec (no extra regions, none missing).
2. Uses **tokens only** — no raw colour, spacing or font values outside `tokens.css`.
3. Renders correctly in **light and dark**, and in the "always-dark terminal/editor" mix.
4. Fully keyboard-reachable; visible focus ring; correct roles/labels.
5. Holds at **960 × 600** (minimum) and **1360 × 860** (default) without overlap or layout shift.
6. Renders its empty, populated and error/degraded state from fixtures (see below).
7. One Playwright smoke test: open the screen, assert key regions exist, take one screenshot per theme. **No pixel-diff gating before Phase S exit.**
8. Idle cost: no timers, polling or animation running while the screen is idle (perf budget in `../04-tech-stack.md`).
9. Its row in the status table below is updated.

## Fixtures policy — read this before adding any data

The shell phase exists to settle **layout and interaction**, not data plumbing. To keep every session (and every AI) from sinking time into mock data:

1. **One data seam.** UI reads state only through the `ShellPort` interface (ADR 0005). Fixtures are one adapter behind it; the real Tauri/Rust adapter replaces it in Phase 1 with zero component changes.
2. **One fixtures module** (`apps/desktop/src/shell/fixtures/`, ≤ 400 lines total). No per-screen mock generators, no random data, no faker libraries, no mock servers, no fake LLM backends.
3. **Smallest set that shows every state:** 3 projects (one empty), ≤ 4 chats each, one chat containing **one of every card type**, a 2-file diff, 8 apps (generic glyphs, no third-party logos), 6 knowledge pages, 3 automations, 3 delegates.
4. **A dev-only state switcher** (`?fixture=empty|busy|error`) toggles whole-app states. Do not build per-component storybook matrices.
5. **One canned stream** for chat (scripted ~3 s) so streaming UI can be seen. Nothing else is simulated over time.
6. **Never test fixture content.** Tests assert regions, interaction, keyboard, theme and layout — not that fixture text appears or that mock numbers add up.
7. **Delete, don't extend.** When real data exists for a slice, remove its fixture in the same PR.
8. The shell has **no ability to write files, run commands, spend or send**. Fixtures only. Safety rule 7 in `00-START-HERE.md` stays intact.
9. **Timebox.** If a screen is not at "built" after its session's budget, ship what is done, mark the gaps in the status table and move on. Do not polish a screen beyond its spec before every Tier A/B screen exists.

## Screen status

`—` not started · `spec` specified · `built` meets definition of done

| ID | Screen | Tier | Spec | Built |
|---|---|---|---|---|
| S-01 | App frame + titlebar | A | spec | — |
| S-02 | Icon rail | A | spec | — |
| S-03 | Project sidebar | A | spec | — |
| S-04 | Pane workbench | A | spec | — |
| S-05 | Chat view + card catalogue | B | spec | — |
| S-06 | Composer | B | spec | — |
| S-07 | Model / engine switcher | B | spec | — |
| S-08 | Home / new chat | B | spec | — |
| S-09 | Editor pane | B | spec | — |
| S-10 | Files pane | B | spec | — |
| S-11 | Terminal pane | B | spec | — |
| S-12 | Browser pane | B | spec | — |
| S-13 | Review panel | B | spec | — |
| S-14 | Git panel | B | spec | — |
| S-15 | Inbox | C | spec | — |
| S-16 | Customize hub | C | spec | — |
| S-17 | App detail + actions + connect flow | C | spec | — |
| S-18 | App host + Database app | C | spec | — |
| S-19 | Atlas (knowledge) | C | spec | — |
| S-20 | Automations | C | spec | — |
| S-21 | Director | C | spec | — |
| S-22 | Design app | C | spec | — |
| S-23 | Settings shell + pages | A/C | spec | — |
| S-24 | Command palette | A | spec | — |
| S-25 | Dialogs, toasts, banners | A | spec | — |
| S-26 | Tray + notifications | D | spec | — |
| S-27 | Voice orb | D | spec | — |
| S-28 | Mobile companion | D | spec | — |
| S-29 | First run / onboarding | C | spec | — |
| S-30 | Status surfaces (rings, popovers) | B | spec | — |

---

### Handoff — design session 2, 2026-11-24
- **Changed:** `docs/design/*` (new), `docs/11-windows-dev-setup.md`, `docs/handoff/*`, ADRs 0004–0006; additions to `00-START-HERE.md`, `README.md`, `CONTRIBUTING.md`, `docs/01`, `02`, `04`, `05`, `08`, `09`, `10`, `research/reference-images/INDEX.md`; `.gitattributes`, `.editorconfig`.
- **Decisions:** shell first with a `ShellPort` data seam (ADR 0005); plain-CSS tokens, no Tailwind (ADR 0004); CodeMirror 6 (ADR 0006); roadmap gains Phase S and Phase 0 splits into 0a/0b; Phase 1 becomes "wire the shell".
- **Verified:** documents cross-checked for consistent screen IDs (S-01–S-30), feature IDs (F-101–F-112 appended, none renumbered) and tier assignments. No code was built or run this session.
- **Open questions:** custom Windows titlebar vs native decorations (2 h spike in session 3); exact shortcut set (proposed in `07`, finalise in Settings → Shortcuts); whether to adopt generic glyphs permanently or license brand logos for apps later.
- **Next suggested task:** shell session 3 — see `docs/handoff/session-03-prompt.md`.

