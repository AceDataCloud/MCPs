"""Maestro MCP exceptions."""


class MaestroError(Exception):
    """Base Maestro error."""

    def __init__(self, message: str, code: str = "unknown") -> None:
        self.message = message
        self.code = code
        super().__init__(message)


class MaestroAuthError(MaestroError):
    """Authentication or authorization failure."""

    def __init__(self, message: str = "Authentication failed") -> None:
        super().__init__(message, code="auth_error")


class MaestroAPIError(MaestroError):
    """Error returned by the Maestro API."""

    def __init__(
        self,
        message: str,
        code: str = "api_error",
        status_code: int | None = None,
    ) -> None:
        self.status_code = status_code
        super().__init__(message, code=code)


class MaestroTimeoutError(MaestroError):
    """Maestro request timeout."""

    def __init__(self, message: str = "Request timed out") -> None:
        super().__init__(message, code="timeout_error")
