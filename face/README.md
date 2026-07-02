# MCP Face Transform Server

<!-- mcp-name: io.github.AceDataCloud/mcp-face-transform -->

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

## Tool Reference

| Tool | Description |
|------|-------------|
| `face_detect_keypoints` | Detect 90+ keypoints per face (multi-face supported). |
| `face_beautify` | Smoothing, whitening, face slimming, and eye enlarging. |
| `face_change_age` | Age or de-age a portrait. |
| `face_change_gender` | Swap perceived facial gender characteristics. |
| `face_swap` | Move a source face onto a target image (with optional async webhook). |
| `face_cartoonize` | Render a portrait in cartoon / animated style. |
| `face_detect_liveness` | Distinguish a live capture from a printed / screen photo. |
| `face_get_usage_guide` | Concise client-side tool usage reference. |

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
