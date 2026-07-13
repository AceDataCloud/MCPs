# Happy Horse MCP Server

[![PyPI](https://img.shields.io/pypi/v/mcp-happyhorse.svg)](https://pypi.org/project/mcp-happyhorse/)
[![Python](https://img.shields.io/pypi/pyversions/mcp-happyhorse.svg)](https://pypi.org/project/mcp-happyhorse/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Model Context Protocol server for Happy Horse AI video generation and editing through the
[Ace Data Cloud](https://platform.acedata.cloud/service/happyhorse) API.

## Capabilities

- Text-to-video generation
- First-frame image-to-video animation
- Reference-to-video generation with 1-9 subject or style images
- Video editing with up to 5 reference images
- 720P and 1080P output
- Single and batch task polling
- Local stdio and hosted Streamable HTTP/SSE transports
- Direct Bearer token and AceDataCloud OAuth authentication

## Install

```bash
pip install mcp-happyhorse
export ACEDATACLOUD_API_TOKEN="your-token"
mcp-happyhorse
```

Get a token from [platform.acedata.cloud](https://platform.acedata.cloud/console/credentials).

## Configure

### Claude Desktop

```json
{
  "mcpServers": {
    "happyhorse": {
      "command": "uvx",
      "args": ["mcp-happyhorse"],
      "env": {
        "ACEDATACLOUD_API_TOKEN": "your-token"
      }
    }
  }
}
```

### Hosted MCP

```json
{
  "mcpServers": {
    "happyhorse": {
      "url": "https://happyhorse.mcp.acedata.cloud/mcp",
      "headers": {
        "Authorization": "Bearer your-token"
      }
    }
  }
}
```

The hosted endpoint also supports OAuth-capable MCP clients.

## Tools

| Tool | Purpose |
|---|---|
| `happyhorse_generate_video` | Generate a video from text |
| `happyhorse_generate_video_from_image` | Animate one first-frame image |
| `happyhorse_generate_video_from_references` | Generate from 1-9 reference images |
| `happyhorse_edit_video` | Edit a source video with up to 5 references |
| `happyhorse_get_task` | Query one task |
| `happyhorse_get_tasks_batch` | Query multiple tasks |
| `happyhorse_list_models` | List valid models for each action |

Generation tools submit asynchronously when no `callback_url` is supplied. Keep the returned
`task_id`, wait about 15 seconds, then call `happyhorse_get_task` until the response contains a
final `video_url` or terminal error.

## Models

| Action | Models | Default |
|---|---|---|
| Text-to-video | `happyhorse-1.0-t2v`, `happyhorse-1.1-t2v` | `happyhorse-1.1-t2v` |
| Image-to-video | `happyhorse-1.0-i2v`, `happyhorse-1.1-i2v` | `happyhorse-1.1-i2v` |
| Reference-to-video | `happyhorse-1.0-r2v`, `happyhorse-1.1-r2v` | `happyhorse-1.1-r2v` |
| Video edit | `happyhorse-1.0-video-edit` | `happyhorse-1.0-video-edit` |

Generation duration is 3-15 seconds. Supported resolutions are `720P` and `1080P`. Text and
reference generation support `16:9`, `9:16`, `1:1`, `4:3`, and `3:4`. Image-to-video follows the
input image ratio. Video-edit duration follows the source video.

## Example Requests

Ask your MCP client:

> Generate a 720P, 9:16 video of a white horse crossing a snowy ridge at sunrise.

> Animate https://example.com/horse.jpg with a slow camera push and wind moving the mane.

> Edit https://example.com/source.mp4 to preserve the camera motion but apply the costume style
> from https://example.com/reference.jpg. Keep the original audio.

## Environment

| Variable | Default | Purpose |
|---|---|---|
| `ACEDATACLOUD_API_TOKEN` | none | API token for local stdio mode |
| `ACEDATACLOUD_API_BASE_URL` | `https://api.acedata.cloud` | API origin |
| `HAPPYHORSE_REQUEST_TIMEOUT` | `60` | HTTP request timeout in seconds |
| `MCP_TRANSPORT` | `stdio` | `stdio` or `http` |
| `MCP_SERVER_URL` | none | Public URL that enables hosted OAuth |
| `LOG_LEVEL` | `INFO` | Logging level |

## Development

```bash
pip install -e ".[all]"
pytest --cov=core --cov=tools
ruff check .
mypy core tools main.py
```

## License

[MIT](LICENSE)