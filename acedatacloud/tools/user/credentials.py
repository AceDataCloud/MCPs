"""Credential self-service tools."""

from typing import Annotated, Any, Literal

from pydantic import Field

from core.client import client, get_request_user_id
from core.exceptions import PlatformError
from core.server import mcp
from core.utils import confirmation_required, dumps, error_json


def _body(**values: Any) -> dict[str, Any]:
    return {key: value for key, value in values.items() if value is not None}


@mcp.tool()
async def acedatacloud_list_credentials(
    application_id: Annotated[
        str | list[str] | None, Field(description="Filter by one or more application UUIDs.")
    ] = None,
    host: Annotated[
        str | list[str] | None, Field(description="Filter by one or more credential hosts.")
    ] = None,
    granted: Annotated[
        bool | None,
        Field(description="Filter owner-issued grants (true) or owner-held credentials (false)."),
    ] = None,
    ordering: Annotated[
        Literal["created_at", "-created_at"] | None, Field(description="Order by creation time.")
    ] = None,
    limit: Annotated[int, Field(description="Max credentials to return.", ge=1, le=100)] = 50,
    offset: Annotated[int, Field(description="Pagination offset.", ge=0)] = 0,
) -> str:
    """List API credentials with multi-value, grant, ordering, and pagination filters."""
    try:
        result = await client.get(
            "/credentials/",
            {
                "user_id": await get_request_user_id(),
                "application_id": application_id,
                "host": host,
                "granted": None if granted is None else str(granted).lower(),
                "ordering": ordering,
                "limit": limit,
                "offset": offset,
            },
        )
        return dumps(result)
    except PlatformError as error:
        return error_json(error.code, error.message)


@mcp.tool()
async def acedatacloud_create_credential(
    application_id: Annotated[str, Field(description="Application UUID.")],
    name: Annotated[str | None, Field(description="Optional human-readable name.")] = None,
    limited_amount: Annotated[
        float | None, Field(description="Optional spend cap in Credits.", ge=0)
    ] = None,
    expired_at: Annotated[str | None, Field(description="Optional ISO-8601 expiry.")] = None,
    host: Annotated[str | None, Field(description="Optional host restriction.")] = None,
    for_user_id: Annotated[
        str | None, Field(description="User ID to authorize; application owners only.")
    ] = None,
    metadata: Annotated[
        dict[str, Any] | None, Field(description="Optional credential metadata.")
    ] = None,
    allowed_api_ids: Annotated[
        list[str] | None,
        Field(description="Optional API UUID allowlist; empty means unrestricted."),
    ] = None,
    confirm: Annotated[bool, Field(description="Must be true to create the credential.")] = False,
) -> str:
    """Create an API credential or owner-issued grant. Requires ``confirm=true``."""
    body = _body(
        application_id=application_id,
        name=name,
        limited_amount=limited_amount,
        expired_at=expired_at,
        host=host,
        for_user_id=for_user_id,
        metadata=metadata,
        allowed_api_ids=allowed_api_ids,
    )
    if not confirm:
        return confirmation_required("POST /credentials/", body)
    try:
        result = await client.post("/credentials/", body)
        return dumps(result, disclose={"/token", "/password"})
    except PlatformError as error:
        return error_json(error.code, error.message)


@mcp.tool()
async def acedatacloud_get_credential(
    credential_id: Annotated[str, Field(description="Credential UUID.")],
) -> str:
    """Get one credential with token/password values masked."""
    try:
        return dumps(await client.get(f"/credentials/{credential_id}"))
    except PlatformError as error:
        return error_json(error.code, error.message)


@mcp.tool()
async def acedatacloud_update_credential(
    credential_id: Annotated[str, Field(description="Credential UUID.")],
    name: Annotated[str | None, Field(description="New display name.")] = None,
    limited_amount: Annotated[
        float | None, Field(description="New spend cap in Credits; null leaves unchanged.", ge=0)
    ] = None,
    expired_at: Annotated[
        str | None, Field(description="New ISO-8601 expiry; omitted leaves unchanged.")
    ] = None,
    clear_limited_amount: Annotated[bool, Field(description="Set the spend cap to null.")] = False,
    clear_expired_at: Annotated[bool, Field(description="Set the expiry to null.")] = False,
    allowed_api_ids: Annotated[
        list[str] | None, Field(description="API UUID allowlist; [] clears the restriction.")
    ] = None,
    confirm: Annotated[bool, Field(description="Must be true to update the credential.")] = False,
) -> str:
    """Update credential limits, name, expiry, or API allowlist. Requires confirmation."""
    body = _body(
        name=name,
        limited_amount=limited_amount,
        expired_at=expired_at,
        allowed_api_ids=allowed_api_ids,
    )
    if clear_limited_amount:
        body["limited_amount"] = None
    if clear_expired_at:
        body["expired_at"] = None
    endpoint = f"/credentials/{credential_id}"
    if not confirm:
        return confirmation_required(f"PATCH {endpoint}", body)
    try:
        return dumps(await client.patch(endpoint, body))
    except PlatformError as error:
        return error_json(error.code, error.message)


@mcp.tool()
async def acedatacloud_rotate_credential(
    credential_id: Annotated[str, Field(description="Credential UUID.")],
    confirm: Annotated[
        bool, Field(description="Must be true to rotate the credential secret.")
    ] = False,
) -> str:
    """Rotate a credential token/password and disclose the new value once."""
    endpoint = f"/credentials/{credential_id}/rotate/"
    if not confirm:
        return confirmation_required(f"POST {endpoint}", {"credential_id": credential_id})
    try:
        result = await client.post(endpoint, {})
        return dumps(result, disclose={"/token", "/password"})
    except PlatformError as error:
        return error_json(error.code, error.message)


@mcp.tool()
async def acedatacloud_delete_credential(
    credential_id: Annotated[str, Field(description="Credential UUID.")],
    confirm: Annotated[bool, Field(description="Must be true to revoke the credential.")] = False,
) -> str:
    """Revoke an API credential. Irreversible; requires ``confirm=true``."""
    endpoint = f"/credentials/{credential_id}"
    if not confirm:
        return confirmation_required(f"DELETE {endpoint}", {"id": credential_id})
    try:
        await client.delete(endpoint)
        return dumps({"status": "deleted", "credential_id": credential_id})
    except PlatformError as error:
        return error_json(error.code, error.message)
