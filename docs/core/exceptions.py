"""Custom exceptions for the AceData Docs MCP server."""


class DocsError(Exception):
    """Base exception for docs API errors."""

    def __init__(self, message: str, code: str = "unknown"):
        self.message = message
        self.code = code
        super().__init__(self.message)


class DocsAPIError(DocsError):
    """API request error."""

    def __init__(self, message: str, code: str = "api_error", status_code: int | None = None):
        self.status_code = status_code
        super().__init__(message, code)


class DocsNotFoundError(DocsError):
    """Requested resource was not found."""

    def __init__(self, message: str = "Not found"):
        super().__init__(message, code="not_found")


class DocsTimeoutError(DocsError):
    """Request timeout error."""

    def __init__(self, message: str = "Request timed out"):
        super().__init__(message, code="timeout_error")
