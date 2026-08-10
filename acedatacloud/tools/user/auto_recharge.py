"""Auto-recharge self-service tools."""

from typing import Annotated, Any, Literal

from pydantic import Field

from core.client import client, get_request_user_id
from core.exceptions import PlatformError
from core.server import mcp
from core.utils import confirmation_required, dumps, error_json

Status = Literal["Paused", "Active", "Disabled"]


@mcp.tool()
async def acedatacloud_list_auto_recharges(
    application_id: Annotated[
        str | list[str] | None, Field(description="Optional application UUID filters.")
    ] = None,
    ordering: Annotated[
        Literal["created_at", "-created_at", "updated_at", "-updated_at"] | None,
        Field(description="Creation/update ordering."),
    ] = None,
    limit: Annotated[int, Field(description="Max configs to return.", ge=1, le=100)] = 50,
    offset: Annotated[int, Field(description="Pagination offset.", ge=0)] = 0,
) -> str:
    """List caller-owned auto-recharge configurations."""
    try:
        return dumps(
            await client.get(
                "/auto-recharge-configs/",
                {
                    "user_id": await get_request_user_id(),
                    "application_id": application_id,
                    "ordering": ordering,
                    "limit": limit,
                    "offset": offset,
                },
            )
        )
    except PlatformError as error:
        return error_json(error.code, error.message)


@mcp.tool()
async def acedatacloud_create_auto_recharge(
    application_id: Annotated[str, Field(description="Application UUID.")],
    package_id: Annotated[str, Field(description="Recharge package UUID.")],
    metadata: Annotated[dict[str, Any] | None, Field(description="Optional metadata.")] = None,
    confirm: Annotated[
        bool, Field(description="Must be true to create the paused config.")
    ] = False,
) -> str:
    """Create a paused auto-recharge configuration. Requires confirmation."""
    body: dict[str, Any] = {"application_id": application_id, "package_id": package_id}
    if metadata is not None:
        body["metadata"] = metadata
    if not confirm:
        return confirmation_required("POST /auto-recharge-configs/", body)
    try:
        return dumps(await client.post("/auto-recharge-configs/", body))
    except PlatformError as error:
        return error_json(error.code, error.message)


@mcp.tool()
async def acedatacloud_get_auto_recharge(
    config_id: Annotated[str, Field(description="Auto-recharge config UUID.")],
) -> str:
    """Get one auto-recharge configuration and its authoritative quote."""
    try:
        return dumps(await client.get(f"/auto-recharge-configs/{config_id}"))
    except PlatformError as error:
        return error_json(error.code, error.message)


@mcp.tool()
async def acedatacloud_update_auto_recharge(
    config_id: Annotated[str, Field(description="Auto-recharge config UUID.")],
    package_id: Annotated[str | None, Field(description="New package UUID.")] = None,
    enabled: Annotated[bool | None, Field(description="Enable or pause triggering.")] = None,
    metadata: Annotated[dict[str, Any] | None, Field(description="Replacement metadata.")] = None,
    confirm: Annotated[bool, Field(description="Must be true to update the config.")] = False,
) -> str:
    """Patch an auto-recharge config. Requires confirmation."""
    body = {
        key: value
        for key, value in {
            "package_id": package_id,
            "enabled": enabled,
            "metadata": metadata,
        }.items()
        if value is not None
    }
    endpoint = f"/auto-recharge-configs/{config_id}"
    if not confirm:
        return confirmation_required(f"PATCH {endpoint}", body)
    try:
        return dumps(await client.patch(endpoint, body))
    except PlatformError as error:
        return error_json(error.code, error.message)


@mcp.tool()
async def acedatacloud_delete_auto_recharge(
    config_id: Annotated[str, Field(description="Auto-recharge config UUID.")],
    confirm: Annotated[bool, Field(description="Must be true to delete the config.")] = False,
) -> str:
    """Delete an auto-recharge configuration. Requires confirmation."""
    endpoint = f"/auto-recharge-configs/{config_id}"
    if not confirm:
        return confirmation_required(f"DELETE {endpoint}", {"id": config_id})
    try:
        await client.delete(endpoint)
        return dumps({"status": "deleted", "config_id": config_id})
    except PlatformError as error:
        return error_json(error.code, error.message)


@mcp.tool()
async def acedatacloud_quote_auto_recharge(
    application_id: Annotated[str, Field(description="Application UUID.")],
    package_ids: Annotated[
        list[str], Field(description="One or more package UUIDs.", min_length=1)
    ],
) -> str:
    """Get exact after-discount auto-recharge quotes without creating state."""
    try:
        return dumps(
            await client.post(
                "/auto-recharge-configs/quote/",
                {"application_id": application_id, "package_ids": package_ids},
            )
        )
    except PlatformError as error:
        return error_json(error.code, error.message)


@mcp.tool()
async def acedatacloud_setup_auto_recharge(
    config_id: Annotated[str, Field(description="Auto-recharge config UUID.")],
    confirm: Annotated[
        bool, Field(description="Must be true to create provider setup state.")
    ] = False,
) -> str:
    """Create card setup state and disclose its client secret once."""
    endpoint = f"/auto-recharge-configs/{config_id}/setup/"
    if not confirm:
        return confirmation_required(f"POST {endpoint}", {"config_id": config_id})
    try:
        return dumps(await client.post(endpoint, {}), disclose={"/client_secret", "/id"})
    except PlatformError as error:
        return error_json(error.code, error.message)


@mcp.tool()
async def acedatacloud_confirm_auto_recharge_setup(
    config_id: Annotated[str, Field(description="Auto-recharge config UUID.")],
    setup_intent_id: Annotated[str, Field(description="Completed setup intent ID.")],
    confirm: Annotated[
        bool, Field(description="Must be true to persist consent and saved card.")
    ] = False,
) -> str:
    """Confirm completed setup and activate auto recharge. Requires confirmation."""
    endpoint = f"/auto-recharge-configs/{config_id}/confirm-setup/"
    body = {"setup_intent_id": setup_intent_id}
    if not confirm:
        return confirmation_required(f"POST {endpoint}", body)
    try:
        return dumps(await client.post(endpoint, body))
    except PlatformError as error:
        return error_json(error.code, error.message)


@mcp.tool()
async def acedatacloud_disable_auto_recharge(
    config_id: Annotated[str, Field(description="Auto-recharge config UUID.")],
    confirm: Annotated[bool, Field(description="Must be true to disable triggering.")] = False,
) -> str:
    """Disable auto recharge while retaining the saved card. Requires confirmation."""
    endpoint = f"/auto-recharge-configs/{config_id}/disable/"
    if not confirm:
        return confirmation_required(f"POST {endpoint}", {"config_id": config_id})
    try:
        return dumps(await client.post(endpoint, {}))
    except PlatformError as error:
        return error_json(error.code, error.message)
