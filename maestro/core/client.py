"""Async HTTP client for the public Maestro API."""

import contextvars
from typing import Any

import httpx

from core.config import settings
from core.exceptions import MaestroAPIError, MaestroAuthError, MaestroError, MaestroTimeoutError

_request_api_token: contextvars.ContextVar[str | None] = contextvars.ContextVar(
    "_request_api_token", default=None
)


def set_request_api_token(token: str | None) -> None:
    """Set the token for the current remote MCP request."""
    _request_api_token.set(token)


def get_request_api_token() -> str | None:
    """Return the token for the current remote MCP request."""
    return _request_api_token.get()


class MaestroClient:
    """Client for Maestro video and task endpoints."""

    def __init__(self, api_token: str | None = None, base_url: str | None = None) -> None:
        self.api_token = api_token if api_token is not None else settings.api_token
        self.base_url = (base_url or settings.api_base_url).rstrip("/")
        self.timeout = settings.request_timeout

    def _headers(self) -> dict[str, str]:
        token = get_request_api_token() or self.api_token
        if not token:
            raise MaestroAuthError("API token not configured")
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
        if response.status_code in (401, 403):
            raise MaestroAuthError(message)
        raise MaestroAPIError(message, code=code, status_code=response.status_code)

    async def request(self, endpoint: str, payload: dict[str, Any]) -> dict[str, Any]:
        """POST JSON to a Maestro endpoint."""
        try:
            async with httpx.AsyncClient() as http_client:
                response = await http_client.post(
                    f"{self.base_url}{endpoint}",
                    json=payload,
                    headers=self._headers(),
                    timeout=self.timeout,
                )
            if response.status_code >= 400:
                self._raise_for_error(response)
            result = response.json()
            if not isinstance(result, dict):
                raise MaestroAPIError("Maestro returned a non-object response")
            return result
        except httpx.TimeoutException as exc:
            raise MaestroTimeoutError(
                f"Request to {endpoint} timed out after {self.timeout}s"
            ) from exc
        except MaestroError:
            raise
        except (httpx.HTTPError, ValueError) as exc:
            raise MaestroAPIError(str(exc)) from exc

    async def create_video(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Create or iterate on a Maestro video."""
        return await self.request("/maestro/videos", payload)

    async def get_task(self, task_id: str) -> dict[str, Any]:
        """Retrieve one Maestro task."""
        return await self.request("/maestro/tasks", {"id": task_id, "action": "retrieve"})

    async def list_tasks(
        self,
        limit: int,
        created_at_min: int | None = None,
        created_at_max: int | None = None,
    ) -> dict[str, Any]:
        """List recent Maestro tasks for the authenticated user."""
        payload: dict[str, Any] = {"action": "retrieve_batch", "limit": limit}
        if created_at_min is not None:
            payload["created_at_min"] = created_at_min
        if created_at_max is not None:
            payload["created_at_max"] = created_at_max
        return await self.request("/maestro/tasks", payload)


client = MaestroClient()
