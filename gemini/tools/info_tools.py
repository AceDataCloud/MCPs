"""Informational tools for Gemini API."""

from core.server import mcp


@mcp.tool()
async def gemini_list_models() -> str:
    """List all available Gemini models."""
    return """Available Gemini Models:

## Gemini 3 Series
| Model | Description |
|-------|-------------|
| gemini-3.1-pro | Gemini 3.1 Pro - most capable |
| gemini-3.0-pro | Gemini 3.0 Pro |
| gemini-3-flash-preview | Gemini 3 Flash Preview - fast |

## Gemini 2 Series
| Model | Description |
|-------|-------------|
| gemini-2.5-pro | Gemini 2.5 Pro |
| gemini-2.5-flash | Gemini 2.5 Flash (recommended default) |
| gemini-2.0-flash | Gemini 2.0 Flash |"""
