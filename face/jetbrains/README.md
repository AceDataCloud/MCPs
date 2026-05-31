# Face Transform MCP — JetBrains Plugin

Face analysis & transformation via the [Ace Data Cloud Face API](https://acedata.cloud), exposed through [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) for JetBrains IDEs.

<!-- Plugin description -->
This plugin sets up the MCP Face Transform server for JetBrains AI Assistant.
Once configured, AI Assistant can detect keypoints, beautify portraits,
age or de-age faces, swap perceived gender, transplant a face onto a different
scene, cartoonize a portrait, and run liveness checks — all powered by
[Ace Data Cloud](https://platform.acedata.cloud).

**8 MCP Tools** covering the full AceDataCloud Face API surface.
<!-- Plugin description end -->

## Quick Start

1. Install this plugin from the [JetBrains Marketplace](https://plugins.jetbrains.com/plugin/com.acedatacloud.mcp.face)
2. Open **Settings → Tools → Face Transform MCP**
3. Enter your [Ace Data Cloud](https://platform.acedata.cloud) API token
4. Click **Copy Config** (STDIO or HTTP)
5. Paste into **Settings → Tools → AI Assistant → Model Context Protocol (MCP)**

### STDIO Mode (Local)

Runs the MCP server locally. Requires [uv](https://github.com/astral-sh/uv) installed.

```json
{
  "mcpServers": {
    "face": {
      "command": "uvx",
      "args": ["mcp-face-transform"],
      "env": {
        "ACEDATACLOUD_API_TOKEN": "your-token"
      }
    }
  }
}
```

### HTTP Mode (Remote)

Connects to the hosted MCP server at `face.mcp.acedata.cloud`. No local install needed.

```json
{
  "mcpServers": {
    "face": {
      "url": "https://face.mcp.acedata.cloud/mcp",
      "headers": {
        "Authorization": "Bearer your-token"
      }
    }
  }
}
```

## Links

- [Ace Data Cloud Platform](https://platform.acedata.cloud)
- [API Documentation](https://docs.acedata.cloud)
- [PyPI Package](https://pypi.org/project/mcp-face-transform/)
- [Source Code](https://github.com/AceDataCloud/FaceTransformMCP)

## License

MIT
