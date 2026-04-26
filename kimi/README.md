# KimiMCP

A [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server for Kimi API access using [AceDataCloud](https://platform.acedata.cloud).

Interact with Kimi models for chat completions and more — directly from Claude, VS Code, or any MCP-compatible client.

## Features

- **Chat Completions** — Access Kimi models including kimi-k2-thinking-turbo, kimi-k2.5, kimi-k2-thinking, and more

## Quick Start

### Prerequisites

Get an API token from [AceDataCloud](https://platform.acedata.cloud).

### Installation

```bash
pip install mcp-kimi
```

### Configuration

Set your API token:

```bash
export ACEDATACLOUD_API_TOKEN=your_api_token_here
```

### Run

```bash
mcp-kimi
```

## Available Tools

| Tool | Description |
|------|-------------|
| `kimi_chat_completion` | Create chat completions using Kimi models |
| `kimi_list_models` | List available Kimi models |
| `kimi_get_usage_guide` | Get usage guide and examples |

## Supported Models

| Model | Notes |
|-------|-------|
| `kimi-k2-thinking-turbo` | **(default)** |
| `kimi-k2.5` |  |
| `kimi-k2-thinking` |  |
| `kimi-k2-instruct-0905` |  |
| `kimi-k2-0905-preview` |  |
| `kimi-k2-turbo-preview` |  |
| `kimi-k2-0711-preview` |  |

## MCP Configuration

### Claude Desktop

```json
{
  "mcpServers": {
    "kimi": {
      "command": "uvx",
      "args": ["mcp-kimi"],
      "env": {
        "ACEDATACLOUD_API_TOKEN": "your_api_token_here"
      }
    }
  }
}
```

## License

MIT License - see [LICENSE](LICENSE) for details.
