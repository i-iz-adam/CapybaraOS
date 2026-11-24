# Next session prompt — Shell build, session 3 (Tier A chrome)

> Paste everything in the block below as the **first message** of a new session. Attach `capybaraos-context.zip` (docs + research including the local-only reference images — see `docs/11-windows-dev-setup.md` §4).

```text
You are continuing CapybaraOS: a local-first, open-source AI workstation (Tauri 2 + React/TypeScript + Rust), inspired in LAYOUT PATTERN by pandaos.ai but with its own look, tokens, icons and copy. We are building the SHELL FIRST: every screen as real, themed (light/dark/mixed), keyboard-reachable UI driven by fixtures, before any feature logic. Multiple AI sessions work on this repo, so follow the docs exactly.

READ FIRST, IN THIS ORDER: 00-START-HERE.md → docs/01-vision.md → docs/design/README.md → docs/design/01-principles-and-tokens.md → docs/design/02-frame-and-layout.md → docs/design/06-settings-and-dialogs.md (S-24, S-25 only) → docs/design/07-components-and-a11y.md → docs/04-tech-stack.md → docs/08-roadmap.md (Phase S) → docs/adr/0004 and 0005 → docs/09-agent-workflow.md (incl. §5a). Look at docs/design/reference/shell-main.html and the reference images listed for S-01–S-04 in research/reference-images/INDEX.md (layout/pattern reference only — never copy visuals).

CLAIM in docs/09-agent-workflow.md before editing: the files/screens you will touch.

YOUR SCOPE (this session only): Phase 0a scaffold + Tier A chrome.
1. Scaffold the minimum: pnpm workspace; apps/desktop (Vite + React + TypeScript); packages/protocol (hand-written shell types for now); packages/ui (primitives actually used). Add Tauri 2 to apps/desktop and confirm `pnpm tauri dev` opens the window — but do ALL iteration in the browser via `pnpm dev`. No empty crates, no CI (that is Phase 0b). I am on WINDOWS (PowerShell) — give every command in PowerShell and respect docs/11-windows-dev-setup.md.
2. Copy docs/design/reference/tokens.css into the app as the single token file. Implement theme switching (system/light/dark + terminal/editor "mixed" surface) with the pre-paint inline script. No raw colour/spacing/font values anywhere else.
3. Define the `ShellPort` interface (state projections + intent methods) and ONE fixtures adapter (≤ 400 lines, smallest set: 3 projects incl. one empty, ≤ 4 chats each with all status types, workbench layout for one chat). Components may only use ShellPort — never import fixtures directly. Add the dev-only `?fixture=empty|busy|error` switcher.
4. Build, to the definition of done in docs/design/README.md: S-01 frame + titlebar (platform flag; Windows controls right; timebox the custom-titlebar spike to 2 h, fall back to native decorations if it fails), S-02 icon rail, S-03 project sidebar (virtualised, status dots, filters, collapse), S-04 pane workbench (strip, resize, collapse, overflow→tabbed single-pane, focus mode, panes are placeholders), S-24 command palette, and the minimal overlay primitives they need from S-25 (Dialog, Popover, Tooltip, Menu via Radix).
5. A functional Settings → Appearance page is a bonus only if time remains; the Settings frame itself is session 6.

HARD RULES
- FIXTURES POLICY (docs/design/README.md): one module, ≤ 400 lines, no generators/faker/mock servers/fake backends, NEVER write tests that assert fixture content. Do not spend time on mock data — design and interaction are the goal.
- Tests: one Playwright smoke per screen (key regions present, keyboard reachable, one screenshot per theme). No pixel-diff gating, no data-correctness tests.
- Timebox: if a screen is not "built" by the end of the session, mark the gaps in the screen status table and stop. Do not polish beyond spec; do not start Tier B/C screens.
- Idle cost: no timers/polling/animation while idle; state idle CPU/RAM impact. Project switch must stay < 150 ms with 10 fixture projects.
- The shell must not write files, run commands, spend or send. Safety rule 7 stands.
- New dependency = one-line justification in the PR/handoff. Prefer: React, Vite, TypeScript, Radix, Lucide, TanStack Router + Virtual, Vitest, Playwright. No Tailwind, no CSS-in-JS, no state library (use useSyncExternalStore inside the port).
- Conventional commits; one logical change each. Docs updated in the same change.

DELIVERABLES (when done)
1. Updated repo files as a zip of CHANGED/NEW files only (paths relative to repo root, forward slashes).
2. The exact PowerShell commands I should run (install, dev, test, commit).
3. docs/design/README.md screen status table updated; a handoff block (format in docs/09-agent-workflow.md §2) appended to docs/design/README.md; one line added to 00-START-HERE.md → Current state.
4. A ready-to-paste prompt for session 4 (S-05–S-08: chat view with full card catalogue, composer, model switcher, home) saved to docs/handoff/session-04-prompt.md.
```

## Notes for the human

- The reference images are not in git. Always upload the full `capybaraos-context.zip` so the new session can see them.
- If a session runs long, stop it at the tier boundary and start the next session from the saved prompt rather than extending scope.
