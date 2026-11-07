"""Read-only Nano Banana model information, derived from the runtime model type."""

import json
from typing import get_args

from core.server import mcp
from core.types import NanoBananaModel


@mcp.tool()
async def nanobanana_list_models() -> str:
    """List accepted model identifiers without an API request or image generation.

    This is local reference information. It does not validate the application key,
    service access, account balance, or current model price.
    """
    return json.dumps(
        {
            "models": list(get_args(NanoBananaModel)),
            "verification": "Local reference only; application authentication is not checked.",
            "pricing": "Check current account pricing before any image generation or edit.",
            "task_queries": "Query an existing task ID; never regenerate to poll.",
        },
        ensure_ascii=False,
        indent=2,
    )
