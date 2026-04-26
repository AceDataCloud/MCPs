"""Custom exceptions for MCP DeepSeek server."""


class DeepSeekError(Exception):
    """Base exception for DeepSeek API errors."""

    def __init__(self, message: str, code: str = "unknown"):
        self.message = message
        self.code = code
        super().__init__(self.message)


class DeepSeekAuthError(DeepSeekError):
    """Authentication error."""

    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, code="auth_error")


class DeepSeekAPIError(DeepSeekError):
    """API request error."""

    def __init__(self, message: str, code: str = "api_error", status_code: int | None = None):
        self.status_code = status_code
        super().__init__(message, code)


class DeepSeekValidationError(DeepSeekError):
    """Validation error for request parameters."""

    def __init__(self, message: str):
        super().__init__(message, code="validation_error")


class DeepSeekTimeoutError(DeepSeekError):
    """Request timeout error."""

    def __init__(self, message: str = "Request timed out"):
        super().__init__(message, code="timeout_error")
