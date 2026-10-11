# Face Transform MCP

Face analysis and transforms — keypoints, beautify, age/gender, swap, cartoon, liveness. (Alpha)


[![VS Code Marketplace](https://img.shields.io/visual-studio-marketplace/v/acedatacloud.mcp-face-transform?label=VS%20Code)](https://marketplace.visualstudio.com/items?itemName=acedatacloud.mcp-face-transform) [![PyPI](https://img.shields.io/pypi/v/mcp-face-transform.svg?label=PyPI)](https://pypi.org/project/mcp-face-transform/) [![Hosted MCP](https://img.shields.io/badge/hosted-mcp-blue)](https://face.mcp.acedata.cloud/mcp)

Bring AceDataCloud's Face Transform APIs into Copilot Chat. Detect 90+ keypoints per face, beautify portraits, age or de-age, swap perceived gender, face-swap between photos, cartoonize, and detect liveness.

This extension registers the **face** MCP server with VS Code so GitHub
Copilot and any other agent that speaks the [Model Context Protocol](https://modelcontextprotocol.io/)
can call it directly from chat.

---

## Quick Start

1. **Install this extension.** VS Code registers the `face` MCP server automatically.
2. **Get an API key** from [Ace Data Cloud](https://platform.acedata.cloud/console/applications?utm_source=vscode_marketplace&utm_medium=referral&utm_campaign=evergreen&utm_content=face_mcp_vscode_api_key) (Applications → API Key). New accounts include free trial credit.
3. **Open Copilot Chat** in agent mode and ask for an image task — the extension prompts for the API key the first time and stores it in the OS keychain via VS Code's `SecretStorage`.

You can rotate or remove the API key any time from the command palette:

- **Face Transform MCP: Set Ace Data Cloud API Key**
- **Face Transform MCP: Clear Ace Data Cloud API Key**

> The default config talks to the **hosted streamable-HTTP endpoint** at
> `https://face.mcp.acedata.cloud/mcp` — no Python, no `uvx`, no local install needed.

### Example prompts

- "Detect every face in https://example.com/group.jpg and return their keypoints."
- "Beautify https://example.com/me.jpg with smoothing 15 and whitening 25."
- "Swap the face from https://example.com/headshot.jpg onto https://example.com/scene.jpg."

---

## Tool Reference

**8 tools** available via this server.

| Tool | Description |
| --- | --- |
| `face_detect_keypoints` | Detect 90+ keypoints per face (multi-face supported). |
| `face_beautify` | Smoothing, whitening, face slimming, and eye enlarging. |
| `face_change_age` | Age or de-age a portrait. |
| `face_change_gender` | Swap perceived facial gender characteristics. |
| `face_swap` | Move a source face onto a target image (with optional async webhook). |
| `face_cartoonize` | Render a portrait in cartoon / animated style. |
| `face_detect_liveness` | Distinguish a live capture from a printed / screen photo. |
| `face_get_usage_guide` | Concise client-side tool usage reference. |

## Pricing

All Face APIs are currently in Alpha. Free trial credit on sign-up. See [Service details](https://platform.acedata.cloud/services/8efa1d83-9b75-4562-b44a-af95ce563d05?utm_source=vscode_marketplace&utm_medium=referral&utm_campaign=evergreen&utm_content=face_mcp_vscode_quick_start).

---

## Configuration

This extension implements the `mcpServerDefinitionProviders` contribution point
and registers a single hosted server with VS Code:

```text
Provider id : acedatacloud.face
Server label: Face Transform MCP
Server URL  : https://face.mcp.acedata.cloud/mcp
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
    "face": {
      "type": "http",
      "url": "https://face.mcp.acedata.cloud/mcp",
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
    "face": {
      "type": "stdio",
      "command": "uvx",
      "args": ["mcp-face-transform"],
      "env": { "ACEDATACLOUD_API_TOKEN": "${input:acedatacloud_api_token}" }
    }
  }
}
```

`uvx` will download and run the latest [`mcp-face-transform`](https://pypi.org/project/mcp-face-transform/) on demand.

---

## Links

- **Hosted endpoint:** https://face.mcp.acedata.cloud/mcp
- **PyPI package:** [`mcp-face-transform`](https://pypi.org/project/mcp-face-transform/)
- **Source repository:** https://github.com/AceDataCloud/FaceTransformMCP
- **Ace Data Cloud platform:** https://platform.acedata.cloud?utm_source=vscode_marketplace&utm_medium=referral&utm_campaign=evergreen&utm_content=face_mcp_vscode_platform
- **Service details:** https://platform.acedata.cloud/services/8efa1d83-9b75-4562-b44a-af95ce563d05?utm_source=vscode_marketplace&utm_medium=referral&utm_campaign=evergreen&utm_content=face_mcp_vscode_quick_start

## License

MIT — see [LICENSE](LICENSE).
