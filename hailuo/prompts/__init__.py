"""Prompt templates for Hailuo MCP server.

MCP Prompts provide guidance to LLMs on when and how to use the available tools.
These are exposed via the MCP protocol and help LLMs make better decisions.
"""

from core.server import mcp


@mcp.prompt()
def hailuo_video_generation_guide() -> str:
    """Guide for choosing the right Hailuo tool for video generation."""
    return """# Hailuo Video Generation Guide

When the user wants to generate video, choose the appropriate tool based on their needs:

## Text to Video (Simple)
**Tool:** `hailuo_generate_video`
**Use when:**
- User gives a text description: "make me a video of a cat"
- User wants Hailuo to handle the visuals from scratch
- Quick, prompt-based video creation

**Example:** "Create a video of astronauts in space"
-> Call `hailuo_generate_video` with prompt="Astronauts floating in space, stars in background, cinematic"

## Image to Video (Reference Image)
**Tool:** `hailuo_generate_video_from_image`
**Use when:**
- User provides an image URL to animate
- User wants video generated from a specific image
- User needs image-to-video generation

**Example:** "Animate this image: [image_url]"
-> Call `hailuo_generate_video_from_image` with first_image_url=image_url and appropriate prompt

## Choosing the Right Model
- **minimax-t2v:** Default text-to-video model. Use for pure text prompts.
- **minimax-i2v:** Image-to-video model. Requires first_image_url.
- **minimax-i2v-director:** Director-mode image-to-video. More creative control. Requires first_image_url.

## Checking Status
**Tool:** `hailuo_get_task`
**Use when:**
- Generation takes time and user wants to check if it's ready
- User asks "is my video done?"

## Important Notes:
1. Video generation is async in MCP - generation tools should return quickly with a task_id
2. After submit, poll with `hailuo_get_task` until the final video URLs are available
3. Generation typically takes 1-3 minutes
4. minimax-i2v and minimax-i2v-director models REQUIRE a first_image_url parameter
5. Use minimax-t2v (default) for text-only video generation
"""


@mcp.prompt()
def hailuo_workflow_examples() -> str:
    """Common workflow examples for Hailuo video generation."""
    return """# Hailuo Workflow Examples

## Workflow 1: Quick Text-to-Video
1. User: "Make me a video of waves on a beach"
2. Call `hailuo_generate_video(prompt="Ocean waves gently crashing on a sandy beach, sunset, peaceful")`
3. Return the task_id from the submission response
4. Poll with `hailuo_get_task(task_id)` until the completed video URLs are available

## Workflow 2: Animate an Image
1. User provides image URL
2. Call `hailuo_generate_video_from_image(prompt="Camera slowly zooming in, gentle movement", first_image_url=user_url, model="minimax-i2v")`
3. Return task_id

## Workflow 3: Director-Mode Image-to-Video
1. User provides image URL and wants creative control
2. Call `hailuo_generate_video_from_image(prompt="Dynamic camera movement, dramatic lighting transition", first_image_url=user_url, model="minimax-i2v-director")`
3. Return task_id

## Workflow 4: Batch Generation
1. Generate multiple videos with different prompts
2. Collect all task_ids
3. Use `hailuo_get_tasks_batch(task_ids=[...])` to check all at once

## Tips:
- Always be descriptive in prompts - include motion, style, mood
- Mention camera movements: "zooming in", "panning left", "tracking shot"
- Specify style: "cinematic", "realistic", "dreamy", "dramatic"
- For image-to-video, describe the desired motion and transformation
"""


@mcp.prompt()
def hailuo_prompt_suggestions() -> str:
    """Prompt writing suggestions for Hailuo video generation."""
    return """# Hailuo Prompt Writing Guide

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
5. For image-to-video, describe what should change or move in the image
"""
