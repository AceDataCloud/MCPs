"""Async HTTP client for the AceDataCloud platform management API."""

import contextvars
import json
from typing import Any

import httpx
from loguru import logger

from core.config import settings
from core.exceptions import (
    PlatformAPIError,
    PlatformAuthError,
    PlatformError,
    PlatformTimeoutError,
)

# Context variable for per-request token (used in HTTP/remote mode where the
# token arrives in the Authorization header instead of the environment).
_request_api_token: contextvars.ContextVar[str | None] = contextvars.ContextVar(
    "_request_api_token", default=None
)


def set_request_api_token(token: str | None) -> None:
    """Set the platform token for the current request context (HTTP mode)."""
    _request_api_token.set(token)


def get_request_api_token() -> str | None:
    """Get the platform token from the current request context."""
    return _request_api_token.get()


def get_request_user_id() -> str | None:
    """Best-effort caller user id, decoded from the current bearer token.

    Account endpoints are NOT scoped to the caller server-side (a superuser would
    see the whole table → huge response, a regular user 403s on the first
    non-owned row), so the tools must pass ``user_id``. When the access token is
    an AceDataCloud JWT it carries ``user_id``; opaque tokens return None.
    """
    token = get_request_api_token()
    if not token or token.count(".") != 2:
        return None
    try:
        import base64
        import json

        payload = token.split(".")[1]
        payload += "=" * (-len(payload) % 4)
        claims = json.loads(base64.urlsafe_b64decode(payload))
        uid = claims.get("user_id")
        return str(uid) if uid else None
    except Exception:
        return None


class PlatformClient:
    """Async HTTP client for the AceDataCloud platform management API.

    Targets ``{base_url}/api/v1`` and authenticates with a platform token.
    """

    def __init__(self, api_token: str | None = None, base_url: str | None = None):
        self.api_token = api_token if api_token is not None else settings.api_token
        self.base_url = (base_url or settings.api_base_url).rstrip("/")
        self.timeout = settings.request_timeout
        logger.info(f"PlatformClient initialized with base_url: {self.base_url}")
        logger.debug(f"Platform token configured: {'Yes' if self.api_token else 'No'}")

    def _get_headers(self, auth_required: bool = True) -> dict[str, str]:
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
        }
        token = get_request_api_token() or self.api_token
        if token:
            headers["authorization"] = f"Bearer {token}"
        elif auth_required:
            logger.error("Platform token not configured!")
            raise PlatformAuthError("Platform token not configured")
        return headers

    def _handle_error_response(self, response: httpx.Response) -> None:
        """Parse an API error response and raise the appropriate exception."""
        status = response.status_code
        try:
            body = response.json()
        except Exception:
            body = {}

        error_obj = body.get("error", {}) if isinstance(body, dict) else {}
        code = (
            error_obj.get("code", f"http_{status}")
            if isinstance(error_obj, dict)
            else f"http_{status}"
        )
        message = (
            (error_obj.get("message") if isinstance(error_obj, dict) else None)
            or (body.get("detail") if isinstance(body, dict) else None)
            or response.text
            or f"HTTP {status}"
        )
        logger.error(f"API error {status} [{code}]: {message}")

        if status in (401, 403):
            raise PlatformAuthError(message)
        raise PlatformAPIError(message=message, code=code, status_code=status)

    async def request(
        self,
        method: str,
        endpoint: str,
        params: dict[str, Any] | None = None,
        json_body: dict[str, Any] | None = None,
        timeout: float | None = None,
        auth_required: bool = True,
    ) -> Any:
        """Make a request to ``/api/v1{endpoint}`` and return parsed JSON.

        Returns ``None`` for empty bodies (e.g. ``204 No Content`` on delete).
        """
        url = f"{self.base_url}/api/v1{endpoint}"
        request_timeout = timeout or self.timeout
        clean_params = {k: v for k, v in (params or {}).items() if v is not None}

        logger.info(f"{method} {url}")
        if json_body is not None:
            logger.debug(f"Body: {json.dumps(json_body, ensure_ascii=False)}")

        async with httpx.AsyncClient() as http_client:
            try:
                response = await http_client.request(
                    method,
                    url,
                    params=clean_params or None,
                    json=json_body,
                    headers=self._get_headers(auth_required),
                    timeout=request_timeout,
                )
                logger.info(f"Response status: {response.status_code}")
                if response.status_code >= 400:
                    self._handle_error_response(response)
                if response.status_code == 204 or not response.content:
                    return None
                return response.json()

            except httpx.TimeoutException as e:
                logger.error(f"Request timeout after {request_timeout}s: {e}")
                raise PlatformTimeoutError(
                    f"Request to {endpoint} timed out after {request_timeout}s"
                ) from e
            except PlatformError:
                raise
            except Exception as e:
                logger.error(f"Request error: {e}")
                raise PlatformAPIError(message=str(e)) from e

    async def get(self, endpoint: str, params: dict[str, Any] | None = None) -> Any:
        return await self.request("GET", endpoint, params=params)

    async def get_public(self, endpoint: str, params: dict[str, Any] | None = None) -> Any:
        """GET a public endpoint (catalog/docs/models/search). Sends the token if
        configured but does not require one."""
        return await self.request("GET", endpoint, params=params, auth_required=False)

    async def post(self, endpoint: str, json_body: dict[str, Any] | None = None) -> Any:
        return await self.request("POST", endpoint, json_body=json_body or {})

    async def delete(self, endpoint: str) -> Any:
        return await self.request("DELETE", endpoint)


# Global client instance
client = PlatformClient()
