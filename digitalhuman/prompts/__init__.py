"""Reusable Digital Human workflow guidance."""

from core.server import mcp


@mcp.prompt()
def digitalhuman_workflow() -> str:
    """Explain the recommended Digital Human workflow."""
    return """Use the Digital Human tools in this order:
1. Use digitalhuman_clone_voice when the user needs a new voice_id from reference audio.
2. Use digitalhuman_create_video with either video_url or image_url.
3. For audio driving, provide either audio_url or text with voice_id.
4. If the response includes a pending task_id, poll with digitalhuman_get_task every 15 seconds.
5. Use digitalhuman_get_tasks_batch for multiple pending tasks or digitalhuman_delete_task to cancel one.

Do not invent task results. Keep polling until the task reaches a terminal state."""
