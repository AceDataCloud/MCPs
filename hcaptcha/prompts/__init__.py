"""Prompt templates for the hCaptcha MCP server."""

from core.server import mcp


@mcp.prompt()
def hcaptcha_guide() -> str:
    return """Use `hcaptcha_recognize` for image challenges, `hcaptcha_get_token` for site tokens, and `hcaptcha_get_task` for async polling."""


@mcp.prompt()
def hcaptcha_workflow_examples() -> str:
    return """Submit an hCaptcha tool, capture `task_id`, then poll with `hcaptcha_get_task` until `status` is `ready`."""
