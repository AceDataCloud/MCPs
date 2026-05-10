"""Informational tools for Fish API."""

from core.server import mcp


@mcp.tool()
async def fish_list_models() -> str:
    """List all available models for Fish audio generation.

    Shows all available model options with their descriptions and use cases.
    Use this to understand which model to choose for your audio generation.

    Returns:
        Table of all models with their descriptions and use cases.
    """
    # Last updated: 2026-05-10
    return """Available Fish TTS Models:

| Model     | Description                                          |
|-----------|------------------------------------------------------|
| fish-tts  | Fish text-to-speech model for voice cloning (default)|

Recommended:
- Use fish-tts for all text-to-speech and voice cloning tasks
"""


@mcp.tool()
async def fish_list_actions() -> str:
    """List all available Fish API actions and corresponding tools.

    Reference guide for what each action does and which tool to use.
    Helpful for understanding the full capabilities of the Fish MCP.

    Returns:
        Categorized list of all actions and their corresponding tools.
    """
    # Last updated: 2026-05-10
    return """Available Fish Actions and Tools:

Audio Generation:
- fish_generate_audio: Convert text to speech using a voice ID

Voice Management:
- fish_create_voice: Create a custom voice by cloning from an audio URL

Task Management:
- fish_get_task: Check status of a single generation
- fish_get_tasks_batch: Check status of multiple generations

Information:
- fish_list_models: Show available TTS models
- fish_list_actions: Show this action reference (you are here)

Workflow Examples:
1. Text to speech: fish_generate_audio -> fish_get_task
2. Custom voice: fish_create_voice -> fish_generate_audio -> fish_get_task
3. Batch check: fish_generate_audio (multiple) -> fish_get_tasks_batch

Tips:
- Use descriptive, natural text for best TTS quality
- Include punctuation to control pacing and pauses
- Audio generation typically takes a few seconds to a minute
- Use callback_url for async processing in production
- Use fish_create_voice to register custom voices before using them in TTS
"""
