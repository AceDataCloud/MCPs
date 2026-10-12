# NanoBanana MCP

Gemini-powered NanoBanana — generate and edit images via natural language.

[![VS Code Marketplace](https://img.shields.io/badge/VS%20Code-Marketplace-blue?logo=visualstudiocode&logoColor=white)](https://marketplace.visualstudio.com/items?itemName=acedatacloud.mcp-nanobanana) [![PyPI](https://img.shields.io/pypi/v/mcp-nanobanana-pro.svg?label=PyPI)](https://pypi.org/project/mcp-nanobanana-pro/) [![Hosted MCP](https://img.shields.io/badge/hosted-mcp-blue)](https://nanobanana.mcp.acedata.cloud/mcp)

Image generation and edit-by-instruction using NanoBanana, NanoBanana 2, and NanoBanana Pro (built on Gemini).

This extension registers the **nanobanana** MCP server with VS Code so GitHub
Copilot and any other agent that speaks the [Model Context Protocol](https://modelcontextprotocol.io/)
can call it directly from chat.

---

## Quick Start

1. **Install this extension.** VS Code registers the `nanobanana` MCP server automatically.
2. **Get an application API key** using the detailed steps below. Check service access and your current balance before the first request.
3. **Open Copilot Chat** in agent mode and ask for a image task — the extension prompts for the API key the first time and stores it in the OS keychain via VS Code's `SecretStorage`.

You can rotate or remove the API key any time from the command palette:

- **NanoBanana MCP: Set Ace Data Cloud API Key**
- **NanoBanana MCP: Clear Ace Data Cloud API Key**

> The default config talks to the **hosted streamable-HTTP endpoint** at
> `https://nanobanana.mcp.acedata.cloud/mcp` — no Python, no `uvx`, no local install needed.

### Get your API key

<!-- BEGIN TOKEN ONBOARDING -->
1. Open [Ace Data Cloud → Applications](https://platform.acedata.cloud/console/applications?utm_source=vscode_marketplace&utm_medium=referral&utm_campaign=evergreen&utm_content=nanobanana_mcp_vscode_api_key). Sign in, or register an account first.
2. Find **General application**. If it has not been created, choose **Initialize General Application**. A general key can use the services available to your account; a dedicated application's key is limited to its service. Check the required service/model access and [current pricing](https://platform.acedata.cloud/models?utm_source=vscode_marketplace&utm_medium=referral&utm_campaign=evergreen&utm_content=nanobanana_mcp_vscode_models).
3. Copy the **API Key** from the application card, or open **Keys / Manage Keys → Create** to create a separate key for this integration. Give it a recognizable name so you can revoke or rotate it independently.
4. When creating a key, review **Expiration Time**, **Set Usage Limitation**, and **Allowed APIs**. Enable only the restrictions you need, allow the operations you will call, then click **Create** and copy the token from the key list. Task lookup does not grant permission to submit a generation. Confirm the application's balance can cover your first request; any trial allowance is whatever your account currently displays.
5. Copy only the token value, without quotation marks, spaces, or `Bearer `. An API Key / API Token field expects this raw value; only a manually configured HTTP `Authorization` header needs the `Bearer ` prefix. A `platform-...` account-management token cannot replace a generation API key.

![Copy an application API key or open Manage Keys](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/get-api-key-en.png)

![Create a separately named key with optional restrictions](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/create-api-key-en.png)

Save the key in the client's credential store or the environment variable shown below. Never put it in a prompt, shared workflow, screenshot, or Git commit. If authentication fails, check the full copied value, application/service access, expiration, usage limit, and balance before creating another key.
<!-- END TOKEN ONBOARDING -->

## VS Code Setup Guide

For screenshots, token setup, project-level and user-level `mcp.json`, and Copilot Agent Mode examples, see:

- [NanoBanana MCP VS Code guide](https://platform.acedata.cloud/documents/promotion_article_mcp_nanobanana_vscode?utm_source=vscode_marketplace&utm_medium=referral&utm_campaign=evergreen&utm_content=nanobanana_mcp_vscode_documents_promotion_article_mcp_nanobanana_vscode)
- [All Ace Data Cloud MCP servers in VS Code](https://platform.acedata.cloud/documents/promotion_article_mcp_all_vscode?utm_source=vscode_marketplace&utm_medium=referral&utm_campaign=evergreen&utm_content=nanobanana_mcp_vscode_documents_promotion_article_mcp_all_vscode)

### Example prompts

- "Generate a watercolor postcard of Kyoto in cherry-blossom season. Use nanobanana pro."
- "Edit https://example.com/desk.jpg — clear the desk and add a single houseplant."

---

## Tool Reference

**4 tools** available via this server.

| Tool | Description |
| --- | --- |
| `nanobanana_generate_image` | Generate an AI image from a text prompt using Google's Nano Banana model. |
| `nanobanana_edit_image` | Edit or combine images using AI based on a text prompt. |
| `nanobanana_get_task` | Query the status and result of an image generation or edit task. |
| `nanobanana_get_tasks_batch` | Query multiple image generation/edit tasks at once. |

## Supported Models

`nano-banana`, `nano-banana-2-lite`, `nano-banana-2`, `nano-banana-2.1`, `nano-banana-pro`

Nano Banana 2.1 supports 1K, 2K, and 4K generation and editing. Use exactly `nano-banana-2.1`; it has no `:official` variant. The default remains `nano-banana`.

## Pricing

From $0.015 per image. Free trial credit on sign-up. See full pricing at [https://platform.acedata.cloud/documents/nano-banana-mcp](https://platform.acedata.cloud/documents/nano-banana-mcp?utm_source=vscode_marketplace&utm_medium=referral&utm_campaign=evergreen&utm_content=nanobanana_mcp_vscode_quick_start).

---

## Configuration

This extension implements the `mcpServerDefinitionProviders` contribution point
and registers a single hosted server with VS Code:

```text
Provider id : acedatacloud.nanobanana
Server label: NanoBanana MCP
Server URL  : https://nanobanana.mcp.acedata.cloud/mcp
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
    "nanobanana": {
      "type": "http",
      "url": "https://nanobanana.mcp.acedata.cloud/mcp",
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
    "nanobanana": {
      "type": "stdio",
      "command": "uvx",
      "args": ["mcp-nanobanana-pro"],
      "env": { "ACEDATACLOUD_API_TOKEN": "${input:acedatacloud_api_token}" }
    }
  }
}
```

`uvx` will download and run the latest [`mcp-nanobanana-pro`](https://pypi.org/project/mcp-nanobanana-pro/) on demand.

---

## Links

- **Hosted endpoint:** https://nanobanana.mcp.acedata.cloud/mcp
- **PyPI package:** [`mcp-nanobanana-pro`](https://pypi.org/project/mcp-nanobanana-pro/)
- **Source repository:** https://github.com/AceDataCloud/NanoBananaMCP
- **Ace Data Cloud platform:** https://platform.acedata.cloud?utm_source=vscode_marketplace&utm_medium=referral&utm_campaign=evergreen&utm_content=nanobanana_mcp_vscode_platform
- **MCP documentation:** https://platform.acedata.cloud/documents/nano-banana-mcp?utm_source=vscode_marketplace&utm_medium=referral&utm_campaign=evergreen&utm_content=nanobanana_mcp_vscode_quick_start

## License

MIT — see [LICENSE](LICENSE).
