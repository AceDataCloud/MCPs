"""Unit tests for HTTP client."""

from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from core.client import AIChatClient
from core.exceptions import AIChatAPIError, AIChatAuthError, AIChatTimeoutError


@pytest.fixture
def client():
    """Create a client instance for testing."""
    return AIChatClient(api_token="test-token", base_url="https://api.test.com")


class TestAIChatClient:
    """Tests for AIChatClient class."""

    def test_init_with_params(self):
        """Test client initialization with explicit parameters."""
        client = AIChatClient(api_token="my-token", base_url="https://custom.api.com")
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
        client = AIChatClient(api_token="", base_url="https://api.test.com")
        with pytest.raises(AIChatAuthError, match="not configured"):
            client._get_headers()

    @pytest.mark.asyncio
    async def test_request_success(self, client, mock_conversation_response):
        """Test successful API request."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_conversation_response

        with patch("httpx.AsyncClient") as mock_http:
            mock_instance = AsyncMock()
            mock_instance.post.return_value = mock_response
            mock_http.return_value.__aenter__.return_value = mock_instance

            result = await client.request(
                "/aichat/conversations",
                {"model": "gpt-4.1", "question": "Hello!"},
            )
            assert result == mock_conversation_response

    @pytest.mark.asyncio
    async def test_request_auth_error_401(self, client):
        """Test 401 response raises auth error."""
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.json.return_value = {
            "error": {"code": "invalid_token", "message": "Invalid API token"}
        }
        mock_response.text = "Invalid API token"

        with patch("httpx.AsyncClient") as mock_http:
            mock_instance = AsyncMock()
            mock_instance.post.return_value = mock_response
            mock_http.return_value.__aenter__.return_value = mock_instance

            with pytest.raises(AIChatAuthError, match="Invalid API token"):
                await client.request("/aichat/conversations", {})

    @pytest.mark.asyncio
    async def test_request_timeout(self, client):
        """Test timeout raises timeout error."""
        with patch("httpx.AsyncClient") as mock_http:
            mock_instance = AsyncMock()
            mock_instance.post.side_effect = httpx.TimeoutException("Timeout")
            mock_http.return_value.__aenter__.return_value = mock_instance

            with pytest.raises(AIChatTimeoutError, match="timed out"):
                await client.request("/aichat/conversations", {})

    @pytest.mark.asyncio
    async def test_request_http_error(self, client):
        """Test HTTP error raises API error."""
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.json.return_value = {
            "error": {"code": "api_error", "message": "Internal Server Error"}
        }
        mock_response.text = "Internal Server Error"

        with patch("httpx.AsyncClient") as mock_http:
            mock_instance = AsyncMock()
            mock_instance.post.return_value = mock_response
            mock_http.return_value.__aenter__.return_value = mock_instance

            with pytest.raises(AIChatAPIError, match="Internal Server Error") as exc_info:
                await client.request("/aichat/conversations", {})

            assert exc_info.value.status_code == 500

    @pytest.mark.asyncio
    async def test_conversations_method(self, client, mock_conversation_response):
        """Test the conversations convenience method."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_conversation_response

        with patch("httpx.AsyncClient") as mock_http:
            mock_instance = AsyncMock()
            mock_instance.post.return_value = mock_response
            mock_http.return_value.__aenter__.return_value = mock_instance

            result = await client.conversations(
                model="gpt-4.1",
                question="What is machine learning?",
            )
            assert result == mock_conversation_response

            call_args = mock_instance.post.call_args
            assert "/aichat/conversations" in call_args[0][0]
