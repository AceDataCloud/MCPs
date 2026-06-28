"""Write tools (create/delete/pay) for the platform management API.

Every tool here mutates account state, so each requires an explicit
``confirm=True``. Without it the tool returns a dry-run preview and does nothing.
"""

from typing import Annotated

from pydantic import Field

from core.client import client
from core.exceptions import PlatformAPIError, PlatformAuthError
from core.server import mcp
from core.utils import confirmation_required, dumps, error_json


@mcp.tool()
async def acedatacloud_create_credential(
    application_id: Annotated[
        str,
        Field(description="UUID of the application (subscription) to attach the key to. Required."),
    ],
    name: Annotated[
        str | None, Field(description="Optional human-readable name for the key.")
    ] = None,
    limited_amount: Annotated[
        float | None, Field(description="Optional spend cap for this key, in Credits.")
    ] = None,
    expired_at: Annotated[
        str | None, Field(description="Optional ISO-8601 expiry, e.g. '2026-12-31T00:00:00Z'.")
    ] = None,
    confirm: Annotated[bool, Field(description="Must be true to actually create the key.")] = False,
) -> str:
    """Create an API key (credential) on one of your applications.

    The full token is returned ONLY on creation — store it immediately. Requires
    ``confirm=true``.
    """
    body: dict = {"application_id": application_id}
    if name is not None:
        body["name"] = name
    if limited_amount is not None:
        body["limited_amount"] = limited_amount
    if expired_at is not None:
        body["expired_at"] = expired_at
    if not confirm:
        return confirmation_required("POST /credentials/", body)
    try:
        result = await client.post("/credentials/", body)
        # reveal=True: the caller needs the freshly minted token in full.
        return dumps(result, reveal=True)
    except PlatformAuthError as e:
        return error_json("Authentication Error", e.message)
    except PlatformAPIError as e:
        return error_json("API Error", e.message)


@mcp.tool()
async def acedatacloud_delete_credential(
    credential_id: Annotated[str, Field(description="UUID of the credential to delete. Required.")],
    confirm: Annotated[bool, Field(description="Must be true to actually delete the key.")] = False,
) -> str:
    """Delete (revoke) an API key. Irreversible. Requires ``confirm=true``.

    To rotate a key, delete it and create a new one.
    """
    if not confirm:
        return confirmation_required(f"DELETE /credentials/{credential_id}", {"id": credential_id})
    try:
        await client.delete(f"/credentials/{credential_id}")
        return dumps({"status": "deleted", "credential_id": credential_id})
    except PlatformAuthError as e:
        return error_json("Authentication Error", e.message)
    except PlatformAPIError as e:
        return error_json("API Error", e.message)


@mcp.tool()
async def acedatacloud_create_order(
    application_id: Annotated[
        str, Field(description="UUID of the application to recharge. Required.")
    ],
    package_id: Annotated[
        str, Field(description="UUID of the package (quota bundle) to buy. Required.")
    ],
    confirm: Annotated[
        bool, Field(description="Must be true to actually create the order.")
    ] = False,
) -> str:
    """Create a recharge order for an application. Requires ``confirm=true``.

    Returns the order (with its ``id``); call ``acedatacloud_pay_order`` next to get a
    payment link.
    """
    body = {"application_id": application_id, "package_id": package_id}
    if not confirm:
        return confirmation_required("POST /orders/", body)
    try:
        result = await client.post("/orders/", body)
        return dumps(result)
    except PlatformAuthError as e:
        return error_json("Authentication Error", e.message)
    except PlatformAPIError as e:
        return error_json("API Error", e.message)


@mcp.tool()
async def acedatacloud_pay_order(
    order_id: Annotated[str, Field(description="UUID of the order to pay. Required.")],
    pay_way: Annotated[
        str, Field(description="Payment method: WechatPay/AliPay/Stripe/X402/PayPal/Reward.")
    ] = "Stripe",
    confirm: Annotated[
        bool, Field(description="Must be true to create the payment session.")
    ] = False,
) -> str:
    """Create a payment session for an order and return its ``pay_url``.

    Requires ``confirm=true``. The returned ``pay_url`` is where the user completes
    payment.
    """
    body = {"pay_way": pay_way}
    if not confirm:
        return confirmation_required(f"POST /orders/{order_id}/pay/", body)
    try:
        result = await client.post(f"/orders/{order_id}/pay/", body)
        # pay_url is needed by the caller to complete payment.
        return dumps(result, reveal=True)
    except PlatformAuthError as e:
        return error_json("Authentication Error", e.message)
    except PlatformAPIError as e:
        return error_json("API Error", e.message)


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
        return dumps(result, reveal=True)
    except PlatformAuthError as e:
        return error_json("Authentication Error", e.message)
    except PlatformAPIError as e:
        return error_json("API Error", e.message)


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
    except PlatformAuthError as e:
        return error_json("Authentication Error", e.message)
    except PlatformAPIError as e:
        return error_json("API Error", e.message)
