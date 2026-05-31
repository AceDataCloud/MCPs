# OpenAI MCP — JetBrains Plugin

OpenAI models via Ace Data Cloud via [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) for JetBrains IDEs.

<!-- Plugin description -->
This plugin helps you set up the OpenAI MCP server with JetBrains AI Assistant.
Once configured, AI Assistant can run OpenAI chat completions, generate embeddings, create or edit images, and orchestrate the Responses API — all routed through Ace Data Cloud.

**11 AI Tools** — OpenAI models via Ace Data Cloud.
<!-- Plugin description end -->

## Quick Start

1. Install this plugin from the [JetBrains Marketplace](https://plugins.jetbrains.com/plugin/com.acedatacloud.mcp.openai)
2. Open **Settings → Tools → OpenAI MCP**
3. Enter your [Ace Data Cloud](https://platform.acedata.cloud) API token
4. Click **Copy Config** (STDIO or HTTP)
5. Paste into **Settings → Tools → AI Assistant → Model Context Protocol (MCP)**

### HTTP Mode (Remote, recommended)

Connects to the hosted MCP server at `openai.mcp.acedata.cloud`. No local install needed.

```json
{
  "mcpServers": {
    "openai": {
      "url": "https://openai.mcp.acedata.cloud/mcp",
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
    "openai": {
      "command": "uvx",
      "args": ["mcp-openai"],
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
| `openai_chat_completion` | Create a chat completion using OpenAI models via AceDataCloud. |
| `openai_create_embedding` | Create text embeddings using OpenAI embedding models via AceDataCloud. |
| `openai_generate_image` | Generate images using OpenAI image models via AceDataCloud. |
| `openai_edit_image` | Edit or modify existing images using OpenAI image models via AceDataCloud. |
| `openai_create_response` | Create a response using the OpenAI Responses API via AceDataCloud. |
| `openai_get_task` | Retrieve a single async image task by its task ID or custom trace ID. |
| `openai_list_tasks` | List async image tasks using batch query filters. |
| `openai_list_chat_models` | List all available chat completion models. |
| `openai_list_image_models` | List all available image generation and editing models. |
| `openai_list_embedding_models` | List all available text embedding models. |
| `openai_get_usage_guide` | Get a comprehensive guide for using the OpenAI tools. |

## Links

- [Ace Data Cloud Platform](https://platform.acedata.cloud)
- [API Documentation](https://docs.acedata.cloud)
- [PyPI Package](https://pypi.org/project/mcp-openai/)
- [Source Code](https://github.com/AceDataCloud/OpenAIMCP)

## License

MIT
