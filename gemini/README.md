# GeminiMCP

A [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server for Gemini API access using [AceDataCloud](https://platform.acedata.cloud).

Interact with Gemini models for chat completions and more — directly from Claude, VS Code, or any MCP-compatible client.

## Features

- **Chat Completions** — Access Gemini models including gemini-3.1-pro, gemini-3.0-pro, gemini-3-flash-preview, and more

## Quick Start

### Prerequisites

Get an API token from [AceDataCloud](https://platform.acedata.cloud).

### Installation

```bash
pip install mcp-gemini
```

### Configuration

Set your API token:

```bash
export ACEDATACLOUD_API_TOKEN=your_api_token_here
```

### Run

```bash
mcp-gemini
```

## Available Tools

| Tool | Description |
|------|-------------|
| `gemini_chat_completion` | Create chat completions using Gemini models |
| `gemini_generate_content` | Generate content using the Google native API |
| `gemini_list_models` | List available Gemini models |
| `gemini_get_usage_guide` | Get usage guide and examples |

## Supported Models

| Model | Notes |
|-------|-------|
| `gemini-3.1-pro` |  |
| `gemini-3.0-pro` |  |
| `gemini-3-flash-preview` |  |
| `gemini-2.5-pro` | **(default)** |
| `gemini-2.5-flash` |  |
| `gemini-2.0-flash` |  |

## MCP Configuration

### Claude Desktop

```json
{
  "mcpServers": {
    "gemini": {
      "command": "uvx",
      "args": ["mcp-gemini"],
      "env": {
        "ACEDATACLOUD_API_TOKEN": "your_api_token_here"
      }
    }
  }
}
```

## License

MIT License - see [LICENSE](LICENSE) for details.
