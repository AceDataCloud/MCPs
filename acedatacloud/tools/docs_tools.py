"""Public documentation tools: full-text search, browse, and fetch by id.

Discovery is via ``/search/?query=`` (rich results with alias/title/snippet/url).
A single document's content is fetched via ``documents/?id=`` because the
``documents/{id}/`` detail route is not reliable.
"""

import re
from typing import Annotated

from pydantic import Field

from core.client import client
from core.exceptions import PlatformAPIError, PlatformAuthError
from core.server import mcp
from core.utils import dumps, error_json

_UUID = re.compile(r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$")


@mcp.tool()
async def acedatacloud_search_docs(
    query: Annotated[
        str,
        Field(description="Search text, e.g. 'suno lyrics' or 'midjourney imagine'."),
    ],
    lang: Annotated[
        str | None,
        Field(description="Optional language code, e.g. 'en', 'zh-cn', 'ja'."),
    ] = None,
    limit: Annotated[
        int, Field(description="Max results to return (server caps at 30).", ge=1, le=30)
    ] = 10,
) -> str:
    """Full-text search the AceDataCloud documentation. Returns matching docs with
    alias, title, snippet and url. No token required.

    This is content-relevance search over *public* docs only; it does not accept
    structural filters. To filter by tag / type / privacy, use
    ``acedatacloud_list_docs`` (e.g. ``tag='application'``, ``private=False``).
    """
    try:
        result = await client.get_public("/search/", {"query": query, "lang": lang, "limit": limit})
        if not isinstance(result, dict):
            return error_json("No Response", "The API returned an empty response.")
        return dumps(result)
    except PlatformAuthError as e:
        return error_json("Authentication Error", e.message)
    except PlatformAPIError as e:
        return error_json("API Error", e.message)


@mcp.tool()
async def acedatacloud_list_docs(
    doc_type: Annotated[
        str | None,
        Field(description="Optional document type filter, e.g. 'Text'."),
    ] = None,
    tag: Annotated[
        str | None,
        Field(
            description="Optional tag filter, e.g. 'application'. Matches docs carrying this tag."
        ),
    ] = None,
    private: Annotated[
        bool | None,
        Field(
            description="Filter by privacy: False = public only, True = private only, unset = all."
        ),
    ] = None,
    offset: Annotated[int, Field(description="Pagination offset.", ge=0)] = 0,
    limit: Annotated[int, Field(description="Max documents to return.", ge=1, le=100)] = 30,
) -> str:
    """Browse documentation pages (newest/ranked), optionally filtered by ``doc_type``,
    ``tag`` and ``private``. For content-relevance search prefer
    ``acedatacloud_search_docs``. No token required.
    """
    try:
        result = await client.get_public(
            "/documents/",
            {
                "limit": limit,
                "offset": offset,
                "type": doc_type,
                "tag": tag,
                "private": None if private is None else str(private).lower(),
            },
        )
        if not isinstance(result, dict):
            return error_json("No Response", "The API returned an empty response.")
        # Trim long content in the browse view; use get_doc for full content.
        items = []
        for it in result.get("items", []):
            slim = {k: v for k, v in it.items() if k != "content"}
            content = it.get("content")
            if isinstance(content, str):
                slim["content_preview"] = content[:200]
            items.append(slim)
        return dumps({"count": result.get("count"), "items": items})
    except PlatformAuthError as e:
        return error_json("Authentication Error", e.message)
    except PlatformAPIError as e:
        return error_json("API Error", e.message)


@mcp.tool()
async def acedatacloud_get_doc(
    doc_id: Annotated[
        str,
        Field(description="Document UUID (from search results or list)."),
    ],
) -> str:
    """Fetch one documentation page's full content by its UUID. No token required."""
    try:
        ref = doc_id.strip()
        if not _UUID.match(ref):
            return error_json("Invalid Input", "doc_id must be a document UUID.")
        result = await client.get_public("/documents/", {"id": ref})
        items = result.get("items", []) if isinstance(result, dict) else []
        if not items:
            return error_json("Not Found", f"No document with id '{ref}'.")
        return dumps(items[0])
    except PlatformAuthError as e:
        return error_json("Authentication Error", e.message)
    except PlatformAPIError as e:
        return error_json("API Error", e.message)
