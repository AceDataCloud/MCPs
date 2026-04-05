"""Prompt templates for Wan MCP server.

MCP Prompts provide guidance to LLMs on when and how to use the available tools.
These are exposed via the MCP protocol and help LLMs make better decisions.
"""

from core.server import mcp


@mcp.prompt()
def wan_video_generation_guide() -> str:
    """Guide for choosing the right Wan tool for video generation."""
    return """# Wan Video Generation Guide

When the user wants to generate video, choose the appropriate tool based on their needs:

## Text to Video
**Tool:** `wan_generate_video`
**Use when:**
- User gives a text description: "make me a video of a cat"
- User wants to create video from scratch without reference images
- Quick, prompt-based video creation

**Example:** "Create a video of astronauts in space"
-> Call `wan_generate_video` with prompt="Astronauts floating in space, stars in background, cinematic"

## Image to Video
**Tool:** `wan_generate_video_from_image`
**Use when:**
- User provides an image URL to animate
- User wants video based on a reference image
- User needs character/timbre extraction (wan2.6-r2v model)

**Example:** "Animate this image: [image_url]"
-> Call `wan_generate_video_from_image` with image_url and appropriate prompt

## Checking Status
**Tool:** `wan_get_task`
**Use when:**
- Generation takes time and user wants to check if it's ready
- User asks "is my video done?"

## Important Notes:
1. Video generation is async - tools return quickly with a task_id
2. After submit, poll with `wan_get_task` until the final video URLs are available
3. Generation typically takes 2-5 minutes
4. Default resolution is 720P
5. Available resolutions: 480P (draft), 720P (default), 1080P (high quality)
6. Duration options: 5s, 10s, or 15s
7. Use prompt_extend=true for AI-enhanced prompts
8. Use audio=true to generate video with sound

## Model Selection:
- wan2.6-t2v: Text-to-video only (use wan_generate_video)
- wan2.6-i2v: Standard image-to-video (use wan_generate_video_from_image)
- wan2.6-r2v: Reference video-to-video with character extraction
- wan2.6-i2v-flash: Fast image-to-video (lower quality but faster)
"""


@mcp.prompt()
def wan_workflow_examples() -> str:
    """Common workflow examples for Wan video generation."""
    return """# Wan Workflow Examples

## Workflow 1: Quick Video Generation
1. User: "Make me a video of waves on a beach"
2. Call `wan_generate_video(prompt="Ocean waves gently crashing on a sandy beach, sunset, peaceful")`
3. Return the task_id from the submission response
4. Poll with `wan_get_task(task_id)` until the completed video URLs are available

## Workflow 2: Animate an Image
1. User provides image URL
2. Call `wan_generate_video_from_image(prompt="Camera slowly zooming in, gentle movement", image_url=user_url)`
3. Return task_id

## Workflow 3: High Quality Video
1. User wants professional quality
2. Call `wan_generate_video(prompt="...", resolution="1080P", duration=15)`
3. Return task_id

## Workflow 4: Fast Preview
1. User wants a quick draft
2. Call `wan_generate_video_from_image(prompt="...", image_url=url, model="wan2.6-i2v-flash")`
3. Return task_id

## Workflow 5: Video with Sound
1. User wants video with audio
2. Call `wan_generate_video(prompt="...", audio=true)`
3. Return task_id

## Workflow 6: Character Transfer
1. User has a reference video with a character they want to transfer
2. Call `wan_generate_video_from_image(prompt="...", image_url=url, model="wan2.6-r2v", reference_video_urls="video1_url,video2_url")`
3. Return task_id

## Tips:
- Always be descriptive in prompts - include motion, style, mood
- Mention camera movements: "zooming in", "panning left", "tracking shot"
- Specify style: "cinematic", "realistic", "dreamy", "dramatic"
- Use negative_prompt to exclude unwanted content
- Use 480P for draft previews, 720P for general use, 1080P for final output
"""


@mcp.prompt()
def wan_prompt_suggestions() -> str:
    """Prompt writing suggestions for Wan video generation."""
    return """# Wan Prompt Writing Guide

## Effective Prompt Elements

Good prompts include:
- **Subject:** What is the main focus? (person, animal, object, scene)
- **Motion:** What movement happens? (walking, flying, zooming, panning)
- **Style:** What's the visual style? (cinematic, realistic, artistic, anime)
- **Mood:** What's the atmosphere? (peaceful, dramatic, mysterious, joyful)
- **Setting:** Where does it take place? (beach, city, forest, space)
- **Lighting:** What's the light like? (sunset, golden hour, neon, dramatic)

## Example Prompts by Category

**Nature:**
"Ocean waves crashing on rocky cliffs at sunset, dramatic lighting, cinematic, slow motion"

**Animals:**
"A majestic lion walking through the savanna, golden hour lighting, documentary style"

**Urban:**
"Busy city street at night, neon lights reflecting on wet pavement, cyberpunk aesthetic"

**Space:**
"Astronauts floating in zero gravity inside a space station, Earth visible through window"

**Fantasy:**
"A magical forest with glowing fireflies, mist rising from the ground, ethereal atmosphere"

**Action:**
"Sports car racing through mountain roads, tracking shot, cinematic, fast motion"

## Motion Keywords

Camera movements:
- "zooming in/out" - Changes focal distance
- "panning left/right" - Horizontal camera rotation
- "tilting up/down" - Vertical camera rotation
- "tracking shot" - Camera follows subject
- "dolly shot" - Camera moves toward/away from subject
- "aerial view" - Bird's eye perspective

Subject movements:
- "walking", "running", "flying", "swimming"
- "dancing", "jumping", "falling", "rising"
- "morphing", "transforming", "dissolving"

## Tips for Better Results

1. Be specific about motion - don't just say "a cat", say "a cat slowly walking"
2. Include camera movement for dynamic videos
3. Mention lighting conditions for mood
4. Keep prompts focused - one main action per video
5. Use resolution appropriate for content (480P draft, 720P general, 1080P final)
6. Use prompt_extend=true for AI-enhanced descriptions
7. Use negative_prompt to avoid unwanted elements
"""
