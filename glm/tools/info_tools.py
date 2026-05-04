"""Informational tools for GLM API."""

from core.server import mcp


@mcp.tool()
async def glm_list_models() -> str:
    """List all available GLM models for the GLM API.

    Returns a list of supported GLM models with descriptions.

    Returns:
        Formatted list of available GLM models.
    """
    return """# Available GLM Models

## Zhipu GLM Models
- glm-5.1 — Latest GLM model with enhanced capabilities
- glm-4.7 — Recommended default, strong general-purpose model
- glm-4.6 — Balanced performance and speed
- glm-4.5-air — Lightweight and fast GLM model
- glm-3-turbo — Previous generation, fast and efficient
"""


@mcp.tool()
async def glm_get_usage_guide() -> str:
    """Get a comprehensive guide for using the GLM tools.

    Provides detailed information on how to use the GLM tools effectively,
    including parameters, examples, and best practices.

    Returns:
        Complete usage guide for GLM tools.
    """
    return """# GLM Tools Usage Guide

## Available Tools

### glm_chat_completions
Create a chat completion with any supported GLM model.

**Parameters:**
- `messages` (required): List of conversation messages. Each message is a dict with 'role' and 'content'.
- `model` (optional): The GLM model to use. Default: `glm-4.7`
- `temperature` (optional): Sampling temperature between 0 and 2. Default: 1
- `max_tokens` (optional): Maximum tokens to generate.
- `top_p` (optional): Nucleus sampling probability mass. Default: 1
- `stream` (optional): Whether to stream the response. Default: False
- `n` (optional): Number of completions to generate. Default: 1
- `stop` (optional): Stop sequences.
- `frequency_penalty` (optional): Frequency penalty (-2 to 2). Default: 0
- `presence_penalty` (optional): Presence penalty (-2 to 2). Default: 0
- `seed` (optional): Random seed for deterministic output.
- `response_format` (optional): Response format specification.
- `reasoning_effort` (optional): Reasoning effort level (minimal/low/medium/high). Default: medium
- `service_tier` (optional): Service tier (auto/default/flex/scale/priority). Default: auto
- `tools` (optional): Tools the model may call.
- `tool_choice` (optional): Which tool to call.

### glm_list_models
List all available GLM models.

### glm_get_usage_guide
Show this usage guide.

## Example Usage

### Simple Chat
```
glm_chat_completions(
    messages=[{"role": "user", "content": "What is the capital of France?"}],
    model="glm-4.7"
)
```

**Response:**
```json
{
  "id": "chatcmpl-...",
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "The capital of France is Paris."
      },
      "finish_reason": "stop"
    }
  ],
  "model": "glm-4.7"
}
```

### Multi-turn Conversation
```
glm_chat_completions(
    messages=[
        {"role": "user", "content": "Tell me about Paris."},
        {"role": "assistant", "content": "Paris is the capital of France..."},
        {"role": "user", "content": "What is its population?"}
    ],
    model="glm-4.7"
)
```

### Use a Specific Model
```
glm_chat_completions(
    messages=[{"role": "user", "content": "Explain quantum computing."}],
    model="glm-5.1"
)
```

### Chinese Language Task
```
glm_chat_completions(
    messages=[{"role": "user", "content": "请用中文解释机器学习的基本概念。"}],
    model="glm-4.7"
)
```

## Notes
- GLM models excel at Chinese language tasks
- Use glm-5.1 for the most advanced capabilities
- Use glm-4.5-air for faster, lighter tasks
- Bearer token authentication is required
"""
