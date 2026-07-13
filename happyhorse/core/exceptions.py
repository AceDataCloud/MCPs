"""Happy Horse MCP exceptions."""


class HappyHorseError(Exception):
    """Base Happy Horse error."""

    def __init__(self, message: str, code: str = "unknown") -> None:
        self.message = message
        self.code = code
        super().__init__(message)


class HappyHorseAuthError(HappyHorseError):
    """Authentication failure."""

    def __init__(self, message: str = "Authentication failed") -> None:
        super().__init__(message, code="auth_error")


class HappyHorseAPIError(HappyHorseError):
    """Error returned by the Happy Horse API."""

    def __init__(
        self,
        message: str,
        code: str = "api_error",
        status_code: int | None = None,
    ) -> None:
        self.status_code = status_code
        super().__init__(message, code=code)


class HappyHorseTimeoutError(HappyHorseError):
    """Happy Horse request timeout."""

    def __init__(self, message: str = "Request timed out") -> None:
        super().__init__(message, code="timeout_error")
