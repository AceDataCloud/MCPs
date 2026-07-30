"""Prompt templates for the Turnstile MCP server."""

from core.server import mcp


@mcp.prompt()
def turnstile_guide() -> str:
    return """Use `turnstile_get_token` for Cloudflare Turnstile tokens and `turnstile_get_task` for async polling."""


@mcp.prompt()
def turnstile_workflow_examples() -> str:
    return """Submit `turnstile_get_token`, capture `task_id`, then poll with `turnstile_get_task` until ready."""
