"""Prompt templates for Fish MCP server.

MCP Prompts provide guidance to LLMs on when and how to use the available tools.
These are exposed via the MCP protocol and help LLMs make better decisions.
"""

from core.server import mcp


@mcp.prompt()
def fish_guide() -> str:
    """Guide for choosing the right Fish TTS tool."""
    return """# Fish TTS Guide

When the user wants to generate speech or clone a voice, use the appropriate tool:

## Text-to-Speech Generation
**Tool:** `fish_generate_audio`
**Use when:**
- User wants to convert text to speech
- User wants audio narration
- User needs TTS with a specific voice

**Example:** "Convert this text to speech: 'Hello World'"
→ Call `fish_generate_audio` with prompt="Hello World" and a voice_id

## Voice Cloning
**Tool:** `fish_create_voice`
**Use when:**
- User has an audio sample and wants to clone the voice
- User wants a custom voice for future TTS requests
- User provides a URL to an audio recording

**Example:** "Clone this voice from my recording: https://example.com/sample.mp3"
→ Call `fish_create_voice` with voice_url="https://example.com/sample.mp3"

## Check Task Status
**Tool:** `fish_get_task`
**Use when:**
- User wants to check if a generation task is complete
- A previous call returned a task_id
- You need to poll for the final audio URL

## Check Multiple Tasks
**Tool:** `fish_get_tasks_batch`
**Use when:**
- User has multiple pending tasks to check
- You want to check several tasks at once

## Model Information
**Tool:** `fish_list_models`
**Use when:**
- User asks what models are available
- User wants to know about Fish TTS capabilities

## Usage Guide
**Tool:** `fish_get_usage_guide`
**Use when:**
- User wants to understand how to use the tools
- User needs examples or workflow guidance

## Important Notes:
1. voice_id is required for fish_generate_audio
2. Use fish_create_voice to create a custom voice_id from an audio sample
3. Tasks may be asynchronous — poll fish_get_task until state='complete'
4. Bearer token authentication is required
"""


@mcp.prompt()
def fish_workflow_examples() -> str:
    """Common workflow examples for Fish TTS tasks."""
    return """# Fish TTS Workflow Examples

## Workflow 1: Quick Text-to-Speech
1. User: "Say 'Hello World' in a specific voice"
2. Call `fish_generate_audio(prompt="Hello World", voice_id="d7900c21663f485ab63ebdb7e5905036")`
3. If task_id is returned, poll `fish_get_task` until complete
4. Return the audio URL to the user

## Workflow 2: Clone a Voice then Use It
1. User: "Clone my voice from this recording and use it to read this text"
2. Call `fish_create_voice(voice_url="https://example.com/my-recording.mp3", title="My Voice")`
3. Get the voice_id from the response
4. Call `fish_generate_audio(prompt="...", voice_id=<new_voice_id>)`
5. Poll for completion and return the audio URL

## Workflow 3: Batch Task Monitoring
1. User starts multiple TTS generations
2. Collect all task_ids
3. Call `fish_get_tasks_batch(task_ids=[...])`
4. Report status of all tasks at once

## Tips:
- Always check task state before presenting results
- state='complete' means the audio is ready
- state='pending' or 'processing' means keep polling
- Use fish_create_voice to get custom voice_ids
"""
