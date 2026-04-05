"""Informational tools for Hailuo API."""

from core.server import mcp


@mcp.tool()
async def hailuo_list_models() -> str:
    """List all available models for Hailuo video generation.

    Shows all available model options with their descriptions and use cases.
    Use this to understand which model to choose for your video.

    Returns:
        Table of all models with their descriptions and use cases.
    """
    # Last updated: 2026-04-05
    return """Available Hailuo (MiniMax) Video Models:

| Model                  | Type            | Description                                      | Requires Image |
|------------------------|-----------------|--------------------------------------------------|----------------|
| minimax-t2v            | Text-to-Video   | Generate video from text prompt (default)        | No             |
| minimax-i2v            | Image-to-Video  | Generate video from a reference image            | Yes            |
| minimax-i2v-director   | Director Mode   | Image-to-video with more creative control        | Yes            |

Recommended:
- Use minimax-t2v for pure text-to-video generation (no image needed)
- Use minimax-i2v when you have a reference image to animate
- Use minimax-i2v-director for director-style control over image-to-video
"""


@mcp.tool()
async def hailuo_list_actions() -> str:
    """List all available Hailuo API actions and corresponding tools.

    Reference guide for what each action does and which tool to use.
    Helpful for understanding the full capabilities of the Hailuo MCP.

    Returns:
        Categorized list of all actions and their corresponding tools.
    """
    # Last updated: 2026-04-05
    return """Available Hailuo Actions and Tools:

Video Generation:
- hailuo_generate_video: Create video from a text prompt (text-to-video)
- hailuo_generate_video_from_image: Create video using a reference image (image-to-video)

Task Management:
- hailuo_get_task: Check status of a single generation
- hailuo_get_tasks_batch: Check status of multiple generations

Information:
- hailuo_list_models: Show available video models
- hailuo_list_actions: Show this action reference (you are here)

Workflow Examples:
1. Text to video: hailuo_generate_video -> hailuo_get_task
2. Image to video: hailuo_generate_video_from_image -> hailuo_get_task
3. Batch check: hailuo_generate_video (multiple) -> hailuo_get_tasks_batch

Tips:
- Use descriptive prompts for better results
- Include motion descriptions: "walking", "flying", "zooming in"
- Specify style: "cinematic", "realistic", "artistic"
- Video generation takes 1-3 minutes typically
- Use callback_url for async processing in production
- minimax-i2v and minimax-i2v-director require a first_image_url
"""
