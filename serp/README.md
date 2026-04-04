# MCP Serp

<!-- mcp-name: io.github.AceDataCloud/mcp-serp -->

[![PyPI version](https://img.shields.io/pypi/v/mcp-serp.svg)](https://pypi.org/project/mcp-serp/)
[![PyPI downloads](https://img.shields.io/pypi/dm/mcp-serp.svg)](https://pypi.org/project/mcp-serp/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![MCP](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io)

A [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server for Google search using [SERP API](https://platform.acedata.cloud/documents/44c86226-8eaa-49bf-85f3-1fae8d2e23f1) through the [AceDataCloud API](https://platform.acedata.cloud).

Perform Google searches and get structured results directly from Claude, VS Code, or any MCP-compatible client.

## Features

- **Web Search** - Regular Google web search with structured results
- **Image Search** - Search for images with URLs and thumbnails
- **News Search** - Get latest news articles on any topic
- **Video Search** - Find videos from YouTube and other sources
- **Places Search** - Search for local businesses and places
- **Maps Search** - Find locations and geographic information
- **Knowledge Graph** - Get structured entity information
- **Localization** - Support for multiple countries and languages
- **Time Filtering** - Filter results by time range

## Quick Start

### 1. Get Your API Token

1. Sign up at [AceDataCloud Platform](https://platform.acedata.cloud)
2. Go to the [API documentation page](https://platform.acedata.cloud/documents/44c86226-8eaa-49bf-85f3-1fae8d2e23f1)
3. Click **"Acquire"** to get your API token
4. Copy the token for use below

### 2. Use the Hosted Server (Recommended)

AceDataCloud hosts a managed MCP server — **no local installation required**.

**Endpoint:** `https://serp.mcp.acedata.cloud/mcp`

All requests require a Bearer token. Use the API token from Step 1.

#### Claude.ai

Connect directly on [Claude.ai](https://claude.ai) with OAuth — **no API token needed**:

1. Go to Claude.ai **Settings → Integrations → Add More**
2. Enter the server URL: `https://serp.mcp.acedata.cloud/mcp`
3. Complete the OAuth login flow
4. Start using the tools in your conversation

#### Claude Desktop

Add to your config (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "serp": {
      "type": "streamable-http",
      "url": "https://serp.mcp.acedata.cloud/mcp",
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
    "serp": {
      "type": "streamable-http",
      "url": "https://serp.mcp.acedata.cloud/mcp",
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
    "serp": {
      "type": "streamable-http",
      "url": "https://serp.mcp.acedata.cloud/mcp",
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
    "serp": {
      "url": "https://serp.mcp.acedata.cloud/mcp",
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
claude mcp add serp --transport http https://serp.mcp.acedata.cloud/mcp \
  -h "Authorization: Bearer YOUR_API_TOKEN"
```

Or add to your project's `.mcp.json`:

```json
{
  "mcpServers": {
    "serp": {
      "type": "streamable-http",
      "url": "https://serp.mcp.acedata.cloud/mcp",
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
    "serp": {
      "type": "streamable-http",
      "url": "https://serp.mcp.acedata.cloud/mcp",
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
    "serp": {
      "type": "streamable-http",
      "url": "https://serp.mcp.acedata.cloud/mcp",
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
    "serp": {
      "type": "streamable-http",
      "url": "https://serp.mcp.acedata.cloud/mcp",
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
  - name: serp
    type: streamable-http
    url: https://serp.mcp.acedata.cloud/mcp
    headers:
      Authorization: "Bearer YOUR_API_TOKEN"
```

#### Zed

Add to Zed's settings (`~/.config/zed/settings.json`):

```json
{
  "language_models": {
    "mcp_servers": {
      "serp": {
        "url": "https://serp.mcp.acedata.cloud/mcp",
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
curl https://serp.mcp.acedata.cloud/health

# MCP initialize
curl -X POST https://serp.mcp.acedata.cloud/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}'
```

### 3. Or Run Locally (Alternative)

If you prefer to run the server on your own machine:

```bash
# Install from PyPI
pip install mcp-serp
# or
uvx mcp-serp

# Set your API token
export ACEDATACLOUD_API_TOKEN="your_token_here"

# Run (stdio mode for Claude Desktop / local clients)
mcp-serp

# Run (HTTP mode for remote access)
mcp-serp --transport http --port 8000
```

#### Claude Desktop (Local)

```json
{
  "mcpServers": {
    "serp": {
      "command": "uvx",
      "args": ["mcp-serp"],
      "env": {
        "ACEDATACLOUD_API_TOKEN": "your_token_here"
      }
    }
  }
}
```

#### Docker (Self-Hosting)

```bash
docker pull ghcr.io/acedatacloud/mcp-serp:latest
docker run -p 8000:8000 ghcr.io/acedatacloud/mcp-serp:latest
```

Clients connect with their own Bearer token — the server extracts the token from each request's `Authorization` header.

## Available Tools

### Search Tools

| Tool                 | Description                             |
| -------------------- | --------------------------------------- |
| `serp_google_search` | Flexible Google search with all options |
| `serp_google_images` | Search for images                       |
| `serp_google_news`   | Search for news articles                |
| `serp_google_videos` | Search for videos                       |
| `serp_google_places` | Search for local places/businesses      |
| `serp_google_maps`   | Search for map locations                |

### Information Tools

| Tool                     | Description                          |
| ------------------------ | ------------------------------------ |
| `serp_list_search_types` | List available search types          |
| `serp_list_countries`    | List country codes for localization  |
| `serp_list_languages`    | List language codes for localization |
| `serp_list_time_ranges`  | List time range filter options       |
| `serp_get_usage_guide`   | Get comprehensive usage guide        |

## Usage Examples

### Basic Web Search

```
User: Search for information about artificial intelligence

Claude: I'll search for information about AI.
[Calls serp_google_search with query="artificial intelligence"]
```

### News Search with Time Filter

```
User: What's the latest news about technology?

Claude: I'll search for recent tech news.
[Calls serp_google_news with query="technology", time_range="qdr:d"]
```

### Localized Search

```
User: Find popular restaurants in Tokyo

Claude: I'll search for restaurants in Tokyo.
[Calls serp_google_places with query="popular restaurants Tokyo", country="jp"]
```

### Image Search

```
User: Find images of the Northern Lights

Claude: I'll search for aurora borealis images.
[Calls serp_google_images with query="Northern Lights aurora borealis"]
```

## Search Parameters

### Search Types

| Type     | Description                  |
| -------- | ---------------------------- |
| `search` | Regular web search (default) |
| `images` | Image search                 |
| `news`   | News articles                |
| `maps`   | Map results                  |
| `places` | Local businesses             |
| `videos` | Video results                |

### Time Range Filters

| Code    | Time Range |
| ------- | ---------- |
| `qdr:h` | Past hour  |
| `qdr:d` | Past day   |
| `qdr:w` | Past week  |
| `qdr:m` | Past month |

### Common Country Codes

| Code | Country        |
| ---- | -------------- |
| `us` | United States  |
| `uk` | United Kingdom |
| `cn` | China          |
| `jp` | Japan          |
| `de` | Germany        |
| `fr` | France         |

### Common Language Codes

| Code    | Language             |
| ------- | -------------------- |
| `en`    | English              |
| `zh-cn` | Chinese (Simplified) |
| `ja`    | Japanese             |
| `es`    | Spanish              |
| `fr`    | French               |
| `de`    | German               |

## Response Structure

### Regular Search Results

- **knowledge_graph**: Entity information (company, person, etc.)
- **answer_box**: Direct answers
- **organic**: Regular search results with title, link, snippet
- **people_also_ask**: Related questions
- **related_searches**: Related queries

### Image Search Results

- **images**: Image results with URLs and thumbnails

### News Search Results

- **news**: News articles with source and date

## Configuration

### Environment Variables

| Variable                    | Description                 | Default                     |
| --------------------------- | --------------------------- | --------------------------- |
| `ACEDATACLOUD_API_TOKEN`    | API token from AceDataCloud | **Required**                |
| `ACEDATACLOUD_API_BASE_URL` | API base URL                | `https://api.acedata.cloud` |
| `ACEDATACLOUD_OAUTH_CLIENT_ID`  | OAuth client ID (hosted mode) | —                           |
| `ACEDATACLOUD_PLATFORM_BASE_URL` | Platform base URL            | `https://platform.acedata.cloud` |
| `SERP_REQUEST_TIMEOUT`      | Request timeout in seconds  | `30`                        |
| `LOG_LEVEL`                 | Logging level               | `INFO`                      |

### Command Line Options

```bash
mcp-serp --help

Options:
  --version          Show version
  --transport        Transport mode: stdio (default) or http
  --port             Port for HTTP transport (default: 8000)
```

## Development

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/AceDataCloud/SerpMCP.git
cd SerpMCP

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
SerpMCP/
├── core/                   # Core modules
│   ├── __init__.py
│   ├── client.py          # HTTP client for SERP API
│   ├── config.py          # Configuration management
│   ├── exceptions.py      # Custom exceptions
│   └── server.py          # MCP server initialization
├── tools/                  # MCP tool definitions
│   ├── __init__.py
│   ├── search_tools.py    # Search tools
│   └── info_tools.py      # Information tools
├── prompts/                # MCP prompt templates
│   └── __init__.py
├── tests/                  # Test suite
│   ├── conftest.py
│   ├── test_client.py
│   └── test_config.py
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

This server wraps the [AceDataCloud Google SERP API](https://platform.acedata.cloud/documents/44c86226-8eaa-49bf-85f3-1fae8d2e23f1):

- [Google SERP API Documentation](https://platform.acedata.cloud/documents/44c86226-8eaa-49bf-85f3-1fae8d2e23f1)

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
- [Google SERP API](https://platform.acedata.cloud/documents/44c86226-8eaa-49bf-85f3-1fae8d2e23f1)
- [Model Context Protocol](https://modelcontextprotocol.io)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)

---

Made with love by [AceDataCloud](https://platform.acedata.cloud)
