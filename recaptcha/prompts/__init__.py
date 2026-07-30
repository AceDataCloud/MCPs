"""Prompt templates for the reCAPTCHA MCP server."""

from core.server import mcp


@mcp.prompt()
def recaptcha_guide() -> str:
    return """Use the v2 image tool for grids, the v2 token tool for widget tokens, the v3 token tool for action-based tokens, and `recaptcha_get_task` for async polling."""


@mcp.prompt()
def recaptcha_workflow_examples() -> str:
    return """Submit a reCAPTCHA tool in async mode, capture `task_id`, then poll with `recaptcha_get_task` until ready."""
