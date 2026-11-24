# 03 — Chat, Cards & Composer (S-05 – S-08)

**Owner:** design session 2 · **Tier:** B · **Reference:** `01-interface-design.png`, `06-ai-native-dev-env.webp`, `21-app-per-tool.png`, `23-chat-switch-engine.png`

Behaviour behind these surfaces is specified in `../03-product-teardown.md` §2 and `../07-security-and-permissions.md`. This doc covers layout and states only.

---

## S-05 · Chat view

**Features:** F-10, F-12, F-15, F-17, F-20, F-39 · **Purpose:** where work is requested and watched.

```
┌ 💬 Fix the cart total          northwind · ⎇ main        🔗  ⋯   ✕ ┐
│                                                                    │
│                         ┌───────────────────────────────────────┐  │
│                         │ Why is the cart total off by 1p?      │  │  user bubble
│                         └───────────────────────────────────────┘  │
│                                        ↺ ⑂ ✎   11:24              │  hover actions
│  🦫 Capybara  11:24                                                │
│  I'll look at the totals code first.                               │
│  ┌ ▸ Read  src/cart/total.ts                          0.4s  ✓ ┐    │  card (collapsed)
│  ┌ ▾ Edit  src/cart/total.ts                  +4 −2   1.1s  ✓ ┐    │  card (expanded)
│  │  - const t = Math.round(sum * 100) / 100                    │    │
│  │  + const t = roundHalfEven(sum)                [Open in Review]   │
│  └─────────────────────────────────────────────────────────────┘    │
│  Found it — rounding mode. Fixed and verified.                     │
│                                                                    │
│                                          ⌄ Jump to latest          │
│  [ queued: "also check the invoice page" ✕ ]                       │
│  ┌ composer (S-06) ───────────────────────────────────────────┐    │
└────────────────────────────────────────────────────────────────────┘
```

| Region | Spec |
|---|---|
| Header | Editable title (click), project + branch subtitle, *Copy link* (F-23), overflow (rename, export, fork, archive). |
| Message list | Virtualised, max readable width 760 px centred inside the pane (wider panes add margins, not line length). Sticks to bottom while streaming unless the user scrolled up; then shows **Jump to latest**. |
| User bubble | Right-aligned, `--accent-tint` fill, `--r-lg`. Hover shows **Rewind to here** (F-39), **Fork**, **Edit & resend** (F-20, with "later turns will be dropped" warning), timestamp. |
| Assistant message | Left-aligned, no bubble; small product mark + name + time; Markdown with copyable code blocks; inline file/URL chips open panes. |
| Queue | Messages queued mid-turn show as dismissable chips above the composer (count also shown in the sidebar row). |
| Streaming | Text appends in place; no per-token animation. Cards appear immediately in *running* state. |

**States:** empty chat (greeting + 3 suggestions + rule hint) · streaming · awaiting approval (composer shows a "needs you" strip) · error · context full · limit hit · offline.

### Card catalogue

All action cards share one anatomy: **header** (icon · verb · target · meta · timer · status · chevron) → **body** (collapsible) → **footer** (actions). Cards are **collapsed when done**, **expanded while running or awaiting you**. One message may hold 5–6 cards; consecutive reads group into a single *"Read 5 files"* row.

| Card | Header | Body | Footer / actions | Feature |
|---|---|---|---|---|
| **Read / Search** | Read · path / grep pattern | Matched lines (≤ 8) | — | F-34 |
| **Edit / Write** | Edit · path · `+a −d` | Inline mini-diff | *Open in Review*, *Revert* | F-34, F-38 |
| **Shell** | Run · command | Live output tail (mono, last 12 lines), exit code | *Open terminal*, *Stop* while running | F-34, F-80 |
| **Web** | Fetch · URL | Title + excerpt | *Open in browser* | F-34 |
| **Subagent** | Agent kind · activity · tool count | Nested cards (indented, collapsible) | *Open* | F-17 |
| **App action** | App glyph · tool · **level chip** (Auto / Ask) | Inputs / result | *Open app tab* | F-45 |
| **Approval** | ⚠ *Wants to …* · risk label | **Exact before/after** or full command | **Allow · Deny · Always allow** (+ "for this session") | F-11, F-36 |
| **Question** | Capybara asks | Options (radio/checkbox) + free text | *Submit* | F-70 |
| **Plan** | Plan · step count | Numbered steps; inline comment markup | *Approve & run (All permissions, fresh chat)* · *Approve (All permissions)* · *Approve (manual edits)* · *Revise…* | F-15 |
| **Compact summary** | Context compacted | Summary text (collapsed) | — | F-13 |
| **Context full** | Error · "Context full" | Explanation | **Compact and retry** | F-13 |
| **Limit hit / failover** | Limit reached on *connection* | "Continued on *connection*" with timeline | *Change failover order* | F-27 |
| **Engine switched** | divider line "Switched to *Sonnet 5.5* (Claude)" | — | — | F-25 |
| **Rewind marker** | divider "Files rewound to here" | Changed-file count | *Undo rewind* | F-39 |
| **Memory written** | chip "Saved to Atlas: *title*" | — | *Open page*, *Undo* | F-54 |
| **Generated UI** | placeholder frame "Interactive result" | table / chart / board / form slot | — | F-21 (Phase 7) |

**Card states:** pending · running (timer ticking via a single shared 1 Hz clock) · success · error (red rule on the left edge, error text selectable) · denied · awaiting approval (amber rule, shadow-md) · stopped.

---

## S-06 · Composer

**Features:** F-11, F-12, F-13, F-14, F-18, F-19, F-25, F-86 · **Purpose:** compose, steer, switch engine/mode, see context and quota.

```
┌──────────────────────────────────────────────────────────────────────┐
│ [📎 notes.png ✕] [@ src/cart/total.ts ✕]                              │ attachment chips
│ Type your message, / for commands, @ to mention…                      │ textarea (auto-grow)
│                                                                       │
│ ＋  🤖 Agent ▾  🛡 Auto-edit ▾  ⚙ Tools ▾             ◔  ◔ │ Sonnet 5.5 ▾  🎤  ➤ │
└──────────────────────────────────────────────────────────────────────┘
   left group (context & permissions)                right group (budget, engine, send)
```

| Control | Spec |
|---|---|
| Textarea | Auto-grows to 40 % of pane height, then scrolls. `Enter` = send (or **queue** while a turn is running); `Shift+Enter` newline; `Ctrl+Enter` = **steer** while running (F-12). Paste image/file creates an attachment chip. Drop zone overlay on drag-over. |
| `＋` | Attach: file, image, email (from app), long-quote paste. |
| Agent ▾ | None / project agents (F-18). |
| **Mode ▾** | Ask first · Auto-edit · Plan · All permissions. All permissions renders the chip with an `--status-needs` outline and a one-time confirm. |
| Tools ▾ | Per-chat toggles: image generation, generative UI, agent models, enhanced plans, Spotlight, Director. A **"Not connected"** row appears only when a tool server this chat uses needs attention (S-30). |
| Context ring | 16 px arc = context-window fill. Amber ≥ 70 %, red ≥ 90 %. Click → popover with `/compact` (S-30). |
| Usage ring | Plan usage across chats; same thresholds; click → per-limit breakdown with reset countdowns (S-30). Hidden when the connection reports no limits. |
| Model chip | Shows current model; opens S-07. |
| Mic | Hold-to-talk / toggle; opens voice orb (Phase 8, disabled with tooltip until then). |
| Send / Stop | `➤` becomes `■ Stop` while running; while running with text present it splits into **Queue** and **Steer**. |
| `/` popover | Fuzzy list: built-ins (`/compact`, `/plan`, `/clear`), skills, agents, apps. Arrow keys + Enter; `Esc` closes. |
| `@` popover | Files, apps, Atlas pages, other chats. Selected item becomes an inline chip. |

**States:** idle · typing · attachments · running (send→stop) · queued · awaiting approval (disabled textarea with "Respond to the approval above or type to steer") · offline (send disabled, banner) · no connection (shows **Connect a model** inline CTA — never a dead composer).

---

## S-07 · Model / engine switcher

**Features:** F-24, F-25, F-28 · **Purpose:** change connection, model and effort mid-chat without losing history.

```
        ┌───┬──────────────────────────────────┐
        │ A │  ⬡ Large-model-A          Medium │
        │ ● │  ⬡ Mid-model-B      ✓     Medium │  ← selected
        │ O │  ⬡ Small-model-C          Medium │
        │ L │                                  │
        │ +1│                                  │
        │───│  Show 7 more                  ⌄  │
        │ ⚙ │  Effort  [Low][Med][High][X][Max]│
        └───┴──────────────────────────────────┘
          ▲ connection strip: glyph per connection, dot = in use,
            tooltip "Connection · account", gear → Settings → Models
```

Notes: left strip lists connections (subscriptions, API keys, local, optional cloud). Right list shows that connection's models with their **tier** (High / Medium / Low / Utility / Vision). Changing a model **only affects this chat**; a toast says "This chat now uses *X*. Defaults unchanged." (F-25). A footer note makes explicit that **permissions do not follow the connection**. Generic glyphs only in Phase S.

---

## S-08 · Home / new chat

**Features:** F-01, F-22, F-29 · **Purpose:** the start screen for a new chat and for an empty project.

```
                    🦫
          What are we working on?
   ┌─────────────────────────────────────────────┐
   │ Working in  [ northwind ▾ ]                  │
   │ Type your message…                           │   ← composer (S-06)
   │ ＋ Agent ▾ Auto-edit ▾ …              Model ▾ ➤│
   └─────────────────────────────────────────────┘
   [ New project ] [ Open folder ] [ Connect an app ] [ Start from template ]

   Needs you                         Recent
   ● Approve migration (ledger-api)  Fix the cart total
   ● Question: staging DB? (field…)  Add idempotency keys
```

| Region | Spec |
|---|---|
| Composer | Same component as S-06 with a **project selector** row. |
| Quick starts | Four tiles. Only *relevant* tiles show (no *Connect an app* once apps are connected; no *Connect a model* ever hidden if none exist). |
| Needs you | Up to 3 items from the Inbox, each deep-links. Hidden when empty. |
| Recent | Up to 5 chats. |
| Health strip | Slim banner when a connection or tool server needs attention ("1 app not connected"). |

**States:** first run (with S-29 hand-off) · no connection (composer replaced by *Connect a model*) · normal · degraded.
