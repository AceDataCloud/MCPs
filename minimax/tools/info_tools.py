"""Informational tools for the MiniMax H3 API."""

from core.server import mcp


@mcp.tool()
async def minimax_list_models() -> str:
    """Describe H3/H3 Max and their model-specific output settings."""
    return """MiniMax H3 Video Model

| Model | Inputs | Duration | Resolution |
|---|---|---|---|
| MiniMax-H3 | text, image, video, and audio URLs | 4-15 seconds | 768P, 2K |
| MiniMax-H3-Max | text, image, video, and audio URLs | 5-15 seconds | 480P, 768P |

Use minimax_generate_max_video for H3 Max. Existing H3 tool defaults are unchanged.

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

Native capabilities:
- minimax_generate_max_video: H3 Max generation
- minimax_enhance_prompt: Structured prompt guidance
- minimax_regenerate_video: Owned H3 768P or exact-original-material regeneration at 2K

Tasks:
- minimax_list_tasks
- minimax_get_task
- minimax_get_tasks_batch
- minimax_delete_task

Generation/native tools return a task_id asynchronously by default. Set async=false to wait synchronously; providing a callback_url enables asynchronous delivery. Poll with minimax_get_task.
"""
