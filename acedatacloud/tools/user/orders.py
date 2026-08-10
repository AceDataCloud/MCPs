"""Order self-service tools."""

from typing import Annotated, Any, Literal

from pydantic import Field

from core.client import client, get_request_user_id
from core.exceptions import PlatformError
from core.server import mcp
from core.utils import confirmation_required, dumps, error_json

OrderState = Literal["Pending", "Paid", "Finished", "Expired", "Failed", "Refunded"]
PayWay = Literal[
    "WechatPay", "AliPay", "Stripe", "Card", "X402", "PayPal", "AppleIAP", "Reward", "BankTransfer"
]
Surface = Literal["pc", "wap", "android", "ios"]


def _filters(
    states: OrderState | list[OrderState] | None,
    pay_ways: PayWay | list[PayWay] | None,
    created_at_from: str | None,
    created_at_to: str | None,
) -> dict[str, Any]:
    return {
        "state": states,
        "pay_way": pay_ways,
        "created_at_from": created_at_from,
        "created_at_to": created_at_to,
    }


@mcp.tool()
async def acedatacloud_list_orders(
    state: Annotated[
        OrderState | list[OrderState] | None, Field(description="Filter by one or more states.")
    ] = None,
    pay_way: Annotated[
        PayWay | list[PayWay] | None, Field(description="Filter by one or more payment methods.")
    ] = None,
    created_at_from: Annotated[
        str | None, Field(description="ISO-8601 lower creation bound.")
    ] = None,
    created_at_to: Annotated[
        str | None, Field(description="ISO-8601 upper creation bound.")
    ] = None,
    ordering: Annotated[
        Literal["created_at", "-created_at"] | None, Field(description="Order by creation time.")
    ] = None,
    limit: Annotated[int, Field(description="Max orders to return.", ge=1, le=100)] = 20,
    offset: Annotated[int, Field(description="Pagination offset.", ge=0)] = 0,
) -> str:
    """List caller-owned recharge orders with multi-value and time filters."""
    try:
        params = _filters(state, pay_way, created_at_from, created_at_to)
        params.update(
            {
                "user_id": await get_request_user_id(),
                "ordering": ordering,
                "limit": limit,
                "offset": offset,
            }
        )
        return dumps(await client.get("/orders/", params))
    except PlatformError as error:
        return error_json(error.code, error.message)


@mcp.tool()
async def acedatacloud_create_order(
    application_id: Annotated[str | None, Field(description="Single application UUID.")] = None,
    package_id: Annotated[str | None, Field(description="Single package UUID.")] = None,
    application_ids: Annotated[
        list[str] | None, Field(description="Batch application UUIDs.")
    ] = None,
    package_ids: Annotated[
        list[str] | None, Field(description="Batch package UUIDs in matching order.")
    ] = None,
    scope: Annotated[str | None, Field(description="Optional order scope.")] = None,
    description: Annotated[str | None, Field(description="Optional order description.")] = None,
    metadata: Annotated[
        dict[str, Any] | None, Field(description="Optional order metadata.")
    ] = None,
    confirm: Annotated[bool, Field(description="Must be true to create the order.")] = False,
) -> str:
    """Create a single or batch recharge order. The two modes are mutually exclusive."""
    single = application_id is not None or package_id is not None
    batch = application_ids is not None or package_ids is not None
    if single == batch:
        return error_json("validation_error", "Provide exactly one of single or batch order mode")
    if single and (not application_id or not package_id):
        return error_json("validation_error", "application_id and package_id are both required")
    if batch and (
        not application_ids or not package_ids or len(application_ids) != len(package_ids)
    ):
        return error_json(
            "validation_error", "application_ids and package_ids must be non-empty and equal length"
        )
    body = {
        key: value
        for key, value in {
            "application_id": application_id,
            "package_id": package_id,
            "application_ids": application_ids,
            "package_ids": package_ids,
            "scope": scope,
            "description": description,
            "metadata": metadata,
        }.items()
        if value is not None
    }
    if not confirm:
        return confirmation_required("POST /orders/", body)
    try:
        return dumps(await client.post("/orders/", body))
    except PlatformError as error:
        return error_json(error.code, error.message)


@mcp.tool()
async def acedatacloud_get_order(order_id: Annotated[str, Field(description="Order UUID.")]) -> str:
    """Get one caller-owned order in its authenticated detail representation."""
    try:
        return dumps(await client.get(f"/orders/{order_id}"))
    except PlatformError as error:
        return error_json(error.code, error.message)


@mcp.tool()
async def acedatacloud_get_order_summary(
    state: Annotated[
        OrderState | list[OrderState] | None, Field(description="Optional state filters.")
    ] = None,
    pay_way: Annotated[
        PayWay | list[PayWay] | None, Field(description="Optional payment filters.")
    ] = None,
    created_at_from: Annotated[
        str | None, Field(description="ISO-8601 lower creation bound.")
    ] = None,
    created_at_to: Annotated[
        str | None, Field(description="ISO-8601 upper creation bound.")
    ] = None,
) -> str:
    """Get caller order counts and finished spend summary."""
    try:
        params = _filters(state, pay_way, created_at_from, created_at_to)
        params["user_id"] = await get_request_user_id()
        return dumps(await client.get("/orders/summary/", params))
    except PlatformError as error:
        return error_json(error.code, error.message)


@mcp.tool()
async def acedatacloud_export_orders(
    state: Annotated[
        OrderState | list[OrderState] | None, Field(description="Optional state filters.")
    ] = None,
    pay_way: Annotated[
        PayWay | list[PayWay] | None, Field(description="Optional payment filters.")
    ] = None,
    created_at_from: Annotated[
        str | None, Field(description="ISO-8601 lower creation bound.")
    ] = None,
    created_at_to: Annotated[
        str | None, Field(description="ISO-8601 upper creation bound.")
    ] = None,
    max_bytes: Annotated[
        int, Field(description="Maximum CSV bytes returned.", ge=1024, le=10_485_760)
    ] = 2_097_152,
) -> str:
    """Export caller orders as bounded CSV text."""
    try:
        params = _filters(state, pay_way, created_at_from, created_at_to)
        params["user_id"] = await get_request_user_id()
        result = await client.request_text("/orders/export/", params, max_bytes=max_bytes)
        return dumps(
            {
                "filename": result.filename,
                "content_type": result.content_type,
                "size_bytes": result.size_bytes,
                "content": result.content,
            }
        )
    except PlatformError as error:
        return error_json(error.code, error.message)


@mcp.tool()
async def acedatacloud_pay_order(
    order_id: Annotated[str, Field(description="Order UUID.")],
    pay_way: Annotated[PayWay, Field(description="Payment method.")] = "Stripe",
    surface: Annotated[
        Surface, Field(description="Client surface affecting hosted payment flow.")
    ] = "pc",
    confirm: Annotated[bool, Field(description="Must be true to create payment state.")] = False,
) -> str:
    """Create a payment session. Requires ``confirm=true``."""
    body = {"pay_way": pay_way, "surface": surface}
    endpoint = f"/orders/{order_id}/pay/"
    if not confirm:
        return confirmation_required(f"POST {endpoint}", body)
    try:
        return dumps(await client.post(endpoint, body), disclose={"/pay_url"})
    except PlatformError as error:
        return error_json(error.code, error.message)


@mcp.tool()
async def acedatacloud_refresh_order(
    order_id: Annotated[str, Field(description="Order UUID.")],
    payer_id: Annotated[str | None, Field(description="PayPal payer ID when applicable.")] = None,
    confirm: Annotated[
        bool, Field(description="Must be true to query provider state and refresh the order.")
    ] = False,
) -> str:
    """Refresh an order from its payment provider. Requires confirmation."""
    body = {"payer_id": payer_id} if payer_id is not None else {}
    endpoint = f"/orders/{order_id}/refresh/"
    if not confirm:
        return confirmation_required(f"POST {endpoint}", body)
    try:
        return dumps(await client.post(endpoint, body))
    except PlatformError as error:
        return error_json(error.code, error.message)


@mcp.tool()
async def acedatacloud_verify_apple_order(
    order_id: Annotated[str, Field(description="Order UUID.")],
    transaction_id: Annotated[str, Field(description="StoreKit transaction ID.")],
    confirm: Annotated[
        bool, Field(description="Must be true to verify and fulfill the purchase.")
    ] = False,
) -> str:
    """Verify and fulfill an Apple IAP order. Requires confirmation."""
    body = {"transaction_id": transaction_id}
    endpoint = f"/orders/{order_id}/apple-verify/"
    if not confirm:
        return confirmation_required(f"POST {endpoint}", body)
    try:
        return dumps(await client.post(endpoint, body))
    except PlatformError as error:
        return error_json(error.code, error.message)
