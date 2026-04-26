"""Informational tools for Gemini API."""

from core.server import mcp


@mcp.tool()
async def gemini_list_models() -> str:
    """List all available Gemini models.

    Shows all models available for the Gemini API.

    Returns:
        Table of all Gemini models with descriptions.
    """
    # Last updated: 2026-04-26
    return """Available Gemini Models:

| Model | Description |
|-------|-------------|
| gemini-3.1-pro | Gemini model |
| gemini-3.0-pro | Gemini model |
| gemini-3-flash-preview | Gemini model |
| gemini-2.5-pro | (default) Gemini model |
| gemini-2.5-flash | Gemini model |
| gemini-2.0-flash | Gemini model |
"""


@mcp.tool()
async def gemini_get_usage_guide() -> str:
    """Get a comprehensive guide for using the Gemini tools.

    Provides detailed information on how to use all available Gemini tools
    effectively, including examples and best practices.

    Returns:
        Complete usage guide for Gemini tools.
    """
    # Last updated: 2026-04-26
    return """# Gemini Tools Usage Guide

## Available Tools

### Chat Completion
**gemini_chat_completion** - Generate text responses from a conversation
- messages: Conversation history (required)
- model: Gemini model to use (default: gemini-2.5-pro)
- max_tokens: Response length limit
- temperature: Creativity level (0-2, default: 1)
- n: Number of responses to generate

### Generate Content (Google Native)
**gemini_generate_content** - Generate content using the Google native Gemini API
- model: Gemini model to use (required)
- contents: Input content list (required)
- system_instruction: System instruction dict (optional)
- generation_config: Generation configuration dict (optional)

### Information Tools
- **gemini_list_models** - List available Gemini models
- **gemini_get_usage_guide** - This guide

## Example Usage

### Basic Chat
```
gemini_chat_completion(
    messages=[{"role": "user", "content": "What is machine learning?"}]
)
```

### Chat with System Prompt
```
gemini_chat_completion(
    messages=[
        {"role": "system", "content": "You are a helpful coding assistant."},
        {"role": "user", "content": "Write a Python hello world"}
    ],
    model="gemini-2.5-pro"
)
```

### Generate Content (Google Native)
```
gemini_generate_content(
    model="gemini-2.5-pro",
    contents=[{"role": "user", "parts": [{"text": "Explain quantum computing"}]}]
)
```

## Best Practices

1. **Model selection**: Use the default model for general tasks
2. **Temperature**: Lower (0.1-0.3) for factual tasks, higher (0.7-1.0) for creative tasks
3. **Tokens**: Set max_tokens when you need predictable response lengths
"""
