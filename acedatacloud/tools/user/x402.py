"""X402 continuous-payment authorization tools."""

from typing import Annotated

from pydantic import Field

from core.client import client
from core.exceptions import PlatformError
from core.server import mcp
from core.utils import confirmation_required, dumps, error_json

BASE = "/x402/payment-authorization"


@mcp.tool()
async def acedatacloud_get_x402_authorization() -> str:
    """Get the caller's current continuous-payment authorization."""
    try:
        return dumps(await client.get(f"{BASE}/"))
    except PlatformError as error:
        return error_json(error.code, error.message)


@mcp.tool()
async def acedatacloud_setup_x402_authorization(
    wallet: Annotated[str, Field(description="Solana wallet address.")],
    daily_limit_atomic: Annotated[int, Field(description="Daily atomic-unit limit.", gt=0)],
    expiry_ts: Annotated[int, Field(description="Unix expiry within 365 days.", gt=0)],
    confirm: Annotated[
        bool, Field(description="Must be true to create expiring setup state.")
    ] = False,
) -> str:
    """Create an authorization setup payload for external wallet signing."""
    body = {"wallet": wallet, "daily_limit_atomic": daily_limit_atomic, "expiry_ts": expiry_ts}
    if not confirm:
        return confirmation_required(f"POST {BASE}/setup/", body)
    try:
        return dumps(await client.post(f"{BASE}/setup/", body), disclose={"/setup_token"})
    except PlatformError as error:
        return error_json(error.code, error.message)


@mcp.tool()
async def acedatacloud_confirm_x402_authorization(
    setup_token: Annotated[str, Field(description="One-time setup token.")],
    delegation: Annotated[str, Field(description="Delegation account address.")],
    delegation_tx: Annotated[str, Field(description="Delegation transaction signature.")],
    setup_tx: Annotated[
        str | None, Field(description="Optional setup transaction signature.")
    ] = None,
    confirm: Annotated[
        bool, Field(description="Must be true to verify and persist authorization.")
    ] = False,
) -> str:
    """Confirm on-chain delegation and persist continuous authorization."""
    body = {
        "setup_token": setup_token,
        "delegation": delegation,
        "delegation_tx": delegation_tx,
        "setup_tx": setup_tx,
    }
    if not confirm:
        return confirmation_required(f"POST {BASE}/confirm/", body)
    try:
        return dumps(await client.post(f"{BASE}/confirm/", body))
    except PlatformError as error:
        return error_json(error.code, error.message)


async def _set_state(action: str, confirm: bool) -> str:
    endpoint = f"{BASE}/{action}/"
    if not confirm:
        return confirmation_required(f"POST {endpoint}", {"action": action})
    try:
        return dumps(await client.post(endpoint, {}))
    except PlatformError as error:
        return error_json(error.code, error.message)


@mcp.tool()
async def acedatacloud_disable_x402_authorization(
    confirm: Annotated[bool, Field(description="Must be true to disable authorization.")] = False,
) -> str:
    """Disable the current authorization without revoking it on-chain."""
    return await _set_state("disable", confirm)


@mcp.tool()
async def acedatacloud_enable_x402_authorization(
    confirm: Annotated[bool, Field(description="Must be true to re-enable authorization.")] = False,
) -> str:
    """Re-enable a valid current authorization."""
    return await _set_state("enable", confirm)


@mcp.tool()
async def acedatacloud_confirm_x402_revocation(
    revoked_tx: Annotated[str, Field(description="On-chain revocation transaction signature.")],
    confirm: Annotated[bool, Field(description="Must be true to verify revocation.")] = False,
) -> str:
    """Verify on-chain revocation and mark the authorization revoked."""
    body = {"revoked_tx": revoked_tx}
    if not confirm:
        return confirmation_required(f"POST {BASE}/revoke-confirm/", body)
    try:
        return dumps(await client.post(f"{BASE}/revoke-confirm/", body))
    except PlatformError as error:
        return error_json(error.code, error.message)
