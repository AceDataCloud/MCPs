# AiChat MCP

Unified OpenAI-compatible LLM gateway — chat with GPT, Claude, Gemini, Grok, DeepSeek, Kimi and more via a single endpoint.

[![VS Code Marketplace](https://img.shields.io/badge/VS%20Code-Marketplace-blue?logo=visualstudiocode&logoColor=white)](https://marketplace.visualstudio.com/items?itemName=acedatacloud.mcp-aichat) [![PyPI](https://img.shields.io/pypi/v/mcp-aichat.svg?label=PyPI)](https://pypi.org/project/mcp-aichat/) [![Hosted MCP](https://img.shields.io/badge/hosted-mcp-blue)](https://aichat.mcp.acedata.cloud/mcp)

Connect VS Code's AI agents to the **Unified LLM gateway via Ace Data Cloud** service. Once configured, AI Assistant can chat with 50+ LLM models — GPT, Claude, Gemini, Grok, DeepSeek and more — through a single endpoint.

This extension registers the **aichat** MCP server with VS Code so GitHub
Copilot and any other agent that speaks the [Model Context Protocol](https://modelcontextprotocol.io/)
can call it directly from chat.

---

## Quick Start

1. **Install this extension.** VS Code registers the `aichat` MCP server automatically.
2. **Get an API token** from [Ace Data Cloud](https://platform.acedata.cloud?utm_source=vscode_marketplace&utm_medium=referral&utm_campaign=evergreen&utm_content=aichat_mcp_vscode_platform) → *API Keys*. New accounts include free trial credit.
3. **Open Copilot Chat** in agent mode and call a tool — VS Code will prompt for the token the first time and store it securely.

> The default config talks to the **hosted streamable-HTTP endpoint** at
> `https://aichat.mcp.acedata.cloud/mcp` — no Python, no `uvx`, no local install needed.

### Get your API key

<!-- BEGIN TOKEN ONBOARDING -->
1. Open [Ace Data Cloud → Applications](https://platform.acedata.cloud/console/applications?utm_source=vscode_marketplace&utm_medium=referral&utm_campaign=evergreen&utm_content=aichat_mcp_vscode_api_key). Sign in, or register an account first.
2. Find **General application**. If it has not been created, choose **Initialize General Application**. A general key can use the services available to your account; a dedicated application's key is limited to its service. Check the required service/model access and [current pricing](https://platform.acedata.cloud/models?utm_source=vscode_marketplace&utm_medium=referral&utm_campaign=evergreen&utm_content=aichat_mcp_vscode_models).
3. Copy the **API Key** from the application card, or open **Keys / Manage Keys → Create** to create a separate key for this integration. Give it a recognizable name so you can revoke or rotate it independently.
4. When creating a key, review **Expiration Time**, **Set Usage Limitation**, and **Allowed APIs**. Enable only the restrictions you need, allow the operations you will call, then click **Create** and copy the token from the key list. Task lookup does not grant permission to submit a generation. Confirm the application's balance can cover your first request; any trial allowance is whatever your account currently displays.
5. Copy only the token value, without quotation marks, spaces, or `Bearer `. An API Key / API Token field expects this raw value; only a manually configured HTTP `Authorization` header needs the `Bearer ` prefix. A `platform-...` account-management token cannot replace a generation API key.

![Copy an application API key or open Manage Keys](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/get-api-key-en.png)

![Create a separately named key with optional restrictions](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/create-api-key-en.png)

Save the key in the client's credential store or the environment variable shown below. Never put it in a prompt, shared workflow, screenshot, or Git commit. If authentication fails, check the full copied value, application/service access, expiration, usage limit, and balance before creating another key.
<!-- END TOKEN ONBOARDING -->

## VS Code Setup Guide

For the full VS Code walkthrough, see [All Ace Data Cloud MCP servers in VS Code](https://platform.acedata.cloud/documents/promotion_article_mcp_all_vscode?utm_source=vscode_marketplace&utm_medium=referral&utm_campaign=evergreen&utm_content=aichat_mcp_vscode_documents_promotion_article_mcp_all_vscode). It covers token setup, project-level and user-level `mcp.json`, Copilot Agent Mode, and using one Ace Data Cloud token across hosted MCP servers.

---

## Tool Reference

**4 tools** available via this server.

| Tool | Description |
| --- | --- |
| `aichat_create_conversation` | Create an AI conversation using the AiChat API. |
| `aichat_create_conversation_v2` | Create / manage conversations via the AiChat v2 endpoint. |
| `aichat_list_models` | List all available AI models for the AiChat API. |
| `aichat_get_usage_guide` | Get a comprehensive guide for using the AiChat tools. |

---

## Configuration

This extension contributes the following entry to your VS Code MCP config:

```jsonc
{
  "servers": {
    "aichat": {
      "type": "http",
      "url": "https://aichat.mcp.acedata.cloud/mcp",
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
    "aichat": {
      "type": "stdio",
      "command": "uvx",
      "args": ["mcp-aichat"],
      "env": { "ACEDATACLOUD_API_TOKEN": "${input:acedatacloud_api_token}" }
    }
  }
}
```

`uvx` will download and run the latest [`mcp-aichat`](https://pypi.org/project/mcp-aichat/) on demand.

### Alternative: OAuth via Dynamic Client Registration

The hosted endpoint also accepts OAuth 2.1 with [DCR](https://datatracker.ietf.org/doc/html/rfc7591).
Drop the `headers` and `inputs` blocks and VS Code will run the auth flow on
first use (redirect URL `http://127.0.0.1:33418` or `https://vscode.dev/redirect`).

---

## Links

- **Hosted endpoint:** https://aichat.mcp.acedata.cloud/mcp
- **PyPI package:** [`mcp-aichat`](https://pypi.org/project/mcp-aichat/)
- **Source repository:** https://github.com/AceDataCloud/AiChatMCP
- **Ace Data Cloud platform:** https://platform.acedata.cloud?utm_source=vscode_marketplace&utm_medium=referral&utm_campaign=evergreen&utm_content=aichat_mcp_vscode_platform
- **MCP documentation:** https://platform.acedata.cloud/documents/aichat?utm_source=vscode_marketplace&utm_medium=referral&utm_campaign=evergreen&utm_content=aichat_mcp_vscode_quick_start

## License

MIT — see [LICENSE](LICENSE).
