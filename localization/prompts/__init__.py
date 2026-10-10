"""Prompt templates for the Localization MCP server."""

from core.server import mcp


@mcp.prompt()
def localization_guide() -> str:
    return """Use `localization_translate` to translate Markdown strings or JSON localization objects."""


@mcp.prompt()
def localization_workflow_examples() -> str:
    return """For Markdown, pass extension='md' and a string input. For localization JSON, pass extension='json' and an object input."""
