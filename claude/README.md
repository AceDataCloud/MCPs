# ClaudeMCP

A [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server for Claude API access using [AceDataCloud](https://platform.acedata.cloud).

Interact with Claude models for chat completions and more — directly from Claude, VS Code, or any MCP-compatible client.

## Features

- **Chat Completions** — Access Claude models including claude-sonnet-4-6, claude-opus-4-7, claude-opus-4-6, and more

## Quick Start

### Prerequisites

Get an API token from [AceDataCloud](https://platform.acedata.cloud).

### Installation

```bash
pip install mcp-claude
```

### Configuration

Set your API token:

```bash
export ACEDATACLOUD_API_TOKEN=your_api_token_here
```

### Run

```bash
mcp-claude
```

## Available Tools

| Tool | Description |
|------|-------------|
| `claude_chat_completion` | Create chat completions using Claude models |
| `claude_create_message` | Create a message using the Anthropic native API |
| `claude_list_models` | List available Claude models |
| `claude_get_usage_guide` | Get usage guide and examples |

## Supported Models

| Model | Notes |
|-------|-------|
| `claude-sonnet-4-6` |  |
| `claude-opus-4-7` |  |
| `claude-opus-4-6` |  |
| `claude-opus-4-5-20251101` |  |
| `claude-haiku-4-5-20251001` |  |
| `claude-sonnet-4-5-20250929` |  |
| `claude-opus-4-1-20250805` |  |
| `claude-sonnet-4-20250514` | **(default)** |
| `claude-opus-4-20250514` |  |
| `claude-3-7-sonnet-20250219` |  |
| `claude-3-5-sonnet-20241022` |  |
| `claude-3-5-haiku-20241022` |  |
| `claude-3-5-sonnet-20240620` |  |
| `claude-3-haiku-20240307` |  |
| `claude-3-sonnet-20240229` |  |
| `claude-3-opus-20240229` |  |

## MCP Configuration

### Claude Desktop

```json
{
  "mcpServers": {
    "claude": {
      "command": "uvx",
      "args": ["mcp-claude"],
      "env": {
        "ACEDATACLOUD_API_TOKEN": "your_api_token_here"
      }
    }
  }
}
```

### Claude Desktop (Alternative: Anthropic Native API)

```json
{
  "mcpServers": {
    "claude": {
      "command": "uvx",
      "args": ["mcp-claude"],
      "env": {
        "ACEDATACLOUD_API_TOKEN": "your_api_token_here"
      }
    }
  }
}
```

## License

MIT License - see [LICENSE](LICENSE) for details.
