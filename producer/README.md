# ProducerMCP

<!-- mcp-name: io.github.AceDataCloud/mcp-producer -->

[![PyPI version](https://img.shields.io/pypi/v/mcp-producer.svg)](https://pypi.org/project/mcp-producer/)
[![PyPI downloads](https://img.shields.io/pypi/dm/mcp-producer.svg)](https://pypi.org/project/mcp-producer/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![MCP](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io)

A [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server for AI music generation using [Producer/Riffusion](https://www.riffusion.com/) (FUZZ models) through the [AceDataCloud API](https://platform.acedata.cloud).

Generate AI music directly from Claude, VS Code, or any MCP-compatible client.

## Features

- **Text to Music** - Create AI-generated music from text prompts
- **Custom Music** - Full control with custom lyrics, title, and style
- **Song Extension** - Continue songs from any timestamp
- **Cover/Remix** - Create covers in different genres and styles
- **Variations** - Generate alternative versions of songs
- **Vocal/Instrumental Swap** - Mix vocals and instrumentals between songs
- **Section Replacement** - Re-generate specific sections of a song
- **Stem Separation** - Split songs into vocal and instrumental tracks
- **Lyrics Generation** - Generate structured lyrics from prompts
- **Video Generation** - Create music videos for songs
- **WAV Export** - Get lossless audio format
- **8 FUZZ Models** - From FUZZ-0.8 to FUZZ-2.0 Pro

## Tool Reference

| Tool | Description |
|------|-------------|
| `producer_generate_music` | Generate AI music from a text prompt. |
| `producer_generate_custom_music` | Generate music with custom lyrics, title, and style. |
| `producer_extend_music` | Extend an existing song from a specific timestamp. |
| `producer_cover_music` | Create a cover/remix version in a different style. |
| `producer_variation_music` | Create a variation of an existing song. |
| `producer_swap_vocals` | Swap vocals between two songs. |
| `producer_swap_instrumentals` | Swap instrumentals between two songs. |
| `producer_replace_section` | Replace a specific time range with new content. |
| `producer_stems_music` | Separate a song into vocal and instrumental stems. |
| `producer_generate_lyrics` | Generate structured song lyrics from a prompt. |
| `producer_upload_audio` | Upload external audio for processing. |
| `producer_generate_video` | Generate a music video for a song. |
| `producer_generate_wav` | Get lossless WAV format of a song. |
| `producer_get_task` | Query the status of a generation task. |
| `producer_get_tasks_batch` | Query multiple generation tasks at once. |
| `producer_list_models` | List all available FUZZ models. |
| `producer_list_actions` | List all available actions and tools. |
| `producer_get_lyric_format_guide` | Get lyrics formatting guide. |

## Quick Start

### 1. Get Your API Token

1. Sign up at [AceDataCloud Platform](https://platform.acedata.cloud)
2. Navigate to the API documentation
3. Click **"Acquire"** to get your API token
4. Copy the token for use below

### 2. Use the Hosted Server (Recommended)

AceDataCloud hosts a managed MCP server -- **no local installation required**.

**Endpoint:** `https://producer.mcp.acedata.cloud/mcp`

All requests require a Bearer token. Use the API token from Step 1.

#### Claude.ai

Connect directly on [Claude.ai](https://claude.ai) with OAuth -- **no API token needed**:

1. Go to Claude.ai **Settings > Integrations > Add More**
2. Enter the server URL: `https://producer.mcp.acedata.cloud/mcp`
3. Complete the OAuth login flow
4. Start using the tools in your conversation

#### Claude Desktop

Add to your config (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "producer": {
      "type": "streamable-http",
      "url": "https://producer.mcp.acedata.cloud/mcp",
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
    "producer": {
      "type": "streamable-http",
      "url": "https://producer.mcp.acedata.cloud/mcp",
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
    "producer": {
      "type": "streamable-http",
      "url": "https://producer.mcp.acedata.cloud/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_API_TOKEN"
      }
    }
  }
}
```

Or install the [Ace Data Cloud MCP extension](https://marketplace.visualstudio.com/items?itemName=acedatacloud.acedatacloud-mcp) for VS Code, which bundles all MCP servers with one-click setup.

#### JetBrains IDEs

1. Go to **Settings > Tools > AI Assistant > Model Context Protocol (MCP)**
2. Click **Add** > **HTTP**
3. Paste:

```json
{
  "mcpServers": {
    "producer": {
      "url": "https://producer.mcp.acedata.cloud/mcp",
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
claude mcp add producer --transport http https://producer.mcp.acedata.cloud/mcp \
  -h "Authorization: Bearer YOUR_API_TOKEN"
```

Or add to your project's `.mcp.json`:

```json
{
  "mcpServers": {
    "producer": {
      "type": "streamable-http",
      "url": "https://producer.mcp.acedata.cloud/mcp",
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
    "producer": {
      "type": "streamable-http",
      "url": "https://producer.mcp.acedata.cloud/mcp",
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
    "producer": {
      "type": "streamable-http",
      "url": "https://producer.mcp.acedata.cloud/mcp",
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
    "producer": {
      "type": "streamable-http",
      "url": "https://producer.mcp.acedata.cloud/mcp",
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
  - name: producer
    type: streamable-http
    url: https://producer.mcp.acedata.cloud/mcp
    headers:
      Authorization: "Bearer YOUR_API_TOKEN"
```

#### Zed

Add to Zed's settings (`~/.config/zed/settings.json`):

```json
{
  "language_models": {
    "mcp_servers": {
      "producer": {
        "url": "https://producer.mcp.acedata.cloud/mcp",
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
curl https://producer.mcp.acedata.cloud/health

# MCP initialize
curl -X POST https://producer.mcp.acedata.cloud/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}'
```

### 3. Or Run Locally (Alternative)

If you prefer to run the server on your own machine:

```bash
# Install from PyPI
pip install mcp-producer
# or
uvx mcp-producer

# Set your API token
export ACEDATACLOUD_API_TOKEN="your_token_here"

# Run (stdio mode for Claude Desktop / local clients)
mcp-producer

# Run (HTTP mode for remote access)
mcp-producer --transport http --port 8000
```

#### Claude Desktop (Local)

```json
{
  "mcpServers": {
    "producer": {
      "command": "uvx",
      "args": ["mcp-producer"],
      "env": {
        "ACEDATACLOUD_API_TOKEN": "your_token_here"
      }
    }
  }
}
```

#### Docker (Self-Hosting)

```bash
docker pull ghcr.io/acedatacloud/mcp-producer:latest
docker run -p 8000:8000 ghcr.io/acedatacloud/mcp-producer:latest
```

Clients connect with their own Bearer token -- the server extracts the token from each request's `Authorization` header.

## Available Tools

### Music Generation

| Tool                             | Description                             |
| -------------------------------- | --------------------------------------- |
| `producer_generate_music`        | Generate music from a text prompt       |
| `producer_generate_custom_music` | Generate with custom lyrics and style   |
| `producer_extend_music`          | Extend a song from a timestamp          |
| `producer_cover_music`           | Create a cover in a different style     |
| `producer_variation_music`       | Create a variation of a song            |

### Vocal/Instrumental

| Tool                             | Description                             |
| -------------------------------- | --------------------------------------- |
| `producer_swap_vocals`           | Swap vocals between two songs           |
| `producer_swap_instrumentals`    | Swap instrumentals between two songs    |
| `producer_replace_section`       | Replace a time range with new content   |
| `producer_stems_music`           | Separate into stems                     |

### Lyrics

| Tool                       | Description                      |
| -------------------------- | -------------------------------- |
| `producer_generate_lyrics` | Generate lyrics from a prompt    |

### Media

| Tool                       | Description                      |
| -------------------------- | -------------------------------- |
| `producer_upload_audio`    | Upload external audio            |
| `producer_generate_video`  | Generate video for a song        |
| `producer_generate_wav`    | Get lossless WAV format          |

### Tasks

| Tool                       | Description                      |
| -------------------------- | -------------------------------- |
| `producer_get_task`        | Query a single task status       |
| `producer_get_tasks_batch` | Query multiple tasks at once     |

### Information

| Tool                              | Description                      |
| --------------------------------- | -------------------------------- |
| `producer_list_models`            | List available FUZZ models       |
| `producer_list_actions`           | List available API actions       |
| `producer_get_lyric_format_guide` | Lyric formatting guide           |

## Usage Examples

### Generate Music from Prompt

```
User: Create a jazz song about rainy nights

Claude: I'll generate a jazz song for you.
[Calls producer_generate_music with prompt="Smooth jazz song about rainy nights, saxophone, piano, moody"]
```

### Custom Song with Lyrics

```
User: Here are my lyrics:
[Verse] Walking in the rain...
[Chorus] But I keep moving on...

Claude: I'll create a song with your lyrics.
[Calls producer_generate_custom_music with lyrics, title, and style]
```

### Extend a Song

```
User: Make this song longer with another verse

Claude: I'll extend the song from where it left off.
[Calls producer_extend_music with audio_id, continue_at, and new lyrics]
```

### Create a Cover

```
User: Make an acoustic version of this song

Claude: I'll create an acoustic cover.
[Calls producer_cover_music with audio_id and style="acoustic folk, gentle guitar"]
```

## Available Models

| Model            | Tier    | Description                                      |
|------------------|---------|--------------------------------------------------|
| FUZZ-2.0 Pro     | Pro     | Highest quality, best for professional production |
| FUZZ-2.0         | Default | Recommended for most use cases (default)          |
| FUZZ-2.0 Raw     | Raw     | Unprocessed output, for custom post-processing    |
| FUZZ-1.1 Pro     | Pro     | High quality legacy model                         |
| FUZZ-1.0 Pro     | Pro     | Professional legacy model                         |
| FUZZ-1.0         | Default | Stable legacy model                               |
| FUZZ-1.1         | Default | Improved legacy model                              |
| FUZZ-0.8         | Legacy  | Original model, basic quality                      |

## Configuration

### Environment Variables

| Variable                    | Description                 | Default                     |
| --------------------------- | --------------------------- | --------------------------- |
| `ACEDATACLOUD_API_TOKEN`    | API token from AceDataCloud | **Required**                |
| `ACEDATACLOUD_API_BASE_URL` | API base URL                | `https://api.acedata.cloud` |
| `ACEDATACLOUD_OAUTH_CLIENT_ID`  | OAuth client ID (hosted mode) | --                          |
| `ACEDATACLOUD_PLATFORM_BASE_URL` | Platform base URL            | `https://platform.acedata.cloud` |
| `PRODUCER_DEFAULT_MODEL`    | Default FUZZ model          | `FUZZ-2.0`                  |
| `PRODUCER_REQUEST_TIMEOUT`  | Request timeout in seconds  | `1800`                      |
| `LOG_LEVEL`                 | Logging level               | `INFO`                      |

### Command Line Options

```bash
mcp-producer --help

Options:
  --version          Show version
  --transport        Transport mode: stdio (default) or http
  --port             Port for HTTP transport (default: 8000)
```

## Development

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/AceDataCloud/ProducerMCP.git
cd ProducerMCP

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
ProducerMCP/
├── core/                   # Core modules
│   ├── __init__.py
│   ├── client.py          # HTTP client for Producer API
│   ├── config.py          # Configuration management
│   ├── exceptions.py      # Custom exceptions
│   ├── oauth.py           # OAuth 2.1 provider
│   ├── server.py          # MCP server initialization
│   ├── types.py           # Type definitions (models, actions)
│   └── utils.py           # Utility functions
├── tools/                  # MCP tool definitions
│   ├── __init__.py
│   ├── audio_tools.py     # Audio generation tools (9 tools)
│   ├── lyrics_tools.py    # Lyrics generation
│   ├── media_tools.py     # Upload, video, WAV tools
│   ├── task_tools.py      # Task query tools
│   └── info_tools.py      # Information tools
├── prompts/                # MCP prompts
│   └── __init__.py        # Prompt templates
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
├── .ruff.toml             # Ruff linter config
├── CHANGELOG.md
├── Dockerfile             # Docker image for HTTP mode
├── docker-compose.yaml    # Docker Compose config
├── LICENSE
├── main.py                # Entry point
├── pyproject.toml         # Project configuration
└── README.md
```

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
- [Riffusion](https://www.riffusion.com/)
- [Model Context Protocol](https://modelcontextprotocol.io)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)

---

Made with love by [AceDataCloud](https://platform.acedata.cloud)
