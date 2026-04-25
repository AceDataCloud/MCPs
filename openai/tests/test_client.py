"""Unit tests for HTTP client."""

from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from core.client import OpenaiClient
from core.exceptions import OpenaiAPIError, OpenaiAuthError, OpenaiTimeoutError


@pytest.fixture
def client():
    """Create a client instance for testing."""
    return OpenaiClient(api_token="test-token", base_url="https://api.test.com")


class TestOpenaiClient:
    """Tests for OpenaiClient class."""

    def test_init_with_params(self):
        """Test client initialization with explicit parameters."""
        c = OpenaiClient(api_token="my-token", base_url="https://custom.api.com")
        assert c.api_token == "my-token"
        assert c.base_url == "https://custom.api.com"

    def test_get_headers(self, client):
        """Test that headers are correctly generated."""
        headers = client._get_headers()
        assert headers["accept"] == "application/json"
        assert headers["authorization"] == "Bearer test-token"
        assert headers["content-type"] == "application/json"

    def test_get_headers_no_token(self):
        """Test that missing token raises auth error."""
        c = OpenaiClient(api_token="", base_url="https://api.test.com")
        with pytest.raises(OpenaiAuthError, match="not configured"):
            c._get_headers()

    @pytest.mark.asyncio
    async def test_request_success(self, client, mock_chat_response):
        """Test successful API request."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_chat_response

        with patch("httpx.AsyncClient") as mock_http:
            mock_instance = AsyncMock()
            mock_instance.post.return_value = mock_response
            mock_http.return_value.__aenter__.return_value = mock_instance

            result = await client.request(
                "/openai/chat/completions",
                {"model": "gpt-4o", "messages": []},
            )
            assert result == mock_chat_response

    @pytest.mark.asyncio
    async def test_request_auth_error_401(self, client):
        """Test 401 response raises auth error."""
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.json.return_value = {
            "error": {"code": "unauthorized", "message": "Invalid API token"}
        }
        mock_response.text = "Invalid API token"

        with patch("httpx.AsyncClient") as mock_http:
            mock_instance = AsyncMock()
            mock_instance.post.return_value = mock_response
            mock_http.return_value.__aenter__.return_value = mock_instance

            with pytest.raises(OpenaiAuthError, match="Invalid API token"):
                await client.request("/openai/chat/completions", {})

    @pytest.mark.asyncio
    async def test_request_timeout(self, client):
        """Test timeout raises timeout error."""
        with patch("httpx.AsyncClient") as mock_http:
            mock_instance = AsyncMock()
            mock_instance.post.side_effect = httpx.TimeoutException("Timeout")
            mock_http.return_value.__aenter__.return_value = mock_instance

            with pytest.raises(OpenaiTimeoutError, match="timed out"):
                await client.request("/openai/chat/completions", {})

    @pytest.mark.asyncio
    async def test_request_http_error(self, client):
        """Test HTTP error raises API error."""
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.json.return_value = {
            "error": {"code": "internal_error", "message": "Internal Server Error"}
        }
        mock_response.text = "Internal Server Error"

        with patch("httpx.AsyncClient") as mock_http:
            mock_instance = AsyncMock()
            mock_instance.post.return_value = mock_response
            mock_http.return_value.__aenter__.return_value = mock_instance

            with pytest.raises(OpenaiAPIError, match="Internal Server Error") as exc_info:
                await client.request("/openai/chat/completions", {})

            assert exc_info.value.status_code == 500

    @pytest.mark.asyncio
    async def test_chat_completion_method(self, client, mock_chat_response):
        """Test the chat_completion convenience method."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_chat_response

        with patch("httpx.AsyncClient") as mock_http:
            mock_instance = AsyncMock()
            mock_instance.post.return_value = mock_response
            mock_http.return_value.__aenter__.return_value = mock_instance

            result = await client.chat_completion(
                model="gpt-4o", messages=[{"role": "user", "content": "Hello"}]
            )
            assert result == mock_chat_response

            call_args = mock_instance.post.call_args
            assert "/openai/chat/completions" in call_args[0][0]
