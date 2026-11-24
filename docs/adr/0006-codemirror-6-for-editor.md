# 0006 — CodeMirror 6 for the embedded editor and diffs

- **Status:** proposed
- **Context:** The editor pane (S-09) and diff views (S-13) must be themeable by our tokens, fast to open, and light on memory (renderer budget < 120 MB). `04-tech-stack.md` says "embed a capable editor" without naming one.
- **Decision:** Use **CodeMirror 6** (with `@codemirror/merge` for diffs), lazily loaded per surface, themed through CSS variables from `tokens.css`.
- **Consequences:**
  - Good: small bundle, low RAM, modular, easy to theme, good accessibility baseline.
  - Bad: fewer IDE features than Monaco (no built-in IntelliSense); language servers, if ever wanted, are extra work.
- **Alternatives:** Monaco (rejected for now: several MB and notably higher RAM, harder to theme to tokens); Ace (older architecture); a plain `<textarea>` (insufficient for diffs and highlighting).
