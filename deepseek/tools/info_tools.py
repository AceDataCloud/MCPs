"""Informational tools for DeepSeek API."""

from core.server import mcp


@mcp.tool()
async def deepseek_list_models() -> str:
    """List all available DeepSeek models.

    Shows all models available for the DeepSeek API.

    Returns:
        Table of all DeepSeek models with descriptions.
    """
    # Last updated: 2026-04-26
    return """Available DeepSeek Models:

| Model | Description |
|-------|-------------|
| deepseek-r1 | DeepSeek model |
| deepseek-r1-0528 | DeepSeek model |
| deepseek-v3 | (default) DeepSeek model |
| deepseek-v3-250324 | DeepSeek model |
| deepseek-v3.2-exp | DeepSeek model |
"""


@mcp.tool()
async def deepseek_get_usage_guide() -> str:
    """Get a comprehensive guide for using the DeepSeek tools.

    Provides detailed information on how to use all available DeepSeek tools
    effectively, including examples and best practices.

    Returns:
        Complete usage guide for DeepSeek tools.
    """
    # Last updated: 2026-04-26
    return """# DeepSeek Tools Usage Guide

## Available Tools

### Chat Completion
**deepseek_chat_completion** - Generate text responses from a conversation
- messages: Conversation history (required)
- model: DeepSeek model to use (default: deepseek-v3)
- max_tokens: Response length limit
- temperature: Creativity level (0-2, default: 1)
- n: Number of responses to generate

### Information Tools
- **deepseek_list_models** - List available DeepSeek models
- **deepseek_get_usage_guide** - This guide

## Example Usage

### Basic Chat
```
deepseek_chat_completion(
    messages=[{"role": "user", "content": "What is machine learning?"}]
)
```

### Chat with System Prompt
```
deepseek_chat_completion(
    messages=[
        {"role": "system", "content": "You are a helpful coding assistant."},
        {"role": "user", "content": "Write a Python hello world"}
    ],
    model="deepseek-v3"
)
```

## Best Practices

1. **Model selection**: Use the default model for general tasks
2. **Temperature**: Lower (0.1-0.3) for factual tasks, higher (0.7-1.0) for creative tasks
3. **Tokens**: Set max_tokens when you need predictable response lengths
"""
