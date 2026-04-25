# AIChatMCP

<!-- mcp-name: io.github.AceDataCloud/mcp-aichat -->

[![PyPI version](https://img.shields.io/pypi/v/mcp-aichat.svg)](https://pypi.org/project/mcp-aichat/)
[![PyPI downloads](https://img.shields.io/pypi/dm/mcp-aichat.svg)](https://pypi.org/project/mcp-aichat/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![MCP](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io)

A [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server for AI dialogue using the [AIChat API](https://platform.acedata.cloud) through the [AceDataCloud API](https://platform.acedata.cloud).

Access 70+ AI models including GPT-5, GPT-4, o-series, DeepSeek, Grok, and GLM directly from Claude, VS Code, or any MCP-compatible client.

## Features

- **Multi-Model Support** - Access GPT-5, GPT-4, o-series, DeepSeek, Grok, GLM, and more
- **Stateful Conversations** - Multi-turn dialogue with conversation memory
- **Reference Support** - Provide URLs as context for model responses
- **Preset Configurations** - Use preset model configurations
- **Model Listing** - Browse all available models with descriptions

## Tool Reference

| Tool | Description |
|------|-------------|
| `aichat_conversation` | Send a question to an AI model and get an answer. |
| `aichat_list_models` | List all available AI chat models. |
| `aichat_get_usage_guide` | Get a comprehensive guide for using the AIChat tools. |

## Quick Start

### 1. Get Your API Token

1. Sign up at [AceDataCloud Platform](https://platform.acedata.cloud)
2. Go to the API documentation page
3. Click **"Acquire"** to get your API token
4. Copy the token for use below

### 2. Install and Configure

```bash
# Install with pip
pip install mcp-aichat

# Or use with uvx (no installation needed)
uvx mcp-aichat
```

### 3. Add to Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "aichat": {
      "command": "uvx",
      "args": ["mcp-aichat"],
      "env": {
        "ACEDATACLOUD_API_TOKEN": "your_token_here"
      }
    }
  }
}
```

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `ACEDATACLOUD_API_TOKEN` | Yes | - | API token from AceDataCloud |
| `ACEDATACLOUD_API_BASE_URL` | No | `https://api.acedata.cloud` | API base URL |
| `AICHAT_REQUEST_TIMEOUT` | No | `60` | Request timeout in seconds |
| `MCP_SERVER_NAME` | No | `aichat` | MCP server name |
| `LOG_LEVEL` | No | `INFO` | Logging level |

## Available Models

The AIChat API supports 70+ models including:

- **GPT-5 Series**: gpt-5.5, gpt-5.5-pro, gpt-5.4, gpt-5.2, gpt-5.1, gpt-5, gpt-5-mini, gpt-5-nano
- **GPT-4 Series**: gpt-4.1, gpt-4o, gpt-4o-mini, gpt-4, gpt-4-turbo, and dated variants
- **o-series**: o1, o1-mini, o1-pro, o3, o3-mini, o3-pro, o4-mini, and variants
- **DeepSeek**: deepseek-r1, deepseek-r1-0528, deepseek-v3, deepseek-v3-250324
- **Grok**: grok-3
- **GLM**: glm-5.1, glm-4.7, glm-4.6, glm-4.5-air, glm-3-turbo

Use `aichat_list_models` to see the full list.

## License

MIT License - see [LICENSE](LICENSE) file for details.
