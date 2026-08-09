"""Unit tests for search tools."""

import json

import pytest

from tools.search_tools import serp_google_images, serp_google_search


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
