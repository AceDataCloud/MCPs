"""Informational tools for Sora API."""

from core.server import mcp


@mcp.tool()
async def sora_list_models() -> str:
    """List all available Sora models and their capabilities.

    Shows all available model versions with their limits, features, and
    recommended use cases. Use this to understand which model to choose
    for your video generation.

    Returns:
        Table of all models with their version, limits, and features.
    """
    return """Available Sora Models:

| Model        | Max Duration (v1) | Max Duration (v2) | Quality | Features                          |
|--------------|--------------------|--------------------|---------|-----------------------------------|
| sora-2       | 15 seconds         | 12 seconds         | Good    | Standard generation, cost-effective |
| sora-2-pro   | 25 seconds         | 12 seconds         | Best    | Longer videos, higher quality     |

=== Version 1 Options ===

Video Size:
| Size   | Description                    |
|--------|--------------------------------|
| small  | Standard definition            |
| large  | HD (only sora-2-pro for 25s)   |

Video Orientation:
| Orientation | Aspect Ratio | Use Case                    |
|-------------|--------------|-----------------------------|
| landscape   | 16:9         | YouTube, presentations      |
| portrait    | 9:16         | TikTok, Instagram Stories   |

Duration:
| Duration | Models                    |
|----------|---------------------------|
| 10s      | sora-2, sora-2-pro       |
| 15s      | sora-2, sora-2-pro       |
| 25s      | sora-2-pro only          |

=== Version 2 Options ===

Video Resolution:
| Resolution | Orientation | Description              |
|------------|-------------|--------------------------|
| 720x1280   | Vertical    | HD vertical (default)    |
| 1280x720   | Horizontal  | HD horizontal            |
| 1024x1792   | Vertical    | Tall vertical            |
| 1792x1024   | Horizontal  | Wide horizontal          |

Duration (seconds):
| Seconds | Models                    |
|---------|---------------------------|
| 4s      | sora-2, sora-2-pro       |
| 8s      | sora-2, sora-2-pro       |
| 12s     | sora-2, sora-2-pro       |

Recommendations:
- Version 1: Use 'sora-2' with 'large' size for most use cases. Use 'sora-2-pro' for 25s videos.
- Version 2: Use for precise resolution control and shorter videos (4-12s). Supports image reference via input_reference.
"""


@mcp.tool()
async def sora_list_actions() -> str:
    """List all available Sora API actions and corresponding tools.

    Reference guide for what each action does and which tool to use.
    Helpful for understanding the full capabilities of the Sora MCP.

    Returns:
        Categorized list of all actions and their corresponding tools.
    """
    return """Available Sora Actions and Tools:

Video Generation (Version 1 - classic):
- sora_generate_video: Create video from a text prompt (duration: 10/15/25s, size: small/large)
- sora_generate_video_from_image: Create video from reference images (Image-to-Video)
- sora_generate_video_with_character: Create video with a character from reference video
- sora_generate_video_async: Create video with callback notification

Video Generation (Version 2 - partner channel):
- sora_generate_video_v2: Create video with pixel resolution (seconds: 4/8/12, size: 720x1280 etc.)
- sora_generate_video_v2_async: Create video v2 with callback notification

Task Management:
- sora_get_task: Check status of a single generation
- sora_get_tasks_batch: Check status of multiple generations

Information:
- sora_list_models: Show available models and their capabilities
- sora_list_actions: Show this action reference (you are here)

Workflow Examples:

1. Simple Video (v1):
   sora_generate_video(prompt) → sora_get_task(task_id)

2. Image-to-Video (v1):
   sora_generate_video_from_image(prompt, image_urls) → sora_get_task(task_id)

3. Character-based Video (v1):
   sora_generate_video_with_character(prompt, character_url) → sora_get_task(task_id)

4. Quick Video with precise resolution (v2):
   sora_generate_video_v2(prompt, seconds=8, size="1280x720") → sora_get_task(task_id)

5. Async with Callback (v1 or v2):
   sora_generate_video_async(prompt, callback_url) → Wait for callback
   sora_generate_video_v2_async(prompt, callback_url) → Wait for callback

Tips:
- Video generation takes 1-2 minutes on average
- Use async generation with callbacks for production workflows
- Version 1: sora-2-pro is required for 25-second videos
- Version 2: Supports 4, 8, or 12 second videos with pixel-based resolution
- Character videos (v1 only) cannot use real people, only animated characters
"""
