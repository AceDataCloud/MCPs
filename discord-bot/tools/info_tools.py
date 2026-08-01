"""Informational tools for Discord Bot MCP server."""

from core.server import mcp


@mcp.tool()
async def discord_get_usage_guide() -> str:
    """Get a comprehensive guide for using the Discord Bot tools.

    Provides detailed information on how to use the Discord Bot MCP tools
    effectively, including available tools, parameters, and examples.

    Returns:
        Complete usage guide for Discord Bot tools.
    """
    # Last updated: 2026-08-01
    return """# Discord Bot Tools Usage Guide

## Overview

The Discord Bot MCP server connects to a Discord Agent Proxy deployed on AceDataCloud.
It lets you automate Discord operations from your AI client (Claude, Cursor, etc.).

## Prerequisites

You need a running Discord Agent Proxy instance. Deploy one at:
https://platform.acedata.cloud/console/applications

⚠️ **Warning**: Automating a personal Discord account (self-bot) violates Discord's Terms
of Service. Use a dedicated account and avoid high-frequency or mass-messaging behavior.

## Available Tools

### Account Information
- **discord_whoami** — View the proxied Discord account details

### Guild (Server) Operations
- **discord_list_guilds** — List all servers the account has joined
- **discord_list_channels** — List channels in a server
- **discord_create_text_channel** — Create a new text channel
- **discord_list_members** — List server members

### Message Operations
- **discord_send_message** — Send a message to a channel (with optional reply)
- **discord_read_messages** — Read recent messages from a channel
- **discord_edit_message** — Edit a message you sent
- **discord_delete_message** — Delete a message
- **discord_search_messages** — Search for messages in a channel
- **discord_add_reaction** — Add an emoji reaction to a message
- **discord_pin_message** — Pin a message in a channel

### Direct Messages
- **discord_create_dm** — Open a DM channel with a user (returns channel ID)
- **discord_send_dm** — Send a direct message to a user

## Example Workflows

### Check Recent Messages
1. Call `discord_list_guilds` to find your server IDs
2. Call `discord_list_channels` with a guild_id to find channel IDs
3. Call `discord_read_messages` with the channel_id to read messages

### Reply to a Message
1. Use `discord_read_messages` to get recent messages and find the message_id
2. Call `discord_send_message` with channel_id, content, and reply_to=message_id

### Send a Direct Message
```
discord_send_dm(recipient_id="123456789012345678", content="Hello!")
```

## Finding IDs

Enable Developer Mode in Discord (User Settings → Advanced → Developer Mode),
then right-click any channel, server, or user to copy their ID.

You can also use:
- `discord_list_guilds` to get guild IDs
- `discord_list_channels` to get channel IDs
- `discord_list_members` to get user IDs

## Rate Limits

If you receive a 429 error, Discord has rate-limited your account. Wait the number
of seconds indicated in the `retry_after` field before retrying.
"""
