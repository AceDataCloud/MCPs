# GrokMCP

[![PyPI version](https://img.shields.io/pypi/v/mcp-grok.svg)](https://pypi.org/project/mcp-grok/)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server for **Grok** (xAI) — chat/reasoning/vision **and** Grok Imagine video generation, powered by the [AceDataCloud](https://platform.acedata.cloud) API.

Chat with Grok models, or generate short AI videos from a text prompt or a still image — directly from any MCP-compatible client (Claude Desktop, Claude Code, Cursor, etc.).

## Features

- **Chat / Reasoning / Vision** — Talk to Grok 4 / Grok 3 family models, including vision (`grok-2-vision`) and tool calling
- **Text to Video** — Generate a video clip from a text description
- **Image to Video** — Animate a reference image into a video
- **Async task tracking** — Submit a job, poll for the result, single or batch
- **stdio & HTTP transports** — Local stdio for desktop clients, HTTP for remote hosting

## Tools

| Tool | Description |
| --- | --- |
| `grok_chat_completions` | Chat completion (reasoning / vision / tool calling) with Grok chat models. |
| `grok_text_to_video` | Generate a video from a text prompt (model `grok-imagine-video`). |
| `grok_image_to_video` | Generate a video from an input image (+ optional motion prompt). |
| `grok_get_task` | Query the status/result of a single generation task. |
| `grok_get_tasks_batch` | Query the status/result of multiple tasks at once. |
| `grok_list_models` | List available models and their capabilities. |
| `grok_list_actions` | List all tools and example workflows. |
| `grok_get_prompt_guide` | Tips for writing effective video prompts. |

## Models

### Chat (`grok_chat_completions`)

| Model | Notes |
| --- | --- |
| `grok-4` | Flagship reasoning model |
| `grok-4-1-fast` | Default — fast, capable |
| `grok-4-1-fast-non-reasoning` | Fast, no reasoning trace |
| `grok-3` | Previous-gen flagship |
| `grok-3-mini` | Smaller/cheaper; supports `reasoning_effort` |
| `grok-2-vision` | Vision-capable (image understanding) |

### Video

| Model | Text→Video | Image→Video | Notes |
| --- | --- | --- | --- |
| `grok-imagine-video` | ✅ | ✅ | Default. Lower price. Up to 30s, duration-banded billing. |
| `grok-imagine-video-1.5-preview` | ❌ | ✅ | Image-to-video only (requires `image_url`). Up to 15s, billed per second. |

## Parameters

| Parameter | Applies to | Values |
| --- | --- | --- |
| `prompt` | both | Text description (required for text-to-video) |
| `image_url` | image-to-video | Input image URL (required for `-1.5-preview`) |
| `reference_image_urls` | image-to-video | Optional list of style/content reference images |
| `aspect_ratio` | both | `1:1`, `16:9` (default), `9:16`, `4:3`, `3:4`, `3:2`, `2:3` |
| `resolution` | both | `480p` (default), `720p`, `1080p` |
| `duration` | both | `grok-imagine-video`: `1`–`30`s; `grok-imagine-video-1.5-preview`: `1`–`15`s (default `8`) |
| `callback_url` | both | Optional async webhook |

## Installation

### Via uvx (recommended)

```bash
uvx mcp-grok
```

### Via pip

```bash
pip install mcp-grok
mcp-grok
```

## Configuration

Set your AceDataCloud API token (get one at <https://platform.acedata.cloud>):

```bash
export ACEDATACLOUD_API_TOKEN=your_api_token_here
```

### Claude Desktop / Claude Code

Add to your MCP config (`claude_desktop_config.json` or `.mcp.json`):

```json
{
  "mcpServers": {
    "grok": {
      "command": "uvx",
      "args": ["mcp-grok"],
      "env": {
        "ACEDATACLOUD_API_TOKEN": "your_api_token_here"
      }
    }
  }
}
```

### Remote (HTTP)

A hosted Streamable HTTP endpoint is available at:

```
https://grok.mcp.acedata.cloud/mcp
```

## Environment Variables

| Variable | Description | Default |
| --- | --- | --- |
| `ACEDATACLOUD_API_TOKEN` | API token (required) | — |
| `ACEDATACLOUD_API_BASE_URL` | API base URL | `https://api.acedata.cloud` |
| `GROK_DEFAULT_MODEL` | Default model | `grok-imagine-video` |
| `GROK_REQUEST_TIMEOUT` | Request timeout (seconds) | `180` |
| `MCP_SERVER_NAME` | MCP server name | `grok` |
| `MCP_TRANSPORT` | Transport mode (`stdio`/`http`) | `stdio` |
| `LOG_LEVEL` | Logging level | `INFO` |

## Usage Notes

- Generation is **asynchronous**: the generation tools return a `task_id` quickly. Poll with `grok_get_task(task_id)` until the state is `succeeded` and the `video_url` is available.
- Generation typically takes ~30 seconds to a few minutes.
- Keep `resolution` at `480p` and `duration` short for faster, cheaper iterations.

## Development

```bash
pip install -e ".[dev,test]"
pytest --cov=core --cov=tools
ruff check .
```

## License

MIT — see [LICENSE](LICENSE).
