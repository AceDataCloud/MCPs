"""HTTP client for OpenAI API via AceDataCloud."""

import contextvars
import json
from typing import Any
from urllib.parse import urlencode

import httpx
from loguru import logger

from core.config import settings
from core.exceptions import OpenAIAPIError, OpenAIAuthError, OpenAIError, OpenAITimeoutError

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


class OpenAIClient:
    """Async HTTP client for AceDataCloud OpenAI API."""

    def __init__(self, api_token: str | None = None, base_url: str | None = None):
        """Initialize the OpenAI API client.

        Args:
            api_token: API token for authentication. If not provided, uses settings.
            base_url: Base URL for the API. If not provided, uses settings.
        """
        self.api_token = api_token if api_token is not None else settings.api_token
        self.base_url = base_url or settings.api_base_url
        self.timeout = settings.request_timeout

        logger.info(f"OpenAIClient initialized with base_url: {self.base_url}")
        logger.debug(f"API token configured: {'Yes' if self.api_token else 'No'}")
        logger.debug(f"Request timeout: {self.timeout}s")

    def _get_headers(self) -> dict[str, str]:
        """Get request headers with authentication."""
        token = get_request_api_token() or self.api_token
        if not token:
            logger.error("API token not configured!")
            raise OpenAIAuthError("API token not configured")

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
            raise OpenAIAuthError(message)
        raise OpenAIAPIError(message=message, code=code, status_code=status)

    async def request(
        self,
        endpoint: str,
        payload: dict[str, Any],
        timeout: float | None = None,
    ) -> dict[str, Any]:
        """Make a POST request to the OpenAI API.

        Args:
            endpoint: API endpoint path (e.g., "/openai/chat/completions")
            payload: Request body as dictionary
            timeout: Optional timeout override

        Returns:
            API response as dictionary

        Raises:
            OpenAIAuthError: If authentication fails
            OpenAIAPIError: If the API request fails
            OpenAITimeoutError: If the request times out
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

                if response.status_code >= 400:
                    self._handle_error_response(response)

                result = response.json()
                logger.success("Request successful!")

                return result  # type: ignore[no-any-return]

            except httpx.TimeoutException as e:
                logger.error(f"Request timeout after {request_timeout}s: {e}")
                raise OpenAITimeoutError(
                    f"Request to {endpoint} timed out after {request_timeout}s"
                ) from e

            except OpenAIError:
                raise

            except Exception as e:
                logger.error(f"Request error: {e}")
                raise OpenAIAPIError(message=str(e)) from e

    async def request_get(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
        timeout: float | None = None,
    ) -> dict[str, Any]:
        """Make a GET request to the OpenAI API."""
        url = f"{self.base_url}{endpoint}"
        request_timeout = timeout or self.timeout

        logger.info(f"GET {url}")

        async with httpx.AsyncClient() as http_client:
            try:
                response = await http_client.get(
                    url,
                    params=params,
                    headers=self._get_headers(),
                    timeout=request_timeout,
                )

                logger.info(f"Response status: {response.status_code}")

                if response.status_code >= 400:
                    self._handle_error_response(response)

                result = response.json()
                logger.success("GET request successful!")

                return result  # type: ignore[no-any-return]

            except httpx.TimeoutException as e:
                logger.error(f"Request timeout after {request_timeout}s: {e}")
                raise OpenAITimeoutError(
                    f"Request to {endpoint} timed out after {request_timeout}s"
                ) from e

            except OpenAIError:
                raise

            except Exception as e:
                logger.error(f"Request error: {e}")
                raise OpenAIAPIError(message=str(e)) from e

    async def chat_completions(self, **kwargs: Any) -> dict[str, Any]:
        """Create a chat completion."""
        logger.info(f"Chat completion with model: {kwargs.get('model', 'unknown')}")
        return await self.request("/openai/chat/completions", kwargs)

    async def models(self) -> dict[str, Any]:
        """List available OpenAI models."""
        logger.info("List OpenAI models")
        return await self.request_get("/openai/models")

    async def realtime(self, model: str, voice: str) -> dict[str, Any]:
        """Get realtime connection information."""
        logger.info(f"Realtime API with model: {model}")
        return await self.request_get("/v1/realtime", {"model": model, "voice": voice})

    async def embeddings(self, **kwargs: Any) -> dict[str, Any]:
        """Create text embeddings."""
        logger.info(f"Embeddings with model: {kwargs.get('model', 'unknown')}")
        return await self.request("/openai/embeddings", kwargs)

    async def images_generations(self, **kwargs: Any) -> dict[str, Any]:
        """Generate images."""
        logger.info(f"Image generation with model: {kwargs.get('model', 'unknown')}")
        return await self.request("/openai/images/generations", kwargs)

    async def images_edits(self, **kwargs: Any) -> dict[str, Any]:
        """Edit images."""
        logger.info(f"Image edit with model: {kwargs.get('model', 'unknown')}")
        return await self.request("/openai/images/edits", kwargs)

    def _with_async_callback(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Ensure long-running image operations are submitted asynchronously."""
        request_payload = dict(payload)
        if not request_payload.get("callback_url") and "async" not in request_payload:
            request_payload["async"] = True
        return request_payload

    async def images_generations_async(self, **kwargs: Any) -> dict[str, Any]:
        """Generate images in async mode and return the submission response immediately."""
        return await self.images_generations(**self._with_async_callback(kwargs))

    async def images_edits_async(self, **kwargs: Any) -> dict[str, Any]:
        """Edit images in async mode and return the submission response immediately."""
        return await self.images_edits(**self._with_async_callback(kwargs))

    async def responses(self, **kwargs: Any) -> dict[str, Any]:
        """Create a response using the Responses API."""
        logger.info(f"Responses API with model: {kwargs.get('model', 'unknown')}")
        return await self.request("/openai/responses", kwargs)

    async def tasks(self, **kwargs: Any) -> dict[str, Any]:
        """Query async image tasks."""
        logger.info(f"Tasks API action: {kwargs.get('action', 'unknown')}")
        return await self.request("/openai/tasks", kwargs)

    async def request_binary(
        self,
        endpoint: str,
        payload: dict[str, Any],
        timeout: float | None = None,
    ) -> bytes:
        """Make a POST request to the OpenAI API and return raw binary response bytes.

        Args:
            endpoint: API endpoint path (e.g., "/v1/audio/speech")
            payload: Request body as dictionary
            timeout: Optional timeout override

        Returns:
            Raw response bytes

        Raises:
            OpenAIAuthError: If authentication fails
            OpenAIAPIError: If the API request fails
            OpenAITimeoutError: If the request times out
        """
        url = f"{self.base_url}{endpoint}"
        request_timeout = timeout or self.timeout

        logger.info(f"POST {url} (binary response)")
        logger.debug(f"Request payload: {json.dumps(payload, ensure_ascii=False, indent=2)}")

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

                logger.success("Binary request successful!")
                return response.content

            except httpx.TimeoutException as e:
                logger.error(f"Request timeout after {request_timeout}s: {e}")
                raise OpenAITimeoutError(
                    f"Request to {endpoint} timed out after {request_timeout}s"
                ) from e

            except OpenAIError:
                raise

            except Exception as e:
                logger.error(f"Request error: {e}")
                raise OpenAIAPIError(message=str(e)) from e

    async def audio_speech(self, **kwargs: Any) -> bytes:
        """Generate speech audio from text."""
        logger.info(f"Audio speech with model: {kwargs.get('model', 'unknown')}")
        return await self.request_binary("/v1/audio/speech", kwargs)

    async def request_multipart(
        self,
        endpoint: str,
        fields: dict[str, Any],
        timeout: float | None = None,
    ) -> dict[str, Any]:
        """Make a multipart/form-data POST request to the OpenAI API.

        Args:
            endpoint: API endpoint path (e.g., "/v1/audio/transcriptions")
            fields: Form fields; any value that is bytes is sent as a file part
                    with filename "audio" and the detected content-type, while
                    plain strings/numbers are sent as form text fields.
            timeout: Optional timeout override

        Returns:
            API response as dictionary (or plain text wrapped in {"text": …})

        Raises:
            OpenAIAuthError: If authentication fails
            OpenAIAPIError: If the API request fails
            OpenAITimeoutError: If the request times out
        """
        url = f"{self.base_url}{endpoint}"
        request_timeout = timeout or self.timeout

        logger.info(f"POST {url} (multipart/form-data)")
        logger.debug(f"Timeout: {request_timeout}s")

        files: list[tuple[str, Any]] = []
        data: dict[str, str] = {}
        for key, value in fields.items():
            if isinstance(value, bytes):
                files.append((key, ("audio", value, "application/octet-stream")))
            elif isinstance(value, list):
                for item in value:
                    files.append((f"{key}[]", (None, str(item))))
            else:
                data[key] = str(value)

        # The auth header must NOT include content-type — httpx sets it for multipart
        token = get_request_api_token() or self.api_token
        if not token:
            raise OpenAIAuthError("API token not configured")
        headers = {
            "accept": "application/json",
            "authorization": f"Bearer {token}",
        }

        async with httpx.AsyncClient() as http_client:
            try:
                response = await http_client.post(
                    url,
                    files=files if files else None,
                    data=data,
                    headers=headers,
                    timeout=request_timeout,
                )

                logger.info(f"Response status: {response.status_code}")

                if response.status_code >= 400:
                    self._handle_error_response(response)

                content_type = response.headers.get("content-type", "")
                if "application/json" in content_type:
                    result = response.json()
                else:
                    result = {"text": response.text}

                logger.success("Multipart request successful!")
                return result  # type: ignore[no-any-return]

            except httpx.TimeoutException as e:
                logger.error(f"Request timeout after {request_timeout}s: {e}")
                raise OpenAITimeoutError(
                    f"Request to {endpoint} timed out after {request_timeout}s"
                ) from e

            except OpenAIError:
                raise

            except Exception as e:
                logger.error(f"Request error: {e}")
                raise OpenAIAPIError(message=str(e)) from e

    async def audio_transcriptions(self, audio_bytes: bytes, **kwargs: Any) -> dict[str, Any]:
        """Transcribe audio to text using the Whisper model."""
        logger.info(f"Audio transcription with model: {kwargs.get('model', 'whisper-1')}")
        fields: dict[str, Any] = {"file": audio_bytes, **kwargs}
        return await self.request_multipart("/v1/audio/transcriptions", fields)

    def realtime_connection_url(self, model: str, voice: str) -> str:
        """Build websocket URL for the realtime endpoint."""
        query = urlencode({"model": model, "voice": voice})
        if self.base_url.startswith("https://"):
            ws_base = "wss://" + self.base_url[len("https://") :]
        elif self.base_url.startswith("http://"):
            ws_base = "ws://" + self.base_url[len("http://") :]
        else:
            ws_base = self.base_url
        return f"{ws_base}/v1/realtime?{query}"


# Global client instance
client = OpenAIClient()
