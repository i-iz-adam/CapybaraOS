# 04 — Workbench Panes (S-09 – S-14)

**Owner:** design session 2 · **Tier:** B · **Reference:** `01-interface-design.png` (editor + files beside chat), `06-ai-native-dev-env.webp` (terminal)

All panes follow the pane contract in `02-frame-and-layout.md` S-04 (header, close, min width, overlay hook, state retained per chat).

---

## S-09 · Editor pane

**Features:** F-79 · **Purpose:** read and lightly edit files beside the chat.

```
┌ 📄 total.ts   ● ×  │ cart.test.ts ×  │ +                ┐  tabs (preview tab = italic)
│ src › cart › total.ts                 [Diff ◐] [⋯]     │  breadcrumb + view toggle
├────────────────────────────────────────────────────────┤
│  1  import { roundHalfEven } from "./round";            │
│  2                                                      │
│  3  export function total(items: Item[]) {              │
│  4 ▌  const t = roundHalfEven(sum);        ← agent mark │
│  …                                                      │
└────────────────────────────────────────────────────────┘
```

| Concern | Spec |
|---|---|
| Engine | **CodeMirror 6** (ADR 0006): small, fast, themeable by our tokens. No Monaco (RAM). |
| Tabs | Preview tab (single click, italic, replaced by next preview) → pinned on edit or double-click. Dirty dot. Middle-click closes. |
| Views | *Code* (default) · *Diff* (vs last snapshot / HEAD) · *Rendered* for Markdown / images. |
| Agent edits | Gutter bar in `--accent` on lines changed by the agent this turn; file shows a transient "Capybara is editing…" read-only strip while a write is in flight. |
| Chrome | Line numbers, soft-wrap toggle, language label in the footer, `Ctrl+F` find, `Ctrl+G` go-to-line. No minimap, no breadcrumbs dropdown. |
| Surface | Honours *terminal & editor surface* (`match` / `dark`). |

**States:** empty (recent files + "Open a file from Files or a chat card") · loading large file (> 2 MB → read-only with banner) · binary (hex notice) · deleted-on-disk banner · merge-conflict banner.

---

## S-10 · Files pane

**Features:** F-01, F-79 · **Purpose:** project tree.

```
┌ 📁 Files                          ⌕ ＋📄 ＋📁 ⟳ ┐
│ ▾ src                                          │
│   ▾ cart                                       │
│       total.ts                    M            │  git status letter, coloured
│       round.ts                    A            │
│   ▸ pages                                      │
│ ▸ public                                       │
│   .gitignore                                   │
│   package.json                                 │
└────────────────────────────────────────────────┘
```

Virtualised tree; icons by file type (Lucide set); git status letters (M, A, D, U) with token colours; ignored files dimmed; filter box (`⌕`) is fuzzy. Context menu: Open, Open to the side, Reveal in File Explorer, Copy path, Rename, Delete (confirm → goes through the permission gate when initiated by an agent). Drag a file onto the composer to attach it. **States:** empty folder · loading · permission denied · watcher offline (manual refresh).

---

## S-11 · Terminal pane

**Features:** F-80, F-82 · **Purpose:** persistent PTY per chat.

```
┌ >_ Terminal   [PowerShell ▾]  ● dev server :3000     ＋ ⋯ ✕ ┐
│ tabs: pwsh 1 │ npm run dev │ +                              │
├──────────────────────────────────────────────────────────────┤
│ PS C:\code\northwind> pnpm dev                               │
│ ▲ Next.js … Ready in 1310ms                                  │
└──────────────────────────────────────────────────────────────┘
```

xterm.js; tabs belong to the chat and survive switching. **Shell picker** (Windows: PowerShell, cmd, Git Bash, WSL distros; macOS/Linux: login shell + detected). Dev-server badge shows command, port and ready state (F-82); clicking opens the Browser pane at that port. Toolbar: new, split (P2), clear, kill, find. Links (`http://localhost…`, `file:line`) are clickable. **Always-dark option** applies here (`data-surface="dark"`). **States:** no shell started (one-click start) · exited (shows code, *Restart*) · running agent command (tab marked with the agent mark, read-only until the command ends, user can take over).

---

## S-12 · Browser pane

**Features:** F-81 · **Purpose:** persistent in-app browser and dev-server preview.

```
┌ 🌐  ◀ ▶ ⟳  [ http://localhost:3000/cart            ] ⭐ ⋯ ✕ ┐
│ tabs: Preview │ Docs │ +                                      │
├──────────────────────────────────────────────────────────────┤
│                  (native child webview)                       │
└──────────────────────────────────────────────────────────────┘
```

Persistent profile (cookies and sign-ins retained). **Preview chip** appears when a dev server becomes ready and offers to open it. Address bar shows lock state; blocked/unsafe pages show an interstitial. **Native-overlay rule:** swaps to a snapshot whenever DOM overlays are open (see S-04). **States:** blank new tab · loading · load error · *disabled in a limited chat* placeholder with link to Settings → Execution environment (F-40) · webview crashed (reload CTA).

---

## S-13 · Review panel

**Features:** F-38, F-39 · **Purpose:** see, comment on, revert and commit every change.

```
┌ ± Review   4 files  +38 −12            [Split | Unified]  ⋯ ┐
├───────────────────┬───────────────────────────────────────────┤
│ ☑ src/cart/total  │  src/cart/total.ts            [Revert]    │
│   +4 −2        M  │ ┌───────────────┬───────────────┐         │
│ ☑ src/cart/round  │ │ - old line    │ + new line    │         │
│   +20 −0       A  │ │               │ ＋ comment…   │         │
│ ☐ package.json    │ └───────────────┴───────────────┘         │
│   +1 −1        M  │                                           │
├───────────────────┴───────────────────────────────────────────┤
│ Commit message [ fix: round half-even in cart total ] ✨ [Commit] │
└────────────────────────────────────────────────────────────────┘
```

| Region | Spec |
|---|---|
| File list | Status, path, `+/−`, checkbox for inclusion in commit. Sorted by path; group by folder toggle. |
| Diff | **Split** and **Unified** (toggle persisted). Gutter `＋` on hover adds a **line comment** (thread UI; comments can be sent to the chat as instructions). Hunk-level *Revert hunk*. |
| Actions | *Revert file*, *Revert all* (confirm), *Rewind chat to message…* (opens S-25 rewind dialog with preview). |
| Commit bar | Message field, ✨ generate message (utility tier), *Commit* (Ask-level action — goes through the gate). |

**States:** no changes ("Nothing to review") · agent still editing (live badge, list updates) · conflict · binary file · very large diff (collapsed hunks).

---

## S-14 · Git panel

**Features:** F-83, F-05 · **Purpose:** day-to-day git without leaving the app.

Sections, top to bottom: **Branch bar** (current branch ▾ switch/create, ahead/behind, pull/push) · **Worktrees** (list with "Open chat here"; *New worktree from branch…* — F-05) · **Changes** (Staged / Unstaged / Untracked groups, stage/unstage, discard with confirm) · **Commit box** (shares component with S-13) · **History** (last 20 commits, click → diff in Review). All write actions are *Ask*-level through the permission gate. **States:** not a git repo (offer *Initialise*) · detached HEAD · merge/rebase in progress banner · no remote.
