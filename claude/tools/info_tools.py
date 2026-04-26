"""Informational tools for Claude API."""

from core.server import mcp


@mcp.tool()
async def claude_list_models() -> str:
    """List all available Claude models.

    Shows all models available for the Claude API.

    Returns:
        Table of all Claude models with descriptions.
    """
    # Last updated: 2026-04-26
    return """Available Claude Models:

| Model | Description |
|-------|-------------|
| claude-sonnet-4-6 | Claude model |
| claude-opus-4-7 | Claude model |
| claude-opus-4-6 | Claude model |
| claude-opus-4-5-20251101 | Claude model |
| claude-haiku-4-5-20251001 | Claude model |
| claude-sonnet-4-5-20250929 | Claude model |
| claude-opus-4-1-20250805 | Claude model |
| claude-sonnet-4-20250514 | (default) Claude model |
| claude-opus-4-20250514 | Claude model |
| claude-3-7-sonnet-20250219 | Claude model |
| claude-3-5-sonnet-20241022 | Claude model |
| claude-3-5-haiku-20241022 | Claude model |
| claude-3-5-sonnet-20240620 | Claude model |
| claude-3-haiku-20240307 | Claude model |
| claude-3-sonnet-20240229 | Claude model |
| claude-3-opus-20240229 | Claude model |
"""


@mcp.tool()
async def claude_get_usage_guide() -> str:
    """Get a comprehensive guide for using the Claude tools.

    Provides detailed information on how to use all available Claude tools
    effectively, including examples and best practices.

    Returns:
        Complete usage guide for Claude tools.
    """
    # Last updated: 2026-04-26
    return """# Claude Tools Usage Guide

## Available Tools

### Chat Completion
**claude_chat_completion** - Generate text responses from a conversation
- messages: Conversation history (required)
- model: Claude model to use (default: claude-sonnet-4-20250514)
- max_tokens: Response length limit
- temperature: Creativity level (0-2, default: 1)
- n: Number of responses to generate

### Create Message (Anthropic Native)
**claude_create_message** - Create a message using the Anthropic native API
- messages: Conversation messages (required)
- model: Claude model (required)
- max_tokens: Maximum tokens to generate (required)
- system: System prompt (optional)
- temperature: Sampling temperature (optional)

### Information Tools
- **claude_list_models** - List available Claude models
- **claude_get_usage_guide** - This guide

## Example Usage

### Basic Chat
```
claude_chat_completion(
    messages=[{"role": "user", "content": "What is machine learning?"}]
)
```

### Chat with System Prompt
```
claude_chat_completion(
    messages=[
        {"role": "system", "content": "You are a helpful coding assistant."},
        {"role": "user", "content": "Write a Python hello world"}
    ],
    model="claude-sonnet-4-20250514"
)
```

### Create Message (Anthropic Native)
```
claude_create_message(
    messages=[{"role": "user", "content": "Explain quantum computing"}],
    model="claude-sonnet-4-20250514",
    max_tokens=1024
)
```

## Best Practices

1. **Model selection**: Use the default model for general tasks
2. **Temperature**: Lower (0.1-0.3) for factual tasks, higher (0.7-1.0) for creative tasks
3. **Tokens**: Set max_tokens when you need predictable response lengths
"""
