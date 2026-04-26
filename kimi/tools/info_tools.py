"""Informational tools for Kimi API."""

from core.server import mcp


@mcp.tool()
async def kimi_list_models() -> str:
    """List all available Kimi models."""
    return """Available Kimi Models:

| Model | Description |
|-------|-------------|
| kimi-k2.5 | Kimi K2.5 (recommended default) |
| kimi-k2-thinking-turbo | Kimi K2 Thinking Turbo - fast reasoning |
| kimi-k2-thinking | Kimi K2 Thinking - advanced reasoning |
| kimi-k2-instruct-0905 | Kimi K2 Instruct (2025-09-05) |
| kimi-k2-0905-preview | Kimi K2 Preview (2025-09-05) |
| kimi-k2-turbo-preview | Kimi K2 Turbo Preview |
| kimi-k2-0711-preview | Kimi K2 Preview (2025-07-11) |"""
