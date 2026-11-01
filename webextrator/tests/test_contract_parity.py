"""Check real MCP validation through to the outgoing browser API body."""

import json
from unittest.mock import AsyncMock

import httpx
import pytest
from mcp.server.fastmcp.exceptions import ToolError

import tools  # noqa: F401
from core.server import mcp
from tools import extract_tools


@pytest.mark.asyncio
@pytest.mark.parametrize("tool_name", ["webextrator_extract", "webextrator_render"])
async def test_cookie_and_cache_controls_reach_http(monkeypatch, tool_name):
    captured = {}

    async def post(_client, url, **kwargs):
        captured.update(kwargs["json"])
        return httpx.Response(
            200, json={"success": True, "data": {}}, request=httpx.Request("POST", url)
        )

    monkeypatch.setattr(httpx.AsyncClient, "post", post)
    monkeypatch.setattr(extract_tools.client, "api_token", "test-token")
    cookie = {
        "name": "session",
        "value": "test-value",
        "domain": "example.com",
        "httpOnly": False,
        "sameSite": "Lax",
    }
    await mcp.call_tool(
        tool_name,
        {
            "url": "https://example.com",
            "cookies": [cookie],
            "bypass_cache": False,
            "cache_ttl_seconds": 0,
            "timeout": 2,
            "delay": 0,
        },
    )
    assert captured["cookies"] == [cookie]
    assert captured["bypass_cache"] is False
    assert captured["cache_ttl_seconds"] == 0
    assert captured["timeout"] == 2
    assert captured["delay"] == 0


@pytest.mark.asyncio
@pytest.mark.parametrize("tool_name", ["webextrator_extract", "webextrator_render"])
@pytest.mark.parametrize(
    "field,value",
    [
        ("timeout", 0),
        ("timeout", 2.5),
        ("delay", -1),
        ("delay", 0.5),
        ("cache_ttl_seconds", -1),
        ("cache_ttl_seconds", 0.5),
    ],
)
async def test_invalid_integer_controls_fail_before_http(monkeypatch, tool_name, field, value):
    request = AsyncMock()
    monkeypatch.setattr(httpx.AsyncClient, "post", request)
    with pytest.raises(ToolError):
        await mcp.call_tool(tool_name, {"url": "https://example.com", field: value})
    request.assert_not_awaited()


@pytest.mark.asyncio
async def test_default_wait_condition_is_documented_without_overriding_api(monkeypatch):
    request = AsyncMock(return_value={"success": True, "data": {}})
    monkeypatch.setattr(extract_tools.client, "render", request)
    result = await extract_tools.webextrator_render(url="https://example.com")
    assert json.loads(result)["success"] is True
    assert request.await_args.kwargs["wait_until"] is None
    schema = mcp._tool_manager._tools["webextrator_render"].parameters
    assert "Default is 'load'" in schema["properties"]["wait_until"]["description"]
    assert {"name", "value", "domain"} <= set(schema["$defs"]["Cookie"]["required"])
