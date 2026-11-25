"""ACE Music workflow guidance."""

from core.server import mcp


@mcp.prompt()
def acemusic_music_generation_guide() -> str:
    """Choose an ACE Music workflow and recover the same task."""
    return (
        "Use acemusic_upload_audio only for an explicitly requested priced import; acemusic_cover_audio or acemusic_mashup_audio use caller-owned compatible platform audio IDs. Use acemusic_generate_music for a song idea, or acemusic_generate_custom_music "
        "for supplied lyrics/style/title. Generate lyrics only when needed as a separate "
        "priced request. Save task_id immediately; query acemusic_get_task until the group "
        "is terminal. Present final MP3 URLs and describe any partial failure. If waiting "
        "or submission times out, preserve the original identity and reconcile it; do not "
        "automatically submit another paid generation. Check current account pricing."
    )
