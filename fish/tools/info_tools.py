"""Informational tools for Fish API."""

from core.server import mcp


@mcp.tool()
async def fish_get_usage_guide() -> str:
    """Get a comprehensive guide for using the Fish TTS tools.

    Provides detailed information on how to use the Fish tools effectively,
    including parameters, examples, and best practices.

    Returns:
        Complete usage guide for Fish TTS tools.
    """
    # Last updated: 2026-05-10
    return """# Fish TTS Tools Usage Guide

## Available Tools

### Audio Generation
**fish_generate_audio** - Convert text to speech using a voice
- prompt: The text to convert to speech (required)
- voice_id: The voice ID to use (required)
- action: "speech" (required, default)
- model: "fish-tts" (optional, default)
- callback_url: Async callback URL (optional)

### Voice Cloning
**fish_create_voice** - Clone a voice from an audio sample
- voice_url: Public URL of an audio sample (required)
- title: Name for the voice (optional)
- description: Description of the voice (optional)
- image_url: Cover image URL for the voice (optional)
- callback_url: Async callback URL (optional)

### Task Status
**fish_get_task** - Check status of a single task
- task_id: The task ID from a generation request (required)

**fish_get_tasks_batch** - Check status of multiple tasks
- task_ids: List of task IDs (required)

## Example Usage

### Generate Speech
```
fish_generate_audio(
    prompt="Hello, welcome to our service!",
    voice_id="d7900c21663f485ab63ebdb7e5905036"
)
```

### Clone a Voice
```
fish_create_voice(
    voice_url="https://example.com/my-voice-sample.mp3",
    title="My Custom Voice"
)
```

### Check Task Status
```
fish_get_task(task_id="93f11baf-347b-4bb4-9520-8653cb46d6a3")
```

## Workflow: Async Generation

For long-running tasks, the API may return a task_id immediately.
Poll fish_get_task until the state is 'complete':

1. Call fish_generate_audio → get task_id
2. Call fish_get_task(task_id=...) repeatedly
3. When state='complete', retrieve the audio URL from the response

## Response Structure

### Successful Response
- **success**: `true` - request was successful
- **task_id**: Task ID for polling
- **data**: Array of result items with audio URLs or voice IDs

### Error Response
- **error.code**: Error code (e.g., `bad_request`, `invalid_token`)
- **error.message**: Human-readable error description
- **trace_id**: Request trace ID for debugging
"""


@mcp.tool()
async def fish_list_models() -> str:
    """List available Fish TTS models.

    Returns information about the supported models for Fish TTS.

    Returns:
        List of available Fish TTS models with descriptions.
    """
    # Last updated: 2026-05-10
    return """# Available Fish TTS Models

## Models

| Model     | Description                                      | Default |
|-----------|--------------------------------------------------|---------|
| fish-tts  | Fish Audio TTS model with voice cloning support  | ✓       |

## Notes
- Currently only `fish-tts` is supported
- The model supports voice cloning via voice_id
- Use fish_create_voice to create custom voice IDs
"""
