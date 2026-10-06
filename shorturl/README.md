# ShortURLMCP

<!-- mcp-name: io.github.AceDataCloud/mcp-shorturl -->

[![PyPI version](https://img.shields.io/pypi/v/mcp-shorturl.svg)](https://pypi.org/project/mcp-shorturl/)
[![PyPI downloads](https://img.shields.io/pypi/dm/mcp-shorturl.svg)](https://pypi.org/project/mcp-shorturl/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![MCP](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io)

A [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server for URL shortening using [Short URL API](https://platform.acedata.cloud/documents/shorturl?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=shorturl_mcp_readme_documents_shorturl) through the [AceDataCloud API](https://platform.acedata.cloud?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=shorturl_mcp_readme_platform).

Create short, shareable URLs directly from Claude, VS Code, or any MCP-compatible client.

## Features

- **URL Shortening** - Convert long URLs into short, shareable links
- **Batch Shortening** - Shorten multiple URLs at once (up to 10 per batch)
- **Free Service** - Zero credit consumption per request
- **Permanent Links** - Short URLs never expire
- **surl.id Domain** - Short URLs use the clean `surl.id` domain
- **Bearer Auth** - Secure API access with token authentication

## Tool Reference

| Tool | Description |
|------|-------------|
| `shorturl_create` | Create a short URL from a long URL. |
| `shorturl_batch_create` | Create short URLs for multiple long URLs in a single batch. |
| `shorturl_get_usage_guide` | Get a comprehensive guide for using the ShortURL tools. |
| `shorturl_get_api_info` | Get information about the ShortURL API service. |

## Connect: hosted OAuth, API token, or local stdio

The hosted endpoint is `https://shorturl.mcp.acedata.cloud/mcp`. Choose one route for the MCP client:

| Route | When to use it | Credential setup |
|---|---|---|
| Hosted OAuth | The client supports remote MCP OAuth | Add only the URL, then sign in to AceDataCloud and approve access. No token needs to be pasted into client configuration. |
| Hosted API token | The client cannot finish OAuth, or you need an explicit integration credential | Send an AceDataCloud API token in the `Authorization: Bearer …` header. Keep it in a local secret store or environment variable. |
| Local stdio | The client runs a local MCP process | Install `mcp-shorturl` and pass `ACEDATACLOUD_API_TOKEN` to that process. It still calls the AceDataCloud API. |

The hosted service advertises OAuth metadata and Dynamic Client Registration (DCR). **DCR registers the client application; it is not an API key.** OAuth signs you in and the client sends the resulting Bearer token; it may reuse or create an API credential for the account. Browser sign-in still requires an AceDataCloud account. The hosted service can be metered: review [current service documentation](https://platform.acedata.cloud/documents/short-url-mcp?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=shorturl_mcp_readme_quick_start) and displayed pricing before a real operation. Do not configure both an OAuth login and a fixed `Authorization` header for the same server.

### Hosted OAuth examples

- **Claude and Claude Desktop chat:** Add a remote custom connector in `Customize → Connectors → Add custom connector`, enter `https://shorturl.mcp.acedata.cloud/mcp`, select sign-in, and choose **Register automatically** if Claude asks how to register its OAuth client. Complete consent. Claude Desktop's local `claude_desktop_config.json` is a separate setup. [Claude connector guide](https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp).
- **Claude Code:** `claude mcp add --transport http --scope user shorturl https://shorturl.mcp.acedata.cloud/mcp`, then `claude mcp login shorturl`. Check `/mcp`. [Claude Code MCP guide](https://code.claude.com/docs/en/mcp).
- **Cursor:** Add a remote server with only `https://shorturl.mcp.acedata.cloud/mcp`. For a project, merge the entry below into `<project>/.cursor/mcp.json`; for personal use, use `~/.cursor/mcp.json`. [Cursor MCP guide](https://cursor.com/docs/mcp).
- **VS Code / Copilot:** Run **MCP: Add Server**, select HTTP, enter `https://shorturl.mcp.acedata.cloud/mcp`, then finish the browser sign-in. New portable workspace configs use `<project>/.mcp.json`; the VS Code-specific format below uses `<project>/.vscode/mcp.json` or the user profile. Check **MCP: List Servers**. [VS Code MCP setup](https://code.visualstudio.com/docs/agent-customization/mcp-servers).
- **Codex:** `codex mcp add shorturl --url https://shorturl.mcp.acedata.cloud/mcp`, then `codex mcp login shorturl`. Its user settings are in `~/.codex/config.toml`. [Official Codex MCP guide](https://developers.openai.com/codex/mcp/).

Cursor project config (OAuth):

```json
{
  "mcpServers": {
    "shorturl": {"url": "https://shorturl.mcp.acedata.cloud/mcp"}
  }
}
```

VS Code-specific workspace config (OAuth):

```json
{
  "servers": {
    "shorturl": {"type": "http", "url": "https://shorturl.mcp.acedata.cloud/mcp"}
  }
}
```

### Hosted API token

Sign in at [AceDataCloud Platform](https://platform.acedata.cloud?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=shorturl_mcp_readme_platform), open the [service page](https://platform.acedata.cloud/documents/short-url-mcp?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=shorturl_mcp_readme_quick_start), and obtain an API credential. A fixed Bearer header is useful when your client lacks OAuth; an invalid header does not fall back to OAuth in Claude Code. The header value is sensitive, so keep it out of committed files and screenshots.

For Claude Code, the shell expands the token when you add the server; treat the saved user MCP config as a secret:

```bash
export ACEDATACLOUD_API_TOKEN='YOUR_API_TOKEN'
claude mcp add --transport http --scope user shorturl https://shorturl.mcp.acedata.cloud/mcp \
  --header "Authorization: Bearer $ACEDATACLOUD_API_TOKEN"
```

For a Claude Code project config, put a variable reference in `<project>/.mcp.json` and set that variable in the environment that launches Claude Code:

```json
{
  "mcpServers": {
    "shorturl": {
      "type": "http",
      "url": "https://shorturl.mcp.acedata.cloud/mcp",
      "headers": {"Authorization": "Bearer ${ACEDATACLOUD_API_TOKEN}"}
    }
  }
}
```

Cursor uses a different environment-variable syntax in `~/.cursor/mcp.json` or an uncommitted project config:

```json
{
  "mcpServers": {
    "shorturl": {
      "url": "https://shorturl.mcp.acedata.cloud/mcp",
      "headers": {"Authorization": "Bearer ${env:ACEDATACLOUD_API_TOKEN}"}
    }
  }
}
```

In VS Code, run **MCP: Open User Configuration** and merge this server plus its masked input; `${input:...}` is for VS Code's user/workspace format and is not portable to the Agent Host `.mcp.json` format:

```json
{
  "inputs": [
    {"id": "acedata-shorturl-token", "type": "promptString", "description": "AceDataCloud API token", "password": true}
  ],
  "servers": {
    "shorturl": {
      "type": "http",
      "url": "https://shorturl.mcp.acedata.cloud/mcp",
      "headers": {"Authorization": "Bearer ${input:acedata-shorturl-token}"}
    }
  }
}
```

For **Cline**, use its MCP configuration UI or CLI file `~/.cline/data/settings/cline_mcp_settings.json`; its remote transport value is `streamableHttp`. For **JetBrains AI Assistant**, add a remote URL from **Settings → Tools → AI Assistant → Model Context Protocol (MCP)**. For **Zed**, use a `context_servers` entry with the URL only for OAuth or add a local Bearer header. These clients have different configuration schemas; follow their current UI rather than copying another client's JSON. [Cline](https://docs.cline.bot/mcp/mcp-overview) · [JetBrains](https://www.jetbrains.com/help/ai-assistant/mcp.html) · [Zed](https://zed.dev/docs/ai/mcp).

### Local stdio

Install the package and give the local process an API token:

```bash
python -m pip install mcp-shorturl
export ACEDATACLOUD_API_TOKEN='YOUR_API_TOKEN'
mcp-shorturl
```

For Claude Desktop local MCP, merge this entry into the file opened by its developer settings (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS). `uvx` requires [uv](https://docs.astral.sh/uv/) on `PATH`:

```json
{
  "mcpServers": {
    "shorturl": {
      "command": "uvx",
      "args": ["mcp-shorturl"],
      "env": {"ACEDATACLOUD_API_TOKEN": "YOUR_API_TOKEN"}
    }
  }
}
```

Keep this user-level file private. Self-hosted HTTP uses `mcp-shorturl --transport http --port 8000`; expose it only with suitable network and TLS controls. Local execution still calls the AceDataCloud API.

### Check before using the service

1. `https://shorturl.mcp.acedata.cloud/health` returning `{"status":"ok"}` checks endpoint reachability only.
2. Confirm that the MCP client loads tools. `shorturl_get_usage_guide` is a reference tool; it does not verify downstream API access or balance.
3. If you need a full API check, call `shorturl_create` with your own valid input after reviewing [current service documentation](https://platform.acedata.cloud/documents/short-url-mcp?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=shorturl_mcp_readme_quick_start) and displayed pricing.

For **401**, check which auth route the client used and whether the token or OAuth session is valid. A **403** may mean an account permission or content moderation failure; read the returned error. Insufficient balance and downstream service failures need their own diagnosis. A listed tool or submitted task does not prove a successful result.

## Available Tools

### URL Shortening Tools

| Tool                    | Description                            |
| ----------------------- | -------------------------------------- |
| `shorturl_create`       | Shorten a single URL                   |
| `shorturl_batch_create` | Shorten multiple URLs at once (max 10) |

### Information Tools

| Tool                       | Description                     |
| -------------------------- | ------------------------------- |
| `shorturl_get_usage_guide` | Get comprehensive usage guide   |
| `shorturl_get_api_info`    | Get API details and error codes |

## Usage Examples

### Shorten a Single URL

```
User: Shorten this URL: https://platform.acedata.cloud/documents/shorturl

Claude: I'll shorten that URL for you.
[Calls shorturl_create with url="https://platform.acedata.cloud/documents/shorturl"]

Result: https://surl.id/1uHCs01xa5
```

### Batch Shorten Multiple URLs

```
User: Shorten these URLs for my social media posts:
- https://example.com/blog/very-long-article-title-about-ai
- https://example.com/products/new-release-2024

Claude: I'll shorten both URLs at once.
[Calls shorturl_batch_create with urls=[...]]
```

### Create Links for Documentation

```
User: I need clean short links for these reference URLs in my doc.

Claude: I'll create short links for all your references.
[Calls shorturl_batch_create with the list of URLs]
```

## Response Structure

### Successful Response

```json
{
  "success": true,
  "data": {
    "url": "https://surl.id/1uHCs01xa5"
  }
}
```

### Error Response

```json
{
  "success": false,
  "error": {
    "code": "api_error",
    "message": "fetch failed"
  },
  "trace_id": "2cf86e86-22a4-46e1-ac2f-032c0f2a4e89"
}
```

## Configuration

### Environment Variables

| Variable                    | Description                 | Default                     |
| --------------------------- | --------------------------- | --------------------------- |
| `ACEDATACLOUD_API_TOKEN`    | API token from AceDataCloud | **Required**                |
| `ACEDATACLOUD_API_BASE_URL` | API base URL                | `https://api.acedata.cloud` |
| `ACEDATACLOUD_OAUTH_CLIENT_ID`  | OAuth client ID (hosted mode) | —                           |
| `ACEDATACLOUD_PLATFORM_BASE_URL` | Platform base URL            | `https://platform.acedata.cloud` |
| `SHORTURL_REQUEST_TIMEOUT`  | Request timeout in seconds  | `30`                        |
| `LOG_LEVEL`                 | Logging level               | `INFO`                      |

### Command Line Options

```bash
mcp-shorturl --help

Options:
  --version          Show version
  --transport        Transport mode: stdio (default) or http
  --port             Port for HTTP transport (default: 8000)
```

## Development

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/AceDataCloud/ShortURLMCP.git
cd ShortURLMCP

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
ShortURLMCP/
├── core/                   # Core modules
│   ├── __init__.py
│   ├── client.py          # HTTP client for ShortURL API
│   ├── config.py          # Configuration management
│   ├── exceptions.py      # Custom exceptions
│   └── server.py          # MCP server initialization
├── tools/                  # MCP tool definitions
│   ├── __init__.py
│   ├── shorturl_tools.py  # URL shortening tools
│   └── info_tools.py      # Information tools
├── prompts/                # MCP prompt templates
│   └── __init__.py
├── tests/                  # Test suite
│   ├── conftest.py
│   ├── test_client.py
│   ├── test_config.py
│   └── test_integration.py
├── deploy/                 # Deployment configs
│   ├── run.sh
│   └── production/
│       ├── deployment.yaml
│       ├── ingress.yaml
│       └── service.yaml
├── .env.example           # Environment template
├── .gitignore
├── .ruff.toml             # Ruff linter configuration
├── CHANGELOG.md
├── Dockerfile             # Docker image for HTTP mode
├── docker-compose.yaml    # Docker Compose config
├── LICENSE
├── main.py                # Entry point
├── pyproject.toml         # Project configuration
└── README.md
```

## API Reference

This server wraps the [AceDataCloud Short URL API](https://platform.acedata.cloud/documents/shorturl?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=shorturl_mcp_readme_documents_shorturl):

- **Endpoint**: `POST /shorturl`
- **Input**: `{ "content": "https://long-url.example.com/..." }`
- **Output**: `{ "success": true, "data": { "url": "https://surl.id/..." } }`
- **Pricing**: Free (0 credits)
- **Auth**: Bearer token

Full API documentation: [AceDataCloud Platform](https://platform.acedata.cloud/documents/shorturl?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=shorturl_mcp_readme_documents_shorturl)

## Documentation

<!-- canonical-documentation -->
[Documentation](https://platform.acedata.cloud/documents/short-url-mcp?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=shorturl_mcp_readme_quick_start)

## License

MIT License - see [LICENSE](LICENSE) for details.
