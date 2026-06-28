"""Public catalog tools: services, APIs, OpenAPI specs, pricing, datasets, integrations.

All read AceDataCloud's public, read-only endpoints — no token required.
"""

from typing import Annotated

from pydantic import Field

from core.client import client
from core.exceptions import PlatformAPIError, PlatformAuthError
from core.server import mcp
from core.utils import dumps, error_json, unwrap

PUBLIC_STAGES = ["Beta", "Production"]


async def _list_services_raw() -> list:
    data = await client.get_public("/services/", {"private": "false", "limit": 200})
    items = unwrap(data)
    return items if isinstance(items, list) else []


async def _resolve_service_id(service: str) -> str | None:
    if not service:
        return None
    for s in await _list_services_raw():
        if isinstance(s, dict) and (s.get("alias") == service or str(s.get("id")) == service):
            return str(s.get("id"))
    return None


def _filter_public(apis: list, service_id: str | None = None) -> list:
    out = []
    for a in apis:
        if not isinstance(a, dict) or a.get("stage") not in PUBLIC_STAGES:
            continue
        if service_id is not None and str(a.get("service_id")) != str(service_id):
            continue
        out.append(a)
    return out


@mcp.tool()
async def acedatacloud_list_services(
    service_type: Annotated[
        str | None,
        Field(
            description="Optional filter: Api, Proxy, Integration, Dataset, Agent, Introduction."
        ),
    ] = None,
    search: Annotated[
        str | None, Field(description="Optional case-insensitive alias/title substring.")
    ] = None,
) -> str:
    """List AceDataCloud services (the public catalog of API groupings). No token needed."""
    try:
        data = await client.get_public(
            "/services/", {"private": "false", "limit": 200, "type": service_type}
        )
        items = unwrap(data)
        items = items if isinstance(items, list) else []
        if search:
            s = search.lower()
            items = [
                it
                for it in items
                if s in (it.get("alias") or "").lower() or s in (it.get("title") or "").lower()
            ]
        slim = [
            {
                "id": it.get("id"),
                "alias": it.get("alias"),
                "title": it.get("title") or it.get("name"),
                "type": it.get("type"),
                "unit": it.get("unit"),
                "free_amount": it.get("free_amount"),
            }
            for it in items
            if isinstance(it, dict)
        ]
        return dumps({"count": len(slim), "items": slim})
    except (PlatformAuthError, PlatformAPIError) as e:
        return error_json("API Error", e.message)


@mcp.tool()
async def acedatacloud_get_service(
    service: Annotated[str, Field(description="Service alias (e.g. 'suno') or UUID. Required.")],
) -> str:
    """Get full detail for one service: its APIs, pricing packages, and metadata. No token needed."""
    try:
        data = await client.get_public(f"/services/{service}")
        return dumps(data)
    except PlatformAuthError as e:
        return error_json("API Error", e.message)
    except PlatformAPIError as e:
        return error_json("API Error", e.message)


@mcp.tool()
async def acedatacloud_list_apis(
    service: Annotated[
        str | None, Field(description="Optional service alias/id to list only its APIs.")
    ] = None,
) -> str:
    """List public API endpoints (Beta/Production), optionally for one service. No token needed."""
    try:
        sid = await _resolve_service_id(service) if service else None
        data = await client.get_public("/apis/", {"service": service, "stage": PUBLIC_STAGES})
        apis = unwrap(data)
        apis = apis if isinstance(apis, list) else []
        slim = [
            {
                "name": a.get("name"),
                "title": a.get("title"),
                "method": a.get("method"),
                "path": a.get("path"),
                "stage": a.get("stage"),
                "service_id": a.get("service_id"),
            }
            for a in _filter_public(apis, service_id=sid)
        ]
        return dumps({"count": len(slim), "items": slim})
    except (PlatformAuthError, PlatformAPIError) as e:
        return error_json("API Error", e.message)


@mcp.tool()
async def acedatacloud_get_api_spec(
    api_path: Annotated[
        str | None, Field(description="API path, e.g. '/suno/audios' or '/serp/google'.")
    ] = None,
    service: Annotated[
        str | None, Field(description="Service alias to return all of its API specs.")
    ] = None,
) -> str:
    """Get the OpenAPI spec for an API. Provide api_path or service (never the full unfiltered spec)."""
    if not api_path and not service:
        return error_json(
            "Validation Error", "Provide an api_path (e.g. /suno/audios) or a service alias."
        )
    try:
        sid = await _resolve_service_id(service) if service else None
        data = await client.get_public(
            "/apis/", {"service": service, "path": api_path, "stage": PUBLIC_STAGES}
        )
        apis = _filter_public(
            unwrap(data) if isinstance(unwrap(data), list) else [], service_id=sid
        )
        if api_path:
            apis = [a for a in apis if api_path in (a.get("path"), a.get("path2"))]
        specs = [
            {
                "name": a.get("name"),
                "path": a.get("path"),
                "method": a.get("method"),
                "definition": a.get("definition"),
            }
            for a in apis
            if isinstance(a, dict) and a.get("definition")
        ]
        if not specs:
            return error_json(
                "Not Found",
                f"No public API spec for path={api_path or '-'} service={service or '-'}.",
            )
        return dumps(specs)
    except (PlatformAuthError, PlatformAPIError) as e:
        return error_json("API Error", e.message)


@mcp.tool()
async def acedatacloud_get_pricing(
    service: Annotated[
        str | None,
        Field(description="Optional service alias (e.g. 'suno'). Omit for all services."),
    ] = None,
) -> str:
    """Get display pricing (unit, free quota, cost rules) for a service or all services. No token needed."""
    try:
        items = []
        for s in await _list_services_raw():
            if not isinstance(s, dict):
                continue
            if service and s.get("alias") != service and str(s.get("id")) != service:
                continue
            items.append(
                {
                    "alias": s.get("alias"),
                    "title": s.get("title") or s.get("name"),
                    "unit": s.get("unit"),
                    "free_amount": s.get("free_amount"),
                    "cost": s.get("cost"),
                }
            )
        if service and not items:
            return error_json("Not Found", f"Service '{service}' not found.")
        return dumps(items)
    except (PlatformAuthError, PlatformAPIError) as e:
        return error_json("API Error", e.message)


@mcp.tool()
async def acedatacloud_list_datasets() -> str:
    """List downloadable datasets in the catalog. No token needed."""
    try:
        data = await client.get_public("/datasets/", {"private": "false", "limit": 100})
        return dumps({"items": unwrap(data)})
    except (PlatformAuthError, PlatformAPIError) as e:
        return error_json("API Error", e.message)


@mcp.tool()
async def acedatacloud_list_integrations() -> str:
    """List third-party integrations in the catalog. No token needed."""
    try:
        data = await client.get_public("/integrations/", {"private": "false", "limit": 100})
        return dumps({"items": unwrap(data)})
    except (PlatformAuthError, PlatformAPIError) as e:
        return error_json("API Error", e.message)
