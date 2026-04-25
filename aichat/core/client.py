"""HTTP client for AiChat API."""

import contextvars
import json
from typing import Any

import httpx
from loguru import logger

from core.config import settings
from core.exceptions import AiChatAPIError, AiChatAuthError, AiChatError, AiChatTimeoutError

# Context variable for per-request API token (used in HTTP/remote mode)
_request_api_token: contextvars.ContextVar[str | None] = contextvars.ContextVar(
    "_request_api_token", default=None
)


def set_request_api_token(token: str | None) -> None:
    """Set the API token for the current request context (HTTP mode)."""
    _request_api_token.set(token)


def get_request_api_token() -> str | None:
    """Get the API token from the current request context."""
    return _request_api_token.get()


class AiChatClient:
    """Async HTTP client for AceDataCloud AiChat API."""

    def __init__(self, api_token: str | None = None, base_url: str | None = None):
        """Initialize the AiChat API client.

        Args:
            api_token: API token for authentication. If not provided, uses settings.
            base_url: Base URL for the API. If not provided, uses settings.
        """
        self.api_token = api_token if api_token is not None else settings.api_token
        self.base_url = base_url or settings.api_base_url
        self.timeout = settings.request_timeout

        logger.info(f"AiChatClient initialized with base_url: {self.base_url}")
        logger.debug(f"API token configured: {'Yes' if self.api_token else 'No'}")
        logger.debug(f"Request timeout: {self.timeout}s")

    def _get_headers(self) -> dict[str, str]:
        """Get request headers with authentication."""
        token = get_request_api_token() or self.api_token
        if not token:
            logger.error("API token not configured!")
            raise AiChatAuthError("API token not configured")

        return {
            "accept": "application/json",
            "authorization": f"Bearer {token}",
            "content-type": "application/json",
        }

    def _handle_error_response(self, response: httpx.Response) -> None:
        """Parse API error response and raise the appropriate exception.

        The AceDataCloud API returns errors in the format:
            {"error": {"code": "...", "message": "..."}}
        """
        status = response.status_code
        try:
            body = response.json()
        except Exception:
            body = {}

        error_obj = body.get("error", {})
        code = error_obj.get("code", f"http_{status}")
        message = (
            error_obj.get("message") or body.get("detail") or response.text or f"HTTP {status}"
        )

        logger.error(f"API error {status} [{code}]: {message}")

        if status in (401, 403):
            raise AiChatAuthError(message)
        raise AiChatAPIError(message=message, code=code, status_code=status)

    async def create_conversation(
        self,
        question: str,
        model: str,
        conversation_id: str | None = None,
        preset: str | None = None,
        stateful: bool | None = None,
        references: list[str] | None = None,
    ) -> dict[str, Any]:
        """Create an AI conversation.

        Args:
            question: The prompt or question to be answered.
            model: The model to use for generating the answer.
            conversation_id: Optional conversation ID for continuing a conversation.
            preset: Optional preset model configuration.
            stateful: Whether to use stateful conversation mode.
            references: Optional list of reference sources.

        Returns:
            API response dictionary containing the answer and conversation ID.
        """
        payload: dict[str, Any] = {
            "question": question,
            "model": model,
        }
        if conversation_id is not None:
            payload["id"] = conversation_id
        if preset is not None:
            payload["preset"] = preset
        if stateful is not None:
            payload["stateful"] = stateful
        if references is not None:
            payload["references"] = references

        logger.info(f"Creating conversation with model: {model}")
        logger.debug(f"Question: {question[:100]}...")

        url = f"{self.base_url}/aichat/conversations"

        logger.info(f"POST {url}")
        logger.debug(f"Request payload: {json.dumps(payload, ensure_ascii=False, indent=2)}")

        async with httpx.AsyncClient() as http_client:
            try:
                response = await http_client.post(
                    url,
                    json=payload,
                    headers=self._get_headers(),
                    timeout=self.timeout,
                )

                logger.info(f"Response status: {response.status_code}")

                if response.status_code >= 400:
                    self._handle_error_response(response)

                result = response.json()
                logger.success("Conversation created successfully!")

                return result  # type: ignore[no-any-return]

            except httpx.TimeoutException as e:
                logger.error(f"Request timeout after {self.timeout}s: {e}")
                raise AiChatTimeoutError(
                    f"Request to /aichat/conversations timed out after {self.timeout}s"
                ) from e

            except AiChatError:
                raise

            except Exception as e:
                logger.error(f"Request error: {e}")
                raise AiChatAPIError(message=str(e)) from e


# Global client instance
client = AiChatClient()
