"""Safe error metadata shared by OpenAI HTTP clients and tools."""

import json
import re
from collections.abc import Iterable
from typing import Any

import httpx

# Unknown upstream codes can contain supplier/model names; expose only known
# provider-neutral codes and use an HTTP-derived fallback for everything else.
_PUBLIC_CODES = frozenset(
    {
        "api_error",
        "invalid_api_key",
        "invalid_token",
        "unauthorized",
        "forbidden",
        "permission_denied",
        "access_denied",
        "authentication_error",
        "invalid_request",
        "invalid_request_error",
        "bad_request",
        "invalid_parameter",
        "validation_error",
        "model_not_found",
        "not_found",
        "context_length_exceeded",
        "rate_limit_exceeded",
        "rate_limit_error",
        "insufficient_quota",
        "insufficient_balance",
        "content_filter",
        "content_policy_violation",
        "moderation_blocked",
        "internal_error",
        "server_error",
        "service_unavailable",
        "overloaded",
        "timeout",
        "timeout_error",
        "request_timeout",
        "network_error",
        "invalid_response",
        "auth_error",
    }
)
_MESSAGES = {
    400: "Invalid API request.",
    401: "API authentication failed. Check the application API key.",
    403: "API access denied. Check permissions and content restrictions.",
    404: "The requested API resource was not found.",
    408: "The API request timed out.",
    422: "The API request could not be processed. Check its parameters.",
    429: "API rate or usage limit exceeded. Check limits before retrying.",
}
_LOCAL_MESSAGES = {
    "auth_error": "API authentication failed. Check the application API key.",
    "validation_error": "Invalid tool arguments.",
    "timeout_error": "The API request timed out.",
    "network_error": "Could not reach the API service.",
    "invalid_response": "The API response could not be processed.",
}


def public_http_message(status_code: int) -> str:
    """Do not expose an untrusted JSON/HTML body as a customer message."""
    if status_code in _MESSAGES:
        return _MESSAGES[status_code]
    if status_code >= 500:
        return "The API service is temporarily unavailable."
    return "The API request failed."


def public_error_code(value: Any, fallback: str) -> str:
    """Keep known public codes, not arbitrary upstream diagnostics."""
    return value if isinstance(value, str) and value in _PUBLIC_CODES else fallback


def public_request_id(value: Any, secrets: Iterable[str] = ()) -> str | None:
    """Correlation IDs must not be URLs, tokens, or arbitrary text."""
    if not isinstance(value, str) or not re.fullmatch(r"[A-Za-z0-9_-]{1,128}", value):
        return None
    if re.search(r"(?:sk[-_]|bearer|token|secret|password)", value, re.IGNORECASE):
        return None
    if any(secret and secret in value for secret in secrets):
        return None
    return value


class OpenAIError(Exception):
    """Missing HTTP metadata stays null, never a fabricated HTTP response."""

    def __init__(
        self,
        message: str,
        code: str = "unknown",
        status_code: int | None = None,
        request_id: str | None = None,
    ):
        self.message = message
        self.code = code
        self.status_code = status_code
        self.request_id = request_id
        super().__init__(message)


class OpenAIAuthError(OpenAIError):
    """Authentication/permission error retaining the actual HTTP status."""

    def __init__(
        self,
        message: str = "Authentication failed",
        code: str = "auth_error",
        status_code: int | None = None,
        request_id: str | None = None,
    ):
        super().__init__(message, code, status_code, request_id)


class OpenAIAPIError(OpenAIError):
    """API request error."""

    def __init__(
        self,
        message: str,
        code: str = "api_error",
        status_code: int | None = None,
        request_id: str | None = None,
    ):
        super().__init__(message, code, status_code, request_id)


class OpenAIValidationError(OpenAIError):
    """Request parameter validation error."""

    def __init__(self, message: str):
        super().__init__(message, code="validation_error")


class OpenAITimeoutError(OpenAIError):
    """Transport timeout, without inventing an HTTP 408 or 504."""

    def __init__(self, message: str = "Request timed out"):
        super().__init__(message, code="timeout_error")


class OpenAINetworkError(OpenAIError):
    """Connection/read/protocol failure without a usable API response."""

    def __init__(self) -> None:
        super().__init__("Could not reach the API service.", code="network_error")


def error_from_response(response: httpx.Response, secrets: Iterable[str] = ()) -> OpenAIError:
    """Keep safe metadata only; JSON messages and non-JSON bodies are untrusted."""
    status = response.status_code
    try:
        body = response.json()
    except (ValueError, UnicodeError):
        body = {}
    error_obj = body.get("error") if isinstance(body, dict) else None
    error_obj = error_obj if isinstance(error_obj, dict) else {}
    code = public_error_code(error_obj.get("code"), f"http_{status}")
    request_id = public_request_id(response.headers.get("x-request-id"), secrets)
    error_type = OpenAIAuthError if status in (401, 403) else OpenAIAPIError
    return error_type(
        message=public_http_message(status), code=code, status_code=status, request_id=request_id
    )


def format_tool_error(
    error: Exception, fallback: str = "API Error", *, secrets: Iterable[str] = ()
) -> str:
    """Retain legacy error/message fields while adding safe structured metadata."""
    status_code = None
    request_id = None
    code = "internal_error"
    message = "The operation failed."
    label = fallback
    download_error = isinstance(error, httpx.HTTPStatusError)
    if isinstance(error, httpx.HTTPStatusError):
        error = error_from_response(error.response, secrets)
    elif isinstance(error, httpx.TimeoutException):
        error = OpenAITimeoutError()
    elif isinstance(error, httpx.RequestError):
        error = OpenAINetworkError()
    if isinstance(error, OpenAIError):
        if isinstance(error.status_code, int) and 400 <= error.status_code <= 599:
            status_code = error.status_code
        request_id = public_request_id(error.request_id, secrets)
        code = public_error_code(error.code, f"http_{status_code}" if status_code else "api_error")
        message = (
            public_http_message(status_code)
            if status_code
            else _LOCAL_MESSAGES.get(code, "The API request failed.")
        )
        if isinstance(error, OpenAIAuthError) and not download_error:
            label = "Authentication Error"
        elif isinstance(error, OpenAIAPIError) and not download_error:
            label = "API Error"
    return json.dumps(
        {
            "error": label,
            "message": message,
            "status_code": status_code,
            "code": code,
            "request_id": request_id,
        },
        ensure_ascii=False,
    )
