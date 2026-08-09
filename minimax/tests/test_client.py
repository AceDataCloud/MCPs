"""Unit tests for HTTP client."""

from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from core.client import MinimaxClient
from core.exceptions import MinimaxAPIError, MinimaxAuthError, MinimaxTimeoutError


@pytest.fixture
def client():
    """Create a client instance for testing."""
    return MinimaxClient(api_token="test-token", base_url="https://api.test.com")


class TestMinimaxClient:
    """Tests for MinimaxClient class."""

    def test_init_with_params(self):
        """Test client initialization with explicit parameters."""
        client = MinimaxClient(api_token="my-token", base_url="https://custom.api.com")
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
        client = MinimaxClient(api_token="", base_url="https://api.test.com")
        with pytest.raises(MinimaxAuthError, match="not configured"):
            client._get_headers()

    def test_with_async_callback_injects_documented_async_field(self, client):
        """Test async submission uses the documented async request field."""
        payload = {"model": "MiniMax-H3", "content": [{"type": "text", "text": "fox"}]}
        assert client._with_async_callback(payload)["async"] is True

    def test_with_async_callback_preserves_explicit_callback(self, client):
        """Test async submission preserves a user-provided callback."""
        payload = client._with_async_callback(
            {"model": "MiniMax-H3", "callback_url": "https://example.com/webhook"}
        )
        assert payload["callback_url"] == "https://example.com/webhook"

    @pytest.mark.asyncio
    async def test_request_success(self, client, mock_video_response):
        """Test successful API request."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_video_response

        with patch("httpx.AsyncClient") as mock_client:
            mock_instance = AsyncMock()
            mock_instance.post.return_value = mock_response
            mock_client.return_value.__aenter__.return_value = mock_instance

            result = await client.request(
                "/minimax/videos",
                {"model": "MiniMax-H3", "content": [{"type": "text", "text": "fox"}]},
            )
            assert result == mock_video_response

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

            with pytest.raises(MinimaxAuthError, match="Invalid API token"):
                await client.request("/minimax/videos", {})

    @pytest.mark.asyncio
    async def test_request_timeout(self, client):
        """Test timeout raises timeout error."""
        with patch("httpx.AsyncClient") as mock_client:
            mock_instance = AsyncMock()
            mock_instance.post.side_effect = httpx.TimeoutException("Timeout")
            mock_client.return_value.__aenter__.return_value = mock_instance

            with pytest.raises(MinimaxTimeoutError, match="timed out"):
                await client.request("/minimax/videos", {})

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

            with pytest.raises(MinimaxAPIError, match="Internal Server Error") as exc_info:
                await client.request("/minimax/videos", {})

            assert exc_info.value.status_code == 500

    @pytest.mark.asyncio
    async def test_request_worker_error_uses_documented_type(self, client):
        """Test documented WorkerError responses expose the worker error type."""
        mock_response = MagicMock()
        mock_response.status_code = 422
        mock_response.json.return_value = {
            "type": "error",
            "error": {
                "type": "unprocessable_entity_error",
                "message": "The request did not pass content safety checks.",
                "http_code": "422",
            },
            "request_id": "req_123",
        }
        mock_response.text = "worker error"

        with patch("httpx.AsyncClient") as mock_client:
            mock_instance = AsyncMock()
            mock_instance.post.return_value = mock_response
            mock_client.return_value.__aenter__.return_value = mock_instance

            with pytest.raises(MinimaxAPIError, match="content safety") as exc_info:
                await client.request("/minimax/videos", {})

            assert exc_info.value.code == "unprocessable_entity_error"
            assert exc_info.value.status_code == 422

    @pytest.mark.asyncio
    async def test_request_invalid_json_error_uses_documented_code(self, client):
        """Test documented InvalidJsonError responses expose the top-level code."""
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.json.return_value = {
            "code": "bad_request",
            "detail": "The request body must be a JSON object.",
        }
        mock_response.text = "bad request"

        with patch("httpx.AsyncClient") as mock_client:
            mock_instance = AsyncMock()
            mock_instance.post.return_value = mock_response
            mock_client.return_value.__aenter__.return_value = mock_instance

            with pytest.raises(MinimaxAPIError, match="JSON object") as exc_info:
                await client.request("/minimax/tasks", {})

            assert exc_info.value.code == "bad_request"
            assert exc_info.value.status_code == 400
