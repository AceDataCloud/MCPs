# MCP Hailuo

<!-- mcp-name: io.github.AceDataCloud/mcp-hailuo -->

[![PyPI version](https://img.shields.io/pypi/v/mcp-hailuo.svg)](https://pypi.org/project/mcp-hailuo/)
[![PyPI downloads](https://img.shields.io/pypi/dm/mcp-hailuo.svg)](https://pypi.org/project/mcp-hailuo/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![MCP](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io)

A [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server for AI video generation using [Hailuo (MiniMax)](https://hailuoai.video/) through the [AceDataCloud API](https://platform.acedata.cloud).

Generate AI videos directly from Claude, VS Code, or any MCP-compatible client.

## Features

- **Text to Video** - Create AI-generated videos from text prompts
- **Image to Video** - Generate videos from reference images
- **Director Mode** - Image-to-video with enhanced creative control
- **Multiple Models** - Support for minimax-t2v, minimax-i2v, minimax-i2v-director
- **Task Tracking** - Monitor generation progress and retrieve results

## Tool Reference

| Tool | Description |
|------|-------------|
| `hailuo_generate_video` | Generate AI video from a text prompt using Hailuo (MiniMax). |
| `hailuo_generate_video_from_image` | Generate AI video from a reference image using Hailuo (MiniMax). |
| `hailuo_get_task` | Query the status and result of a video generation task. |
| `hailuo_get_tasks_batch` | Query multiple video generation tasks at once. |
| `hailuo_list_models` | List all available Hailuo models for video generation. |
| `hailuo_list_actions` | List all available Hailuo API actions and corresponding tools. |

## Quick Start

### 1. Get Your API Token

1. Sign up at [AceDataCloud Platform](https://platform.acedata.cloud)
2. Go to the API documentation page
3. Click **"Acquire"** to get your API token
4. Copy the token for use below

### 2. Use the Hosted Server (Recommended)

AceDataCloud hosts a managed MCP server — **no local installation required**.

**Endpoint:** `https://hailuo.mcp.acedata.cloud/mcp`

All requests require a Bearer token. Use the API token from Step 1.

#### Claude.ai

Connect directly on [Claude.ai](https://claude.ai) with OAuth — **no API token needed**:

1. Go to Claude.ai **Settings → Integrations → Add More**
2. Enter the server URL: `https://hailuo.mcp.acedata.cloud/mcp`
3. Complete the OAuth login flow
4. Start using the tools in your conversation

#### Claude Desktop

Add to your config (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "hailuo": {
      "type": "streamable-http",
      "url": "https://hailuo.mcp.acedata.cloud/mcp",
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
    "hailuo": {
      "type": "streamable-http",
      "url": "https://hailuo.mcp.acedata.cloud/mcp",
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
    "hailuo": {
      "type": "streamable-http",
      "url": "https://hailuo.mcp.acedata.cloud/mcp",
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
    "hailuo": {
      "url": "https://hailuo.mcp.acedata.cloud/mcp",
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
claude mcp add hailuo --transport http https://hailuo.mcp.acedata.cloud/mcp \
  -h "Authorization: Bearer YOUR_API_TOKEN"
```

Or add to your project's `.mcp.json`:

```json
{
  "mcpServers": {
    "hailuo": {
      "type": "streamable-http",
      "url": "https://hailuo.mcp.acedata.cloud/mcp",
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
    "hailuo": {
      "type": "streamable-http",
      "url": "https://hailuo.mcp.acedata.cloud/mcp",
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
    "hailuo": {
      "type": "streamable-http",
      "url": "https://hailuo.mcp.acedata.cloud/mcp",
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
    "hailuo": {
      "type": "streamable-http",
      "url": "https://hailuo.mcp.acedata.cloud/mcp",
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
  - name: hailuo
    type: streamable-http
    url: https://hailuo.mcp.acedata.cloud/mcp
    headers:
      Authorization: "Bearer YOUR_API_TOKEN"
```

#### Zed

Add to Zed's settings (`~/.config/zed/settings.json`):

```json
{
  "language_models": {
    "mcp_servers": {
      "hailuo": {
        "url": "https://hailuo.mcp.acedata.cloud/mcp",
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
curl https://hailuo.mcp.acedata.cloud/health

# MCP initialize
curl -X POST https://hailuo.mcp.acedata.cloud/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}'
```

### 3. Or Run Locally (Alternative)

If you prefer to run the server on your own machine:

```bash
# Install from PyPI
pip install mcp-hailuo
# or
uvx mcp-hailuo

# Set your API token
export ACEDATACLOUD_API_TOKEN="your_token_here"

# Run (stdio mode for Claude Desktop / local clients)
mcp-hailuo

# Run (HTTP mode for remote access)
mcp-hailuo --transport http --port 8000
```

#### Claude Desktop (Local)

```json
{
  "mcpServers": {
    "hailuo": {
      "command": "uvx",
      "args": ["mcp-hailuo"],
      "env": {
        "ACEDATACLOUD_API_TOKEN": "your_token_here"
      }
    }
  }
}
```

#### Docker (Self-Hosting)

```bash
docker pull ghcr.io/acedatacloud/mcp-hailuo:latest
docker run -p 8000:8000 ghcr.io/acedatacloud/mcp-hailuo:latest
```

Clients connect with their own Bearer token — the server extracts the token from each request's `Authorization` header.

## Available Tools

### Video Generation

| Tool                                | Description                            |
| ----------------------------------- | -------------------------------------- |
| `hailuo_generate_video`             | Generate video from a text prompt      |
| `hailuo_generate_video_from_image`  | Generate video using a reference image |

### Tasks

| Tool                    | Description                  |
| ----------------------- | ---------------------------- |
| `hailuo_get_task`       | Query a single task status   |
| `hailuo_get_tasks_batch`| Query multiple tasks at once |

### Information

| Tool                  | Description                |
| --------------------- | -------------------------- |
| `hailuo_list_models`  | List available models      |
| `hailuo_list_actions` | List available API actions |

## Usage Examples

### Generate Video from Prompt

```
User: Create a video of waves on a beach

Claude: I'll generate a beach wave video for you.
[Calls hailuo_generate_video with prompt="Ocean waves gently crashing on sandy beach, sunset"]
```

### Animate an Image

```
User: Animate this image: https://example.com/image.jpg

Claude: I'll create a video from your image.
[Calls hailuo_generate_video_from_image with first_image_url and appropriate prompt]
```

## Available Models

| Model                | Type            | Description                               | Requires Image |
| -------------------- | --------------- | ----------------------------------------- | -------------- |
| `minimax-t2v`        | Text-to-Video   | Generate video from text prompt (default) | No             |
| `minimax-i2v`        | Image-to-Video  | Generate video from a reference image     | Yes            |
| `minimax-i2v-director` | Director Mode | Image-to-video with creative control      | Yes            |

## Configuration

### Environment Variables

| Variable                    | Description                 | Default                     |
| --------------------------- | --------------------------- | --------------------------- |
| `ACEDATACLOUD_API_TOKEN`    | API token from AceDataCloud | **Required**                |
| `ACEDATACLOUD_API_BASE_URL` | API base URL                | `https://api.acedata.cloud` |
| `ACEDATACLOUD_OAUTH_CLIENT_ID`  | OAuth client ID (hosted mode) | —                       |
| `ACEDATACLOUD_PLATFORM_BASE_URL` | Platform base URL          | `https://platform.acedata.cloud` |
| `HAILUO_DEFAULT_MODEL`     | Default video model         | `minimax-t2v`               |
| `HAILUO_REQUEST_TIMEOUT`   | Request timeout in seconds  | `1800`                      |
| `LOG_LEVEL`                 | Logging level               | `INFO`                      |

### Command Line Options

```bash
mcp-hailuo --help

Options:
  --version          Show version
  --transport        Transport mode: stdio (default) or http
  --port             Port for HTTP transport (default: 8000)
```

## Development

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/AceDataCloud/HailuoMCP.git
cd HailuoMCP

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
HailuoMCP/
├── core/                   # Core modules
│   ├── __init__.py
│   ├── client.py          # HTTP client for Hailuo API
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

This server wraps the AceDataCloud Hailuo API:

- Hailuo Videos API - Video generation
- Hailuo Tasks API - Task queries

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
- [Hailuo AI](https://hailuoai.video/)
- [Model Context Protocol](https://modelcontextprotocol.io)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)

---

Made with love by [AceDataCloud](https://platform.acedata.cloud)
