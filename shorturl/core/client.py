"""HTTP client for ShortURL API."""

import contextvars
import json
from typing import Any

import httpx
from loguru import logger

from core.config import settings
from core.exceptions import ShortURLAPIError, ShortURLAuthError, ShortURLTimeoutError

# Context variable for per-request API token (used in HTTP/remote mode)
_request_api_token: contextvars.ContextVar[str | None] = contextvars.ContextVar(
    "_request_api_token", default=None
)


def set_request_api_token(token: str | None) -> None:
    """Set the API token for the current request context (HTTP mode)."""
    _request_api_token.set(token)


def get_request_api_token() -> str | None:
    """Get the API token from the current request context."""
    return _request_api_token.get()


class ShortURLClient:
    """Async HTTP client for AceDataCloud ShortURL API."""

    def __init__(self, api_token: str | None = None, base_url: str | None = None):
        """Initialize the ShortURL API client.

        Args:
            api_token: API token for authentication. If not provided, uses settings.
            base_url: Base URL for the API. If not provided, uses settings.
        """
        self.api_token = api_token if api_token is not None else settings.api_token
        self.base_url = base_url or settings.api_base_url
        self.timeout = settings.request_timeout

        logger.info(f"ShortURLClient initialized with base_url: {self.base_url}")
        logger.debug(f"API token configured: {'Yes' if self.api_token else 'No'}")
        logger.debug(f"Request timeout: {self.timeout}s")

    def _get_headers(self) -> dict[str, str]:
        """Get request headers with authentication."""
        token = get_request_api_token() or self.api_token
        if not token:
            logger.error("API token not configured!")
            raise ShortURLAuthError("API token not configured")

        return {
            "accept": "application/json",
            "authorization": f"Bearer {token}",
            "content-type": "application/json",
        }

    async def request(
        self,
        endpoint: str,
        payload: dict[str, Any],
        timeout: float | None = None,
    ) -> dict[str, Any]:
        """Make a POST request to the ShortURL API.

        Args:
            endpoint: API endpoint path (e.g., "/shorturl")
            payload: Request body as dictionary
            timeout: Optional timeout override

        Returns:
            API response as dictionary

        Raises:
            ShortURLAuthError: If authentication fails
            ShortURLAPIError: If the API request fails
            ShortURLTimeoutError: If the request times out
        """
        url = f"{self.base_url}{endpoint}"
        request_timeout = timeout or self.timeout

        logger.info(f"POST {url}")
        logger.debug(f"Request payload: {json.dumps(payload, ensure_ascii=False, indent=2)}")
        logger.debug(f"Timeout: {request_timeout}s")

        async with httpx.AsyncClient() as http_client:
            try:
                response = await http_client.post(
                    url,
                    json=payload,
                    headers=self._get_headers(),
                    timeout=request_timeout,
                )

                logger.info(f"Response status: {response.status_code}")

                if response.status_code == 401:
                    logger.error("Authentication failed: Invalid API token")
                    raise ShortURLAuthError("Invalid API token")

                if response.status_code == 403:
                    logger.error("Access denied: Check API permissions")
                    raise ShortURLAuthError("Access denied. Check your API permissions.")

                response.raise_for_status()

                result = response.json()
                logger.success("Request successful!")

                if result.get("success") and "data" in result:
                    short_url = result["data"].get("url", "")
                    logger.info(f"Short URL created: {short_url}")

                return result  # type: ignore[no-any-return]

            except httpx.TimeoutException as e:
                logger.error(f"Request timeout after {request_timeout}s: {e}")
                raise ShortURLTimeoutError(
                    f"Request to {endpoint} timed out after {request_timeout}s"
                ) from e

            except ShortURLAuthError:
                raise

            except httpx.HTTPStatusError as e:
                logger.error(f"HTTP error {e.response.status_code}: {e.response.text}")
                raise ShortURLAPIError(
                    message=e.response.text,
                    code=f"http_{e.response.status_code}",
                    status_code=e.response.status_code,
                ) from e

            except Exception as e:
                logger.error(f"Request error: {e}")
                raise ShortURLAPIError(message=str(e)) from e

    async def shorten(self, content: str) -> dict[str, Any]:
        """Create a short URL from a long URL.

        Args:
            content: The long URL to shorten.

        Returns:
            API response dictionary containing the short URL.
        """
        logger.info(f"Shortening URL: {content[:80]}...")
        return await self.request("/shorturl", {"content": content})


# Global client instance
client = ShortURLClient()
