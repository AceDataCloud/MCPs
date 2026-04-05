"""Informational tools for Kling API."""

from core.server import mcp


@mcp.tool()
async def kling_list_models() -> str:
    """List all available Kling models for video generation.

    Shows all available model options with their capabilities and use cases.
    Use this to understand which model to choose for your video.

    Returns:
        Table of all models with their descriptions and use cases.
    """
    # Last updated: 2026-04-05
    return """Available Kling Models:

| Model              | Description          | Use Case                              |
|--------------------|----------------------|---------------------------------------|
| kling-v1           | First generation     | Basic video generation                |
| kling-v1-6         | V1 extended          | Improved quality over v1              |
| kling-v2-master    | V2 master (default)  | High-quality, balanced performance    |
| kling-v2-1-master  | V2.1 master          | Enhanced quality and consistency      |
| kling-v2-5-turbo   | V2.5 turbo           | Faster generation, good quality       |
| kling-video-o1     | Video O1             | Advanced reasoning-based generation   |

Recommended: kling-v2-master for most video content, kling-v2-5-turbo for faster results.
"""


@mcp.tool()
async def kling_list_actions() -> str:
    """List all available Kling API actions and corresponding tools.

    Reference guide for what each action does and which tool to use.
    Helpful for understanding the full capabilities of the Kling MCP.

    Returns:
        Categorized list of all actions and their corresponding tools.
    """
    # Last updated: 2026-04-05
    return """Available Kling Actions and Tools:

Video Generation:
- kling_generate_video: Create video from a text prompt (text2video)
- kling_generate_video_from_image: Create video using reference images (image2video)
- kling_extend_video: Extend an existing video by its ID

Motion Transfer:
- kling_generate_motion: Transfer motion from a reference video to a character image

Task Management:
- kling_get_task: Check status of a single generation
- kling_get_tasks_batch: Check status of multiple generations

Information:
- kling_list_models: Show available models
- kling_list_actions: Show this action reference (you are here)

Workflow Examples:
1. Quick video: kling_generate_video -> kling_get_task
2. Image to video: kling_generate_video_from_image -> kling_get_task
3. Long video: kling_generate_video -> kling_extend_video (repeat) -> kling_get_task
4. Motion transfer: kling_generate_motion -> kling_get_task

Tips:
- Use descriptive prompts for better results
- Include motion descriptions: "walking", "flying", "zooming in"
- Specify style: "cinematic", "realistic", "artistic"
- Use negative_prompt to avoid unwanted content
- Use mode='pro' for higher quality at the cost of speed
- Video generation takes 1-2 minutes typically
- Use callback_url for async processing in production
"""
