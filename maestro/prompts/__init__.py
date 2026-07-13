"""Reusable Maestro workflow guidance."""

from core.server import mcp


@mcp.prompt()
def maestro_video_workflow() -> str:
    """Explain the recommended Maestro workflow."""
    return """Use Maestro as an asynchronous end-to-end video producer:
1. Call maestro_create_video with a concrete brief, audience, duration, aspect, and language.
2. Keep the returned task_id and call maestro_get_task periodically.
3. Treat pending/planning/producing states as in progress; stop at succeeded or failed.
4. On success, read response.data.variants and present every output_url to the user.
5. To revise the result, call maestro_create_video with action remix, edit, or extend and pass the
   original task_id as ref_task_id. Describe only the desired changes in prompt.

Use file_urls for product photos, logos, portrait references, source footage, or reference audio.
Do not invent output URLs or claim completion before the task reaches succeeded."""
