# MCP Sora

<!-- mcp-name: io.github.AceDataCloud/mcp-sora -->

[![PyPI version](https://img.shields.io/pypi/v/mcp-sora.svg)](https://pypi.org/project/mcp-sora/)
[![PyPI downloads](https://img.shields.io/pypi/dm/mcp-sora.svg)](https://pypi.org/project/mcp-sora/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![MCP](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io)

A [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server for AI video generation using [Sora](https://openai.com/sora) through the [AceDataCloud API](https://platform.acedata.cloud).

Generate AI videos directly from Claude, VS Code, or any MCP-compatible client.

## Features

- **Text-to-Video** - Generate videos from text descriptions
- **Image-to-Video** - Animate images and create videos from reference images
- **Character Videos** - Reuse characters across different scenes
- **Async Generation** - Webhook callbacks for production workflows
- **Multiple Orientations** - Landscape and portrait videos
- **Task Tracking** - Monitor generation progress and retrieve results

## Quick Start

### 1. Get Your API Token

1. Sign up at [AceDataCloud Platform](https://platform.acedata.cloud)
2. Go to the [API documentation page](https://platform.acedata.cloud/documents/99a24421-2e22-4028-8201-e19cb834b67e)
3. Click **"Acquire"** to get your API token
4. Copy the token for use below

### 2. Use the Hosted Server (Recommended)

AceDataCloud hosts a managed MCP server — **no local installation required**.

**Endpoint:** `https://sora.mcp.acedata.cloud/mcp`

All requests require a Bearer token. Use the API token from Step 1.

#### Claude.ai

Connect directly on [Claude.ai](https://claude.ai) with OAuth — **no API token needed**:

1. Go to Claude.ai **Settings → Integrations → Add More**
2. Enter the server URL: `https://sora.mcp.acedata.cloud/mcp`
3. Complete the OAuth login flow
4. Start using the tools in your conversation

#### Claude Desktop

Add to your config (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "sora": {
      "type": "streamable-http",
      "url": "https://sora.mcp.acedata.cloud/mcp",
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
    "sora": {
      "type": "streamable-http",
      "url": "https://sora.mcp.acedata.cloud/mcp",
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
    "sora": {
      "type": "streamable-http",
      "url": "https://sora.mcp.acedata.cloud/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_API_TOKEN"
      }
    }
  }
}
```

Or install the [Ace Data Cloud MCP extension](https://marketplace.visualstudio.com/items?itemName=acedatacloud.acedatacloud-mcp) for VS Code, which bundles all 11 MCP servers with one-click setup.

#### JetBrains IDEs

1. Go to **Settings → Tools → AI Assistant → Model Context Protocol (MCP)**
2. Click **Add** → **HTTP**
3. Paste:

```json
{
  "mcpServers": {
    "sora": {
      "url": "https://sora.mcp.acedata.cloud/mcp",
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
claude mcp add sora --transport http https://sora.mcp.acedata.cloud/mcp \
  -h "Authorization: Bearer YOUR_API_TOKEN"
```

Or add to your project's `.mcp.json`:

```json
{
  "mcpServers": {
    "sora": {
      "type": "streamable-http",
      "url": "https://sora.mcp.acedata.cloud/mcp",
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
    "sora": {
      "type": "streamable-http",
      "url": "https://sora.mcp.acedata.cloud/mcp",
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
    "sora": {
      "type": "streamable-http",
      "url": "https://sora.mcp.acedata.cloud/mcp",
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
    "sora": {
      "type": "streamable-http",
      "url": "https://sora.mcp.acedata.cloud/mcp",
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
  - name: sora
    type: streamable-http
    url: https://sora.mcp.acedata.cloud/mcp
    headers:
      Authorization: "Bearer YOUR_API_TOKEN"
```

#### Zed

Add to Zed's settings (`~/.config/zed/settings.json`):

```json
{
  "language_models": {
    "mcp_servers": {
      "sora": {
        "url": "https://sora.mcp.acedata.cloud/mcp",
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
curl https://sora.mcp.acedata.cloud/health

# MCP initialize
curl -X POST https://sora.mcp.acedata.cloud/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}'
```

### 3. Or Run Locally (Alternative)

If you prefer to run the server on your own machine:

```bash
# Install from PyPI
pip install mcp-sora
# or
uvx mcp-sora

# Set your API token
export ACEDATACLOUD_API_TOKEN="your_token_here"

# Run (stdio mode for Claude Desktop / local clients)
mcp-sora

# Run (HTTP mode for remote access)
mcp-sora --transport http --port 8000
```

#### Claude Desktop (Local)

```json
{
  "mcpServers": {
    "sora": {
      "command": "uvx",
      "args": ["mcp-sora"],
      "env": {
        "ACEDATACLOUD_API_TOKEN": "your_token_here"
      }
    }
  }
}
```

#### Docker (Self-Hosting)

```bash
docker pull ghcr.io/acedatacloud/mcp-sora:latest
docker run -p 8000:8000 ghcr.io/acedatacloud/mcp-sora:latest
```

Clients connect with their own Bearer token — the server extracts the token from each request's `Authorization` header.

## Available Tools

### Video Generation

| Tool                                 | Description                                          |
| ------------------------------------ | ---------------------------------------------------- |
| `sora_generate_video`                | Generate video from a text prompt                    |
| `sora_generate_video_from_image`     | Generate video from reference images                 |
| `sora_generate_video_with_character` | Generate video with a character from reference video |
| `sora_generate_video_async`          | Generate video with callback notification            |

### Tasks

| Tool                   | Description                  |
| ---------------------- | ---------------------------- |
| `sora_get_task`        | Query a single task status   |
| `sora_get_tasks_batch` | Query multiple tasks at once |

### Information

| Tool                | Description                |
| ------------------- | -------------------------- |
| `sora_list_models`  | List available Sora models |
| `sora_list_actions` | List available API actions |

## Usage Examples

### Generate Video from Prompt

```
User: Create a video of a sunset over mountains

Claude: I'll generate a sunset video for you.
[Calls sora_generate_video with prompt="A beautiful sunset over mountains..."]
```

### Generate from Image

```
User: Animate this image of a city skyline

Claude: I'll bring this image to life.
[Calls sora_generate_video_from_image with image_urls and prompt]
```

### Character-based Video

```
User: Use the robot character in a new scene

Claude: I'll create a new scene with the robot character.
[Calls sora_generate_video_with_character with character_url and prompt]
```

## Available Models

| Model        | Max Duration | Quality | Features                      |
| ------------ | ------------ | ------- | ----------------------------- |
| `sora-2`     | 15 seconds   | Good    | Standard generation           |
| `sora-2-pro` | 25 seconds   | Best    | Higher quality, longer videos |

### Video Options

**Size:**

- `small` - Lower resolution, faster generation
- `large` - Higher resolution (recommended)

**Orientation:**

- `landscape` - 16:9 (YouTube, presentations)
- `portrait` - 9:16 (TikTok, Instagram Stories)

**Duration:**

- `10` seconds - All models
- `15` seconds - All models
- `25` seconds - sora-2-pro only

## Configuration

### Environment Variables

| Variable                    | Description                 | Default                     |
| --------------------------- | --------------------------- | --------------------------- |
| `ACEDATACLOUD_API_TOKEN`    | API token from AceDataCloud | **Required**                |
| `ACEDATACLOUD_API_BASE_URL` | API base URL                | `https://api.acedata.cloud` |
| `ACEDATACLOUD_OAUTH_CLIENT_ID`  | OAuth client ID (hosted mode) | —                           |
| `ACEDATACLOUD_PLATFORM_BASE_URL` | Platform base URL            | `https://platform.acedata.cloud` |
| `SORA_DEFAULT_MODEL`        | Default model               | `sora-2`                    |
| `SORA_DEFAULT_SIZE`         | Default video size          | `large`                     |
| `SORA_DEFAULT_DURATION`     | Default duration (seconds)  | `15`                        |
| `SORA_DEFAULT_ORIENTATION`  | Default orientation         | `landscape`                 |
| `SORA_REQUEST_TIMEOUT`      | Request timeout (seconds)   | `3600`                      |
| `LOG_LEVEL`                 | Logging level               | `INFO`                      |

### Command Line Options

```bash
mcp-sora --help

Options:
  --version          Show version
  --transport        Transport mode: stdio (default) or http
  --port             Port for HTTP transport (default: 8000)
```

## Development

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/AceDataCloud/SoraMCP.git
cd SoraMCP

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
SoraMCP/
├── core/                   # Core modules
│   ├── __init__.py
│   ├── client.py          # HTTP client for Sora API
│   ├── config.py          # Configuration management
│   ├── exceptions.py      # Custom exceptions
│   ├── server.py          # MCP server initialization
│   ├── types.py           # Type definitions
│   └── utils.py           # Utility functions
├── tools/                  # MCP tool definitions
│   ├── __init__.py
│   ├── video_tools.py     # Video generation tools
│   ├── task_tools.py      # Task query tools
│   └── info_tools.py      # Information tools
├── prompts/                # MCP prompt templates
│   └── __init__.py
├── tests/                  # Test suite
│   ├── conftest.py
│   ├── test_client.py
│   ├── test_config.py
│   ├── test_integration.py
│   └── test_utils.py
├── deploy/                 # Deployment configs
│   └── production/
│       ├── deployment.yaml
│       ├── ingress.yaml
│       └── service.yaml
├── .env.example           # Environment template
├── .gitignore
├── CHANGELOG.md
├── Dockerfile             # Docker image for HTTP mode
├── docker-compose.yaml    # Docker Compose config
├── LICENSE
├── main.py                # Entry point
├── pyproject.toml         # Project configuration
└── README.md
```

## API Reference

This server wraps the [AceDataCloud Sora API](https://platform.acedata.cloud/documents/99a24421-2e22-4028-8201-e19cb834b67e):

- [Sora Videos API](https://platform.acedata.cloud/documents/99a24421-2e22-4028-8201-e19cb834b67e) - Video generation
- [Sora Tasks API](https://platform.acedata.cloud/documents/c9d81bad-9064-4796-86b6-4fb43cc93a16) - Task queries

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
- [Sora Official](https://openai.com/sora)
- [Model Context Protocol](https://modelcontextprotocol.io)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)

---

Made with love by [AceDataCloud](https://platform.acedata.cloud)
