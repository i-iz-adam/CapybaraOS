# 02 — Frame & Layout (S-01 – S-04)

**Owner:** design session 2 · **Tier:** A · **Reference:** `01-interface-design.png`, `02-multi-project.webp`, `20-app-connections.png`

---

## S-01 · App frame + titlebar

**Features:** F-97, F-98, F-02 · **Purpose:** the window every other screen lives in.

```
┌────────────────────────────────────────────────────────────────────────────┐
│ ▭  (drag region)        ▸ project-name  ⎇ main                  ─   ▢   ✕ │ 36
├────┬───────────────┬───────────────────────────────────────────────────────┤
│    │               │                                                       │
│ R  │   SIDEBAR     │   WORKBENCH  (pane strip, see S-04)                   │
│ A  │   272         │                                                       │
│ I  │               │                                                       │
│ L  │               │                                                       │
│ 48 │               │                                                       │
├────┴───────────────┴───────────────────────────────────────────────────────┤
│ status bar (24, optional): engine · mode · usage · dev server · updates    │
└────────────────────────────────────────────────────────────────────────────┘
```

| Region | Spec |
|---|---|
| Titlebar | Custom, 36 px, whole bar is a drag region except controls. Centre/left shows **project name + branch chip**; clicking it opens the project switcher (S-24 scoped to projects). |
| Window controls | **Windows/Linux:** right-aligned min / max / close, 46 × 36 hit area, close hover is `--status-error`. **macOS:** traffic lights left (inset 72 px). Control rendering is platform-switched by one `platform` flag. |
| Panel gaps | Rail, sidebar and workbench are separate rounded panels (`--r-lg`) on `--bg-app` with 6 px gaps — the "floating panels" look. In compact density the gap is 4 px. |
| Status bar | Off by default (Settings → Appearance). When on: left = engine + mode, centre = running/needs-you counts, right = dev-server, update-ready, offline dot. |
| Banners | Appear between titlebar and panels, full width (S-25). |

**States:** normal · maximised (gaps removed, radius 0) · unfocused (titlebar text `--text-faint`) · fullscreen (titlebar hides, edge reveal) · recovery banner after crash.

**Build note (timebox 2 h):** custom titlebar on Windows must keep Windows 11 snap-layout behaviour if feasible; if the spike fails, fall back to native decorations and keep the in-window project/branch strip. Do not block other work on this.

---

## S-02 · Icon rail

**Features:** F-02, F-44, F-22 · **Purpose:** global navigation; one tap to any surface.

```
 ┌────┐
 │ ⌂  │  Home
 │ 💬 │  Chats
 │ ▦  │  Customize
 │ ◍  │  Atlas
 │ ✉  │  Inbox        ● badge
 │ ⟳  │  Automations
 │ ✦  │  Director
 │ ◇  │  Design
 ├────┤
 │ 📁 │  Files         ← pane toggles
 │ >_ │  Terminal
 │ 🌐 │  Browser
 │ ± │  Review
 ├────┤
 │ G  │  pinned apps (≤ 5, drag to reorder)
 │ …  │  overflow → app dock menu
 │    │
 │ 🐞 │  Report a problem
 │ 💭 │  Feedback
 │ ⚙  │  Settings
 └────┘
```
*(glyphs are placeholders — use Lucide: `home`, `message-square`, `layout-grid`, `brain`, `inbox`, `repeat`, `sparkles`, `palette`, `folder`, `terminal`, `globe`, `git-compare`, `settings`.)*

| Behaviour | Spec |
|---|---|
| Item | 36 × 36 hit target, 20 px icon, tooltip with name + shortcut after 400 ms. |
| Active | `--bg-selected` pill + `--accent` icon. Surface items (Home…Design) are **mutually exclusive** (they change what the workbench shows). Pane toggles (Files…Review) are **independent** (they add/remove panes in the strip). |
| Badges | Dot for "needs you" (amber) on Inbox and on any pane/app awaiting attention; number badge ≤ 9+. |
| Pinned apps | Up to 5 connected apps; clicking opens (or focuses) the app pane beside the chat. Overflow "…" opens the app dock popover (grid). |
| Reorder / hide | Right-click item → Hide / Move; managed in Settings → Appearance → Rail. |
| Collapsed sidebar | Rail stays; it is never hidden. |

**Empty/degraded:** pinned-apps group hidden when no apps are connected (shows a single "Connect an app" `+`).

---

## S-03 · Project sidebar

**Features:** F-02, F-03, F-05 · **Purpose:** every project and chat, with live status.

```
┌─────────────────────────────┐
│ ✎ New Chat      🔍  ←  →  ⟦ │  ← search, history back/fwd, collapse
│ ▸ New Project               │
│ ▦ Customize                 │
│ ✉ Inbox                  3  │
│                             │
│ Recents                     │
│  ● Fix the cart total       │  ← status dot, title, project subtitle
│    northwind                │
│  ✓ Add idempotency keys     │
│    ledger-api               │
│  more                       │
│                             │
│ Projects                    │
│ [All projects ▾] [All][Client][Personal] │  ← scope select + group chips
│ 🔍 Search chats…            │
│ ▾ 📁 Northwind Storefront   │  ← project colour on name
│     ● Spring release     ⎇  │  ← worktree chat
│       Why is the cart…      │
│     more                    │
│ ▸ 📁 Ledger API             │
│ ▸ 📁 Field Reports          │
│                             │
├─────────────────────────────┤
│ 🦫 CapybaraOS  Alpha   ◔ ◔  │  ← footer: build badge + usage mini-rings
└─────────────────────────────┘
```

| Region | Spec |
|---|---|
| Header actions | New Chat (`Ctrl+N`), New Project (`Ctrl+Shift+N`), Customize, Inbox with count. Search icon opens a chat-title search (inline, not the palette). Back/forward walk **navigation history** (`Ctrl+[` / `Ctrl+]`). |
| Recents | Cross-project, latest 8, row = status + title + project name (muted). "more" expands in place. |
| Projects | Scope select (All / a group / pinned) + group chips (user-defined tags) + chat search. Each project: folder icon, name in its `--proj-N` colour, collapse caret, `…` menu (rename, colour, group, reveal in Explorer, remove). Shows 5 chats then "more". |
| Chat row | 28 px (comfortable). Leading **status dot**, title (ellipsis), trailing slot: branch icon for worktree chats, queued count, `…` on hover. |
| Footer | Product mark + build badge (Alpha), usage mini-rings (open S-30 popover). |

**Status dot (F-03)**

| State | Visual | A11y label |
|---|---|---|
| Running | `--status-running`, gentle pulse (CSS, paused when hidden) | "Running" |
| Needs you | `--status-needs`, solid, count if > 1 | "Needs your input" |
| Done (unseen) | `--status-done` check | "Finished" |
| Done (seen) / idle | no dot | — |
| Error | `--status-error` ! | "Failed" |

**Interactions:** click opens the chat in the workbench (instant switch — chat/pane state is retained, F-04). Middle-click / `Ctrl+click` opens in a new window (later). Right-click and `…` menu: Rename, Pin, Duplicate, Fork from…, Archive, Copy link (F-23), Delete. Keyboard: `↑/↓` move, `Enter` open, `→/←` expand/collapse, `F2` rename, `Del` archive-with-confirm. Sidebar is **virtualised** (budget: project switch < 150 ms with 10 projects).

**States:** loading skeleton rows · no projects (empty CTA: *Add a folder as a project* + *Start from a template*) · filter with no results · collapsed (width 0, reveal with `Ctrl+B` or hover edge for overlay mode).

**Settings mode:** opening Settings (S-23) swaps this sidebar's content for the settings navigation; the rail and workbench remain.

---

## S-04 · Pane workbench

**Features:** F-04, F-79, F-80, F-81 · **Purpose:** the horizontal strip where the chat and its tools sit side by side.

```
┌─ Chat ───────────────┬─ package-lock.json ─────┬─ Files ──────────┬─ Terminal ────┐
│ header               │ header + tabs           │ header           │ header        │
│                      │                         │                  │               │
│  messages            │  editor                 │  tree            │  PTY          │
│                      │                         │                  │               │
│ [ composer ]         │                         │                  │               │
└──────────────────────┴─────────────────────────┴──────────────────┴───────────────┘
         ▲ 8px resize handles between panes · strip scrolls horizontally if it overflows
```

| Concept | Spec |
|---|---|
| **Pane** | A rounded panel with a 40 px header (icon, title, subtitle, pane actions, close ×). Types: `chat`, `editor`, `files`, `terminal`, `browser`, `review`, `git`, `app`, `atlas-page`, `design`. |
| **Strip** | Ordered list of panes. The **chat pane is always first and cannot be closed** (it can be collapsed to a 48 px stub). Min pane width 320 (chat 420). |
| **Opening** | Rail toggles, `Ctrl+K` → "Open …", clicking a file path/URL/diff chip in chat, or *Spotlight* (agent uses an app → its pane opens). New panes insert immediately right of the **focused** pane. |
| **Resizing** | Drag handle resizes the two neighbours; double-click equalises; `Alt+←/→` nudges by 40 px. |
| **Overflow** | When panes exceed width, the strip scrolls horizontally with snap; a **Fit** toggle shrinks all to their minimum first; below 1000 px wide it becomes **tabbed single-pane** (one visible, tab strip on top). |
| **Focus mode** | `Ctrl+Shift+Enter` maximises the focused pane; same key restores. |
| **Persistence (F-04)** | The strip layout, open tabs, terminal sessions, browser tabs and scroll positions **belong to the chat** and are restored on switch. Layout is stored per chat; a project-level default seeds new chats. |
| **Presets** | Command palette: *Chat only*, *Chat + Editor*, *Chat + Files + Editor*, *Chat + Terminal*, *Chat + Browser*, *Review layout*. |
| **Drag & drop (P2)** | Dragging a tab onto another pane's edge splits/moves it. Not in Phase S. |

**Native webview rule:** the Browser pane (S-12) is a native child webview that renders *above* DOM. While any popover, menu, dialog or palette is open over it, the pane swaps to a static snapshot (or hides). Build this seam into the pane contract from the start (`pane.onOverlayChange`).

**States:** empty project (chat pane shows S-08 home) · single pane · overflowed · focus mode · limited chat (Browser pane replaced by "disabled in a limited chat" placeholder — F-40).
