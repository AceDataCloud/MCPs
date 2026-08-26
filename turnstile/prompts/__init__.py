"""Prompt templates for the Turnstile MCP server."""

from core.server import mcp


@mcp.prompt()
def turnstile_guide() -> str:
    return """Use `turnstile_get_token` for Cloudflare Turnstile tokens."""


@mcp.prompt()
def turnstile_workflow_examples() -> str:
    return """Submit `turnstile_get_token` with `website_key` and `website_url`, and include `async` only when asynchronous processing is needed."""
