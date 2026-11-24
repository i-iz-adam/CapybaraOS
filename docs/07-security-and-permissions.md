# 07 — Security & Permissions

**Owner:** research session 1 · **Status:** proposed · **Read before:** implementing any tool, app or automation

> **Core rule:** autonomy is earned, not assumed. No capability may write, send, spend or deploy until its approval path exists.

---

## 1. Threat model

| Threat | Mitigation |
|---|---|
| Agent edits unintended files | Mode defaults, per-tool gates, Review panel, snapshots + Rewind [18][28] |
| Agent exfiltrates secrets via a connected app | Limited environment, MCP capability tiers, redaction [19] |
| Malicious MCP connector | Least-privilege capability declaration, per-tool levels, sandbox, audit |
| Prompt injection in fetched pages/email | Treat all external content as data; never as instructions; tool gate still applies |
| Subscription token theft | Launch provider's official binary; never read, store or forward tokens [8][23] |
| User data used for training | No training, no hosted inference by default; documented provider agreements |
| Local network attack on mobile bridge | Opt-in listener, QR pairing, self-signed cert, revocable device tokens [17] |
| Supply chain | Pinned dependencies, lockfiles, signed releases, reproducible CI |
| Insider/organisation misuse (later) | Versioned policies, audit export, hard spend caps [11] |

---

## 2. Modes

| Mode | Writes | Shell | Network | Use |
|---|---|---|---|---|
| **Ask first** | Ask every time | Ask every time | Ask when leaving project | Untrusted work |
| **Auto-edit** | Auto inside project | Ask | Ask when leaving project | Default for new chats |
| **Plan** | Denied while planning | Denied | Read-only fetch allowed | Expensive/risky changes |
| **All permissions** | Auto | Auto | Auto | Trusted, user-selected only |

Each engine implements the same four names with engine-appropriate behaviour [18]. Chats Panda starts (our delegates) add extra checks before reading outside their project in the lower modes — we adopt the same rule.

Answers to a prompt: **Allow**, **Deny**, **Always allow** (or "Allow for session"). The approval card shows the exact before/after text for a file edit [28].

---

## 3. Permission gate algorithm

```
decision(tool_call, chat, policy):

  1. tool in chat.mode deny-list?            → DENY
  2. target outside project fence?           → ASK (or DENY in Plan)
  3. site not in trusted sites?              → ASK
  4. tool has explicit grant?
       level = auto → ALLOW
       level = ask  → ASK
       level = off  → DENY
  5. category auto-approved globally?        → ALLOW (warn in settings)
  6. risk = send | spend | deploy | delete?  → ASK always unless Rules allow
  7. default                                 → ASK
```

Every result — allow, deny, ask, timed out — is appended to the audit log with actor, target, policy version and timestamp.

---

## 4. Execution environment

Three fences compose:

1. **Filesystem fence** — project folder + `~/.capybaraos` + engine config + temp dirs. Access presets add Git SSH keys, npm cache, Homebrew, AWS credentials, GPG, Docker config, Python/pip and Rust/Cargo caches [19].
2. **Tool fence** — MCP capability tiers: `project_scoped` (blocks credential-dumping tools, the default), `read_only`, `full` (discouraged with a filesystem fence).
3. **Network fence** — `full`, `localhost_only`, `off`.

Platform enforcement: macOS `sandbox-exec`; Linux bubblewrap when available plus our own path checks; Windows use the platform's available isolation primitive and always keep our path checks as a backstop. Never rely on OS enforcement alone — validate every path in `cap-sandbox` too [19].

Our addition: a **capability token** is issued per turn and passed to the engine child; tool calls without a valid token are rejected. Tokens expire with the turn.

---

## 5. Unattended automations

| Profile | Behaviour |
|---|---|
| **Restricted** | Small allowlist, never asks; scheduled runs use this by default |
| **Rules** | Pre-approved calls run; unmatched calls pause and ask; webhook runs always use this |
| **Full** | All tools allowed; user must explicitly opt in per automation |

Matches observed behaviour [4]. Each run records trigger, duration, cost and every tool call; the user is notified on completion.

---

## 6. Secrets

- Tokens are stored in the OS keychain; SQLite holds only an opaque handle and a label.
- Provider subscription login is performed by the provider's own binary; its credentials stay in its own store [8][23].
- A `redact()` pass runs before any prompt leaves the machine: `.env` values, private keys, tokens and configured personal data are replaced with placeholders.
- `.env` files are never included in project context by default.
- No secret is ever sent to our infrastructure — there is no hosted inference in core mode.

---

## 7. Connected app permissions

Per app: **Always ready / When needed / Off**. Per tool: **Auto / Ask / Off**. Our guidance, matching PandaOS's docs: Auto for reading, Ask for anything that leaves the building (email, messages, deploys) [15]. Spotlight (opening the app tab) is a separate switch and is not a permission.

Database app specifically: **Safe Mode** (structured builder, writes blocked), **Direct SQL**, **No AI Access**, plus AI Data Access toggle and table exclusions [16].

---

## 8. Mobile bridge

- Listener binds to loopback/LAN only, opt-in, and pairs by QR with a short-lived code.
- Each device gets a rotating token; individual revoke and global revoke are supported; remote access requires an explicit Tailscale opt-in [17].
- The phone is a *view and approval surface* — the desktop performs all work and holds all secrets.

---

## 9. Enterprise (future)

Permission matrix per team, approved-model allowlist through a gateway, per-team hard spend caps, versioned policies with one-click rollback, MCP allowlists, EU-region pinning, sensitive-data redaction, one-step offboarding and audit/evidence export [11]. Agents always inherit the permissions of the user who started them — never more.

---

## 10. User-facing guarantees (put these in Settings → Privacy)

1. We do not use your data to train models.
2. Core features work with no account and no network call to us.
3. Your keys and subscription tokens are billed by your provider, from your machine.
4. Every autonomous action is visible in the audit log.
5. Every file change is reviewable and reversible.
6. Telemetry is off until you turn it on; crash reports are separate.

## Sources

[4] https://pandaos.ai/features/automations
[8] https://pandaos.ai/pricing
[11] https://pandaos.ai/enterprise
[15] https://docs.pandaos.ai/docs/apps/connecting
[16] https://docs.pandaos.ai/docs/apps/database
[17] https://docs.pandaos.ai/docs/apps/mobile-access
[18] https://docs.pandaos.ai/docs/help/permissions
[19] https://docs.pandaos.ai/docs/help/execution-environment
[23] https://docs.pandaos.ai/docs/help/connections
[28] https://docs.pandaos.ai/docs/projects/checking-edits
