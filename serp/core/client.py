"""HTTP client for Google SERP API."""

import contextvars
import json
from typing import Any

import httpx
from loguru import logger

from core.config import settings
from core.exceptions import SerpAPIError, SerpAuthError, SerpTimeoutError

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


class SerpClient:
    """Async HTTP client for AceDataCloud Google SERP API."""

    def __init__(self, api_token: str | None = None, base_url: str | None = None):
        """Initialize the SERP API client.

        Args:
            api_token: API token for authentication. If not provided, uses settings.
            base_url: Base URL for the API. If not provided, uses settings.
        """
        self.api_token = api_token if api_token is not None else settings.api_token
        self.base_url = base_url or settings.api_base_url
        self.timeout = settings.request_timeout

        logger.info(f"SerpClient initialized with base_url: {self.base_url}")
        logger.debug(f"API token configured: {'Yes' if self.api_token else 'No'}")
        logger.debug(f"Request timeout: {self.timeout}s")

    def _get_headers(self) -> dict[str, str]:
        """Get request headers with authentication."""
        token = get_request_api_token() or self.api_token
        if not token:
            logger.error("API token not configured!")
            raise SerpAuthError("API token not configured")

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
        """Make a POST request to the SERP API.

        Args:
            endpoint: API endpoint path (e.g., "/serp/google")
            payload: Request body as dictionary
            timeout: Optional timeout override

        Returns:
            API response as dictionary

        Raises:
            SerpAuthError: If authentication fails
            SerpAPIError: If the API request fails
            SerpTimeoutError: If the request times out
        """
        url = f"{self.base_url}{endpoint}"
        request_timeout = timeout or self.timeout

        logger.info(f"POST {url}")
        logger.debug(f"Request payload: {json.dumps(payload, ensure_ascii=False, indent=2)}")
        logger.debug(f"Timeout: {request_timeout}s")

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    url,
                    json=payload,
                    headers=self._get_headers(),
                    timeout=request_timeout,
                )

                logger.info(f"Response status: {response.status_code}")

                if response.status_code == 401:
                    logger.error("Authentication failed: Invalid API token")
                    raise SerpAuthError("Invalid API token")

                if response.status_code == 403:
                    logger.error("Access denied: Check API permissions")
                    raise SerpAuthError("Access denied. Check your API permissions.")

                response.raise_for_status()

                result = response.json()
                logger.success("Request successful!")

                # Log summary of response
                if "organic" in result:
                    logger.info(f"Returned {len(result.get('organic', []))} organic results")
                if "knowledge_graph" in result:
                    logger.info(f"Knowledge graph: {result['knowledge_graph'].get('title', 'N/A')}")

                return result  # type: ignore[no-any-return]

            except httpx.TimeoutException as e:
                logger.error(f"Request timeout after {request_timeout}s: {e}")
                raise SerpTimeoutError(
                    f"Request to {endpoint} timed out after {request_timeout}s"
                ) from e

            except SerpAuthError:
                raise

            except httpx.HTTPStatusError as e:
                logger.error(f"HTTP error {e.response.status_code}: {e.response.text}")
                raise SerpAPIError(
                    message=e.response.text,
                    code=f"http_{e.response.status_code}",
                    status_code=e.response.status_code,
                ) from e

            except Exception as e:
                logger.error(f"Request error: {e}")
                raise SerpAPIError(message=str(e)) from e

    async def search(self, **kwargs: Any) -> dict[str, Any]:
        """Perform a Google search using the SERP API.

        Args:
            **kwargs: Search parameters including:
                - query: Search query string (required)
                - type: Search type (search, images, news, maps, places, videos)
                - country: Country code for localized results
                - language: Language code for results
                - range: Time range filter
                - number: Number of results per page
                - page: Page number

        Returns:
            Search results dictionary
        """
        logger.info(f"Searching for: {kwargs.get('query', '')[:50]}...")
        return await self.request("/serp/google", kwargs)


# Global client instance
client = SerpClient()
