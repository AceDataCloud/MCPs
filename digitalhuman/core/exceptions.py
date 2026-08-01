"""Digital Human MCP exceptions."""


class DigitalHumanError(Exception):
    """Base Digital Human error."""

    def __init__(self, message: str, code: str = "unknown") -> None:
        self.message = message
        self.code = code
        super().__init__(message)


class DigitalHumanAuthError(DigitalHumanError):
    """Authentication failure."""

    def __init__(self, message: str = "Authentication failed") -> None:
        super().__init__(message, code="auth_error")


class DigitalHumanAPIError(DigitalHumanError):
    """Error returned by the Digital Human API."""

    def __init__(
        self,
        message: str,
        code: str = "api_error",
        status_code: int | None = None,
    ) -> None:
        self.status_code = status_code
        super().__init__(message, code=code)


class DigitalHumanTimeoutError(DigitalHumanError):
    """Digital Human request timeout."""

    def __init__(self, message: str = "Request timed out") -> None:
        super().__init__(message, code="timeout_error")
