"""Unit tests for HTTP client."""

from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from core.client import AiChatClient
from core.exceptions import AiChatAPIError, AiChatAuthError, AiChatTimeoutError


@pytest.fixture
def client():
    """Create a client instance for testing."""
    return AiChatClient(api_token="test-token", base_url="https://api.test.com")


class TestAiChatClient:
    """Tests for AiChatClient class."""

    def test_init_with_params(self):
        """Test client initialization with explicit parameters."""
        client = AiChatClient(api_token="my-token", base_url="https://custom.api.com")
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
        client = AiChatClient(api_token="", base_url="https://api.test.com")
        with pytest.raises(AiChatAuthError, match="not configured"):
            client._get_headers()

    @pytest.mark.asyncio
    async def test_create_conversation_success(self, client, mock_conversation_response):
        """Test successful conversation creation."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_conversation_response

        with patch("httpx.AsyncClient") as mock_http_client:
            mock_instance = AsyncMock()
            mock_instance.post.return_value = mock_response
            mock_http_client.return_value.__aenter__.return_value = mock_instance

            result = await client.create_conversation(
                question="What is the capital of France?",
                model="gpt-4.1",
            )
            assert result == mock_conversation_response
            assert result["answer"] == "I am a highly intelligent question answering AI."

    @pytest.mark.asyncio
    async def test_create_conversation_with_id(self, client, mock_conversation_response):
        """Test conversation creation with existing conversation ID."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_conversation_response

        with patch("httpx.AsyncClient") as mock_http_client:
            mock_instance = AsyncMock()
            mock_instance.post.return_value = mock_response
            mock_http_client.return_value.__aenter__.return_value = mock_instance

            result = await client.create_conversation(
                question="Tell me more.",
                model="gpt-4.1",
                conversation_id="64a67fff-61dc-4801-8339-2c69334c61d6",
            )
            assert result == mock_conversation_response

            # Verify the payload included the conversation ID
            call_args = mock_instance.post.call_args
            payload = call_args[1]["json"]
            assert payload["id"] == "64a67fff-61dc-4801-8339-2c69334c61d6"

    @pytest.mark.asyncio
    async def test_create_conversation_auth_error_401(self, client):
        """Test 401 response raises auth error."""
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.json.return_value = {
            "error": {"code": "invalid_token", "message": "Invalid API token"}
        }
        mock_response.headers = {"content-type": "application/json"}
        mock_response.text = "Invalid API token"

        with patch("httpx.AsyncClient") as mock_http_client:
            mock_instance = AsyncMock()
            mock_instance.post.return_value = mock_response
            mock_http_client.return_value.__aenter__.return_value = mock_instance

            with pytest.raises(AiChatAuthError, match="Invalid API token"):
                await client.create_conversation(question="Hello", model="gpt-4.1")

    @pytest.mark.asyncio
    async def test_create_conversation_timeout(self, client):
        """Test timeout raises timeout error."""
        with patch("httpx.AsyncClient") as mock_http_client:
            mock_instance = AsyncMock()
            mock_instance.post.side_effect = httpx.TimeoutException("Timeout")
            mock_http_client.return_value.__aenter__.return_value = mock_instance

            with pytest.raises(AiChatTimeoutError, match="timed out"):
                await client.create_conversation(question="Hello", model="gpt-4.1")

    @pytest.mark.asyncio
    async def test_create_conversation_http_error(self, client):
        """Test HTTP error raises API error."""
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.json.return_value = {
            "error": {"code": "api_error", "message": "Internal Server Error"}
        }
        mock_response.headers = {"content-type": "application/json"}
        mock_response.text = "Internal Server Error"

        with patch("httpx.AsyncClient") as mock_http_client:
            mock_instance = AsyncMock()
            mock_instance.post.return_value = mock_response
            mock_http_client.return_value.__aenter__.return_value = mock_instance

            with pytest.raises(AiChatAPIError, match="Internal Server Error") as exc_info:
                await client.create_conversation(question="Hello", model="gpt-4.1")

            assert exc_info.value.status_code == 500

    @pytest.mark.asyncio
    async def test_create_conversation_payload_structure(self, client, mock_conversation_response):
        """Test that the payload is correctly structured."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_conversation_response

        with patch("httpx.AsyncClient") as mock_http_client:
            mock_instance = AsyncMock()
            mock_instance.post.return_value = mock_response
            mock_http_client.return_value.__aenter__.return_value = mock_instance

            await client.create_conversation(
                question="What is AI?",
                model="gpt-4o",
                stateful=True,
                references=["https://example.com"],
            )

            call_args = mock_instance.post.call_args
            payload = call_args[1]["json"]
            assert payload["question"] == "What is AI?"
            assert payload["model"] == "gpt-4o"
            assert payload["stateful"] is True
            assert payload["references"] == ["https://example.com"]
            assert "id" not in payload
            assert "preset" not in payload
