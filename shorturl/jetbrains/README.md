# ShortURL MCP — JetBrains Plugin

URL Shortening with [ShortURL](https://surl.id) via [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) for JetBrains IDEs.

<!-- Plugin description -->
This plugin helps you set up the MCP ShortURL server with JetBrains AI Assistant.
Once configured, AI Assistant can create and manage short urls
— all powered by [Ace Data Cloud](https://platform.acedata.cloud).

**4 AI Tools** — Create and manage short URLs.
<!-- Plugin description end -->

## Quick Start

1. Install this plugin from the [JetBrains Marketplace](https://plugins.jetbrains.com/plugin/com.acedatacloud.mcp.shorturl)
2. Open **Settings → Tools → ShortURL MCP**
3. Enter your [Ace Data Cloud](https://platform.acedata.cloud) API token
4. Click **Copy Config** (STDIO or HTTP)
5. Paste into **Settings → Tools → AI Assistant → Model Context Protocol (MCP)**

### STDIO Mode (Local)

Runs the MCP server locally. Requires [uv](https://github.com/astral-sh/uv) installed.

```json
{
  "mcpServers": {
    "shorturl": {
      "command": "uvx",
      "args": ["mcp-shorturl"],
      "env": {
        "ACEDATACLOUD_API_TOKEN": "your-token"
      }
    }
  }
}
```

### HTTP Mode (Remote)

Connects to the hosted MCP server at `shorturl.mcp.acedata.cloud`. No local install needed.

```json
{
  "mcpServers": {
    "shorturl": {
      "url": "https://shorturl.mcp.acedata.cloud/mcp",
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
- [PyPI Package](https://pypi.org/project/mcp-shorturl/)
- [Source Code](https://github.com/AceDataCloud/ShortURLMCP)

## License

MIT
