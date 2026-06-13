# Grok MCP

Google Grok video generation — Grok 2, Grok 3, Grok 3.1 (incl. fast variants and upscale).

[![VS Code Marketplace](https://img.shields.io/visual-studio-marketplace/v/acedatacloud.mcp-grok?label=VS%20Code)](https://marketplace.visualstudio.com/items?itemName=acedatacloud.mcp-grok) [![PyPI](https://img.shields.io/pypi/v/mcp-grok.svg?label=PyPI)](https://pypi.org/project/mcp-grok/) [![Hosted MCP](https://img.shields.io/badge/hosted-mcp-blue)](https://grok.mcp.acedata.cloud/mcp)

Generate AI video with Google Grok from text or images, including high-quality Grok 3.1 and the fast variants. Supports 1080p upscale.

This extension registers the **grok** MCP server with VS Code so GitHub
Copilot and any other agent that speaks the [Model Context Protocol](https://modelcontextprotocol.io/)
can call it directly from chat.

---

## Quick Start

1. **Install this extension.** VS Code registers the `grok` MCP server automatically.
2. **Get an API key** from [Ace Data Cloud](https://platform.acedata.cloud/console/applications) (Applications → API Key). New accounts include free trial credit.
3. **Open Copilot Chat** in agent mode and ask for a video task — the extension prompts for the API key the first time and stores it in the OS keychain via VS Code's `SecretStorage`.

You can rotate or remove the API key any time from the command palette:

- **Grok MCP: Set Ace Data Cloud API Key**
- **Grok MCP: Clear Ace Data Cloud API Key**

> The default config talks to the **hosted streamable-HTTP endpoint** at
> `https://grok.mcp.acedata.cloud/mcp` — no Python, no `uvx`, no local install needed.

## VS Code Setup Guide

For screenshots, token setup, project-level and user-level `mcp.json`, and Copilot Agent Mode examples, see:

- [Grok MCP VS Code guide](https://platform.acedata.cloud/documents/promotion_article_mcp_grok_vscode)
- [All Ace Data Cloud MCP servers in VS Code](https://platform.acedata.cloud/documents/promotion_article_mcp_all_vscode)

### Example prompts

- "Generate a Grok 3.1 video of a vintage train pulling into a snowy station at dusk."
- "Animate https://example.com/portrait.jpg into a Grok Fast clip with subtle head turn."

---

## Tool Reference

**12 tools** available via this server.

| Tool | Description |
| --- | --- |
| `grok_text_to_video` | Generate AI video from a text prompt using Grok. |
| `grok_image_to_video` | Generate AI video from one or more reference images using Grok. |
| `grok_get_1080p` | Get the 1080p high-resolution version of a generated video. |
| `grok_upsample` | Upsample a generated video to 1080p, 4K, or GIF. |
| `grok_extend_video` | Extend a Grok 3.1 video with additional content. |
| `grok_reshoot` | Re-render an existing video with a different camera motion. |
| `grok_video_objects` | Insert or remove objects in a generated video. |
| `grok_get_task` | Query the status and result of a video generation task. |
| `grok_get_tasks_batch` | Query multiple video generation tasks at once. |
| `grok_list_models` | List all available Grok models and their capabilities. |
| `grok_list_actions` | List all available Grok API actions and corresponding tools. |
| `grok_get_prompt_guide` | Get guidance on writing effective prompts for Grok video generation. |

## Supported Models

`grok-2`, `grok-2-fast`, `grok-3`, `grok-3-fast`, `grok-3.1`, `grok-3.1-fast`

## Pricing

From $0.30 per clip. Free trial credit on sign-up. See full pricing at [https://docs.acedata.cloud](https://docs.acedata.cloud).

---

## Configuration

This extension implements the `mcpServerDefinitionProviders` contribution point
and registers a single hosted server with VS Code:

```text
Provider id : acedatacloud.grok
Server label: Grok MCP
Server URL  : https://grok.mcp.acedata.cloud/mcp
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
    "grok": {
      "type": "http",
      "url": "https://grok.mcp.acedata.cloud/mcp",
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
    "grok": {
      "type": "stdio",
      "command": "uvx",
      "args": ["mcp-grok"],
      "env": { "ACEDATACLOUD_API_TOKEN": "${input:acedatacloud_api_token}" }
    }
  }
}
```

`uvx` will download and run the latest [`mcp-grok`](https://pypi.org/project/mcp-grok/) on demand.

---

## Links

- **Hosted endpoint:** https://grok.mcp.acedata.cloud/mcp
- **PyPI package:** [`mcp-grok`](https://pypi.org/project/mcp-grok/)
- **Source repository:** https://github.com/AceDataCloud/GrokMCP
- **Ace Data Cloud platform:** https://platform.acedata.cloud
- **MCP documentation:** https://docs.acedata.cloud

## License

MIT — see [LICENSE](LICENSE).
