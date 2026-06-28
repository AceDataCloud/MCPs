"""Admin-only tools for the platform management API.

These require a SUPERUSER platform token; a normal token gets 403. Like all
mutating tools, they require an explicit ``confirm=True``.
"""

from typing import Annotated

from pydantic import Field

from core.client import client
from core.exceptions import PlatformAPIError, PlatformAuthError
from core.server import mcp
from core.utils import confirmation_required, dumps, error_json


@mcp.tool()
async def platform_create_announcement(
    title: Annotated[str, Field(description="Announcement title. Required.")],
    content: Annotated[str, Field(description="Announcement body in Markdown. Required.")],
    rank: Annotated[
        int | None, Field(description="Optional sort weight; higher shows first.")
    ] = None,
    tags: Annotated[list[str] | None, Field(description="Optional tags, e.g. ['product'].")] = None,
    published: Annotated[
        bool, Field(description="Publish immediately (True) or save as draft (False).")
    ] = True,
    confirm: Annotated[bool, Field(description="Must be true to actually publish.")] = False,
) -> str:
    """Publish a platform announcement (SUPERUSER token only).

    The Chinese content is stored as the source-of-truth and other locales are
    auto-translated by a background job. Requires ``confirm=true``.
    """
    body: dict = {"title": title, "content": content, "published": published}
    if rank is not None:
        body["rank"] = rank
    if tags is not None:
        body["tags"] = tags
    if not confirm:
        return confirmation_required("POST /announcements/admin/ (superuser)", body)
    try:
        result = await client.post("/announcements/admin/", body)
        return dumps(result)
    except PlatformAuthError as e:
        return error_json(
            "Authentication Error", f"{e.message} (announcements require a superuser token)"
        )
    except PlatformAPIError as e:
        return error_json("API Error", e.message)
