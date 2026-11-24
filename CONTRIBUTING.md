# Contributing to CapybaraOS

Thanks for helping build an open, local-first AI workstation. This project is in the **specification phase** — documentation contributions are as valuable as code.

## Before you start

1. Read [`00-START-HERE.md`](00-START-HERE.md).
2. Read [`docs/09-agent-workflow.md`](docs/09-agent-workflow.md) — it applies to human contributors too, especially the claims table and handoff format.
3. Check the issue tracker for an existing issue before opening a new one.

## What we need most

- **Connector implementations** (MCP servers) for Gmail, GitHub, Slack, calendars, databases and deployment tools
- **Engine adapters** and protocol reverse-engineering notes for official CLIs
- **Cross-platform testing** — Windows, macOS and especially WebKitGTK on Linux
- **Performance work** against the budget in `docs/04-tech-stack.md`
- **Security review** of the permission gate and sandbox design
- **Design** of a fast, calm interface that is our own, not a copy

## Development rules

- Safety before autonomy: no write/send/spend/deploy capability ships without its permission gate and audit hook.
- One logical change per commit, conventional prefix (`docs:`, `feat:`, `fix:`, `test:`, `perf:`, `chore:`).
- Tests for every feature; a Playwright path for every user-visible change.
- State the idle CPU/RAM impact of any new background work in your PR.
- No proprietary assets, logos or screenshots from the reference product in the product itself.

## Pull requests

- Fill in the PR template with: what changed, how verified, perf impact, security impact.
- Link the feature ID from `docs/02-target-features.md` when applicable.
- Update the docs in the same PR as the code.
- Leave a handoff block as described in `docs/09-agent-workflow.md`.

## Reporting bugs

Use the bug report template. Include OS and version, steps, expected vs actual, logs (with secrets redacted), and whether telemetry was enabled. Never paste tokens or `.env` contents into an issue.

## Security issues

Do not open a public issue. Use GitHub's private vulnerability reporting for the repository. We will acknowledge within 72 hours.

## License

By contributing you agree that your work is licensed under the MIT License. See [LICENSE](LICENSE).
