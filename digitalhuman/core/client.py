"""Async HTTP client for the Digital Human API."""

import contextvars
from typing import Any

import httpx

from core.config import settings
from core.exceptions import (
    DigitalHumanAPIError,
    DigitalHumanAuthError,
    DigitalHumanError,
    DigitalHumanTimeoutError,
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


class DigitalHumanClient:
    """Client for Digital Human video, voice, and task endpoints."""

    def __init__(self, api_token: str | None = None, base_url: str | None = None) -> None:
        self.api_token = api_token if api_token is not None else settings.api_token
        self.base_url = (base_url or settings.api_base_url).rstrip("/")
        self.timeout = settings.request_timeout

    def _headers(self) -> dict[str, str]:
        token = get_request_api_token() or self.api_token
        if not token:
            raise DigitalHumanAuthError("API token not configured")
        return {
            "accept": "application/json",
            "authorization": "Bearer " + token,
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
            raise DigitalHumanAuthError(message)
        raise DigitalHumanAPIError(message, code=code, status_code=response.status_code)

    async def request(self, endpoint: str, payload: dict[str, Any]) -> dict[str, Any]:
        """POST JSON to a Digital Human endpoint."""
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
                raise DigitalHumanAPIError("Digital Human returned a non-object response")
            return result
        except httpx.TimeoutException as exc:
            raise DigitalHumanTimeoutError(
                f"Request to {endpoint} timed out after {self.timeout}s"
            ) from exc
        except DigitalHumanError:
            raise
        except (httpx.HTTPError, ValueError) as exc:
            raise DigitalHumanAPIError(str(exc)) from exc

    async def create_video(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Create a digital human video."""
        return await self.request("/digital-human/videos", payload)

    async def clone_voice(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Clone a voice from reference audio."""
        return await self.request("/digital-human/voices", payload)

    async def get_task(self, task_id: str, action: str | None = None) -> dict[str, Any]:
        """Retrieve one task."""
        payload: dict[str, Any] = {"task_id": task_id}
        if action is not None:
            payload["action"] = action
        return await self.request("/digital-human/tasks", payload)

    async def get_tasks_batch(self, task_ids: list[str]) -> dict[str, Any]:
        """Retrieve multiple tasks."""
        return await self.request(
            "/digital-human/tasks",
            {"task_id": task_ids, "action": "retrieve_batch"},
        )

    async def delete_task(self, task_id: str) -> dict[str, Any]:
        """Delete one task."""
        return await self.request("/digital-human/tasks", {"task_id": task_id, "action": "delete"})


client = DigitalHumanClient()
