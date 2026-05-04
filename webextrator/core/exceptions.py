"""Custom exceptions for MCP WebExtrator server."""


class WebExtraterError(Exception):
    """Base exception for WebExtrator API errors."""

    def __init__(self, message: str, code: str = "unknown"):
        self.message = message
        self.code = code
        super().__init__(self.message)


class WebExtraterAuthError(WebExtraterError):
    """Authentication error."""

    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, code="auth_error")


class WebExtraterAPIError(WebExtraterError):
    """API request error."""

    def __init__(self, message: str, code: str = "api_error", status_code: int | None = None):
        self.status_code = status_code
        super().__init__(message, code)


class WebExtraterValidationError(WebExtraterError):
    """Validation error for request parameters."""

    def __init__(self, message: str):
        super().__init__(message, code="validation_error")


class WebExtraterTimeoutError(WebExtraterError):
    """Request timeout error."""

    def __init__(self, message: str = "Request timed out"):
        super().__init__(message, code="timeout_error")
