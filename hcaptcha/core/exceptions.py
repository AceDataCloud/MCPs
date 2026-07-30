"""Custom exceptions for MCP HCaptcha server."""


class HCaptchaError(Exception):
    def __init__(self, message: str, code: str = "unknown"):
        self.message = message
        self.code = code
        super().__init__(self.message)


class HCaptchaAuthError(HCaptchaError):
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, code="auth_error")


class HCaptchaAPIError(HCaptchaError):
    def __init__(self, message: str, code: str = "api_error", status_code: int | None = None):
        self.status_code = status_code
        super().__init__(message, code)


class HCaptchaValidationError(HCaptchaError):
    def __init__(self, message: str):
        super().__init__(message, code="validation_error")


class HCaptchaTimeoutError(HCaptchaError):
    def __init__(self, message: str = "Request timed out"):
        super().__init__(message, code="timeout_error")
