"""Informational tools for AiChat API."""

from typing import get_args

from core.server import mcp
from core.types import AiChatModel


@mcp.tool()
async def aichat_list_models() -> str:
    """List all available AI models for the AiChat API.

    Returns a comprehensive list of supported models grouped by provider,
    including GPT-4/5, o-series, DeepSeek, Grok, and GLM models.

    Returns:
        Formatted list of available models with descriptions.
    """
    model_lines = "\n".join(f"- {model}" for model in get_args(AiChatModel))
    return f"# Available AiChat Models\n\n{model_lines}"


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
Create an AI conversation with any supported model.

**Parameters:**
- `question` (required): The prompt or question to ask the AI model.
- `message` (optional): Multi-modal message content for chat turns.
- `model` (optional): The AI model to use. Default: `gpt-4.1`
- `action` (optional): One of `chat`, `retrieve`, `retrieve_batch`, `update`, `delete`.
- `conversation_id` (optional): Continue an existing conversation by providing its ID.
- `preset` (optional): Preset model configuration name.
- `stateful` (optional): Enable stateful conversation mode (boolean).
- `references` (optional): List of reference sources for context.
- `max_turns`, `tool_results`, `messages`, `title`, `user_id`, `application_id`, `model_group`, `offset`, `limit` (optional): Advanced fields for v2 endpoint behavior.

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
