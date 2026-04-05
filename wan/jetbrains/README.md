# Wan MCP — JetBrains Plugin

AI Video Generation with [Wan](https://wanx.aliyun.com/) via [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) for JetBrains IDEs.

<!-- Plugin description -->
This plugin helps you set up the MCP Wan server with JetBrains AI Assistant.
Once configured, AI Assistant can generate videos from text or images
— all powered by [Ace Data Cloud](https://platform.acedata.cloud).

**7 AI Tools** — Generate videos from text or images.
<!-- Plugin description end -->

## Quick Start

1. Install this plugin from the [JetBrains Marketplace](https://plugins.jetbrains.com/plugin/com.acedatacloud.mcp.wan)
2. Open **Settings → Tools → Wan MCP**
3. Enter your [Ace Data Cloud](https://platform.acedata.cloud) API token
4. Click **Copy Config** (STDIO or HTTP)
5. Paste into **Settings → Tools → AI Assistant → Model Context Protocol (MCP)**

### STDIO Mode (Local)

Runs the MCP server locally. Requires [uv](https://github.com/astral-sh/uv) installed.

```json
{
  "mcpServers": {
    "wan": {
      "command": "uvx",
      "args": ["mcp-wan"],
      "env": {
        "ACEDATACLOUD_API_TOKEN": "your-token"
      }
    }
  }
}
```

### HTTP Mode (Remote)

Connects to the hosted MCP server at `wan.mcp.acedata.cloud`. No local install needed.

```json
{
  "mcpServers": {
    "wan": {
      "url": "https://wan.mcp.acedata.cloud/mcp",
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
- [PyPI Package](https://pypi.org/project/mcp-wan/)
- [Source Code](https://github.com/AceDataCloud/WanMCP)

## License

MIT
