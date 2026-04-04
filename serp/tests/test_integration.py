"""Integration tests for SERP API.

These tests require a valid API token and will make real API calls.
Run with: pytest tests/test_integration.py -m integration
"""

import pytest

from core.client import SerpClient


@pytest.mark.integration
class TestSerpIntegration:
    """Integration tests for SERP API."""

    @pytest.mark.asyncio
    async def test_web_search(self, api_token):
        """Test basic web search."""
        client = SerpClient(api_token=api_token)
        result = await client.search(query="Python programming", type="search")

        assert "organic" in result
        assert len(result["organic"]) > 0
        assert "title" in result["organic"][0]
        assert "link" in result["organic"][0]

    @pytest.mark.asyncio
    async def test_news_search(self, api_token):
        """Test news search."""
        client = SerpClient(api_token=api_token)
        result = await client.search(query="technology news", type="news")

        assert "news" in result or "organic" in result

    @pytest.mark.asyncio
    async def test_image_search(self, api_token):
        """Test image search."""
        client = SerpClient(api_token=api_token)
        result = await client.search(query="sunset", type="images")

        assert "images" in result or "organic" in result

    @pytest.mark.asyncio
    async def test_knowledge_graph(self, api_token):
        """Test search with knowledge graph."""
        client = SerpClient(api_token=api_token)
        result = await client.search(query="Apple Inc", type="search")

        # Knowledge graph may or may not be present
        if "knowledge_graph" in result:
            assert "title" in result["knowledge_graph"]

    @pytest.mark.asyncio
    async def test_localized_search(self, api_token):
        """Test localized search with country and language."""
        client = SerpClient(api_token=api_token)
        result = await client.search(query="weather", type="search", country="uk", language="en")

        assert "organic" in result

    @pytest.mark.asyncio
    async def test_time_filtered_search(self, api_token):
        """Test search with time filter."""
        client = SerpClient(api_token=api_token)
        result = await client.search(query="AI news", type="news", range="qdr:d")

        assert "news" in result or "organic" in result
