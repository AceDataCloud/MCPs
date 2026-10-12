# AiChat MCP — JetBrains Plugin

Unified LLM gateway via Ace Data Cloud via [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) for JetBrains IDEs.

<!-- Plugin description -->
This plugin helps you set up the AiChat MCP server with JetBrains AI Assistant.
Once configured, AI Assistant can chat with 50+ LLM models — GPT, Claude, Gemini, Grok, DeepSeek and more — through a single endpoint.

**4 AI Tools** — Unified LLM gateway via Ace Data Cloud.
<!-- Plugin description end -->

## Quick Start

1. Install this plugin from the [JetBrains Marketplace](https://plugins.jetbrains.com/plugin/com.acedatacloud.mcp.aichat)
2. Open **Settings → Tools → AiChat MCP**
3. Enter your [Ace Data Cloud](https://platform.acedata.cloud?utm_source=jetbrains_marketplace&utm_medium=referral&utm_campaign=evergreen&utm_content=aichat_mcp_jetbrains_platform) API token
4. Click **Copy Config** (STDIO or HTTP)
5. Paste into **Settings → Tools → AI Assistant → Model Context Protocol (MCP)**

### Get your API key

<!-- BEGIN TOKEN ONBOARDING -->
1. Open [Ace Data Cloud → Applications](https://platform.acedata.cloud/console/applications?utm_source=jetbrains_marketplace&utm_medium=referral&utm_campaign=evergreen&utm_content=aichat_mcp_jetbrains_api_key). Sign in, or register an account first.
2. Find **General application**. If it has not been created, choose **Initialize General Application**. A general key can use the services available to your account; a dedicated application's key is limited to its service. Check the required service/model access and [current pricing](https://platform.acedata.cloud/models?utm_source=jetbrains_marketplace&utm_medium=referral&utm_campaign=evergreen&utm_content=aichat_mcp_jetbrains_models).
3. Copy the **API Key** from the application card, or open **Keys / Manage Keys → Create** to create a separate key for this integration. Give it a recognizable name so you can revoke or rotate it independently.
4. When creating a key, review **Expiration Time**, **Set Usage Limitation**, and **Allowed APIs**. Enable only the restrictions you need, allow the operations you will call, then click **Create** and copy the token from the key list. Task lookup does not grant permission to submit a generation. Confirm the application's balance can cover your first request; any trial allowance is whatever your account currently displays.
5. Copy only the token value, without quotation marks, spaces, or `Bearer `. An API Key / API Token field expects this raw value; only a manually configured HTTP `Authorization` header needs the `Bearer ` prefix. A `platform-...` account-management token cannot replace a generation API key.

![Copy an application API key or open Manage Keys](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/get-api-key-en.png)

![Create a separately named key with optional restrictions](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/create-api-key-en.png)

Save the key in the client's credential store or the environment variable shown below. Never put it in a prompt, shared workflow, screenshot, or Git commit. If authentication fails, check the full copied value, application/service access, expiration, usage limit, and balance before creating another key.
<!-- END TOKEN ONBOARDING -->

### HTTP Mode (Remote, recommended)

Connects to the hosted MCP server at `aichat.mcp.acedata.cloud`. No local install needed.

```json
{
  "mcpServers": {
    "aichat": {
      "url": "https://aichat.mcp.acedata.cloud/mcp",
      "headers": {
        "Authorization": "Bearer your-token"
      }
    }
  }
}
```

### STDIO Mode (Local)

Runs the MCP server locally. Requires [uv](https://github.com/astral-sh/uv) installed.

```json
{
  "mcpServers": {
    "aichat": {
      "command": "uvx",
      "args": ["mcp-aichat"],
      "env": {
        "ACEDATACLOUD_API_TOKEN": "your-token"
      }
    }
  }
}
```

## Tool Reference

| Tool | Description |
| --- | --- |
| `aichat_create_conversation` | Create an AI conversation using the AiChat API. |
| `aichat_create_conversation_v2` | Create / manage conversations via the AiChat v2 endpoint. |
| `aichat_list_models` | List all available AI models for the AiChat API. |
| `aichat_get_usage_guide` | Get a comprehensive guide for using the AiChat tools. |

## Links

- [Ace Data Cloud Platform](https://platform.acedata.cloud?utm_source=jetbrains_marketplace&utm_medium=referral&utm_campaign=evergreen&utm_content=aichat_mcp_jetbrains_platform)
- [Documentation](https://platform.acedata.cloud/documents/aichat?utm_source=jetbrains_marketplace&utm_medium=referral&utm_campaign=evergreen&utm_content=aichat_mcp_jetbrains_quick_start)
- [PyPI Package](https://pypi.org/project/mcp-aichat/)
- [Source Code](https://github.com/AceDataCloud/AiChatMCP)

## License

MIT
