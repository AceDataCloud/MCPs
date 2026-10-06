# KlingMCP

<!-- mcp-name: io.github.AceDataCloud/mcp-kling -->

[![PyPI version](https://img.shields.io/pypi/v/mcp-kling.svg)](https://pypi.org/project/mcp-kling/)
[![PyPI downloads](https://img.shields.io/pypi/dm/mcp-kling.svg)](https://pypi.org/project/mcp-kling/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![MCP](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io)

A [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server for AI video generation using [Kling](https://klingai.com/) through the [AceDataCloud API](https://platform.acedata.cloud?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=kling_mcp_readme_platform).

Generate AI videos, extend clips, and transfer motion directly from Claude, VS Code, or any MCP-compatible client.

## Features

- **Text to Video** - Create AI-generated videos from text prompts
- **Image to Video** - Generate videos using reference start/end images
- **Video Extension** - Extend existing videos with additional content
- **Motion Transfer** - Transfer motion from a reference video to a character image
- **Multiple Models** - Support for 9 Kling models, including V3, V3 Omni, and canonical Kling O1
- **Camera Control** - Fine-grained camera movement control
- **Task Tracking** - Monitor generation progress and retrieve results

## Tool Reference

| Tool | Description |
|------|-------------|
| `kling_generate_video` | Generate AI video from a text prompt using Kling. |
| `kling_generate_video_from_image` | Generate AI video using reference images as start and/or end frames. |
| `kling_extend_video` | Extend an existing video with additional content. |
| `kling_generate_motion` | Transfer motion from a reference video to a character image. |
| `kling_get_task` | Query the status and result of a video generation task. |
| `kling_get_tasks_batch` | Query multiple video generation tasks at once. |
| `kling_list_models` | List all available Kling models for video generation. |
| `kling_list_actions` | List all available Kling API actions and corresponding tools. |

## Connect: hosted OAuth, API token, or local stdio

The hosted endpoint is `https://kling.mcp.acedata.cloud/mcp`. Choose one route for the MCP client:

| Route | When to use it | Credential setup |
|---|---|---|
| Hosted OAuth | The client supports remote MCP OAuth | Add only the URL, then sign in to AceDataCloud and approve access. No token needs to be pasted into client configuration. |
| Hosted API token | The client cannot finish OAuth, or you need an explicit integration credential | Send an AceDataCloud API token in the `Authorization: Bearer …` header. Keep it in a local secret store or environment variable. |
| Local stdio | The client runs a local MCP process | Install `mcp-kling` and pass `ACEDATACLOUD_API_TOKEN` to that process. It still calls the AceDataCloud API. |

The hosted service advertises OAuth metadata and Dynamic Client Registration (DCR). **DCR registers the client application; it is not an API key.** OAuth signs you in and the client sends the resulting Bearer token; it may reuse or create an API credential for the account. Browser sign-in still requires an AceDataCloud account. The hosted service can be metered: review [current service documentation](https://platform.acedata.cloud/documents/kling?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=kling_mcp_readme_quick_start) and displayed pricing before a real operation. Do not configure both an OAuth login and a fixed `Authorization` header for the same server.

### Hosted OAuth examples

- **Claude and Claude Desktop chat:** Add a remote custom connector in `Customize → Connectors → Add custom connector`, enter `https://kling.mcp.acedata.cloud/mcp`, select sign-in, and choose **Register automatically** if Claude asks how to register its OAuth client. Complete consent. Claude Desktop's local `claude_desktop_config.json` is a separate setup. [Claude connector guide](https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp).
- **Claude Code:** `claude mcp add --transport http --scope user kling https://kling.mcp.acedata.cloud/mcp`, then `claude mcp login kling`. Check `/mcp`. [Claude Code MCP guide](https://code.claude.com/docs/en/mcp).
- **Cursor:** Add a remote server with only `https://kling.mcp.acedata.cloud/mcp`. For a project, merge the entry below into `<project>/.cursor/mcp.json`; for personal use, use `~/.cursor/mcp.json`. [Cursor MCP guide](https://cursor.com/docs/mcp).
- **VS Code / Copilot:** Run **MCP: Add Server**, select HTTP, enter `https://kling.mcp.acedata.cloud/mcp`, then finish the browser sign-in. New portable workspace configs use `<project>/.mcp.json`; the VS Code-specific format below uses `<project>/.vscode/mcp.json` or the user profile. Check **MCP: List Servers**. [VS Code MCP setup](https://code.visualstudio.com/docs/agent-customization/mcp-servers).
- **Codex:** `codex mcp add kling --url https://kling.mcp.acedata.cloud/mcp`, then `codex mcp login kling`. Its user settings are in `~/.codex/config.toml`. [Official Codex MCP guide](https://developers.openai.com/codex/mcp/).

Cursor project config (OAuth):

```json
{
  "mcpServers": {
    "kling": {"url": "https://kling.mcp.acedata.cloud/mcp"}
  }
}
```

VS Code-specific workspace config (OAuth):

```json
{
  "servers": {
    "kling": {"type": "http", "url": "https://kling.mcp.acedata.cloud/mcp"}
  }
}
```

### Hosted API token

Sign in at [AceDataCloud Platform](https://platform.acedata.cloud?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=kling_mcp_readme_platform), open the [service page](https://platform.acedata.cloud/documents/kling?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=kling_mcp_readme_quick_start), and obtain an API credential. A fixed Bearer header is useful when your client lacks OAuth; an invalid header does not fall back to OAuth in Claude Code. The header value is sensitive, so keep it out of committed files and screenshots.

For Claude Code, the shell expands the token when you add the server; treat the saved user MCP config as a secret:

```bash
export ACEDATACLOUD_API_TOKEN='YOUR_API_TOKEN'
claude mcp add --transport http --scope user kling https://kling.mcp.acedata.cloud/mcp \
  --header "Authorization: Bearer $ACEDATACLOUD_API_TOKEN"
```

For a Claude Code project config, put a variable reference in `<project>/.mcp.json` and set that variable in the environment that launches Claude Code:

```json
{
  "mcpServers": {
    "kling": {
      "type": "http",
      "url": "https://kling.mcp.acedata.cloud/mcp",
      "headers": {"Authorization": "Bearer ${ACEDATACLOUD_API_TOKEN}"}
    }
  }
}
```

Cursor uses a different environment-variable syntax in `~/.cursor/mcp.json` or an uncommitted project config:

```json
{
  "mcpServers": {
    "kling": {
      "url": "https://kling.mcp.acedata.cloud/mcp",
      "headers": {"Authorization": "Bearer ${env:ACEDATACLOUD_API_TOKEN}"}
    }
  }
}
```

In VS Code, run **MCP: Open User Configuration** and merge this server plus its masked input; `${input:...}` is for VS Code's user/workspace format and is not portable to the Agent Host `.mcp.json` format:

```json
{
  "inputs": [
    {"id": "acedata-kling-token", "type": "promptString", "description": "AceDataCloud API token", "password": true}
  ],
  "servers": {
    "kling": {
      "type": "http",
      "url": "https://kling.mcp.acedata.cloud/mcp",
      "headers": {"Authorization": "Bearer ${input:acedata-kling-token}"}
    }
  }
}
```

For **Cline**, use its MCP configuration UI or CLI file `~/.cline/data/settings/cline_mcp_settings.json`; its remote transport value is `streamableHttp`. For **JetBrains AI Assistant**, add a remote URL from **Settings → Tools → AI Assistant → Model Context Protocol (MCP)**. For **Zed**, use a `context_servers` entry with the URL only for OAuth or add a local Bearer header. These clients have different configuration schemas; follow their current UI rather than copying another client's JSON. [Cline](https://docs.cline.bot/mcp/mcp-overview) · [JetBrains](https://www.jetbrains.com/help/ai-assistant/mcp.html) · [Zed](https://zed.dev/docs/ai/mcp).

### Local stdio

Install the package and give the local process an API token:

```bash
python -m pip install mcp-kling
export ACEDATACLOUD_API_TOKEN='YOUR_API_TOKEN'
mcp-kling
```

For Claude Desktop local MCP, merge this entry into the file opened by its developer settings (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS). `uvx` requires [uv](https://docs.astral.sh/uv/) on `PATH`:

```json
{
  "mcpServers": {
    "kling": {
      "command": "uvx",
      "args": ["mcp-kling"],
      "env": {"ACEDATACLOUD_API_TOKEN": "YOUR_API_TOKEN"}
    }
  }
}
```

Keep this user-level file private. Self-hosted HTTP uses `mcp-kling --transport http --port 8000`; expose it only with suitable network and TLS controls. Local execution still calls the AceDataCloud API.

### Check before using the service

1. `https://kling.mcp.acedata.cloud/health` returning `{"status":"ok"}` checks endpoint reachability only.
2. Confirm that the MCP client loads tools. `kling_list_models` is a reference tool; it does not verify downstream API access or balance.
3. If you need a full API check, call `kling_generate_video` with your own valid input after reviewing [current service documentation](https://platform.acedata.cloud/documents/kling?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=kling_mcp_readme_quick_start) and displayed pricing. If the result contains a task ID, call `kling_get_task` on that same ID until terminal success or failure. Do not resubmit the operation just to check progress.

For **401**, check which auth route the client used and whether the token or OAuth session is valid. A **403** may mean an account permission or content moderation failure; read the returned error. Insufficient balance and downstream service failures need their own diagnosis. A listed tool or submitted task does not prove a successful result.

## Available Models

| Model              | Description          | Use Case                            |
| ------------------ | -------------------- | ----------------------------------- |
| `kling-v1`         | First generation     | Basic video generation              |
| `kling-v1-6`       | V1 extended          | Improved quality over v1            |
| `kling-v2-master`  | V2 master (default)  | High-quality, balanced performance  |
| `kling-v2-1-master`| V2.1 master          | Enhanced quality and consistency    |
| `kling-v2-5-turbo` | V2.5 turbo           | Faster generation, good quality     |
| `kling-o1`         | Kling O1             | Omni image/video reference generation |

## Configuration

### Environment Variables

| Variable                    | Description                 | Default                     |
| --------------------------- | --------------------------- | --------------------------- |
| `ACEDATACLOUD_API_TOKEN`    | API token from AceDataCloud | **Required**                |
| `ACEDATACLOUD_API_BASE_URL` | API base URL                | `https://api.acedata.cloud` |
| `KLING_DEFAULT_MODEL`       | Default video model         | `kling-v2-master`           |
| `KLING_DEFAULT_MODE`        | Default generation mode     | `std`                       |
| `KLING_DEFAULT_ASPECT_RATIO`| Default aspect ratio        | `16:9`                      |
| `KLING_REQUEST_TIMEOUT`     | Request timeout in seconds  | `300`                       |
| `LOG_LEVEL`                 | Logging level               | `INFO`                      |

### Command Line Options

```bash
mcp-kling --help

Options:
  --version          Show version
  --transport        Transport mode: stdio (default) or http
  --port             Port for HTTP transport (default: 8000)
```

## Development

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/AceDataCloud/KlingMCP.git
cd KlingMCP

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
KlingMCP/
├── core/                   # Core modules
│   ├── __init__.py
│   ├── client.py          # HTTP client for Kling API
│   ├── config.py          # Configuration management
│   ├── exceptions.py      # Custom exceptions
│   ├── oauth.py           # OAuth 2.1 provider
│   ├── server.py          # MCP server initialization
│   ├── types.py           # Type definitions
│   └── utils.py           # Utility functions
├── tools/                  # MCP tool definitions
│   ├── __init__.py
│   ├── video_tools.py     # Video generation tools
│   ├── motion_tools.py    # Motion transfer tools
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

This server wraps the AceDataCloud Kling API:

- Kling Videos API - Video generation (text2video, image2video, extend)
- Kling Motion API - Motion transfer
- Kling Tasks API - Task queries

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing`)
5. Open a Pull Request

## Documentation

<!-- canonical-documentation -->
[Documentation](https://platform.acedata.cloud/documents/kling?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=kling_mcp_readme_quick_start)

## License

MIT License - see [LICENSE](LICENSE) for details.

## Links

- [AceDataCloud Platform](https://platform.acedata.cloud?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=kling_mcp_readme_platform)
- [Kling AI](https://klingai.com/)
- [Model Context Protocol](https://modelcontextprotocol.io)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)

---

Made with love by [AceDataCloud](https://platform.acedata.cloud?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=kling_mcp_readme_platform)

## Turbo, storyboards and commerce

Use `kling_generate_turbo_video` for V3 Turbo (std 720p / pro 1080p, integer 3–15 seconds). Native audio is included and cannot be disabled. Tail frames, standalone negative prompts, cfg_scale, camera controls and Omni references are unsupported.

Use `kling_generate_storyboard` for V3/V3 Omni multishot generation: `shot_type="intelligence"` uses a prompt; `customize` takes 1–6 indexed `multi_prompt` shots whose durations sum to the total. For example: `{"shot_type":"customize","duration":5,"multi_prompt":[{"index":1,"prompt":"Ocean","duration":2},{"index":2,"prompt":"Beach","duration":3}]}`.

Public commerce tools are `kling_goods_studio` and `kling_video_commerce`. Both accept a structured request and return a task ID for `kling_get_task`.

## Reference inputs

Use `element_list` and `voice_list` only with already valid platform references and the supported model combinations in the current backend guide. Standalone asset creation and management are not published.
