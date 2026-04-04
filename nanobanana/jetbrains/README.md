# NanoBanana MCP — JetBrains Plugin

AI Image Generation with [NanoBanana (Gemini-based)](https://nanobanana.com) via [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) for JetBrains IDEs.

<!-- Plugin description -->
This plugin helps you set up the MCP NanoBanana (Gemini-based) server with JetBrains AI Assistant.
Once configured, AI Assistant can generate and edit images
— all powered by [Ace Data Cloud](https://platform.acedata.cloud).

**4 AI Tools** — Generate and edit images.
<!-- Plugin description end -->

## Quick Start

1. Install this plugin from the [JetBrains Marketplace](https://plugins.jetbrains.com/plugin/com.acedatacloud.mcp.nanobanana)
2. Open **Settings → Tools → NanoBanana MCP**
3. Enter your [Ace Data Cloud](https://platform.acedata.cloud) API token
4. Click **Copy Config** (STDIO or HTTP)
5. Paste into **Settings → Tools → AI Assistant → Model Context Protocol (MCP)**

### STDIO Mode (Local)

Runs the MCP server locally. Requires [uv](https://github.com/astral-sh/uv) installed.

```json
{
  "mcpServers": {
    "nanobanana": {
      "command": "uvx",
      "args": ["mcp-nanobanana-pro"],
      "env": {
        "ACEDATACLOUD_API_TOKEN": "your-token"
      }
    }
  }
}
```

### HTTP Mode (Remote)

Connects to the hosted MCP server at `nanobanana.mcp.acedata.cloud`. No local install needed.

```json
{
  "mcpServers": {
    "nanobanana": {
      "url": "https://nanobanana.mcp.acedata.cloud/mcp",
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
- [PyPI Package](https://pypi.org/project/mcp-nanobanana-pro/)
- [Source Code](https://github.com/AceDataCloud/NanoBananaMCP)

## License

MIT
