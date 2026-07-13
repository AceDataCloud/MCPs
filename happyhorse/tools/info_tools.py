"""Model information tools for Happy Horse."""

import json

from core.server import mcp


@mcp.tool()
async def happyhorse_list_models() -> str:
    """List Happy Horse actions, compatible models, and defaults."""
    return json.dumps(
        {
            "generate": {
                "models": ["happyhorse-1.0-t2v", "happyhorse-1.1-t2v"],
                "default": "happyhorse-1.1-t2v",
            },
            "image_to_video": {
                "models": ["happyhorse-1.0-i2v", "happyhorse-1.1-i2v"],
                "default": "happyhorse-1.1-i2v",
            },
            "reference_to_video": {
                "models": ["happyhorse-1.0-r2v", "happyhorse-1.1-r2v"],
                "default": "happyhorse-1.1-r2v",
            },
            "video_edit": {
                "models": ["happyhorse-1.0-video-edit"],
                "default": "happyhorse-1.0-video-edit",
            },
        },
        indent=2,
    )
