# 04 — Tech Stack Decision

**Owner:** research session 1 · **Status:** decision proposed · **Supersedes:** none  
**Related ADRs to create:** `0001-tauri-over-electron`, `0002-sqlite-single-file-store`, `0003-mcp-as-extension-boundary`

---

## 1. Requirements that drive the stack

| Requirement | Consequence |
|---|---|
| Windows, macOS and Linux from day one | Cross-platform shell with native installers |
| All-day, every-day use | Low idle RAM, near-zero background CPU, no fan spin |
| Highly responsive UI | Native core, async I/O, incremental rendering, no blocking IPC |
| Real files, terminals, browsers, dev servers | OS process control, PTY, persistent webview profiles |
| Many long-running tasks and automations | Background scheduler in a tray-resident process |
| Provider-neutral, user-owned keys | Provider adapter layer; tokens never enter our storage |
| Extensible by strangers | MCP + plugin API as a stable boundary |
| Open source, low contributor friction | One monorepo, mainstream languages, small dependency surface |

PandaOS's own stack is TypeScript / Next.js / Node.js / Electron [31]. We deliberately diverge on the desktop shell because the resource requirement is different for us.

---

## 2. The decision

### Desktop shell: **Tauri 2 (Rust core + system webview)**

| | Tauri 2 | Electron |
|---|---|---|
| Browser runtime | OS webview (WebView2 / WKWebView / WebKitGTK) | Bundled Chromium |
| Idle RAM (typical) | ~60–150 MB | ~300–500 MB+ |
| Installer size | ~5–15 MB | ~80–150 MB |
| Startup | ~0.4–1.5 s | ~1.5–4 s |
| Native OS integration | Rust plugins, tray, menus, deep links | Node + native modules |
| Ecosystem maturity | Good, smaller than Electron | Excellent |

**Why:** for an app left open all day, a bundled Chromium per window is the single largest avoidable cost. Tauri is the strongest fit for "highly performant, responsive, little resources".  
**Cost:** system webviews differ across platforms (CSS/JS feature gaps, especially WebKitGTK); we must test all three in CI and avoid bleeding-edge web APIs. The in-app browser needs persistent profiles and cookie jars — implement as platform-native child webviews with a persistent data store, and offer an optional CEF-backed browser engine for users who need Chromium fidelity. Record this as ADR 0001.

### Core: **Rust (stable, edition 2024)**

Owns: filesystem, process supervision, PTY, scheduling, SQLite, indexing, sandbox enforcement, IPC, secrets broker, updater. Async runtime `tokio`. All heavy work off the UI thread.

### Renderer: **TypeScript + React 19 + Vite 7 + TanStack Router/Query**

Plain CSS with design tokens (or Tailwind 4 at build time — zero runtime cost). Radix UI primitives for accessible widgets. Lucide icons and system font stack to avoid font-loading cost. **No** component library that ships a runtime theme engine.

### Persistence: **SQLite (single file per workspace)**

`rusqlite` behind a blocking-task bridge, WAL mode, foreign keys on. FTS5 for keyword search; `sqlite-vec` for embeddings so vectors stay in the same file. Markdown files on disk for knowledge pages and project rules, with SQLite as the index — matching the local-first, versioned-files approach that works well for user-editable content.[6] ADR 0002.

### Extension boundary: **MCP (Model Context Protocol)**

Connectors are MCP servers; tools are discovered at runtime and gated by permissions. Use `rmcp` on the Rust side. First-party plugins extend UI panels, commands and settings via a versioned manifest. ADR 0003.

### Agent engines: **adapters, not a new harness**

Three engine adapters — Claude Code, Codex, OpenCode — launched as supervised child processes, plus a direct OpenAI-compatible API client for BYO keys and local models. Engine adapters expose a common `TurnEvent` stream (text deltas, tool calls, results, errors, usage). Where an official CLI exposes a structured protocol we use it; otherwise we maintain a thin bridge and pin engine versions. Subscription credentials stay in the provider's own store; we launch their login command and never read the resulting token.[8][23]

### Supporting choices

| Concern | Choice | Why |
|---|---|---|
| Terminal | `portable-pty` + xterm.js | True PTY, small, mature |
| Embedded browser | Native child webview, persistent data store; optional CEF engine | State retention, low memory |
| HTTP / WebSocket | `reqwest`, `tokio-tungstenite` | Standard, async |
| Scheduler | `tokio-cron-scheduler` + tray service | Cron + event triggers, no window needed |
| Local STT | `whisper-rs` (whisper.cpp) | On-device, no network |
| Local TTS | `piper` via Rust binding or sidecar | On-device |
| Video export | `ffmpeg` sidecar (optional feature) | MP4 for design app |
| Git | `git2` for reads, official `git` binary for writes | Safe, compatible |
| Crypto | `ring` / `aes-gcm`, OS keychain via `keyring` crate | Tokens never on disk in plaintext |
| Logging | `tracing` + local rolling file, off by default | Debuggability without telemetry |
| Tests | `cargo test`, Vitest, Playwright | Fast unit + real E2E |
| Packaging | Tauri bundler: `.msi`/NSIS, `.dmg`, `.deb`/`.rpm`/AppImage | All target OSes |
| Monorepo | pnpm workspaces + Cargo workspace | One checkout, shared types |

---

## 3. Performance budget (hard requirements)

Measured on a mid-range laptop after 10 minutes idle, 3 projects open, no active turns:

| Metric | Budget | Enforcement |
|---|---|---|
| Main-process RSS | **< 150 MB** | CI smoke test |
| Renderer RSS | **< 120 MB** | CI smoke test |
| Idle CPU (all processes) | **< 1%** averaged over 60 s | CI smoke test |
| Cold start to interactive | **< 2.0 s** | CI smoke test |
| Project switch (10 projects loaded) | **< 150 ms** | Playwright perf assertion |
| Panel open / keystroke to paint | **< 16 ms** | Playwright perf assertion |
| Background indexer | Max 1 core, 200 MB, yield to UI | Benchmark |
| Installer size | **< 25 MB** | Release check |
| Memory growth over 8 h | **< 20%** | Nightly soak test |

Rules for contributors:
- No polling loops faster than 1 Hz; prefer OS events and watchers.
- Every background job is cancellable and reports CPU/RAM cost in dev stats.
- No dependency that bundles a second browser engine by default.
- Virtualise all long lists (chats, files, pages, run history).

---

## 4. Repository layout (planned)

```
CapybaraOS/
├── crates/
│   ├── cap-core/          # state, event log, permissions, scheduler
│   ├── cap-engine/        # engine adapters + TurnEvent protocol
│   ├── cap-tools/         # built-in tools, MCP client, tool registry
│   ├── cap-store/         # SQLite schema, migrations, FTS + vec
│   ├── cap-memory/        # knowledge page pipeline + retrieval
│   ├── cap-apps/          # app runtime, connector manifests, built-in apps
│   ├── cap-pty/           # terminal processes
│   ├── cap-browser/       # persistent browser tabs
│   ├── cap-sandbox/       # platform sandboxes, network policy
│   └── cap-desktop/       # Tauri app, tray, IPC, updater
├── apps/
│   ├── desktop/           # React renderer
│   └── mobile/            # companion PWA / Expo client (Phase 8)
├── packages/
│   ├── protocol/          # shared TS types generated from Rust schemas
│   ├── ui/                # design system primitives
│   └── connector-sdk/     # third-party connector authoring kit
├── docs/                  # this documentation
├── research/              # source notes and reference images
└── .github/workflows/     # ci.yml, perf.yml, release.yml
```

---

## 5. Explicitly out of scope

- Training or hosting models.
- A hosted control plane required for core use.
- A bespoke code editor engine (we embed one; we do not build one).
- A bespoke agent planning loop (we orchestrate existing engines).
- Replicating PandaOS branding, icons, copy or screenshots in the product.

---

## Sources

[6] https://pandaos.ai/features/atlas
[8] https://pandaos.ai/pricing
[23] https://docs.pandaos.ai/docs/help/connections
[31] https://www.pandata.de/career/full-stack-developer
