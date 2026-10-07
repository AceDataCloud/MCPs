"""Public blog reads and permission-controlled editorial tools."""

from typing import Annotated, Any, Literal
from uuid import UUID

from pydantic import Field

from core.client import client
from core.exceptions import PlatformError
from core.server import mcp
from core.utils import confirmation_required, dumps, error_json

Category = Annotated[
    str,
    Field(
        max_length=32,
        description=(
            "Existing blog category slug: product-updates, tech-sharing (default), "
            "product-recommendations, industry-insights, or an administrator-defined category. "
            "Legacy aliases product, engineering, model-news and comparison remain accepted."
        ),
    ),
]
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
    category: Category | None = None,
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
    category: Category | None = None,
    published: Annotated[
        bool | None,
        Field(
            description="False for unpublished editorial records, true for published, null for both."
        ),
    ] = False,
    status: Annotated[
        Literal["draft", "pending", "rejected", "approved", "published"] | None,
        Field(description="Optional editorial status filter."),
    ] = None,
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
            "status": status,
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
async def acedatacloud_list_blog_comments(
    blog_id: Annotated[UUID, Field(description="Blog UUID from the editorial list.")],
) -> str:
    """List private review threads, replies and resolution states. Requires blog:read."""
    return await _read(f"/blogs/admin/{blog_id}/comments/", {})


@mcp.tool()
async def acedatacloud_add_blog_comment(
    blog_id: UUID,
    expected_version: Annotated[
        int, Field(ge=1, description="review_version from the saved draft.")
    ],
    body: Annotated[str, Field(min_length=1, max_length=2000)],
    field: Literal["overall", "title", "summary", "content"] = "overall",
    start_offset: Annotated[
        int | None, Field(ge=0, description="UTF-16 start offset for selected source text.")
    ] = None,
    end_offset: Annotated[
        int | None, Field(ge=1, description="UTF-16 end offset for selected source text.")
    ] = None,
    quote: Annotated[
        str | None, Field(max_length=2000, description="Exact selected source text.")
    ] = None,
    confirm: Annotated[bool, Field(description="True to post this review comment.")] = False,
) -> str:
    """Add an overall or inline review thread. Requires blog:read plus blog:write or blog:publish.

    For inline comments, provide field, start_offset, end_offset and quote from
    the saved source. Comments can be added after rejection without changing status.
    """
    body_data: dict[str, Any] = {"expected_version": expected_version, "body": body, "field": field}
    if field != "overall":
        body_data.update(start_offset=start_offset, end_offset=end_offset, quote=quote)
    return await _write("POST", f"/blogs/admin/{blog_id}/comments/", body_data, confirm)


@mcp.tool()
async def acedatacloud_reply_blog_comment(
    blog_id: UUID,
    comment_id: UUID,
    body: Annotated[str, Field(min_length=1, max_length=2000)],
    confirm: Annotated[bool, Field(description="True to post this reply.")] = False,
) -> str:
    """Reply to a review thread, including after rejection. Requires blog:read plus blog:write or blog:publish."""
    return await _write(
        "POST", f"/blogs/admin/{blog_id}/comments/{comment_id}/replies/", {"body": body}, confirm
    )


@mcp.tool()
async def acedatacloud_resolve_blog_comment(
    blog_id: UUID,
    comment_id: UUID,
    resolved: Annotated[bool, Field(description="True to resolve the thread; false to reopen it.")],
    confirm: Annotated[
        bool, Field(description="True to change the thread resolution state.")
    ] = False,
) -> str:
    """Resolve or reopen a private review thread. Requires blog:read plus blog:write or blog:publish."""
    return await _write(
        "PATCH", f"/blogs/admin/{blog_id}/comments/{comment_id}/", {"resolved": resolved}, confirm
    )


@mcp.tool()
async def acedatacloud_create_blog_draft(
    slug: Annotated[str, Field(pattern=r"^[a-zA-Z0-9_-]{1,200}$")],
    title: Annotated[str, Field(min_length=1, max_length=255)],
    summary: Annotated[str, Field(min_length=1)],
    content: Annotated[str, Field(min_length=1, description="Article source in Markdown.")],
    source_lang: SourceLanguage = "zh-cn",
    category: Category = "tech-sharing",
    author: Annotated[str, Field(max_length=120)] = "Ace Data Cloud",
    cover_url: Annotated[str, Field(description="HTTPS cover URL; empty for no cover.")] = "",
    cover_alt: Annotated[str, Field(max_length=255, description="Required with a cover.")] = "",
    tags: list[str] | None = None,
    confirm: Annotated[bool, Field(description="True to save the reviewed draft.")] = False,
) -> str:
    """Save an unpublished blog draft. Requires blog:write; translations run automatically.

    Submit the saved draft for review before another account can approve it.
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
    Source language cannot change after publication. Unpublish before changing public content.
    Withdraw a pending request before editing. Any source change revokes approval.
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
async def acedatacloud_submit_blog_post(
    blog_id: UUID,
    expected_version: Annotated[
        int, Field(ge=1, description="review_version from the draft you read.")
    ],
    confirm: Annotated[bool, Field(description="True to submit this version for review.")] = False,
) -> str:
    """Submit a draft or rejected post for peer review. Requires blog:write."""
    return await _write(
        "POST", f"/blogs/admin/{blog_id}/submit/", {"expected_version": expected_version}, confirm
    )


@mcp.tool()
async def acedatacloud_withdraw_blog_submission(
    blog_id: UUID,
    expected_version: Annotated[
        int, Field(ge=1, description="review_version from the pending post.")
    ],
    confirm: Annotated[
        bool, Field(description="True to return a pending review to draft.")
    ] = False,
) -> str:
    """Withdraw a pending review request. Requires blog:write."""
    return await _write(
        "DELETE", f"/blogs/admin/{blog_id}/submit/", {"expected_version": expected_version}, confirm
    )


@mcp.tool()
async def acedatacloud_approve_blog_post(
    blog_id: UUID,
    expected_version: Annotated[
        int, Field(ge=1, description="review_version from the draft you read.")
    ],
    comment: Annotated[str, Field(max_length=2000, description="Optional review comment.")] = "",
    confirm: Annotated[
        bool, Field(description="True after reviewing this exact draft version.")
    ] = False,
) -> str:
    """Approve a submitted post for publication. Requires blog:read and blog:publish.

    Read the full draft first. The reviewer must differ from its creator. A stale
    version is rejected, and content changes revoke approval.
    """
    return await _write(
        "POST",
        f"/blogs/admin/{blog_id}/approval/",
        {"expected_version": expected_version, "comment": comment},
        confirm,
    )


@mcp.tool()
async def acedatacloud_reject_blog_post(
    blog_id: UUID,
    expected_version: Annotated[
        int, Field(ge=1, description="review_version from the submitted post.")
    ],
    comment: Annotated[
        str,
        Field(
            max_length=2000,
            description="Rejection summary. Optional when this version already has an open review comment.",
        ),
    ] = "",
    confirm: Annotated[bool, Field(description="True to reject this submitted version.")] = False,
) -> str:
    """Reject a submitted post. Requires blog:read and blog:publish; add a comment first or provide a summary."""
    return await _write(
        "POST",
        f"/blogs/admin/{blog_id}/reject/",
        {"expected_version": expected_version, "comment": comment},
        confirm,
    )


@mcp.tool()
async def acedatacloud_withdraw_blog_approval(
    blog_id: UUID,
    confirm: Annotated[
        bool, Field(description="True to withdraw approval before publication.")
    ] = False,
) -> str:
    """Withdraw a draft's approval. Requires blog:read and blog:publish; published posts must be unpublished first."""
    return await _write("DELETE", f"/blogs/admin/{blog_id}/approval/", {}, confirm)


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

    A future publish_at schedules public visibility. The submitted version must
    be approved by a different account, and the publisher cannot be that reviewer.
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
