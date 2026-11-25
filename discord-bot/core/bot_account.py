"""Read-only MCP tools for an installed Discord application bot."""

import os
from importlib.metadata import version
from typing import Any

import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("discord-bot-account")


async def _get(path: str, params: dict[str, str] | None = None) -> Any:
    token = os.environ.get("DISCORDBOT_TOKEN", "").strip()
    if not token:
        raise ValueError("Set DISCORDBOT_TOKEN to your Discord application's bot token.")
    headers = {
        "Authorization": f"Bot {token}",
        "User-Agent": (
            f"DiscordBot (https://github.com/AceDataCloud/DiscordBotMCP, {version('mcp-discord-bot')})"
        ),
    }
    async with httpx.AsyncClient(
        base_url="https://discord.com/api/v10/", headers=headers
    ) as client:
        response = await client.get(path, params=params)
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def discord_whoami() -> dict[str, str]:
    """Get the bot's Discord ID and username."""
    user = await _get("users/@me")
    if user.get("bot") is not True:
        raise ValueError("Discord did not identify this account as a bot.")
    return {"id": user["id"], "username": user["username"]}


@mcp.tool()
async def discord_list_guilds(after: str | None = None) -> list[dict[str, str]]:
    """List up to 200 servers the bot has joined. Pass the last server ID as after to continue."""
    params = {"limit": "200"}
    if after is not None:
        params["after"] = after
    guilds = await _get("users/@me/guilds", params)
    return [{"id": guild["id"], "name": guild["name"]} for guild in guilds]
