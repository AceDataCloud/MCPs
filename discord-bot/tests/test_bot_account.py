"""Discord application bot mode uses only the official API and dedicated token."""

from unittest.mock import patch

import httpx
import pytest
import respx

from core.bot_account import discord_list_guilds, discord_whoami
from main import main


@respx.mock
async def test_bot_account_requests(monkeypatch):
    monkeypatch.setenv("DISCORDBOT_TOKEN", "test-application-credential")
    monkeypatch.setenv("DISCORD_BOT_TOKEN", "test-proxy-credential")
    monkeypatch.setenv("DISCORD_BOT_BASE_URL", "https://proxy.invalid")
    whoami = respx.get("https://discord.com/api/v10/users/@me").mock(
        return_value=httpx.Response(200, json={"id": "1", "username": "Test", "bot": True})
    )
    guilds = respx.get(
        "https://discord.com/api/v10/users/@me/guilds", params={"limit": "200", "after": "2"}
    ).mock(return_value=httpx.Response(200, json=[{"id": "3", "name": "Test Guild"}]))
    assert await discord_whoami() == {"id": "1", "username": "Test"}
    assert await discord_list_guilds(after="2") == [{"id": "3", "name": "Test Guild"}]
    for route in [whoami, guilds]:
        assert (
            route.calls.last.request.headers["Authorization"] == "Bot test-application-credential"
        )
        assert route.calls.last.request.headers["User-Agent"].startswith("DiscordBot (")


@respx.mock
async def test_missing_bot_token_ignores_proxy_credential(monkeypatch):
    monkeypatch.delenv("DISCORDBOT_TOKEN", raising=False)
    monkeypatch.setenv("DISCORD_BOT_TOKEN", "test-proxy-credential")
    with pytest.raises(ValueError, match="DISCORDBOT_TOKEN"):
        await discord_whoami()
    assert not respx.calls


@respx.mock
async def test_whoami_requires_a_bot_identity(monkeypatch):
    monkeypatch.setenv("DISCORDBOT_TOKEN", "test-application-credential")
    respx.get("https://discord.com/api/v10/users/@me").mock(
        return_value=httpx.Response(200, json={"id": "1", "username": "Test"})
    )
    with pytest.raises(ValueError, match="as a bot"):
        await discord_whoami()


def test_select_bot_mode(monkeypatch):
    monkeypatch.setattr("sys.argv", ["mcp-discord-bot", "--bot-account"])
    with patch("core.bot_account.mcp.run") as run:
        main()
    run.assert_called_once_with(transport="stdio")
