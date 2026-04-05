"""Informational tools for Wan API."""

from core.server import mcp


@mcp.tool()
async def wan_list_models() -> str:
    """List all available Wan video generation models.

    Shows models with their capabilities, supported actions, and use cases.

    Returns:
        Table of all models with descriptions and constraints.
    """
    # Last updated: 2026-04-05
    return """Available Wan Models:

| Model            | Action       | Description                              | Use Case                     |
|------------------|--------------|------------------------------------------|------------------------------|
| wan2.6-t2v       | text2video   | Text-to-video generation                 | Create video from text only  |
| wan2.6-i2v       | image2video  | Standard image-to-video                  | Animate an image             |
| wan2.6-r2v       | image2video  | Reference video-to-video                 | Character/timbre extraction  |
| wan2.6-i2v-flash | image2video  | Fast image-to-video                      | Quick image animation        |

Model Constraints:
- wan2.6-t2v can ONLY be used with action=text2video (no image input)
- wan2.6-i2v, wan2.6-r2v, wan2.6-i2v-flash can ONLY be used with action=image2video (requires image_url)
- wan2.6-r2v supports reference_video_urls for character/timbre extraction
- wan2.6-i2v-flash is optimized for speed with slightly lower quality

Recommended: wan2.6-t2v for text-only, wan2.6-i2v for image animation.
"""


@mcp.tool()
async def wan_list_resolutions() -> str:
    """List all available resolutions for Wan video generation.

    Shows resolution options with their quality and use cases.

    Returns:
        Table of resolutions with descriptions.
    """
    # Last updated: 2026-04-05
    return """Available Wan Resolutions:

| Resolution | Description      | Use Case                        |
|------------|------------------|---------------------------------|
| 480P       | Standard         | Draft previews, fast generation |
| 720P       | HD (default)     | General use, social media       |
| 1080P      | Full HD          | High quality, professional      |

Duration Options: 5s, 10s, or 15s

Recommended: 720P for most content, 1080P for final output.
"""


@mcp.tool()
async def wan_list_actions() -> str:
    """List all available Wan API actions and corresponding tools.

    Reference guide for what each action does and which tool to use.

    Returns:
        Categorized list of all actions and their corresponding tools.
    """
    # Last updated: 2026-04-05
    return """Available Wan Actions and Tools:

Video Generation:
- wan_generate_video: Create video from text prompt (wan2.6-t2v model)
- wan_generate_video_from_image: Create video from reference image (wan2.6-i2v/r2v/i2v-flash)

Task Management:
- wan_get_task: Check status of a single generation
- wan_get_tasks_batch: Check status of multiple generations

Information:
- wan_list_models: Show available models and constraints
- wan_list_resolutions: Show available resolutions
- wan_list_actions: Show this action reference (you are here)

Workflow Examples:
1. Text to video: wan_generate_video -> wan_get_task
2. Image to video: wan_generate_video_from_image(image_url=...) -> wan_get_task
3. Fast preview: wan_generate_video_from_image(model="wan2.6-i2v-flash") -> wan_get_task
4. With audio: wan_generate_video(audio=true) -> wan_get_task
5. Character transfer: wan_generate_video_from_image(model="wan2.6-r2v", reference_video_urls=...) -> wan_get_task

Tips:
- Use descriptive prompts with motion and style keywords
- Enable prompt_extend=true for AI-enhanced prompts
- Use audio=true to generate video with sound
- wan2.6-i2v-flash is faster but lower quality than wan2.6-i2v
- Video generation typically takes 2-5 minutes
"""
