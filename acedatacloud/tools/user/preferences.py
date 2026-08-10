"""Translation, email preference, and content-report tools."""

from typing import Annotated, Any, Literal

from pydantic import Field

from core.client import client
from core.exceptions import PlatformError
from core.server import mcp
from core.utils import confirmation_required, dumps, error_json


@mcp.tool()
async def acedatacloud_get_translation_capabilities() -> str:
    """List models and fields that support automatic translation."""
    try:
        return dumps(await client.get("/translations/capabilities/"))
    except PlatformError as error:
        return error_json(error.code, error.message)


@mcp.tool()
async def acedatacloud_enable_translation(
    model: Annotated[str, Field(description="Capability model alias.")],
    object_id: Annotated[str, Field(description="Target object UUID.")],
    field: Annotated[str, Field(description="Translatable field name.")],
    content: Annotated[str, Field(description="Source-language content.")],
    confirm: Annotated[bool, Field(description="Must be true to enable auto-translation.")] = False,
) -> str:
    """Store source text and replace a field with an auto-translation reference."""
    body = {"model": model, "object_id": object_id, "field": field, "content": content}
    if not confirm:
        return confirmation_required("POST /translations/enable", body)
    try:
        return dumps(await client.post("/translations/enable", body))
    except PlatformError as error:
        return error_json(error.code, error.message)


@mcp.tool()
async def acedatacloud_disable_translation(
    model: Annotated[str, Field(description="Capability model alias.")],
    object_id: Annotated[str, Field(description="Target object UUID.")],
    field: Annotated[str, Field(description="Translatable field name.")],
    content: Annotated[str | None, Field(description="Optional replacement source text.")] = None,
    confirm: Annotated[
        bool, Field(description="Must be true to disable auto-translation.")
    ] = False,
) -> str:
    """Remove an auto-translation reference and restore source content."""
    body = {"model": model, "object_id": object_id, "field": field}
    if content is not None:
        body["content"] = content
    if not confirm:
        return confirmation_required("POST /translations/disable", body)
    try:
        return dumps(await client.post("/translations/disable", body))
    except PlatformError as error:
        return error_json(error.code, error.message)


@mcp.tool()
async def acedatacloud_list_email_preferences() -> str:
    """List the caller's product update, promotion, and newsletter preferences."""
    try:
        return dumps(await client.get("/email-marketing/preferences/"))
    except PlatformError as error:
        return error_json(error.code, error.message)


@mcp.tool()
async def acedatacloud_update_email_preference(
    topic: Annotated[
        Literal["product_updates", "promotions", "newsletter"], Field(description="Email topic.")
    ],
    state: Annotated[
        Literal["Subscribed", "Unsubscribed"], Field(description="Subscription state.")
    ],
    confirm: Annotated[bool, Field(description="Must be true to update the preference.")] = False,
) -> str:
    """Subscribe or unsubscribe from one email topic."""
    body = {"state": state}
    endpoint = f"/email-marketing/preferences/{topic}/"
    if not confirm:
        return confirmation_required(f"PUT {endpoint}", body)
    try:
        return dumps(await client.put(endpoint, body))
    except PlatformError as error:
        return error_json(error.code, error.message)


@mcp.tool()
async def acedatacloud_report_content(
    service: Annotated[str, Field(description="Service identifier.")],
    target_id: Annotated[str, Field(description="Reported content/task identifier.")],
    reason: Annotated[str, Field(description="Report reason.")],
    detail: Annotated[str | None, Field(description="Optional detail, capped server-side.")] = None,
    snapshot: Annotated[
        dict[str, Any] | None, Field(description="Optional bounded context snapshot.")
    ] = None,
    confirm: Annotated[bool, Field(description="Must be true to submit the report.")] = False,
) -> str:
    """Submit a moderation report for AI-generated content."""
    body = {
        "service": service,
        "target_id": target_id,
        "reason": reason,
        "detail": detail,
        "snapshot": snapshot,
    }
    if not confirm:
        return confirmation_required("POST /content-reports/", body)
    try:
        return dumps(await client.post("/content-reports/", body))
    except PlatformError as error:
        return error_json(error.code, error.message)
