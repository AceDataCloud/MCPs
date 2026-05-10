"""Prompt templates for Fish MCP server.

MCP Prompts provide guidance to LLMs on when and how to use the available tools.
These are exposed via the MCP protocol and help LLMs make better decisions.
"""

from core.server import mcp


@mcp.prompt()
def fish_guide() -> str:
    """Guide for choosing the right Fish TTS tool."""
    return """# Fish TTS Guide

When the user wants to generate speech or inspect voice models, use the appropriate tool:

## Text-to-Speech Generation
**Tool:** `fish_generate_audio`
**Use when:**
- User wants to convert text to speech
- User wants audio narration
- User needs TTS with a specific voice

**Example:** "Convert this text to speech: 'Hello World'"
→ Call `fish_generate_audio` with text="Hello World" and optional reference_id

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
- User wants to browse available voice models

**Tool:** `fish_get_model`
**Use when:**
- User asks for details about a specific model ID
- User already has a model ID from `fish_list_models`

## Usage Guide
**Tool:** `fish_get_usage_guide`
**Use when:**
- User wants to understand how to use the tools
- User needs examples or workflow guidance

## Important Notes:
1. text is required for fish_generate_audio
2. reference_id is optional for voice conditioning
3. Tasks may be asynchronous — poll fish_get_task until state='complete'
4. Bearer token authentication is required
"""


@mcp.prompt()
def fish_workflow_examples() -> str:
    """Common workflow examples for Fish TTS tasks."""
    return """# Fish TTS Workflow Examples

## Workflow 1: Quick Text-to-Speech
1. User: "Say 'Hello World' in a specific voice"
2. Call `fish_generate_audio(text="Hello World", reference_id="d7900c21663f485ab63ebdb7e5905036")`
3. If task_id is returned, poll `fish_get_task` until complete
4. Return the audio URL to the user

## Workflow 2: Browse Models then Synthesize
1. User: "Find a model and use it to read this text"
2. Call `fish_list_models(language="en")`
3. Pick a model and call `fish_get_model(model_id="...")` if details are needed
4. Call `fish_generate_audio(text="...", reference_id=<model_id>)`
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
- Use fish_list_models / fish_get_model to discover available model IDs
"""
