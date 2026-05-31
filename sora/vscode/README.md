# Sora MCP

OpenAI Sora video generation — text-to-video, image-to-video, character references.

[![VS Code Marketplace](https://img.shields.io/visual-studio-marketplace/v/acedatacloud.mcp-sora?label=VS%20Code)](https://marketplace.visualstudio.com/items?itemName=acedatacloud.mcp-sora) [![PyPI](https://img.shields.io/pypi/v/mcp-sora.svg?label=PyPI)](https://pypi.org/project/mcp-sora/) [![Hosted MCP](https://img.shields.io/badge/hosted-mcp-blue)](https://sora.mcp.acedata.cloud/mcp)

Generate short Sora videos from text prompts, animate stills, or carry a character reference across clips. Sora 1 and Sora 2 models supported.

This extension registers the **sora** MCP server with VS Code so GitHub
Copilot and any other agent that speaks the [Model Context Protocol](https://modelcontextprotocol.io/)
can call it directly from chat.

---

## Quick Start

1. **Install this extension.** VS Code registers the `sora` MCP server automatically.
2. **Get an API token** from [Ace Data Cloud](https://platform.acedata.cloud) → *API Keys*. New accounts include free trial credit.
3. **Open Copilot Chat** in agent mode and ask for a video task — the extension prompts for the token the first time and stores it in the OS keychain via VS Code's `SecretStorage`.

You can rotate or remove the token any time from the command palette:

- **Sora MCP: Set Ace Data Cloud API Token**
- **Sora MCP: Clear Ace Data Cloud API Token**

> The default config talks to the **hosted streamable-HTTP endpoint** at
> `https://sora.mcp.acedata.cloud/mcp` — no Python, no `uvx`, no local install needed.

### Example prompts

- "Generate a Sora video: time-lapse of a coffee being poured in slow motion. Use sora 2 portrait."
- "Animate https://example.com/dog.jpg into a Sora clip of the dog walking through a meadow."

---

## Tool Reference

**10 tools** available via this server.

| Tool | Description |
| --- | --- |
| `sora_generate_video` | Generate an AI video from a text prompt using Sora. |
| `sora_generate_video_from_image` | Generate an AI video from reference images using Sora (Image-to-Video). |
| `sora_generate_video_with_character` | Generate an AI video featuring a character from a reference video. |
| `sora_generate_video_async` | Generate an AI video asynchronously with callback notification. |
| `sora_generate_video_v2` | Generate an AI video using Sora Version 2 (partner channel). |
| `sora_generate_video_v2_async` | Generate an AI video asynchronously using Sora Version 2 with callback. |
| `sora_get_task` | Query the status and result of a video generation task. |
| `sora_get_tasks_batch` | Query multiple video generation tasks at once. |
| `sora_list_models` | List all available Sora models and their capabilities. |
| `sora_list_actions` | List all available Sora API actions and corresponding tools. |

## Supported Models

`sora-1`, `sora-2`

## Pricing

From $0.50 per clip. Free trial credit on sign-up. See full pricing at [https://docs.acedata.cloud](https://docs.acedata.cloud).

---

## Configuration

This extension implements the `mcpServerDefinitionProviders` contribution point
and registers a single hosted server with VS Code:

```text
Provider id : acedatacloud.sora
Server label: Sora MCP
Server URL  : https://sora.mcp.acedata.cloud/mcp
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
    "sora": {
      "type": "http",
      "url": "https://sora.mcp.acedata.cloud/mcp",
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
    "sora": {
      "type": "stdio",
      "command": "uvx",
      "args": ["mcp-sora"],
      "env": { "ACEDATACLOUD_API_TOKEN": "${input:acedatacloud_api_token}" }
    }
  }
}
```

`uvx` will download and run the latest [`mcp-sora`](https://pypi.org/project/mcp-sora/) on demand.

---

## Links

- **Hosted endpoint:** https://sora.mcp.acedata.cloud/mcp
- **PyPI package:** [`mcp-sora`](https://pypi.org/project/mcp-sora/)
- **Source repository:** https://github.com/AceDataCloud/SoraMCP
- **Ace Data Cloud platform:** https://platform.acedata.cloud
- **MCP documentation:** https://docs.acedata.cloud

## License

MIT — see [LICENSE](LICENSE).
