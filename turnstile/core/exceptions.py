"""Custom exceptions for MCP Turnstile server."""


class TurnstileError(Exception):
    def __init__(self, message: str, code: str = "unknown"):
        self.message = message
        self.code = code
        super().__init__(self.message)


class TurnstileAuthError(TurnstileError):
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, code="auth_error")


class TurnstileAPIError(TurnstileError):
    def __init__(self, message: str, code: str = "api_error", status_code: int | None = None):
        self.status_code = status_code
        super().__init__(message, code)


class TurnstileValidationError(TurnstileError):
    def __init__(self, message: str):
        super().__init__(message, code="validation_error")


class TurnstileTimeoutError(TurnstileError):
    def __init__(self, message: str = "Request timed out"):
        super().__init__(message, code="timeout_error")
