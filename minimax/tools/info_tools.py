"""Informational tools for the MiniMax H3 API."""

from core.server import mcp


@mcp.tool()
async def minimax_list_models() -> str:
    """Describe the MiniMax H3 model and supported input modes."""
    return """MiniMax H3 Video Model

| Model | Inputs | Duration | Ratios |
|---|---|---|---|
| MiniMax-H3 | text, image, video, and audio URLs | 4-15 seconds | 768P, 2K |

Mode inference:
- text: text-to-video
- image_url: image-guided video
- video_url: video-guided video
- audio_url: audio-guided video
"""


@mcp.tool()
async def minimax_list_actions() -> str:
    """List MiniMax H3 generation and task tools."""
    return """MiniMax H3 Tools

Generation:
- minimax_generate_video_from_text
- minimax_generate_video_from_images
- minimax_generate_video_from_audio
- minimax_generate_video

Tasks:
- minimax_get_task
- minimax_get_tasks_batch

All generation tools submit asynchronously by default. Poll the returned task_id with minimax_get_task until the final video is available.
"""
