"""Discord Bot tools for interacting with the Discord Agent Proxy REST API."""

import json
from typing import Annotated

from pydantic import Field

from core.client import client
from core.exceptions import DiscordBotAPIError, DiscordBotAuthError
from core.server import mcp


@mcp.tool()
async def discord_whoami() -> str:
    """Get information about the currently proxied Discord account.

    Returns the account details including username, ID, and discriminator
    for the Discord account connected to this Agent Proxy.

    Returns:
        JSON object with the Discord account information.
    """
    try:
        result = await client.whoami()
        return json.dumps(result, ensure_ascii=False, indent=2)
    except DiscordBotAuthError as e:
        return json.dumps({"error": "Authentication Error", "message": e.message})
    except DiscordBotAPIError as e:
        return json.dumps({"error": "API Error", "message": e.message})
    except Exception as e:
        return json.dumps({"error": "Error fetching account info", "message": str(e)})


@mcp.tool()
async def discord_list_guilds() -> str:
    """List all Discord servers (guilds) the proxied account has joined.

    Returns a list of all guilds with their IDs and names.

    Returns:
        JSON array of guild objects with id and name.
    """
    try:
        result = await client.list_guilds()
        return json.dumps(result, ensure_ascii=False, indent=2)
    except DiscordBotAuthError as e:
        return json.dumps({"error": "Authentication Error", "message": e.message})
    except DiscordBotAPIError as e:
        return json.dumps({"error": "API Error", "message": e.message})
    except Exception as e:
        return json.dumps({"error": "Error listing guilds", "message": str(e)})


@mcp.tool()
async def discord_list_channels(
    guild_id: Annotated[
        str,
        Field(description="The ID of the Discord guild (server) to list channels for. Required."),
    ],
) -> str:
    """List all channels in a Discord guild (server).

    Returns a list of all channels with their IDs, names, and types.

    Args:
        guild_id: The ID of the Discord guild. Use discord_list_guilds to find guild IDs.

    Returns:
        JSON array of channel objects.
    """
    if not guild_id:
        return json.dumps({"error": "Validation Error", "message": "guild_id is required"})

    try:
        result = await client.list_channels(guild_id=guild_id)
        return json.dumps(result, ensure_ascii=False, indent=2)
    except DiscordBotAuthError as e:
        return json.dumps({"error": "Authentication Error", "message": e.message})
    except DiscordBotAPIError as e:
        return json.dumps({"error": "API Error", "message": e.message})
    except Exception as e:
        return json.dumps({"error": "Error listing channels", "message": str(e)})


@mcp.tool()
async def discord_create_text_channel(
    guild_id: Annotated[
        str,
        Field(description="The ID of the Discord guild (server) to create the channel in. Required."),
    ],
    name: Annotated[
        str,
        Field(description="The name for the new text channel. Required."),
    ],
) -> str:
    """Create a new text channel in a Discord guild (server).

    Args:
        guild_id: The ID of the Discord guild.
        name: The name for the new text channel.

    Returns:
        JSON object with the created channel details.
    """
    if not guild_id:
        return json.dumps({"error": "Validation Error", "message": "guild_id is required"})
    if not name:
        return json.dumps({"error": "Validation Error", "message": "name is required"})

    try:
        result = await client.create_text_channel(guild_id=guild_id, name=name)
        return json.dumps(result, ensure_ascii=False, indent=2)
    except DiscordBotAuthError as e:
        return json.dumps({"error": "Authentication Error", "message": e.message})
    except DiscordBotAPIError as e:
        return json.dumps({"error": "API Error", "message": e.message})
    except Exception as e:
        return json.dumps({"error": "Error creating channel", "message": str(e)})


@mcp.tool()
async def discord_list_members(
    guild_id: Annotated[
        str,
        Field(description="The ID of the Discord guild (server) to list members for. Required."),
    ],
    limit: Annotated[
        int | None,
        Field(description="Maximum number of members to return. Default is 100."),
    ] = None,
) -> str:
    """List members of a Discord guild (server).

    Args:
        guild_id: The ID of the Discord guild.
        limit: Maximum number of members to return (default: 100).

    Returns:
        JSON array of member objects.
    """
    if not guild_id:
        return json.dumps({"error": "Validation Error", "message": "guild_id is required"})

    try:
        result = await client.list_members(guild_id=guild_id, limit=limit)
        return json.dumps(result, ensure_ascii=False, indent=2)
    except DiscordBotAuthError as e:
        return json.dumps({"error": "Authentication Error", "message": e.message})
    except DiscordBotAPIError as e:
        return json.dumps({"error": "API Error", "message": e.message})
    except Exception as e:
        return json.dumps({"error": "Error listing members", "message": str(e)})


@mcp.tool()
async def discord_send_message(
    channel_id: Annotated[
        str,
        Field(description="The ID of the Discord channel to send the message to. Required."),
    ],
    content: Annotated[
        str,
        Field(description="The text content of the message to send. Required."),
    ],
    reply_to: Annotated[
        str | None,
        Field(description="The ID of a message to reply to. Optional."),
    ] = None,
) -> str:
    """Send a message to a Discord channel.

    Args:
        channel_id: The ID of the channel to send the message to.
        content: The text content of the message.
        reply_to: Optional ID of a message to reply to.

    Returns:
        JSON object with the sent message details.
    """
    if not channel_id:
        return json.dumps({"error": "Validation Error", "message": "channel_id is required"})
    if not content:
        return json.dumps({"error": "Validation Error", "message": "content is required"})

    try:
        result = await client.send_message(
            channel_id=channel_id, content=content, reply_to=reply_to
        )
        return json.dumps(result, ensure_ascii=False, indent=2)
    except DiscordBotAuthError as e:
        return json.dumps({"error": "Authentication Error", "message": e.message})
    except DiscordBotAPIError as e:
        return json.dumps({"error": "API Error", "message": e.message})
    except Exception as e:
        return json.dumps({"error": "Error sending message", "message": str(e)})


@mcp.tool()
async def discord_read_messages(
    channel_id: Annotated[
        str,
        Field(description="The ID of the Discord channel to read messages from. Required."),
    ],
    limit: Annotated[
        int | None,
        Field(
            description=(
                "Number of recent messages to retrieve. Default is 50, maximum is 100."
            )
        ),
    ] = None,
) -> str:
    """Read recent messages from a Discord channel.

    Args:
        channel_id: The ID of the channel to read messages from.
        limit: Number of recent messages to return (default: 50, max: 100).

    Returns:
        JSON array of message objects with author, content, and timestamp.
    """
    if not channel_id:
        return json.dumps({"error": "Validation Error", "message": "channel_id is required"})

    try:
        result = await client.read_messages(channel_id=channel_id, limit=limit)
        return json.dumps(result, ensure_ascii=False, indent=2)
    except DiscordBotAuthError as e:
        return json.dumps({"error": "Authentication Error", "message": e.message})
    except DiscordBotAPIError as e:
        return json.dumps({"error": "API Error", "message": e.message})
    except Exception as e:
        return json.dumps({"error": "Error reading messages", "message": str(e)})


@mcp.tool()
async def discord_edit_message(
    channel_id: Annotated[
        str,
        Field(description="The ID of the Discord channel containing the message. Required."),
    ],
    message_id: Annotated[
        str,
        Field(description="The ID of the message to edit. Required."),
    ],
    content: Annotated[
        str,
        Field(description="The new text content for the message. Required."),
    ],
) -> str:
    """Edit a message previously sent by the proxied Discord account.

    Only messages sent by the proxied account can be edited.

    Args:
        channel_id: The ID of the channel containing the message.
        message_id: The ID of the message to edit.
        content: The new text content for the message.

    Returns:
        JSON object with the updated message details.
    """
    if not channel_id:
        return json.dumps({"error": "Validation Error", "message": "channel_id is required"})
    if not message_id:
        return json.dumps({"error": "Validation Error", "message": "message_id is required"})
    if not content:
        return json.dumps({"error": "Validation Error", "message": "content is required"})

    try:
        result = await client.edit_message(
            channel_id=channel_id, message_id=message_id, content=content
        )
        return json.dumps(result, ensure_ascii=False, indent=2)
    except DiscordBotAuthError as e:
        return json.dumps({"error": "Authentication Error", "message": e.message})
    except DiscordBotAPIError as e:
        return json.dumps({"error": "API Error", "message": e.message})
    except Exception as e:
        return json.dumps({"error": "Error editing message", "message": str(e)})


@mcp.tool()
async def discord_delete_message(
    channel_id: Annotated[
        str,
        Field(description="The ID of the Discord channel containing the message. Required."),
    ],
    message_id: Annotated[
        str,
        Field(description="The ID of the message to delete. Required."),
    ],
) -> str:
    """Delete a message from a Discord channel.

    Args:
        channel_id: The ID of the channel containing the message.
        message_id: The ID of the message to delete.

    Returns:
        JSON confirmation of deletion or error details.
    """
    if not channel_id:
        return json.dumps({"error": "Validation Error", "message": "channel_id is required"})
    if not message_id:
        return json.dumps({"error": "Validation Error", "message": "message_id is required"})

    try:
        await client.delete_message(channel_id=channel_id, message_id=message_id)
        return json.dumps({"success": True, "message": "Message deleted successfully"})
    except DiscordBotAuthError as e:
        return json.dumps({"error": "Authentication Error", "message": e.message})
    except DiscordBotAPIError as e:
        return json.dumps({"error": "API Error", "message": e.message})
    except Exception as e:
        return json.dumps({"error": "Error deleting message", "message": str(e)})


@mcp.tool()
async def discord_search_messages(
    channel_id: Annotated[
        str,
        Field(description="The ID of the Discord channel to search messages in. Required."),
    ],
    query: Annotated[
        str,
        Field(description="The search query string. Required."),
    ],
    limit: Annotated[
        int | None,
        Field(description="Maximum number of results to return. Default is 25."),
    ] = None,
) -> str:
    """Search for messages in a Discord channel.

    Args:
        channel_id: The ID of the channel to search in.
        query: The search query string.
        limit: Maximum number of results to return (default: 25).

    Returns:
        JSON array of matching message objects.
    """
    if not channel_id:
        return json.dumps({"error": "Validation Error", "message": "channel_id is required"})
    if not query:
        return json.dumps({"error": "Validation Error", "message": "query is required"})

    try:
        result = await client.search_messages(channel_id=channel_id, query=query, limit=limit)
        return json.dumps(result, ensure_ascii=False, indent=2)
    except DiscordBotAuthError as e:
        return json.dumps({"error": "Authentication Error", "message": e.message})
    except DiscordBotAPIError as e:
        return json.dumps({"error": "API Error", "message": e.message})
    except Exception as e:
        return json.dumps({"error": "Error searching messages", "message": str(e)})


@mcp.tool()
async def discord_add_reaction(
    channel_id: Annotated[
        str,
        Field(description="The ID of the Discord channel containing the message. Required."),
    ],
    message_id: Annotated[
        str,
        Field(description="The ID of the message to add a reaction to. Required."),
    ],
    emoji: Annotated[
        str,
        Field(
            description=(
                "The emoji to react with. Use standard Unicode emojis (e.g., '👍', '❤️') "
                "or Discord custom emoji format. Required."
            )
        ),
    ],
) -> str:
    """Add an emoji reaction to a Discord message.

    Args:
        channel_id: The ID of the channel containing the message.
        message_id: The ID of the message to react to.
        emoji: The emoji to react with (Unicode or Discord custom emoji format).

    Returns:
        JSON confirmation of the reaction being added.
    """
    if not channel_id:
        return json.dumps({"error": "Validation Error", "message": "channel_id is required"})
    if not message_id:
        return json.dumps({"error": "Validation Error", "message": "message_id is required"})
    if not emoji:
        return json.dumps({"error": "Validation Error", "message": "emoji is required"})

    try:
        result = await client.add_reaction(
            channel_id=channel_id, message_id=message_id, emoji=emoji
        )
        return json.dumps(result, ensure_ascii=False, indent=2)
    except DiscordBotAuthError as e:
        return json.dumps({"error": "Authentication Error", "message": e.message})
    except DiscordBotAPIError as e:
        return json.dumps({"error": "API Error", "message": e.message})
    except Exception as e:
        return json.dumps({"error": "Error adding reaction", "message": str(e)})


@mcp.tool()
async def discord_pin_message(
    channel_id: Annotated[
        str,
        Field(description="The ID of the Discord channel containing the message. Required."),
    ],
    message_id: Annotated[
        str,
        Field(description="The ID of the message to pin. Required."),
    ],
) -> str:
    """Pin a message in a Discord channel.

    Args:
        channel_id: The ID of the channel containing the message.
        message_id: The ID of the message to pin.

    Returns:
        JSON confirmation of the message being pinned.
    """
    if not channel_id:
        return json.dumps({"error": "Validation Error", "message": "channel_id is required"})
    if not message_id:
        return json.dumps({"error": "Validation Error", "message": "message_id is required"})

    try:
        result = await client.pin_message(channel_id=channel_id, message_id=message_id)
        return json.dumps(result, ensure_ascii=False, indent=2)
    except DiscordBotAuthError as e:
        return json.dumps({"error": "Authentication Error", "message": e.message})
    except DiscordBotAPIError as e:
        return json.dumps({"error": "API Error", "message": e.message})
    except Exception as e:
        return json.dumps({"error": "Error pinning message", "message": str(e)})


@mcp.tool()
async def discord_create_dm(
    recipient_id: Annotated[
        str,
        Field(description="The Discord user ID of the recipient. Required."),
    ],
) -> str:
    """Open a direct message (DM) channel with a Discord user.

    Creates or retrieves the DM channel with the specified user.

    Args:
        recipient_id: The Discord user ID to open a DM with.

    Returns:
        JSON object with the DM channel ID, which can be used with other tools.
    """
    if not recipient_id:
        return json.dumps({"error": "Validation Error", "message": "recipient_id is required"})

    try:
        result = await client.create_dm(recipient_id=recipient_id)
        return json.dumps(result, ensure_ascii=False, indent=2)
    except DiscordBotAuthError as e:
        return json.dumps({"error": "Authentication Error", "message": e.message})
    except DiscordBotAPIError as e:
        return json.dumps({"error": "API Error", "message": e.message})
    except Exception as e:
        return json.dumps({"error": "Error creating DM channel", "message": str(e)})


@mcp.tool()
async def discord_send_dm(
    recipient_id: Annotated[
        str,
        Field(description="The Discord user ID of the recipient. Required."),
    ],
    content: Annotated[
        str,
        Field(description="The text content of the direct message. Required."),
    ],
) -> str:
    """Send a direct message (DM) to a Discord user.

    Args:
        recipient_id: The Discord user ID to send the DM to.
        content: The text content of the direct message.

    Returns:
        JSON object with the sent message details.
    """
    if not recipient_id:
        return json.dumps({"error": "Validation Error", "message": "recipient_id is required"})
    if not content:
        return json.dumps({"error": "Validation Error", "message": "content is required"})

    try:
        result = await client.send_dm(recipient_id=recipient_id, content=content)
        return json.dumps(result, ensure_ascii=False, indent=2)
    except DiscordBotAuthError as e:
        return json.dumps({"error": "Authentication Error", "message": e.message})
    except DiscordBotAPIError as e:
        return json.dumps({"error": "API Error", "message": e.message})
    except Exception as e:
        return json.dumps({"error": "Error sending DM", "message": str(e)})
