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
3. Enter your [Ace Data Cloud](https://platform.acedata.cloud?utm_source=jetbrains_marketplace&utm_medium=referral&utm_campaign=evergreen) API token
4. Click **Copy Config** (STDIO or HTTP)
5. Paste into **Settings → Tools → AI Assistant → Model Context Protocol (MCP)**

### Get your API key

<!-- BEGIN TOKEN ONBOARDING -->
Sign in to [Applications](https://platform.acedata.cloud/console/applications?utm_source=jetbrains_marketplace&utm_medium=referral&utm_campaign=evergreen) and open **General Application**. If it is missing, select **Initialize General Application**. Click the copy button marked **1** beside **API KEY**.

![Copy the General Application API key with the button marked 1](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/get-api-key-en.png)

Store the raw key in your client’s credential store or in the environment variable shown below. Add `Bearer ` only when setting an HTTP `Authorization` header yourself. Check access to the required operations, the current pricing, and the application balance. To use a separate key for this integration, open **Manage Keys** to set **Allowed APIs**, expiration, and usage limit.
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

- [Ace Data Cloud Platform](https://platform.acedata.cloud?utm_source=jetbrains_marketplace&utm_medium=referral&utm_campaign=evergreen)
- [Documentation](https://platform.acedata.cloud/documents/aichat?utm_source=jetbrains_marketplace&utm_medium=referral&utm_campaign=evergreen)
- [PyPI Package](https://pypi.org/project/mcp-aichat/)
- [Source Code](https://github.com/AceDataCloud/AiChatMCP)

## License

MIT
