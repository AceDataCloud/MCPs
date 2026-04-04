"""Integration tests for ShortURL API.

These tests require a valid API token and will make real API calls.
Run with: pytest tests/test_integration.py -m integration
"""

import pytest

from core.client import ShortURLClient


@pytest.mark.integration
class TestShortURLIntegration:
    """Integration tests for ShortURL API."""

    @pytest.mark.asyncio
    async def test_shorten_url(self, api_token):
        """Test basic URL shortening."""
        client = ShortURLClient(api_token=api_token)
        result = await client.shorten(
            content="https://platform.acedata.cloud/documents/a2303356-6672-4eb8-9778-75f55c998fe9"
        )

        assert result["success"] is True
        assert "data" in result
        assert "url" in result["data"]
        assert result["data"]["url"].startswith("https://")

    @pytest.mark.asyncio
    async def test_shorten_simple_url(self, api_token):
        """Test shortening a simple URL."""
        client = ShortURLClient(api_token=api_token)
        result = await client.shorten(content="https://www.google.com")

        assert result["success"] is True
        assert "data" in result
        assert "url" in result["data"]

    @pytest.mark.asyncio
    async def test_shorten_url_with_params(self, api_token):
        """Test shortening a URL with query parameters."""
        client = ShortURLClient(api_token=api_token)
        result = await client.shorten(
            content="https://example.com/path?param1=value1&param2=value2#section"
        )

        assert result["success"] is True
        assert "data" in result
        assert "url" in result["data"]
