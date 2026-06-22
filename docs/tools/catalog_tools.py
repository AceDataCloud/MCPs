"""Service / API catalog + OpenAPI spec tools."""

import json

from core.client import client
from core.exceptions import DocsError
from core.server import mcp

PUBLIC_STAGES = ["Beta", "Production"]


def _dump(data: object) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2)


async def _resolve_service_id(service: str) -> str | None:
    """Map a Service alias (or id) to its id, client-side, so service filtering
    is correct even if the backend ignores the `service` query param.

    Returns ``None`` if the service can't be resolved (e.g. beyond the fetched
    page) — the caller then trusts the backend `service` filter rather than
    over-filtering every result to empty.
    """
    if not service:
        return None
    services = await client.list_services()
    for s in services:
        if isinstance(s, dict) and (s.get("alias") == service or str(s.get("id")) == service):
            return str(s.get("id"))
    return None


def _filter_public(apis: list, service_id: str | None = None) -> list:
    """Always enforce public stages (and service identity) locally — never rely
    on the backend having applied the filters."""
    out = []
    for a in apis:
        if not isinstance(a, dict):
            continue
        if a.get("stage") not in PUBLIC_STAGES:
            continue
        if service_id is not None and str(a.get("service_id")) != str(service_id):
            continue
        out.append(a)
    return out


@mcp.tool()
async def acedata_list_services(service_type: str = "") -> str:
    """List AceData Cloud services (logical API groupings).

    Args:
        service_type: Optional filter — Api, Proxy, Integration, Dataset, Agent, Introduction.
    """
    try:
        services = await client.list_services(service_type=service_type or None)
        items = [
            {
                "alias": s.get("alias"),
                "name": s.get("name") or s.get("title"),
                "type": s.get("type"),
                "unit": s.get("unit"),
            }
            for s in services
            if isinstance(s, dict)
        ]
        return _dump(items)
    except DocsError as e:
        return f"Failed to list services: {e.message}"


@mcp.tool()
async def acedata_list_apis(service: str = "") -> str:
    """List public API endpoints (Beta/Production), optionally for one service.

    Args:
        service: Optional Service alias or id to filter to one service's APIs.
    """
    try:
        sid = await _resolve_service_id(service) if service else None
        apis = await client.list_apis(service=service or None, stages=PUBLIC_STAGES)
        items = [
            {
                "name": a.get("name"),
                "title": a.get("title"),
                "method": a.get("method"),
                "path": a.get("path"),
                "stage": a.get("stage"),
            }
            for a in _filter_public(apis, service_id=sid)
        ]
        return _dump(items)
    except DocsError as e:
        return f"Failed to list apis: {e.message}"


@mcp.tool()
async def acedata_get_spec(api_path: str = "", service: str = "") -> str:
    """Get the OpenAPI specification for an API.

    You MUST provide `api_path` or `service` — the full spec is never returned
    unfiltered (it would be huge).

    Args:
        api_path: An API path, e.g. "/suno/audios" or "/serp/google".
        service: A Service alias to return all of that service's API specs.
    """
    if not api_path and not service:
        return "Provide an `api_path` (e.g. /suno/audios) or a `service` alias to filter the spec."
    try:
        sid = await _resolve_service_id(service) if service else None
        apis = await client.list_apis(
            service=service or None, path=api_path or None, stages=PUBLIC_STAGES
        )
        # Verify path / stage / service client-side so we never return the wrong
        # (or non-public, or cross-service) spec if a backend filter isn't applied.
        apis = _filter_public(apis, service_id=sid)
        if api_path:
            apis = [a for a in apis if api_path in (a.get("path"), a.get("path2"))]
        if not apis:
            return f"No public API found for path={api_path or '-'} service={service or '-'}."
        specs = []
        for a in apis:
            if isinstance(a, dict) and a.get("definition"):
                specs.append(
                    {
                        "name": a.get("name"),
                        "path": a.get("path"),
                        "method": a.get("method"),
                        "definition": a.get("definition"),
                    }
                )
        if not specs:
            return "Matched API(s) have no OpenAPI definition published."
        return _dump(specs)
    except DocsError as e:
        return f"Failed to get spec: {e.message}"
