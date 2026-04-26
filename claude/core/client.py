"""HTTP client for Claude API via AceDataCloud."""

import contextvars
import json
from typing import Any

import httpx
from loguru import logger

from core.config import settings
from core.exceptions import ClaudeAPIError, ClaudeAuthError, ClaudeError, ClaudeTimeoutError

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


class ClaudeClient:
    """Async HTTP client for AceDataCloud Claude API."""

    def __init__(self, api_token: str | None = None, base_url: str | None = None):
        """Initialize the Claude API client.

        Args:
            api_token: API token for authentication. If not provided, uses settings.
            base_url: Base URL for the API. If not provided, uses settings.
        """
        self.api_token = api_token if api_token is not None else settings.api_token
        self.base_url = base_url or settings.api_base_url
        self.timeout = settings.request_timeout

        logger.info(f"ClaudeClient initialized with base_url: {self.base_url}")
        logger.debug(f"API token configured: {'Yes' if self.api_token else 'No'}")
        logger.debug(f"Request timeout: {self.timeout}s")

    def _get_headers(self) -> dict[str, str]:
        """Get request headers with authentication."""
        token = get_request_api_token() or self.api_token
        if not token:
            logger.error("API token not configured!")
            raise ClaudeAuthError("API token not configured")

        return {
            "accept": "application/json",
            "authorization": f"Bearer {token}",
            "content-type": "application/json",
        }

    def _handle_error_response(self, response: httpx.Response) -> None:
        """Parse API error response and raise the appropriate exception."""
        status = response.status_code
        try:
            body = response.json()
        except Exception:
            body = {}

        error_obj = body.get("error", {})
        code = error_obj.get("code", f"http_{status}")
        message = (
            error_obj.get("message") or body.get("detail") or response.text or f"HTTP {status}"
        )

        logger.error(f"API error {status} [{code}]: {message}")

        if status in (401, 403):
            raise ClaudeAuthError(message)
        raise ClaudeAPIError(message=message, code=code, status_code=status)

    async def request(
        self,
        endpoint: str,
        payload: dict[str, Any],
        timeout: float | None = None,
    ) -> dict[str, Any]:
        """Make a POST request to the Claude API."""
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

                if response.status_code >= 400:
                    self._handle_error_response(response)

                result = response.json()
                logger.success("Request successful!")

                return result  # type: ignore[no-any-return]

            except httpx.TimeoutException as e:
                logger.error(f"Request timeout after {request_timeout}s: {e}")
                raise ClaudeTimeoutError(
                    f"Request to {endpoint} timed out after {request_timeout}s"
                ) from e

            except ClaudeError:
                raise

            except Exception as e:
                logger.error(f"Request error: {e}")
                raise ClaudeAPIError(message=str(e)) from e

    async def chat_completions(self, **kwargs: Any) -> dict[str, Any]:
        """Create a chat completion (OpenAI-compatible)."""
        logger.info(f"Chat completion with model: {kwargs.get('model', 'unknown')}")
        return await self.request("/v1/chat/completions", kwargs)

    async def messages(self, **kwargs: Any) -> dict[str, Any]:
        """Create a message using the native Anthropic messages API."""
        logger.info(f"Messages with model: {kwargs.get('model', 'unknown')}")
        return await self.request("/v1/messages", kwargs)

    async def count_tokens(self, **kwargs: Any) -> dict[str, Any]:
        """Count tokens for a message."""
        logger.info(f"Count tokens with model: {kwargs.get('model', 'unknown')}")
        return await self.request("/v1/messages/count_tokens", kwargs)


# Global client instance
client = ClaudeClient()
