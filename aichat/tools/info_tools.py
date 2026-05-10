"""Informational tools for AiChat API."""

from typing import get_args

from core.server import mcp
from core.types import AiChatModel


def _group_models() -> dict[str, list[str]]:
    groups: dict[str, list[str]] = {
        "OpenAI": [],
        "Anthropic Claude": [],
        "Google Gemini": [],
        "xAI Grok": [],
        "DeepSeek": [],
        "Moonshot Kimi": [],
        "Zhipu GLM": [],
    }

    for model in get_args(AiChatModel):
        if model.startswith(("gpt-", "o")):
            groups["OpenAI"].append(model)
        elif model.startswith("claude-"):
            groups["Anthropic Claude"].append(model)
        elif model.startswith("gemini-"):
            groups["Google Gemini"].append(model)
        elif model.startswith("grok-"):
            groups["xAI Grok"].append(model)
        elif model.startswith("deepseek-"):
            groups["DeepSeek"].append(model)
        elif model.startswith("kimi-"):
            groups["Moonshot Kimi"].append(model)
        elif model.startswith("glm-"):
            groups["Zhipu GLM"].append(model)

    return groups


@mcp.tool()
async def aichat_list_models() -> str:
    """List all available AI models for the AiChat API.

    Returns a comprehensive list of supported models grouped by provider,
    including GPT-4/5, o-series, DeepSeek, Grok, and GLM models.

    Returns:
        Formatted list of available models with descriptions.
    """
    groups = _group_models()
    sections = ["# Available AiChat Models", ""]
    for heading, models in groups.items():
        if not models:
            continue
        sections.append(f"## {heading}")
        sections.extend(f"- {model}" for model in models)
        sections.append("")
    return "\n".join(sections).rstrip()


@mcp.tool()
async def aichat_get_usage_guide() -> str:
    """Get a comprehensive guide for using the AiChat tools.

    Provides detailed information on how to use the AiChat tools effectively,
    including parameters, examples, and best practices.

    Returns:
        Complete usage guide for AiChat tools.
    """
    return """# AiChat Tools Usage Guide

## Available Tools

### aichat_create_conversation
Create, retrieve, list, update, or delete AiChat conversations.

**Parameters:**
- `question` (optional): Legacy plain-text prompt for chat requests.
- `model` (optional): The AI model to use. Default: `gpt-4.1`
- `conversation_id` (optional): Conversation ID used for resume, retrieve, update, or delete actions.
- `preset` (optional): Preset model configuration name.
- `stateful` (optional): Persist the conversation when supported by the API.
- `references` (optional): List of reference sources for context.
- `action` (optional): One of `chat`, `retrieve`, `retrieve_batch`, `update`, or `delete`.
- `message` (optional): Multimodal user content as a string or content-block array.
- `max_turns` (optional): Cap the number of agentic-loop iterations.
- `tool_results` (optional): Resume payload for `ask_user_question` flows.
- `messages` / `title` (optional): Fields used by `update` actions.
- `user_id` / `application_id` / `model_group` / `offset` / `limit` (optional): Filters for `retrieve_batch`.

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

### Send a Multimodal Message
```
aichat_create_conversation(
    model="gpt-4o-image",
    message=[
        {"type": "text", "text": "Describe this image."},
        {"type": "image_url", "image_url": {"url": "https://example.com/image.png"}}
    ]
)
```

### List Conversations
```
aichat_create_conversation(
    action="retrieve_batch",
    model="claude-sonnet-4-6",
    model_group="claude",
    limit=20
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

## Response Structure

### Successful Response
- **id**: Unique conversation identifier (use to continue the conversation)
- **answer**: The generated response from the AI model

### Error Response
- **error.code**: Error code (e.g., `api_error`, `invalid_token`)
- **error.message**: Human-readable error description
- **trace_id**: Request trace ID for debugging

## Notes
- The `conversation_id` from the response can be used to continue or manage the conversation
- Use `message` when you need image or file inputs
- Use reasoning models (o1, o3, o4-mini) for complex math or logic problems
- Bearer token authentication is required
"""
