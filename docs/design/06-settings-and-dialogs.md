# 06 — Settings, Palette, Dialogs & Status (S-23 – S-25, S-29, S-30)

**Owner:** design session 2 · **Tier:** A (S-23 frame, S-24, S-25) / B (S-30) / C (S-23 pages, S-29) · **Reference:** `22-model-connections.png`, `24-mobile-pairing.png`, `21-app-per-tool.png`

---

## S-23 · Settings shell + pages

**Features:** many (see page table) · **Purpose:** every preference, in one predictable place.

```
┌────┬─────────────────────┬──────────────────────────────────────────┐
│    │ ‹ Back              │ 🔍 Search settings…                   /  │
│ R  │ WORKSPACE           │                                          │
│ A  │  General            │  Connections                             │
│ I  │  Appearance         │  The subscriptions, keys and runners…    │
│ L  │  Shortcuts          │  [Subscriptions|API keys|Local|Cloud]    │
│    │  Mobile access      │  ┌──────────────────────────────────┐    │
│    │  Voice              │  │ row │ row │ row                  │    │
│    │  Director           │  └──────────────────────────────────┘    │
│    │ ACCOUNT             │  Default                                 │
│    │  Account · Profiles │  ┌ label + description … control ───┐    │
│    │  Usage · Plan       │                                          │
│    │ AI                  │            (content column ≤ 680)        │
│    │  Models ▾           │                                          │
│    │   Connections …     │                                          │
│    │  Atlas              │                                          │
│    │ SAFETY              │                                          │
│    │  Permissions …      │                                          │
│    │  Privacy            │                                          │
│    │ v0.0.0 · Alpha      │                                          │
└────┴─────────────────────┴──────────────────────────────────────────┘
```

Settings replaces the **sidebar** with its navigation (rail and workbench context stay). `Back` (or `Esc`) returns to the previous surface. Sub-sections (e.g. *Models → Connections, Default, Usage limit failover, Behavior, Image generation*) are anchors inside one scrolling page with a sticky mini-nav. Search filters pages and rows and highlights matches; `/` focuses it (not `Ctrl+F`, which belongs to the focused pane).

**Row patterns:** *Setting row* = label + description left, control right · *Group card* = rounded container of rows with hairlines · *Segmented tabs* at the top of a page · *Danger zone* = bottom group with red-outlined actions · *Info callout* for guarantees and warnings. Controls: toggle, select, segmented, slider (chat scale), text field (masked for secrets), shortcut recorder, button.

### Page catalogue

| Group | Page | Key controls | Features |
|---|---|---|---|
| WORKSPACE | **General** | Startup (open last / home), default project folder, language, updates channel, tray behaviour, close-to-tray | F-97, F-98 |
| | **Appearance** | Appearance system/light/dark, terminal & editor surface (match/dark), density, chat text size, reduce motion, rail items, status bar toggle, sidebar width | — |
| | **Shortcuts** | Searchable table, recorder, reset, conflicts | — |
| | **Mobile access** | Mobile bridge toggle (with the plain-language "starts an encrypted listener" text), paired devices list + revoke / revoke all, QR pairing, *Remote access (Tailscale)* sub-card with numbered how-it-works | F-52, F-91 |
| | **Voice** | STT engine (on-device / cloud / own key), model download, hold vs hands-free, keywords, spoken replies, dictionary | F-86 – F-89 |
| | **Director** | Defaults for delegate permissions, watch limit info (≤ 12 h) | F-68 – F-72 |
| ACCOUNT | **Account** | "No account needed" explainer; optional sign-in (later) | — |
| | **Profiles** | Named setting sets linked to projects | F-08 |
| | **Usage** | Per-connection usage, spend caps (day/week/month), cost history | F-14, F-30 |
| | **Plan** | Placeholder (open source: none) — hidden until needed | — |
| AI | **Models → Connections** | Tabs *Subscriptions · API keys · Local · Cloud (optional)*; rows with account, plan, *Default* tag, expand for Account / Models / Tiers; **Connect** CTA; local discovery list | F-24, F-26, F-31, F-32 |
| | Default | Default connection, model for new chats, reasoning effort (Low→Max), reuse-last toggles | F-28 |
| | Usage-limit failover | Ordered connection list (drag), on/off, test | F-27 |
| | Behavior / Image generation | Auto router, tier pinning, utility-model choice | F-29, F-33 |
| | **Atlas** | Enable, scope defaults, ground-every-message, storage path, review-queue behaviour | F-54 – F-61 |
| SAFETY | **Permissions** | Mode defaults, auto-approve categories (file writes, shell — with red warning), additional allowed tools, trusted sites | F-11, F-35, F-36 |
| | **Plan mode** | Plan-approval defaults | F-15 |
| | **Tool access** | Per-app availability + per-tool Auto/Ask/Off (same matrix as S-17) | F-37, F-45 |
| | **Execution environment** | Filesystem fence + access presets (Git SSH, npm cache, AWS, GPG, Docker, pip, Cargo), MCP capability tier, network policy | F-40 |
| | **Automations** | Default sandbox profile, catch-up policy, notifications | F-41 |
| | **Privacy** | The six user-facing guarantees (`../07-security-and-permissions.md` §10), data-paths table with *Open folder*, telemetry toggle (off), crash-report toggle (off), *Export all data*, *Delete all data* | F-43, F-100 |
| ABOUT | **About & performance** | Version, update check, **live perf stats** (core/renderer RAM, idle CPU vs budget), licences | F-99 |
| | **Advanced / Experimental** | Feature flags, nightly channel, reset layout | — |

Phase C builds **every page frame and control as a non-persisting form** *except* Appearance, which is fully functional from day one (theme switching is how we judge every other screen).

---

## S-24 · Command palette

**Features:** F-18 · `Ctrl+K`. Centre-top overlay, 640 px wide, `--z-palette`.

```
┌──────────────────────────────────────────────┐
│ 🔍 Type a command, chat, file or setting…     │
├──────────────────────────────────────────────┤
│ Actions                                      │
│  ✎ New chat                          Ctrl+N  │
│  ▸ Open layout: Chat + Terminal              │
│ Chats                                        │
│  ● Fix the cart total          northwind     │
│ Files · Projects · Settings · Apps           │
└──────────────────────────────────────────────┘
```

Fuzzy search across Actions, Chats, Projects, Files (current project), Settings pages/rows, Apps. Prefix scopes: `>` actions only · `@` apps · `#` chats · `/` settings · `:` go to line. Empty query shows *Recent* and *Suggested*. Every item shows its shortcut. `↑↓` navigate, `Enter` run, `Ctrl+Enter` run in new pane where meaningful, `Esc` close. Focus returns to the previously focused element.

---

## S-25 · Dialogs, toasts, banners, tooltips

**Features:** F-39, F-20, F-06 · Shared overlay system. **Z-order and the native-webview rule are defined in S-04.**

| Overlay | Spec |
|---|---|
| **Dialog** | Centre, 440 / 560 / 720 px sizes, `--r-xl`, scrim `--overlay`, focus trapped, `Esc` closes unless destructive-in-flight. Header, body, footer (primary right). |
| **Confirm (destructive)** | Red primary, names the exact thing being removed and its consequence; "Don't ask again" only for reversible actions. |
| **Rewind dialog** | Message picker + **diff preview of files that will change** + *Rewind files* / *Cancel*. Notes that forked chats have no earlier points and snapshots expire after 30 days. |
| **Edit & resend warning** | "Later turns will be removed." with undo window. |
| **New project dialog** | Name · folder (picker) · template/starter (S: grid of 4) · *Coding tools* toggle (terminal, dev server, git — F-07) · dev-server command (optional). |
| **Approval modal** | Only when the window is unfocused-then-refocused with pending approvals; otherwise approvals live in chat (S-05). |
| **Toast** | Bottom-right stack ≤ 3, 5 s (errors 8 s, hover pauses), types: info / success / warning / error, optional action, `aria-live`. |
| **Banner** | Full-width strip under the titlebar or at the top of a pane. Kinds: *limit hit*, *offline*, *update ready*, *recovered from crash*, *connection needs attention*. One primary action + dismiss. |
| **Tooltip** | 400 ms delay, 12 px, includes shortcut; never contains the only copy of important info. |
| **Menu / popover** | Radix primitives, `--shadow-md`, arrow-key navigation, typeahead, collision-aware. |

---

## S-29 · First run / onboarding

**Features:** F-24, F-01, F-100 · Goal: **install → first useful task in < 10 minutes**.

Full-window, 4 skippable steps with a progress dots row:
1. **Welcome** — the promise in three lines: *local-first · your keys · every change reversible*. No account.
2. **Look** — theme picker (System / Light / Dark with live preview) and terminal/editor surface.
3. **Connect a model** — cards: *Use my subscription · Use an API key · Use a local model · Skip for now*. Skip leads to the Home *Connect a model* state, never a dead end.
4. **Add a project** — choose a folder, or start from a template, or skip.

Final: *You're set* → opens Home (S-08) with focus in the composer. Re-runnable from Settings → General.

---

## S-30 · Status surfaces

| Surface | Spec |
|---|---|
| **Context popover** (from ring) | Used / window tokens, bar, what's in context (files, rules, memory hits, attachments), **/compact** button, note on auto-compaction. |
| **Usage popover** | Per-connection rows with progress bars, session/weekly limits, **reset countdown**, active connection marker, link to failover order. Amber ≥ 70 %, red ≥ 90 %. |
| **Tool servers row** | In the Tools menu: *Not connected* only when needed, with *Reconnect*. |
| **Dev-server badge** | Command · port · starting / ready / crashed; click opens Browser pane. |
| **Connectivity** | Offline dot (status bar) + banner; composer disabled only for network engines (local models stay usable). |
| **Perf stats (dev)** | Overlay toggled with `Ctrl+Alt+P` showing renderer heap, core RSS, idle CPU, last panel-switch time — powers F-99 checks. |
