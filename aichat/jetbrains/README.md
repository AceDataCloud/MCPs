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
3. Enter your [Ace Data Cloud](https://platform.acedata.cloud) API token
4. Click **Copy Config** (STDIO or HTTP)
5. Paste into **Settings → Tools → AI Assistant → Model Context Protocol (MCP)**

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

- [Ace Data Cloud Platform](https://platform.acedata.cloud)
- [API Documentation](https://docs.acedata.cloud)
- [PyPI Package](https://pypi.org/project/mcp-aichat/)
- [Source Code](https://github.com/AceDataCloud/AiChatMCP)

## License

MIT
