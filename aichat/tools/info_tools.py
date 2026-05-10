"""Informational tools for AiChat API."""

from core.server import mcp


@mcp.tool()
async def aichat_list_models() -> str:
    """List all available AI models for the AiChat API.

    Returns a comprehensive list of supported models grouped by provider,
    including GPT-4/5, o-series, DeepSeek, Grok, GLM, Claude, Gemini, and Kimi models.

    Returns:
        Formatted list of available models with descriptions.
    """
    # Last updated: 2026-05-10
    return """# Available AiChat Models

## v1 Endpoint (/aichat/conversations) — aichat_create_conversation

### OpenAI GPT-5 Series
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

### OpenAI GPT-4.1 Series
- gpt-4.1 (recommended default)
- gpt-4.1-2025-04-14
- gpt-4.1-mini
- gpt-4.1-mini-2025-04-14
- gpt-4.1-nano
- gpt-4.1-nano-2025-04-14

### OpenAI GPT-4.5 Series
- gpt-4.5-preview
- gpt-4.5-preview-2025-02-27

### OpenAI GPT-4o Series
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

### OpenAI GPT-4 Series
- gpt-4
- gpt-4-all
- gpt-4-turbo
- gpt-4-turbo-preview
- gpt-4-vision-preview

### OpenAI o-Series (Reasoning)
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

### DeepSeek
- deepseek-r1
- deepseek-r1-0528
- deepseek-v3
- deepseek-v3-250324
- deepseek-v4-flash

### xAI Grok
- grok-3

### Zhipu GLM
- glm-5.1
- glm-4.7
- glm-4.6
- glm-4.5-air
- glm-3-turbo

## v2 Endpoint (/aichat2/conversations) — aichat_create_conversation_v2

### OpenAI GPT-4 / GPT-4o / GPT-5
- gpt-4
- gpt-4.1
- gpt-4.1-mini
- gpt-4.1-nano
- gpt-4o
- gpt-4o-2024-05-13
- gpt-4o-all
- gpt-4o-image
- gpt-4o-mini
- gpt-5-all
- gpt-5.1-all
- gpt-5.2-pro
- gpt-5.4-mini
- gpt-5.4-nano
- gpt-image-1

### Anthropic Claude
- claude-3-5-haiku-20241022
- claude-3-5-sonnet-20240620
- claude-3-5-sonnet-20241022
- claude-3-7-sonnet-20250219
- claude-3-haiku-20240307
- claude-3-opus-20240229
- claude-3-sonnet-20240229
- claude-haiku-4-5-20251001
- claude-opus-4-1-20250805
- claude-opus-4-20250514
- claude-opus-4-5-20251101
- claude-opus-4-6
- claude-opus-4-7
- claude-sonnet-4-20250514
- claude-sonnet-4-5-20250929
- claude-sonnet-4-6

### Google Gemini
- gemini-2.0-flash-lite
- gemini-2.5-flash-lite
- gemini-3-pro-preview
- gemini-3.1-flash-image-preview
- gemini-3.1-flash-lite-preview
- gemini-3.1-pro
- gemini-3.1-pro-preview

### xAI Grok
- grok-2-vision
- grok-2-vision-1212
- grok-3
- grok-3-fast
- grok-3-mini
- grok-3-mini-fast
- grok-4
- grok-4-0709
- grok-4-1-fast
- grok-4-1-fast-non-reasoning
- grok-4-1-fast-reasoning

### DeepSeek
- deepseek-chat
- deepseek-r1
- deepseek-r1-0528
- deepseek-reasoner
- deepseek-v3
- deepseek-v3-250324
- deepseek-v3.2-exp
- deepseek-v4-flash

### Kimi (Moonshot)
- kimi-k2-0711-preview
- kimi-k2-0905-preview
- kimi-k2-instruct-0905
- kimi-k2-thinking
- kimi-k2-thinking-turbo
- kimi-k2-turbo-preview
- kimi-k2.5

### Zhipu GLM
- glm-3-turbo
- glm-4-air
- glm-4-flash
- glm-4-plus
- glm-4.5
- glm-4.5-air
- glm-4.5v
- glm-4.6
- glm-4.7
- glm-5
- glm-5-turbo
- glm-5.1

### OpenAI o-Series (Reasoning)
- o1
- o1-mini
- o1-pro
- o3
- o3-mini
- o3-pro
- o4-mini
"""


@mcp.tool()
async def aichat_get_usage_guide() -> str:
    """Get a comprehensive guide for using the AiChat tools.

    Provides detailed information on how to use the AiChat tools effectively,
    including parameters, examples, and best practices.

    Returns:
        Complete usage guide for AiChat tools.
    """
    # Last updated: 2026-05-10
    return """# AiChat Tools Usage Guide

## Available Tools

### aichat_create_conversation
Create an AI conversation using the v1 endpoint (/aichat/conversations).
Supports GPT-4/5, o-series, DeepSeek, Grok, and GLM models.

**Parameters:**
- `question` (required): The prompt or question to ask the AI model.
- `model` (optional): The AI model to use. Default: `gpt-4.1`
- `conversation_id` (optional): Continue an existing conversation by providing its ID.
- `preset` (optional): Preset model configuration name.
- `stateful` (optional): Enable stateful conversation mode (boolean).
- `references` (optional): List of reference sources for context.

### aichat_create_conversation_v2
Create an AI conversation using the v2 endpoint (/aichat2/conversations).
Supports a wider range of providers including Claude, Gemini, Grok-4, and Kimi.

**Parameters:**
- `model` (optional): The AI model to use. Default: `gpt-4.1`
- `question` (optional): The prompt or question to ask the AI model.
- `conversation_id` (optional): Continue an existing conversation by providing its ID.
- `preset` (optional): Preset model configuration name.
- `stateful` (optional): Enable stateful conversation mode (default True).
- `references` (optional): List of reference sources for context.

### aichat_list_models
List all available AI models grouped by provider and endpoint.

### aichat_get_usage_guide
Show this usage guide.

## Example Usage

### Simple Question (v1)
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

### Use Claude (v2)
```
aichat_create_conversation_v2(
    question="Explain the theory of relativity.",
    model="claude-opus-4-7"
)
```

### Use Gemini (v2)
```
aichat_create_conversation_v2(
    question="Summarize the latest AI research trends.",
    model="gemini-3.1-pro"
)
```

### Use Grok-4 (v2)
```
aichat_create_conversation_v2(
    question="What are the key differences between quantum and classical computing?",
    model="grok-4"
)
```

### Use Kimi (v2)
```
aichat_create_conversation_v2(
    question="Solve this optimization problem step by step.",
    model="kimi-k2.5"
)
```

### Use a Reasoning Model (v1)
```
aichat_create_conversation(
    question="Solve this step by step: If x^2 + 5x + 6 = 0, find x.",
    model="o3-mini"
)
```

### Use DeepSeek (v1 or v2)
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
- Use `aichat_create_conversation` (v1) for GPT-4/5, o-series, DeepSeek, Grok, and GLM
- Use `aichat_create_conversation_v2` (v2) for Claude, Gemini, Grok-4, Kimi, and additional models
- The `conversation_id` from the response can be used to continue the conversation
- Use reasoning models (o1, o3, o4-mini) for complex math or logic problems
- Use search-preview models for questions requiring web search
- Bearer token authentication is required
"""
