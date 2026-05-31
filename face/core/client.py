"""HTTP client for Face Transform API."""

import contextvars
import json
from typing import Any

import httpx
from loguru import logger

from core.config import settings
from core.exceptions import FaceAPIError, FaceAuthError, FaceError, FaceTimeoutError

# Context variable for per-request API token (used in HTTP/remote mode).
_request_api_token: contextvars.ContextVar[str | None] = contextvars.ContextVar(
    "_request_api_token", default=None
)


def set_request_api_token(token: str | None) -> None:
    """Set the API token for the current request context (HTTP mode)."""
    _request_api_token.set(token)


def get_request_api_token() -> str | None:
    """Get the API token from the current request context."""
    return _request_api_token.get()


class FaceClient:
    """Async HTTP client for the AceDataCloud Face Transform API."""

    def __init__(self, api_token: str | None = None, base_url: str | None = None):
        self.api_token = api_token if api_token is not None else settings.api_token
        self.base_url = base_url or settings.api_base_url
        self.timeout = settings.request_timeout

        logger.info(f"FaceClient initialized with base_url: {self.base_url}")
        logger.debug(f"API token configured: {'Yes' if self.api_token else 'No'}")
        logger.debug(f"Request timeout: {self.timeout}s")

    def _get_headers(self) -> dict[str, str]:
        token = get_request_api_token() or self.api_token
        if not token:
            logger.error("API token not configured!")
            raise FaceAuthError("API token not configured")

        return {
            "accept": "application/json",
            "authorization": f"Bearer {token}",
            "content-type": "application/json",
        }

    def _handle_error_response(self, response: httpx.Response) -> None:
        status = response.status_code
        try:
            body = response.json()
        except Exception:
            body = {}

        error_obj = body.get("error", {}) if isinstance(body, dict) else {}
        code = error_obj.get("code", f"http_{status}")
        message = (
            error_obj.get("message")
            or (body.get("detail") if isinstance(body, dict) else None)
            or response.text
            or f"HTTP {status}"
        )

        logger.error(f"API error {status} [{code}]: {message}")

        if status in (401, 403):
            raise FaceAuthError(message)
        raise FaceAPIError(message=message, code=code, status_code=status)

    async def request(
        self,
        method: str,
        endpoint: str,
        *,
        payload: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        timeout: float | None = None,
    ) -> dict[str, Any]:
        method_upper = method.upper()
        url = f"{self.base_url}{endpoint}"
        request_timeout = timeout or self.timeout

        logger.info(f"🚀 {method_upper} {url}")
        if payload is not None:
            logger.debug(f"Request payload: {json.dumps(payload, ensure_ascii=False, indent=2)}")
        if params is not None:
            logger.debug(f"Request params: {json.dumps(params, ensure_ascii=False, indent=2)}")
        logger.debug(f"Timeout: {request_timeout}s")

        async with httpx.AsyncClient() as http_client:
            try:
                response = await http_client.request(
                    method_upper,
                    url,
                    json=payload,
                    params=params,
                    headers=self._get_headers(),
                    timeout=request_timeout,
                )
                logger.info(f"📥 Response status: {response.status_code}")

                if response.status_code >= 400:
                    self._handle_error_response(response)

                result = response.json()
                logger.success("✅ Request successful")
                return result  # type: ignore[no-any-return]

            except httpx.TimeoutException as e:
                logger.error(f"⏰ Request timeout after {request_timeout}s: {e}")
                raise FaceTimeoutError(
                    f"Request to {endpoint} timed out after {request_timeout}s"
                ) from e

            except FaceError:
                raise

            except Exception as e:
                logger.error(f"❌ Request error: {e}")
                raise FaceAPIError(message=str(e)) from e

    async def analyze(self, **kwargs: Any) -> dict[str, Any]:
        logger.info(f"🔍 Analyzing face keypoints for: {kwargs.get('image_url', '')}")
        return await self.request("POST", "/face/analyze", payload=kwargs)

    async def beautify(self, **kwargs: Any) -> dict[str, Any]:
        logger.info(f"✨ Beautifying face for: {kwargs.get('image_url', '')}")
        return await self.request("POST", "/face/beautify", payload=kwargs)

    async def change_age(self, **kwargs: Any) -> dict[str, Any]:
        logger.info(f"🕰️ Transforming age for: {kwargs.get('image_url', '')}")
        return await self.request("POST", "/face/change-age", payload=kwargs)

    async def change_gender(self, **kwargs: Any) -> dict[str, Any]:
        logger.info(f"🔁 Swapping gender for: {kwargs.get('image_url', '')}")
        return await self.request("POST", "/face/change-gender", payload=kwargs)

    async def swap(self, **kwargs: Any) -> dict[str, Any]:
        logger.info(
            f"🔄 Swapping face: source={kwargs.get('source_image_url', '')} "
            f"target={kwargs.get('target_image_url', '')}"
        )
        return await self.request("POST", "/face/swap", payload=kwargs)

    async def cartoon(self, **kwargs: Any) -> dict[str, Any]:
        logger.info(f"🎨 Cartoonizing face for: {kwargs.get('image_url', '')}")
        return await self.request("POST", "/face/cartoon", payload=kwargs)

    async def detect_live(self, **kwargs: Any) -> dict[str, Any]:
        logger.info(f"🛡️ Detecting liveness for: {kwargs.get('image_url', '')}")
        return await self.request("POST", "/face/detect-live", payload=kwargs)


# Global client instance
client = FaceClient()
