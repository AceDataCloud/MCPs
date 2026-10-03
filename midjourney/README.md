# MidjourneyMCP

<!-- mcp-name: io.github.AceDataCloud/mcp-midjourney -->

[![PyPI version](https://img.shields.io/pypi/v/mcp-midjourney.svg)](https://pypi.org/project/mcp-midjourney/)
[![PyPI downloads](https://img.shields.io/pypi/dm/mcp-midjourney.svg)](https://pypi.org/project/mcp-midjourney/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![MCP](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io)

A [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server for AI image and video generation using [Midjourney](https://midjourney.com) through the [AceDataCloud API](https://platform.acedata.cloud).

Generate AI images, videos, and manage creative projects directly from Claude, VS Code, or any MCP-compatible client.

<!-- BEGIN GENERATED FIRST USE: scripts/build_entry_readmes.py -->
## Start with the hosted server

[Check current pricing and setup](https://platform.acedata.cloud/api/v1/marketing-attribution/entry/midjourneymcp/?utm_source=midjourneymcp&utm_medium=readme&utm_campaign=opensource_activation&utm_content=quick_start) · [Example prompt](#verify-your-first-result)

1. In a client that supports remote MCP OAuth, add **`https://midjourney.mcp.acedata.cloud/mcp`** as an HTTP server.
2. Choose **Connect / Sign in**, log in to AceDataCloud, review the requested permissions, and authorize.
3. Enable the tools and ask for a viewable image. You do not need to create or paste an API token for this route.

The server already supports OAuth discovery, dynamic client registration (DCR), and S256 PKCE.
DCR registers the **client application**; you still sign in and approve access. Authorization does
not make generation free. Review the consent screen: the media integration can read your profile
and manage the applications and credentials used for API access. Usage is charged to your account.

### Client compatibility

| Client / mode | Start path | Boundary |
| --- | --- | --- |
| Claude web / Desktop with remote custom connectors | Add the URL in the connector UI, then authorize | Availability and menu names depend on your plan and app version. The local Desktop JSON is for stdio; do not paste HTTP config there. |
| VS Code with native remote MCP support | Run **MCP: Add Server**, select HTTP, paste the URL, then follow authentication | Use a version with OAuth/DCR support. The optional AceDataCloud extension has its own API-key setup. |
| Other remote clients | Use the client's documented HTTP + OAuth flow | Support varies by client and version; an endpoint alone does not prove the client's login flow works. |
| Local stdio / self-hosted / clients without OAuth | Use the API Token path below | Keep the token in a local secret or environment variable; never in the server URL or Git. |

### Verify your first result

> Generate an image of a ceramic cup on a sunny desk, then retrieve the completed task and final image URL.

This is a reproducible example prompt, not a promised generation time or a recorded success.
A connected server, `tools/list`, and a task ID only confirm setup/submission. Keep the task ID,
wait for terminal success, then open or play the final media. Pending previews and failed tasks
are not a completed result. [View setup and billing guidance](https://platform.acedata.cloud/api/v1/marketing-attribution/entry/midjourneymcp/?utm_source=midjourneymcp&utm_medium=readme&utm_campaign=opensource_activation&utm_content=usage).

### Charges and common failures

- The MCP code is open source; hosted API generation is metered. Check current service pricing,
  model availability, account balance, and applicable terms before generating. No free allowance
  or commercial-use right is implied by installing this package.
- **Login loop / 401:** reconnect using the client's authentication UI; for local usage check the
  token and its scope. Update a client that cannot discover or register an OAuth server.
- **403 / access denied:** inspect the error and account permissions; a moderation rejection
  requires changing the input. **Insufficient balance:** inspect billing before retrying.
- **Pending / failed generation:** poll the same task; read the final error. Do not repeatedly
  submit new tasks to fix polling. A new generation may incur a new charge.

### API Token path

For local stdio or a client without OAuth, [open the setup page](https://platform.acedata.cloud/api/v1/marketing-attribution/entry/midjourneymcp/?utm_source=midjourneymcp&utm_medium=readme&utm_campaign=opensource_activation&utm_content=api_token),
sign in, choose the service, and create an API credential with the required scope. Configure
`ACEDATACLOUD_API_TOKEN` locally, or use the client's documented Bearer-header setting.
Use the local commands below for stdio; HTTP configuration formats are client-specific.

The setup link preserves the four campaign labels in the first-party browser session. Pasting
the bare endpoint directly into a native client remains supported; if no source can be matched,
that visit is reported as unknown. No token belongs in a tracking link.
<!-- END GENERATED FIRST USE -->

## Features

- **Image Generation** - Create AI-generated images from text prompts
- **Image Transformation** - Upscale, create variations, zoom, and pan images
- **Image Blending** - Combine multiple images into creative fusions
- **Reference-Based Generation** - Use existing images as inspiration
- **Image Description** - Get AI descriptions of images (reverse prompt)
- **Image Editing** - Edit images with text prompts and masks
- **Video Generation** - Create videos from text and reference images
- **Video Extension** - Extend existing videos to make them longer
- **Translation** - Translate Chinese prompts to English
- **Task Tracking** - Monitor generation progress and retrieve results

## Tool Reference

| Tool | Description |
|------|-------------|
| `midjourney_imagine` | Generate AI images from a text prompt using Midjourney. |
| `midjourney_transform` | Transform an existing Midjourney image with various operations. |
| `midjourney_blend` | Blend multiple images together using Midjourney. |
| `midjourney_with_reference` | Generate images using a reference image as inspiration. |
| `midjourney_edit` | Edit an existing image using Midjourney. |
| `midjourney_describe` | Get AI-generated descriptions of an image. |
| `midjourney_generate_video` | Generate a video from text prompt and reference image using Midjourney. |
| `midjourney_extend_video` | Extend an existing Midjourney video to make it longer. |
| `midjourney_translate` | Translate Chinese text to English for use as Midjourney prompts. |
| `midjourney_shorten` | Analyze and shorten long Midjourney prompts while preserving key ideas. |
| `midjourney_get_seed` | Get the seed value of a previously generated Midjourney image. |
| `midjourney_get_task` | Query the status and result of a Midjourney generation task. |
| `midjourney_get_tasks_batch` | Query multiple Midjourney generation tasks at once. |
| `midjourney_list_actions` | List all available Midjourney API actions and corresponding tools. |
| `midjourney_get_prompt_guide` | Get guidance on writing effective prompts for Midjourney. |
| `midjourney_list_transform_actions` | List all available transformation actions for Midjourney images. |

## Run locally with an API token

If you prefer to run the server on your own machine:

```bash
# Install from PyPI
pip install mcp-midjourney
# or
uvx mcp-midjourney

# Set your API token
export ACEDATACLOUD_API_TOKEN="your_token_here"

# Run (stdio mode for Claude Desktop / local clients)
mcp-midjourney

# Run (HTTP mode for remote access)
mcp-midjourney --transport http --port 8000
```

#### Claude Desktop (Local)

```json
{
  "mcpServers": {
    "midjourney": {
      "command": "uvx",
      "args": ["mcp-midjourney"],
      "env": {
        "ACEDATACLOUD_API_TOKEN": "your_token_here"
      }
    }
  }
}
```

#### Docker (Self-Hosting)

```bash
docker pull ghcr.io/acedatacloud/mcp-midjourney:latest
docker run -p 8000:8000 ghcr.io/acedatacloud/mcp-midjourney:latest
```

Clients connect with their own Bearer token — the server extracts the token from each request's `Authorization` header.

## Available Tools

### Image Generation

| Tool                        | Description                                           |
| --------------------------- | ----------------------------------------------------- |
| `midjourney_imagine`        | Generate images from a text prompt (creates 2x2 grid) |
| `midjourney_transform`      | Transform images (upscale, variation, zoom, pan)      |
| `midjourney_blend`          | Blend multiple images together                        |
| `midjourney_with_reference` | Generate using a reference image as inspiration       |

### Image Editing

| Tool                  | Description                                      |
| --------------------- | ------------------------------------------------ |
| `midjourney_edit`     | Edit an existing image with text prompt          |
| `midjourney_describe` | Get AI descriptions of an image (reverse prompt) |

### Video

| Tool                        | Description                                  |
| --------------------------- | -------------------------------------------- |
| `midjourney_generate_video` | Generate video from text and reference image |
| `midjourney_extend_video`   | Extend existing video to make it longer      |

### Utility

| Tool                   | Description                                   |
| ---------------------- | --------------------------------------------- |
| `midjourney_translate` | Translate Chinese text to English for prompts |
| `midjourney_get_seed`  | Get the seed value of a generated image       |

### Tasks

| Tool                         | Description                  |
| ---------------------------- | ---------------------------- |
| `midjourney_get_task`        | Query a single task status   |
| `midjourney_get_tasks_batch` | Query multiple tasks at once |

### Information

| Tool                                | Description                 |
| ----------------------------------- | --------------------------- |
| `midjourney_list_actions`           | List available API actions  |
| `midjourney_get_prompt_guide`       | Get prompt writing guide    |
| `midjourney_list_transform_actions` | List transformation actions |

## Usage Examples

### Generate Image from Prompt

```
User: Create a cyberpunk city at night

Claude: I'll generate a cyberpunk city image for you.
[Calls midjourney_imagine with prompt="Cyberpunk city at night, neon lights, rain, futuristic, detailed --ar 16:9"]
```

### Upscale an Image

```
User: Upscale the second image

Claude: I'll upscale the top-right image from the grid.
[Calls midjourney_transform with image_id and action="upscale2"]
```

### Blend Multiple Images

```
User: Blend these two images: [url1] and [url2]

Claude: I'll blend these images together.
[Calls midjourney_blend with image_urls=[url1, url2]]
```

### Generate Video

```
User: Animate this image [url] with gentle movement

Claude: I'll create a video from this image.
[Calls midjourney_generate_video with image_url and prompt="Gentle camera movement, cinematic"]
```

## Generation Modes

| Mode    | Description                              |
| ------- | ---------------------------------------- |
| `fast`  | Recommended for most use cases (default) |
| `turbo` | Faster generation, uses more credits     |
| `relax` | Slower generation, cheaper               |

## Configuration

### Environment Variables

| Variable                     | Description                 | Default                     |
| ---------------------------- | --------------------------- | --------------------------- |
| `ACEDATACLOUD_API_TOKEN`     | API token from AceDataCloud | **Required**                |
| `ACEDATACLOUD_API_BASE_URL`  | API base URL                | `https://api.acedata.cloud` |
| `ACEDATACLOUD_OAUTH_CLIENT_ID`  | OAuth client ID (hosted mode) | —                           |
| `ACEDATACLOUD_PLATFORM_BASE_URL` | Platform base URL            | `https://platform.acedata.cloud` |
| `MIDJOURNEY_DEFAULT_MODE`    | Default generation mode     | `fast`                      |
| `MIDJOURNEY_REQUEST_TIMEOUT` | Request timeout in seconds  | `1800`                      |
| `LOG_LEVEL`                  | Logging level               | `INFO`                      |

### Command Line Options

```bash
mcp-midjourney --help

Options:
  --version          Show version
  --transport        Transport mode: stdio (default) or http
  --port             Port for HTTP transport (default: 8000)
```

## Development

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/AceDataCloud/MidjourneyMCP.git
cd MidjourneyMCP

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
MidjourneyMCP/
├── core/                   # Core modules
│   ├── __init__.py
│   ├── client.py          # HTTP client for Midjourney API
│   ├── config.py          # Configuration management
│   ├── exceptions.py      # Custom exceptions
│   ├── server.py          # MCP server initialization
│   ├── types.py           # Type definitions
│   └── utils.py           # Utility functions
├── tools/                  # MCP tool definitions
│   ├── __init__.py
│   ├── describe_tools.py  # Image description tools
│   ├── edits_tools.py     # Image editing tools
│   ├── imagine_tools.py   # Image generation tools
│   ├── info_tools.py      # Information tools
│   ├── task_tools.py      # Task query tools
│   ├── translate_tools.py # Translation tools
│   └── video_tools.py     # Video generation tools
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
├── CHANGELOG.md
├── Dockerfile             # Docker image for HTTP mode
├── docker-compose.yaml    # Docker Compose config
├── LICENSE
├── main.py                # Entry point
├── pyproject.toml         # Project configuration
└── README.md
```

## API Reference

This server wraps the [AceDataCloud Midjourney API](https://platform.acedata.cloud):

- [Midjourney Imagine API](https://platform.acedata.cloud/services/d87e5e99-b797-4ade-9e73-b896896b0461) - Image generation
- [Midjourney Describe API](https://platform.acedata.cloud/services/d87e5e99-b797-4ade-9e73-b896896b0461) - Image description
- [Midjourney Tasks API](https://platform.acedata.cloud/services/d87e5e99-b797-4ade-9e73-b896896b0461) - Task queries
- [Midjourney Edits API](https://platform.acedata.cloud/documents/midjourney-edits) - Image editing
- [Midjourney Videos API](https://platform.acedata.cloud/documents/midjourney-videos) - Video generation
- [Midjourney Translate API](https://platform.acedata.cloud/services/d87e5e99-b797-4ade-9e73-b896896b0461) - Translation

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing`)
5. Open a Pull Request

## Service details

<!-- canonical-documentation -->
[Service details](https://platform.acedata.cloud/services/d87e5e99-b797-4ade-9e73-b896896b0461)

## License

MIT License - see [LICENSE](LICENSE) for details.

## Links

- [AceDataCloud Platform](https://platform.acedata.cloud)
- [Midjourney Official](https://midjourney.com)
- [Model Context Protocol](https://modelcontextprotocol.io)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)

---

Made with love by [AceDataCloud](https://platform.acedata.cloud)
