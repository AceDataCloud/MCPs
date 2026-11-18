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
            "actions": ["generate", "upload", "cover", "mashup"],
            "generation_modes": ["idea", "custom lyrics"],
            "references": "Cover uses one public audio_id; mashup uses exactly two distinct public mashup_audio_ids. References must be caller-owned and compatible. These actions require acemusic-v1.1 and audio_influence 1–100 (default 60).",
            "upload": "Separate priced import from a public HTTPS MP3 audio_url; optional name and owned audio_id anchor. Never import automatically to cover.",
            "results": "Generation, cover and mashup target two MP3 candidates; upload imports one MP3 track.",
            "lyrics": "Separate priced lyrics request; no implicit extra request.",
            "pricing": "Check current ACE Music service pricing for the caller's package before generation.",
            "task_queries": "Authenticated and free; query the original task ID.",
            "unsupported": [
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
