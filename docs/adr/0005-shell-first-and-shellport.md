# 0005 — Shell-first build order with a `ShellPort` data seam

- **Status:** proposed
- **Context:** The UI is large (30 specified screens) and many sessions/agents will build it over time. Previously the roadmap put engines and permissions before most UI. The project owner wants every shell designed and built first so features land in finished homes — without sessions burning time on mock-data scaffolding.
- **Decision:** Insert **Phase S (Shell)** before Phase 1 (see `docs/08-roadmap.md`). All UI reads state through one typed interface, `ShellPort` (`packages/protocol` types + `apps/desktop/src/shell/ports/`). Phase S ships exactly one adapter: **fixtures** (≤ 400 lines, smallest set that shows every state — policy in `docs/design/README.md`). Phase 1 adds the Tauri/Rust adapter behind the same interface; components are not edited. Intents (user actions) are also methods on the port and are **no-ops or local-state only** in fixtures; the shell has no capability to write files, run commands, spend or send.
- **Consequences:**
  - Good: layout/interaction settled early; one place to delete mock data; no component rewrite when real data arrives; safety rule 7 preserved.
  - Bad: some interfaces may need revision when the real core arrives (mitigated by keeping port methods coarse and projections of the event log); risk of fixtures growing (mitigated by the line cap and the "delete, don't extend" rule).
- **Alternatives:** Build features vertically with UI last (rejected by owner); mock servers / MSW (rejected: more moving parts); Storybook-first (rejected: matrix of states is the time sink we are avoiding).
