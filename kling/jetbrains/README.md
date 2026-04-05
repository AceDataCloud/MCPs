# Kling MCP — JetBrains Plugin

AI Video Generation with [Kling](https://klingai.com) via [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) for JetBrains IDEs.

<!-- Plugin description -->
This plugin helps you set up the MCP Kling server with JetBrains AI Assistant.
Once configured, AI Assistant can generate, extend, and animate videos
— all powered by [Ace Data Cloud](https://platform.acedata.cloud).

**8 AI Tools** — Generate, extend, and animate videos.
<!-- Plugin description end -->

## Quick Start

1. Install this plugin from the [JetBrains Marketplace](https://plugins.jetbrains.com/plugin/com.acedatacloud.mcp.kling)
2. Open **Settings -> Tools -> Kling MCP**
3. Enter your [Ace Data Cloud](https://platform.acedata.cloud) API token
4. Click **Copy Config** (STDIO or HTTP)
5. Paste into **Settings -> Tools -> AI Assistant -> Model Context Protocol (MCP)**

### STDIO Mode (Local)

Runs the MCP server locally. Requires [uv](https://github.com/astral-sh/uv) installed.

```json
{
  "mcpServers": {
    "kling": {
      "command": "uvx",
      "args": ["mcp-kling"],
      "env": {
        "ACEDATACLOUD_API_TOKEN": "your-token"
      }
    }
  }
}
```

### HTTP Mode (Remote)

Connects to the hosted MCP server at `kling.mcp.acedata.cloud`. No local install needed.

```json
{
  "mcpServers": {
    "kling": {
      "url": "https://kling.mcp.acedata.cloud/mcp",
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
- [PyPI Package](https://pypi.org/project/mcp-kling/)
- [Source Code](https://github.com/AceDataCloud/KlingMCP)

## License

MIT
