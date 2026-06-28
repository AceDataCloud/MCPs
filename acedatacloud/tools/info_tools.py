"""Informational tools for the Platform MCP server."""

from core.server import mcp


@mcp.tool()
async def platform_get_usage_guide() -> str:
    """Get a guide for using the AceDataCloud platform management tools.

    Explains the available tools, the write-confirmation model, and the
    authentication requirements.
    """
    # Last updated: 2026-06-28
    return """# AceDataCloud Platform Management — Tool Guide

These tools manage your AceDataCloud account via the console API
(platform.acedata.cloud). Authentication uses a **platform token** set as
ACEDATACLOUD_PLATFORM_TOKEN — NOT the api.acedata.cloud service token.
Create one at https://platform.acedata.cloud/console/platform-tokens

## Read tools (safe)
- platform_get_balance — remaining credits per subscription (+ total)
- platform_list_applications — your subscriptions and balances
- platform_list_services — list/search available services
- platform_list_usage — recent API call records
- platform_usage_summary — spend aggregated by API over N days
- platform_list_credentials — your API keys (tokens masked)
- platform_list_orders — recharge orders
- platform_list_platform_tokens — platform tokens (masked)
- platform_list_models — available chat models
- platform_list_announcements — published announcements

## Write tools — require confirm=true
Calling them without confirm returns a dry-run preview and does nothing.
- platform_create_credential / platform_delete_credential
- platform_create_order then platform_pay_order (returns pay_url)
- platform_create_platform_token / platform_delete_platform_token

## Admin tools — superuser token + confirm=true
- platform_create_announcement

## Notes
- Amounts (remaining_amount, used_amount, total) are in Credits, not USD.
- Newly created credential/platform tokens are shown in full only once — store them.
- Credential rotation = delete + recreate (no in-place rotate endpoint).
"""
