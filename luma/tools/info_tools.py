"""Informational tools for Luma API."""

from core.server import mcp


@mcp.tool()
async def luma_list_aspect_ratios() -> str:
    """List all available aspect ratios for Luma video generation.

    Shows all available aspect ratio options with their use cases.
    Use this to understand which aspect ratio to choose for your video.

    Returns:
        Table of all aspect ratios with their descriptions and use cases.
    """
    return """Available Luma Aspect Ratios:

| Aspect Ratio | Description          | Use Case                              |
|--------------|----------------------|---------------------------------------|
| 16:9         | Landscape (default)  | YouTube, TV, presentations            |
| 9:16         | Portrait             | TikTok, Instagram Reels, mobile       |
| 1:1          | Square               | Instagram posts, social media         |
| 4:3          | Traditional TV       | Classic video, presentations          |
| 3:4          | Portrait traditional | Portrait photos, some social media    |
| 21:9         | Ultrawide            | Cinematic, movies, widescreen         |
| 9:21         | Tall ultrawide       | Special vertical displays             |

Recommended: 16:9 for most video content, 9:16 for mobile-first platforms.
"""


@mcp.tool()
async def luma_list_actions() -> str:
    """List all available Luma API actions and corresponding tools.

    Reference guide for what each action does and which tool to use.
    Helpful for understanding the full capabilities of the Luma MCP.

    Returns:
        Categorized list of all actions and their corresponding tools.
    """
    return """Available Luma Actions and Tools:

Video Generation:
- luma_generate_video: Create video from a text prompt
- luma_generate_video_from_image: Create video using reference images
- luma_extend_video: Extend an existing video by its ID
- luma_extend_video_from_url: Extend an existing video by its URL

Task Management:
- luma_get_task: Check status of a single generation
- luma_get_tasks_batch: Check status of multiple generations

Information:
- luma_list_aspect_ratios: Show available aspect ratios
- luma_list_actions: Show this action reference (you are here)

Workflow Examples:
1. Quick video: luma_generate_video -> luma_get_task
2. Image to video: luma_generate_video_from_image -> luma_get_task
3. Long video: luma_generate_video -> luma_extend_video (repeat) -> luma_get_task
4. Video from frames: luma_generate_video_from_image (with start and end) -> luma_get_task

Tips:
- Use descriptive prompts for better results
- Include motion descriptions: "walking", "flying", "zooming in"
- Specify style: "cinematic", "realistic", "artistic"
- Video generation takes 1-2 minutes typically
- Use callback_url for async processing in production
"""
