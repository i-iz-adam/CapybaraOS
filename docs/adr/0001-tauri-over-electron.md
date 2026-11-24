# 0001 — Tauri 2 over Electron for the desktop shell

- **Status:** proposed
- **Context:** CapybaraOS is intended for all-day, every-day use on Windows, macOS and Linux. The shell must be light, responsive and cross-platform. PandaOS's own stack is TypeScript/Next.js/Node.js/Electron [31], but Electron bundles Chromium per app.
- **Decision:** Use Tauri 2 — Rust core plus the operating system's webview (WebView2, WKWebView, WebKitGTK). The renderer is React/TypeScript. The in-app browser will use platform-native child webviews with persistent data stores, with an optional CEF engine for users needing Chromium fidelity.
- **Consequences:**
  - Good: much lower idle RAM, smaller installers, faster startup, native OS integration from Rust.
  - Bad: webview differences across platforms require a three-OS CI matrix and avoidance of bleeding-edge web APIs; browser-profile fidelity needs extra work.
- **Alternatives:** Electron (faster ecosystem, much heavier); Flutter (good perf, weaker desktop PTY/webview ecosystem); .NET MAUI (Windows-first); PWA (no deep OS integration).

## Sources

[31] https://www.pandata.de/career/full-stack-developer
