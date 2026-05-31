# Serp MCP

Google Search via Ace Data Cloud — web, images, news, maps, local, video.

[![VS Code Marketplace](https://img.shields.io/visual-studio-marketplace/v/acedatacloud.mcp-serp?label=VS%20Code)](https://marketplace.visualstudio.com/items?itemName=acedatacloud.mcp-serp) [![PyPI](https://img.shields.io/pypi/v/mcp-serp.svg?label=PyPI)](https://pypi.org/project/mcp-serp/) [![Hosted MCP](https://img.shields.io/badge/hosted-mcp-blue)](https://serp.mcp.acedata.cloud/mcp)

Give Copilot live Google search results — web pages, images, news, maps, local places, and videos — with localization and time filters.

This extension registers the **serp** MCP server with VS Code so GitHub
Copilot and any other agent that speaks the [Model Context Protocol](https://modelcontextprotocol.io/)
can call it directly from chat.

---

## Quick Start

1. **Install this extension.** VS Code registers the `serp` MCP server automatically.
2. **Get an API key** from [Ace Data Cloud](https://platform.acedata.cloud/console/applications) (Applications → API Key). New accounts include free trial credit.
3. **Open Copilot Chat** in agent mode and ask for a search task — the extension prompts for the API key the first time and stores it in the OS keychain via VS Code's `SecretStorage`.

You can rotate or remove the API key any time from the command palette:

- **Serp MCP: Set Ace Data Cloud API Key**
- **Serp MCP: Clear Ace Data Cloud API Key**

> The default config talks to the **hosted streamable-HTTP endpoint** at
> `https://serp.mcp.acedata.cloud/mcp` — no Python, no `uvx`, no local install needed.

### Example prompts

- "Search Google for the most recent news on the EU AI Act and summarize it."
- "Find image results for "mid-century modern living room", give me 10 URLs."
- "Search Google Maps for coffee shops near "1 Infinite Loop, Cupertino"."

---

## Tool Reference

**11 tools** available via this server.

| Tool | Description |
| --- | --- |
| `serp_google_search` | Search Google and get structured results using the SERP API. |
| `serp_google_images` | Search Google Images and get image results. |
| `serp_google_news` | Search Google News and get news article results. |
| `serp_google_videos` | Search Google Videos and get video results. |
| `serp_google_places` | Search Google for local places and businesses. |
| `serp_google_maps` | Search Google Maps for locations. |
| `serp_list_search_types` | List all available Google search types. |
| `serp_list_countries` | List commonly used country codes for Google search. |
| `serp_list_languages` | List commonly used language codes for Google search. |
| `serp_list_time_ranges` | List available time range filters for Google search. |
| `serp_get_usage_guide` | Get a comprehensive guide for using the Google SERP tools. |

## Pricing

From $0.003 per query. Free trial credit on sign-up. See full pricing at [https://docs.acedata.cloud](https://docs.acedata.cloud).

---

## Configuration

This extension implements the `mcpServerDefinitionProviders` contribution point
and registers a single hosted server with VS Code:

```text
Provider id : acedatacloud.serp
Server label: Serp MCP
Server URL  : https://serp.mcp.acedata.cloud/mcp
Transport   : Streamable HTTP
Auth        : Bearer API key from VS Code SecretStorage (or $ACEDATACLOUD_API_TOKEN)
```

You don't need to edit `mcp.json` — the extension handles registration and
token handling automatically. If you'd rather configure things by hand, the
sections below show equivalent `mcp.json` snippets you can use **instead of**
this extension.

### Alternative: manual `mcp.json` (hosted)

```jsonc
{
  "servers": {
    "serp": {
      "type": "http",
      "url": "https://serp.mcp.acedata.cloud/mcp",
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
    "serp": {
      "type": "stdio",
      "command": "uvx",
      "args": ["mcp-serp"],
      "env": { "ACEDATACLOUD_API_TOKEN": "${input:acedatacloud_api_token}" }
    }
  }
}
```

`uvx` will download and run the latest [`mcp-serp`](https://pypi.org/project/mcp-serp/) on demand.

---

## Links

- **Hosted endpoint:** https://serp.mcp.acedata.cloud/mcp
- **PyPI package:** [`mcp-serp`](https://pypi.org/project/mcp-serp/)
- **Source repository:** https://github.com/AceDataCloud/SerpMCP
- **Ace Data Cloud platform:** https://platform.acedata.cloud
- **MCP documentation:** https://docs.acedata.cloud

## License

MIT — see [LICENSE](LICENSE).
