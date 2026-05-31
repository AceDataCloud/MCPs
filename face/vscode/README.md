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
2. **Get an API token** from [Ace Data Cloud](https://platform.acedata.cloud) → *API Keys*. New accounts include free trial credit.
3. **Open Copilot Chat** in agent mode and ask for a image task — VS Code will prompt for the token the first time and store it securely.

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

All Face APIs are currently in Alpha. Free trial credit on sign-up. See full pricing at [https://docs.acedata.cloud](https://docs.acedata.cloud).

---

## Configuration

This extension contributes the following entry to your VS Code MCP config:

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

### Alternative: OAuth via Dynamic Client Registration

The hosted endpoint also accepts OAuth 2.1 with [DCR](https://datatracker.ietf.org/doc/html/rfc7591).
Drop the `headers` and `inputs` blocks and VS Code will run the auth flow on
first use (redirect URL `http://127.0.0.1:33418` or `https://vscode.dev/redirect`).

---

## Links

- **Hosted endpoint:** https://face.mcp.acedata.cloud/mcp
- **PyPI package:** [`mcp-face-transform`](https://pypi.org/project/mcp-face-transform/)
- **Source repository:** https://github.com/AceDataCloud/FaceTransformMCP
- **Ace Data Cloud platform:** https://platform.acedata.cloud
- **MCP documentation:** https://docs.acedata.cloud

## License

MIT — see [LICENSE](LICENSE).
