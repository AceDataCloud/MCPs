"""Informational tools for Grok API."""

from core.server import mcp


@mcp.tool()
async def grok_list_models() -> str:
    """List all available Grok models.

    Shows all models available for the Grok API.

    Returns:
        Table of all Grok models with descriptions.
    """
    # Last updated: 2026-04-26
    return """Available Grok Models:

| Model | Description |
|-------|-------------|
| grok-4 | Grok model |
| grok-4-1-fast | Grok model |
| grok-4-1-fast-non-reasoning | Grok model |
| grok-3 | (default) Grok model |
| grok-3-mini | Grok model |
| grok-2-vision | Grok model |
"""


@mcp.tool()
async def grok_get_usage_guide() -> str:
    """Get a comprehensive guide for using the Grok tools.

    Provides detailed information on how to use all available Grok tools
    effectively, including examples and best practices.

    Returns:
        Complete usage guide for Grok tools.
    """
    # Last updated: 2026-04-26
    return """# Grok Tools Usage Guide

## Available Tools

### Chat Completion
**grok_chat_completion** - Generate text responses from a conversation
- messages: Conversation history (required)
- model: Grok model to use (default: grok-3)
- max_tokens: Response length limit
- temperature: Creativity level (0-2, default: 1)
- n: Number of responses to generate

### Information Tools
- **grok_list_models** - List available Grok models
- **grok_get_usage_guide** - This guide

## Example Usage

### Basic Chat
```
grok_chat_completion(
    messages=[{"role": "user", "content": "What is machine learning?"}]
)
```

### Chat with System Prompt
```
grok_chat_completion(
    messages=[
        {"role": "system", "content": "You are a helpful coding assistant."},
        {"role": "user", "content": "Write a Python hello world"}
    ],
    model="grok-3"
)
```

## Best Practices

1. **Model selection**: Use the default model for general tasks
2. **Temperature**: Lower (0.1-0.3) for factual tasks, higher (0.7-1.0) for creative tasks
3. **Tokens**: Set max_tokens when you need predictable response lengths
"""
