"""Unit tests for Realtime API helper tools."""

import json

import pytest

from core.server import mcp
from tools import realtime_tools


def test_openai_get_realtime_connection_info_registered():
    """The realtime helper tool must be registered with the MCP server."""
    tool_names = [tool.name for tool in mcp._tool_manager.list_tools()]
    assert "openai_get_realtime_connection_info" in tool_names


def test_openai_get_realtime_connection_info_schema():
    """The MCP schema must expose the documented realtime model options."""
    tool = next(
        tool
        for tool in mcp._tool_manager.list_tools()
        if tool.name == "openai_get_realtime_connection_info"
    )
    model_schema = tool.parameters["properties"]["model"]

    assert model_schema["default"] == "gpt-realtime"
    assert model_schema["enum"] == ["gpt-realtime", "gpt-realtime-2"]


@pytest.mark.asyncio
async def test_openai_get_realtime_connection_info_returns_websocket_url(monkeypatch):
    """The helper should translate the configured HTTPS base URL to a WSS endpoint."""
    monkeypatch.setattr(realtime_tools.settings, "api_base_url", "https://api.test.com")

    response = await realtime_tools.openai_get_realtime_connection_info(model="gpt-realtime-2")
    result = json.loads(response)

    assert result["url"] == "wss://api.test.com/v1/realtime?model=gpt-realtime-2"
    assert result["model"] == "gpt-realtime-2"
