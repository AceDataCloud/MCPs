# Producer MCP — JetBrains Plugin

AI Music Generation with [Producer/Riffusion (FUZZ)](https://www.riffusion.com) via [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) for JetBrains IDEs.

<!-- Plugin description -->
This plugin helps you set up the MCP Producer server with JetBrains AI Assistant.
Once configured, AI Assistant can generate music, create covers, extend songs, and more
— all powered by [Ace Data Cloud](https://platform.acedata.cloud).

**18 AI Tools** — Generate, extend, cover, remix, and separate music.
<!-- Plugin description end -->

## Quick Start

1. Install this plugin from the [JetBrains Marketplace](https://plugins.jetbrains.com/plugin/com.acedatacloud.mcp.producer)
2. Open **Settings → Tools → Producer MCP**
3. Enter your [Ace Data Cloud](https://platform.acedata.cloud) API token
4. Click **Copy Config** (STDIO or HTTP)
5. Paste into **Settings → Tools → AI Assistant → Model Context Protocol (MCP)**

### STDIO Mode (Local)

Runs the MCP server locally. Requires [uv](https://github.com/astral-sh/uv) installed.

```json
{
  "mcpServers": {
    "producer": {
      "command": "uvx",
      "args": ["mcp-producer"],
      "env": {
        "ACEDATACLOUD_API_TOKEN": "your-token"
      }
    }
  }
}
```

### HTTP Mode (Remote)

Connects to the hosted MCP server at `producer.mcp.acedata.cloud`. No local install needed.

```json
{
  "mcpServers": {
    "producer": {
      "url": "https://producer.mcp.acedata.cloud/mcp",
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
- [PyPI Package](https://pypi.org/project/mcp-producer/)
- [Source Code](https://github.com/AceDataCloud/ProducerMCP)

## License

MIT
