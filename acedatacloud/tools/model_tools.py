"""Public model catalog tools: list models (all modalities) + per-model detail/pricing.

Read public, read-only endpoints — no token required.
"""

from typing import Annotated

from pydantic import Field

from core.client import client
from core.exceptions import PlatformAPIError, PlatformAuthError
from core.server import mcp
from core.utils import dumps, error_json


def _catalog_items(data: object) -> list:
    if isinstance(data, dict) and isinstance(data.get("items"), list):
        return [m for m in data["items"] if isinstance(m, dict)]
    return []


def _models_list(data: object) -> list:
    if isinstance(data, dict):
        for key in ("data", "results", "models"):
            value = data.get(key)
            if isinstance(value, list):
                return value
    return data if isinstance(data, list) else []


@mcp.tool()
async def acedatacloud_list_models(
    modality: Annotated[
        str | None,
        Field(description="Optional filter: chat, image, video, music, search, embedding."),
    ] = None,
    with_pricing: Annotated[bool, Field(description="Include pricing per model.")] = True,
) -> str:
    """List the models AceDataCloud offers (all modalities) with credit pricing. No token needed."""
    try:
        data = await client.get_public("/models/catalog/")
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
        return dumps({"count": len(slim), "rates": rates, "models": slim})
    except (PlatformAuthError, PlatformAPIError) as e:
        return error_json("API Error", e.message)


@mcp.tool()
async def acedatacloud_get_model(
    model_id: Annotated[
        str, Field(description="Model id, e.g. 'gpt-5.1', 'claude-opus-4-8'. Required.")
    ],
) -> str:
    """Get full details and pricing for one model by id. No token needed."""
    try:
        data = await client.get_public("/models/catalog/")
        item = next((m for m in _catalog_items(data) if m.get("id") == model_id), None)
        if item is not None:
            out = dict(item)
            out["rates"] = data.get("rates") if isinstance(data, dict) else None
            return dumps(out)
        chat = await client.get_public("/models/", {"with_pricing": "1"})
        for m in _models_list(chat):
            if isinstance(m, dict) and m.get("id") == model_id:
                return dumps(m)
        return error_json(
            "Not Found", f"Model '{model_id}' not found. Use acedatacloud_list_models."
        )
    except (PlatformAuthError, PlatformAPIError) as e:
        return error_json("API Error", e.message)
