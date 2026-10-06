# WanMCP

<!-- mcp-name: io.github.AceDataCloud/mcp-wan -->

[![PyPI version](https://img.shields.io/pypi/v/mcp-wan.svg)](https://pypi.org/project/mcp-wan/)
[![PyPI downloads](https://img.shields.io/pypi/dm/mcp-wan.svg)](https://pypi.org/project/mcp-wan/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![MCP](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io)

A [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server for AI video generation using [Wan](https://wanx.aliyun.com/) through the [AceDataCloud API](https://platform.acedata.cloud?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=wan_mcp_readme_platform).

Generate AI videos from text or images directly from Claude, VS Code, or any MCP-compatible client.

## Features

- **Text to Video** - Create AI-generated videos from text prompts
- **Image to Video** - Generate videos using reference images
- **Multiple Models** - Support for 5 Wan models (wan2.6-t2v, wan2.6-i2v, wan2.6-r2v, wan2.6-i2v-flash, wan3.0-video)
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

## Connect: hosted OAuth, API token, or local stdio

The hosted endpoint is `https://wan.mcp.acedata.cloud/mcp`. Choose one route for the MCP client:

| Route | When to use it | Credential setup |
|---|---|---|
| Hosted OAuth | The client supports remote MCP OAuth | Add only the URL, then sign in to AceDataCloud and approve access. No token needs to be pasted into client configuration. |
| Hosted API token | The client cannot finish OAuth, or you need an explicit integration credential | Send an AceDataCloud API token in the `Authorization: Bearer …` header. Keep it in a local secret store or environment variable. |
| Local stdio | The client runs a local MCP process | Install `mcp-wan` and pass `ACEDATACLOUD_API_TOKEN` to that process. It still calls the AceDataCloud API. |

The hosted service advertises OAuth metadata and Dynamic Client Registration (DCR). **DCR registers the client application; it is not an API key.** OAuth signs you in and the client sends the resulting Bearer token; it may reuse or create an API credential for the account. Browser sign-in still requires an AceDataCloud account. The hosted service can be metered: review [current service documentation](https://platform.acedata.cloud/documents/wan?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=wan_mcp_readme_quick_start) and displayed pricing before a real operation. Do not configure both an OAuth login and a fixed `Authorization` header for the same server.

### Hosted OAuth examples

- **Claude and Claude Desktop chat:** Add a remote custom connector in `Customize → Connectors → Add custom connector`, enter `https://wan.mcp.acedata.cloud/mcp`, select sign-in, and choose **Register automatically** if Claude asks how to register its OAuth client. Complete consent. Claude Desktop's local `claude_desktop_config.json` is a separate setup. [Claude connector guide](https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp).
- **Claude Code:** `claude mcp add --transport http --scope user wan https://wan.mcp.acedata.cloud/mcp`, then `claude mcp login wan`. Check `/mcp`. [Claude Code MCP guide](https://code.claude.com/docs/en/mcp).
- **Cursor:** Add a remote server with only `https://wan.mcp.acedata.cloud/mcp`. For a project, merge the entry below into `<project>/.cursor/mcp.json`; for personal use, use `~/.cursor/mcp.json`. [Cursor MCP guide](https://cursor.com/docs/mcp).
- **VS Code / Copilot:** Run **MCP: Add Server**, select HTTP, enter `https://wan.mcp.acedata.cloud/mcp`, then finish the browser sign-in. New portable workspace configs use `<project>/.mcp.json`; the VS Code-specific format below uses `<project>/.vscode/mcp.json` or the user profile. Check **MCP: List Servers**. [VS Code MCP setup](https://code.visualstudio.com/docs/agent-customization/mcp-servers).
- **Codex:** `codex mcp add wan --url https://wan.mcp.acedata.cloud/mcp`, then `codex mcp login wan`. Its user settings are in `~/.codex/config.toml`. [Official Codex MCP guide](https://developers.openai.com/codex/mcp/).

Cursor project config (OAuth):

```json
{
  "mcpServers": {
    "wan": {"url": "https://wan.mcp.acedata.cloud/mcp"}
  }
}
```

VS Code-specific workspace config (OAuth):

```json
{
  "servers": {
    "wan": {"type": "http", "url": "https://wan.mcp.acedata.cloud/mcp"}
  }
}
```

### Hosted API token

Sign in at [AceDataCloud Platform](https://platform.acedata.cloud?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=wan_mcp_readme_platform), open the [service page](https://platform.acedata.cloud/documents/wan?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=wan_mcp_readme_quick_start), and obtain an API credential. A fixed Bearer header is useful when your client lacks OAuth; an invalid header does not fall back to OAuth in Claude Code. The header value is sensitive, so keep it out of committed files and screenshots.

For Claude Code, the shell expands the token when you add the server; treat the saved user MCP config as a secret:

```bash
export ACEDATACLOUD_API_TOKEN='YOUR_API_TOKEN'
claude mcp add --transport http --scope user wan https://wan.mcp.acedata.cloud/mcp \
  --header "Authorization: Bearer $ACEDATACLOUD_API_TOKEN"
```

For a Claude Code project config, put a variable reference in `<project>/.mcp.json` and set that variable in the environment that launches Claude Code:

```json
{
  "mcpServers": {
    "wan": {
      "type": "http",
      "url": "https://wan.mcp.acedata.cloud/mcp",
      "headers": {"Authorization": "Bearer ${ACEDATACLOUD_API_TOKEN}"}
    }
  }
}
```

Cursor uses a different environment-variable syntax in `~/.cursor/mcp.json` or an uncommitted project config:

```json
{
  "mcpServers": {
    "wan": {
      "url": "https://wan.mcp.acedata.cloud/mcp",
      "headers": {"Authorization": "Bearer ${env:ACEDATACLOUD_API_TOKEN}"}
    }
  }
}
```

In VS Code, run **MCP: Open User Configuration** and merge this server plus its masked input; `${input:...}` is for VS Code's user/workspace format and is not portable to the Agent Host `.mcp.json` format:

```json
{
  "inputs": [
    {"id": "acedata-wan-token", "type": "promptString", "description": "AceDataCloud API token", "password": true}
  ],
  "servers": {
    "wan": {
      "type": "http",
      "url": "https://wan.mcp.acedata.cloud/mcp",
      "headers": {"Authorization": "Bearer ${input:acedata-wan-token}"}
    }
  }
}
```

For **Cline**, use its MCP configuration UI or CLI file `~/.cline/data/settings/cline_mcp_settings.json`; its remote transport value is `streamableHttp`. For **JetBrains AI Assistant**, add a remote URL from **Settings → Tools → AI Assistant → Model Context Protocol (MCP)**. For **Zed**, use a `context_servers` entry with the URL only for OAuth or add a local Bearer header. These clients have different configuration schemas; follow their current UI rather than copying another client's JSON. [Cline](https://docs.cline.bot/mcp/mcp-overview) · [JetBrains](https://www.jetbrains.com/help/ai-assistant/mcp.html) · [Zed](https://zed.dev/docs/ai/mcp).

### Local stdio

Install the package and give the local process an API token:

```bash
python -m pip install mcp-wan
export ACEDATACLOUD_API_TOKEN='YOUR_API_TOKEN'
mcp-wan
```

For Claude Desktop local MCP, merge this entry into the file opened by its developer settings (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS). `uvx` requires [uv](https://docs.astral.sh/uv/) on `PATH`:

```json
{
  "mcpServers": {
    "wan": {
      "command": "uvx",
      "args": ["mcp-wan"],
      "env": {"ACEDATACLOUD_API_TOKEN": "YOUR_API_TOKEN"}
    }
  }
}
```

Keep this user-level file private. Self-hosted HTTP uses `mcp-wan --transport http --port 8000`; expose it only with suitable network and TLS controls. Local execution still calls the AceDataCloud API.

### Check before using the service

1. `https://wan.mcp.acedata.cloud/health` returning `{"status":"ok"}` checks endpoint reachability only.
2. Confirm that the MCP client loads tools. `wan_list_models` is a reference tool; it does not verify downstream API access or balance.
3. If you need a full API check, call `wan_generate_video` with your own valid input after reviewing [current service documentation](https://platform.acedata.cloud/documents/wan?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=wan_mcp_readme_quick_start) and displayed pricing. If the result contains a task ID, call `wan_get_task` on that same ID until terminal success or failure. Do not resubmit the operation just to check progress.

For **401**, check which auth route the client used and whether the token or OAuth session is valid. A **403** may mean an account permission or content moderation failure; read the returned error. Insufficient balance and downstream service failures need their own diagnosis. A listed tool or submitted task does not prove a successful result.

## Available Models

| Model              | Description               | Use Case                                |
| ------------------ | ------------------------- | --------------------------------------- |
| `wan2.6-t2v`       | Text to video             | Generate video from text prompts        |
| `wan2.6-i2v`       | Image to video            | Standard image-to-video generation      |
| `wan2.6-r2v`       | Reference video-to-video  | Character extraction and transfer       |
| `wan2.6-i2v-flash` | Fast image to video       | Quick preview, lower quality            |
| `wan3.0-video`     | Text to video             | Video generation with optional media    |

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

## Documentation

<!-- canonical-documentation -->
[Documentation](https://platform.acedata.cloud/documents/wan?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=wan_mcp_readme_quick_start)

## License

MIT License - see [LICENSE](LICENSE) for details.

## Links

- [AceDataCloud Platform](https://platform.acedata.cloud?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=wan_mcp_readme_platform)
- [Wan AI](https://wanx.aliyun.com/)
- [Model Context Protocol](https://modelcontextprotocol.io)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)

---

Made with love by [AceDataCloud](https://platform.acedata.cloud?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=wan_mcp_readme_platform)
