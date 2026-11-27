"""Authenticated JSON transport for the four Tripo resources."""

from contextvars import ContextVar
from typing import Any, Literal

import httpx

from core.config import settings

Resource = Literal["generations", "models", "animations", "tasks"]
_request_token: ContextVar[str | None] = ContextVar("tripo_request_token", default=None)


def set_request_api_token(token: str | None) -> None:
    _request_token.set(token)


async def post(
    resource: Resource,
    payload: dict[str, Any],
    *,
    idempotency_key: str | None = None,
) -> dict[str, Any]:
    token = _request_token.get() if settings.server_url else settings.api_token
    if not token:
        raise ValueError("An Ace Data Cloud API token is required")
    headers = {"Authorization": f"Bearer {token}"}
    if idempotency_key is not None:
        headers["Idempotency-Key"] = idempotency_key
    async with httpx.AsyncClient(timeout=settings.request_timeout) as client:
        response = await client.post(
            settings.api_base_url.rstrip("/") + "/tripo/" + resource,
            headers=headers,
            json={key: value for key, value in payload.items() if value is not None},
        )
    if response.is_error:
        try:
            body = response.json()
        except ValueError:
            body = {}
        error = body.get("error") if isinstance(body, dict) else None
        detail = error.get("message") if isinstance(error, dict) else None
        raise ValueError(
            f"Tripo returned HTTP {response.status_code}: {detail or response.reason_phrase}"
        )
    response.raise_for_status()
    data = response.json()
    if not isinstance(data, dict):
        raise ValueError("Tripo returned an invalid response")
    return data
