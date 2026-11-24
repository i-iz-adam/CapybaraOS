# 0003 — MCP as the extension boundary

- **Status:** proposed
- **Context:** The product must connect to many third-party apps and let users build their own, without core code growing a bespoke integration per service. Connected apps are already exposed as MCP-style tool servers in the reference product [15][19].
- **Decision:** All tool providers — built-in tools, third-party connectors and user-built apps — implement the Model Context Protocol. Core holds a capability-aware MCP client with per-tool Auto/Ask/Off permissions and capability tiers. Plugins may extend UI, commands and settings through a versioned manifest but not bypass the tool gate.
- **Consequences:**
  - Good: one permission path, one audit path, large ecosystem, cheap third-party connectors.
  - Bad: protocol version churn; need careful sandboxing of local stdio servers; some vendors lack MCP servers.
- **Alternatives:** bespoke connector API (more control, far more maintenance); HTTP webhooks only (no tool discovery); WASM-only plugins (poor fit for network apps).

## Sources

[15] https://docs.pandaos.ai/docs/apps/connecting
[19] https://docs.pandaos.ai/docs/help/execution-environment
