# Luma MCP

AI video generation with Luma Dream Machine — text-to-video, image-to-video, extend.

[![VS Code Marketplace](https://img.shields.io/visual-studio-marketplace/v/acedatacloud.mcp-luma?label=VS%20Code)](https://marketplace.visualstudio.com/items?itemName=acedatacloud.mcp-luma) [![PyPI](https://img.shields.io/pypi/v/mcp-luma.svg?label=PyPI)](https://pypi.org/project/mcp-luma/) [![Hosted MCP](https://img.shields.io/badge/hosted-mcp-blue)](https://luma.mcp.acedata.cloud/mcp)

Generate short cinematic videos from text or stills with Luma Dream Machine, or extend an existing clip — directly from chat.

This extension registers the **luma** MCP server with VS Code so GitHub
Copilot and any other agent that speaks the [Model Context Protocol](https://modelcontextprotocol.io/)
can call it directly from chat.

---

## Quick Start

1. **Install this extension.** VS Code registers the `luma` MCP server automatically.
2. **Get an API key** from [Ace Data Cloud](https://platform.acedata.cloud/console/applications) (Applications → API Key). New accounts include free trial credit.
3. **Open Copilot Chat** in agent mode and ask for a video task — the extension prompts for the API key the first time and stores it in the OS keychain via VS Code's `SecretStorage`.

You can rotate or remove the API key any time from the command palette:

- **Luma MCP: Set Ace Data Cloud API Key**
- **Luma MCP: Clear Ace Data Cloud API Key**

> The default config talks to the **hosted streamable-HTTP endpoint** at
> `https://luma.mcp.acedata.cloud/mcp` — no Python, no `uvx`, no local install needed.

### Example prompts

- "Generate a 5-second video of a paper airplane drifting through neon clouds. Use luma."
- "Animate https://example.com/cat.jpg into a 5-second video of the cat yawning."

---

## Tool Reference

**8 tools** available via this server.

| Tool | Description |
| --- | --- |
| `luma_generate_video` | Generate AI video from a text prompt using Luma Dream Machine. |
| `luma_generate_video_from_image` | Generate AI video using reference images as start and/or end frames. |
| `luma_extend_video` | Extend an existing video with additional content. |
| `luma_extend_video_from_url` | Extend an existing video using its URL. |
| `luma_get_task` | Query the status and result of a video generation task. |
| `luma_get_tasks_batch` | Query multiple video generation tasks at once. |
| `luma_list_aspect_ratios` | List all available aspect ratios for Luma video generation. |
| `luma_list_actions` | List all available Luma API actions and corresponding tools. |

## Pricing

From $0.35 per 5s clip. Free trial credit on sign-up. See full pricing at [https://docs.acedata.cloud](https://docs.acedata.cloud).

---

## Configuration

This extension implements the `mcpServerDefinitionProviders` contribution point
and registers a single hosted server with VS Code:

```text
Provider id : acedatacloud.luma
Server label: Luma MCP
Server URL  : https://luma.mcp.acedata.cloud/mcp
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
    "luma": {
      "type": "http",
      "url": "https://luma.mcp.acedata.cloud/mcp",
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
    "luma": {
      "type": "stdio",
      "command": "uvx",
      "args": ["mcp-luma"],
      "env": { "ACEDATACLOUD_API_TOKEN": "${input:acedatacloud_api_token}" }
    }
  }
}
```

`uvx` will download and run the latest [`mcp-luma`](https://pypi.org/project/mcp-luma/) on demand.

---

## Links

- **Hosted endpoint:** https://luma.mcp.acedata.cloud/mcp
- **PyPI package:** [`mcp-luma`](https://pypi.org/project/mcp-luma/)
- **Source repository:** https://github.com/AceDataCloud/LumaMCP
- **Ace Data Cloud platform:** https://platform.acedata.cloud
- **MCP documentation:** https://docs.acedata.cloud

## License

MIT — see [LICENSE](LICENSE).
