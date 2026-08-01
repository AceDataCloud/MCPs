# MCP Discord Bot Server

A Model Context Protocol (MCP) server that provides tools for automating Discord
through a self-hosted [Discord Agent Proxy](https://platform.acedata.cloud) instance.

## Overview

The Discord Agent Proxy is a standalone service you deploy on AceDataCloud. It maintains
a persistent connection to Discord using your account credentials and exposes both an MCP
and REST API interface.

This MCP server wraps the Discord Agent Proxy's REST API, exposing Discord operations
as MCP tools for use with Claude, Cursor, and other MCP-compatible AI clients.

> ⚠️ **Warning**: Automating a personal Discord account (self-bot) violates Discord's Terms
> of Service. Use a dedicated account and keep automation frequency reasonable.

## Prerequisites

1. Deploy a Discord Agent Proxy at [platform.acedata.cloud](https://platform.acedata.cloud/console/applications)
2. Configure it with your Discord account credentials
3. Note down the deployment URL and access token

## Installation

```bash
pip install mcp-discord-bot
```

## Configuration

Copy `.env.example` to `.env` and fill in your values:

```bash
DISCORD_BOT_BASE_URL=https://discord-bot-xxxxxxxxxxxx.app.acedata.cloud
DISCORD_BOT_TOKEN=your_bot_token_here
```

## Usage

### stdio (for AI clients)

```bash
mcp-discord-bot
```

Add to your MCP client configuration:

```json
{
  "mcpServers": {
    "discord-bot": {
      "command": "mcp-discord-bot",
      "env": {
        "DISCORD_BOT_BASE_URL": "https://discord-bot-xxxxxxxxxxxx.app.acedata.cloud",
        "DISCORD_BOT_TOKEN": "your_bot_token_here"
      }
    }
  }
}
```

### HTTP Transport

```bash
mcp-discord-bot --transport http --port 8000
```

## Available Tools

| Tool | Description |
|------|-------------|
| `discord_whoami` | View the proxied Discord account details |
| `discord_list_guilds` | List all servers the account has joined |
| `discord_list_channels` | List channels in a server |
| `discord_create_text_channel` | Create a new text channel |
| `discord_list_members` | List server members |
| `discord_send_message` | Send a message (with optional reply) |
| `discord_read_messages` | Read recent messages from a channel |
| `discord_edit_message` | Edit a message you sent |
| `discord_delete_message` | Delete a message |
| `discord_search_messages` | Search for messages in a channel |
| `discord_add_reaction` | Add an emoji reaction to a message |
| `discord_pin_message` | Pin a message in a channel |
| `discord_create_dm` | Open a DM channel with a user |
| `discord_send_dm` | Send a direct message to a user |
| `discord_get_usage_guide` | Get comprehensive usage documentation |

## License

MIT
