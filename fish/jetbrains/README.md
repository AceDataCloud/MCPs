# Fish Audio MCP — JetBrains Plugin

Text-to-speech via the [Fish Audio](https://acedata.cloud) API, exposed through [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) for JetBrains IDEs.

<!-- Plugin description -->
This plugin sets up the MCP Fish Audio server for JetBrains AI Assistant.
Once configured, AI Assistant can synthesise natural-sounding speech from text,
list available voice models, and track TTS tasks — all powered by
[Ace Data Cloud](https://platform.acedata.cloud).

**6 MCP Tools** — Generate speech, browse voice models, track tasks.
<!-- Plugin description end -->

## Quick Start

1. Install this plugin from the [JetBrains Marketplace](https://plugins.jetbrains.com/plugin/com.acedatacloud.mcp.fish)
2. Open **Settings → Tools → Fish Audio MCP**
3. Enter your [Ace Data Cloud](https://platform.acedata.cloud) API token
4. Click **Copy Config** (STDIO or HTTP)
5. Paste into **Settings → Tools → AI Assistant → Model Context Protocol (MCP)**

### STDIO Mode (Local)

Runs the MCP server locally. Requires [uv](https://github.com/astral-sh/uv) installed.

```json
{
  "mcpServers": {
    "fish": {
      "command": "uvx",
      "args": ["mcp-fish"],
      "env": {
        "ACEDATACLOUD_API_TOKEN": "your-token"
      }
    }
  }
}
```

### HTTP Mode (Remote)

Connects to the hosted MCP server at `fish.mcp.acedata.cloud`. No local install needed.

```json
{
  "mcpServers": {
    "fish": {
      "url": "https://fish.mcp.acedata.cloud/mcp",
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
- [PyPI Package](https://pypi.org/project/mcp-fish/)
- [Source Code](https://github.com/AceDataCloud/FishMCP)

## License

MIT
