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
3. **Open Copilot Chat** in agent mode and ask for a utility task — VS Code will prompt for the token the first time and store it securely.

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

This extension contributes the following entry to your VS Code MCP config:

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

VS Code will prompt for the token on first use and persist it in the OS
secret store (Keychain / Credential Manager / libsecret).

### Alternative: local stdio (no network roundtrip)

If you prefer running the server locally — for offline dev, air-gapped
environments, or to pin to a specific PyPI version — install
[`uv`](https://docs.astral.sh/uv/) and replace your `mcp.json` entry with:

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

### Alternative: OAuth via Dynamic Client Registration

The hosted endpoint also accepts OAuth 2.1 with [DCR](https://datatracker.ietf.org/doc/html/rfc7591).
Drop the `headers` and `inputs` blocks and VS Code will run the auth flow on
first use (redirect URL `http://127.0.0.1:33418` or `https://vscode.dev/redirect`).

---

## Links

- **Hosted endpoint:** https://shorturl.mcp.acedata.cloud/mcp
- **PyPI package:** [`mcp-shorturl`](https://pypi.org/project/mcp-shorturl/)
- **Source repository:** https://github.com/AceDataCloud/ShortURLMCP
- **Ace Data Cloud platform:** https://platform.acedata.cloud
- **MCP documentation:** https://docs.acedata.cloud

## License

MIT — see [LICENSE](LICENSE).
