"""Distribution, wallet, access-request, and survey self-service tools."""

from typing import Annotated, Any, Literal

from pydantic import Field

from core.client import client, get_request_user_id
from core.exceptions import PlatformError
from core.server import mcp
from core.utils import confirmation_required, dumps, error_json


def _error(error: PlatformError) -> str:
    return error_json(error.code, error.message)


@mcp.tool()
async def acedatacloud_initialize_distribution(
    confirm: Annotated[
        bool, Field(description="Must be true to initialize or refresh status.")
    ] = False,
) -> str:
    """Initialize or refresh the caller's distribution status."""
    if not confirm:
        return confirmation_required("POST /distribution-statuses/initialize/", {})
    try:
        return dumps(await client.post("/distribution-statuses/initialize/", {}))
    except PlatformError as error:
        return _error(error)


@mcp.tool()
async def acedatacloud_list_distribution_levels() -> str:
    """List public affiliate levels, thresholds, and reward percentages."""
    try:
        return dumps(await client.get("/distribution-levels/"))
    except PlatformError as error:
        return _error(error)


@mcp.tool()
async def acedatacloud_get_distribution_rank(
    ordering: Annotated[
        Literal["price", "-price", "reward", "-reward"], Field(description="Rank ordering.")
    ] = "-price",
    limit: Annotated[int, Field(ge=1, le=100)] = 20,
    offset: Annotated[int, Field(ge=0)] = 0,
) -> str:
    """Rank the caller's invitees by attributed price or reward."""
    try:
        return dumps(
            await client.get(
                "/distribution-histories/rank/",
                {
                    "user_id": await get_request_user_id(),
                    "ordering": ordering,
                    "limit": limit,
                    "offset": offset,
                },
            )
        )
    except PlatformError as error:
        return _error(error)


@mcp.tool()
async def acedatacloud_get_platform_distribution_rank(
    ordering: Annotated[
        Literal[
            "total_price",
            "-total_price",
            "total_reward",
            "-total_reward",
            "invitee_count",
            "-invitee_count",
        ],
        Field(description="Global rank ordering."),
    ] = "-total_reward",
    start_time: Annotated[
        str | None, Field(description="Optional ISO date/time lower bound.")
    ] = None,
    end_time: Annotated[
        str | None, Field(description="Optional ISO date/time upper bound.")
    ] = None,
    search: Annotated[
        str | None, Field(description="Optional masked username/user ID search.")
    ] = None,
    limit: Annotated[int, Field(ge=1, le=100)] = 20,
    offset: Annotated[int, Field(ge=0)] = 0,
) -> str:
    """Get the privacy-masked platform affiliate leaderboard."""
    try:
        return dumps(
            await client.get(
                "/distribution-histories/platform-rank/",
                {
                    "ordering": ordering,
                    "start_time": start_time,
                    "end_time": end_time,
                    "search": search,
                    "limit": limit,
                    "offset": offset,
                },
            )
        )
    except PlatformError as error:
        return _error(error)


@mcp.tool()
async def acedatacloud_get_distribution_trend(
    start_time: Annotated[
        str | None, Field(description="Optional ISO date/time lower bound.")
    ] = None,
    end_time: Annotated[
        str | None, Field(description="Optional ISO date/time upper bound.")
    ] = None,
    granularity: Annotated[
        Literal["day", "week", "month"], Field(description="Time bucket size.")
    ] = "day",
) -> str:
    """Get caller reward, price, and invitee trend buckets."""
    try:
        return dumps(
            await client.get(
                "/distribution-histories/trend/",
                {
                    "user_id": await get_request_user_id(),
                    "start_time": start_time,
                    "end_time": end_time,
                    "granularity": granularity,
                },
            )
        )
    except PlatformError as error:
        return _error(error)


@mcp.tool()
async def acedatacloud_list_coin_info() -> str:
    """List the caller's verified ACE wallet information."""
    try:
        return dumps(await client.get("/coin-infos/", {"user_id": await get_request_user_id()}))
    except PlatformError as error:
        return _error(error)


@mcp.tool()
async def acedatacloud_refresh_coin_info(
    coin_info_id: Annotated[str, Field(description="CoinInfo UUID.")],
    confirm: Annotated[
        bool, Field(description="Must be true to refresh on-chain balance.")
    ] = False,
) -> str:
    """Refresh a verified wallet's ACE balance."""
    endpoint = f"/coin-infos/{coin_info_id}/update-balance/"
    if not confirm:
        return confirmation_required(f"POST {endpoint}", {"coin_info_id": coin_info_id})
    try:
        return dumps(await client.post(endpoint, {}))
    except PlatformError as error:
        return _error(error)


@mcp.tool()
async def acedatacloud_get_wallet_summary() -> str:
    """Get wallet binding, balance freshness, discounts, and visible ACE services."""
    try:
        return dumps(await client.get("/coin-wallet/summary/"))
    except PlatformError as error:
        return _error(error)


@mcp.tool()
async def acedatacloud_create_wallet_challenge(
    operation: Annotated[Literal["bind", "unbind"], Field(description="Wallet binding operation.")],
    address: Annotated[str, Field(description="Solana wallet address.")],
    confirm: Annotated[
        bool, Field(description="Must be true to create an expiring challenge.")
    ] = False,
) -> str:
    """Create a wallet-signature challenge."""
    body = {"operation": operation, "address": address}
    if not confirm:
        return confirmation_required("POST /coin-wallet/challenge/", body)
    try:
        return dumps(await client.post("/coin-wallet/challenge/", body))
    except PlatformError as error:
        return _error(error)


@mcp.tool()
async def acedatacloud_confirm_wallet_challenge(
    challenge_id: Annotated[str, Field(description="Wallet challenge UUID.")],
    signature: Annotated[str, Field(description="Wallet signature; never echoed.")],
    confirm: Annotated[bool, Field(description="Must be true to consume the challenge.")] = False,
) -> str:
    """Verify a wallet signature and bind/unbind the wallet."""
    body = {"challenge_id": challenge_id, "signature": signature}
    if not confirm:
        return confirmation_required("POST /coin-wallet/confirm/", body)
    try:
        return dumps(await client.post("/coin-wallet/confirm/", body))
    except PlatformError as error:
        return _error(error)


@mcp.tool()
async def acedatacloud_list_access_requests(
    mine: Annotated[bool, Field(description="Restrict to caller requests.")] = True,
    status: Annotated[str | None, Field(description="Optional request status.")] = None,
    policy: Annotated[str | None, Field(description="Optional policy UUID.")] = None,
    service: Annotated[str | None, Field(description="Optional service UUID.")] = None,
    ordering: Annotated[
        Literal["created_at", "-created_at", "updated_at", "-updated_at"] | None,
        Field(description="Ordering."),
    ] = None,
    limit: Annotated[int, Field(ge=1, le=100)] = 50,
    offset: Annotated[int, Field(ge=0)] = 0,
) -> str:
    """List caller-visible service access requests."""
    try:
        return dumps(
            await client.get(
                "/access-requests/",
                {
                    "mine": str(mine).lower(),
                    "status": status,
                    "policy": policy,
                    "service": service,
                    "ordering": ordering,
                    "limit": limit,
                    "offset": offset,
                },
            )
        )
    except PlatformError as error:
        return _error(error)


@mcp.tool()
async def acedatacloud_create_access_request(
    service: Annotated[str | None, Field(description="Service UUID or alias.")] = None,
    policy: Annotated[str | None, Field(description="Policy UUID or alias.")] = None,
    reason: Annotated[str | None, Field(description="Request reason.")] = None,
    contact: Annotated[str | None, Field(description="Contact details.")] = None,
    metadata: Annotated[dict[str, Any] | None, Field(description="Optional metadata.")] = None,
    confirm: Annotated[bool, Field(description="Must be true to submit the request.")] = False,
) -> str:
    """Request access to a restricted service or policy."""
    body = {
        k: v
        for k, v in {
            "service": service,
            "policy": policy,
            "reason": reason,
            "contact": contact,
            "metadata": metadata,
        }.items()
        if v is not None
    }
    if not confirm:
        return confirmation_required("POST /access-requests/", body)
    try:
        return dumps(await client.post("/access-requests/", body))
    except PlatformError as error:
        return _error(error)


@mcp.tool()
async def acedatacloud_get_access_request(
    request_id: Annotated[str, Field(description="Access request UUID.")],
) -> str:
    """Get one caller-visible access request."""
    try:
        return dumps(await client.get(f"/access-requests/{request_id}"))
    except PlatformError as error:
        return _error(error)


@mcp.tool()
async def acedatacloud_cancel_access_request(
    request_id: Annotated[str, Field(description="Access request UUID.")],
    confirm: Annotated[bool, Field(description="Must be true to cancel the request.")] = False,
) -> str:
    """Cancel a pending access request."""
    endpoint = f"/access-requests/{request_id}"
    if not confirm:
        return confirmation_required(f"DELETE {endpoint}", {"id": request_id})
    try:
        return dumps(await client.delete(endpoint))
    except PlatformError as error:
        return _error(error)


@mcp.tool()
async def acedatacloud_list_surveys() -> str:
    """List active survey templates available to the caller."""
    try:
        return dumps(await client.get("/surveys/templates/"))
    except PlatformError as error:
        return _error(error)


@mcp.tool()
async def acedatacloud_get_survey(
    alias: Annotated[str, Field(description="Survey template alias.")],
) -> str:
    """Get one active survey template."""
    try:
        return dumps(await client.get(f"/surveys/templates/{alias}/"))
    except PlatformError as error:
        return _error(error)


@mcp.tool()
async def acedatacloud_get_survey_response(
    alias: Annotated[str, Field(description="Survey template alias.")],
) -> str:
    """Get the caller's response state for a survey."""
    try:
        return dumps(await client.get("/surveys/responses/me/", {"template": alias}))
    except PlatformError as error:
        return _error(error)


@mcp.tool()
async def acedatacloud_submit_survey(
    template: Annotated[str, Field(description="Survey template alias.")],
    answers: Annotated[dict[str, Any], Field(description="Answers matching the template schema.")],
    metadata: Annotated[dict[str, Any] | None, Field(description="Optional metadata.")] = None,
    confirm: Annotated[bool, Field(description="Must be true to submit the response.")] = False,
) -> str:
    """Submit a survey response and receive any configured reward once."""
    body = {"template": template, "answers": answers, "metadata": metadata or {}}
    if not confirm:
        return confirmation_required("POST /surveys/responses/", body)
    try:
        return dumps(await client.post("/surveys/responses/", body))
    except PlatformError as error:
        return _error(error)
