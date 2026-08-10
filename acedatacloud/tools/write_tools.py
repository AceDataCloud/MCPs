"""Write tools (create/delete/pay) for the platform management API.

Every tool here mutates account state, so each requires an explicit
``confirm=True``. Without it the tool returns a dry-run preview and does nothing.
"""

from typing import Annotated

from pydantic import Field

from core.client import client
from core.exceptions import PlatformError
from core.server import mcp
from core.utils import confirmation_required, dumps, error_json
from tools.user.credentials import (
    acedatacloud_create_credential,
    acedatacloud_delete_credential,
)
from tools.user.orders import acedatacloud_create_order, acedatacloud_pay_order

__all__ = [
    "acedatacloud_create_credential",
    "acedatacloud_create_order",
    "acedatacloud_delete_credential",
    "acedatacloud_pay_order",
]


@mcp.tool()
async def acedatacloud_create_platform_token(
    confirm: Annotated[
        bool, Field(description="Must be true to actually create the token.")
    ] = False,
) -> str:
    """Create a new platform token (never expires). Requires ``confirm=true``.

    The full token is returned ONLY on creation — store it immediately.
    """
    if not confirm:
        return confirmation_required("POST /platform-tokens/", {})
    try:
        result = await client.post("/platform-tokens/", {})
        return dumps(result, disclose={"/token"})
    except PlatformError as error:
        return error_json(error.code, error.message)


@mcp.tool()
async def acedatacloud_delete_platform_token(
    token_id: Annotated[str, Field(description="UUID of the platform token to delete. Required.")],
    confirm: Annotated[
        bool, Field(description="Must be true to actually delete the token.")
    ] = False,
) -> str:
    """Delete (revoke) a platform token. Irreversible. Requires ``confirm=true``."""
    if not confirm:
        return confirmation_required(f"DELETE /platform-tokens/{token_id}/", {"id": token_id})
    try:
        await client.delete(f"/platform-tokens/{token_id}/")
        return dumps({"status": "deleted", "token_id": token_id})
    except PlatformError as error:
        return error_json(error.code, error.message)
