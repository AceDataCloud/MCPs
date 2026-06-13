"""Prompt templates for Grok MCP server.

MCP Prompts provide guidance to LLMs on when and how to use the available tools.
These are exposed via the MCP protocol and help LLMs make better decisions.
"""

from core.server import mcp


@mcp.prompt()
def grok_video_generation_guide() -> str:
    """Guide for choosing the right Grok Imagine tool for video generation."""
    return """# Grok Imagine Video Generation Guide

When the user wants to generate video, choose the appropriate tool based on their needs:

## Text to Video
**Tool:** `grok_text_to_video`
**Use when:**
- User gives a text description without images
- User wants to generate video from scratch
- User describes a scene, action, or concept

Only the `grok-imagine-video` model supports text-to-video.

**Example:** "Create a video of a sunset over the ocean"
→ Call `grok_text_to_video` with prompt="Cinematic shot of a sunset over the ocean, golden hour lighting, waves gently rolling, peaceful atmosphere"

## Image to Video
**Tool:** `grok_image_to_video`
**Use when:**
- User provides a reference image to animate
- User wants to turn a still photo into a short video

`grok-imagine-video-1.5-preview` is image-to-video only and requires an image_url.

**Example:** "Animate this product image"
→ Call `grok_image_to_video` with image_url and a motion prompt

## Checking Status
**Tool:** `grok_get_task`
**Use when:**
- Generation takes time and user wants to check progress
- User asks "is my video done?"
- Retrieving video URLs from a previous task

## Important Notes:
1. Video generation is async in MCP — generation tools return quickly with a task_id
2. After submission, poll with `grok_get_task` until the final video URLs are available
3. Generation typically takes ~30 seconds to a few minutes
4. Use callback_url for async notifications
5. Match aspect ratio to intended use (16:9 landscape, 9:16 portrait)
6. 480p + shorter duration costs fewer credits while iterating
"""


@mcp.prompt()
def grok_workflow_examples() -> str:
    """Common workflow examples for Grok Imagine video generation."""
    return """# Grok Imagine Workflow Examples

## Workflow 1: Text to Video Generation
1. User: "Create a video of a cat playing with yarn"
2. Call `grok_text_to_video(prompt="Close-up shot of an adorable cat playfully batting at a ball of red yarn, soft indoor lighting, shallow depth of field")`
3. Return the task_id from the submission response
4. Poll with `grok_get_task(task_id)` until the final video URLs are available

## Workflow 2: Image Animation
1. User provides an image URL
2. Ask what motion/action they want if not specified
3. Call `grok_image_to_video(image_url="user_image_url", prompt="The subject slowly turns to face the camera")`
4. Return task_id and poll with `grok_get_task`

## Workflow 3: Higher Fidelity Image Animation
1. User wants the best quality animation of a reference image
2. Call `grok_image_to_video(image_url="...", model="grok-imagine-video-1.5-preview", resolution="720p")`
3. Return task_id and poll with `grok_get_task`

## Tips:
- For text-to-video, only `grok-imagine-video` works
- Write detailed prompts including subject, action, camera, lighting
- Choose aspect ratio based on platform (16:9 YouTube, 9:16 TikTok/Reels)
- Keep duration short and resolution at 480p for fast, cheap iterations
"""


@mcp.prompt()
def grok_style_suggestions() -> str:
    """Style and prompt writing suggestions for Grok Imagine."""
    return """# Grok Imagine Prompt Style Guide

## Effective Prompt Components

Good prompts include:
- **Subject:** The main focus of the video
- **Action:** What is happening, motion description
- **Camera:** Camera movement and angle
- **Lighting:** Time of day, light quality
- **Style:** Visual style, mood, quality

## Example Prompts by Use Case

**Product Commercial:**
"A sleek smartphone rotating slowly on a reflective surface, studio lighting with soft shadows, premium commercial style"

**Social Media Content:**
"POV walking through a vibrant night market in Tokyo, colorful neon signs reflecting on wet pavement, handheld camera movement, cinematic"

**Nature/Travel:**
"Aerial drone shot slowly descending over a pristine turquoise lagoon, tropical island in background, golden hour lighting, peaceful atmosphere"

**Portrait/Lifestyle:**
"Young woman sitting in a cozy cafe, turning to look out the window, soft natural light, shallow depth of field, lifestyle photography style"

**Action/Sports:**
"Skateboarder performing a kickflip in slow motion, tracking shot following the board, sunset backlighting, urban environment"

## Camera Movement Terms
- Static, Pan left/right, Tilt up/down, Zoom in/out
- Tracking shot, Dolly in/out, Crane shot, Handheld, Aerial/Drone

## Lighting Descriptions
- Golden hour, Blue hour, High key, Low key
- Backlit, Rim light, Natural, Studio, Neon

## Quality and Style Keywords
- Cinematic, Slow motion, Timelapse, Macro, Wide angle
- Shallow depth of field, Documentary, Artistic
"""
