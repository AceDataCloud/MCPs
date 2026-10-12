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
- minimax_list_tasks
- minimax_get_task
- minimax_get_tasks_batch
- minimax_delete_task

MCP generation tools default async to true and return a task_id immediately.
Call minimax_get_task with that ID until status is succeeded, failed, or cancelled.
Only present the video URL after succeeded; for failed or cancelled, inspect the error.
A task_id or HTTP 200 means submission was accepted, not that the video is ready.
Set async to false only when the client can wait for the complete result.
The HTTP API defaults async to false, unlike these MCP tools.
"""
