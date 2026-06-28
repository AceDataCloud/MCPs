"""Custom exceptions for the Platform MCP server."""


class PlatformError(Exception):
    """Base exception for platform management API errors."""

    def __init__(self, message: str, code: str = "unknown"):
        self.message = message
        self.code = code
        super().__init__(self.message)


class PlatformAuthError(PlatformError):
    """Authentication error (401/403)."""

    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, code="auth_error")


class PlatformAPIError(PlatformError):
    """API request error."""

    def __init__(self, message: str, code: str = "api_error", status_code: int | None = None):
        self.status_code = status_code
        super().__init__(message, code)


class PlatformValidationError(PlatformError):
    """Validation error for request parameters."""

    def __init__(self, message: str):
        super().__init__(message, code="validation_error")


class PlatformTimeoutError(PlatformError):
    """Request timeout error."""

    def __init__(self, message: str = "Request timed out"):
        super().__init__(message, code="timeout_error")
