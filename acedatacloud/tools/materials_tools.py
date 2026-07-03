"""Marketing-material tools for the AceDataCloud platform management API.

Read-only access to the ``PublishMaterial`` catalog (``/publish-materials/``):
search by keyword / language / channel / category / tags, pick random items,
and fetch a single material's full content. Handy for pulling ready-to-post
marketing copy into an agent workflow.

The backend only filters ``title`` / ``lang`` / ``channel_id`` server-side, so
keyword (title+content), category, tags and random selection are applied
client-side over a generous fetch window.
"""

import random as _random
import uuid
from typing import Annotated, Any

from pydantic import Field

from core.client import client
from core.exceptions import PlatformAPIError, PlatformAuthError
from core.server import mcp
from core.utils import dumps, error_json

# Upper bound on how many rows we pull before client-side filtering. Materials
# are ordered newest-first server-side; if the catalog ever grows beyond this,
# client-side filters/random only see the newest MAX_FETCH rows (acceptable for
# a marketing helper).
MAX_FETCH = 300


def _is_uuid(value: str) -> bool:
    try:
        uuid.UUID(value)
        return True
    except (ValueError, AttributeError, TypeError):
        return False


async def _resolve_channel_ids(channel: str) -> list[str]:
    """Map a channel UUID or a name/title/domain substring to channel id(s)."""
    if _is_uuid(channel):
        return [channel]
    result = await client.get("/publish-channels/", {"limit": MAX_FETCH})
    items = result.get("items", []) if isinstance(result, dict) else []
    needle = channel.lower()
    return [
        c["id"]
        for c in items
        if c.get("id")
        and (
            needle in (c.get("name") or "").lower()
            or needle in (c.get("title") or "").lower()
            or needle in (c.get("domain") or "").lower()
        )
    ]


def _trim(material: dict[str, Any], include_content: bool) -> dict[str, Any]:
    md = material.get("metadata") or {}
    channels = material.get("channels") or []
    out: dict[str, Any] = {
        "id": material.get("id"),
        "title": material.get("title"),
        "lang": material.get("lang"),
        "category": material.get("category"),
        "tags": material.get("tags"),
        "quality_score": md.get("quality_score"),
        "channel_style": md.get("channel_style"),
        "channels": [c.get("name") or c.get("title") for c in channels if isinstance(c, dict)],
        "created_at": material.get("created_at"),
    }
    content = material.get("content") or ""
    if include_content:
        out["content"] = content
    else:
        out["content_preview"] = content[:200] + ("…" if len(content) > 200 else "")
    return out


def _match(
    material: dict[str, Any],
    keyword: str | None,
    category: str | None,
    tags: list[str] | None,
) -> bool:
    if keyword:
        kw = keyword.lower()
        title = (material.get("title") or "").lower()
        content = (material.get("content") or "").lower()
        if kw not in title and kw not in content:
            return False
    if category and category.lower() not in (material.get("category") or "").lower():
        return False
    if tags:
        want = {t.lower() for t in tags}
        have = {str(t).lower() for t in (material.get("tags") or [])}
        if not (want & have):
            return False
    return True


async def _query_materials(
    keyword: str | None,
    langs: list[str] | None,
    channel: str | None,
    channel_id: str | None,
    category: str | None,
    tags: list[str] | None,
    randomize: bool,
    include_content: bool,
    limit: int,
) -> dict[str, Any]:
    # Resolve channel filter (name/substring → ids). channel_id takes precedence.
    resolved_ids: list[str] | None = None
    if channel_id:
        resolved_ids = [channel_id]
    elif channel:
        resolved_ids = await _resolve_channel_ids(channel)
        if not resolved_ids:
            return {
                "count": 0,
                "returned": 0,
                "items": [],
                "note": f"No channel matched '{channel}'.",
            }

    server_params: dict[str, Any] = {"limit": MAX_FETCH}
    if langs:
        server_params["lang"] = langs
    if resolved_ids:
        server_params["channel_id"] = resolved_ids

    result = await client.get("/publish-materials/", server_params)
    items = result.get("items", []) if isinstance(result, dict) else []

    matched = [m for m in items if _match(m, keyword, category, tags)]
    total = len(matched)

    if randomize:
        _random.shuffle(matched)
    selected = matched[: max(1, limit)]

    return {
        "count": total,
        "returned": len(selected),
        "items": [_trim(m, include_content) for m in selected],
    }


@mcp.tool()
async def acedatacloud_list_publish_channels(
    search: Annotated[
        str | None,
        Field(
            description="Optional case-insensitive substring to match channel name/title/domain."
        ),
    ] = None,
    limit: Annotated[int, Field(description="Max channels to return.", ge=1, le=300)] = 100,
) -> str:
    """List publish channels (Zhihu, CSDN, Medium, X, ...).

    Use this to discover channel names/ids before filtering materials by channel.
    """
    try:
        result = await client.get("/publish-channels/", {"limit": limit})
        items = result.get("items", []) if isinstance(result, dict) else []
        if search:
            s = search.lower()
            items = [
                c
                for c in items
                if s in (c.get("name") or "").lower()
                or s in (c.get("title") or "").lower()
                or s in (c.get("domain") or "").lower()
            ]
        trimmed = [
            {
                "id": c.get("id"),
                "name": c.get("name"),
                "title": c.get("title"),
                "domain": c.get("domain"),
            }
            for c in items
        ]
        return dumps({"count": len(trimmed), "items": trimmed})
    except PlatformAuthError as e:
        return error_json("Authentication Error", e.message)
    except PlatformAPIError as e:
        return error_json("API Error", e.message)


@mcp.tool()
async def acedatacloud_search_materials(
    keyword: Annotated[
        str | None,
        Field(
            description="Case-insensitive substring matched against the material title AND content."
        ),
    ] = None,
    langs: Annotated[
        list[str] | None,
        Field(description="Filter by one or more language codes, e.g. ['zh-cn', 'en']."),
    ] = None,
    channel: Annotated[
        str | None,
        Field(description="Channel UUID, or a name/title/domain substring (e.g. 'zhihu', 'CSDN')."),
    ] = None,
    channel_id: Annotated[
        str | None, Field(description="Explicit channel UUID (takes precedence over `channel`).")
    ] = None,
    category: Annotated[
        str | None,
        Field(description="Case-insensitive substring matched against the material category."),
    ] = None,
    tags: Annotated[
        list[str] | None, Field(description="Keep materials whose tags overlap any of these.")
    ] = None,
    randomize: Annotated[
        bool, Field(description="Shuffle matches before returning (for random picks).")
    ] = False,
    include_content: Annotated[
        bool, Field(description="Return full content instead of a short preview.")
    ] = False,
    limit: Annotated[int, Field(description="Max materials to return.", ge=1, le=100)] = 20,
) -> str:
    """Search marketing materials (ready-to-post copy) in the PublishMaterial catalog.

    Combines server-side filters (language, channel) with client-side keyword
    (title+content), category and tag matching, plus optional random selection.
    Returns ``{count, returned, items}``; each item carries its quality_score,
    channel_style and either a content preview or full content.
    """
    try:
        data = await _query_materials(
            keyword, langs, channel, channel_id, category, tags, randomize, include_content, limit
        )
        return dumps(data)
    except PlatformAuthError as e:
        return error_json("Authentication Error", e.message)
    except PlatformAPIError as e:
        return error_json("API Error", e.message)


@mcp.tool()
async def acedatacloud_pick_random_materials(
    count: Annotated[
        int, Field(description="How many random materials to return.", ge=1, le=20)
    ] = 1,
    langs: Annotated[
        list[str] | None, Field(description="Optional language filter, e.g. ['zh-cn'].")
    ] = None,
    channel: Annotated[
        str | None, Field(description="Optional channel UUID or name/title/domain substring.")
    ] = None,
    category: Annotated[
        str | None, Field(description="Optional category substring filter.")
    ] = None,
) -> str:
    """Pick random ready-to-post materials (full content included).

    Convenience wrapper over search with ``randomize=True`` and full content —
    e.g. "grab a random Zhihu post to publish".
    """
    try:
        data = await _query_materials(
            keyword=None,
            langs=langs,
            channel=channel,
            channel_id=None,
            category=category,
            tags=None,
            randomize=True,
            include_content=True,
            limit=count,
        )
        return dumps(data)
    except PlatformAuthError as e:
        return error_json("Authentication Error", e.message)
    except PlatformAPIError as e:
        return error_json("API Error", e.message)


@mcp.tool()
async def acedatacloud_get_material(
    material_id: Annotated[str, Field(description="The material UUID.")],
) -> str:
    """Fetch one material's full detail (title, content, lang, tags, channels)."""
    try:
        result = await client.get(f"/publish-materials/{material_id}/")
        if result is None:
            return error_json("Not Found", f"No material with id {material_id}.")
        return dumps(result)
    except PlatformAuthError as e:
        return error_json("Authentication Error", e.message)
    except PlatformAPIError as e:
        return error_json("API Error", e.message)
