"""Public model-catalog tools: rich catalog listing + per-model lookup.

``acedatacloud_list_models`` (in read_tools) returns the OpenAI-style flat list.
These add the richer ``/models/catalog/`` view with provider, modality and
per-model credit pricing.
"""

from typing import Annotated, Any

from pydantic import Field

from core.client import client
from core.exceptions import PlatformAPIError, PlatformAuthError
from core.server import mcp
from core.utils import dumps, error_json


async def _catalog() -> dict[str, Any]:
    result = await client.get_public("/models/catalog/")
    return result if isinstance(result, dict) else {}


@mcp.tool()
async def acedatacloud_list_model_catalog(
    modality: Annotated[
        str | None,
        Field(description="Filter by modality: chat/video/image/music/search/embedding."),
    ] = None,
    provider: Annotated[
        str | None,
        Field(description="Filter by provider substring, e.g. 'OpenAI', 'Anthropic'."),
    ] = None,
) -> str:
    """List the model catalog with provider, modality and per-model credit pricing.

    Returns the modality counts plus matching models. No token required.
    """
    try:
        cat = await _catalog()
        items = cat.get("items", [])
        if modality:
            m = modality.lower()
            items = [it for it in items if (it.get("modality") or "").lower() == m]
        if provider:
            p = provider.lower()
            items = [it for it in items if p in (it.get("provider") or "").lower()]
        return dumps(
            {
                "modalities": cat.get("modalities"),
                "count": len(items),
                "items": items,
            }
        )
    except PlatformAuthError as e:
        return error_json("Authentication Error", e.message)
    except PlatformAPIError as e:
        return error_json("API Error", e.message)


@mcp.tool()
async def acedatacloud_get_model(
    model: Annotated[
        str,
        Field(description="Model id or name, e.g. 'gpt-4.1', 'claude', 'veo'."),
    ],
) -> str:
    """Look up models by id/name (case-insensitive substring) with their credit
    pricing and capabilities. No token required.
    """
    try:
        cat = await _catalog()
        q = model.strip().lower()
        matches = [
            it
            for it in cat.get("items", [])
            if q in (it.get("id") or "").lower() or q in (it.get("name") or "").lower()
        ]
        if not matches:
            return error_json("Not Found", f"No model matched '{model}'.")
        return dumps({"count": len(matches), "items": matches})
    except PlatformAuthError as e:
        return error_json("Authentication Error", e.message)
    except PlatformAPIError as e:
        return error_json("API Error", e.message)
