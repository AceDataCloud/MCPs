"""Reusable Happy Horse workflow guidance."""

from core.server import mcp


@mcp.prompt()
def happyhorse_video_workflow() -> str:
    """Explain the recommended Happy Horse workflow."""
    return """Use the Happy Horse tool that matches the input modality:
1. Use happyhorse_generate_video for text-only generation.
2. Use happyhorse_generate_video_from_image to animate one first-frame image.
3. Use happyhorse_generate_video_from_references for 1-9 subject or style references.
4. Use happyhorse_edit_video for an existing video, with up to 5 optional reference images.
5. Keep the returned task_id and call happyhorse_get_task every 15 seconds.
6. Stop only when the task response contains a final video_url or a terminal error.

Never mix a model with the wrong action. Do not invent video URLs or claim completion while the
task remains pending."""
