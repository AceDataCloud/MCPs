"""Informational tools for Claude API."""

from core.server import mcp


@mcp.tool()
async def claude_list_models() -> str:
    """List all available Claude models."""
    return """Available Claude Models:

## Claude 4 Series
| Model | Description |
|-------|-------------|
| claude-sonnet-4-6 | Claude Sonnet 4.6 (recommended default) |
| claude-opus-4-7 | Claude Opus 4.7 - most capable |
| claude-opus-4-6 | Claude Opus 4.6 |
| claude-opus-4-5-20251101 | Claude Opus 4.5 (2025-11-01) |
| claude-haiku-4-5-20251001 | Claude Haiku 4.5 (2025-10-01) - fast and efficient |
| claude-sonnet-4-5-20250929 | Claude Sonnet 4.5 (2025-09-29) |
| claude-opus-4-1-20250805 | Claude Opus 4.1 (2025-08-05) |
| claude-sonnet-4-20250514 | Claude Sonnet 4 (2025-05-14) |
| claude-opus-4-20250514 | Claude Opus 4 (2025-05-14) |

## Claude 3 Series
| Model | Description |
|-------|-------------|
| claude-3-7-sonnet-20250219 | Claude 3.7 Sonnet (2025-02-19) |
| claude-3-5-sonnet-20241022 | Claude 3.5 Sonnet (2024-10-22) |
| claude-3-5-haiku-20241022 | Claude 3.5 Haiku (2024-10-22) |
| claude-3-5-sonnet-20240620 | Claude 3.5 Sonnet (2024-06-20) |
| claude-3-haiku-20240307 | Claude 3 Haiku (2024-03-07) |
| claude-3-sonnet-20240229 | Claude 3 Sonnet (2024-02-29) |
| claude-3-opus-20240229 | Claude 3 Opus (2024-02-29) |"""
