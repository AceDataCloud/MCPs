# MiniMax H3 MCP

<!-- mcp-name: io.github.AceDataCloud/mcp-minimax -->

[![PyPI](https://img.shields.io/pypi/v/mcp-minimax.svg)](https://pypi.org/project/mcp-minimax/)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)

Model Context Protocol server for MiniMax H3 multimodal video generation through AceDataCloud.

## Capabilities

- Text-to-video
- Image-to-video with 1–9 reference images
- Audio-guided video with 1–3 audio references and optional images
- 4–15 second output in 16:9 or 9:16
- Asynchronous single and batch task retrieval
- Hosted OAuth HTTP transport and local stdio transport

## Tools

| Tool | Purpose |
| --- | --- |
| `minimax_generate_video_from_text` | Generate from a detailed prompt |
| `minimax_generate_video_from_images` | Generate from one to nine image URLs |
| `minimax_generate_video_from_audio` | Generate with one to three audio URLs and optional images |
| `minimax_get_task` | Retrieve one task |
| `minimax_get_tasks_batch` | Retrieve several tasks |
| `minimax_list_models` | Show model constraints |
| `minimax_list_actions` | Show available workflows |

## Hosted server

```text
https://minimax.mcp.acedata.cloud/mcp
```

The hosted server supports AceDataCloud OAuth. MCP clients that support remote OAuth can connect directly to this URL.

## Local installation

```bash
pipx install mcp-minimax
export ACEDATACLOUD_API_TOKEN="YOUR_API_TOKEN"
mcp-minimax
```

Get a token from [AceDataCloud](https://platform.acedata.cloud/console/applications).

### Claude Code

```bash
claude mcp add minimax --transport stdio \
  --env ACEDATACLOUD_API_TOKEN=YOUR_API_TOKEN \
  -- mcp-minimax
```

### Generic MCP configuration

```json
{
  "mcpServers": {
    "minimax": {
      "command": "mcp-minimax",
      "env": {
        "ACEDATACLOUD_API_TOKEN": "YOUR_API_TOKEN"
      }
    }
  }
}
```

## Examples

Text:

```text
Generate a 6-second 16:9 video: a red fox running through a snowy forest at dawn, low tracking shot.
```

Images:

```text
Animate these two reference images for 8 seconds while preserving the character and clothing.
```

Audio:

```text
Create a 9:16 dance video guided by this audio, with cuts and motion following the beat.
```

Generation tools submit asynchronously. Poll the returned task ID with `minimax_get_task` until the final AceDataCloud CDN video is available.

## Development

```bash
pip install -e ".[dev,test]"
ruff check .
pytest --cov=core --cov=tools
mypy core tools
```

## License

MIT
