# Ace Data Cloud MCP — JetBrains Plugin

Manage your Ace Data Cloud account via [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) for JetBrains IDEs.

<!-- Plugin description -->
This plugin helps you set up the Ace Data Cloud platform MCP server with JetBrains AI Assistant.
Once configured, AI Assistant can check your balance, look up usage and spend, manage API keys
and orders, and list services and models — all powered by [Ace Data Cloud](https://platform.acedata.cloud?utm_source=jetbrains_marketplace&utm_medium=referral&utm_campaign=evergreen&utm_content=acedatacloud_mcp_jetbrains_platform).

**Account management tools** — Balance, usage, API keys, orders, tokens, services, and models.
<!-- Plugin description end -->

## Quick Start

1. Install this plugin from the [JetBrains Marketplace](https://plugins.jetbrains.com/plugin/com.acedatacloud.mcp.acedatacloud)
2. Open **Settings → Tools → Ace Data Cloud MCP**
3. Enter your [Ace Data Cloud](https://platform.acedata.cloud?utm_source=jetbrains_marketplace&utm_medium=referral&utm_campaign=evergreen&utm_content=acedatacloud_mcp_jetbrains_platform) platform token
4. Click **Copy Config** (STDIO or HTTP)
5. Paste into **Settings → Tools → AI Assistant → Model Context Protocol (MCP)**

### Get the account-management token

<!-- BEGIN TOKEN ONBOARDING -->
1. Sign in or register at [Ace Data Cloud → Account Tokens](https://platform.acedata.cloud/console/platform-tokens?utm_source=jetbrains_marketplace&utm_medium=referral&utm_campaign=evergreen&utm_content=acedatacloud_mcp_jetbrains_platform_token).
2. Click **Create** and copy the token with the copy button. It starts with `platform-`; it is an account-management credential, separate from an application's generation API key.
3. Paste only the token into this account MCP's credential field, or set `ACEDATACLOUD_PLATFORM_TOKEN` for local stdio. Add `Bearer ` only when configuring an HTTP `Authorization` header yourself.
4. Keep it private and remove it from **Account Tokens** to revoke access when no longer needed. For a client that supports hosted OAuth, you can instead use the browser sign-in flow described in this guide.
<!-- END TOKEN ONBOARDING -->

### STDIO Mode (Local)

Runs the MCP server locally. Requires [uv](https://github.com/astral-sh/uv) installed.

```json
{
  "mcpServers": {
    "acedatacloud": {
      "command": "uvx",
      "args": ["mcp-acedatacloud"],
      "env": {
        "ACEDATACLOUD_PLATFORM_TOKEN": "your-token"
      }
    }
  }
}
```

### HTTP Mode (Remote)

Connects to the hosted MCP server at `mcp.acedata.cloud`. No local install needed.

```json
{
  "mcpServers": {
    "acedatacloud": {
      "url": "https://mcp.acedata.cloud/mcp",
      "headers": {
        "Authorization": "Bearer your-token"
      }
    }
  }
}
```

## Links

- [Ace Data Cloud Platform](https://platform.acedata.cloud?utm_source=jetbrains_marketplace&utm_medium=referral&utm_campaign=evergreen&utm_content=acedatacloud_mcp_jetbrains_platform)
- [Documentation](https://platform.acedata.cloud/documents/acedatacloud-mcp?utm_source=jetbrains_marketplace&utm_medium=referral&utm_campaign=evergreen&utm_content=acedatacloud_mcp_jetbrains_quick_start)
- [PyPI Package](https://pypi.org/project/mcp-acedatacloud/)
- [Source Code](https://github.com/AceDataCloud/AceDataCloudMCP)

## License

MIT
