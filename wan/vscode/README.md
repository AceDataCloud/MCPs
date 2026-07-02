# Wan MCP

Alibaba Wan video generation — text-to-video, image-to-video, reference video transfer.

[![VS Code Marketplace](https://img.shields.io/badge/VS%20Code-Marketplace-blue?logo=visualstudiocode&logoColor=white)](https://marketplace.visualstudio.com/items?itemName=acedatacloud.mcp-wan) [![PyPI](https://img.shields.io/pypi/v/mcp-wan.svg?label=PyPI)](https://pypi.org/project/mcp-wan/) [![Hosted MCP](https://img.shields.io/badge/hosted-mcp-blue)](https://wan.mcp.acedata.cloud/mcp)

Generate AI video with Alibaba Wan in 480P/720P/1080P, with optional audio and reference-video transfer.

This extension registers the **wan** MCP server with VS Code so GitHub
Copilot and any other agent that speaks the [Model Context Protocol](https://modelcontextprotocol.io/)
can call it directly from chat.

---

## Quick Start

1. **Install this extension.** VS Code registers the `wan` MCP server automatically.
2. **Get an API key** from [Ace Data Cloud](https://platform.acedata.cloud/console/applications) (Applications → API Key). New accounts include free trial credit.
3. **Open Copilot Chat** in agent mode and ask for a video task — the extension prompts for the API key the first time and stores it in the OS keychain via VS Code's `SecretStorage`.

You can rotate or remove the API key any time from the command palette:

- **Wan MCP: Set Ace Data Cloud API Key**
- **Wan MCP: Clear Ace Data Cloud API Key**

> The default config talks to the **hosted streamable-HTTP endpoint** at
> `https://wan.mcp.acedata.cloud/mcp` — no Python, no `uvx`, no local install needed.

## VS Code Setup Guide

For the full VS Code walkthrough, see [All Ace Data Cloud MCP servers in VS Code](https://platform.acedata.cloud/documents/promotion_article_mcp_all_vscode). It covers token setup, project-level and user-level `mcp.json`, Copilot Agent Mode, and using one Ace Data Cloud token across hosted MCP servers.

### Example prompts

- "Generate a Wan 1080P video of waves crashing on a black-sand beach, with ambient audio."
- "Transfer the motion of reference video <id> onto https://example.com/character.png."

---

## Tool Reference

**7 tools** available via this server.

| Tool | Description |
| --- | --- |
| `wan_generate_video` | Generate AI video from a text prompt using Wan. |
| `wan_generate_video_from_image` | Generate AI video using a reference image as the starting frame. |
| `wan_get_task` | Query the status and result of a video generation task. |
| `wan_get_tasks_batch` | Query multiple video generation tasks at once. |
| `wan_list_models` | List all available Wan models for video generation. |
| `wan_list_resolutions` | List all available resolution options. |
| `wan_list_actions` | List all available Wan API actions and corresponding tools. |

## Pricing

From $0.18 per clip. Free trial credit on sign-up. See full pricing at [https://docs.acedata.cloud](https://docs.acedata.cloud).

---

## Configuration

This extension implements the `mcpServerDefinitionProviders` contribution point
and registers a single hosted server with VS Code:

```text
Provider id : acedatacloud.wan
Server label: Wan MCP
Server URL  : https://wan.mcp.acedata.cloud/mcp
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
    "wan": {
      "type": "http",
      "url": "https://wan.mcp.acedata.cloud/mcp",
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
    "wan": {
      "type": "stdio",
      "command": "uvx",
      "args": ["mcp-wan"],
      "env": { "ACEDATACLOUD_API_TOKEN": "${input:acedatacloud_api_token}" }
    }
  }
}
```

`uvx` will download and run the latest [`mcp-wan`](https://pypi.org/project/mcp-wan/) on demand.

---

## Links

- **Hosted endpoint:** https://wan.mcp.acedata.cloud/mcp
- **PyPI package:** [`mcp-wan`](https://pypi.org/project/mcp-wan/)
- **Source repository:** https://github.com/AceDataCloud/WanMCP
- **Ace Data Cloud platform:** https://platform.acedata.cloud
- **MCP documentation:** https://docs.acedata.cloud

## License

MIT — see [LICENSE](LICENSE).
