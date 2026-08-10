"""API and proxy usage self-service tools."""

import datetime as dt
from typing import Annotated, Literal

from pydantic import Field

from core.client import client, get_request_user_id
from core.exceptions import PlatformError
from core.server import mcp
from core.utils import dumps, error_json

Perspective = Literal["billing", "actor", "both"]


def _params(
    application_id: str | list[str] | None,
    resource_id: str | list[str] | None,
    credential_id: str | list[str] | None,
    status_code: int | list[int] | None,
    created_at_from: str | None,
    created_at_to: str | None,
    perspective: Perspective,
) -> dict:
    return {
        "application_id": application_id,
        "api_id": resource_id,
        "credential_id": credential_id,
        "status_code": status_code,
        "created_at_from": created_at_from,
        "created_at_to": created_at_to,
        "perspective": perspective,
    }


@mcp.tool()
async def acedatacloud_list_usage(
    application_id: Annotated[
        str | list[str] | None, Field(description="Application UUID filters.")
    ] = None,
    api_id: Annotated[str | list[str] | None, Field(description="API UUID filters.")] = None,
    credential_id: Annotated[
        str | list[str] | None, Field(description="Credential UUID filters.")
    ] = None,
    status_code: Annotated[
        int | list[int] | None, Field(description="HTTP status filters.")
    ] = None,
    created_at_from: Annotated[str | None, Field(description="ISO-8601 lower time bound.")] = None,
    created_at_to: Annotated[str | None, Field(description="ISO-8601 upper time bound.")] = None,
    days: Annotated[
        int | None,
        Field(description="Compatibility shortcut: records newer than N days.", ge=1, le=365),
    ] = None,
    perspective: Annotated[
        Perspective, Field(description="Billing, actor, or union perspective.")
    ] = "both",
    ordering: Annotated[
        Literal["-created_at", "-updated_at"] | None, Field(description="Usage ordering.")
    ] = None,
    limit: Annotated[int, Field(description="Max records.", ge=1, le=100)] = 20,
    offset: Annotated[int, Field(description="Pagination offset.", ge=0)] = 0,
) -> str:
    """List API usage with complete backend-supported filters."""
    try:
        if days is not None and created_at_from is None:
            created_at_from = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=days)).strftime(
                "%Y-%m-%dT%H:%M:%SZ"
            )
        params = _params(
            application_id,
            api_id,
            credential_id,
            status_code,
            created_at_from,
            created_at_to,
            perspective,
        )
        params.update(
            {
                "user_id": await get_request_user_id(),
                "ordering": ordering,
                "limit": limit,
                "offset": offset,
            }
        )
        return dumps(await client.get("/usage/apis/", params))
    except PlatformError as error:
        return error_json(error.code, error.message)


@mcp.tool()
async def acedatacloud_get_usage(
    usage_id: Annotated[str, Field(description="API usage UUID.")],
) -> str:
    """Get one caller-authorized API usage record."""
    try:
        return dumps(await client.get(f"/usage/apis/{usage_id}"))
    except PlatformError as error:
        return error_json(error.code, error.message)


@mcp.tool()
async def acedatacloud_list_usage_status_codes(
    created_at_from: Annotated[str | None, Field(description="ISO-8601 lower time bound.")] = None,
    created_at_to: Annotated[str | None, Field(description="ISO-8601 upper time bound.")] = None,
    perspective: Annotated[
        Perspective, Field(description="Billing, actor, or union perspective.")
    ] = "both",
) -> str:
    """List distinct HTTP status codes seen by the caller."""
    try:
        return dumps(
            await client.get(
                "/usage/apis/status-codes/",
                {
                    "created_at_from": created_at_from,
                    "created_at_to": created_at_to,
                    "perspective": perspective,
                },
            )
        )
    except PlatformError as error:
        return error_json(error.code, error.message)


@mcp.tool()
async def acedatacloud_export_usage(
    application_id: Annotated[
        str | list[str] | None, Field(description="Application UUID filters.")
    ] = None,
    api_id: Annotated[str | list[str] | None, Field(description="API UUID filters.")] = None,
    credential_id: Annotated[
        str | list[str] | None, Field(description="Credential UUID filters.")
    ] = None,
    status_code: Annotated[
        int | list[int] | None, Field(description="HTTP status filters.")
    ] = None,
    created_at_from: Annotated[str | None, Field(description="ISO-8601 lower time bound.")] = None,
    created_at_to: Annotated[str | None, Field(description="ISO-8601 upper time bound.")] = None,
    perspective: Annotated[
        Perspective, Field(description="Billing, actor, or union perspective.")
    ] = "both",
    max_bytes: Annotated[
        int, Field(description="Maximum CSV bytes returned.", ge=1024, le=10_485_760)
    ] = 2_097_152,
) -> str:
    """Export bounded API usage CSV; narrow filters when the response exceeds the limit."""
    try:
        params = _params(
            application_id,
            api_id,
            credential_id,
            status_code,
            created_at_from,
            created_at_to,
            perspective,
        )
        result = await client.request_text("/usage/apis/export/", params, max_bytes=max_bytes)
        return dumps(
            {
                "filename": result.filename,
                "content_type": result.content_type,
                "size_bytes": result.size_bytes,
                "content": result.content,
            }
        )
    except PlatformError as error:
        return error_json(error.code, error.message)


@mcp.tool()
async def acedatacloud_list_proxy_usage(
    application_id: Annotated[
        str | list[str] | None, Field(description="Proxy application UUID filters.")
    ] = None,
    proxy_id: Annotated[str | list[str] | None, Field(description="Proxy UUID filters.")] = None,
    ordering: Annotated[
        Literal["-created_at", "-updated_at"] | None, Field(description="Usage ordering.")
    ] = None,
    limit: Annotated[int, Field(description="Max records.", ge=1, le=100)] = 20,
    offset: Annotated[int, Field(description="Pagination offset.", ge=0)] = 0,
) -> str:
    """List caller-owned proxy usage records."""
    try:
        return dumps(
            await client.get(
                "/usage/proxies/",
                {
                    "user_id": await get_request_user_id(),
                    "application_id": application_id,
                    "proxy_id": proxy_id,
                    "ordering": ordering,
                    "limit": limit,
                    "offset": offset,
                },
            )
        )
    except PlatformError as error:
        return error_json(error.code, error.message)


@mcp.tool()
async def acedatacloud_get_proxy_usage(
    usage_id: Annotated[str, Field(description="Proxy usage UUID.")],
) -> str:
    """Get one caller-authorized proxy usage record."""
    try:
        return dumps(await client.get(f"/usage/proxies/{usage_id}"))
    except PlatformError as error:
        return error_json(error.code, error.message)
