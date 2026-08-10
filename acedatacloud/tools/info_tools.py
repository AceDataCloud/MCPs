"""Informational tools for the Platform MCP server."""

from core.client import client
from core.exceptions import PlatformAPIError, PlatformAuthError
from core.server import mcp
from core.utils import dumps, error_json


@mcp.tool()
async def acedatacloud_get_user_info() -> str:
    """Get the current authenticated AceDataCloud account's user profile.

    Returns id, username, email, nickname, and avatar for the account
    represented by the current platform credential. Useful for constructing
    personalized content (e.g. inviter_id referral links).
    """
    try:
        result = await client.get("/platform-tokens/me/")
        if result is None:
            return error_json("No Response", "The API returned an empty response.")
        return dumps(result)
    except PlatformAuthError as e:
        return error_json("Authentication Error", e.message)
    except PlatformAPIError as e:
        return error_json("API Error", e.message)


@mcp.tool()
async def acedatacloud_get_usage_guide() -> str:
    """Get a guide for using the AceDataCloud platform management tools.

    Explains the available tools, the write-confirmation model, and the
    authentication requirements.
    """
    # Last updated: 2026-08-10
    return """# AceDataCloud Platform Management — Tool Guide

These tools manage your AceDataCloud account via the console API
(platform.acedata.cloud). Authentication uses a **platform token** set as
ACEDATACLOUD_PLATFORM_TOKEN — NOT the api.acedata.cloud service token.
Create one at https://platform.acedata.cloud/console/platform-tokens

## Read tools (safe)
- acedatacloud_get_user_info — current authenticated account user ID
- acedatacloud_get_balance — remaining credits per subscription (+ total)
- acedatacloud_list_applications — your subscriptions and balances
- acedatacloud_list_services — list/search available services
- acedatacloud_list_usage — recent API call records
- acedatacloud_usage_summary — spend aggregated by API over N days
- acedatacloud_list_credentials — your API keys (tokens masked)
- acedatacloud_list_orders — recharge orders
- acedatacloud_list_platform_tokens — platform tokens (masked)
- acedatacloud_list_models — available chat models
- acedatacloud_list_announcements — published announcements

## Write tools — require confirm=true
Calling them without confirm returns a dry-run preview and does nothing.
- acedatacloud_create_credential / acedatacloud_delete_credential
- acedatacloud_create_order then acedatacloud_pay_order (returns pay_url)
- acedatacloud_create_platform_token / acedatacloud_delete_platform_token

## Admin tools — superuser token + confirm=true
- acedatacloud_create_announcement

## Notes
- Amounts (remaining_amount, used_amount, total) are in Credits, not USD.
- Newly created credential/platform tokens are shown in full only once — store them.
- Credential rotation = delete + recreate (no in-place rotate endpoint).
"""
