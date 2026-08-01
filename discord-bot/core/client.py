"""HTTP client for Discord Agent Proxy REST API."""

import contextvars
import json
from typing import Any

import httpx
from loguru import logger

from core.config import settings
from core.exceptions import (
    DiscordBotAPIError,
    DiscordBotAuthError,
    DiscordBotError,
    DiscordBotTimeoutError,
)

# Context variable for per-request bot token (used in HTTP/remote mode)
_request_bot_token: contextvars.ContextVar[str | None] = contextvars.ContextVar(
    "_request_bot_token", default=None
)


def set_request_bot_token(token: str | None) -> None:
    """Set the bot token for the current request context (HTTP mode)."""
    _request_bot_token.set(token)


def get_request_bot_token() -> str | None:
    """Get the bot token from the current request context."""
    return _request_bot_token.get()


class DiscordBotClient:
    """Async HTTP client for Discord Agent Proxy REST API."""

    def __init__(
        self,
        bot_token: str | None = None,
        base_url: str | None = None,
    ):
        """Initialize the Discord Bot client.

        Args:
            bot_token: Bot access token for authentication. If not provided, uses settings.
            base_url: Base URL of the deployed Discord Agent Proxy. If not provided, uses settings.
        """
        self.bot_token = bot_token if bot_token is not None else settings.bot_token
        self.base_url = (base_url or settings.bot_base_url).rstrip("/")
        self.timeout = settings.request_timeout

        logger.info(f"DiscordBotClient initialized with base_url: {self.base_url}")
        logger.debug(f"Bot token configured: {'Yes' if self.bot_token else 'No'}")
        logger.debug(f"Request timeout: {self.timeout}s")

    def _get_headers(self) -> dict[str, str]:
        """Get request headers with authentication."""
        token = get_request_bot_token() or self.bot_token
        if not token:
            logger.error("Bot token not configured!")
            raise DiscordBotAuthError("Bot token not configured")

        return {
            "accept": "application/json",
            "authorization": token,
            "content-type": "application/json",
        }

    def _handle_error_response(self, response: httpx.Response) -> None:
        """Parse API error response and raise the appropriate exception.

        The Discord Agent Proxy returns errors in the format:
            {"error": "..."}
        """
        status = response.status_code
        try:
            body = response.json()
        except Exception:
            body = {}

        message = body.get("error") or response.text or f"HTTP {status}"

        logger.error(f"API error {status}: {message}")

        if status in (401, 403):
            raise DiscordBotAuthError(message)
        raise DiscordBotAPIError(message=message, status_code=status)

    async def _request(
        self,
        method: str,
        path: str,
        payload: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        timeout: float | None = None,
    ) -> Any:
        """Make an HTTP request to the Discord Agent Proxy API.

        Args:
            method: HTTP method (GET, POST, PATCH, DELETE)
            path: API path (e.g., "/api/whoami")
            payload: Request body as dictionary (for POST/PATCH)
            params: Query parameters
            timeout: Optional timeout override

        Returns:
            Parsed response data (from {"data": ...} envelope)

        Raises:
            DiscordBotAuthError: If authentication fails
            DiscordBotAPIError: If the API request fails
            DiscordBotTimeoutError: If the request times out
        """
        url = f"{self.base_url}{path}"
        request_timeout = timeout or self.timeout

        logger.info(f"{method} {url}")
        if payload:
            logger.debug(f"Request payload: {json.dumps(payload, ensure_ascii=False, indent=2)}")
        if params:
            logger.debug(f"Request params: {params}")
        logger.debug(f"Timeout: {request_timeout}s")

        async with httpx.AsyncClient() as client:
            try:
                response = await client.request(
                    method=method,
                    url=url,
                    json=payload,
                    params=params,
                    headers=self._get_headers(),
                    timeout=request_timeout,
                )

                logger.info(f"Response status: {response.status_code}")

                if response.status_code >= 400:
                    self._handle_error_response(response)

                if response.status_code == 204 or not response.content:
                    return None

                result = response.json()
                logger.success("Request successful!")

                # Unwrap {"data": ...} envelope
                if isinstance(result, dict) and "data" in result:
                    return result["data"]
                return result

            except httpx.TimeoutException as e:
                logger.error(f"Request timeout after {request_timeout}s: {e}")
                raise DiscordBotTimeoutError(
                    f"Request to {path} timed out after {request_timeout}s"
                ) from e

            except DiscordBotError:
                raise

            except Exception as e:
                logger.error(f"Request error: {e}")
                raise DiscordBotAPIError(message=str(e)) from e

    async def whoami(self) -> Any:
        """Get information about the currently proxied Discord account."""
        return await self._request("GET", "/api/whoami")

    async def list_guilds(self) -> Any:
        """List all guilds (servers) the account has joined."""
        return await self._request("GET", "/api/guilds")

    async def list_channels(self, guild_id: str) -> Any:
        """List all channels in a guild."""
        return await self._request("GET", f"/api/guilds/{guild_id}/channels")

    async def create_text_channel(self, guild_id: str, name: str) -> Any:
        """Create a text channel in a guild."""
        return await self._request("POST", f"/api/guilds/{guild_id}/channels", payload={"name": name})

    async def list_members(self, guild_id: str, limit: int | None = None) -> Any:
        """List members of a guild."""
        params: dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        return await self._request("GET", f"/api/guilds/{guild_id}/members", params=params or None)

    async def send_message(
        self, channel_id: str, content: str, reply_to: str | None = None
    ) -> Any:
        """Send a message to a channel."""
        payload: dict[str, Any] = {"channel_id": channel_id, "content": content}
        if reply_to:
            payload["reply_to"] = reply_to
        return await self._request("POST", "/api/messages", payload=payload)

    async def read_messages(self, channel_id: str, limit: int | None = None) -> Any:
        """Read recent messages from a channel."""
        params: dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        return await self._request(
            "GET", f"/api/channels/{channel_id}/messages", params=params or None
        )

    async def edit_message(
        self, channel_id: str, message_id: str, content: str
    ) -> Any:
        """Edit a message."""
        return await self._request(
            "PATCH",
            f"/api/channels/{channel_id}/messages/{message_id}",
            payload={"content": content},
        )

    async def delete_message(self, channel_id: str, message_id: str) -> Any:
        """Delete a message."""
        return await self._request(
            "DELETE", f"/api/channels/{channel_id}/messages/{message_id}"
        )

    async def search_messages(
        self, channel_id: str, query: str, limit: int | None = None
    ) -> Any:
        """Search messages in a channel."""
        params: dict[str, Any] = {"q": query}
        if limit is not None:
            params["limit"] = limit
        return await self._request(
            "GET", f"/api/channels/{channel_id}/messages/search", params=params
        )

    async def add_reaction(
        self, channel_id: str, message_id: str, emoji: str
    ) -> Any:
        """Add an emoji reaction to a message."""
        return await self._request(
            "POST",
            f"/api/channels/{channel_id}/messages/{message_id}/reactions",
            payload={"emoji": emoji},
        )

    async def pin_message(self, channel_id: str, message_id: str) -> Any:
        """Pin a message in a channel."""
        return await self._request(
            "POST", f"/api/channels/{channel_id}/messages/{message_id}/pin"
        )

    async def create_dm(self, recipient_id: str) -> Any:
        """Open a direct message channel with a user."""
        return await self._request("POST", "/api/dms", payload={"recipient_id": recipient_id})

    async def send_dm(self, recipient_id: str, content: str) -> Any:
        """Send a direct message to a user."""
        return await self._request(
            "POST", "/api/dms/send", payload={"recipient_id": recipient_id, "content": content}
        )


# Global client instance
client = DiscordBotClient()
