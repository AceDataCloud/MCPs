"""Public catalog tools: services, pricing, APIs, specs, datasets, integrations.

These hit the public catalog endpoints (no token required). The platform's
detail endpoints (``/services/{id}/``, ``/apis/{id}/``) are unreliable, so every
lookup here uses the list endpoints with the filters that actually work:
``services/?id=``, ``apis/?path=`` and ``apis/?service_id=``.
"""

import re
from decimal import Decimal, InvalidOperation
from typing import Annotated, Any

from pydantic import Field

from core.client import client
from core.exceptions import PlatformError, PlatformValidationError
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
    target = ref.casefold()
    offset = 0
    title_match = None
    tag_matches: list[dict[str, Any]] = []
    while offset < 600:
        result = await client.get_public("/services/", {"limit": 50, "offset": offset})
        page: list[dict[str, Any]] = result.get("items", []) if isinstance(result, dict) else []
        if not page:
            break
        for it in page:
            if (it.get("alias") or "").casefold() == target:
                return it
            if title_match is None and (it.get("title") or "").casefold() == target:
                title_match = it
            if any(str(tag).casefold() == target for tag in (it.get("tags") or [])):
                tag_matches.append(it)
        count = result.get("count", 0) if isinstance(result, dict) else 0
        offset += 50
        if offset >= count:
            break
    if title_match:
        return title_match
    if len(tag_matches) == 1:
        return tag_matches[0]
    if len(tag_matches) > 1:
        raise PlatformValidationError(
            f"Service reference '{ref}' matches multiple tags; use a service UUID or exact alias."
        )
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
    except PlatformError as error:
        return error_json(error.code, error.message)


@mcp.tool()
async def acedatacloud_get_pricing(
    service: Annotated[
        str,
        Field(description="Service UUID or alias to price (e.g. 'suno')."),
    ],
) -> str:
    """Get billing unit, free amount and display cost rules. Public contact-only
    datasets also return pricing_mode and any reference_quote, not checkout prices.
    No token required.
    """
    try:
        svc = await _resolve_service(service)
        if not svc:
            return error_json("Not Found", f"No service matched '{service}'.")
        pricing = {
            "service_id": svc.get("id"),
            "alias": svc.get("alias"),
            "title": svc.get("title"),
            "type": svc.get("type"),
            "unit": svc.get("unit"),
            "free_amount": svc.get("free_amount"),
            "cost": svc.get("cost"),
        }
        metadata = svc.get("metadata") or {}
        if (
            svc.get("type") == "Dataset"
            and svc.get("private") is False
            and metadata.get("pricing_mode") == "contact_only"
        ):
            pricing["pricing_mode"] = metadata["pricing_mode"]
            quote = metadata.get("reference_quote")
            if quote is not None:
                pricing["reference_quote"] = {
                    key: quote[key]
                    for key in ("currency", "min_amount", "max_amount", "unit", "status")
                    if key in quote
                }
        return dumps(pricing)
    except PlatformError as error:
        return error_json(error.code, error.message)


@mcp.tool()
async def acedatacloud_get_public_usage_packages(
    service: Annotated[
        str,
        Field(description="Service UUID or exact alias whose public Usage packages are needed."),
    ],
) -> str:
    """Get one service's public Usage packages for Credit-to-USD pricing.

    The pricing reader returns Credit cost rules, but not the package
    amount/price pairs. Package ladders can differ between services, so the
    generic model catalog's ladder must not be substituted for this service.
    Fail closed if the public service detail cannot be read.
    """
    try:
        svc = await _resolve_service(service)
        if not svc:
            return error_json("Not Found", f"No service matched '{service}'.")
        detail = await client.get_public(f"/services/{svc['id']}/")
        rates = detail.get("packages") if isinstance(detail, dict) else None
        if not isinstance(rates, list):
            return error_json(
                "Unavailable", "This service's public Usage packages are unavailable."
            )
        packages = []
        for rate in rates:
            if (
                not isinstance(rate, dict)
                or rate.get("private") is True
                or rate.get("type") != "Usage"
            ):
                continue
            try:
                amount = Decimal(str(rate["amount"]))
                price = Decimal(str(rate["price"]))
            except (KeyError, InvalidOperation, TypeError, ValueError):
                continue
            if not amount.is_finite() or not price.is_finite() or amount <= 0 or price <= 0:
                continue
            packages.append({"amount": str(amount), "price": str(price)})
        if not packages:
            return error_json(
                "Unavailable", "No positive public Usage packages were returned for this service."
            )
        return dumps(
            {"source": "public_service_detail", "service_id": svc["id"], "packages": packages}
        )
    except PlatformError as error:
        return error_json(error.code, error.message)


@mcp.tool()
async def acedatacloud_list_apis(
    service: Annotated[
        str | None,
        Field(description="Optional service UUID or alias to filter the APIs by."),
    ] = None,
    stage: Annotated[
        str | None,
        Field(description="Optional publication stage filter: Alpha/Beta/Production."),
    ] = None,
    limit: Annotated[int, Field(description="Max APIs to return.", ge=1, le=100)] = 50,
) -> str:
    """List API endpoints, optionally scoped to one ``service`` and/or ``stage``.
    Each item carries the path, method, stage and billing ``cost``. No token required.
    """
    try:
        service_id = service
        if service:
            resolved = await _resolve_service(service)
            if not resolved:
                return error_json("Not Found", f"No service matched '{service}'.")
            service_id = resolved.get("id")
        result = await client.get_public(
            "/apis/", {"limit": limit, "service": service_id, "stage": stage}
        )
        if not isinstance(result, dict):
            return error_json("No Response", "The API returned an empty response.")
        # Trim the OpenAPI blob from list view to keep output compact.
        items = [
            {k: v for k, v in it.items() if k != "definition"} for it in result.get("items", [])
        ]
        return dumps({"count": result.get("count"), "items": items})
    except PlatformError as error:
        return error_json(error.code, error.message)


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
    except PlatformError as error:
        return error_json(error.code, error.message)


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
    except PlatformError as error:
        return error_json(error.code, error.message)


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
    except PlatformError as error:
        return error_json(error.code, error.message)
