"""Informational tools for the MiniMax H3 API."""

from core.server import mcp


@mcp.tool()
async def minimax_list_models() -> str:
    """Describe the MiniMax H3 model and supported input modes."""
    return """MiniMax H3 Video Model

| Model | Inputs | Duration | Ratios |
|---|---|---|---|
| minimax-h3 | text, 1-9 images, 1-3 audio references | 4-15 seconds | 16:9, 9:16 |

Mode inference:
- prompt only: text-to-video
- image_urls without audio: image-to-video
- audio_urls: audio-guided video (images and prompt remain optional)
"""


@mcp.tool()
async def minimax_list_actions() -> str:
    """List MiniMax H3 generation and task tools."""
    return """MiniMax H3 Tools

Generation:
- minimax_generate_video_from_text
- minimax_generate_video_from_images
- minimax_generate_video_from_audio

Tasks:
- minimax_get_task
- minimax_get_tasks_batch

All generation tools submit asynchronously by default. Poll the returned task_id with minimax_get_task until the final video is available.
"""
