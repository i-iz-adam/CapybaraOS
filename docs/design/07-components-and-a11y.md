# 07 — Components, States, Shortcuts & Accessibility

**Owner:** design session 2 · Lives in `packages/ui` (primitives) and `apps/desktop/src/shell` (compositions).

---

## 1. Component inventory

Build primitives **once**, in `packages/ui`, with Radix for behaviour and our tokens for looks. Do not build a component the screens don't use.

| Group | Components |
|---|---|
| **Actions** | `Button` (primary, secondary, ghost, danger), `IconButton`, `SplitButton` (Queue/Steer), `Kbd` |
| **Inputs** | `TextField`, `TextArea` (auto-grow), `Select`, `Toggle`, `Checkbox`, `Radio`, `Slider`, `SegmentedControl` (also the Auto/Ask/Off control), `ShortcutRecorder`, `SearchField` |
| **Navigation** | `RailItem`, `Tabs` (pane tabs and page tabs), `Breadcrumb`, `TreeView` (virtualised), `SettingsNav` |
| **Layout** | `AppFrame`, `Panel`, `PaneStrip`, `Pane`, `Divider` (resizable), `ScrollArea`, `VirtualList`, `Card`, `GroupCard`, `SettingRow` |
| **Feedback** | `StatusDot`, `Badge`, `Chip`, `Ring` (context/usage), `ProgressBar`, `Spinner`, `Skeleton`, `Toast`, `Banner`, `EmptyState` |
| **Overlays** | `Dialog`, `Popover`, `Menu` / `ContextMenu`, `Tooltip`, `CommandPalette` |
| **Domain** | `ActionCard` (+ variants per catalogue), `MessageBubble`, `Composer`, `ModelSwitcher`, `AppGlyph` (generic), `DiffView` (split/unified), `CodeBlock`, `TerminalView`, `BrowserView`, `KnowledgeMap` |

Each component ships with: tokens-only CSS, a `data-state` attribute for every state below, keyboard behaviour, and an accessible name.

## 2. State matrix

Every interactive component implements: **default · hover · focus-visible · active/pressed · selected · disabled · loading · error**. Rules:

- Hover uses `--bg-hover`; selected uses `--bg-selected`; neither changes layout.
- Disabled uses `--text-faint` and `cursor: not-allowed`, and keeps its tooltip explaining *why*.
- Loading never shifts layout (reserve space; spinner replaces icon).
- Error uses `--status-error` plus an icon and text — never colour alone.
- Touch-style hit target minimum 32 × 32 even in compact density.

## 3. Keyboard map (proposed — finalise in S-23 *Shortcuts*)

`Mod` = `Ctrl` on Windows/Linux, `Cmd` on macOS.

| Action | Shortcut |
|---|---|
| Command palette | `Mod+K` |
| New chat / New project | `Mod+N` / `Mod+Shift+N` |
| Toggle sidebar | `Mod+B` |
| Back / forward in history | `Mod+[` / `Mod+]` |
| Open settings | `Mod+,` |
| Toggle Files / Terminal / Browser / Review / Git | `Mod+Shift+E` / `` Mod+` `` / `Mod+Shift+B` / `Mod+Shift+R` / `Mod+Shift+G` |
| Focus next / previous pane | `Mod+Alt+→` / `Mod+Alt+←` |
| Maximise / restore pane | `Mod+Shift+Enter` |
| Nudge pane width | `Alt+←` / `Alt+→` (on a focused divider) |
| Send / newline | `Enter` / `Shift+Enter` |
| Queue vs **steer** while running | `Enter` / `Mod+Enter` |
| Stop the running turn | `Esc` (in composer) or `Mod+.` |
| Cycle permission mode | `Mod+Shift+M` |
| Open model switcher | `Mod+Shift+L` |
| Jump to latest | `Mod+↓` |
| Perf overlay (dev) | `Mod+Alt+P` |

Shortcuts are data (one registry), shown in tooltips and the palette, and rebindable. No shortcut may exist only in a component's `onKeyDown`.

## 4. Accessibility baseline

1. **Focus:** visible 2 px `--accent` ring with 2 px offset on every focusable element; logical tab order; focus never lost on overlay close (returns to trigger).
2. **Landmarks & roles:** rail = `navigation`, sidebar = `navigation` (labelled), workbench = `main`, panes = `region` (labelled by header), chat list = `log` (`aria-live="polite"` only for the newest assistant block, off for cards' timers), toasts = `status`/`alert`.
3. **Names:** every icon-only button has `aria-label`; status dots carry text equivalents.
4. **Contrast:** text ≥ 4.5:1, UI glyphs ≥ 3:1, in **both** themes; checked by axe in the smoke test.
5. **Motion:** honours `prefers-reduced-motion` and the in-app override; no essential information conveyed by motion.
6. **Zoom & text size:** layout holds at 200 % zoom (tabbed single-pane fallback) and chat text scaling 12–18 px.
7. **Keyboard-only paths exist** for: opening any pane, resizing panes, approving/denying a card, switching chat/model/mode, and reaching every settings row.
8. **Screen-reader smoke:** NVDA (Windows) pass over Home, a chat with every card type, Settings → Permissions, and the Actions modal before Phase S exit.

## 5. Performance rules for UI code

- All lists > 50 rows are virtualised (sidebar, chat, files, runs, pages).
- Panel switch and keystroke-to-paint stay under 16 ms; pane contents mount lazily and **stay mounted** (hidden) once opened to preserve state, except `browser` which is hibernated by the core after inactivity.
- One shared 1 Hz clock drives every running-timer; no per-card intervals.
- No JS-driven animation loops; no `backdrop-filter` on panes larger than a popover; no layout thrash in resize handlers (use `requestAnimationFrame` and CSS variables for widths).
- Code-split by surface (Tier C surfaces are dynamic imports).
- Every PR touching UI states idle CPU/RAM impact (rule 8 in `00-START-HERE.md`).
