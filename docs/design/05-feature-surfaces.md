# 05 — Feature Surfaces (S-15 – S-22, S-26 – S-28)

**Owner:** design session 2 · **Tier:** C (S-26 – S-28 are D) · **Reference:** `20-app-connections.png`, `21-app-per-tool.png`, `05-project-memory.webp`, `03-agent-workflows.webp`, `07-connected-apps.webp`, `01-interface-design.png` (design start)

Tier C means: **layout, one empty state, one populated state, navigation in/out. No logic.** Each surface opens as a *surface* (replaces the workbench content via the rail) unless noted as a pane.

---

## S-15 · Inbox

**Features:** F-22 · One list of everything waiting on you.

```
┌ ✉ Inbox            [All][Approvals][Questions][Plans][Results]     ┐
├───────────────────────────┬───────────────────────────────────────┤
│ ● Approve: run migration  │  Approve: run migration                │
│   ledger-api · 2m         │  ledger-api › Migrate audit table      │
│ ● Question: staging DB?   │  ┌ exact command ─────────────────┐    │
│   field-reports · 9m      │  └────────────────────────────────┘    │
│ ✓ Result: weekly digest   │  [Allow] [Deny] [Open chat]            │
└───────────────────────────┴───────────────────────────────────────┘
```

Left list grouped by recency with kind icon; right detail renders the same card component as the chat. Actions resolve in place and the item greys out. Counts feed the rail badge, sidebar count and tray. **Empty:** "You're all caught up." **Populated:** one of each kind.

---

## S-16 · Customize hub

**Features:** F-18, F-45, F-46 · One page for everything you can add to Capybara.

```
┌ Customize                                         [＋ Connect app] ┐
│ Connected accounts, built-in apps, and the ones you built.         │
│ 🔍 Search agents, skills, apps, rules…                              │
│ [All projects ▾] │ Agents 0 │ Subagents 0 │ Skills 70 │ Apps │ Integrations 2 │ Rules 2 │
│ ▾ 🌐 Global · applies to every project               [＋ Add app]  │
│  ┌ ▣ Database   Explorer, SQL, charts…       [Project] [Connected] ┐│
│  ┌ ▣ Mail       Read and draft email         [Global]  [Enabled]   ┐│
│ ▾ 📁 northwind · this project only                                  │
└─────────────────────────────────────────────────────────────────────┘
```

Filter pills with counts switch the list type (Agents / Subagents / Skills / Apps / Integrations / Rules). Rows are cards: glyph, name, one-line description, **scope tag** (Global / Project) and **status tag** (Connected / Enabled / Needs attention / Off). Click → S-17 (apps) or an inline editor drawer (agents / skills / rules are Markdown files — F-57 style). **Empty:** per-tab empty state with the single most useful CTA.

---

## S-17 · App detail, actions & connect flow

**Features:** F-45, F-46, F-48 · Per-app and per-tool permission control.

**App detail drawer:** header (glyph, name, account, status) · *Availability* segmented (**Always ready / When a chat needs it / Off**) · *Project link* (resource chosen for this project — F-48) · *Spotlight* toggle (clearly not a permission) · **Actions (N)** list.

**Actions modal** (the per-tool matrix):

```
┌ ⚡ Actions  16     Capybara can use these in any conversation       ✕ ┐
│ ✦ Spotlight lets the app tab follow along when actions run          │
│ ┌────────────────────────────────────────────────────────────────┐ │
│ │ ▣ List emails  ⫶4 ✦   List or search email         [Auto|Ask|Off] ›│ │
│ │ ▣ Compose      ⫶9     Save a reviewable draft      [Auto|Ask|Off] ›│ │
│ │ ▣ Send         ⫶9 ✦   Send immediately, no UI      [Auto|•Ask•|Off]│ │  Auto disabled
│ └────────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────────┘
```

Segmented control tokens: Auto = `--perm-auto`, Ask = `--perm-ask`, Off = `--perm-off`. **Rules:** tools that send / spend / deploy / delete have **Auto disabled** (Ask or Off only, unless a Rules profile allows). Row `›` opens tool detail (inputs, last calls). Guidance line: *"Auto for reading, Ask for anything that leaves the building."*

**Connect flow** (dialog, 3 steps): ① *Choose method* (OAuth / token / URL+credentials / MCP server) → ② *Authorise* (opens browser, shows waiting + cancel; token fields masked; "stored in your OS keychain") → ③ *Link to project* (choose resource or skip) → done toast. **Errors:** auth failed, scope missing, network, token invalid — each with a retry and a *Copy details* (secrets redacted).

---

## S-18 · App host + Database app

**Features:** F-44, F-49 · **Pane** type `app`.

**App host (generic):** header = glyph · name · account · *project link chip* · *Spotlight* toggle · `⋯`. Body slot fills with the app UI; Phase C ships a placeholder body *"This app's view appears here"* so the host chrome is verified separately from any app.

**Database app layout:** tabs **Explorer · Query · History**; left = connection/schema tree; centre = query editor (Direct SQL) or *question box* (AI mode); bottom/right = results as table with a *Chart* toggle. Top mode chips: **Safe mode** (builder, writes blocked) · **Direct SQL** · **No AI access**; *AI data access* toggle and *Exclusions…* link. Cost-estimate chip appears for metered engines. **States:** not connected · connected/empty schema · running query · error.

---

## S-19 · Atlas (knowledge)

**Features:** F-54 – F-61 · Surface.

```
┌ ◍ Atlas   [Project ▾ | Global]   [Map | List | Review 3]   🔍  [＋ Remember] ┐
├───────────────────────────────────────────────────┬────────────────────────┤
│        ◯──── Verify fixes before commit           │ Verify fixes before …   │
│       ╱                                           │ Decision · 12 Nov       │
│  Validate root cause ── ◉ ── Static HTML config   │ From: chat "Fix cart…"  │
│       ╲                                           │ Links: 3   [Edit] [Undo]│
│        ◯──── Folder index generation              │ markdown body…          │
└───────────────────────────────────────────────────┴────────────────────────┘
```

**Map:** grouped, linked nodes (dashed edges, node = rounded card with kind colour); pan/zoom; click opens the page drawer. Must render ≤ 300 nodes without jank (canvas or SVG with culling; layout computed once, not animated per frame). **List:** virtualised, filter by kind/date. **Review queue:** agent-authored changes with *Accept* / *Undo each* (F-58, F-59). **Page drawer:** Markdown view/edit, backlinks, origin session link, version history. **Empty:** "Atlas fills itself as you work. Say *remember …* to add a note." **Indicators:** scope switch, *Ground every message* toggle (F-60).

---

## S-20 · Automations

**Features:** F-62 – F-67 · Surface with three views.

- **List:** rows = name, trigger chip (⏰ weekdays 09:00 / webhook / event), next run, last status, enable toggle, scope tag. Header CTA **＋ New automation** → opens a chat pre-filled "Describe the routine" (generation is Phase 6) with the builder beside it.
- **Builder:** trigger card at top → vertical stack of step cards (**AI step · Agent · Condition · Output · App action**) with `＋` insert points, **sandbox profile** select (Restricted / Rules / Full, default Rules) with a plain-language explanation, *Test run*, *Save*.
- **Run history:** table (trigger time, duration, cost, status); row expands to the tool-call trace; last 10 kept; notification setting; catch-up policy (*run once on wake / skip*).

**Empty:** three example prompts (non-functional text chips in Phase C). **Populated:** 3 automations, one with a failed run.

---

## S-21 · Director

**Features:** F-68 – F-72 · Surface.

```
┌ ✦ Director                                               [＋ Start chat] [Adopt…] ┐
│ Working            │ Waiting on you      │ Done               │ Error              │
│ ┌ ledger-api ────┐ │ ┌ field-reports ─┐  │ ┌ northwind ─────┐ │                    │
│ │ Migrate audit… │ │ │ Q: staging DB? │  │ │ Spring release │ │                    │
│ │ ● 4m · 12 tools│ │ │ [Answer]       │  │ │ ✓ 2h           │ │                    │
├─────────────────────────────────────────────────────────────────────────────────────┤
│ Orchestrator chat (S-05 pane, docked bottom or right)        Watches: 2 active ⏱    │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

Board of **delegate cards** grouped by status, filterable by project. Every delegate question is routed to a single banner at the top of the orchestrator chat — *the answer is passed through, never guessed*. **Watches** list shows type, target and remaining time (≤ 12 h). **Empty:** explain what a Director is in one sentence + *Start a Director chat*.

---

## S-22 · Design app

**Features:** F-73 – F-78 · Surface; **Experimental** badge until Phase 7.

**Start view:** hero *"What will you design?"* with a tile grid — **Document · Mockup · Prototype · Motion · Demo · Deck** — and a *Design systems* chip at the bottom. Soft gradient backdrop is allowed here and only here.
**Canvas view (spec only):** left pages/layers list · centre canvas with zoom/fit · right properties/tokens · top version switcher and *Hand off to code*. Chat remains in the chat pane beside it. Phase C builds the start view and an empty canvas frame; canvas behaviour is Phase 7.

---

## S-26 · Tray & notifications (Tier D)

**Features:** F-65, F-98. Tray menu: status line (*3 running · 1 needs you*) · *Open Capybara* · *New chat* · *Pause automations (1 h / until tomorrow)* · *Recent runs* · *Quit* (confirm if work is running). Tray icon variants: idle, running (subtle), needs-you (dot). **Notifications:** short, actionable, no secrets — *"Approve: run migration — ledger-api"* with *Open* / *Deny* actions where the OS supports it; automation completion shows status + duration + cost.

## S-27 · Voice orb (Tier D)

**Features:** F-86 – F-89. A 56 px floating orb (bottom-right of the workbench, draggable) with states **idle · listening · transcribing · speaking**, a transcript bubble, and a *mini orb* that follows the user between surfaces. Orb animation is CSS/opacity only and fully stopped when idle.

## S-28 · Mobile companion (Tier D)

**Features:** F-52, F-90. Phone shell: bottom tabs **Chats · Inbox · Apps · Directors**; chat view reuses the card catalogue at 360 px; approvals as a bottom sheet; **pairing screen** (QR scan, device name, revoke). Designed against the same tokens. Built in Phase 8.
