# Producer MCP — JetBrains Plugin

AI Music Generation with [Producer/Riffusion (FUZZ)](https://www.riffusion.com) via [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) for JetBrains IDEs.

<!-- Plugin description -->
This plugin helps you set up the MCP Producer server with JetBrains AI Assistant.
Once configured, AI Assistant can generate music, create covers, extend songs, and more
— all powered by [Ace Data Cloud](https://platform.acedata.cloud?utm_source=jetbrains_marketplace&utm_medium=referral&utm_campaign=evergreen).

**18 AI Tools** — Generate, extend, cover, remix, and separate music.
<!-- Plugin description end -->

## Quick Start

1. Install this plugin from the [JetBrains Marketplace](https://plugins.jetbrains.com/plugin/com.acedatacloud.mcp.producer)
2. Open **Settings → Tools → Producer MCP**
3. Enter your [Ace Data Cloud](https://platform.acedata.cloud?utm_source=jetbrains_marketplace&utm_medium=referral&utm_campaign=evergreen) API token
4. Click **Copy Config** (STDIO or HTTP)
5. Paste into **Settings → Tools → AI Assistant → Model Context Protocol (MCP)**

### Get your API key

<!-- BEGIN TOKEN ONBOARDING -->
Sign in to [Applications](https://platform.acedata.cloud/console/applications?utm_source=jetbrains_marketplace&utm_medium=referral&utm_campaign=evergreen) and open **General Application**. If it is missing, select **Initialize General Application**. Click the copy button marked **1** beside **API KEY**.

![Copy the General Application API key with the button marked 1](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/get-api-key-en.png)

Store the raw key in your client’s credential store or in the environment variable shown below. Add `Bearer ` only when setting an HTTP `Authorization` header yourself. Check access to the required operations, the current pricing, and the application balance. To use a separate key for this integration, open **Manage Keys** to set **Allowed APIs**, expiration, and usage limit.
<!-- END TOKEN ONBOARDING -->

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

- [Ace Data Cloud Platform](https://platform.acedata.cloud?utm_source=jetbrains_marketplace&utm_medium=referral&utm_campaign=evergreen)
- [Documentation](https://platform.acedata.cloud/documents/producer?utm_source=jetbrains_marketplace&utm_medium=referral&utm_campaign=evergreen)
- [PyPI Package](https://pypi.org/project/mcp-producer/)
- [Source Code](https://github.com/AceDataCloud/ProducerMCP)

## License

MIT
