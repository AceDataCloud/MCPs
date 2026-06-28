"""Public catalog tools: services, pricing, APIs, specs, datasets, integrations.

These hit the public catalog endpoints (no token required). The platform's
detail endpoints (``/services/{id}/``, ``/apis/{id}/``) are unreliable, so every
lookup here uses the list endpoints with the filters that actually work:
``services/?id=``, ``apis/?path=`` and ``apis/?service_id=``.
"""

import re
from typing import Annotated, Any

from pydantic import Field

from core.client import client
from core.exceptions import PlatformAPIError, PlatformAuthError
from core.server import mcp
from core.utils import dumps, error_json

_UUID = re.compile(r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$")


async def _resolve_service(ref: str) -> dict[str, Any] | None:
    """Resolve a service by UUID (``services/?id=``) or by alias (paginated match)."""
    ref = ref.strip()
    if _UUID.match(ref):
        result = await client.get_public("/services/", {"id": ref})
        items: list[dict[str, Any]] = result.get("items", []) if isinstance(result, dict) else []
        return items[0] if items else None
    target = ref.lower()
    offset = 0
    while offset < 600:
        result = await client.get_public("/services/", {"limit": 50, "offset": offset})
        page: list[dict[str, Any]] = result.get("items", []) if isinstance(result, dict) else []
        if not page:
            break
        for it in page:
            if (it.get("alias") or "").lower() == target:
                return it
        count = result.get("count", 0) if isinstance(result, dict) else 0
        offset += 50
        if offset >= count:
            break
    return None


@mcp.tool()
async def acedatacloud_get_service(
    service: Annotated[
        str,
        Field(description="Service UUID or alias (e.g. 'suno', 'midjourney')."),
    ],
) -> str:
    """Get one service's full detail: title, description, type, unit, free_amount
    and its display pricing (``cost``). No token required.
    """
    try:
        svc = await _resolve_service(service)
        if not svc:
            return error_json("Not Found", f"No service matched '{service}'.")
        return dumps(svc)
    except PlatformAuthError as e:
        return error_json("Authentication Error", e.message)
    except PlatformAPIError as e:
        return error_json("API Error", e.message)


@mcp.tool()
async def acedatacloud_get_pricing(
    service: Annotated[
        str,
        Field(description="Service UUID or alias to price (e.g. 'suno')."),
    ],
) -> str:
    """Get a service's pricing: the billing ``unit`` (Count/Token/MB/GB/Credit),
    ``free_amount`` and the display ``cost`` rules. No token required.
    """
    try:
        svc = await _resolve_service(service)
        if not svc:
            return error_json("Not Found", f"No service matched '{service}'.")
        return dumps(
            {
                "service_id": svc.get("id"),
                "alias": svc.get("alias"),
                "title": svc.get("title"),
                "type": svc.get("type"),
                "unit": svc.get("unit"),
                "free_amount": svc.get("free_amount"),
                "cost": svc.get("cost"),
            }
        )
    except PlatformAuthError as e:
        return error_json("Authentication Error", e.message)
    except PlatformAPIError as e:
        return error_json("API Error", e.message)


@mcp.tool()
async def acedatacloud_list_apis(
    service: Annotated[
        str | None,
        Field(description="Optional service UUID or alias to filter the APIs by."),
    ] = None,
    limit: Annotated[int, Field(description="Max APIs to return.", ge=1, le=100)] = 50,
) -> str:
    """List API endpoints, optionally scoped to one service. Each item carries the
    path, method, stage and billing ``cost``. No token required.
    """
    try:
        if service:
            svc = await _resolve_service(service)
            if not svc:
                return error_json("Not Found", f"No service matched '{service}'.")
            sid = svc.get("id")
            # The /apis/?service_id= filter is not honored server-side, so collect
            # and filter client-side by paging through the catalog.
            collected: list[dict[str, Any]] = []
            offset = 0
            while offset < 2000 and len(collected) < limit:
                result = await client.get_public("/apis/", {"limit": 50, "offset": offset})
                page: list[dict[str, Any]] = (
                    result.get("items", []) if isinstance(result, dict) else []
                )
                if not page:
                    break
                for it in page:
                    if it.get("service_id") == sid:
                        collected.append({k: v for k, v in it.items() if k != "definition"})
                        if len(collected) >= limit:
                            break
                count = result.get("count", 0) if isinstance(result, dict) else 0
                offset += 50
                if offset >= count:
                    break
            return dumps({"count": len(collected), "items": collected})
        result = await client.get_public("/apis/", {"limit": limit})
        if not isinstance(result, dict):
            return error_json("No Response", "The API returned an empty response.")
        # Trim the OpenAPI blob from list view to keep output compact.
        items = [
            {k: v for k, v in it.items() if k != "definition"} for it in result.get("items", [])
        ]
        return dumps({"count": result.get("count"), "items": items})
    except PlatformAuthError as e:
        return error_json("Authentication Error", e.message)
    except PlatformAPIError as e:
        return error_json("API Error", e.message)


@mcp.tool()
async def acedatacloud_get_api_spec(
    path: Annotated[
        str,
        Field(description="API path, e.g. '/suno/audios' or '/midjourney/imagine'."),
    ],
) -> str:
    """Get one API endpoint's OpenAPI spec (``definition``) plus its method, stage
    and billing ``cost``, looked up by path. No token required.
    """
    try:
        result = await client.get_public("/apis/", {"path": path})
        items = result.get("items", []) if isinstance(result, dict) else []
        if not items:
            return error_json("Not Found", f"No API matched path '{path}'.")
        api = items[0]
        return dumps(
            {
                "id": api.get("id"),
                "service_id": api.get("service_id"),
                "title": api.get("title"),
                "path": api.get("path"),
                "method": api.get("method"),
                "stage": api.get("stage"),
                "cost": api.get("cost"),
                "definition": api.get("definition"),
            }
        )
    except PlatformAuthError as e:
        return error_json("Authentication Error", e.message)
    except PlatformAPIError as e:
        return error_json("API Error", e.message)


@mcp.tool()
async def acedatacloud_list_datasets(
    limit: Annotated[int, Field(description="Max datasets to return.", ge=1, le=100)] = 50,
) -> str:
    """List downloadable datasets (title, price, download/preview URLs). No token required."""
    try:
        result = await client.get_public("/datasets/", {"limit": limit})
        if not isinstance(result, dict):
            return error_json("No Response", "The API returned an empty response.")
        return dumps(result)
    except PlatformAuthError as e:
        return error_json("Authentication Error", e.message)
    except PlatformAPIError as e:
        return error_json("API Error", e.message)


@mcp.tool()
async def acedatacloud_list_integrations(
    limit: Annotated[int, Field(description="Max integrations to return.", ge=1, le=100)] = 50,
) -> str:
    """List third-party integrations (title, options, stage). No token required."""
    try:
        result = await client.get_public("/integrations/", {"limit": limit})
        if not isinstance(result, dict):
            return error_json("No Response", "The API returned an empty response.")
        return dumps(result)
    except PlatformAuthError as e:
        return error_json("Authentication Error", e.message)
    except PlatformAPIError as e:
        return error_json("API Error", e.message)
