"""Prompt templates for the reCAPTCHA MCP server."""

from core.server import mcp


@mcp.prompt()
def recaptcha_guide() -> str:
    return """Use the v2 image tool for grids, the v2 token tool for widget tokens, and the v3 token tool for action-based tokens."""


@mcp.prompt()
def recaptcha_workflow_examples() -> str:
    return """Submit a reCAPTCHA tool in async mode and use the returned response payload in your workflow."""
