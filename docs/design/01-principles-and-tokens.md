# 01 — Design Principles & Tokens

**Owner:** design session 2 · **Canonical values:** [`reference/tokens.css`](reference/tokens.css) (if this file and the CSS disagree, the CSS wins — fix the doc)

---

## 1. Principles

| # | Principle | In practice |
|---|---|---|
| 1 | **Calm, dense, fast** | An all-day tool. Small type (13 px base), quiet colour, generous hit targets, no gratuitous motion. |
| 2 | **The chat is the centre; tools sit beside it** | Panes open next to the chat, never on top of it. Overlays are for short decisions only. |
| 3 | **State is always visible** | Every chat shows running / needs you / done. Every pane shows what owns it. Nothing "silently working". |
| 4 | **Approvals look serious, reads look light** | Read cards are collapsed and quiet; write / send / spend cards are prominent and show the exact change. |
| 5 | **Two themes, equal quality** | Light and dark are designed together from semantic tokens. Neither is a recolour afterthought. |
| 6 | **Own the look** | Warm neutrals and a moss-teal accent. Generic glyphs, not borrowed logos or art. |
| 7 | **Cheap to render** | System fonts, no runtime theme engine, CSS-only motion, virtualised lists, no blur-heavy effects on large areas. |
| 8 | **Keyboard-first, mouse-friendly** | Every surface reachable and operable from the keyboard; the command palette reaches everything. |

## 2. Theme model

| Setting | Values | Default |
|---|---|---|
| **Appearance** | `system` · `light` · `dark` | `system` |
| **Terminal & editor surface** | `match` · `dark` | `match` |
| **Density** | `comfortable` · `compact` | `comfortable` |
| **Accent** | reserved hook `data-accent`; only `moss` in Phase S | `moss` |

"Mix of light and dark": the app chrome follows Appearance; the **terminal and code surfaces may be pinned dark inside a light app** (many people prefer this). Implemented with a nested `data-surface="dark"` scope that re-applies the dark token set to just those panes.

**Mechanics**

- `<html data-theme="light|dark">` is the *resolved* theme; `data-theme-pref` holds the preference.
- An inline script in `index.html` sets `data-theme` before first paint (no flash). In the Tauri app the preference comes from `config.toml`; in plain-browser dev it may fall back to `localStorage` (dev only).
- `color-scheme: light dark` is set so native scrollbars and form controls match.
- `system` follows `prefers-color-scheme` live via `matchMedia`; no polling.
- Components **only** consume semantic tokens (`--bg-surface`, `--text-muted`), never raw palette values. See ADR 0004.
- Compatibility rule: plain hex / `rgba()` only — no `oklch()`, `color-mix()` or `@property` (older WebKitGTK).

## 3. Colour tokens

### Surfaces and text

| Token | Light | Dark | Used for |
|---|---|---|---|
| `--bg-app` | `#F6F4F0` | `#14130F` | Window backdrop, gaps between panels |
| `--bg-rail` | `#EFEBE4` | `#1A1814` | Icon rail |
| `--bg-sidebar` | `#F9F7F3` | `#1C1A16` | Project sidebar |
| `--bg-surface` | `#FFFFFF` | `#211F1A` | Panes, cards, popovers |
| `--bg-surface-2` | `#F3F0EA` | `#2A2721` | Inset areas, inputs, code blocks |
| `--bg-hover` | `rgba(40,32,20,.05)` | `rgba(255,245,230,.06)` | Row hover |
| `--bg-selected` | `#E3F0EB` | `#1F3A32` | Selected row / active rail item |
| `--border` | `#E3DED5` | `#332F27` | Hairlines |
| `--border-strong` | `#CFC8BB` | `#463F34` | Inputs, dividers on hover |
| `--text` | `#221E18` | `#ECE7DD` | Primary text |
| `--text-muted` | `#6B6458` | `#A89F90` | Secondary text |
| `--text-faint` | `#9A9285` | `#766E61` | Placeholders, disabled |
| `--overlay` | `rgba(20,16,10,.40)` | `rgba(0,0,0,.60)` | Dialog scrim |

### Accent and status

| Token | Light | Dark | Meaning |
|---|---|---|---|
| `--accent` | `#2F7D68` | `#4FB79A` | Primary action, focus, active |
| `--accent-hover` | `#276A58` | `#66C7AC` | |
| `--accent-fg` | `#FFFFFF` | `#0E1A16` | Text on accent |
| `--accent-tint` | `#E3F0EB` | `#1F3A32` | Soft accent backgrounds |
| `--status-running` | `#3B7DD8` | `#6AA5F0` | Working |
| `--status-needs` | `#C98A12` | `#E0A83A` | Needs you (approval, question, plan) |
| `--status-done` | `#2E8B57` | `#5CC48A` | Finished |
| `--status-error` | `#C8443A` | `#EE7B70` | Error / denied |
| `--status-idle` | `#9A9285` | `#766E61` | Idle / unknown |
| `--diff-add-bg` / `--diff-del-bg` | `#E4F4E8` / `#FBE7E4` | `#1C3324` / `#3A2020` | Diff lines |
| `--perm-auto` / `--perm-ask` / `--perm-off` | accent / `--status-needs` / `--text-faint` | same mapping | Auto / Ask / Off control |

Status is never colour-only: dot + label/icon + `aria-label`. Contrast target ≥ 4.5:1 for text, ≥ 3:1 for UI glyphs; verify with axe in the smoke test.

### Project colours

Projects carry one of eight hues for their sidebar heading (as the user's own organisation cue). Each has `--proj-N` (light/dark pairs in `tokens.css`): **moss, sky, violet, rose, amber, teal, slate, clay**. Assigned round-robin on creation; editable later.

## 4. Typography

| Token | Value |
|---|---|
| `--font-ui` | `"Segoe UI Variable", "Segoe UI", system-ui, -apple-system, "SF Pro Text", Roboto, "Helvetica Neue", sans-serif` |
| `--font-mono` | `"Cascadia Mono", "SF Mono", Consolas, "JetBrains Mono", ui-monospace, monospace` |

No web fonts, no font loading cost.

| Step | Size / line | Use |
|---|---|---|
| `--fs-xs` | 11 / 16 | Badges, kbd, meta |
| `--fs-sm` | 12 / 18 | Sidebar rows, secondary text |
| `--fs-md` | **13 / 20** | Base UI text |
| `--fs-lg` | 14 / 22 | Chat body, inputs |
| `--fs-xl` | 16 / 24 | Section titles |
| `--fs-2xl` | 20 / 28 | Page titles |
| `--fs-hero` | 28 / 34 | Home / design-start headline |

Weights 400 / 500 / 600. Chat body may scale 12–18 px via Settings → Appearance (`--chat-scale`).

## 5. Space, shape, elevation, motion

| Group | Tokens |
|---|---|
| **Space** (4 px grid) | `--sp-1` 2 · `--sp-2` 4 · `--sp-3` 8 · `--sp-4` 12 · `--sp-5` 16 · `--sp-6` 24 · `--sp-7` 32 · `--sp-8` 48 |
| **Radius** | `--r-sm` 6 · `--r-md` 10 · `--r-lg` 14 · `--r-xl` 20 · `--r-pill` 999 |
| **Elevation** | `--shadow-sm` (cards) · `--shadow-md` (popovers) · `--shadow-lg` (dialogs). Dark theme uses border + darker shadow, never glow |
| **Motion** | `--dur-fast` 80 ms · `--dur-base` 140 ms · `--dur-slow` 220 ms · `--ease` `cubic-bezier(.2,0,0,1)` |
| **Z-index** | `--z-pane` 1 · `--z-sticky` 10 · `--z-popover` 100 · `--z-dialog` 200 · `--z-toast` 300 · `--z-palette` 400 |

Motion rules: only `opacity` and `transform`; no animation longer than 220 ms; looping animation is permitted only for the *running* status dot (and paused while the window is hidden); everything honours `prefers-reduced-motion` and a Settings override.

Density: `compact` reduces row heights by 4 px and paddings by one `--sp` step via `[data-density="compact"]` overrides.

## 6. Layout constants

| Constant | Value |
|---|---|
| Minimum window | 960 × 600 |
| Default window | 1360 × 860 |
| Titlebar | 36 px |
| Icon rail | 48 px (icons 20 px, hit target 36 px) |
| Sidebar | 272 px default · 220–400 resizable · collapsible to 0 |
| Pane header | 40 px |
| Pane min width | 320 px (chat 420) |
| Divider | 1 px line, 8 px hit area |
| Status bar | 24 px (optional, off by default) |
| Composer | min 72 px, max 40 % of pane height |
| Settings content column | max 680 px, centred |

## 7. Iconography

**Lucide** (already in the stack): 1.5 px stroke; 20 px in the rail, 16 px inline, 14 px in chips. Apps and engines use **generic glyphs** (coloured rounded square + initial or Lucide icon) in the shell phase — no third-party logos until brand-use is reviewed.
