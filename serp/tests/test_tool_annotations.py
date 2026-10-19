"""Verify the public MCP tool catalog and safe reference calls."""

from unittest.mock import AsyncMock

import pytest

from core.client import client
from core.server import mcp
from tools import info_tools, search_tools  # noqa: F401


@pytest.mark.asyncio
async def test_catalog_distinguishes_local_reference_from_billable_search():
    tools = await mcp.list_tools()
    assert len(tools) == 11
    for tool in tools:
        public = tool.model_dump(by_alias=True, exclude_none=True)
        assert public["title"]
        hints = public["annotations"]
        assert hints["readOnlyHint"] is True
        assert hints["destructiveHint"] is False
        is_search = tool.name.startswith("serp_google_")
        assert hints["openWorldHint"] is is_search
        # Repeating an API search can consume additional Credits.
        assert hints["idempotentHint"] is (not is_search)


@pytest.mark.asyncio
async def test_reference_first_call_does_not_call_search_api(monkeypatch):
    search = AsyncMock(side_effect=AssertionError("Reference calls must stay local"))
    monkeypatch.setattr(client, "search", search)
    result = await mcp.call_tool("serp_list_search_types", {})
    assert result
    search.assert_not_awaited()
