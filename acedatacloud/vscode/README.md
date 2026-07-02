# Ace Data Cloud MCP

Manage your Ace Data Cloud account — balance, usage, API keys, orders, and tokens.

[![VS Code Marketplace](https://img.shields.io/badge/VS%20Code-Marketplace-blue?logo=visualstudiocode&logoColor=white)](https://marketplace.visualstudio.com/items?itemName=acedatacloud.mcp-acedatacloud) [![PyPI](https://img.shields.io/pypi/v/mcp-acedatacloud.svg?label=PyPI)](https://pypi.org/project/mcp-acedatacloud/) [![Hosted MCP](https://img.shields.io/badge/hosted-mcp-blue)](https://mcp.acedata.cloud/mcp)

Connect VS Code's AI agents to the Ace Data Cloud platform console. Check your balance, look up usage and spend, manage API keys and platform tokens, list services and models, and create or pay recharge orders — all from chat.

This extension registers the **acedatacloud** MCP server with VS Code so GitHub
Copilot and any other agent that speaks the [Model Context Protocol](https://modelcontextprotocol.io/)
can call it directly from chat.

---

## Quick Start

1. **Install this extension.** VS Code registers the `acedatacloud` MCP server automatically.
2. **Get an API key** from [Ace Data Cloud](https://platform.acedata.cloud/console/applications) (Applications → API Key). New accounts include free trial credit.
3. **Open Copilot Chat** in agent mode and ask for a account task — the extension prompts for the API key the first time and stores it in the OS keychain via VS Code's `SecretStorage`.

You can rotate or remove the API key any time from the command palette:

- **Ace Data Cloud MCP: Set Ace Data Cloud API Key**
- **Ace Data Cloud MCP: Clear Ace Data Cloud API Key**

> The default config talks to the **hosted streamable-HTTP endpoint** at
> `https://mcp.acedata.cloud/mcp` — no Python, no `uvx`, no local install needed.

### Example prompts

- "What is my Ace Data Cloud balance and usage this month?"
- "List my Ace Data Cloud API keys and create a new one for testing."
- "Show recent orders and how much I have spent."

---

## Tool Reference



_Tool list is dynamically loaded from the server. Run a query to discover available tools._

## Pricing

Free — management API calls are not billed. Recharges use your existing balance. See full pricing at [https://docs.acedata.cloud](https://docs.acedata.cloud).

---

## Configuration

This extension implements the `mcpServerDefinitionProviders` contribution point
and registers a single hosted server with VS Code:

```text
Provider id : acedatacloud.acedatacloud
Server label: Ace Data Cloud MCP
Server URL  : https://mcp.acedata.cloud/mcp
Transport   : Streamable HTTP
Auth        : Bearer API key from VS Code SecretStorage (or $ACEDATACLOUD_PLATFORM_TOKEN)
```

You don't need to edit `mcp.json` — the extension handles registration and
token handling automatically. If you'd rather configure things by hand, the
sections below show equivalent `mcp.json` snippets you can use **instead of**
this extension.

### Alternative: manual `mcp.json` (hosted)

```jsonc
{
  "servers": {
    "acedatacloud": {
      "type": "http",
      "url": "https://mcp.acedata.cloud/mcp",
      "headers": { "Authorization": "Bearer ${input:acedatacloud_api_token}" }
    }
  },
  "inputs": [
    {
      "type": "promptString",
      "id": "acedatacloud_api_token",
    "description": "Ace Data Cloud API key",
      "password": true
    }
  ]
}
```

### Alternative: local stdio (no network roundtrip)

For offline dev, air-gapped environments, or pinning to a specific PyPI
version, install [`uv`](https://docs.astral.sh/uv/) and use:

```jsonc
{
  "servers": {
    "acedatacloud": {
      "type": "stdio",
      "command": "uvx",
      "args": ["mcp-acedatacloud"],
      "env": { "ACEDATACLOUD_PLATFORM_TOKEN": "${input:acedatacloud_api_token}" }
    }
  }
}
```

`uvx` will download and run the latest [`mcp-acedatacloud`](https://pypi.org/project/mcp-acedatacloud/) on demand.

---

## Links

- **Hosted endpoint:** https://mcp.acedata.cloud/mcp
- **PyPI package:** [`mcp-acedatacloud`](https://pypi.org/project/mcp-acedatacloud/)
- **Source repository:** https://github.com/AceDataCloud/AceDataCloudMCP
- **Ace Data Cloud platform:** https://platform.acedata.cloud
- **MCP documentation:** https://docs.acedata.cloud

## License

MIT — see [LICENSE](LICENSE).
