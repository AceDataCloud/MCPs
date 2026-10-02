"""Public blog reads and permission-controlled editorial tools."""

from typing import Annotated, Any, Literal
from uuid import UUID

from pydantic import Field

from core.client import client
from core.exceptions import PlatformError
from core.server import mcp
from core.utils import confirmation_required, dumps, error_json

Category = Literal["model-news", "engineering", "comparison", "product"]
SourceLanguage = Literal["zh-cn", "en"]


async def _read(endpoint: str, params: dict[str, Any], *, public: bool = False) -> str:
    try:
        result = (
            await client.get_public(endpoint, params)
            if public
            else await client.get(endpoint, params)
        )
        return dumps(result)
    except PlatformError as error:
        return error_json(error.code, error.message)


async def _write(method: str, endpoint: str, body: dict[str, Any], confirm: bool) -> str:
    if not confirm:
        return confirmation_required(f"{method} {endpoint}", body)
    try:
        return dumps(await client.request(method, endpoint, json_body=body))
    except PlatformError as error:
        return error_json(error.code, error.message)


@mcp.tool()
async def acedatacloud_list_blog_posts(
    category: Annotated[Category | None, Field(description="Optional category filter.")] = None,
    lang: Annotated[str | None, Field(description="Requested translation language.")] = None,
    limit: Annotated[int, Field(ge=1, le=100)] = 20,
    offset: Annotated[int, Field(ge=0)] = 0,
) -> str:
    """List published blog posts. No account or blog permission required."""
    return await _read(
        "/blogs/",
        {"category": category, "lang": lang, "limit": limit, "offset": offset},
        public=True,
    )


@mcp.tool()
async def acedatacloud_get_blog_post(
    slug: Annotated[str, Field(pattern=r"^[a-zA-Z0-9_-]+$", description="Public blog slug.")],
    lang: Annotated[str | None, Field(description="Requested translation language.")] = None,
) -> str:
    """Read a published blog post and its localized Markdown content."""
    return await _read(f"/blogs/{slug}/", {"lang": lang}, public=True)


@mcp.tool()
async def acedatacloud_list_blog_drafts(
    query: Annotated[str | None, Field(description="Search title or slug.")] = None,
    category: Annotated[Category | None, Field(description="Optional category filter.")] = None,
    published: Annotated[
        bool | None, Field(description="False for drafts, true for published, null for both.")
    ] = False,
    limit: Annotated[int, Field(ge=1, le=100)] = 20,
    offset: Annotated[int, Field(ge=0)] = 0,
) -> str:
    """List editorial blog records. Requires blog:read, including for administrators."""
    return await _read(
        "/blogs/admin/",
        {
            "q": query,
            "category": category,
            "published": None if published is None else str(published).lower(),
            "limit": limit,
            "offset": offset,
        },
    )


@mcp.tool()
async def acedatacloud_get_blog_draft(
    blog_id: Annotated[UUID, Field(description="Blog UUID from the editorial list.")],
) -> str:
    """Read the full editable source of a draft or published post. Requires blog:read."""
    return await _read(f"/blogs/admin/{blog_id}/", {})


@mcp.tool()
async def acedatacloud_create_blog_draft(
    slug: Annotated[str, Field(pattern=r"^[a-zA-Z0-9_-]{1,200}$")],
    title: Annotated[str, Field(min_length=1, max_length=255)],
    summary: Annotated[str, Field(min_length=1)],
    content: Annotated[str, Field(min_length=1, description="Article source in Markdown.")],
    source_lang: SourceLanguage = "zh-cn",
    category: Category = "model-news",
    author: Annotated[str, Field(max_length=120)] = "Ace Data Cloud",
    cover_url: Annotated[str, Field(description="HTTPS cover URL; empty for no cover.")] = "",
    cover_alt: Annotated[str, Field(max_length=255, description="Required with a cover.")] = "",
    tags: list[str] | None = None,
    confirm: Annotated[bool, Field(description="True to save the reviewed draft.")] = False,
) -> str:
    """Save an unpublished blog draft. Requires blog:write; translations run automatically.

    Review the preview before confirming. Publish separately with acedatacloud_publish_blog_post.
    """
    return await _write(
        "POST",
        "/blogs/admin/",
        {
            "slug": slug,
            "title": title,
            "summary": summary,
            "content": content,
            "source_lang": source_lang,
            "category": category,
            "author": author,
            "cover_url": cover_url,
            "cover_alt": cover_alt,
            "tags": tags or [],
            "published": False,
        },
        confirm,
    )


@mcp.tool()
async def acedatacloud_update_blog_post(
    blog_id: UUID,
    slug: Annotated[str | None, Field(pattern=r"^[a-zA-Z0-9_-]{1,200}$")] = None,
    title: Annotated[str | None, Field(min_length=1, max_length=255)] = None,
    summary: Annotated[str | None, Field(min_length=1)] = None,
    content: Annotated[str | None, Field(min_length=1, description="Markdown source.")] = None,
    source_lang: SourceLanguage | None = None,
    category: Category | None = None,
    author: Annotated[str | None, Field(max_length=120)] = None,
    cover_url: str | None = None,
    cover_alt: Annotated[str | None, Field(max_length=255)] = None,
    tags: list[str] | None = None,
    confirm: Annotated[bool, Field(description="True to apply the reviewed changes.")] = False,
) -> str:
    """Edit blog source fields. Requires blog:write and blog:publish for published posts.

    Omitted fields stay unchanged; empty cover strings or an empty tags list clear those fields.
    Source language cannot change after publication. Updating a published post changes public content.
    """
    body = {
        key: value
        for key, value in {
            "slug": slug,
            "title": title,
            "summary": summary,
            "content": content,
            "source_lang": source_lang,
            "category": category,
            "author": author,
            "cover_url": cover_url,
            "cover_alt": cover_alt,
            "tags": tags,
        }.items()
        if value is not None
    }
    return await _write("PATCH", f"/blogs/admin/{blog_id}/", body, confirm)


@mcp.tool()
async def acedatacloud_publish_blog_post(
    blog_id: UUID,
    publish_at: Annotated[
        str | None,
        Field(description="Optional ISO 8601 publication time with timezone; omit to publish now."),
    ] = None,
    confirm: Annotated[
        bool, Field(description="True after approval of public publication.")
    ] = False,
) -> str:
    """Publish or schedule a blog post. Requires both blog:write and blog:publish.

    A future publish_at schedules public visibility. Review the source with get_blog_draft first.
    """
    body: dict[str, Any] = {"published": True}
    if publish_at is not None:
        body["publish_at"] = publish_at
    return await _write("PATCH", f"/blogs/admin/{blog_id}/", body, confirm)


@mcp.tool()
async def acedatacloud_unpublish_blog_post(
    blog_id: UUID,
    confirm: Annotated[
        bool, Field(description="True to remove the post from public view.")
    ] = False,
) -> str:
    """Return a published blog post to draft. Requires blog:write and blog:publish."""
    return await _write("PATCH", f"/blogs/admin/{blog_id}/", {"published": False}, confirm)


@mcp.tool()
async def acedatacloud_delete_blog_post(
    blog_id: UUID,
    confirm: Annotated[
        bool, Field(description="True to permanently delete the reviewed post.")
    ] = False,
) -> str:
    """Delete a blog and its translations. Requires blog:write; published posts also need blog:publish."""
    return await _write("DELETE", f"/blogs/admin/{blog_id}/", {}, confirm)
