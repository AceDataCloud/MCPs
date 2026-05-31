# Short URL MCP

Create short URLs (surl.id) — single or batch, with custom slugs and expiration.

[![VS Code Marketplace](https://img.shields.io/visual-studio-marketplace/v/acedatacloud.mcp-shorturl?label=VS%20Code)](https://marketplace.visualstudio.com/items?itemName=acedatacloud.mcp-shorturl) [![PyPI](https://img.shields.io/pypi/v/mcp-shorturl.svg?label=PyPI)](https://pypi.org/project/mcp-shorturl/) [![Hosted MCP](https://img.shields.io/badge/hosted-mcp-blue)](https://shorturl.mcp.acedata.cloud/mcp)

Shorten long URLs into surl.id links, optionally with a custom slug or expiration. Supports batch creation.

This extension registers the **shorturl** MCP server with VS Code so GitHub
Copilot and any other agent that speaks the [Model Context Protocol](https://modelcontextprotocol.io/)
can call it directly from chat.

---

## Quick Start

1. **Install this extension.** VS Code registers the `shorturl` MCP server automatically.
2. **Get an API token** from [Ace Data Cloud](https://platform.acedata.cloud) → *API Keys*. New accounts include free trial credit.
3. **Open Copilot Chat** in agent mode and ask for a utility task — the extension prompts for the token the first time and stores it in the OS keychain via VS Code's `SecretStorage`.

You can rotate or remove the token any time from the command palette:

- **Short URL MCP: Set Ace Data Cloud API Token**
- **Short URL MCP: Clear Ace Data Cloud API Token**

> The default config talks to the **hosted streamable-HTTP endpoint** at
> `https://shorturl.mcp.acedata.cloud/mcp` — no Python, no `uvx`, no local install needed.

### Example prompts

- "Shorten this URL: https://platform.acedata.cloud/documents/... with slug "ace-docs"."
- "Batch-shorten these 5 URLs (paste the list) and give me a markdown table."

---

## Tool Reference

**4 tools** available via this server.

| Tool | Description |
| --- | --- |
| `shorturl_create` | Create a short URL from a long URL. |
| `shorturl_batch_create` | Create short URLs for multiple long URLs in a single batch. |
| `shorturl_get_usage_guide` | Get a comprehensive guide for using the ShortURL tools. |
| `shorturl_get_api_info` | Get information about the ShortURL API service. |

## Pricing

Free tier available. Higher quotas with paid plans. See full pricing at [https://docs.acedata.cloud](https://docs.acedata.cloud).

---

## Configuration

This extension implements the `mcpServerDefinitionProviders` contribution point
and registers a single hosted server with VS Code:

```text
Provider id : acedatacloud.shorturl
Server label: Short URL MCP
Server URL  : https://shorturl.mcp.acedata.cloud/mcp
Transport   : Streamable HTTP
Auth        : Bearer token from VS Code SecretStorage (or $ACEDATACLOUD_API_TOKEN)
```

You don't need to edit `mcp.json` — the extension handles registration and
token handling automatically. If you'd rather configure things by hand, the
sections below show equivalent `mcp.json` snippets you can use **instead of**
this extension.

### Alternative: manual `mcp.json` (hosted)

```jsonc
{
  "servers": {
    "shorturl": {
      "type": "http",
      "url": "https://shorturl.mcp.acedata.cloud/mcp",
      "headers": { "Authorization": "Bearer ${input:acedatacloud_api_token}" }
    }
  },
  "inputs": [
    {
      "type": "promptString",
      "id": "acedatacloud_api_token",
      "description": "Ace Data Cloud API token",
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
    "shorturl": {
      "type": "stdio",
      "command": "uvx",
      "args": ["mcp-shorturl"],
      "env": { "ACEDATACLOUD_API_TOKEN": "${input:acedatacloud_api_token}" }
    }
  }
}
```

`uvx` will download and run the latest [`mcp-shorturl`](https://pypi.org/project/mcp-shorturl/) on demand.

---

## Links

- **Hosted endpoint:** https://shorturl.mcp.acedata.cloud/mcp
- **PyPI package:** [`mcp-shorturl`](https://pypi.org/project/mcp-shorturl/)
- **Source repository:** https://github.com/AceDataCloud/ShortURLMCP
- **Ace Data Cloud platform:** https://platform.acedata.cloud
- **MCP documentation:** https://docs.acedata.cloud

## License

MIT — see [LICENSE](LICENSE).
