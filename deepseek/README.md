# DeepSeekMCP

A [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server for DeepSeek API access using [AceDataCloud](https://platform.acedata.cloud).

Interact with DeepSeek models for chat completions and more — directly from Claude, VS Code, or any MCP-compatible client.

## Features

- **Chat Completions** — Access DeepSeek models including deepseek-r1, deepseek-r1-0528, deepseek-v3, and more

## Quick Start

### Prerequisites

Get an API token from [AceDataCloud](https://platform.acedata.cloud).

### Installation

```bash
pip install mcp-deepseek
```

### Configuration

Set your API token:

```bash
export ACEDATACLOUD_API_TOKEN=your_api_token_here
```

### Run

```bash
mcp-deepseek
```

## Available Tools

| Tool | Description |
|------|-------------|
| `deepseek_chat_completion` | Create chat completions using DeepSeek models |
| `deepseek_list_models` | List available DeepSeek models |
| `deepseek_get_usage_guide` | Get usage guide and examples |

## Supported Models

| Model | Notes |
|-------|-------|
| `deepseek-r1` |  |
| `deepseek-r1-0528` |  |
| `deepseek-v3` | **(default)** |
| `deepseek-v3-250324` |  |
| `deepseek-v3.2-exp` |  |

## MCP Configuration

### Claude Desktop

```json
{
  "mcpServers": {
    "deepseek": {
      "command": "uvx",
      "args": ["mcp-deepseek"],
      "env": {
        "ACEDATACLOUD_API_TOKEN": "your_api_token_here"
      }
    }
  }
}
```

## License

MIT License - see [LICENSE](LICENSE) for details.
