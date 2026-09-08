"""Unit tests for ShortURL tools."""

from unittest.mock import AsyncMock, patch

import pytest

from core.server import mcp
from tools import shorturl_tools  # noqa: F401


class TestShortURLCreateTool:
    @pytest.mark.asyncio
    async def test_fastmcp_dispatch_uses_openapi_content_parameter(self) -> None:
        tools = {tool.name: tool for tool in await mcp.list_tools()}
        properties = tools["shorturl_create"].inputSchema["properties"]

        assert "content" in properties
        assert "url" not in properties

        with patch(
            "tools.shorturl_tools.client.shorten",
            new=AsyncMock(return_value={"success": True, "data": {"url": "https://surl.id/abc"}}),
        ) as mock_shorten:
            result = await mcp.call_tool("shorturl_create", {"content": "https://example.com"})

        assert result
        mock_shorten.assert_awaited_once_with(content="https://example.com")

    @pytest.mark.asyncio
    async def test_fastmcp_dispatch_still_accepts_legacy_url_parameter(self) -> None:
        with patch(
            "tools.shorturl_tools.client.shorten",
            new=AsyncMock(return_value={"success": True, "data": {"url": "https://surl.id/abc"}}),
        ) as mock_shorten:
            result = await mcp.call_tool("shorturl_create", {"url": "https://example.com"})

        assert result
        mock_shorten.assert_awaited_once_with(content="https://example.com")
