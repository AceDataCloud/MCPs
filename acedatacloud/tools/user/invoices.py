"""Invoice and billing-profile self-service tools."""

from typing import Annotated, Literal

from pydantic import Field

from core.client import client
from core.exceptions import PlatformError
from core.server import mcp
from core.utils import confirmation_required, dumps, error_json

Region = Literal["china", "overseas"]
InvoiceType = Literal["general", "special"]
InvoiceStatus = Literal["Pending", "Processing", "Issued", "Rejected", "Voided", "Cancelled"]


@mcp.tool()
async def acedatacloud_list_billing_profiles(
    region: Annotated[Region | None, Field(description="Optional billing region.")] = None,
) -> str:
    """List caller-owned billing profiles used for invoice applications."""
    try:
        return dumps(await client.get("/billing-profiles/", {"region": region}))
    except PlatformError as error:
        return error_json(error.code, error.message)


@mcp.tool()
async def acedatacloud_preview_invoice(
    order_ids: Annotated[list[str], Field(description="Non-empty order UUID list.", min_length=1)],
) -> str:
    """Preview exact invoice amount and currency without creating an invoice."""
    try:
        return dumps(await client.post("/invoices/preview/", {"order_ids": order_ids}))
    except PlatformError as error:
        return error_json(error.code, error.message)


@mcp.tool()
async def acedatacloud_list_invoices(
    status: Annotated[InvoiceStatus | None, Field(description="Optional invoice status.")] = None,
    order_id: Annotated[str | None, Field(description="Optional linked order UUID.")] = None,
    limit: Annotated[int, Field(description="Max invoices to return.", ge=1, le=100)] = 50,
    offset: Annotated[int, Field(description="Pagination offset.", ge=0)] = 0,
) -> str:
    """List caller-owned invoices."""
    try:
        return dumps(
            await client.get(
                "/invoices/",
                {"status": status, "order_id": order_id, "limit": limit, "offset": offset},
            )
        )
    except PlatformError as error:
        return error_json(error.code, error.message)


@mcp.tool()
async def acedatacloud_apply_invoice(
    region: Annotated[Region, Field(description="Invoice region.")],
    billing_profile_id: Annotated[str, Field(description="Billing profile ID.")],
    order_ids: Annotated[list[str], Field(description="Non-empty order UUID list.", min_length=1)],
    invoice_type: Annotated[InvoiceType | None, Field(description="China invoice type.")] = None,
    confirm: Annotated[bool, Field(description="Must be true to apply for the invoice.")] = False,
) -> str:
    """Apply for an invoice covering caller-owned orders. Requires confirmation."""
    body = {"region": region, "billing_profile_id": billing_profile_id, "order_ids": order_ids}
    if invoice_type is not None:
        body["invoice_type"] = invoice_type
    if not confirm:
        return confirmation_required("POST /invoices/", body)
    try:
        return dumps(await client.post("/invoices/", body))
    except PlatformError as error:
        return error_json(error.code, error.message)


@mcp.tool()
async def acedatacloud_get_invoice(
    invoice_id: Annotated[str, Field(description="Invoice UUID.")],
) -> str:
    """Get one caller-owned invoice."""
    try:
        return dumps(await client.get(f"/invoices/{invoice_id}/"))
    except PlatformError as error:
        return error_json(error.code, error.message)


@mcp.tool()
async def acedatacloud_get_order_invoice(
    order_id: Annotated[str, Field(description="Order UUID.")],
) -> str:
    """Get the current active invoice linked to an order."""
    try:
        return dumps(await client.get(f"/orders/{order_id}/invoice/"))
    except PlatformError as error:
        return error_json(error.code, error.message)


@mcp.tool()
async def acedatacloud_cancel_invoice(
    invoice_id: Annotated[str, Field(description="Invoice UUID.")],
    confirm: Annotated[bool, Field(description="Must be true to cancel the invoice.")] = False,
) -> str:
    """Cancel a caller-owned invoice. Requires confirmation."""
    endpoint = f"/invoices/{invoice_id}/cancel/"
    if not confirm:
        return confirmation_required(f"POST {endpoint}", {"invoice_id": invoice_id})
    try:
        return dumps(await client.post(endpoint, {}))
    except PlatformError as error:
        return error_json(error.code, error.message)


@mcp.tool()
async def acedatacloud_get_invoice_download(
    invoice_id: Annotated[str, Field(description="Issued invoice UUID.")],
) -> str:
    """Get a short-lived signed invoice URL as JSON without following redirects."""
    try:
        return dumps(
            await client.get(f"/invoices/{invoice_id}/download/", {"response": "json"}),
            disclose={"/url"},
        )
    except PlatformError as error:
        return error_json(error.code, error.message)
