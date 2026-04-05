# Hailuo MCP — JetBrains Plugin

AI Video Generation with [Hailuo (MiniMax)](https://hailuoai.video) via [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) for JetBrains IDEs.

<!-- Plugin description -->
This plugin helps you set up the MCP Hailuo (MiniMax) server with JetBrains AI Assistant.
Once configured, AI Assistant can generate videos from text and images
— all powered by [Ace Data Cloud](https://platform.acedata.cloud).

**6 AI Tools** — Generate videos from text and images.
<!-- Plugin description end -->

## Quick Start

1. Install this plugin from the [JetBrains Marketplace](https://plugins.jetbrains.com/plugin/com.acedatacloud.mcp.hailuo)
2. Open **Settings → Tools → Hailuo MCP**
3. Enter your [Ace Data Cloud](https://platform.acedata.cloud) API token
4. Click **Copy Config** (STDIO or HTTP)
5. Paste into **Settings → Tools → AI Assistant → Model Context Protocol (MCP)**

### STDIO Mode (Local)

Runs the MCP server locally. Requires [uv](https://github.com/astral-sh/uv) installed.

```json
{
  "mcpServers": {
    "hailuo": {
      "command": "uvx",
      "args": ["mcp-hailuo"],
      "env": {
        "ACEDATACLOUD_API_TOKEN": "your-token"
      }
    }
  }
}
```

### HTTP Mode (Remote)

Connects to the hosted MCP server at `hailuo.mcp.acedata.cloud`. No local install needed.

```json
{
  "mcpServers": {
    "hailuo": {
      "url": "https://hailuo.mcp.acedata.cloud/mcp",
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
- [PyPI Package](https://pypi.org/project/mcp-hailuo/)
- [Source Code](https://github.com/AceDataCloud/HailuoMCP)

## License

MIT
