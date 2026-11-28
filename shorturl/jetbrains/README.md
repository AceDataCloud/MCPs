# ShortURL MCP — JetBrains Plugin

URL Shortening with [ShortURL](https://surl.id) via [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) for JetBrains IDEs.

<!-- Plugin description -->
This plugin helps you set up the MCP ShortURL server with JetBrains AI Assistant.
Once configured, AI Assistant can create and manage short urls
— all powered by [Ace Data Cloud](https://platform.acedata.cloud?utm_source=jetbrains_marketplace&utm_medium=referral&utm_campaign=evergreen).

**4 AI Tools** — Create and manage short URLs.
<!-- Plugin description end -->

## Quick Start

1. Install this plugin from the [JetBrains Marketplace](https://plugins.jetbrains.com/plugin/com.acedatacloud.mcp.shorturl)
2. Open **Settings → Tools → ShortURL MCP**
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

- [Ace Data Cloud Platform](https://platform.acedata.cloud?utm_source=jetbrains_marketplace&utm_medium=referral&utm_campaign=evergreen)
- [Documentation](https://platform.acedata.cloud/documents/short-url-mcp?utm_source=jetbrains_marketplace&utm_medium=referral&utm_campaign=evergreen)
- [PyPI Package](https://pypi.org/project/mcp-shorturl/)
- [Source Code](https://github.com/AceDataCloud/ShortURLMCP)

## License

MIT
