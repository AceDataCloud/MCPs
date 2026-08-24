"""Prompt templates for the Image2Text MCP server."""

from core.server import mcp


@mcp.prompt()
def image2text_guide() -> str:
    return """Use `image2text_recognize` for base64 OCR tasks."""


@mcp.prompt()
def image2text_workflow_examples() -> str:
    return """Submit `image2text_recognize` for an inline OCR result, or pass async=true when you only need the task submission response."""
