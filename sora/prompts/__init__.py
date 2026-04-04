"""Prompt templates for Sora MCP server.

MCP Prompts provide guidance to LLMs on when and how to use the available tools.
These are exposed via the MCP protocol and help LLMs make better decisions.
"""

from core.server import mcp


@mcp.prompt()
def sora_video_generation_guide() -> str:
    """Guide for choosing the right Sora tool for video generation."""
    return """# Sora Video Generation Guide

When the user wants to generate videos, choose the appropriate tool based on their needs:

## Text-to-Video Generation
**Tool:** `sora_generate_video`
**Use when:**
- User gives a text description of the video they want
- User wants to create a video from scratch
- No reference images or characters are provided

**Example:** "Create a video of a cat running on a beach"
→ Call `sora_generate_video` with prompt="A cat running on a sandy beach, sunny day, ocean waves in the background"

## Image-to-Video Generation
**Tool:** `sora_generate_video_from_image`
**Use when:**
- User provides reference images
- User wants to animate or bring images to life
- User wants the video to match a specific visual style

**Example:** "Animate this image of a city skyline"
→ Call `sora_generate_video_from_image` with the image URL and appropriate prompt

## Character-based Video
**Tool:** `sora_generate_video_with_character`
**Use when:**
- User wants to use a character from another video
- User is creating a series with consistent characters
- IMPORTANT: Only animated/digital characters, NO real people

**Example:** "Use the robot character from this video in a new scene"
→ Call `sora_generate_video_with_character` with character_url and new scene prompt

## Async Generation with Callback
**Tool:** `sora_generate_video_async`
**Use when:**
- User has a webhook endpoint
- User doesn't want to wait for generation
- Integration with async workflows

## Checking Status
**Tool:** `sora_get_task`
**Use when:**
- Generation is pending and user wants to check status
- User asks "is my video done?"
- A generation tool returned only a task_id and you need the final video URLs

## Important Notes:
1. Video generation takes 1-2 minutes and MCP tools should return quickly with a task_id
2. After any generation submission, poll with `sora_get_task` until the final video URLs are available
2. Default model is sora-2 (good balance of quality and cost)
3. Use sora-2-pro for 25-second videos or highest quality
4. Character videos CANNOT use real people - only animated characters
5. Available durations: 10s, 15s (all models), 25s (sora-2-pro only)
"""


@mcp.prompt()
def sora_workflow_examples() -> str:
    """Common workflow examples for Sora video generation."""
    return """# Sora Workflow Examples

## Workflow 1: Simple Video Generation
1. User: "Create a video of a sunset over mountains"
2. Call `sora_generate_video(prompt="A beautiful sunset over snow-capped mountains, golden hour lighting, cinematic")`
3. Return the task_id from the submission response
4. Poll with `sora_get_task(task_id)` until the completed video URLs are available

## Workflow 2: Image-to-Video
1. User provides an image URL
2. Ask what motion/action they want if not specified
3. Call `sora_generate_video_from_image(prompt="The scene comes to life with gentle motion", image_urls=[url])`
4. Return task_id

## Workflow 3: Character Reuse
1. User has a previous video with a character they like
2. User describes a new scene for that character
3. Call `sora_generate_video_with_character(prompt="...", character_url="...")`
4. Return task_id

## Workflow 4: High Quality Long Video
1. User needs a high quality 25-second video
2. Must use sora-2-pro model
3. Call `sora_generate_video(prompt="...", model="sora-2-pro", duration=25)`
4. Poll with `sora_get_task(task_id)` for the finished video

## Workflow 5: Async Production Workflow
1. User has a webhook endpoint
2. Call `sora_generate_video_async(prompt="...", callback_url="...")`
3. Return task_id
4. Results will be POSTed to their webhook

## Tips:
- Be descriptive in prompts - include scene, lighting, mood, camera movement
- Specify orientation based on platform (landscape for YouTube, portrait for TikTok)
- Use 'large' size for best quality
- Check task status if the user asks about their video
"""


@mcp.prompt()
def sora_prompt_writing_guide() -> str:
    """Prompt writing guide for best Sora video results."""
    return """# Sora Prompt Writing Guide

## Effective Prompt Structure

Good prompts include:
- **Subject:** What is the main focus (person, animal, object, scene)
- **Action:** What is happening (running, flying, transforming)
- **Setting:** Where is it taking place (beach, city, forest, space)
- **Style:** Visual style (cinematic, anime, realistic, abstract)
- **Mood:** Emotional tone (peaceful, dramatic, energetic, mysterious)
- **Lighting:** Light conditions (sunset, neon, natural, dramatic shadows)
- **Camera:** Camera movement or angle (aerial shot, tracking shot, close-up)

## Example Prompts by Style

**Cinematic:**
"A lone astronaut walks across a red Martian landscape, dramatic lighting, dust particles floating, cinematic wide shot, epic scale"

**Nature:**
"A butterfly emerges from its cocoon in slow motion, macro shot, soft natural lighting, dewdrops on petals, peaceful atmosphere"

**Urban:**
"Neon-lit streets of a futuristic Tokyo at night, flying cars, holographic advertisements, rain-slicked roads, cyberpunk aesthetic"

**Abstract:**
"Colorful paint droplets collide in slow motion, forming organic shapes, high-speed photography style, black background, vibrant colors"

**Character Animation:**
"A friendly robot waves hello and does a little dance, smooth animation, soft studio lighting, white background, Pixar style"

## Orientation Recommendations

| Platform      | Orientation | Aspect Ratio |
|---------------|-------------|--------------|
| YouTube       | landscape   | 16:9         |
| TikTok        | portrait    | 9:16         |
| Instagram Reel| portrait    | 9:16         |
| Instagram Post| square      | 1:1          |
| Presentations | landscape   | 16:9         |

## Duration Recommendations

- **10 seconds:** Quick clips, social media snippets, transitions
- **15 seconds:** Standard content, ads, short scenes
- **25 seconds:** Story-driven content, detailed scenes (requires sora-2-pro)

## Common Mistakes to Avoid

1. Too vague: "A nice video" → Be specific about what you want
2. Too complex: Don't try to describe an entire movie in one prompt
3. Real people: Character videos cannot use real human references
4. Wrong model: Remember 25s duration requires sora-2-pro
"""
