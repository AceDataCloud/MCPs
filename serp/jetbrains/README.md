# Serp MCP — JetBrains Plugin

Google Search with [Google SERP](https://google.com) via [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) for JetBrains IDEs.

<!-- Plugin description -->
This plugin helps you set up the MCP Google SERP server with JetBrains AI Assistant.
Once configured, AI Assistant can web, images, news, videos, maps and more
— all powered by [Ace Data Cloud](https://platform.acedata.cloud).

**11 AI Tools** — Web, Images, News, Videos, Maps and more.
<!-- Plugin description end -->

## Quick Start

1. Install this plugin from the [JetBrains Marketplace](https://plugins.jetbrains.com/plugin/com.acedatacloud.mcp.serp)
2. Open **Settings → Tools → Serp MCP**
3. Enter your [Ace Data Cloud](https://platform.acedata.cloud) API token
4. Click **Copy Config** (STDIO or HTTP)
5. Paste into **Settings → Tools → AI Assistant → Model Context Protocol (MCP)**

### STDIO Mode (Local)

Runs the MCP server locally. Requires [uv](https://github.com/astral-sh/uv) installed.

```json
{
  "mcpServers": {
    "serp": {
      "command": "uvx",
      "args": ["mcp-serp"],
      "env": {
        "ACEDATACLOUD_API_TOKEN": "your-token"
      }
    }
  }
}
```

### HTTP Mode (Remote)

Connects to the hosted MCP server at `serp.mcp.acedata.cloud`. No local install needed.

```json
{
  "mcpServers": {
    "serp": {
      "url": "https://serp.mcp.acedata.cloud/mcp",
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
- [PyPI Package](https://pypi.org/project/mcp-serp/)
- [Source Code](https://github.com/AceDataCloud/SerpMCP)

## License

MIT
