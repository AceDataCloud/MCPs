"""Prompt templates for the Image2Text MCP server."""

from core.server import mcp


@mcp.prompt()
def image2text_guide() -> str:
    return """Use `image2text_recognize` for base64 OCR tasks and `image2text_get_task` for async polling."""


@mcp.prompt()
def image2text_workflow_examples() -> str:
    return """Submit `image2text_recognize`, capture `task_id`, then poll with `image2text_get_task` until ready."""
