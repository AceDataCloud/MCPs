"""Protocol dispatch tests for Fish information tools."""

from unittest.mock import AsyncMock

import pytest

from core.server import mcp
from tools import info_tools


@pytest.mark.asyncio
async def test_fastmcp_dispatch_maps_public_self_parameter(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    request = AsyncMock(return_value={"items": []})
    monkeypatch.setattr(info_tools.client, "request", request)
    tools = {tool.name: tool for tool in await mcp.list_tools()}
    properties = tools["fish_list_models"].inputSchema["properties"]

    assert "self" in properties
    assert "self_" not in properties

    result = await mcp.call_tool("fish_list_models", {"self": True})

    assert result
    request.assert_awaited_once_with("GET", "/fish/model", params={"self": True})
