"""Documentation search / browse / read tools."""

import json
import re
from urllib.parse import unquote, urlparse

from core.client import client
from core.exceptions import DocsError, DocsNotFoundError
from core.server import mcp

# Aliases are kebab-case, UUIDs are hex+hyphen — no dots, slashes, or query chars.
# Disallowing "." also kills "../" path traversal.
_REF_RE = re.compile(r"^[A-Za-z0-9_-]+$")


def _dump(data: object) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2)


def _doc_ref(ref: str) -> str:
    """Normalize a doc reference to a safe alias/uuid, or "" if invalid.

    A full URL is parsed locally to its last path segment — we never fetch an
    arbitrary URL, only ever call our own /api/v1/documents/<ref>. The result is
    constrained to [A-Za-z0-9_-]+ so it cannot traverse to another endpoint
    (e.g. "../apis/?private=true") or carry query/fragment chars.
    """
    ref = (ref or "").strip()
    if "://" in ref:
        ref = unquote(urlparse(ref).path).rstrip("/").rsplit("/", 1)[-1]
    return ref if _REF_RE.match(ref) else ""


@mcp.tool()
async def acedatacloud_search_docs(query: str, lang: str = "zh-cn", limit: int = 10) -> str:
    """Search the AceData Cloud documentation for a topic, API, or keyword.

    Use this first when you don't know the exact API or doc page. Returns
    matching documentation pages with a snippet and a URL.

    Args:
        query: Keywords or a question (e.g. "suno music api", "how to bill tokens").
        lang: Language code (default zh-cn; falls back to zh-cn when missing).
        limit: Max results (1-30, default 10).
    """
    limit = max(1, min(limit, 30))
    try:
        data = await client.search_docs(query=query, lang=lang, limit=limit)
        results = data.get("results", []) if isinstance(data, dict) else data
        if not results:
            return f'No documentation found for "{query}". Try acedatacloud_list_docs to browse.'
        return _dump(results)
    except DocsNotFoundError:
        return (
            "The documentation search index is not available yet. "
            "Use acedatacloud_list_docs to browse pages, or acedatacloud_fetch_doc with a known alias."
        )
    except DocsError as e:
        return f"Search failed: {e.message}"


@mcp.tool()
async def acedatacloud_list_docs(limit: int = 20, offset: int = 0, doc_type: str = "") -> str:
    """List available documentation pages (paginated).

    Args:
        limit: Number of pages to return (default 20).
        offset: Starting index for pagination (default 0).
        doc_type: Optional filter — one of Api, Proxy, Integration, Dataset, Text.
    """
    limit = max(1, min(limit, 50))
    offset = max(0, offset)
    try:
        docs = await client.list_documents(limit=limit, offset=offset, doc_type=doc_type or None)
        if not isinstance(docs, list):
            return "Unexpected response from the documents endpoint."
        items = [
            {
                "alias": d.get("alias"),
                "title": d.get("title") or d.get("name"),
                "type": d.get("type"),
                "url": f"https://platform.acedata.cloud/documents/{d.get('alias')}",
            }
            for d in docs
            if isinstance(d, dict) and d.get("alias")
        ]
        return _dump(items)
    except DocsError as e:
        return f"Failed to list docs: {e.message}"


@mcp.tool()
async def acedatacloud_fetch_doc(ref: str, lang: str = "zh-cn") -> str:
    """Fetch the full content of a documentation page.

    Args:
        ref: A document alias, UUID, or a platform.acedata.cloud/documents/<alias> URL.
        lang: Language code for the content (default zh-cn).
    """
    safe_ref = _doc_ref(ref)
    if not safe_ref:
        return (
            f'Invalid document reference "{ref}". Use an alias, UUID, or a documents/<alias> URL.'
        )
    try:
        doc = await client.get_document(safe_ref, lang=lang)
        if not isinstance(doc, dict):
            return f'Document "{safe_ref}" returned an unexpected response.'
        return _dump(
            {
                "alias": doc.get("alias"),
                "title": doc.get("title") or doc.get("name"),
                "type": doc.get("type"),
                "content": doc.get("content"),
                "url": f"https://platform.acedata.cloud/documents/{doc.get('alias')}",
            }
        )
    except DocsNotFoundError:
        return f'Document "{ref}" not found. Try acedatacloud_search_docs to locate it.'
    except DocsError as e:
        return f"Failed to fetch doc: {e.message}"
