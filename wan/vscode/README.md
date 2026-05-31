# Wan MCP

Alibaba Wan video generation — text-to-video, image-to-video, reference video transfer.

[![VS Code Marketplace](https://img.shields.io/visual-studio-marketplace/v/acedatacloud.mcp-wan?label=VS%20Code)](https://marketplace.visualstudio.com/items?itemName=acedatacloud.mcp-wan) [![PyPI](https://img.shields.io/pypi/v/mcp-wan.svg?label=PyPI)](https://pypi.org/project/mcp-wan/) [![Hosted MCP](https://img.shields.io/badge/hosted-mcp-blue)](https://wan.mcp.acedata.cloud/mcp)

Generate AI video with Alibaba Wan in 480P/720P/1080P, with optional audio and reference-video transfer.

This extension registers the **wan** MCP server with VS Code so GitHub
Copilot and any other agent that speaks the [Model Context Protocol](https://modelcontextprotocol.io/)
can call it directly from chat.

---

## Quick Start

1. **Install this extension.** VS Code registers the `wan` MCP server automatically.
2. **Get an API token** from [Ace Data Cloud](https://platform.acedata.cloud) → *API Keys*. New accounts include free trial credit.
3. **Open Copilot Chat** in agent mode and ask for a video task — VS Code will prompt for the token the first time and store it securely.

> The default config talks to the **hosted streamable-HTTP endpoint** at
> `https://wan.mcp.acedata.cloud/mcp` — no Python, no `uvx`, no local install needed.

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

This extension contributes the following entry to your VS Code MCP config:

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

### Alternative: OAuth via Dynamic Client Registration

The hosted endpoint also accepts OAuth 2.1 with [DCR](https://datatracker.ietf.org/doc/html/rfc7591).
Drop the `headers` and `inputs` blocks and VS Code will run the auth flow on
first use (redirect URL `http://127.0.0.1:33418` or `https://vscode.dev/redirect`).

---

## Links

- **Hosted endpoint:** https://wan.mcp.acedata.cloud/mcp
- **PyPI package:** [`mcp-wan`](https://pypi.org/project/mcp-wan/)
- **Source repository:** https://github.com/AceDataCloud/WanMCP
- **Ace Data Cloud platform:** https://platform.acedata.cloud
- **MCP documentation:** https://docs.acedata.cloud

## License

MIT — see [LICENSE](LICENSE).
