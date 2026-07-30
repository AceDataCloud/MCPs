"""Custom exceptions for MCP Image2Text server."""


class Image2TextError(Exception):
    def __init__(self, message: str, code: str = "unknown"):
        self.message = message
        self.code = code
        super().__init__(self.message)


class Image2TextAuthError(Image2TextError):
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, code="auth_error")


class Image2TextAPIError(Image2TextError):
    def __init__(self, message: str, code: str = "api_error", status_code: int | None = None):
        self.status_code = status_code
        super().__init__(message, code)


class Image2TextValidationError(Image2TextError):
    def __init__(self, message: str):
        super().__init__(message, code="validation_error")


class Image2TextTimeoutError(Image2TextError):
    def __init__(self, message: str = "Request timed out"):
        super().__init__(message, code="timeout_error")
