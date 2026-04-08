"""Unit tests for HTTP client."""

from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from core.client import ShortURLClient
from core.exceptions import ShortURLAPIError, ShortURLAuthError, ShortURLTimeoutError


@pytest.fixture
def client():
    """Create a client instance for testing."""
    return ShortURLClient(api_token="test-token", base_url="https://api.test.com")


class TestShortURLClient:
    """Tests for ShortURLClient class."""

    def test_init_with_params(self):
        """Test client initialization with explicit parameters."""
        client = ShortURLClient(api_token="my-token", base_url="https://custom.api.com")
        assert client.api_token == "my-token"
        assert client.base_url == "https://custom.api.com"

    def test_get_headers(self, client):
        """Test that headers are correctly generated."""
        headers = client._get_headers()
        assert headers["accept"] == "application/json"
        assert headers["authorization"] == "Bearer test-token"
        assert headers["content-type"] == "application/json"

    def test_get_headers_no_token(self):
        """Test that missing token raises auth error."""
        client = ShortURLClient(api_token="", base_url="https://api.test.com")
        with pytest.raises(ShortURLAuthError, match="not configured"):
            client._get_headers()

    @pytest.mark.asyncio
    async def test_request_success(self, client, mock_shorten_response):
        """Test successful API request."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_shorten_response

        with patch("httpx.AsyncClient") as mock_client:
            mock_instance = AsyncMock()
            mock_instance.post.return_value = mock_response
            mock_client.return_value.__aenter__.return_value = mock_instance

            result = await client.request("/shorturl", {"content": "https://example.com"})
            assert result == mock_shorten_response
            assert result["success"] is True
            assert result["data"]["url"] == "https://surl.id/1uHCs01xa5"

    @pytest.mark.asyncio
    async def test_request_auth_error_401(self, client):
        """Test 401 response raises auth error."""
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.json.return_value = {
            "error": {"code": "unauthorized", "message": "Invalid API token"}
        }
        mock_response.headers = {"content-type": "application/json"}
        mock_response.text = "Invalid API token"

        with patch("httpx.AsyncClient") as mock_client:
            mock_instance = AsyncMock()
            mock_instance.post.return_value = mock_response
            mock_client.return_value.__aenter__.return_value = mock_instance

            with pytest.raises(ShortURLAuthError, match="Invalid API token"):
                await client.request("/shorturl", {})

    @pytest.mark.asyncio
    async def test_request_auth_error_403(self, client):
        """Test 403 response raises auth error."""
        mock_response = MagicMock()
        mock_response.status_code = 403
        mock_response.json.return_value = {
            "error": {"code": "forbidden", "message": "Access denied"}
        }
        mock_response.headers = {"content-type": "application/json"}
        mock_response.text = "Access denied"

        with patch("httpx.AsyncClient") as mock_client:
            mock_instance = AsyncMock()
            mock_instance.post.return_value = mock_response
            mock_client.return_value.__aenter__.return_value = mock_instance

            with pytest.raises(ShortURLAuthError, match="Access denied"):
                await client.request("/shorturl", {})

    @pytest.mark.asyncio
    async def test_request_timeout(self, client):
        """Test timeout raises timeout error."""
        with patch("httpx.AsyncClient") as mock_client:
            mock_instance = AsyncMock()
            mock_instance.post.side_effect = httpx.TimeoutException("Timeout")
            mock_client.return_value.__aenter__.return_value = mock_instance

            with pytest.raises(ShortURLTimeoutError, match="timed out"):
                await client.request("/shorturl", {})

    @pytest.mark.asyncio
    async def test_request_http_error(self, client):
        """Test HTTP error raises API error."""
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.json.return_value = {
            "error": {"code": "internal_error", "message": "Internal Server Error"}
        }
        mock_response.headers = {"content-type": "application/json"}
        mock_response.text = "Internal Server Error"

        with patch("httpx.AsyncClient") as mock_client:
            mock_instance = AsyncMock()
            mock_instance.post.return_value = mock_response
            mock_client.return_value.__aenter__.return_value = mock_instance

            with pytest.raises(ShortURLAPIError, match="Internal Server Error") as exc_info:
                await client.request("/shorturl", {})

            assert exc_info.value.status_code == 500

    @pytest.mark.asyncio
    async def test_shorten_method(self, client, mock_shorten_response):
        """Test the shorten convenience method."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_shorten_response

        with patch("httpx.AsyncClient") as mock_client:
            mock_instance = AsyncMock()
            mock_instance.post.return_value = mock_response
            mock_client.return_value.__aenter__.return_value = mock_instance

            result = await client.shorten(content="https://example.com/long-url")
            assert result == mock_shorten_response

            # Verify the correct endpoint was called
            call_args = mock_instance.post.call_args
            assert "/shorturl" in call_args[0][0]
            assert call_args[1]["json"] == {"content": "https://example.com/long-url"}
