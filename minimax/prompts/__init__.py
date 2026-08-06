"""Prompt guidance for MiniMax H3 tools."""

from core.server import mcp


@mcp.prompt()
def minimax_video_generation_guide() -> str:
    """Guide tool selection for MiniMax H3 video generation."""
    return """# MiniMax H3 Video Generation

Choose by available input:
- Text only: `minimax_generate_video_from_text`
- One to nine image URLs: `minimax_generate_video_from_images`
- One to three audio URLs: `minimax_generate_video_from_audio`; images and prompt are optional

The model is always `minimax-h3`. Ratios are `16:9` and `9:16`; duration is an integer from 4 to 15 seconds. Generation is asynchronous by default. Return the task_id, then poll `minimax_get_task` until the final video URL is available.
"""


@mcp.prompt()
def minimax_workflow_examples() -> str:
    """Show common MiniMax H3 workflows."""
    return """# MiniMax H3 Workflows

1. Text: call `minimax_generate_video_from_text(prompt=..., duration=...)`.
2. Images: call `minimax_generate_video_from_images(image_urls=[...], prompt=...)`.
3. Audio: call `minimax_generate_video_from_audio(audio_urls=[...], image_urls=[...], prompt=...)`.
4. Poll the returned task with `minimax_get_task`; use `minimax_get_tasks_batch` for several tasks.

Prompts should describe subject, action, camera movement, lighting, style, and mood. For image input, focus the prompt on desired motion. For audio input, explain how motion and cuts should follow the rhythm.
"""


@mcp.prompt()
def minimax_prompt_suggestions() -> str:
    """Provide MiniMax H3 prompt-writing guidance."""
    return """# MiniMax H3 Prompt Guide

Include:
- subject and setting
- physical action and timing
- camera movement and framing
- lighting, style, and mood
- for audio guidance, the desired relationship between rhythm and visual motion

Example: `A red fox runs through a snowy forest at dawn, low tracking shot, powder snow in the air, soft cinematic light, natural motion.`
"""
