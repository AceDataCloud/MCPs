"""Prompt templates for Luma MCP server.

MCP Prompts provide guidance to LLMs on when and how to use the available tools.
These are exposed via the MCP protocol and help LLMs make better decisions.
"""

from core.server import mcp


@mcp.prompt()
def luma_video_generation_guide() -> str:
    """Guide for choosing the right Luma tool for video generation."""
    return """# Luma Video Generation Guide

When the user wants to generate video, choose the appropriate tool based on their needs:

## Text to Video (Simple)
**Tool:** `luma_generate_video`
**Use when:**
- User gives a text description: "make me a video of a cat"
- User wants Luma to handle the visuals from scratch
- Quick, prompt-based video creation

**Example:** "Create a video of astronauts in space"
-> Call `luma_generate_video` with prompt="Astronauts floating in space, stars in background, cinematic"

## Image to Video (Reference Images)
**Tool:** `luma_generate_video_from_image`
**Use when:**
- User provides an image URL to animate
- User wants video to start/end with a specific image
- User needs precise visual control

**Example:** "Animate this image: [image_url]"
-> Call `luma_generate_video_from_image` with start_image_url=image_url and appropriate prompt

## Extending Videos
**Tool:** `luma_extend_video` or `luma_extend_video_from_url`
**Use when:**
- User wants to make a video longer
- User wants to continue the motion from an existing video
- Building longer content piece by piece

**Example:** "Continue this video with more action"
-> Call `luma_extend_video` with video_id and new prompt

## Checking Status
**Tool:** `luma_get_task`
**Use when:**
- Generation takes time and user wants to check if it's ready
- User asks "is my video done?"

## Important Notes:
1. Video generation is async in MCP - generation tools should return quickly with a task_id
2. After submit, poll with `luma_get_task` until the final video URLs are available
2. Generation typically takes 1-2 minutes
3. Default aspect ratio is 16:9 (landscape)
4. Use 9:16 for mobile/vertical content
5. Enable loop=true for seamless looping videos
6. Enable enhancement=true for better clarity
"""


@mcp.prompt()
def luma_workflow_examples() -> str:
    """Common workflow examples for Luma video generation."""
    return """# Luma Workflow Examples

## Workflow 1: Quick Video Generation
1. User: "Make me a video of waves on a beach"
2. Call `luma_generate_video(prompt="Ocean waves gently crashing on a sandy beach, sunset, peaceful")`
3. Return the task_id from the submission response
4. Poll with `luma_get_task(task_id)` until the completed video URLs are available

## Workflow 2: Animate an Image
1. User provides image URL
2. Call `luma_generate_video_from_image(prompt="Camera slowly zooming in, gentle movement", start_image_url=user_url)`
3. Return task_id

## Workflow 3: Create Transition Between Two Images
1. User provides two image URLs
2. Call `luma_generate_video_from_image(start_image_url=first_url, end_image_url=second_url, prompt="Smooth morphing transition")`
3. Return task_id

## Workflow 4: Creating a Longer Video
1. Generate initial video with `luma_generate_video`
2. Get the video_id from the result
3. Call `luma_extend_video(video_id=video_id, prompt="Continue the motion...")`
4. Repeat step 3 as needed for longer content

## Workflow 5: Mobile-First Content
1. User wants content for TikTok/Instagram Reels
2. Call `luma_generate_video(prompt="...", aspect_ratio="9:16")`
3. Return task_id

## Tips:
- Always be descriptive in prompts - include motion, style, mood
- Mention camera movements: "zooming in", "panning left", "tracking shot"
- Specify style: "cinematic", "realistic", "dreamy", "dramatic"
- For looping content (GIFs, backgrounds), use loop=true
"""


@mcp.prompt()
def luma_prompt_suggestions() -> str:
    """Prompt writing suggestions for Luma video generation."""
    return """# Luma Prompt Writing Guide

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

## Style Keywords

- **Cinematic:** Movie-like quality, widescreen feel
- **Realistic:** Photo-realistic, natural
- **Artistic:** Stylized, creative interpretation
- **Anime:** Japanese animation style
- **Dreamy:** Soft, ethereal, surreal
- **Dramatic:** High contrast, intense
- **Documentary:** Natural, observational

## Tips for Better Results

1. Be specific about motion - don't just say "a cat", say "a cat slowly walking"
2. Include camera movement for dynamic videos
3. Mention lighting conditions for mood
4. Keep prompts focused - one main action per video
5. Use aspect ratio appropriate for content (16:9 landscape, 9:16 vertical)
"""
