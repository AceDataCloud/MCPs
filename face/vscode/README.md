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
2. **Get an application API key** using the detailed steps below. Check service access and your current balance before the first request.
3. **Select a model with tool calling in VS Code Chat.** You can use your existing model, or install [Ace Data Cloud Chat Models](https://marketplace.visualstudio.com/items?itemName=acedatacloud.chat-models). For the Ace model, first follow its [setup guide](https://github.com/AceDataCloud/VSCodeModelProvider#4-show-the-model-in-chat), open **Chat: Manage Language Models**, make the model visible, and select it in Chat. BYOK Chat does not require GitHub sign-in or a Copilot plan; organization policies still apply.
4. **Enable this server's tools.** Open **Chat → Agent → Configure Tools** and select only the tools you need under **Face Transform MCP**. If the list is empty, choose **Update Tools**. The extension prompts for the API key on first use and saves it in VS Code's `SecretStorage`. Disable another copy of the same server from the Ace MCP bundle or manual `mcp.json` to avoid duplicate tools.
5. **Verify one result.** Check the Tool Reference below and current pricing before running a request. If you already have a task ID, enable its task-query tool and query that same ID first. An accepted generation is not a completed result: poll the original task until it reaches a successful terminal state, open the returned media, and match the task ID in [Usage](https://platform.acedata.cloud/console/usage?utm_source=vscode_marketplace&utm_medium=referral&utm_campaign=evergreen&utm_content=face_mcp_vscode_console_usage). Do not resubmit generation to poll. Model Chat and background utility calls can add separate charges to the service request.

You can rotate or remove the API key any time from the command palette:

- **Face Transform MCP: Set Ace Data Cloud API Key**
- **Face Transform MCP: Clear Ace Data Cloud API Key**

> The default config talks to the **hosted streamable-HTTP endpoint** at
> `https://face.mcp.acedata.cloud/mcp` — no Python, no `uvx`, no local install needed.

### Get your API key

<!-- BEGIN TOKEN ONBOARDING -->
1. Open [Ace Data Cloud → Applications](https://platform.acedata.cloud/console/applications?utm_source=vscode_marketplace&utm_medium=referral&utm_campaign=evergreen&utm_content=face_mcp_vscode_api_key). Sign in, or register an account first.
2. Find **General application**. If it has not been created, choose **Initialize General Application**. A general key can use the services available to your account; a dedicated application's key is limited to its service. Check the required service/model access and [current pricing](https://platform.acedata.cloud/models?utm_source=vscode_marketplace&utm_medium=referral&utm_campaign=evergreen&utm_content=face_mcp_vscode_models).
3. Copy the **API Key** from the application card, or open **Keys / Manage Keys → Create** to create a separate key for this integration. Give it a recognizable name so you can revoke or rotate it independently.
4. When creating a key, review **Expiration Time**, **Set Usage Limitation**, and **Allowed APIs**. Enable only the restrictions you need, allow the operations you will call, then click **Create** and copy the token from the key list. Task lookup does not grant permission to submit a generation. Confirm the application's balance can cover your first request; any trial allowance is whatever your account currently displays.
5. Copy only the token value, without quotation marks, spaces, or `Bearer `. An API Key / API Token field expects this raw value; only a manually configured HTTP `Authorization` header needs the `Bearer ` prefix. A `platform-...` account-management token cannot replace a generation API key.

![Copy an application API key or open Manage Keys](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/get-api-key-en.png)

![Create a separately named key with optional restrictions](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/create-api-key-en.png)

Save the key in the client's credential store or the environment variable shown below. Never put it in a prompt, shared workflow, screenshot, or Git commit. If authentication fails, check the full copied value, application/service access, expiration, usage limit, and balance before creating another key.
<!-- END TOKEN ONBOARDING -->

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
