# OpenAIMCP

<!-- mcp-name: io.github.AceDataCloud/mcp-openai -->

[![PyPI version](https://img.shields.io/pypi/v/mcp-openai.svg)](https://pypi.org/project/mcp-openai/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![MCP](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io)

A [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server for OpenAI API through the [AceDataCloud API](https://platform.acedata.cloud).

## Features

- **Chat Completions** - Full OpenAI chat completions API support
- **Embeddings** - Text embedding generation
- **Image Generation** - Generate images with DALL-E and GPT-Image models
- **Responses API** - OpenAI responses API support
- **Image Editing** - Edit existing images with AI

## Tool Reference

| Tool | Description |
|------|-------------|
| `openai_chat_completion` | Perform chat completion using OpenAI API |
| `openai_embeddings` | Create text embeddings |
| `openai_image_generate` | Generate images from text prompts |
| `openai_responses` | Use the OpenAI responses API |
| `openai_image_edit` | Edit images using OpenAI API |
| `openai_list_models` | List all available models by category |

## Quick Start

### 1. Get Your API Token

1. Sign up at [AceDataCloud Platform](https://platform.acedata.cloud)
2. Get your API token

### 2. Install and Run

```bash
# Install from PyPI
pip install mcp-openai
# or
uvx mcp-openai

# Set your API token
export ACEDATACLOUD_API_TOKEN="your_token_here"

# Run (stdio mode for Claude Desktop / local clients)
mcp-openai

# Run (HTTP mode for remote access)
mcp-openai --transport http --port 8000
```

### 3. Configure Claude Desktop

```json
{
  "mcpServers": {
    "openai": {
      "command": "uvx",
      "args": ["mcp-openai"],
      "env": {
        "ACEDATACLOUD_API_TOKEN": "your_token_here"
      }
    }
  }
}
```

## Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `ACEDATACLOUD_API_TOKEN` | API token from AceDataCloud | **Required** |
| `ACEDATACLOUD_API_BASE_URL` | API base URL | `https://api.acedata.cloud` |
| `OPENAI_REQUEST_TIMEOUT` | Request timeout in seconds | `30` |
| `LOG_LEVEL` | Logging level | `INFO` |

## Development

```bash
pip install -e ".[dev,test]"
pytest --cov=core --cov=tools
ruff check .
```

## License

MIT License

---

Made with love by [AceDataCloud](https://platform.acedata.cloud)
