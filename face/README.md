# MCP Face Transform Server

A [Model Context Protocol](https://modelcontextprotocol.io) (MCP) server that
exposes the AceDataCloud Face Transform API — face keypoint detection,
beautification, age/gender transform, face swap, cartoonization, and liveness
detection.

> **Status:** All Face APIs are currently in **Alpha**. Interfaces may evolve.

## Features

- **Keypoint detection** — 90+ landmarks per face, multi-face supported
- **Beautification** — smoothing, whitening, face slimming, eye enlarging
- **Age transform** — age or de-age a portrait
- **Gender transform** — swap perceived facial gender characteristics
- **Face swap** — move a source face onto a target image (with optional async webhook)
- **Cartoonize** — render a portrait in animated / cartoon style
- **Liveness detection** — distinguish live captures from printed / screen photos

## Installation

```bash
pip install mcp-face-transform
```

## Configuration

Set your AceDataCloud API token:

```bash
export ACEDATACLOUD_API_TOKEN=your_token_here
```

Get your token from [https://platform.acedata.cloud](https://platform.acedata.cloud).

## Usage

### stdio mode (default)

```bash
mcp-face-transform
```

### HTTP mode

```bash
mcp-face-transform --transport http --port 8000
```

## Available Tools

| Tool | Endpoint | Purpose |
|------|----------|---------|
| `face_detect_keypoints` | `POST /face/analyze` | Detect 90+ keypoints per face |
| `face_beautify` | `POST /face/beautify` | Smoothing / whitening / slimming / eye enlarging |
| `face_change_age` | `POST /face/change-age` | Age or de-age a portrait |
| `face_change_gender` | `POST /face/change-gender` | Swap perceived facial gender characteristics |
| `face_swap` | `POST /face/swap` | Move source face onto target image |
| `face_cartoonize` | `POST /face/cartoon` | Convert portrait to cartoon style |
| `face_detect_liveness` | `POST /face/detect-live` | Detect live vs printed/screen face |
| `face_get_usage_guide` | _client-side_ | Concise tool usage reference |

## Example

```text
"Detect all faces in https://example.com/group.jpg and return their keypoints."
→ face_detect_keypoints(image_url="https://example.com/group.jpg")

"Lighten and smooth my portrait."
→ face_beautify(image_url="https://example.com/me.jpg", smoothing=15, whitening=25)

"Replace the face in the scene with the headshot."
→ face_swap(
    source_image_url="https://example.com/headshot.jpg",
    target_image_url="https://example.com/scene.jpg",
  )
```

## Configuration in Claude Desktop / Claude Code

```json
{
  "mcpServers": {
    "face-transform": {
      "command": "uvx",
      "args": ["mcp-face-transform"],
      "env": {
        "ACEDATACLOUD_API_TOKEN": "your_api_token_here"
      }
    }
  }
}
```

Or use the hosted endpoint with bearer auth:

```json
{
  "mcpServers": {
    "face-transform": {
      "url": "https://face.mcp.acedata.cloud/mcp",
      "headers": {
        "Authorization": "Bearer your_api_token_here"
      }
    }
  }
}
```

## Development

```bash
pip install -e ".[dev,test]"
pytest --cov=core --cov=tools
ruff check .
```

## License

MIT — see [LICENSE](LICENSE).
