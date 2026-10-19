"""Protocol dispatch tests for Fish information tools."""

import json
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


@pytest.mark.asyncio
@pytest.mark.parametrize(("self_only", "has_more"), [(True, False), (True, True), (False, None)])
async def test_list_models_preserves_pagination_and_forwards_filters(
    monkeypatch: pytest.MonkeyPatch, self_only: bool, has_more: bool | None
) -> None:
    payload = {"total": 0, "items": [], "has_more": has_more}
    request = AsyncMock(return_value=payload)
    monkeypatch.setattr(info_tools.client, "request", request)

    result = json.loads(
        await info_tools.fish_list_models(
            self_=self_only, page_size=5, page_number=2, author_id="author", sort_by="created_at"
        )
    )

    assert result == payload
    request.assert_awaited_once_with(
        "GET",
        "/fish/model",
        params={
            "self": self_only,
            "page_size": 5,
            "page_number": 2,
            "author_id": "author",
            "sort_by": "created_at",
        },
    )


@pytest.mark.asyncio
async def test_self_title_language_conflict_makes_no_request(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    request = AsyncMock()
    monkeypatch.setattr(info_tools.client, "request", request)

    result = await mcp.call_tool("fish_list_models", {"self": True, "title_language": "en"})

    assert "title_language is not supported with self=true" in str(result)
    request.assert_not_awaited()


@pytest.mark.asyncio
@pytest.mark.parametrize("self_only", [None, False])
async def test_public_library_supports_title_language(
    monkeypatch: pytest.MonkeyPatch, self_only: bool | None
) -> None:
    request = AsyncMock(return_value={"total": 0, "items": [], "has_more": None})
    monkeypatch.setattr(info_tools.client, "request", request)

    await info_tools.fish_list_models(self_=self_only, title_language="en")

    params = {"title_language": "en"}
    if self_only is not None:
        params["self"] = self_only
    request.assert_awaited_once_with("GET", "/fish/model", params=params)


@pytest.mark.asyncio
async def test_discovery_guidance_explains_public_saved_voices() -> None:
    guide = await info_tools.fish_get_usage_guide()
    properties = mcp._tool_manager._tools["fish_list_models"].parameters["properties"]

    assert "saved voices remain public" in guide
    assert "not supported with self=true" in guide
    assert "may be null" in guide
    assert "across its API tokens" in properties["self"]["description"]
    assert "does not restrict public use" in properties["self"]["description"]
