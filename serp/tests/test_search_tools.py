"""Unit tests for search tools."""

import json

import pytest

from tools.search_tools import mcp, serp_google_images, serp_google_search


@pytest.mark.asyncio
async def test_serp_google_search_passes_image_size_and_year_range(monkeypatch):
    """serp_google_search should forward docs-supported image_size and qdr:y."""
    captured: dict = {}

    async def mock_search(**kwargs):
        captured.update(kwargs)
        return {"images": []}

    monkeypatch.setattr("tools.search_tools.client.search", mock_search)

    result = await serp_google_search(
        query="aurora",
        search_type="images",
        time_range="qdr:y",
        image_size="20mp",
    )

    assert json.loads(result) == {"images": []}
    assert captured["query"] == "aurora"
    assert captured["type"] == "images"
    assert captured["range"] == "qdr:y"
    assert captured["image_size"] == "20mp"


@pytest.mark.asyncio
async def test_serp_google_images_passes_image_size(monkeypatch):
    """serp_google_images should pass image_size to base search tool."""
    captured: dict = {}

    async def mock_search(**kwargs):
        captured.update(kwargs)
        return {"images": []}

    monkeypatch.setattr("tools.search_tools.client.search", mock_search)

    await serp_google_images(query="mountains", image_size="large")

    assert captured["query"] == "mountains"
    assert captured["type"] == "images"
    assert captured["image_size"] == "large"


@pytest.mark.asyncio
async def test_serp_google_search_rejects_image_size_for_non_image_search(monkeypatch):
    """image_size is rejected unless the requested search type is images."""
    monkeypatch.setattr(
        "tools.search_tools.client.search",
        pytest.fail,
    )

    result = await serp_google_search(
        query="aurora",
        search_type="search",
        image_size="large",
    )

    assert json.loads(result) == {
        "error": "Error performing search",
        "message": "image_size is only valid when search_type is 'images'",
    }


@pytest.mark.asyncio
async def test_serp_google_search_schema_matches_openapi_constraints():
    """The MCP schema enforces the OpenAPI request-field limits."""
    tool = next(tool for tool in await mcp.list_tools() if tool.name == "serp_google_search")
    properties = tool.inputSchema["properties"]

    assert properties["query"]["minLength"] == 1
    assert properties["query"]["maxLength"] == 2048
    assert properties["query"]["pattern"] == r".*\S.*"

    for field in ("country", "language"):
        assert properties[field]["anyOf"][0]["minLength"] == 1
        assert properties[field]["anyOf"][0]["maxLength"] == 32

    for field in ("number", "page"):
        assert properties[field]["anyOf"][0]["minimum"] == 1
        assert properties[field]["anyOf"][0]["maximum"] == 100
