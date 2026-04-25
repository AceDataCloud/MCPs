"""Custom exceptions for MCP OpenAI server."""


class OpenaiError(Exception):
    """Base exception for OpenAI API errors."""

    def __init__(self, message: str, code: str = "unknown"):
        self.message = message
        self.code = code
        super().__init__(self.message)


class OpenaiAuthError(OpenaiError):
    """Authentication error."""

    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, code="auth_error")


class OpenaiAPIError(OpenaiError):
    """API request error."""

    def __init__(self, message: str, code: str = "api_error", status_code: int | None = None):
        self.status_code = status_code
        super().__init__(message, code)


class OpenaiValidationError(OpenaiError):
    """Validation error for request parameters."""

    def __init__(self, message: str):
        super().__init__(message, code="validation_error")


class OpenaiTimeoutError(OpenaiError):
    """Request timeout error."""

    def __init__(self, message: str = "Request timed out"):
        super().__init__(message, code="timeout_error")
