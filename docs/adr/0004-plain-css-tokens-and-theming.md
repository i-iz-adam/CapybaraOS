# 0004 — Plain CSS custom-property tokens for theming (no Tailwind, no runtime theme engine)

- **Status:** proposed
- **Context:** The app ships light and dark themes plus a "mixed" option (terminal/editor pinned dark in a light app). Many AI sessions will write UI; they need one unambiguous styling approach. The product runs in system webviews, including older WebKitGTK builds, and must stay inside the perf budget (`docs/04-tech-stack.md`). `04-tech-stack.md` previously left "plain CSS tokens *or* Tailwind 4" open.
- **Decision:** Styling is **plain CSS with semantic custom properties** defined in one `tokens.css` (canonical copy: `docs/design/reference/tokens.css`). The resolved theme is `<html data-theme="light|dark">`, set by an inline script before first paint; `data-surface="dark"` re-scopes the dark set to individual panes. Components use CSS Modules (or co-located `.css`) and consume **semantic tokens only**. Radix UI provides behaviour. Colour values are plain hex/`rgba()` — no `oklch()`, `color-mix()` or `@property`.
- **Consequences:**
  - Good: zero runtime cost, theme switch is one attribute change, works on every target webview, easy for any agent to follow, "mixed" themes are a CSS scope.
  - Bad: no utility-class speed; more hand-written CSS; discipline needed to avoid raw values (enforce with a lint rule/grep in CI).
- **Alternatives:** Tailwind 4 (rejected: relies on newer CSS features that risk older WebKitGTK; second source of truth for tokens); CSS-in-JS / runtime theme engines (rejected: runtime cost, forbidden by the tech-stack rules); Tailwind 3 mapped to variables (viable fallback, but adds a build dependency for little gain).
