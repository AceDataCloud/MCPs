"""Prompt templates for Fish MCP server.

MCP Prompts provide guidance to LLMs on when and how to use the available tools.
These are exposed via the MCP protocol and help LLMs make better decisions.
"""

from core.server import mcp


@mcp.prompt()
def fish_audio_generation_guide() -> str:
    """Guide for choosing the right Fish tool for audio generation."""
    return """# Fish Audio Generation Guide

When the user wants to generate speech or manage voices, choose the appropriate tool:

## Text-to-Speech (Generate Audio)
**Tool:** `fish_generate_audio`
**Use when:**
- User wants to convert text to speech
- User wants to clone a voice with specific text
- User wants to generate audio using a voice ID

**Example:** "Read this text in a calm voice"
-> Call `fish_generate_audio` with prompt="Your text here" and voice_id="d7900c21663f485ab63ebdb7e5905036"

## Create a Custom Voice
**Tool:** `fish_create_voice`
**Use when:**
- User provides an audio URL to clone a voice from
- User wants to register a custom voice
- User wants to create a voice persona

**Example:** "Create a voice from this audio file: [url]"
-> Call `fish_create_voice` with voice_url=url

## Checking Status
**Tool:** `fish_get_task`
**Use when:**
- Generation takes time and user wants to check if it's ready
- User asks "is my audio done?"

## Important Notes:
1. Audio generation is async - generation tools return quickly with a task_id
2. After submit, poll with `fish_get_task` until the final audio URLs are available
3. Generation typically takes a few seconds to a minute
4. The voice_id parameter identifies which voice to use for text-to-speech
5. Use fish_create_voice to register custom voices from audio URLs
"""


@mcp.prompt()
def fish_workflow_examples() -> str:
    """Common workflow examples for Fish audio generation."""
    return """# Fish Workflow Examples

## Workflow 1: Quick Text-to-Speech
1. User: "Say 'Hello world' in a natural voice"
2. Call `fish_generate_audio(prompt="Hello world", voice_id="d7900c21663f485ab63ebdb7e5905036")`
3. Return the task_id from the submission response
4. Poll with `fish_get_task(task_id)` until the completed audio URL is available

## Workflow 2: Custom Voice Cloning
1. User provides audio URL of a voice they want to clone
2. Call `fish_create_voice(voice_url="https://...", title="My Voice", description="Custom voice")`
3. Retrieve the voice_id from the response
4. Use the voice_id in fish_generate_audio for TTS

## Workflow 3: Batch Generation Check
1. Generate multiple audio clips with different prompts
2. Collect all task_ids
3. Use `fish_get_tasks_batch(task_ids=[...])` to check all at once

## Tips:
- Always provide a clear, natural text prompt for best TTS quality
- Use punctuation to control pacing and tone
- For voice cloning, use high-quality audio URLs
- Voice generation typically takes a few seconds
- Use callback_url for async processing in production
"""


@mcp.prompt()
def fish_prompt_suggestions() -> str:
    """Prompt writing suggestions for Fish audio generation."""
    return """# Fish Prompt Writing Guide

## Effective Text-to-Speech Prompts

Good prompts include:
- **Clear text:** Use complete sentences with proper punctuation
- **Tone markers:** Use commas and periods for natural pauses
- **Context:** Provide context for better prosody

## Example Prompts by Use Case

**Announcements:**
"Welcome to our service. We are pleased to assist you today."

**Narration:**
"In the beginning, there was silence. Then, slowly, the world came to life."

**Conversational:**
"Hey there! How are you doing today? It's great to see you."

**Instructions:**
"Please proceed to the next step. Click the button on the right side of the screen."

**Stories:**
"Once upon a time, in a land far away, there lived a brave knight named Arthur."

## Tips for Better Results

1. Use complete sentences for natural-sounding speech
2. Add commas for natural pauses within sentences
3. Use periods for clear sentence breaks
4. Avoid special characters that might confuse the TTS engine
5. Keep individual segments focused — one idea per generation
6. For long texts, consider splitting into multiple requests
"""
