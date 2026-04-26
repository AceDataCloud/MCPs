"""Informational tools for DeepSeek API."""

from core.server import mcp


@mcp.tool()
async def deepseek_list_models() -> str:
    """List all available DeepSeek models."""
    return """Available DeepSeek Models:

| Model | Description |
|-------|-------------|
| deepseek-v3 | DeepSeek V3 (recommended default) |
| deepseek-v3-250324 | DeepSeek V3 (2025-03-24) |
| deepseek-v3.2-exp | DeepSeek V3.2 Experimental |
| deepseek-r1 | DeepSeek R1 - reasoning model |
| deepseek-r1-0528 | DeepSeek R1 (2025-05-28) |"""
