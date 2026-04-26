# GrokMCP

A [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server for Grok API access using [AceDataCloud](https://platform.acedata.cloud).

Interact with Grok models for chat completions and more — directly from Claude, VS Code, or any MCP-compatible client.

## Features

- **Chat Completions** — Access Grok models including grok-4, grok-4-1-fast, grok-4-1-fast-non-reasoning, and more

## Quick Start

### Prerequisites

Get an API token from [AceDataCloud](https://platform.acedata.cloud).

### Installation

```bash
pip install mcp-grok
```

### Configuration

Set your API token:

```bash
export ACEDATACLOUD_API_TOKEN=your_api_token_here
```

### Run

```bash
mcp-grok
```

## Available Tools

| Tool | Description |
|------|-------------|
| `grok_chat_completion` | Create chat completions using Grok models |
| `grok_list_models` | List available Grok models |
| `grok_get_usage_guide` | Get usage guide and examples |

## Supported Models

| Model | Notes |
|-------|-------|
| `grok-4` |  |
| `grok-4-1-fast` |  |
| `grok-4-1-fast-non-reasoning` |  |
| `grok-3` | **(default)** |
| `grok-3-mini` |  |
| `grok-2-vision` |  |

## MCP Configuration

### Claude Desktop

```json
{
  "mcpServers": {
    "grok": {
      "command": "uvx",
      "args": ["mcp-grok"],
      "env": {
        "ACEDATACLOUD_API_TOKEN": "your_api_token_here"
      }
    }
  }
}
```

## License

MIT License - see [LICENSE](LICENSE) for details.
