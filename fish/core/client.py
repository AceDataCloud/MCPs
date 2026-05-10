"""HTTP client for Fish API."""

import contextvars
import json
from typing import Any

import httpx
from loguru import logger

from core.config import settings
from core.exceptions import FishAPIError, FishAuthError, FishError, FishTimeoutError

# Dummy callback URL used to force the upstream API into async mode.
# When present, the API returns immediately with a task_id instead of blocking
# until generation completes. The health endpoint simply returns 200 OK and
# discards the callback payload — it is never actually processed.
_ASYNC_CALLBACK_URL = "https://api.acedata.cloud/health"

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


class FishClient:
    """Async HTTP client for AceDataCloud Fish API."""

    def __init__(self, api_token: str | None = None, base_url: str | None = None):
        """Initialize the Fish API client.

        Args:
            api_token: API token for authentication. If not provided, uses settings.
            base_url: Base URL for the API. If not provided, uses settings.
        """
        self.api_token = api_token if api_token is not None else settings.api_token
        self.base_url = base_url or settings.api_base_url
        self.timeout = settings.request_timeout

        logger.info(f"FishClient initialized with base_url: {self.base_url}")
        logger.debug(f"API token configured: {'Yes' if self.api_token else 'No'}")
        logger.debug(f"Request timeout: {self.timeout}s")

    def _get_headers(self) -> dict[str, str]:
        """Get request headers with authentication."""
        token = get_request_api_token() or self.api_token
        if not token:
            logger.error("API token not configured!")
            raise FishAuthError("API token not configured")

        return {
            "accept": "application/json",
            "authorization": f"Bearer {token}",
            "content-type": "application/json",
        }

    def _with_async_callback(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Ensure long-running operations are submitted asynchronously."""
        request_payload = dict(payload)
        if not request_payload.get("callback_url"):
            request_payload["callback_url"] = _ASYNC_CALLBACK_URL
        return request_payload

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
            raise FishAuthError(message)
        raise FishAPIError(message=message, code=code, status_code=status)

    async def request(
        self,
        endpoint: str,
        payload: dict[str, Any],
        timeout: float | None = None,
    ) -> dict[str, Any]:
        """Make a POST request to the Fish API.

        Args:
            endpoint: API endpoint path (e.g., "/fish/audios")
            payload: Request body as dictionary
            timeout: Optional timeout override

        Returns:
            API response as dictionary

        Raises:
            FishAuthError: If authentication fails
            FishAPIError: If the API request fails
            FishTimeoutError: If the request times out
        """
        url = f"{self.base_url}{endpoint}"
        request_timeout = timeout or self.timeout

        logger.info(f"🚀 POST {url}")
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

                logger.info(f"📥 Response status: {response.status_code}")

                if response.status_code >= 400:
                    self._handle_error_response(response)

                result = response.json()
                logger.success(f"✅ Request successful! Task ID: {result.get('task_id', 'N/A')}")

                return result  # type: ignore[no-any-return]

            except httpx.TimeoutException as e:
                logger.error(f"⏰ Request timeout after {request_timeout}s: {e}")
                raise FishTimeoutError(
                    f"Request to {endpoint} timed out after {request_timeout}s"
                ) from e

            except FishError:
                raise

            except Exception as e:
                logger.error(f"❌ Request error: {e}")
                raise FishAPIError(message=str(e)) from e

    async def generate_audio(self, **kwargs: Any) -> dict[str, Any]:
        """Generate audio (TTS) using the audios endpoint."""
        logger.info(f"🎙️ Generating audio with voice_id: {kwargs.get('voice_id', '')}")
        return await self.request("/fish/audios", self._with_async_callback(kwargs))

    async def create_voice(self, **kwargs: Any) -> dict[str, Any]:
        """Create/clone a voice using the voices endpoint."""
        logger.info(f"🎤 Creating voice from URL: {kwargs.get('voice_url', '')[:50]}")
        return await self.request("/fish/voices", self._with_async_callback(kwargs))

    async def query_task(self, **kwargs: Any) -> dict[str, Any]:
        """Query task status using the tasks endpoint."""
        task_id = kwargs.get("id") or kwargs.get("ids", [])
        logger.info(f"🔍 Querying task(s): {task_id}")
        return await self.request("/fish/tasks", kwargs)


# Global client instance
client = FishClient()
