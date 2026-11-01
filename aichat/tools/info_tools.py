"""Informational tools for AiChat API."""

from typing import get_args

from core.server import mcp
from core.types import DEFAULT_MODEL, DEFAULT_V2_MODEL, AiChatModel, AiChatV2Model


@mcp.tool()
async def aichat_list_models() -> str:
    """List all available AI models for the AiChat API.

    Returns a comprehensive list of supported models grouped by provider,
    including GPT-4/5, o-series, DeepSeek, Grok, and GLM models.

    Returns:
        Formatted list of available models with descriptions.
    """
    v1_models = "\n".join(f"- {model}" for model in get_args(AiChatModel))
    v2_models = "\n".join(f"- {model}" for model in get_args(AiChatV2Model))
    return (
        "# Available AiChat Models\n\n"
        f"## aichat_create_conversation (default: {DEFAULT_MODEL})\n{v1_models}\n\n"
        f"## aichat_create_conversation_v2 (default: {DEFAULT_V2_MODEL})\n{v2_models}\n\n"
        "## Gemini endpoint coverage\n"
        "gemini-3.8-flash is available through both tools. gemini-4-argon requires "
        "aichat_create_conversation_v2. Use the exact endpoint model list above.\n\n"
        "## Kimi (AiChat v2 only)\n"
        "Kimi models require aichat_create_conversation_v2. The default remains gpt-4.1.\n"
        "\n## Xiaomi MiMo (prepared; not yet available)\n"
        "mimo-v2.6-pro and mimo-v2.6-flash are staged for text chat and function tools. "
        "Check the live catalog and account access before using them. "
        "Do not select them automatically while unavailable.\n"
    )


@mcp.tool()
async def aichat_get_usage_guide() -> str:
    """Get a comprehensive guide for using the AiChat tools.

    Provides detailed information on how to use the AiChat tools effectively,
    including parameters, examples, and best practices.

    Returns:
        Complete usage guide for AiChat tools.
    """
    # Last updated: 2026-04-25
    return """# AiChat Tools Usage Guide

## Available Tools

### aichat_create_conversation
Create an AI conversation with any supported model.

**Parameters:**
- `question` (required): The prompt or question to ask the AI model.
- `model` (optional): The AI model to use. Default: `gpt-4.1`
- `conversation_id` (optional): Continue an existing conversation by providing its ID.
- `preset` (optional): Preset model configuration name.
- `stateful` (optional): Enable stateful conversation mode (boolean).
- `references` (optional): List of reference sources for context.

### aichat_create_conversation_v2
Create/manage conversations via `/aichat2/conversations`.

**Common parameters:**
- `model` (required): Model to use.
- `action` (optional): `chat` (default), `retrieve`, `retrieve_batch`, `update`, `delete`.
- `id` (optional): Conversation ID for retrieve/update/delete.
- `question` (optional): Prompt for chat action.
- `messages` (optional): Messages payload for update/action workflows.
- `async` (optional): Process the request asynchronously.
- `callback_url` (optional): Webhook URL for async completion callbacks.
- `allowed_skills` / `allowed_mcp_servers` (optional): Restrict agent capabilities for async runs.
- `unattended_policy` (optional): Policy object controlling unattended execution.

### aichat_list_models
List all available AI models grouped by provider.

### aichat_get_usage_guide
Show this usage guide.

## Example Usage

### Simple Question
```
aichat_create_conversation(
    question="What is the capital of France?",
    model="gpt-4.1"
)
```

**Response:**
```json
{
  "id": "64a67fff-61dc-4801-8339-2c69334c61d6",
  "answer": "The capital of France is Paris."
}
```

### Continue a Conversation
```
aichat_create_conversation(
    question="Tell me more about it.",
    model="gpt-4.1",
    conversation_id="64a67fff-61dc-4801-8339-2c69334c61d6"
)
```

### Use a Reasoning Model
```
aichat_create_conversation(
    question="Solve this step by step: If x^2 + 5x + 6 = 0, find x.",
    model="o3-mini"
)
```

### Use DeepSeek
```
aichat_create_conversation(
    question="Explain quantum entanglement.",
    model="deepseek-r1"
)
```

### Use Gemini 4 Argon with AiChat v2
```
aichat_create_conversation_v2(
    question="Review this code and identify its key risks.",
    model="gemini-4-argon"
)
```

This uses `/aichat2/conversations`, not native Gemini Generate Content or Google
Interactions. It does not expose `max_tokens`, thinking-level or explicit-cache
controls. The v1 tool does not accept this model; the default remains `gpt-4.1`.

### Use Kimi with AiChat v2
```
aichat_create_conversation_v2(
    question="Review this code and identify its key risks.",
    model="kimi-k3.1-pro"
)
```

`kimi-k3` remains supported by v2. This tool uses `/aichat2/conversations`,
not `/kimi/chat/completions`; it does not expose `reasoning_effort`.

## Response Structure

### Successful Response
- **id**: Unique conversation identifier (use to continue the conversation)
- **answer**: The generated response from the AI model

### Error Response
- **error.code**: Error code (e.g., `api_error`, `invalid_token`)
- **error.message**: Human-readable error description
- **trace_id**: Request trace ID for debugging

## Notes
- The `conversation_id` from the response can be used to continue the conversation
- Use reasoning models (o1, o3, o4-mini) for complex math or logic problems
- Use DeepSeek models for tasks requiring deep reasoning
- Use search-preview models for questions requiring web search
- Bearer token authentication is required
"""
