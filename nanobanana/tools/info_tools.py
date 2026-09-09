"""Informational tools for NanoBanana API."""

from typing import get_args

from core.server import mcp
from core.types import NanoBananaModel


@mcp.tool()
async def nanobanana_list_models() -> str:
    """List available NanoBanana models without making an API request."""
    rows = []
    for model in get_args(NanoBananaModel):
        tier = "Official quality tier" if model.endswith(":official") else "Standard tier"
        rows.append(f"| `{model}` | {tier} |")

    return "\n".join(
        [
            "# Available NanoBanana Models",
            "",
            "| Model | Tier |",
            "|---|---|",
            *rows,
            "",
            "Use `nano-banana-2` for current general-purpose generation and editing. ",
            "Review live pricing before calling a generation tool.",
        ]
    )
