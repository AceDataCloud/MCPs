# NanoBananaMCP

<!-- mcp-name: io.github.AceDataCloud/mcp-nanobanana-pro -->

[![PyPI version](https://img.shields.io/pypi/v/mcp-nanobanana-pro.svg)](https://pypi.org/project/mcp-nanobanana-pro/)
[![PyPI downloads](https://img.shields.io/pypi/dm/mcp-nanobanana-pro.svg)](https://pypi.org/project/mcp-nanobanana-pro/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![MCP](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io)

A [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server for AI image generation and editing using [Google's Nano Banana](https://deepmind.google/technologies/imagen/) model through the [AceDataCloud API](https://platform.acedata.cloud?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=nanobanana_mcp_readme_platform).

Generate and edit AI images directly from Claude, VS Code, or any MCP-compatible client.

## Features

- **Image Generation** - Create high-quality images from text prompts
- **Image Editing** - Modify existing images or combine multiple images
- **Virtual Try-On** - Put clothing on people in photos
- **Product Placement** - Place products in realistic scenes
- **Task Tracking** - Monitor generation progress and retrieve results

## Tool Reference

| Tool | Description |
|------|-------------|
| `nanobanana_generate_image` | Generate an AI image from a text prompt using Google's Nano Banana model. |
| `nanobanana_edit_image` | Edit or combine images using AI based on a text prompt. |
| `nanobanana_get_task` | Query the status and result of an image generation or edit task. |
| `nanobanana_get_tasks_batch` | Query multiple image generation/edit tasks at once. |

## Connect: hosted OAuth, API token, or local stdio

The hosted endpoint is `https://nanobanana.mcp.acedata.cloud/mcp`. Choose one route for the MCP client:

| Route | When to use it | Credential setup |
|---|---|---|
| Hosted OAuth | The client supports remote MCP OAuth | Add only the URL, then sign in to AceDataCloud and approve access. No token needs to be pasted into client configuration. |
| Hosted API token | The client cannot finish OAuth, or you need an explicit integration credential | Send an AceDataCloud API token in the `Authorization: Bearer …` header. Keep it in a local secret store or environment variable. |
| Local stdio | The client runs a local MCP process | Install `mcp-nanobanana-pro` and pass `ACEDATACLOUD_API_TOKEN` to that process. It still calls the AceDataCloud API. |

The hosted service advertises OAuth metadata and Dynamic Client Registration (DCR). **DCR registers the client application; it is not an API key.** OAuth signs you in and the client sends the resulting Bearer token; it may reuse or create an API credential for the account. Browser sign-in still requires an AceDataCloud account. The hosted service can be metered: review [current service documentation](https://platform.acedata.cloud/documents/nano-banana-mcp?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=nanobanana_mcp_readme_quick_start) and displayed pricing before a real operation. Do not configure both an OAuth login and a fixed `Authorization` header for the same server.

### Hosted OAuth examples

- **Claude and Claude Desktop chat:** Add a remote custom connector in `Customize → Connectors → Add custom connector`, enter `https://nanobanana.mcp.acedata.cloud/mcp`, select sign-in, and choose **Register automatically** if Claude asks how to register its OAuth client. Complete consent. Claude Desktop's local `claude_desktop_config.json` is a separate setup. [Claude connector guide](https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp).
- **Claude Code:** `claude mcp add --transport http --scope user nanobanana https://nanobanana.mcp.acedata.cloud/mcp`, then `claude mcp login nanobanana`. Check `/mcp`. [Claude Code MCP guide](https://code.claude.com/docs/en/mcp).
- **Cursor:** Add a remote server with only `https://nanobanana.mcp.acedata.cloud/mcp`. For a project, merge the entry below into `<project>/.cursor/mcp.json`; for personal use, use `~/.cursor/mcp.json`. [Cursor MCP guide](https://cursor.com/docs/mcp).
- **VS Code / Copilot:** Run **MCP: Add Server**, select HTTP, enter `https://nanobanana.mcp.acedata.cloud/mcp`, then finish the browser sign-in. New portable workspace configs use `<project>/.mcp.json`; the VS Code-specific format below uses `<project>/.vscode/mcp.json` or the user profile. Check **MCP: List Servers**. [VS Code MCP setup](https://code.visualstudio.com/docs/agent-customization/mcp-servers).
- **Codex:** `codex mcp add nanobanana --url https://nanobanana.mcp.acedata.cloud/mcp`, then `codex mcp login nanobanana`. Its user settings are in `~/.codex/config.toml`. [Official Codex MCP guide](https://developers.openai.com/codex/mcp/).

Cursor project config (OAuth):

```json
{
  "mcpServers": {
    "nanobanana": {"url": "https://nanobanana.mcp.acedata.cloud/mcp"}
  }
}
```

VS Code-specific workspace config (OAuth):

```json
{
  "servers": {
    "nanobanana": {"type": "http", "url": "https://nanobanana.mcp.acedata.cloud/mcp"}
  }
}
```

### Hosted API token

Sign in at [AceDataCloud Platform](https://platform.acedata.cloud?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=nanobanana_mcp_readme_platform), open the [service page](https://platform.acedata.cloud/documents/nano-banana-mcp?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=nanobanana_mcp_readme_quick_start), and obtain an API credential. A fixed Bearer header is useful when your client lacks OAuth; an invalid header does not fall back to OAuth in Claude Code. The header value is sensitive, so keep it out of committed files and screenshots.

For Claude Code, the shell expands the token when you add the server; treat the saved user MCP config as a secret:

```bash
export ACEDATACLOUD_API_TOKEN='YOUR_API_TOKEN'
claude mcp add --transport http --scope user nanobanana https://nanobanana.mcp.acedata.cloud/mcp \
  --header "Authorization: Bearer $ACEDATACLOUD_API_TOKEN"
```

For a Claude Code project config, put a variable reference in `<project>/.mcp.json` and set that variable in the environment that launches Claude Code:

```json
{
  "mcpServers": {
    "nanobanana": {
      "type": "http",
      "url": "https://nanobanana.mcp.acedata.cloud/mcp",
      "headers": {"Authorization": "Bearer ${ACEDATACLOUD_API_TOKEN}"}
    }
  }
}
```

Cursor uses a different environment-variable syntax in `~/.cursor/mcp.json` or an uncommitted project config:

```json
{
  "mcpServers": {
    "nanobanana": {
      "url": "https://nanobanana.mcp.acedata.cloud/mcp",
      "headers": {"Authorization": "Bearer ${env:ACEDATACLOUD_API_TOKEN}"}
    }
  }
}
```

In VS Code, run **MCP: Open User Configuration** and merge this server plus its masked input; `${input:...}` is for VS Code's user/workspace format and is not portable to the Agent Host `.mcp.json` format:

```json
{
  "inputs": [
    {"id": "acedata-nanobanana-token", "type": "promptString", "description": "AceDataCloud API token", "password": true}
  ],
  "servers": {
    "nanobanana": {
      "type": "http",
      "url": "https://nanobanana.mcp.acedata.cloud/mcp",
      "headers": {"Authorization": "Bearer ${input:acedata-nanobanana-token}"}
    }
  }
}
```

For **Cline**, use its MCP configuration UI or CLI file `~/.cline/data/settings/cline_mcp_settings.json`; its remote transport value is `streamableHttp`. For **JetBrains AI Assistant**, add a remote URL from **Settings → Tools → AI Assistant → Model Context Protocol (MCP)**. For **Zed**, use a `context_servers` entry with the URL only for OAuth or add a local Bearer header. These clients have different configuration schemas; follow their current UI rather than copying another client's JSON. [Cline](https://docs.cline.bot/mcp/mcp-overview) · [JetBrains](https://www.jetbrains.com/help/ai-assistant/mcp.html) · [Zed](https://zed.dev/docs/ai/mcp).

### Local stdio

Install the package and give the local process an API token:

```bash
python -m pip install mcp-nanobanana-pro
export ACEDATACLOUD_API_TOKEN='YOUR_API_TOKEN'
mcp-nanobanana-pro
```

For Claude Desktop local MCP, merge this entry into the file opened by its developer settings (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS). `uvx` requires [uv](https://docs.astral.sh/uv/) on `PATH`:

```json
{
  "mcpServers": {
    "nanobanana": {
      "command": "uvx",
      "args": ["mcp-nanobanana-pro"],
      "env": {"ACEDATACLOUD_API_TOKEN": "YOUR_API_TOKEN"}
    }
  }
}
```

Keep this user-level file private. Self-hosted HTTP uses `mcp-nanobanana-pro --transport http --port 8000`; expose it only with suitable network and TLS controls. Local execution still calls the AceDataCloud API.

### Check before using the service

1. `https://nanobanana.mcp.acedata.cloud/health` returning `{"status":"ok"}` checks endpoint reachability only.
2. Confirm that the MCP client loads tools. The tool list shows MCP discovery, not downstream API access or balance.
3. If you need a full API check, call `nanobanana_generate_image` with your own valid input after reviewing [current service documentation](https://platform.acedata.cloud/documents/nano-banana-mcp?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=nanobanana_mcp_readme_quick_start) and displayed pricing. If the result contains a task ID, call `nanobanana_get_task` on that same ID until terminal success or failure. Do not resubmit the operation just to check progress.

For **401**, check which auth route the client used and whether the token or OAuth session is valid. A **403** may mean an account permission or content moderation failure; read the returned error. Insufficient balance and downstream service failures need their own diagnosis. A listed tool or submitted task does not prove a successful result.

## Available Tools

### Image Generation

| Tool                        | Description                          |
| --------------------------- | ------------------------------------ |
| `nanobanana_generate_image` | Generate an image from a text prompt |
| `nanobanana_edit_image`     | Edit or combine images with AI       |

### Tasks

| Tool                         | Description                  |
| ---------------------------- | ---------------------------- |
| `nanobanana_get_task`        | Query a single task status   |
| `nanobanana_get_tasks_batch` | Query multiple tasks at once |

## Supported Models

| Model | Resolution |
|---|---|
| `nano-banana` (default) | 1K |
| `nano-banana-2-lite` | 1K |
| `nano-banana-2` | 1K, 2K, 4K |
| `nano-banana-2.1` | 1K, 2K, 4K |
| `nano-banana-pro` | 1K, 2K, 4K |

All five models support generation and editing. The existing `nano-banana`, `nano-banana-2-lite`, `nano-banana-2`, and `nano-banana-pro` models also have `:official` variants. **Nano Banana 2.1 has no `:official` variant**; use exactly `nano-banana-2.1`. Omitting `model` still selects `nano-banana`.

## Usage Examples

### Nano Banana 2.1 Generation and Editing

Pass these arguments to `nanobanana_generate_image`:

```json
{
  "prompt": "A blue ceramic vase on a cream background, soft side lighting, no text",
  "model": "nano-banana-2.1",
  "aspect_ratio": "1:1",
  "resolution": "2K",
  "count": 2
}
```

For `nanobanana_edit_image`, supply your reference image URL:

```json
{
  "prompt": "Change the vase to green while preserving the background and lighting",
  "image_urls": ["https://example.com/vase.png"],
  "model": "nano-banana-2.1",
  "resolution": "4K"
}
```

Generation and editing submit asynchronously. Keep the returned `task_id` and query `nanobanana_get_task` until terminal success or failure; submission alone is not a completed image. Editing without `aspect_ratio` preserves the first reference image's aspect ratio; `resolution` defaults to `1K` if omitted. Review the final image and pixel dimensions before using it.

### Generate Image from Prompt

```
User: Create an image of a sunset over mountains

Claude: I'll generate that image for you.
[Calls nanobanana_generate_image with detailed prompt]
```

### Virtual Try-On

```
User: Put this shirt on this model
[Provides two image URLs]

Claude: I'll combine these images.
[Calls nanobanana_edit_image with both image URLs]
```

### Product Photography

```
User: Place this product in a modern kitchen scene
[Provides product image URL]

Claude: I'll create a product scene for you.
[Calls nanobanana_edit_image with scene description]
```

## Prompt Writing Tips

For best results, include these elements in your prompts:

- **Main Subject**: What is the primary focus?
- **Atmosphere**: What mood should the image convey?
- **Lighting**: How is the scene illuminated?
- **Camera/Lens**: What photographic style? (85mm portrait, wide-angle, etc.)
- **Quality Keywords**: Technical descriptors (bokeh, film grain, HDR, etc.)

### Example Prompt

```
A photorealistic close-up portrait of an elderly Japanese ceramicist
with deep wrinkles and a warm smile. Soft golden hour light streaming
through a window. Captured with an 85mm portrait lens, soft bokeh
background. Serene and masterful mood.
```

## Configuration

### Environment Variables

| Variable                     | Description                 | Default                     |
| ---------------------------- | --------------------------- | --------------------------- |
| `ACEDATACLOUD_API_TOKEN`     | API token from AceDataCloud | **Required**                |
| `ACEDATACLOUD_API_BASE_URL`  | API base URL                | `https://api.acedata.cloud` |
| `ACEDATACLOUD_OAUTH_CLIENT_ID`  | OAuth client ID (hosted mode) | —                           |
| `ACEDATACLOUD_PLATFORM_BASE_URL` | Platform base URL            | `https://platform.acedata.cloud` |
| `NANOBANANA_REQUEST_TIMEOUT` | Request timeout in seconds  | `1800`                      |
| `LOG_LEVEL`                  | Logging level               | `INFO`                      |

### Command Line Options

```bash
mcp-nanobanana-pro --help

Options:
  --version          Show version
  --transport        Transport mode: stdio (default) or http
  --port             Port for HTTP transport (default: 8000)
```

## Development

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/AceDataCloud/NanoBananaMCP.git
cd NanoBananaMCP

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
NanoBanana/
├── core/                   # Core modules
│   ├── __init__.py
│   ├── client.py          # HTTP client for NanoBanana API
│   ├── config.py          # Configuration management
│   ├── exceptions.py      # Custom exceptions
│   ├── server.py          # MCP server initialization
│   ├── types.py           # Type definitions
│   └── utils.py           # Utility functions
├── tools/                  # MCP tool definitions
│   ├── __init__.py
│   ├── image_tools.py     # Image generation/editing tools
│   └── task_tools.py      # Task query tools
├── prompts/                # MCP prompt templates
│   └── __init__.py
├── tests/                  # Test suite
├── deploy/                 # Deployment configs
│   └── production/
│       ├── deployment.yaml
│       ├── ingress.yaml
│       └── service.yaml
├── .env.example           # Environment template
├── .gitignore
├── Dockerfile             # Docker image for HTTP mode
├── docker-compose.yaml    # Docker Compose config
├── LICENSE
├── main.py                # Entry point
├── pyproject.toml         # Project configuration
└── README.md
```

## API Reference

This server wraps the [AceDataCloud NanoBanana API](https://platform.acedata.cloud/documents/nano-banana-images?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=nanobanana_mcp_readme_documents_nano-banana-images):

- [NanoBanana Images API](https://platform.acedata.cloud/documents/nano-banana-images?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=nanobanana_mcp_readme_documents_nano-banana-images) - Image generation and editing
- [NanoBanana Tasks API](https://platform.acedata.cloud/documents/nano-banana-tasks?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=nanobanana_mcp_readme_documents_nano-banana-tasks) - Task queries

## Use Cases

- **Portrait Enhancement** - Try different clothing on the same person
- **Product Scene Composition** - Place white-background products in realistic environments
- **Attribute Replacement** - Change materials, colors, or variants
- **Poster Quick Editing** - Rapidly change styles or themes
- **2D to 3D Conversion** - Convert images to 3D product mockups
- **Image Restoration** - Restore old or damaged photos

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing`)
5. Open a Pull Request

## Documentation

<!-- canonical-documentation -->
[Documentation](https://platform.acedata.cloud/documents/nano-banana-mcp?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=nanobanana_mcp_readme_quick_start)

## License

MIT License - see [LICENSE](LICENSE) for details.

## Links

- [AceDataCloud Platform](https://platform.acedata.cloud?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=nanobanana_mcp_readme_platform)
- [Model Context Protocol](https://modelcontextprotocol.io)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)

---

Made with love by [AceDataCloud](https://platform.acedata.cloud?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=nanobanana_mcp_readme_platform)
