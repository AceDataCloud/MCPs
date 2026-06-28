"""Prompt templates for the Platform MCP server.

MCP Prompts guide LLMs on when and how to use the available tools.
"""

from core.server import mcp


@mcp.prompt()
def acedatacloud_guide() -> str:
    """Guide for managing an AceDataCloud account via the platform tools."""
    return """# AceDataCloud Platform Management Guide

Use these tools to help the user manage their AceDataCloud account through the
console API. Authentication is a **platform token** (ACEDATACLOUD_PLATFORM_TOKEN),
distinct from the api.acedata.cloud service token.

## Checking money / usage (read, always safe)
- "How much balance / credits do I have?" → `acedatacloud_get_balance`
- "Show my subscriptions" → `acedatacloud_list_applications`
- "What did I spend this month?" → `acedatacloud_usage_summary` (days=30)
- "Show my recent API calls / errors" → `acedatacloud_list_usage` (status_code to filter)
- "List my orders" → `acedatacloud_list_orders`

## Keys, services, models (read)
- "List / find a service" → `acedatacloud_list_services` (search=...)
- "Show my API keys" → `acedatacloud_list_credentials`
- "Which models are available?" → `acedatacloud_list_models`

## Making changes (write — ALWAYS confirm with the user first)
Write tools do nothing unless called with confirm=true; without it they return a
preview. Always show the user the preview and get explicit approval before
re-calling with confirm=true.
- Create an API key → `acedatacloud_create_credential` (needs an application_id)
- Revoke a key → `acedatacloud_delete_credential`
- Top up: `acedatacloud_create_order` then `acedatacloud_pay_order` → give the user pay_url
- Manage platform tokens → `acedatacloud_create_platform_token` / `acedatacloud_delete_platform_token`

## Admin (superuser token only)
- Publish an announcement → `acedatacloud_create_announcement` (confirm=true)

## Rules
- Never print a full token value back to the user in a shared context.
- Amounts are in Credits, not USD.
- To rotate a key, delete it and create a new one.
"""
