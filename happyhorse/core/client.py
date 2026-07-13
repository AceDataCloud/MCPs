"""Async HTTP client for the public Happy Horse API."""

import contextvars
from typing import Any

import httpx

from core.config import settings
from core.exceptions import (
    HappyHorseAPIError,
    HappyHorseAuthError,
    HappyHorseError,
    HappyHorseTimeoutError,
)

_request_api_token: contextvars.ContextVar[str | None] = contextvars.ContextVar(
    "_request_api_token", default=None
)


def set_request_api_token(token: str | None) -> None:
    """Set the token for the current remote MCP request."""
    _request_api_token.set(token)


def get_request_api_token() -> str | None:
    """Return the token for the current remote MCP request."""
    return _request_api_token.get()


class HappyHorseClient:
    """Client for Happy Horse video and task endpoints."""

    def __init__(self, api_token: str | None = None, base_url: str | None = None) -> None:
        self.api_token = api_token if api_token is not None else settings.api_token
        self.base_url = (base_url or settings.api_base_url).rstrip("/")
        self.timeout = settings.request_timeout

    def _headers(self) -> dict[str, str]:
        token = get_request_api_token() or self.api_token
        if not token:
            raise HappyHorseAuthError("API token not configured")
        return {
            "accept": "application/json",
            "authorization": f"Bearer {token}",
            "content-type": "application/json",
        }

    @staticmethod
    def _raise_for_error(response: httpx.Response) -> None:
        try:
            body = response.json()
        except ValueError:
            body = {}
        error = body.get("error") if isinstance(body.get("error"), dict) else {}
        message = (
            error.get("message") or body.get("detail") or response.text or "API request failed"
        )
        code = error.get("code") or f"http_{response.status_code}"
        if response.status_code == 401:
            raise HappyHorseAuthError(message)
        raise HappyHorseAPIError(message, code=code, status_code=response.status_code)

    async def request(self, endpoint: str, payload: dict[str, Any]) -> dict[str, Any]:
        """POST JSON to a Happy Horse endpoint."""
        request_payload = {key: value for key, value in payload.items() if value is not None}
        try:
            async with httpx.AsyncClient() as http_client:
                response = await http_client.post(
                    f"{self.base_url}{endpoint}",
                    json=request_payload,
                    headers=self._headers(),
                    timeout=self.timeout,
                )
            if response.status_code >= 400:
                self._raise_for_error(response)
            result = response.json()
            if not isinstance(result, dict):
                raise HappyHorseAPIError("Happy Horse returned a non-object response")
            return result
        except httpx.TimeoutException as exc:
            raise HappyHorseTimeoutError(
                f"Request to {endpoint} timed out after {self.timeout}s"
            ) from exc
        except HappyHorseError:
            raise
        except (httpx.HTTPError, ValueError) as exc:
            raise HappyHorseAPIError(str(exc)) from exc

    async def generate_video(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Submit a Happy Horse generation or edit operation."""
        request_payload = dict(payload)
        if not request_payload.get("callback_url"):
            request_payload["async"] = True
        return await self.request("/happyhorse/videos", request_payload)

    async def get_task(self, task_id: str) -> dict[str, Any]:
        """Retrieve one Happy Horse task."""
        return await self.request("/happyhorse/tasks", {"id": task_id, "action": "retrieve"})

    async def get_tasks_batch(self, task_ids: list[str]) -> dict[str, Any]:
        """Retrieve multiple Happy Horse tasks."""
        return await self.request(
            "/happyhorse/tasks", {"ids": task_ids, "action": "retrieve_batch"}
        )


client = HappyHorseClient()
