# Luma MCP — JetBrains Plugin

AI Video Generation with [Luma Dream Machine](https://lumalabs.ai) via [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) for JetBrains IDEs.

<!-- Plugin description -->
This plugin helps you set up the MCP Luma Dream Machine server with JetBrains AI Assistant.
Once configured, AI Assistant can generate and extend videos
— all powered by [Ace Data Cloud](https://platform.acedata.cloud).

**8 AI Tools** — Generate and extend videos.
<!-- Plugin description end -->

## Quick Start

1. Install this plugin from the [JetBrains Marketplace](https://plugins.jetbrains.com/plugin/com.acedatacloud.mcp.luma)
2. Open **Settings → Tools → Luma MCP**
3. Enter your [Ace Data Cloud](https://platform.acedata.cloud) API token
4. Click **Copy Config** (STDIO or HTTP)
5. Paste into **Settings → Tools → AI Assistant → Model Context Protocol (MCP)**

### STDIO Mode (Local)

Runs the MCP server locally. Requires [uv](https://github.com/astral-sh/uv) installed.

```json
{
  "mcpServers": {
    "luma": {
      "command": "uvx",
      "args": ["mcp-luma"],
      "env": {
        "ACEDATACLOUD_API_TOKEN": "your-token"
      }
    }
  }
}
```

### HTTP Mode (Remote)

Connects to the hosted MCP server at `luma.mcp.acedata.cloud`. No local install needed.

```json
{
  "mcpServers": {
    "luma": {
      "url": "https://luma.mcp.acedata.cloud/mcp",
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
- [PyPI Package](https://pypi.org/project/mcp-luma/)
- [Source Code](https://github.com/AceDataCloud/LumaMCP)

## License

MIT
