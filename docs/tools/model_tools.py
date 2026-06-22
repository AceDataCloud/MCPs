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


def _catalog_items(data: object) -> list:
    if isinstance(data, dict) and isinstance(data.get("items"), list):
        return [m for m in data["items"] if isinstance(m, dict)]
    return []


@mcp.tool()
async def acedata_list_models(modality: str = "", with_pricing: bool = True) -> str:
    """List the LLM / image / video / music / search / embedding models AceData Cloud offers.

    Sourced from the full catalog (all modalities), with credit pricing and the
    credit→USD conversion rate.

    Args:
        modality: Optional filter — chat, image, video, music, search, embedding.
        with_pricing: Include pricing on each model (default True).
    """
    try:
        data = await client.get_catalog()
        models = _catalog_items(data)
        if modality:
            models = [m for m in models if m.get("modality") == modality]
        slim = []
        for m in models:
            entry = {
                "id": m.get("id"),
                "name": m.get("name"),
                "modality": m.get("modality"),
                "provider": m.get("provider"),
                "unit": m.get("unit"),
            }
            if with_pricing:
                entry["pricing"] = m.get("pricing")
            slim.append(entry)
        rates = data.get("rates") if isinstance(data, dict) else None
        return _dump({"count": len(slim), "rates": rates, "models": slim})
    except DocsError as e:
        return f"Failed to list models: {e.message}"


@mcp.tool()
async def acedata_get_model(model_id: str) -> str:
    """Get full details (and pricing) for one model by id.

    Args:
        model_id: The model id, e.g. "gpt-5.1", "claude-opus-4-8", "doubao-seedream-5-0-260128".
    """
    try:
        # Catalog covers all modalities; the chat /models/ endpoint adds USD detail.
        data = await client.get_catalog()
        item = next((m for m in _catalog_items(data) if m.get("id") == model_id), None)
        if item is not None:
            out = dict(item)
            out["rates"] = data.get("rates") if isinstance(data, dict) else None
            return _dump(out)
        chat = await client.list_models(with_pricing=True)
        for m in _models_list(chat):
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
