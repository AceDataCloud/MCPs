"""Unit tests for HTTP client."""

from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from core.client import DiscordBotClient
from core.exceptions import DiscordBotAPIError, DiscordBotAuthError, DiscordBotTimeoutError


@pytest.fixture
def bot_client():
    """Create a client instance for testing."""
    return DiscordBotClient(
        bot_token="test-token",
        base_url="https://discord-bot-test.app.acedata.cloud",
    )


class TestDiscordBotClient:
    """Tests for DiscordBotClient class."""

    def test_init_with_params(self):
        """Test client initialization with explicit parameters."""
        client = DiscordBotClient(
            bot_token="my-token",
            base_url="https://discord-bot-test.app.acedata.cloud",
        )
        assert client.bot_token == "my-token"
        assert client.base_url == "https://discord-bot-test.app.acedata.cloud"

    def test_base_url_trailing_slash_stripped(self):
        """Test that trailing slash is stripped from base URL."""
        client = DiscordBotClient(
            bot_token="my-token",
            base_url="https://discord-bot-test.app.acedata.cloud/",
        )
        assert client.base_url == "https://discord-bot-test.app.acedata.cloud"

    def test_get_headers(self, bot_client):
        """Test that headers are correctly generated."""
        headers = bot_client._get_headers()
        assert headers["accept"] == "application/json"
        assert headers["authorization"] == "test-token"
        assert headers["content-type"] == "application/json"

    def test_get_headers_no_token(self):
        """Test that missing token raises auth error."""
        client = DiscordBotClient(
            bot_token="", base_url="https://discord-bot-test.app.acedata.cloud"
        )
        with pytest.raises(DiscordBotAuthError, match="not configured"):
            client._get_headers()

    @pytest.mark.asyncio
    async def test_request_success_with_data_envelope(self, bot_client, mock_whoami_response):
        """Test successful API request unwraps data envelope."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'{"data": {"id": "123"}}'
        mock_response.json.return_value = {"data": mock_whoami_response}

        with patch("httpx.AsyncClient") as mock_client:
            mock_instance = AsyncMock()
            mock_instance.request.return_value = mock_response
            mock_client.return_value.__aenter__.return_value = mock_instance

            result = await bot_client._request("GET", "/api/whoami")
            assert result == mock_whoami_response

    @pytest.mark.asyncio
    async def test_request_success_without_data_envelope(self, bot_client, mock_guilds_response):
        """Test successful API request without data envelope returns raw result."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b"[...]"
        mock_response.json.return_value = mock_guilds_response

        with patch("httpx.AsyncClient") as mock_client:
            mock_instance = AsyncMock()
            mock_instance.request.return_value = mock_response
            mock_client.return_value.__aenter__.return_value = mock_instance

            result = await bot_client._request("GET", "/api/guilds")
            assert result == mock_guilds_response

    @pytest.mark.asyncio
    async def test_request_auth_error_401(self, bot_client):
        """Test 401 response raises auth error."""
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.json.return_value = {"error": "Invalid token"}
        mock_response.text = "Invalid token"

        with patch("httpx.AsyncClient") as mock_client:
            mock_instance = AsyncMock()
            mock_instance.request.return_value = mock_response
            mock_client.return_value.__aenter__.return_value = mock_instance

            with pytest.raises(DiscordBotAuthError, match="Invalid token"):
                await bot_client._request("GET", "/api/whoami")

    @pytest.mark.asyncio
    async def test_request_auth_error_403(self, bot_client):
        """Test 403 response raises auth error."""
        mock_response = MagicMock()
        mock_response.status_code = 403
        mock_response.json.return_value = {"error": "Forbidden"}
        mock_response.text = "Forbidden"

        with patch("httpx.AsyncClient") as mock_client:
            mock_instance = AsyncMock()
            mock_instance.request.return_value = mock_response
            mock_client.return_value.__aenter__.return_value = mock_instance

            with pytest.raises(DiscordBotAuthError, match="Forbidden"):
                await bot_client._request("GET", "/api/guilds")

    @pytest.mark.asyncio
    async def test_request_api_error(self, bot_client):
        """Test API error response raises DiscordBotAPIError."""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"error": "Channel not found"}
        mock_response.text = "Channel not found"

        with patch("httpx.AsyncClient") as mock_client:
            mock_instance = AsyncMock()
            mock_instance.request.return_value = mock_response
            mock_client.return_value.__aenter__.return_value = mock_instance

            with pytest.raises(DiscordBotAPIError, match="Channel not found") as exc_info:
                await bot_client._request("GET", "/api/channels/invalid/messages")

            assert exc_info.value.status_code == 404

    @pytest.mark.asyncio
    async def test_request_timeout(self, bot_client):
        """Test timeout raises DiscordBotTimeoutError."""
        with patch("httpx.AsyncClient") as mock_client:
            mock_instance = AsyncMock()
            mock_instance.request.side_effect = httpx.TimeoutException("Timeout")
            mock_client.return_value.__aenter__.return_value = mock_instance

            with pytest.raises(DiscordBotTimeoutError, match="timed out"):
                await bot_client._request("GET", "/api/whoami")

    @pytest.mark.asyncio
    async def test_request_no_content(self, bot_client):
        """Test 204 No Content returns None."""
        mock_response = MagicMock()
        mock_response.status_code = 204
        mock_response.content = b""

        with patch("httpx.AsyncClient") as mock_client:
            mock_instance = AsyncMock()
            mock_instance.request.return_value = mock_response
            mock_client.return_value.__aenter__.return_value = mock_instance

            result = await bot_client._request("DELETE", "/api/channels/123/messages/456")
            assert result is None

    @pytest.mark.asyncio
    async def test_whoami(self, bot_client, mock_whoami_response):
        """Test whoami method."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'{"data": {}}'
        mock_response.json.return_value = {"data": mock_whoami_response}

        with patch("httpx.AsyncClient") as mock_client:
            mock_instance = AsyncMock()
            mock_instance.request.return_value = mock_response
            mock_client.return_value.__aenter__.return_value = mock_instance

            result = await bot_client.whoami()
            assert result == mock_whoami_response

            call_args = mock_instance.request.call_args
            assert call_args[1]["method"] == "GET"
            assert "/api/whoami" in call_args[1]["url"]

    @pytest.mark.asyncio
    async def test_send_message(self, bot_client, mock_message_response):
        """Test send_message method."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'{"data": {}}'
        mock_response.json.return_value = {"data": mock_message_response}

        with patch("httpx.AsyncClient") as mock_client:
            mock_instance = AsyncMock()
            mock_instance.request.return_value = mock_response
            mock_client.return_value.__aenter__.return_value = mock_instance

            result = await bot_client.send_message(
                channel_id="333333333333333333", content="Hello!"
            )
            assert result == mock_message_response

            call_args = mock_instance.request.call_args
            assert call_args[1]["method"] == "POST"
            assert "/api/messages" in call_args[1]["url"]
            assert call_args[1]["json"]["channel_id"] == "333333333333333333"
            assert call_args[1]["json"]["content"] == "Hello!"

    @pytest.mark.asyncio
    async def test_send_message_with_reply(self, bot_client, mock_message_response):
        """Test send_message method with reply_to parameter."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'{"data": {}}'
        mock_response.json.return_value = {"data": mock_message_response}

        with patch("httpx.AsyncClient") as mock_client:
            mock_instance = AsyncMock()
            mock_instance.request.return_value = mock_response
            mock_client.return_value.__aenter__.return_value = mock_instance

            await bot_client.send_message(
                channel_id="333333333333333333",
                content="Reply here!",
                reply_to="555555555555555555",
            )

            call_args = mock_instance.request.call_args
            assert call_args[1]["json"]["reply_to"] == "555555555555555555"

    @pytest.mark.asyncio
    async def test_read_messages_with_limit(self, bot_client, mock_messages_response):
        """Test read_messages method with limit."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b"[...]"
        mock_response.json.return_value = mock_messages_response

        with patch("httpx.AsyncClient") as mock_client:
            mock_instance = AsyncMock()
            mock_instance.request.return_value = mock_response
            mock_client.return_value.__aenter__.return_value = mock_instance

            result = await bot_client.read_messages(channel_id="333333333333333333", limit=10)
            assert result == mock_messages_response

            call_args = mock_instance.request.call_args
            assert call_args[1]["params"]["limit"] == 10

    @pytest.mark.asyncio
    async def test_delete_message(self, bot_client):
        """Test delete_message method."""
        mock_response = MagicMock()
        mock_response.status_code = 204
        mock_response.content = b""

        with patch("httpx.AsyncClient") as mock_client:
            mock_instance = AsyncMock()
            mock_instance.request.return_value = mock_response
            mock_client.return_value.__aenter__.return_value = mock_instance

            result = await bot_client.delete_message(
                channel_id="333333333333333333", message_id="555555555555555555"
            )
            assert result is None

            call_args = mock_instance.request.call_args
            assert call_args[1]["method"] == "DELETE"
