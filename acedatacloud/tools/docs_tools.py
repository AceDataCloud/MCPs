"""Public documentation tools: search, browse, and read AceDataCloud docs.

All read public, read-only endpoints — no token required.
"""

import re
from typing import Annotated
from urllib.parse import unquote, urlparse

from pydantic import Field

from core.client import client
from core.exceptions import PlatformAPIError, PlatformAuthError
from core.server import mcp
from core.utils import dumps, error_json, unwrap

# Aliases are kebab-case, UUIDs are hex+hyphen — no dots/slashes/query chars.
# Disallowing "." also blocks "../" path traversal.
_REF_RE = re.compile(r"^[A-Za-z0-9_-]+$")
_DOC_URL = "https://platform.acedata.cloud/documents/{}"


def _doc_ref(ref: str) -> str:
    """Normalize a doc reference to a safe alias/uuid, or '' if invalid.

    A full URL is reduced locally to its last path segment — we never fetch an
    arbitrary URL, only ever /api/v1/documents/<ref>, constrained to
    [A-Za-z0-9_-]+ so it can't traverse to another endpoint or carry query chars.
    """
    ref = (ref or "").strip()
    if "://" in ref:
        ref = unquote(urlparse(ref).path).rstrip("/").rsplit("/", 1)[-1]
    return ref if _REF_RE.match(ref) else ""


@mcp.tool()
async def acedatacloud_search_docs(
    query: Annotated[str, Field(description="Keywords or a question, e.g. 'suno music api'.")],
    lang: Annotated[str, Field(description="Language code (default zh-cn).")] = "zh-cn",
    limit: Annotated[int, Field(description="Max results.", ge=1, le=30)] = 10,
) -> str:
    """Search the AceDataCloud documentation. Use first when you don't know the exact page. No token needed."""
    try:
        data = await client.get_public(
            "/search/", {"q": query, "lang": lang, "limit": max(1, min(limit, 30))}
        )
        results = data.get("results", data) if isinstance(data, dict) else data
        if not results:
            return error_json(
                "Not Found", f"No docs for '{query}'. Try acedatacloud_list_docs to browse."
            )
        return dumps(results)
    except PlatformAuthError as e:
        return error_json("API Error", e.message)
    except PlatformAPIError as e:
        if e.status_code == 404:
            return error_json(
                "Unavailable", "Doc search index unavailable; use acedatacloud_list_docs."
            )
        return error_json("API Error", e.message)


@mcp.tool()
async def acedatacloud_list_docs(
    limit: Annotated[int, Field(description="Pages to return.", ge=1, le=50)] = 20,
    offset: Annotated[int, Field(description="Pagination offset.", ge=0)] = 0,
    doc_type: Annotated[
        str | None, Field(description="Optional filter: Api, Proxy, Integration, Dataset, Text.")
    ] = None,
) -> str:
    """List documentation pages (paginated). No token needed."""
    try:
        data = await client.get_public(
            "/documents/", {"private": "false", "limit": limit, "offset": offset, "type": doc_type}
        )
        docs = unwrap(data)
        docs = docs if isinstance(docs, list) else []
        items = [
            {
                "alias": d.get("alias"),
                "title": d.get("title") or d.get("name"),
                "type": d.get("type"),
                "url": _DOC_URL.format(d.get("alias")),
            }
            for d in docs
            if isinstance(d, dict) and d.get("alias")
        ]
        return dumps({"count": len(items), "items": items})
    except (PlatformAuthError, PlatformAPIError) as e:
        return error_json("API Error", e.message)


@mcp.tool()
async def acedatacloud_get_doc(
    ref: Annotated[
        str, Field(description="Document alias, UUID, or a documents/<alias> URL. Required.")
    ],
    lang: Annotated[
        str, Field(description="Language code for the content (default zh-cn).")
    ] = "zh-cn",
) -> str:
    """Fetch the full content of a documentation page. No token needed."""
    safe_ref = _doc_ref(ref)
    if not safe_ref:
        return error_json("Validation Error", f"Invalid document reference '{ref}'.")
    try:
        doc = await client.get_public(f"/documents/{safe_ref}", lang=lang)
        if not isinstance(doc, dict):
            return error_json(
                "API Error", f"Document '{safe_ref}' returned an unexpected response."
            )
        return dumps(
            {
                "alias": doc.get("alias"),
                "title": doc.get("title") or doc.get("name"),
                "type": doc.get("type"),
                "content": doc.get("content"),
                "url": _DOC_URL.format(doc.get("alias")),
            }
        )
    except PlatformAuthError as e:
        return error_json("API Error", e.message)
    except PlatformAPIError as e:
        if e.status_code == 404:
            return error_json(
                "Not Found", f"Document '{ref}' not found. Try acedatacloud_search_docs."
            )
        return error_json("API Error", e.message)
