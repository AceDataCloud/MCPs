"""Prompt templates for the AceDataCloud MCP server.

MCP Prompts guide LLMs on when and how to use the available tools.
"""

from core.server import mcp


@mcp.prompt()
def acedatacloud_guide() -> str:
    """Guide for browsing the AceDataCloud catalog/docs and managing an account."""
    return """# AceDataCloud MCP Guide

One server, two tiers: the **public catalog & docs** (no token) and **account
management** (needs ACEDATACLOUD_PLATFORM_TOKEN, distinct from the
api.acedata.cloud service token).

## Catalog & docs (public — no token)
- "What services / APIs are there?" → `acedatacloud_list_services` / `acedatacloud_list_apis`
- "Show me the X service / its pricing" → `acedatacloud_get_service` / `acedatacloud_get_pricing`
- "Give me the OpenAPI spec for /suno/audios" → `acedatacloud_get_api_spec`
- "How do I do X / find the doc for Y" → `acedatacloud_search_docs` then `acedatacloud_get_doc`
- "Which models / pricing?" → `acedatacloud_list_models` / `acedatacloud_get_model`

## Money / usage (read — needs token)
- "How much balance do I have?" → `acedatacloud_get_balance`
- "What did I spend this month?" → `acedatacloud_usage_summary` (days=30)
- "Recent API calls / errors" → `acedatacloud_list_usage`
- "My orders / keys / referral earnings" → `acedatacloud_list_orders` / `_list_credentials` / `_list_distributions`

## Making changes (write — ALWAYS confirm with the user first)
Write tools do nothing unless called with confirm=true; without it they return a
preview. Show the preview and get explicit approval before re-calling with confirm=true.
- Create / revoke an API key → `acedatacloud_create_credential` / `acedatacloud_delete_credential`
- Top up: `acedatacloud_create_order` then `acedatacloud_pay_order` → give the user pay_url
- Platform tokens → `acedatacloud_create_platform_token` / `acedatacloud_delete_platform_token`

## Admin (superuser token only)
- Publish an announcement → `acedatacloud_create_announcement` (confirm=true)

## Rules
- Never print a full token value back to the user in a shared context.
- Amounts are in Credits, not USD.
- To rotate a key, delete it and create a new one.
"""
