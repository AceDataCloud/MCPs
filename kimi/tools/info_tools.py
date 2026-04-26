"""Informational tools for Kimi API."""

from core.server import mcp


@mcp.tool()
async def kimi_list_models() -> str:
    """List all available Kimi models.

    Shows all models available for the Kimi API.

    Returns:
        Table of all Kimi models with descriptions.
    """
    # Last updated: 2026-04-26
    return """Available Kimi Models:

| Model | Description |
|-------|-------------|
| kimi-k2-thinking-turbo | (default) Kimi model |
| kimi-k2.5 | Kimi model |
| kimi-k2-thinking | Kimi model |
| kimi-k2-instruct-0905 | Kimi model |
| kimi-k2-0905-preview | Kimi model |
| kimi-k2-turbo-preview | Kimi model |
| kimi-k2-0711-preview | Kimi model |
"""


@mcp.tool()
async def kimi_get_usage_guide() -> str:
    """Get a comprehensive guide for using the Kimi tools.

    Provides detailed information on how to use all available Kimi tools
    effectively, including examples and best practices.

    Returns:
        Complete usage guide for Kimi tools.
    """
    # Last updated: 2026-04-26
    return """# Kimi Tools Usage Guide

## Available Tools

### Chat Completion
**kimi_chat_completion** - Generate text responses from a conversation
- messages: Conversation history (required)
- model: Kimi model to use (default: kimi-k2-thinking-turbo)
- max_tokens: Response length limit
- temperature: Creativity level (0-2, default: 1)
- n: Number of responses to generate

### Information Tools
- **kimi_list_models** - List available Kimi models
- **kimi_get_usage_guide** - This guide

## Example Usage

### Basic Chat
```
kimi_chat_completion(
    messages=[{"role": "user", "content": "What is machine learning?"}]
)
```

### Chat with System Prompt
```
kimi_chat_completion(
    messages=[
        {"role": "system", "content": "You are a helpful coding assistant."},
        {"role": "user", "content": "Write a Python hello world"}
    ],
    model="kimi-k2-thinking-turbo"
)
```

## Best Practices

1. **Model selection**: Use the default model for general tasks
2. **Temperature**: Lower (0.1-0.3) for factual tasks, higher (0.7-1.0) for creative tasks
3. **Tokens**: Set max_tokens when you need predictable response lengths
"""
