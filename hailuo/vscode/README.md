# Hailuo MCP

Hailuo (MiniMax) AI video — text-to-video and image-to-video with director mode.

[![VS Code Marketplace](https://img.shields.io/visual-studio-marketplace/v/acedatacloud.mcp-hailuo?label=VS%20Code)](https://marketplace.visualstudio.com/items?itemName=acedatacloud.mcp-hailuo) [![PyPI](https://img.shields.io/pypi/v/mcp-hailuo.svg?label=PyPI)](https://pypi.org/project/mcp-hailuo/) [![Hosted MCP](https://img.shields.io/badge/hosted-mcp-blue)](https://hailuo.mcp.acedata.cloud/mcp)

Generate AI video using MiniMax Hailuo. Includes director-mode camera control for precise framing.

This extension registers the **hailuo** MCP server with VS Code so GitHub
Copilot and any other agent that speaks the [Model Context Protocol](https://modelcontextprotocol.io/)
can call it directly from chat.

---

## Quick Start

1. **Install this extension.** VS Code registers the `hailuo` MCP server automatically.
2. **Get an API token** from [Ace Data Cloud](https://platform.acedata.cloud) → *API Keys*. New accounts include free trial credit.
3. **Open Copilot Chat** in agent mode and ask for a video task — VS Code will prompt for the token the first time and store it securely.

> The default config talks to the **hosted streamable-HTTP endpoint** at
> `https://hailuo.mcp.acedata.cloud/mcp` — no Python, no `uvx`, no local install needed.

### Example prompts

- "Generate a Hailuo video: a chef tossing a pizza in slow motion, dolly-in shot."
- "Animate https://example.com/sketch.jpg into a 6-second Hailuo clip, pan-right."

---

## Tool Reference

**6 tools** available via this server.

| Tool | Description |
| --- | --- |
| `hailuo_generate_video` | Generate AI video from a text prompt using Hailuo (MiniMax). |
| `hailuo_generate_video_from_image` | Generate AI video from a reference image using Hailuo (MiniMax). |
| `hailuo_get_task` | Query the status and result of a video generation task. |
| `hailuo_get_tasks_batch` | Query multiple video generation tasks at once. |
| `hailuo_list_models` | List all available Hailuo models for video generation. |
| `hailuo_list_actions` | List all available Hailuo API actions and corresponding tools. |

## Pricing

From $0.20 per clip. Free trial credit on sign-up. See full pricing at [https://docs.acedata.cloud](https://docs.acedata.cloud).

---

## Configuration

This extension contributes the following entry to your VS Code MCP config:

```jsonc
{
  "servers": {
    "hailuo": {
      "type": "http",
      "url": "https://hailuo.mcp.acedata.cloud/mcp",
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
    "hailuo": {
      "type": "stdio",
      "command": "uvx",
      "args": ["mcp-hailuo"],
      "env": { "ACEDATACLOUD_API_TOKEN": "${input:acedatacloud_api_token}" }
    }
  }
}
```

`uvx` will download and run the latest [`mcp-hailuo`](https://pypi.org/project/mcp-hailuo/) on demand.

### Alternative: OAuth via Dynamic Client Registration

The hosted endpoint also accepts OAuth 2.1 with [DCR](https://datatracker.ietf.org/doc/html/rfc7591).
Drop the `headers` and `inputs` blocks and VS Code will run the auth flow on
first use (redirect URL `http://127.0.0.1:33418` or `https://vscode.dev/redirect`).

---

## Links

- **Hosted endpoint:** https://hailuo.mcp.acedata.cloud/mcp
- **PyPI package:** [`mcp-hailuo`](https://pypi.org/project/mcp-hailuo/)
- **Source repository:** https://github.com/AceDataCloud/HailuoMCP
- **Ace Data Cloud platform:** https://platform.acedata.cloud
- **MCP documentation:** https://docs.acedata.cloud

## License

MIT — see [LICENSE](LICENSE).
