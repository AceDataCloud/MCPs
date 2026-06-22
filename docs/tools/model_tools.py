"""Model catalog + pricing tools."""

import json

from core.client import client
from core.exceptions import DocsError
from core.server import mcp


def _dump(data: object) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2)


def _models_list(data: object) -> list:
    if isinstance(data, dict):
        for key in ("data", "results", "models"):
            if isinstance(data.get(key), list):
                return data[key]
    return data if isinstance(data, list) else []


@mcp.tool()
async def acedata_list_models(modality: str = "", with_pricing: bool = True) -> str:
    """List the LLM / image / video / music / embedding models AceData Cloud offers.

    Args:
        modality: Optional filter — chat, image, video, music, search, embedding.
        with_pricing: Include USD pricing computed from billing rules (default True).
    """
    try:
        data = await client.list_models(with_pricing=with_pricing)
        models = [m for m in _models_list(data) if isinstance(m, dict)]
        if modality:
            models = [m for m in models if modality in (m.get("type"), m.get("modality"))]
        slim = [
            {
                "id": m.get("id"),
                "type": m.get("type") or m.get("modality"),
                "owned_by": m.get("owned_by"),
                "pricing": m.get("pricing"),
            }
            for m in models
            if isinstance(m, dict)
        ]
        return _dump(slim)
    except DocsError as e:
        return f"Failed to list models: {e.message}"


@mcp.tool()
async def acedata_get_model(model_id: str) -> str:
    """Get full details (and pricing) for one model by id.

    Args:
        model_id: The model id, e.g. "gpt-5.1", "claude-opus-4-8", "doubao-seedream-5-0-260128".
    """
    try:
        data = await client.list_models(with_pricing=True)
        for m in _models_list(data):
            if isinstance(m, dict) and m.get("id") == model_id:
                return _dump(m)
        return f'Model "{model_id}" not found. Use acedata_list_models to see available ids.'
    except DocsError as e:
        return f"Failed to get model: {e.message}"


@mcp.tool()
async def acedata_get_pricing(service: str = "") -> str:
    """Get display pricing for a service (or all services).

    Args:
        service: Optional Service alias (e.g. "suno", "serp"). Omit to list all services' pricing.
    """
    try:
        services = await client.list_services()
        items = []
        for s in services:
            if not isinstance(s, dict):
                continue
            if service and s.get("alias") != service:
                continue
            items.append(
                {
                    "alias": s.get("alias"),
                    "name": s.get("name") or s.get("title"),
                    "unit": s.get("unit"),
                    "free_amount": s.get("free_amount"),
                    "cost": s.get("cost"),
                }
            )
        if service and not items:
            return f'Service "{service}" not found. Use acedata_list_services to see aliases.'
        return _dump(items)
    except DocsError as e:
        return f"Failed to get pricing: {e.message}"
