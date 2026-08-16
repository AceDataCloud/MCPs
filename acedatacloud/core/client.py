"""Async HTTP client for the AceDataCloud platform management API."""

import contextvars
from dataclasses import dataclass
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

_request_api_token: contextvars.ContextVar[str | None] = contextvars.ContextVar(
    "_request_api_token", default=None
)
_request_subject: contextvars.ContextVar[tuple[str, dict[str, Any]] | None] = (
    contextvars.ContextVar("_request_subject", default=None)
)


@dataclass(frozen=True)
class TextResponse:
    """A bounded non-JSON response returned by the platform API."""

    content: str
    content_type: str
    filename: str | None
    size_bytes: int


def set_request_api_token(token: str | None) -> contextvars.Token[str | None]:
    """Set the platform token and invalidate cached identity for this context."""
    _request_subject.set(None)
    return _request_api_token.set(token)


def reset_request_api_token(token: contextvars.Token[str | None]) -> None:
    """Restore the previous request token and clear cached identity."""
    _request_api_token.reset(token)
    _request_subject.set(None)


def get_request_api_token() -> str | None:
    """Get the platform token from the current request context."""
    return _request_api_token.get()


def _effective_api_token() -> str:
    token = get_request_api_token() or client.api_token
    if not token:
        raise PlatformAuthError("Platform token not configured")
    return token


async def get_request_subject() -> dict[str, Any]:
    """Resolve and cache the authenticated platform-token subject."""
    token = _effective_api_token()
    cached = _request_subject.get()
    if cached and cached[0] == token:
        return cached[1]

    result = await client.get("/platform-tokens/me/")
    if not isinstance(result, dict) or not result.get("id"):
        raise PlatformAuthError("Unable to resolve the authenticated platform-token subject")
    subject = dict(result)
    _request_subject.set((token, subject))
    return subject


async def get_request_user_id() -> str:
    """Return the authenticated subject ID, including for opaque platform tokens."""
    return str((await get_request_subject())["id"])


class PlatformClient:
    """Async HTTP client targeting ``{base_url}/api/v1``."""

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
        if not auth_required:
            return headers
        token = get_request_api_token() or self.api_token
        if token:
            headers["authorization"] = f"Bearer {token}"
        else:
            logger.error("Platform token not configured")
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
        logger.error(f"API error {status} [{code}]")

        if status == 401:
            raise PlatformAuthError(message)
        if status == 403:
            raise PlatformAPIError(
                message=message,
                code="permission_denied",
                status_code=status,
            )
        raise PlatformAPIError(message=message, code=code, status_code=status)

    async def request(
        self,
        method: str,
        endpoint: str,
        params: dict[str, Any] | list[tuple[str, Any]] | None = None,
        json_body: dict[str, Any] | None = None,
        timeout: float | None = None,
        auth_required: bool = True,
        follow_redirects: bool = False,
    ) -> Any:
        """Make a JSON request to ``/api/v1{endpoint}``."""
        response = await self._send(
            method,
            endpoint,
            params=params,
            json_body=json_body,
            timeout=timeout,
            auth_required=auth_required,
            follow_redirects=follow_redirects,
        )
        if response.status_code == 204 or not response.content:
            return None
        try:
            return response.json()
        except ValueError as error:
            raise PlatformAPIError(
                message="The platform returned a non-JSON response",
                code="invalid_response",
                status_code=response.status_code,
            ) from error

    async def request_text(
        self,
        endpoint: str,
        params: dict[str, Any] | list[tuple[str, Any]] | None = None,
        *,
        max_bytes: int = 2 * 1024 * 1024,
    ) -> TextResponse:
        """GET a bounded text/CSV response without following redirects."""
        response = await self._send("GET", endpoint, params=params)
        size = len(response.content)
        if size > max_bytes:
            raise PlatformAPIError(
                message=(
                    f"Response is {size} bytes, above the {max_bytes}-byte limit; "
                    "narrow the query filters"
                ),
                code="response_too_large",
                status_code=413,
            )
        content_type = response.headers.get("content-type", "text/plain").split(";", 1)[0]
        if not (content_type.startswith("text/") or content_type in {"application/csv"}):
            raise PlatformAPIError(
                message=f"Unsupported response content type: {content_type}",
                code="invalid_response_type",
                status_code=response.status_code,
            )
        return TextResponse(
            content=response.text,
            content_type=content_type,
            filename=_content_disposition_filename(response.headers.get("content-disposition")),
            size_bytes=size,
        )

    async def _send(
        self,
        method: str,
        endpoint: str,
        params: dict[str, Any] | list[tuple[str, Any]] | None = None,
        json_body: dict[str, Any] | None = None,
        timeout: float | None = None,
        auth_required: bool = True,
        follow_redirects: bool = False,
    ) -> httpx.Response:
        url = f"{self.base_url}/api/v1{endpoint}"
        request_timeout = timeout or self.timeout
        clean_params = _clean_params(params)

        logger.info(f"{method} {url}")
        if json_body is not None:
            logger.debug("JSON body configured (values redacted from logs)")

        async with httpx.AsyncClient(follow_redirects=follow_redirects) as http_client:
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
                return response
            except httpx.TimeoutException as error:
                logger.error(f"Request timeout after {request_timeout}s")
                raise PlatformTimeoutError(
                    f"Request to {endpoint} timed out after {request_timeout}s"
                ) from error
            except PlatformError:
                raise
            except Exception as error:
                logger.error(f"Request error: {type(error).__name__}")
                raise PlatformAPIError(message=str(error)) from error

    async def get(
        self,
        endpoint: str,
        params: dict[str, Any] | list[tuple[str, Any]] | None = None,
    ) -> Any:
        return await self.request("GET", endpoint, params=params)

    async def get_public(
        self,
        endpoint: str,
        params: dict[str, Any] | list[tuple[str, Any]] | None = None,
    ) -> Any:
        """GET a public endpoint without forwarding caller credentials."""
        return await self.request("GET", endpoint, params=params, auth_required=False)

    async def post(
        self,
        endpoint: str,
        json_body: dict[str, Any] | None = None,
        params: dict[str, Any] | list[tuple[str, Any]] | None = None,
    ) -> Any:
        return await self.request("POST", endpoint, params=params, json_body=json_body or {})

    async def patch(self, endpoint: str, json_body: dict[str, Any] | None = None) -> Any:
        return await self.request("PATCH", endpoint, json_body=json_body or {})

    async def put(self, endpoint: str, json_body: dict[str, Any] | None = None) -> Any:
        return await self.request("PUT", endpoint, json_body=json_body or {})

    async def delete(
        self,
        endpoint: str,
        params: dict[str, Any] | list[tuple[str, Any]] | None = None,
    ) -> Any:
        return await self.request("DELETE", endpoint, params=params)


def _clean_params(
    params: dict[str, Any] | list[tuple[str, Any]] | None,
) -> list[tuple[str, Any]]:
    if not params:
        return []
    items = params.items() if isinstance(params, dict) else params
    clean: list[tuple[str, Any]] = []
    for key, value in items:
        if value is None:
            continue
        if isinstance(value, list | tuple | set):
            clean.extend((key, item) for item in value if item is not None)
        else:
            clean.append((key, value))
    return clean


def _content_disposition_filename(value: str | None) -> str | None:
    if not value:
        return None
    for part in value.split(";"):
        key, separator, raw = part.strip().partition("=")
        if separator and key.lower() == "filename":
            return raw.strip().strip('"') or None
    return None


client = PlatformClient()
