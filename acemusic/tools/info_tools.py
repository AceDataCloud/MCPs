"""Local capability discovery without a paid request."""

import json

from core.server import mcp


@mcp.tool()
async def acemusic_list_models() -> str:
    """List supported public ACE Music model IDs and the default."""
    return json.dumps({"models": ["acemusic-v1.1", "acemusic-v1"], "default": "acemusic-v1.1"})


@mcp.tool()
def acemusic_get_capabilities() -> str:
    """Describe supported workflows, fees and task recovery boundaries."""
    return json.dumps(
        {
            "service": "ACE Music",
            "actions": ["generate"],
            "generation_modes": ["idea", "custom lyrics"],
            "results": "One task targets two MP3 song candidates with cover, lyrics and duration.",
            "lyrics": "Separate priced lyrics request; no implicit extra request.",
            "pricing": "Check current ACE Music service pricing for the caller's package before generation.",
            "task_queries": "Authenticated and free; query the original task ID.",
            "unsupported": [
                "upload",
                "cover",
                "extend",
                "stems",
                "voice cloning",
                "WAV",
                "MIDI",
                "video",
            ],
            "recovery": "A submission timeout has unknown outcome. Reconcile the original request; do not automatically generate again.",
        },
        ensure_ascii=False,
    )
