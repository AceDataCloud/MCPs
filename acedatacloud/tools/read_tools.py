"""Read-only tools for the AceDataCloud platform management API."""

import datetime as dt
from typing import Annotated

from pydantic import Field

from core.client import client, get_request_user_id
from core.exceptions import PlatformAPIError, PlatformAuthError
from core.server import mcp
from core.utils import dumps, error_json


def _since(days: int | None) -> str | None:
    if not days:
        return None
    return (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=days)).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )


def _wrap(result: object, reveal: bool = False) -> str:
    if result is None:
        return error_json("No Response", "The API returned an empty response.")
    return dumps(result, reveal=reveal)


@mcp.tool()
async def acedatacloud_list_services(
    search: Annotated[
        str | None,
        Field(
            description="Optional case-insensitive substring to match against service alias or title."
        ),
    ] = None,
    service_type: Annotated[
        str | None,
        Field(description="Filter by type: Api/Proxy/Integration/Dataset/Introduction/Agent."),
    ] = None,
    tag: Annotated[str | None, Field(description="Filter by tag, e.g. 'application'.")] = None,
    private: Annotated[
        bool | None,
        Field(description="Filter by privacy: False = public only, True = private only, unset = all."),
    ] = None,
    limit: Annotated[
        int, Field(description="Max services to return when not searching.", ge=1, le=300)
    ] = 100,
) -> str:
    """List the services available on the AceDataCloud platform.

    A *service* is a product (e.g. ``suno``, ``midjourney``) you can subscribe to.
    ``search`` finds one by alias/title (client-side); ``service_type``, ``tag`` and
    ``private`` are applied server-side. Returns count + items.
    """
    try:
        server_filters = {
            "type": service_type,
            "tag": tag,
            "private": None if private is None else str(private).lower(),
        }
        if search:
            result = await client.get("/services/", {"limit": 300, **server_filters})
            items = result.get("items", []) if isinstance(result, dict) else []
            s = search.lower()
            items = [
                it
                for it in items
                if s in (it.get("alias") or "").lower() or s in (it.get("title") or "").lower()
            ]
            return dumps({"count": len(items), "items": items})
        result = await client.get("/services/", {"limit": limit, **server_filters})
        return _wrap(result)
    except PlatformAuthError as e:
        return error_json("Authentication Error", e.message)
    except PlatformAPIError as e:
        return error_json("API Error", e.message)


@mcp.tool()
async def acedatacloud_list_applications(
    service_id: Annotated[str | None, Field(description="Filter by service UUID.")] = None,
    scope: Annotated[
        str | None, Field(description="Filter by scope: 'Individual' or 'Global'.")
    ] = None,
    limit: Annotated[int, Field(description="Max applications to return.", ge=1, le=200)] = 50,
) -> str:
    """List your subscriptions (applications). Each carries the balance
    (``remaining_amount``) and spend (``used_amount``) for one service, in Credits.
    """
    try:
        result = await client.get(
            "/applications/",
            {
                "limit": limit,
                "service_id": service_id,
                "scope": scope,
                "user_id": get_request_user_id(),
            },
        )
        return _wrap(result)
    except PlatformAuthError as e:
        return error_json("Authentication Error", e.message)
    except PlatformAPIError as e:
        return error_json("API Error", e.message)


@mcp.tool()
async def acedatacloud_get_balance(
    service_id: Annotated[
        str | None, Field(description="Optional service UUID to filter by.")
    ] = None,
) -> str:
    """Summarize your remaining credit balance across subscriptions.

    Returns a compact list of ``{service_id, remaining_amount, used_amount, scope}``
    plus the total remaining. Amounts are in Credits, not USD.
    """
    try:
        result = await client.get(
            "/applications/",
            {"limit": 200, "service_id": service_id, "user_id": get_request_user_id()},
        )
        items = result.get("items", []) if isinstance(result, dict) else []
        summary = [
            {
                "service_id": it.get("service_id"),
                "application_id": it.get("id"),
                "remaining_amount": it.get("remaining_amount"),
                "used_amount": it.get("used_amount"),
                "scope": it.get("scope"),
            }
            for it in items
        ]
        total = sum((it.get("remaining_amount") or 0) for it in items)
        return dumps({"total_remaining": total, "unit": "Credit", "applications": summary})
    except PlatformAuthError as e:
        return error_json("Authentication Error", e.message)
    except PlatformAPIError as e:
        return error_json("API Error", e.message)


@mcp.tool()
async def acedatacloud_list_usage(
    api_id: Annotated[str | None, Field(description="Filter by API UUID.")] = None,
    status_code: Annotated[
        int | None, Field(description="Filter by HTTP status code, e.g. 200.")
    ] = None,
    days: Annotated[
        int | None, Field(description="Only records newer than N days.", ge=1, le=365)
    ] = None,
    limit: Annotated[int, Field(description="Max records to return.", ge=1, le=100)] = 20,
) -> str:
    """List recent API call (usage) records: status code, latency, credits deducted."""
    try:
        result = await client.get(
            "/usage/apis/",
            {
                "limit": limit,
                "api_id": api_id,
                "status_code": status_code,
                "created_at_from": _since(days),
                "user_id": get_request_user_id(),
            },
        )
        return _wrap(result)
    except PlatformAuthError as e:
        return error_json("Authentication Error", e.message)
    except PlatformAPIError as e:
        return error_json("API Error", e.message)


@mcp.tool()
async def acedatacloud_usage_summary(
    days: Annotated[
        int, Field(description="Aggregate spend over the last N days.", ge=1, le=365)
    ] = 30,
    api_id: Annotated[str | None, Field(description="Optional API UUID to filter by.")] = None,
) -> str:
    """Aggregate API spend over a time window: total Credits plus a per-API breakdown."""
    try:
        result = await client.get(
            "/usage/apis/aggregate/",
            {"created_at_from": _since(days), "api_id": api_id, "user_id": get_request_user_id()},
        )
        apis = result.get("apis", {}) if isinstance(result, dict) else {}
        by_api: dict[str, float] = {}
        for it in result.get("items", []) if isinstance(result, dict) else []:
            key = it.get("api_id")
            by_api[key] = by_api.get(key, 0.0) + (it.get("amount") or 0.0)
        breakdown = sorted(
            (
                {"api_id": k, "title": apis.get(k, {}).get("title"), "credits": round(v, 4)}
                for k, v in by_api.items()
            ),
            key=lambda r: -r["credits"],
        )
        total = result.get("total") if isinstance(result, dict) else None
        return dumps({"days": days, "total_credits": total, "by_api": breakdown})
    except PlatformAuthError as e:
        return error_json("Authentication Error", e.message)
    except PlatformAPIError as e:
        return error_json("API Error", e.message)


@mcp.tool()
async def acedatacloud_list_credentials(
    application_id: Annotated[str | None, Field(description="Filter by application UUID.")] = None,
    limit: Annotated[int, Field(description="Max credentials to return.", ge=1, le=100)] = 50,
) -> str:
    """List your API keys (credentials). Token values are masked."""
    try:
        result = await client.get(
            "/credentials/",
            {"limit": limit, "application_id": application_id, "user_id": get_request_user_id()},
        )
        return _wrap(result)
    except PlatformAuthError as e:
        return error_json("Authentication Error", e.message)
    except PlatformAPIError as e:
        return error_json("API Error", e.message)


@mcp.tool()
async def acedatacloud_list_orders(
    state: Annotated[
        str | None,
        Field(description="Filter by state: Pending/Paid/Finished/Expired/Failed/Refunded."),
    ] = None,
    pay_way: Annotated[
        str | None,
        Field(description="Filter by pay_way: WechatPay/AliPay/Stripe/X402/PayPal/Reward."),
    ] = None,
    limit: Annotated[int, Field(description="Max orders to return.", ge=1, le=100)] = 20,
) -> str:
    """List recharge orders with their state and payment method."""
    try:
        result = await client.get(
            "/orders/",
            {"limit": limit, "state": state, "pay_way": pay_way, "user_id": get_request_user_id()},
        )
        return _wrap(result)
    except PlatformAuthError as e:
        return error_json("Authentication Error", e.message)
    except PlatformAPIError as e:
        return error_json("API Error", e.message)


@mcp.tool()
async def acedatacloud_list_platform_tokens(
    limit: Annotated[int, Field(description="Max tokens to return.", ge=1, le=100)] = 50,
) -> str:
    """List your platform tokens (the credentials used to call this management API). Masked."""
    try:
        result = await client.get(
            "/platform-tokens/", {"limit": limit, "user_id": get_request_user_id()}
        )
        return _wrap(result)
    except PlatformAuthError as e:
        return error_json("Authentication Error", e.message)
    except PlatformAPIError as e:
        return error_json("API Error", e.message)


@mcp.tool()
async def acedatacloud_list_models() -> str:
    """List the chat-completion models available on the platform (OpenAI-style)."""
    try:
        result = await client.get("/models/")
        return _wrap(result)
    except PlatformAuthError as e:
        return error_json("Authentication Error", e.message)
    except PlatformAPIError as e:
        return error_json("API Error", e.message)


@mcp.tool()
async def acedatacloud_list_announcements(
    limit: Annotated[int, Field(description="Max announcements to return.", ge=1, le=100)] = 20,
) -> str:
    """List published platform announcements (newest first)."""
    try:
        result = await client.get("/announcements/", {"limit": limit})
        return _wrap(result)
    except PlatformAuthError as e:
        return error_json("Authentication Error", e.message)
    except PlatformAPIError as e:
        return error_json("API Error", e.message)


@mcp.tool()
async def acedatacloud_list_distributions(
    limit: Annotated[
        int, Field(description="Max commission history records to return.", ge=1, le=100)
    ] = 20,
) -> str:
    """Show your referral/affiliate earnings: current status (level, total price,
    total reward) plus recent commission events. Amounts are in Credits.
    """
    try:
        status = await client.get(
            "/distribution-statuses/", {"limit": 1, "user_id": get_request_user_id()}
        )
        history = await client.get(
            "/distribution-histories/", {"limit": limit, "user_id": get_request_user_id()}
        )
        status_items = status.get("items", []) if isinstance(status, dict) else []
        return dumps(
            {
                "status": status_items[0] if status_items else None,
                "history_count": history.get("count") if isinstance(history, dict) else None,
                "history": history.get("items", []) if isinstance(history, dict) else [],
            }
        )
    except PlatformAuthError as e:
        return error_json("Authentication Error", e.message)
    except PlatformAPIError as e:
        return error_json("API Error", e.message)
