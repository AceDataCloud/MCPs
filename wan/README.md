# WanMCP

<!-- mcp-name: io.github.AceDataCloud/mcp-wan -->

[![PyPI version](https://img.shields.io/pypi/v/mcp-wan.svg)](https://pypi.org/project/mcp-wan/)
[![PyPI downloads](https://img.shields.io/pypi/dm/mcp-wan.svg)](https://pypi.org/project/mcp-wan/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![MCP](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io)

A [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server for AI video generation using [Wan](https://wanx.aliyun.com/) through the [AceDataCloud API](https://platform.acedata.cloud).

Generate AI videos from text or images directly from Claude, VS Code, or any MCP-compatible client.

## Features

- **Text to Video** - Create AI-generated videos from text prompts
- **Image to Video** - Generate videos using reference images
- **Multiple Models** - Support for 4 Wan models (wan2.6-t2v, wan2.6-i2v, wan2.6-r2v, wan2.6-i2v-flash)
- **Multiple Resolutions** - 480P (draft), 720P (default), 1080P (high quality)
- **Audio Support** - Generate videos with sound
- **Character Transfer** - Extract character appearance via reference videos (wan2.6-r2v)
- **Task Tracking** - Monitor generation progress and retrieve results

## Tool Reference

| Tool | Description |
|------|-------------|
| `wan_generate_video` | Generate AI video from a text prompt using Wan. |
| `wan_generate_video_from_image` | Generate AI video using a reference image as the starting frame. |
| `wan_get_task` | Query the status and result of a video generation task. |
| `wan_get_tasks_batch` | Query multiple video generation tasks at once. |
| `wan_list_models` | List all available Wan models for video generation. |
| `wan_list_resolutions` | List all available resolution options. |
| `wan_list_actions` | List all available Wan API actions and corresponding tools. |

## Quick Start

### 1. Get Your API Token

1. Sign up at [AceDataCloud Platform](https://platform.acedata.cloud)
2. Go to the API documentation page
3. Click **"Acquire"** to get your API token
4. Copy the token for use below

### 2. Use the Hosted Server (Recommended)

AceDataCloud hosts a managed MCP server — **no local installation required**.

**Endpoint:** `https://wan.mcp.acedata.cloud/mcp`

All requests require a Bearer token. Use the API token from Step 1.

#### Claude.ai

Connect directly on [Claude.ai](https://claude.ai) with OAuth — **no API token needed**:

1. Go to Claude.ai **Settings → Integrations → Add More**
2. Enter the server URL: `https://wan.mcp.acedata.cloud/mcp`
3. Complete the OAuth login flow
4. Start using the tools in your conversation

#### Claude Desktop

Add to your config (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "wan": {
      "type": "streamable-http",
      "url": "https://wan.mcp.acedata.cloud/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_API_TOKEN"
      }
    }
  }
}
```

#### Cursor / Windsurf

Add to your MCP config (`.cursor/mcp.json` or `.windsurf/mcp.json`):

```json
{
  "mcpServers": {
    "wan": {
      "type": "streamable-http",
      "url": "https://wan.mcp.acedata.cloud/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_API_TOKEN"
      }
    }
  }
}
```

#### VS Code (Copilot)

Add to your VS Code MCP config (`.vscode/mcp.json`):

```json
{
  "servers": {
    "wan": {
      "type": "streamable-http",
      "url": "https://wan.mcp.acedata.cloud/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_API_TOKEN"
      }
    }
  }
}
```

Or install the [Ace Data Cloud MCP extension](https://marketplace.visualstudio.com/items?itemName=acedatacloud.acedatacloud-mcp) for VS Code, which bundles all MCP servers with one-click setup.

#### JetBrains IDEs

1. Go to **Settings → Tools → AI Assistant → Model Context Protocol (MCP)**
2. Click **Add** → **HTTP**
3. Paste:

```json
{
  "mcpServers": {
    "wan": {
      "url": "https://wan.mcp.acedata.cloud/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_API_TOKEN"
      }
    }
  }
}
```

#### Claude Code

Claude Code supports MCP servers natively:

```bash
claude mcp add wan --transport http https://wan.mcp.acedata.cloud/mcp \
  -h "Authorization: Bearer YOUR_API_TOKEN"
```

Or add to your project's `.mcp.json`:

```json
{
  "mcpServers": {
    "wan": {
      "type": "streamable-http",
      "url": "https://wan.mcp.acedata.cloud/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_API_TOKEN"
      }
    }
  }
}
```

#### Cline

Add to Cline's MCP settings (`.cline/mcp_settings.json`):

```json
{
  "mcpServers": {
    "wan": {
      "type": "streamable-http",
      "url": "https://wan.mcp.acedata.cloud/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_API_TOKEN"
      }
    }
  }
}
```

#### Amazon Q Developer

Add to your MCP configuration:

```json
{
  "mcpServers": {
    "wan": {
      "type": "streamable-http",
      "url": "https://wan.mcp.acedata.cloud/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_API_TOKEN"
      }
    }
  }
}
```

#### Roo Code

Add to Roo Code MCP settings:

```json
{
  "mcpServers": {
    "wan": {
      "type": "streamable-http",
      "url": "https://wan.mcp.acedata.cloud/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_API_TOKEN"
      }
    }
  }
}
```

#### Continue.dev

Add to `.continue/config.yaml`:

```yaml
mcpServers:
  - name: wan
    type: streamable-http
    url: https://wan.mcp.acedata.cloud/mcp
    headers:
      Authorization: "Bearer YOUR_API_TOKEN"
```

#### Zed

Add to Zed's settings (`~/.config/zed/settings.json`):

```json
{
  "language_models": {
    "mcp_servers": {
      "wan": {
        "url": "https://wan.mcp.acedata.cloud/mcp",
        "headers": {
          "Authorization": "Bearer YOUR_API_TOKEN"
        }
      }
    }
  }
}
```

#### cURL Test

```bash
# Health check (no auth required)
curl https://wan.mcp.acedata.cloud/health

# MCP initialize
curl -X POST https://wan.mcp.acedata.cloud/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}'
```

### 3. Or Run Locally (Alternative)

If you prefer to run the server on your own machine:

```bash
# Install from PyPI
pip install mcp-wan
# or
uvx mcp-wan

# Set your API token
export ACEDATACLOUD_API_TOKEN="your_token_here"

# Run (stdio mode for Claude Desktop / local clients)
mcp-wan

# Run (HTTP mode for remote access)
mcp-wan --transport http --port 8000
```

#### Claude Desktop (Local)

```json
{
  "mcpServers": {
    "wan": {
      "command": "uvx",
      "args": ["mcp-wan"],
      "env": {
        "ACEDATACLOUD_API_TOKEN": "your_token_here"
      }
    }
  }
}
```

#### Docker (Self-Hosting)

```bash
docker pull ghcr.io/acedatacloud/mcp-wan:latest
docker run -p 8000:8000 ghcr.io/acedatacloud/mcp-wan:latest
```

Clients connect with their own Bearer token — the server extracts the token from each request's `Authorization` header.

## Available Models

| Model              | Description               | Use Case                                |
| ------------------ | ------------------------- | --------------------------------------- |
| `wan2.6-t2v`       | Text to video             | Generate video from text prompts        |
| `wan2.6-i2v`       | Image to video            | Standard image-to-video generation      |
| `wan2.6-r2v`       | Reference video-to-video  | Character extraction and transfer       |
| `wan2.6-i2v-flash` | Fast image to video       | Quick preview, lower quality            |

## Configuration

### Environment Variables

| Variable                    | Description                 | Default                     |
| --------------------------- | --------------------------- | --------------------------- |
| `ACEDATACLOUD_API_TOKEN`    | API token from AceDataCloud | **Required**                |
| `ACEDATACLOUD_API_BASE_URL` | API base URL                | `https://api.acedata.cloud` |
| `WAN_DEFAULT_MODEL`         | Default video model         | `wan2.6-t2v`                |
| `WAN_DEFAULT_RESOLUTION`    | Default resolution          | `720P`                      |
| `WAN_REQUEST_TIMEOUT`       | Request timeout in seconds  | `1800`                      |
| `LOG_LEVEL`                 | Logging level               | `INFO`                      |

### Command Line Options

```bash
mcp-wan --help

Options:
  --version          Show version
  --transport        Transport mode: stdio (default) or http
  --port             Port for HTTP transport (default: 8000)
```

## Development

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/AceDataCloud/WanMCP.git
cd WanMCP

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # or `.venv\Scripts\activate` on Windows

# Install with dev dependencies
pip install -e ".[dev,test]"
```

### Run Tests

```bash
# Run unit tests
pytest

# Run with coverage
pytest --cov=core --cov=tools

# Run integration tests (requires API token)
pytest tests/test_integration.py -m integration
```

### Code Quality

```bash
# Format code
ruff format .

# Lint code
ruff check .

# Type check
mypy core tools
```

### Build & Publish

```bash
# Install build dependencies
pip install -e ".[release]"

# Build package
python -m build

# Upload to PyPI
twine upload dist/*
```

## Project Structure

```
WanMCP/
├── core/                   # Core modules
│   ├── __init__.py
│   ├── client.py          # HTTP client for Wan API
│   ├── config.py          # Configuration management
│   ├── exceptions.py      # Custom exceptions
│   ├── oauth.py           # OAuth 2.1 provider
│   ├── server.py          # MCP server initialization
│   ├── types.py           # Type definitions
│   └── utils.py           # Utility functions
├── tools/                  # MCP tool definitions
│   ├── __init__.py
│   ├── video_tools.py     # Video generation tools
│   ├── task_tools.py      # Task query tools
│   └── info_tools.py      # Information tools
├── prompts/                # MCP prompts
│   └── __init__.py        # Prompt templates
├── tests/                  # Test suite
│   ├── conftest.py
│   └── __init__.py
├── deploy/                 # Deployment configs
│   └── production/
│       ├── deployment.yaml
│       ├── ingress.yaml
│       └── service.yaml
├── .env.example           # Environment template
├── CHANGELOG.md
├── Dockerfile             # Docker image for HTTP mode
├── docker-compose.yaml    # Docker Compose config
├── LICENSE
├── main.py                # Entry point
├── pyproject.toml         # Project configuration
└── README.md
```

## API Reference

This server wraps the AceDataCloud Wan API:

- Wan Videos API - Video generation (text2video, image2video)
- Wan Tasks API - Task queries

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing`)
5. Open a Pull Request

## License

MIT License - see [LICENSE](LICENSE) for details.

## Links

- [AceDataCloud Platform](https://platform.acedata.cloud)
- [Wan AI](https://wanx.aliyun.com/)
- [Model Context Protocol](https://modelcontextprotocol.io)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)

---

Made with love by [AceDataCloud](https://platform.acedata.cloud)
