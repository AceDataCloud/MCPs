"""Informational tool for the AceDataCloud MCP server."""

from core.server import mcp


@mcp.tool()
async def acedatacloud_get_usage_guide() -> str:
    """Get a guide to the AceDataCloud tools: catalog/docs (public) + account management."""
    # Last updated: 2026-06-28
    return """# AceDataCloud MCP — Tool Guide

One server for the whole AceDataCloud platform: browse the public catalog & docs
(no token), and manage your account (with a platform token).

## Public — no token required
- acedatacloud_list_services / acedatacloud_get_service — the service catalog + detail
- acedatacloud_list_apis / acedatacloud_get_api_spec — API endpoints + OpenAPI specs
- acedatacloud_get_pricing — display pricing (unit, free quota, cost rules)
- acedatacloud_search_docs / acedatacloud_list_docs / acedatacloud_get_doc — documentation
- acedatacloud_list_models / acedatacloud_get_model — model catalog (all modalities) + pricing
- acedatacloud_list_datasets / acedatacloud_list_integrations — catalog extras

## Account management — needs ACEDATACLOUD_PLATFORM_TOKEN
Create one at https://platform.acedata.cloud/console/platform-tokens (NOT the
api.acedata.cloud service token).
- acedatacloud_get_balance — remaining credits per subscription (+ total)
- acedatacloud_list_applications — subscriptions and balances
- acedatacloud_list_usage / acedatacloud_usage_summary — call records + spend
- acedatacloud_list_credentials — your API keys (masked)
- acedatacloud_list_orders — recharge orders
- acedatacloud_list_platform_tokens — platform tokens (masked)
- acedatacloud_list_distributions — referral / affiliate status + commissions
- acedatacloud_list_announcements — announcements

## Write — need confirm=true (dry-run preview otherwise)
- acedatacloud_create_credential / acedatacloud_delete_credential
- acedatacloud_create_order then acedatacloud_pay_order (returns pay_url)
- acedatacloud_create_platform_token / acedatacloud_delete_platform_token

## Admin — superuser token + confirm=true
- acedatacloud_create_announcement

## Notes
- Amounts (remaining_amount, used_amount, totals) are in Credits, not USD.
- Newly created credential/platform tokens are shown in full only once — store them.
- Credential rotation = delete + recreate (no in-place rotate endpoint).
"""
