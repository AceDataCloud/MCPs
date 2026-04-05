"""HTTP client for Producer API."""

import contextvars
import json
from typing import Any

import httpx
from loguru import logger

from core.config import settings
from core.exceptions import ProducerAPIError, ProducerAuthError, ProducerTimeoutError

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


class ProducerClient:
    """Async HTTP client for AceDataCloud Producer API."""

    def __init__(self, api_token: str | None = None, base_url: str | None = None):
        """Initialize the Producer API client.

        Args:
            api_token: API token for authentication. If not provided, uses settings.
            base_url: Base URL for the API. If not provided, uses settings.
        """
        self.api_token = api_token if api_token is not None else settings.api_token
        self.base_url = base_url or settings.api_base_url
        self.timeout = settings.request_timeout

        logger.info(f"ProducerClient initialized with base_url: {self.base_url}")
        logger.debug(f"API token configured: {'Yes' if self.api_token else 'No'}")
        logger.debug(f"Request timeout: {self.timeout}s")

    def _get_headers(self) -> dict[str, str]:
        """Get request headers with authentication."""
        token = get_request_api_token() or self.api_token
        if not token:
            logger.error("API token not configured!")
            raise ProducerAuthError("API token not configured")

        return {
            "accept": "application/json",
            "authorization": f"Bearer {token}",
            "content-type": "application/json",
        }

    def _with_async_callback(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Ensure long-running media operations are submitted asynchronously."""
        request_payload = dict(payload)
        if not request_payload.get("callback_url"):
            request_payload["callback_url"] = _ASYNC_CALLBACK_URL
        return request_payload

    async def request(
        self,
        endpoint: str,
        payload: dict[str, Any],
        timeout: float | None = None,
    ) -> dict[str, Any]:
        """Make a POST request to the Producer API.

        Args:
            endpoint: API endpoint path (e.g., "/producer/audios")
            payload: Request body as dictionary
            timeout: Optional timeout override

        Returns:
            API response as dictionary

        Raises:
            ProducerAuthError: If authentication fails
            ProducerAPIError: If the API request fails
            ProducerTimeoutError: If the request times out
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
                    raise ProducerAuthError("Invalid API token")

                if response.status_code == 403:
                    logger.error("Access denied: Check API permissions")
                    raise ProducerAuthError("Access denied. Check your API permissions.")

                response.raise_for_status()

                result = response.json()
                logger.success(f"Request successful! Task ID: {result.get('task_id', 'N/A')}")

                # Log summary of response
                if result.get("success"):
                    data = result.get("data", [])
                    if isinstance(data, list):
                        logger.info(f"Returned {len(data)} item(s)")
                        for i, item in enumerate(data, 1):
                            if "audio_url" in item:
                                logger.info(
                                    f"   Song {i}: "
                                    f"{item.get('title', 'Untitled')} - "
                                    f"{item.get('duration', 0):.1f}s"
                                )
                            elif "text" in item:
                                logger.info(f"   Lyrics {i}: {item.get('title', 'Untitled')}")
                else:
                    logger.warning(f"API returned success=false: {result.get('error', {})}")

                return result  # type: ignore[no-any-return]

            except httpx.TimeoutException as e:
                logger.error(f"Request timeout after {request_timeout}s: {e}")
                raise ProducerTimeoutError(
                    f"Request to {endpoint} timed out after {request_timeout}s"
                ) from e

            except ProducerAuthError:
                raise

            except httpx.HTTPStatusError as e:
                logger.error(f"HTTP error {e.response.status_code}: {e.response.text}")
                raise ProducerAPIError(
                    message=e.response.text,
                    code=f"http_{e.response.status_code}",
                    status_code=e.response.status_code,
                ) from e

            except Exception as e:
                logger.error(f"Request error: {e}")
                raise ProducerAPIError(message=str(e)) from e

    # Convenience methods for specific endpoints
    async def generate_audio(self, **kwargs: Any) -> dict[str, Any]:
        """Generate audio using the audios endpoint."""
        logger.info(f"Generating audio with action: {kwargs.get('action', 'generate')}")
        return await self.request("/producer/audios", self._with_async_callback(kwargs))

    async def generate_lyrics(self, **kwargs: Any) -> dict[str, Any]:
        """Generate lyrics using the lyrics endpoint."""
        logger.info(f"Generating lyrics with prompt: {kwargs.get('prompt', '')[:50]}...")
        return await self.request("/producer/lyrics", kwargs)

    async def upload_audio(self, **kwargs: Any) -> dict[str, Any]:
        """Upload audio from a URL."""
        logger.info(f"Uploading audio: {kwargs.get('audio_url', '')[:50]}...")
        return await self.request("/producer/upload", kwargs)

    async def generate_video(self, **kwargs: Any) -> dict[str, Any]:
        """Generate video for a song."""
        logger.info(f"Generating video for audio: {kwargs.get('audio_id', '')}")
        return await self.request("/producer/videos", self._with_async_callback(kwargs))

    async def generate_wav(self, **kwargs: Any) -> dict[str, Any]:
        """Get WAV format of a song."""
        logger.info(f"Getting WAV for audio: {kwargs.get('audio_id', '')}")
        return await self.request("/producer/wav", self._with_async_callback(kwargs))

    async def query_task(self, **kwargs: Any) -> dict[str, Any]:
        """Query task status using the tasks endpoint."""
        task_id = kwargs.get("id") or kwargs.get("ids", [])
        logger.info(f"Querying task(s): {task_id}")
        return await self.request("/producer/tasks", kwargs)


# Global client instance
client = ProducerClient()
