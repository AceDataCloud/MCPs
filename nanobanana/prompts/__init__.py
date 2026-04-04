"""Prompt templates for NanoBanana MCP server.

MCP Prompts provide guidance to LLMs on when and how to use the available tools.
These are exposed via the MCP protocol and help LLMs make better decisions.
"""

from core.server import mcp


@mcp.prompt()
def nanobanana_image_generation_guide() -> str:
    """Guide for choosing the right NanoBanana tool for image tasks."""
    return """# NanoBanana Image Generation Guide

When the user wants to generate or edit images, choose the appropriate tool based on their needs:

## Image Generation (From Text)
**Tool:** `nanobanana_generate_image`
**Use when:**
- User wants to create a new image from a text description
- No existing images are involved
- User describes a scene, object, person, or concept

**Example:** "Create a photorealistic image of a cat in a garden"
→ Call `nanobanana_generate_image` with a detailed prompt

## Image Editing (From Existing Images)
**Tool:** `nanobanana_edit_image`
**Use when:**
- User has one or more existing images to modify
- User wants to combine multiple images
- Virtual try-on (person + clothing)
- Product placement in scenes
- Style or attribute changes

**Example:** "Put this shirt on this model"
→ Call `nanobanana_edit_image` with both image URLs and a descriptive prompt

## Checking Results
**Tool:** `nanobanana_get_task`
**Use when:**
- User wants to check if generation is complete
- User asks "is my image ready?"

## Batch Status Check
**Tool:** `nanobanana_get_tasks_batch`
**Use when:**
- Multiple images were generated
- User wants status of several tasks at once

## Important Notes:
1. Image generation is async in MCP - generation tools should return quickly with a task_id
2. After generate/edit submission, poll with `nanobanana_get_task` until the final image URLs are available
2. Detailed prompts produce better results
3. Include: subject, atmosphere, lighting, camera style, quality keywords
4. For edit operations, image_urls must be publicly accessible
5. Base64 encoded images are also supported
"""


@mcp.prompt()
def nanobanana_prompt_writing_guide() -> str:
    """Guide for writing effective image generation prompts."""
    return """# NanoBanana Prompt Writing Guide

## Effective Prompt Structure

A good prompt includes these elements:
- **Main Subject:** What is the primary focus of the image?
- **Atmosphere:** What mood or feeling should the image convey?
- **Lighting:** How is the scene illuminated?
- **Camera/Lens:** What photographic style? (85mm portrait, wide-angle, macro, etc.)
- **Quality Keywords:** Technical quality descriptors (bokeh, film grain, HDR, etc.)

## Example Prompts by Category

### Portrait Photography
"A photorealistic close-up portrait of an elderly Japanese ceramicist with deep, sun-etched wrinkles and a warm, knowing smile. Soft golden hour light streaming through a window. Captured with an 85mm portrait lens, soft bokeh background. Serene and masterful mood."

### Product Photography
"White porcelain coffee cup on a marble surface, morning window light, 85mm portrait lens, shallow depth of field, soft highlights, clean and minimal aesthetic."

### Lifestyle/Scene
"Urban career woman walking through a subway station, backlit by morning sunlight, film grain, orange-gold tones, hopeful dawn atmosphere."

### Artistic/Creative
"Surreal floating islands with waterfalls cascading into clouds, magical golden hour lighting, fantasy art style, ultra-detailed, dreamlike atmosphere."

## Tips for Better Results

1. **Be Specific:** "elderly Japanese ceramicist" is better than "old man"
2. **Describe Lighting:** "soft golden hour light" is better than "good lighting"
3. **Include Camera Details:** Lens type and settings add realism
4. **Set the Mood:** Words like "serene", "dramatic", "hopeful" guide the style
5. **Quality Keywords:** "photorealistic", "ultra-detailed", "professional" help quality

## Common Use Cases

### Virtual Try-On (Edit Mode)
Prompt: "Let this person wear this clothing naturally, matching lighting and perspective"
Images: [person photo URL, clothing photo URL]

### Product Scene Placement (Edit Mode)
Prompt: "Place this product in a modern minimalist kitchen, natural morning light"
Images: [product on white background URL]

### Style Transfer (Edit Mode)
Prompt: "Transform this photo into a watercolor painting style"
Images: [original photo URL]
"""


@mcp.prompt()
def nanobanana_workflow_examples() -> str:
    """Common workflow examples for NanoBanana image generation."""
    return """# NanoBanana Workflow Examples

## Workflow 1: Simple Image Generation
1. User: "Create an image of a sunset over mountains"
2. Call `nanobanana_generate_image(prompt="Breathtaking sunset over mountain range, dramatic orange and purple sky, alpine peaks, landscape photography, wide-angle lens, HDR, golden hour lighting")`
3. Return the task_id from the submission response
4. Poll with `nanobanana_get_task(task_id)` until the final image URLs are available

## Workflow 2: Virtual Try-On
1. User provides: person photo URL + clothing photo URL
2. Call `nanobanana_edit_image(prompt="Let this person wear this clothing naturally", image_urls=[person_url, clothing_url])`
3. Poll with `nanobanana_get_task(task_id)` for the completed edit result

## Workflow 3: Product Photography
1. User has a product on white background
2. Call `nanobanana_edit_image(prompt="Place this product in a luxurious marble bathroom setting, soft natural lighting", image_urls=[product_url])`
3. Poll with `nanobanana_get_task(task_id)` for the completed scene

## Workflow 4: Batch Image Generation
1. Generate multiple variations
2. Collect all task_ids
3. Use `nanobanana_get_tasks_batch(task_ids=[...])` to check all at once

## Workflow 5: Async with Callback
1. User provides a callback URL for webhook
2. Call tool with `callback_url` parameter
3. API immediately returns task_id
4. Result will be POSTed to callback URL when ready

## Tips:
- Always use descriptive, detailed prompts
- For edit operations, ensure image URLs are publicly accessible
- Store task_ids for later status checking
- Consider using callbacks for long-running operations
"""
