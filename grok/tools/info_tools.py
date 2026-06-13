"""Informational tools for Grok Imagine API."""

from core.server import mcp


@mcp.tool()
async def grok_list_models() -> str:
    """List all available Grok models (chat + video) and their capabilities.

    Shows the chat models and the Grok Imagine video models with their features
    and input rules. Use this to understand which model to choose.

    Returns:
        Tables of all models with their capabilities.
    """
    # Last updated: 2026-06-13
    return """Available Grok Chat Models (grok_chat_completions):

| Model                          | Notes                                            |
|--------------------------------|--------------------------------------------------|
| grok-4                         | Flagship reasoning model.                        |
| grok-4-1-fast                  | Default. Fast, capable.                          |
| grok-4-1-fast-non-reasoning    | Fast, no reasoning trace.                        |
| grok-3                         | Previous-gen flagship.                           |
| grok-3-mini                    | Smaller/cheaper; supports reasoning_effort.      |
| grok-2-vision                  | Vision-capable (image understanding) chat model. |

Available Grok Imagine Video Models:

| Model                            | Text2Video | Image2Video | Notes                              |
|----------------------------------|------------|-------------|------------------------------------|
| grok-imagine-video               | ✅         | ✅          | Default. Lower price.              |
| grok-imagine-video-1.5-preview   | ❌         | ✅          | Image-to-video ONLY (image_url required). |

Usage:
- grok_chat_completions: chat/reason/vision/tool-calling with the chat models
- grok_text_to_video: use 'grok-imagine-video' (only model that supports text-to-video)
- grok_image_to_video: either video model; '-1.5-preview' requires an input image

Aspect Ratios:
- 16:9: Landscape/widescreen (default)
- 9:16: Portrait/vertical (social media stories)
- 1:1: Square
- 4:3, 3:4, 3:2, 2:3: Other standard ratios

Resolution Options:
- 480p: Default, cheaper
- 720p: Higher quality, costs more credits per second

Duration:
- 1-15 seconds (default 8). Billing is per output second.
"""


@mcp.tool()
async def grok_list_actions() -> str:
    """List all available Grok Imagine tools and workflows.

    Reference guide for what each tool does and how they fit together.

    Returns:
        Categorized list of all tools and example workflows.
    """
    # Last updated: 2026-06-13
    return """Available Grok Tools:

Chat:
- grok_chat_completions: Chat / reasoning / vision / tool-calling with Grok chat models

Video Generation:
- grok_text_to_video: Create video from a text prompt (grok-imagine-video only)
- grok_image_to_video: Create video from an input image (+ optional prompt)

Task Management:
- grok_get_task: Check status of a single video generation
- grok_get_tasks_batch: Check status of multiple generations at once

Information:
- grok_list_models: Show available models and their capabilities
- grok_list_actions: Show this action reference (you are here)
- grok_get_prompt_guide: Get tips for writing effective video prompts

Workflow Examples:
1. Text to video: grok_text_to_video → grok_get_task (poll until succeeded)
2. Image to video: grok_image_to_video → grok_get_task (poll until succeeded)

API Response States:
- pending/processing: Video is being generated
- succeeded: Generation complete, video URL available
- failed: Generation failed (check error message)

Tips:
- Generation typically takes ~30 seconds to a few minutes
- Use callback_url for async notifications
- Lower resolution (480p) and shorter duration cost fewer credits
"""


@mcp.tool()
async def grok_get_prompt_guide() -> str:
    """Get guidance on writing effective prompts for Grok Imagine video generation.

    Shows how to structure prompts for best video generation results.

    Returns:
        Complete guide with prompt structure, examples, and tips.
    """
    # Last updated: 2026-06-13
    return """Grok Imagine Prompt Writing Guide:

## Prompt Structure

A good video prompt should include:
1. **Subject**: What/who is in the video
2. **Action**: What is happening or moving
3. **Setting**: Where the scene takes place
4. **Camera**: Camera movement or angle
5. **Lighting**: Time of day, lighting style
6. **Style**: Visual style or mood

## Example Prompts by Category

**Product/Commercial:**
"A white ceramic coffee mug on a glossy marble countertop, steam rising gently, soft morning sunlight streaming through a window, shallow depth of field, commercial style"

**Nature/Landscape:**
"Cinematic drone shot slowly ascending over a misty forest at sunrise, golden rays filtering through the trees, documentary style"

**Portrait/People:**
"Close-up of a young woman with curly hair, she turns to look at the camera and smiles warmly, natural lighting, shallow depth of field"

**Action/Movement:**
"A red sports car drifting around a corner on a mountain road, dust and smoke trailing behind, tracking shot following the car, cinematic lighting"

## Camera Movement Keywords
- Static: Fixed camera, no movement
- Pan / Tilt: Camera rotates horizontally / vertically
- Zoom in/out: Changes focal length
- Tracking/Following: Camera moves with subject
- Dolly: Camera moves forward/backward
- Aerial/Drone: Camera moves from above
- Handheld: Slightly shaky, documentary feel

## Lighting Keywords
- Golden hour: Warm sunset/sunrise light
- Blue hour: Cool, moody twilight
- High key: Bright, minimal shadows
- Low key: Dark, dramatic shadows
- Backlit / Rim lighting: Light from behind / around subject
- Natural / Studio lighting

## Image-to-Video Tips
- Describe the MOTION you want, since the image already defines the scene
- Keep motion plausible for the subject (e.g. hair/clothes moving, camera drift)
- Use reference_image_urls to steer style without changing the main subject

## Tips for Best Results
1. Be specific but not overly complex
2. Describe motion and change, not just static scenes
3. Include camera movement for dynamic videos
4. Specify lighting conditions
5. Match aspect ratio to your intended use (16:9 landscape, 9:16 vertical)
6. Shorter duration + 480p = lower cost while iterating
"""
