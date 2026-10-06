# LumaMCP

<!-- mcp-name: io.github.AceDataCloud/mcp-luma -->

[![PyPI version](https://img.shields.io/pypi/v/mcp-luma.svg)](https://pypi.org/project/mcp-luma/)
[![PyPI downloads](https://img.shields.io/pypi/dm/mcp-luma.svg)](https://pypi.org/project/mcp-luma/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![MCP](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io)

A [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server for AI video generation using [Luma Dream Machine](https://lumalabs.ai/dream-machine) through the [AceDataCloud API](https://platform.acedata.cloud?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=luma_mcp_readme_platform).

Generate AI videos directly from Claude, VS Code, or any MCP-compatible client.

## Features

- **Text to Video** - Create AI-generated videos from text prompts
- **Image to Video** - Animate images with start/end frame control
- **Video Extension** - Extend existing videos with additional content
- **Multiple Aspect Ratios** - Support for 16:9, 9:16, 1:1, and more
- **Loop Videos** - Create seamlessly looping animations
- **Clarity Enhancement** - Optional video quality enhancement
- **Task Tracking** - Monitor generation progress and retrieve results

## Tool Reference

| Tool | Description |
|------|-------------|
| `luma_generate_video` | Generate AI video from a text prompt using Luma Dream Machine. |
| `luma_generate_video_from_image` | Generate AI video using reference images as start and/or end frames. |
| `luma_extend_video` | Extend an existing video with additional content. |
| `luma_extend_video_from_url` | Extend an existing video using its URL. |
| `luma_get_task` | Query the status and result of a video generation task. |
| `luma_get_tasks_batch` | Query multiple video generation tasks at once. |
| `luma_list_aspect_ratios` | List all available aspect ratios for Luma video generation. |
| `luma_list_actions` | List all available Luma API actions and corresponding tools. |

## Connect: hosted OAuth, API token, or local stdio

The hosted endpoint is `https://luma.mcp.acedata.cloud/mcp`. Choose one route for the MCP client:

| Route | When to use it | Credential setup |
|---|---|---|
| Hosted OAuth | The client supports remote MCP OAuth | Add only the URL, then sign in to AceDataCloud and approve access. No token needs to be pasted into client configuration. |
| Hosted API token | The client cannot finish OAuth, or you need an explicit integration credential | Send an AceDataCloud API token in the `Authorization: Bearer …` header. Keep it in a local secret store or environment variable. |
| Local stdio | The client runs a local MCP process | Install `mcp-luma` and pass `ACEDATACLOUD_API_TOKEN` to that process. It still calls the AceDataCloud API. |

The hosted service advertises OAuth metadata and Dynamic Client Registration (DCR). **DCR registers the client application; it is not an API key.** OAuth signs you in and the client sends the resulting Bearer token; it may reuse or create an API credential for the account. Browser sign-in still requires an AceDataCloud account. The hosted service can be metered: review [current service documentation](https://platform.acedata.cloud/documents/luma-mcp?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=luma_mcp_readme_quick_start) and displayed pricing before a real operation. Do not configure both an OAuth login and a fixed `Authorization` header for the same server.

### Hosted OAuth examples

- **Claude and Claude Desktop chat:** Add a remote custom connector in `Customize → Connectors → Add custom connector`, enter `https://luma.mcp.acedata.cloud/mcp`, select sign-in, and choose **Register automatically** if Claude asks how to register its OAuth client. Complete consent. Claude Desktop's local `claude_desktop_config.json` is a separate setup. [Claude connector guide](https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp).
- **Claude Code:** `claude mcp add --transport http --scope user luma https://luma.mcp.acedata.cloud/mcp`, then `claude mcp login luma`. Check `/mcp`. [Claude Code MCP guide](https://code.claude.com/docs/en/mcp).
- **Cursor:** Add a remote server with only `https://luma.mcp.acedata.cloud/mcp`. For a project, merge the entry below into `<project>/.cursor/mcp.json`; for personal use, use `~/.cursor/mcp.json`. [Cursor MCP guide](https://cursor.com/docs/mcp).
- **VS Code / Copilot:** Run **MCP: Add Server**, select HTTP, enter `https://luma.mcp.acedata.cloud/mcp`, then finish the browser sign-in. New portable workspace configs use `<project>/.mcp.json`; the VS Code-specific format below uses `<project>/.vscode/mcp.json` or the user profile. Check **MCP: List Servers**. [VS Code MCP setup](https://code.visualstudio.com/docs/agent-customization/mcp-servers).
- **Codex:** `codex mcp add luma --url https://luma.mcp.acedata.cloud/mcp`, then `codex mcp login luma`. Its user settings are in `~/.codex/config.toml`. [Official Codex MCP guide](https://developers.openai.com/codex/mcp/).

Cursor project config (OAuth):

```json
{
  "mcpServers": {
    "luma": {"url": "https://luma.mcp.acedata.cloud/mcp"}
  }
}
```

VS Code-specific workspace config (OAuth):

```json
{
  "servers": {
    "luma": {"type": "http", "url": "https://luma.mcp.acedata.cloud/mcp"}
  }
}
```

### Hosted API token

Sign in at [AceDataCloud Platform](https://platform.acedata.cloud?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=luma_mcp_readme_platform), open the [service page](https://platform.acedata.cloud/documents/luma-mcp?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=luma_mcp_readme_quick_start), and obtain an API credential. A fixed Bearer header is useful when your client lacks OAuth; an invalid header does not fall back to OAuth in Claude Code. The header value is sensitive, so keep it out of committed files and screenshots.

For Claude Code, the shell expands the token when you add the server; treat the saved user MCP config as a secret:

```bash
export ACEDATACLOUD_API_TOKEN='YOUR_API_TOKEN'
claude mcp add --transport http --scope user luma https://luma.mcp.acedata.cloud/mcp \
  --header "Authorization: Bearer $ACEDATACLOUD_API_TOKEN"
```

For a Claude Code project config, put a variable reference in `<project>/.mcp.json` and set that variable in the environment that launches Claude Code:

```json
{
  "mcpServers": {
    "luma": {
      "type": "http",
      "url": "https://luma.mcp.acedata.cloud/mcp",
      "headers": {"Authorization": "Bearer ${ACEDATACLOUD_API_TOKEN}"}
    }
  }
}
```

Cursor uses a different environment-variable syntax in `~/.cursor/mcp.json` or an uncommitted project config:

```json
{
  "mcpServers": {
    "luma": {
      "url": "https://luma.mcp.acedata.cloud/mcp",
      "headers": {"Authorization": "Bearer ${env:ACEDATACLOUD_API_TOKEN}"}
    }
  }
}
```

In VS Code, run **MCP: Open User Configuration** and merge this server plus its masked input; `${input:...}` is for VS Code's user/workspace format and is not portable to the Agent Host `.mcp.json` format:

```json
{
  "inputs": [
    {"id": "acedata-luma-token", "type": "promptString", "description": "AceDataCloud API token", "password": true}
  ],
  "servers": {
    "luma": {
      "type": "http",
      "url": "https://luma.mcp.acedata.cloud/mcp",
      "headers": {"Authorization": "Bearer ${input:acedata-luma-token}"}
    }
  }
}
```

For **Cline**, use its MCP configuration UI or CLI file `~/.cline/data/settings/cline_mcp_settings.json`; its remote transport value is `streamableHttp`. For **JetBrains AI Assistant**, add a remote URL from **Settings → Tools → AI Assistant → Model Context Protocol (MCP)**. For **Zed**, use a `context_servers` entry with the URL only for OAuth or add a local Bearer header. These clients have different configuration schemas; follow their current UI rather than copying another client's JSON. [Cline](https://docs.cline.bot/mcp/mcp-overview) · [JetBrains](https://www.jetbrains.com/help/ai-assistant/mcp.html) · [Zed](https://zed.dev/docs/ai/mcp).

### Local stdio

Install the package and give the local process an API token:

```bash
python -m pip install mcp-luma
export ACEDATACLOUD_API_TOKEN='YOUR_API_TOKEN'
mcp-luma
```

For Claude Desktop local MCP, merge this entry into the file opened by its developer settings (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS). `uvx` requires [uv](https://docs.astral.sh/uv/) on `PATH`:

```json
{
  "mcpServers": {
    "luma": {
      "command": "uvx",
      "args": ["mcp-luma"],
      "env": {"ACEDATACLOUD_API_TOKEN": "YOUR_API_TOKEN"}
    }
  }
}
```

Keep this user-level file private. Self-hosted HTTP uses `mcp-luma --transport http --port 8000`; expose it only with suitable network and TLS controls. Local execution still calls the AceDataCloud API.

### Check before using the service

1. `https://luma.mcp.acedata.cloud/health` returning `{"status":"ok"}` checks endpoint reachability only.
2. Confirm that the MCP client loads tools. `luma_list_actions` is a reference tool; it does not verify downstream API access or balance.
3. If you need a full API check, call `luma_generate_video` with your own valid input after reviewing [current service documentation](https://platform.acedata.cloud/documents/luma-mcp?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=luma_mcp_readme_quick_start) and displayed pricing. If the result contains a task ID, call `luma_get_task` on that same ID until terminal success or failure. Do not resubmit the operation just to check progress.

For **401**, check which auth route the client used and whether the token or OAuth session is valid. A **403** may mean an account permission or content moderation failure; read the returned error. Insufficient balance and downstream service failures need their own diagnosis. A listed tool or submitted task does not prove a successful result.

## Available Tools

### Video Generation

| Tool                             | Description                           |
| -------------------------------- | ------------------------------------- |
| `luma_generate_video`            | Generate video from a text prompt     |
| `luma_generate_video_from_image` | Generate video using reference images |
| `luma_extend_video`              | Extend an existing video by ID        |
| `luma_extend_video_from_url`     | Extend an existing video by URL       |

### Tasks

| Tool                   | Description                  |
| ---------------------- | ---------------------------- |
| `luma_get_task`        | Query a single task status   |
| `luma_get_tasks_batch` | Query multiple tasks at once |

### Information

| Tool                      | Description                  |
| ------------------------- | ---------------------------- |
| `luma_list_aspect_ratios` | List available aspect ratios |
| `luma_list_actions`       | List available API actions   |

## Usage Examples

### Generate Video from Prompt

```
User: Create a video of waves on a beach

Claude: I'll generate a beach wave video for you.
[Calls luma_generate_video with prompt="Ocean waves gently crashing on sandy beach, sunset"]
```

### Animate an Image

```
User: Animate this image: https://example.com/image.jpg

Claude: I'll create a video from your image.
[Calls luma_generate_video_from_image with start_image_url and appropriate prompt]
```

### Extend a Video

```
User: Continue this video with more action

Claude: I'll extend the video with additional content.
[Calls luma_extend_video with video_id and new prompt]
```

## Available Aspect Ratios

| Aspect Ratio | Description          | Use Case                   |
| ------------ | -------------------- | -------------------------- |
| `16:9`       | Landscape (default)  | YouTube, TV, presentations |
| `9:16`       | Portrait             | TikTok, Instagram Reels    |
| `1:1`        | Square               | Instagram posts            |
| `4:3`        | Traditional          | Classic video format       |
| `3:4`        | Portrait traditional | Portrait content           |
| `21:9`       | Ultrawide            | Cinematic content          |
| `9:21`       | Tall ultrawide       | Special vertical displays  |

## Configuration

### Environment Variables

| Variable                    | Description                 | Default                     |
| --------------------------- | --------------------------- | --------------------------- |
| `ACEDATACLOUD_API_TOKEN`    | API token from AceDataCloud | **Required**                |
| `ACEDATACLOUD_API_BASE_URL` | API base URL                | `https://api.acedata.cloud` |
| `ACEDATACLOUD_OAUTH_CLIENT_ID`  | OAuth client ID (hosted mode) | —                           |
| `ACEDATACLOUD_PLATFORM_BASE_URL` | Platform base URL            | `https://platform.acedata.cloud` |
| `LUMA_DEFAULT_ASPECT_RATIO` | Default aspect ratio        | `16:9`                      |
| `LUMA_REQUEST_TIMEOUT`      | Request timeout in seconds  | `1800`                      |
| `LOG_LEVEL`                 | Logging level               | `INFO`                      |

### Command Line Options

```bash
mcp-luma --help

Options:
  --version          Show version
  --transport        Transport mode: stdio (default) or http
  --port             Port for HTTP transport (default: 8000)
```

## Development

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/AceDataCloud/LumaMCP.git
cd LumaMCP

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
LumaMCP/
├── core/                   # Core modules
│   ├── __init__.py
│   ├── client.py          # HTTP client for Luma API
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

This server wraps the [AceDataCloud Luma API](https://platform.acedata.cloud/documents/luma-videos?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=luma_mcp_readme_documents_luma-videos):

- [Luma Videos API](https://platform.acedata.cloud/documents/luma-videos?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=luma_mcp_readme_documents_luma-videos) - Video generation
- [Luma Tasks API](https://platform.acedata.cloud/documents/luma-tasks?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=luma_mcp_readme_documents_luma-tasks) - Task queries

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing`)
5. Open a Pull Request

## Documentation

<!-- canonical-documentation -->
[Documentation](https://platform.acedata.cloud/documents/luma-mcp?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=luma_mcp_readme_quick_start)

## License

MIT License - see [LICENSE](LICENSE) for details.

## Links

- [AceDataCloud Platform](https://platform.acedata.cloud?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=luma_mcp_readme_platform)
- [Luma Dream Machine](https://lumalabs.ai/dream-machine)
- [Model Context Protocol](https://modelcontextprotocol.io)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)

---

Made with love by [AceDataCloud](https://platform.acedata.cloud?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=luma_mcp_readme_platform)
