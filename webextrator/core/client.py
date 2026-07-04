"""HTTP client for WebExtrator API."""

import contextvars
import json
from typing import Any

import httpx
from loguru import logger

from core.config import settings
from core.exceptions import (
    WebExtraterAPIError,
    WebExtraterAuthError,
    WebExtraterError,
    WebExtraterTimeoutError,
)

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


class WebExtraterClient:
    """Async HTTP client for AceDataCloud WebExtrator API."""

    def __init__(self, api_token: str | None = None, base_url: str | None = None):
        """Initialize the WebExtrator API client.

        Args:
            api_token: API token for authentication. If not provided, uses settings.
            base_url: Base URL for the API. If not provided, uses settings.
        """
        self.api_token = api_token if api_token is not None else settings.api_token
        self.base_url = base_url or settings.api_base_url
        self.timeout = settings.request_timeout

        logger.info(f"WebExtraterClient initialized with base_url: {self.base_url}")
        logger.debug(f"API token configured: {'Yes' if self.api_token else 'No'}")
        logger.debug(f"Request timeout: {self.timeout}s")

    def _get_headers(self) -> dict[str, str]:
        """Get request headers with authentication."""
        token = get_request_api_token() or self.api_token
        if not token:
            logger.error("API token not configured!")
            raise WebExtraterAuthError("API token not configured")

        return {
            "accept": "application/json",
            "authorization": f"Bearer {token}",
            "content-type": "application/json",
        }

    def _handle_error_response(self, response: httpx.Response) -> None:
        """Parse API error response and raise the appropriate exception.

        The AceDataCloud API returns errors in the format:
            {"error": {"code": "...", "message": "..."}}
        """
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
            raise WebExtraterAuthError(message)
        raise WebExtraterAPIError(message=message, code=code, status_code=status)

    async def extract(
        self,
        url: str,
        expected_type: str | None = None,
        enable_llm: bool | None = None,
        wait_until: str | None = None,
        timeout: float | None = None,
        delay: float | None = None,
        wait_for_selector: str | None = None,
        block_resources: list[str] | None = None,
        headers: dict[str, str] | None = None,
        user_agent: str | None = None,
        callback_url: str | None = None,
        cookies: list[dict[str, Any]] | None = None,
        bypass_cache: bool | None = None,
        cache_ttl_seconds: float | None = None,
        mode: str | None = None,
    ) -> dict[str, Any]:
        """Extract structured content from a web page.

        Args:
            url: The URL of the web page to extract content from.
            expected_type: Hint about expected page type ('product', 'article', 'general').
            enable_llm: Enable LLM-based semantic normalization.
            wait_until: Page load wait condition.
            timeout: Total timeout in seconds.
            delay: Extra delay in seconds after page load.
            wait_for_selector: CSS selector to wait for.
            block_resources: Resource types to block.
            headers: Extra HTTP headers.
            user_agent: Override User-Agent.
            callback_url: Async processing callback URL.

        Returns:
            API response dictionary containing extracted content.
        """
        payload: dict[str, Any] = {"url": url}
        if expected_type is not None:
            payload["expected_type"] = expected_type
        if enable_llm is not None:
            payload["enable_llm"] = enable_llm
        if wait_until is not None:
            payload["wait_until"] = wait_until
        if timeout is not None:
            payload["timeout"] = timeout
        if delay is not None:
            payload["delay"] = delay
        if wait_for_selector is not None:
            payload["wait_for_selector"] = wait_for_selector
        if block_resources is not None:
            payload["block_resources"] = block_resources
        if headers is not None:
            payload["headers"] = headers
        if user_agent is not None:
            payload["user_agent"] = user_agent
        if callback_url is not None:
            payload["callback_url"] = callback_url
        if cookies is not None:
            payload["cookies"] = cookies
        if bypass_cache is not None:
            payload["bypass_cache"] = bypass_cache
        if cache_ttl_seconds is not None:
            payload["cache_ttl_seconds"] = cache_ttl_seconds
        if mode is not None:
            payload["mode"] = mode

        logger.info(f"Extracting content from: {url}")
        endpoint = f"{self.base_url}/webextrator/extract"
        logger.info(f"POST {endpoint}")
        logger.debug(f"Request payload: {json.dumps(payload, ensure_ascii=False, indent=2)}")

        async with httpx.AsyncClient() as http_client:
            try:
                response = await http_client.post(
                    endpoint,
                    json=payload,
                    headers=self._get_headers(),
                    timeout=self.timeout,
                )

                logger.info(f"Response status: {response.status_code}")

                if response.status_code >= 400:
                    self._handle_error_response(response)

                result = response.json()
                logger.success("Content extracted successfully!")
                return result  # type: ignore[no-any-return]

            except httpx.TimeoutException as e:
                logger.error(f"Request timeout after {self.timeout}s: {e}")
                raise WebExtraterTimeoutError(
                    f"Request to /webextrator/extract timed out after {self.timeout}s"
                ) from e

            except WebExtraterError:
                raise

            except Exception as e:
                logger.error(f"Request error: {e}")
                raise WebExtraterAPIError(message=str(e)) from e

    async def render(
        self,
        url: str,
        wait_until: str | None = None,
        timeout: float | None = None,
        delay: float | None = None,
        wait_for_selector: str | None = None,
        block_resources: list[str] | None = None,
        headers: dict[str, str] | None = None,
        user_agent: str | None = None,
        callback_url: str | None = None,
        cookies: list[dict[str, Any]] | None = None,
        bypass_cache: bool | None = None,
        cache_ttl_seconds: float | None = None,
        mode: str | None = None,
    ) -> dict[str, Any]:
        """Render a web page and return the rendered HTML.

        Args:
            url: The URL of the web page to render.
            wait_until: Page load wait condition.
            timeout: Total timeout in seconds.
            delay: Extra delay in seconds after page load.
            wait_for_selector: CSS selector to wait for before capturing HTML.
            block_resources: Resource types to block.
            headers: Extra HTTP headers.
            user_agent: Override User-Agent.
            callback_url: Async processing callback URL.

        Returns:
            API response dictionary containing rendered HTML.
        """
        payload: dict[str, Any] = {"url": url}
        if wait_until is not None:
            payload["wait_until"] = wait_until
        if timeout is not None:
            payload["timeout"] = timeout
        if delay is not None:
            payload["delay"] = delay
        if wait_for_selector is not None:
            payload["wait_for_selector"] = wait_for_selector
        if block_resources is not None:
            payload["block_resources"] = block_resources
        if headers is not None:
            payload["headers"] = headers
        if user_agent is not None:
            payload["user_agent"] = user_agent
        if callback_url is not None:
            payload["callback_url"] = callback_url
        if cookies is not None:
            payload["cookies"] = cookies
        if bypass_cache is not None:
            payload["bypass_cache"] = bypass_cache
        if cache_ttl_seconds is not None:
            payload["cache_ttl_seconds"] = cache_ttl_seconds
        if mode is not None:
            payload["mode"] = mode

        logger.info(f"Rendering page: {url}")
        endpoint = f"{self.base_url}/webextrator/render"
        logger.info(f"POST {endpoint}")
        logger.debug(f"Request payload: {json.dumps(payload, ensure_ascii=False, indent=2)}")

        async with httpx.AsyncClient() as http_client:
            try:
                response = await http_client.post(
                    endpoint,
                    json=payload,
                    headers=self._get_headers(),
                    timeout=self.timeout,
                )

                logger.info(f"Response status: {response.status_code}")

                if response.status_code >= 400:
                    self._handle_error_response(response)

                result = response.json()
                logger.success("Page rendered successfully!")
                return result  # type: ignore[no-any-return]

            except httpx.TimeoutException as e:
                logger.error(f"Request timeout after {self.timeout}s: {e}")
                raise WebExtraterTimeoutError(
                    f"Request to /webextrator/render timed out after {self.timeout}s"
                ) from e

            except WebExtraterError:
                raise

            except Exception as e:
                logger.error(f"Request error: {e}")
                raise WebExtraterAPIError(message=str(e)) from e

    async def query_tasks(
        self,
        action: str,
        id: str | None = None,
        trace_id: str | None = None,
        ids: list[str] | None = None,
        trace_ids: list[str] | None = None,
        offset: int | None = None,
        limit: int | None = None,
    ) -> dict[str, Any]:
        """Query previously created render/extract tasks.

        Args:
            action: 'retrieve' (single) or 'retrieve_batch' (multiple).
            id: Task UUID for retrieve.
            trace_id: Trace UUID for retrieve (alternative lookup).
            ids: Task UUIDs for retrieve_batch.
            trace_ids: Trace UUIDs for retrieve_batch.
            offset: Pagination offset for retrieve_batch.
            limit: Pagination limit for retrieve_batch.

        Returns:
            API response dictionary containing task data.
        """
        payload: dict[str, Any] = {"action": action}
        if id is not None:
            payload["id"] = id
        if trace_id is not None:
            payload["trace_id"] = trace_id
        if ids is not None:
            payload["ids"] = ids
        if trace_ids is not None:
            payload["trace_ids"] = trace_ids
        if offset is not None:
            payload["offset"] = offset
        if limit is not None:
            payload["limit"] = limit

        logger.info(f"Querying tasks: action={action}")
        endpoint = f"{self.base_url}/webextrator/tasks"
        logger.info(f"POST {endpoint}")
        logger.debug(f"Request payload: {json.dumps(payload, ensure_ascii=False, indent=2)}")

        async with httpx.AsyncClient() as http_client:
            try:
                response = await http_client.post(
                    endpoint,
                    json=payload,
                    headers=self._get_headers(),
                    timeout=self.timeout,
                )

                logger.info(f"Response status: {response.status_code}")

                if response.status_code >= 400:
                    self._handle_error_response(response)

                result = response.json()
                logger.success("Tasks queried successfully!")
                return result  # type: ignore[no-any-return]

            except httpx.TimeoutException as e:
                logger.error(f"Request timeout after {self.timeout}s: {e}")
                raise WebExtraterTimeoutError(
                    f"Request to /webextrator/tasks timed out after {self.timeout}s"
                ) from e

            except WebExtraterError:
                raise

            except Exception as e:
                logger.error(f"Request error: {e}")
                raise WebExtraterAPIError(message=str(e)) from e


# Global client instance
client = WebExtraterClient()
