"""Informational tools for AiChat API."""

from core.server import mcp


@mcp.tool()
async def aichat_list_models() -> str:
    """List all available AI models for the AiChat API.

    Returns a comprehensive list of supported models grouped by provider,
    including GPT-4/5, o-series, DeepSeek, Grok, and GLM models.

    Returns:
        Formatted list of available models with descriptions.
    """
    # Last updated: 2026-04-25
    return """# Available AiChat Models

## OpenAI GPT-5 Series
- gpt-5.5
- gpt-5.5-pro
- gpt-5.4
- gpt-5.4-pro
- gpt-5.2
- gpt-5.1
- gpt-5.1-all
- gpt-5
- gpt-5-mini
- gpt-5-nano
- gpt-5-all

## OpenAI GPT-4.1 Series
- gpt-4.1 (recommended default)
- gpt-4.1-2025-04-14
- gpt-4.1-mini
- gpt-4.1-mini-2025-04-14
- gpt-4.1-nano
- gpt-4.1-nano-2025-04-14

## OpenAI GPT-4.5 Series
- gpt-4.5-preview
- gpt-4.5-preview-2025-02-27

## OpenAI GPT-4o Series
- gpt-4o
- gpt-4o-2024-05-13
- gpt-4o-2024-08-06
- gpt-4o-2024-11-20
- gpt-4o-all
- gpt-4o-image
- gpt-4o-mini
- gpt-4o-mini-2024-07-18
- gpt-4o-mini-search-preview
- gpt-4o-mini-search-preview-2025-03-11
- gpt-4o-search-preview
- gpt-4o-search-preview-2025-03-11

## OpenAI GPT-4 Series
- gpt-4
- gpt-4-all
- gpt-4-turbo
- gpt-4-turbo-preview
- gpt-4-vision-preview

## OpenAI o-Series (Reasoning)
- o1
- o1-2024-12-17
- o1-all
- o1-mini
- o1-mini-2024-09-12
- o1-mini-all
- o1-preview
- o1-preview-2024-09-12
- o1-preview-all
- o1-pro
- o1-pro-2025-03-19
- o1-pro-all
- o3
- o3-2025-04-16
- o3-all
- o3-mini
- o3-mini-2025-01-31
- o3-mini-2025-01-31-high
- o3-mini-2025-01-31-low
- o3-mini-2025-01-31-medium
- o3-mini-all
- o3-mini-high
- o3-mini-high-all
- o3-mini-low
- o3-mini-medium
- o3-pro
- o3-pro-2025-06-10
- o4-mini
- o4-mini-2025-04-16
- o4-mini-all
- o4-mini-high-all

## DeepSeek
- deepseek-r1
- deepseek-r1-0528
- deepseek-v3
- deepseek-v3-250324

## xAI Grok
- grok-3

## Zhipu GLM
- glm-5.1
- glm-4.7
- glm-4.6
- glm-4.5-air
- glm-3-turbo
"""


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
