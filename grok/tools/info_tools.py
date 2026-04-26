"""Informational tools for Grok API."""

from core.server import mcp


@mcp.tool()
async def grok_list_models() -> str:
    """List all available Grok models."""
    return """Available Grok Models:

| Model | Description |
|-------|-------------|
| grok-4 | Grok 4 - most capable |
| grok-4-1-fast | Grok 4.1 Fast |
| grok-4-1-fast-non-reasoning | Grok 4.1 Fast Non-Reasoning |
| grok-3 | Grok 3 (recommended default) |
| grok-3-mini | Grok 3 Mini - efficient |
| grok-2-vision | Grok 2 Vision - multimodal |"""
