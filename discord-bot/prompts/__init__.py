"""Prompt templates for Discord Bot MCP server.

MCP Prompts provide guidance to LLMs on when and how to use the available tools.
These are exposed via the MCP protocol and help LLMs make better decisions.
"""

from core.server import mcp


@mcp.prompt()
def discord_usage_guide() -> str:
    """Guide for using Discord Bot tools to interact with Discord."""
    return """# Discord Bot Usage Guide

When the user wants to interact with Discord, choose the appropriate tool based on their needs:

## Reading Messages
**Tool:** `discord_read_messages`
**Use when:**
- User wants to check recent messages in a channel
- User wants to catch up on a conversation
- "What are the latest messages in #general?"

**Example:** "Show me the last 20 messages in channel 123456789"
→ Call `discord_read_messages(channel_id="123456789", limit=20)`

## Sending Messages
**Tool:** `discord_send_message`
**Use when:**
- User wants to send a message to a channel
- User wants to reply to a specific message
- "Send a message to #announcements"

**Example:** "Send 'Hello everyone!' to channel 123456789"
→ Call `discord_send_message(channel_id="123456789", content="Hello everyone!")`

## Searching Messages
**Tool:** `discord_search_messages`
**Use when:**
- User wants to find specific messages
- User is looking for something mentioned in a channel
- "Search for messages about the release date"

**Example:** "Search for 'release date' in channel 123456789"
→ Call `discord_search_messages(channel_id="123456789", query="release date")`

## Direct Messages
**Tool:** `discord_send_dm`
**Use when:**
- User wants to message someone privately
- User wants to send a one-on-one message

**Example:** "Send a DM to user 987654321 saying 'Can we talk?'"
→ Call `discord_send_dm(recipient_id="987654321", content="Can we talk?")`

## Finding Guild/Channel IDs
If you don't know the IDs:
1. Call `discord_list_guilds` to get guild IDs
2. Call `discord_list_channels(guild_id="...")` to get channel IDs
3. Call `discord_list_members(guild_id="...")` to get user IDs

## Important Notes:
1. Always get IDs before performing operations
2. Only edit/delete messages sent by the proxied account
3. Respect Discord's rate limits - slow down if you get 429 errors
4. The proxied account's actions are permanent - double-check before deleting
"""


@mcp.prompt()
def discord_workflow_examples() -> str:
    """Common workflow examples for Discord Bot automation tasks."""
    return """# Discord Bot Workflow Examples

## Workflow 1: Check and Respond to Messages
1. User: "Check if there are any questions in #support and answer them"
2. Call `discord_list_guilds` to find the guild
3. Call `discord_list_channels(guild_id="...")` to find #support
4. Call `discord_read_messages(channel_id="...", limit=50)` to read recent messages
5. Identify questions and respond with `discord_send_message`

## Workflow 2: Announce Something
1. User: "Post a release announcement in #announcements"
2. Call `discord_list_guilds` then `discord_list_channels` to find #announcements
3. Call `discord_send_message(channel_id="...", content="🎉 New release...")`

## Workflow 3: DM a Specific User
1. User: "Send a DM to John about the meeting"
2. Call `discord_list_guilds` then `discord_list_members` to find John's user ID
3. Call `discord_send_dm(recipient_id="...", content="About the meeting...")`

## Workflow 4: Find and React to a Message
1. User: "React with 👍 to the latest announcement"
2. Call `discord_read_messages` to get recent messages
3. Identify the announcement message
4. Call `discord_add_reaction(channel_id="...", message_id="...", emoji="👍")`

## Workflow 5: Edit a Previous Message
1. User: "Fix the typo in my last message in #general"
2. Call `discord_read_messages` to find your message
3. Call `discord_edit_message(channel_id="...", message_id="...", content="corrected text")`

## Tips:
- Cache guild/channel IDs for repeated operations in the same conversation
- Use `discord_search_messages` to find specific content without reading all messages
- Check `discord_whoami` to confirm you're proxying the correct account
"""
