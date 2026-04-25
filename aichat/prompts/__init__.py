"""Prompt templates for AIChat MCP server.

MCP Prompts provide guidance to LLMs on when and how to use the available tools.
These are exposed via the MCP protocol and help LLMs make better decisions.
"""

from core.server import mcp


@mcp.prompt()
def aichat_usage_guide() -> str:
    """Guide for using the AIChat conversation tool effectively."""
    return """# AIChat Usage Guide

When the user wants to ask a question or have a conversation with an AI model, use the
`aichat_conversation` tool.

## Single-Turn Question
**Use when:** User asks a one-off question
```
aichat_conversation(question="What is the capital of France?")
```

## Multi-Turn Conversation
**Use when:** User wants to continue a conversation
1. First call: `aichat_conversation(question="...", stateful=True)`
2. Extract `id` from the response
3. Follow-up: `aichat_conversation(question="...", stateful=True, conversation_id="<id>")`

## Model Selection
- **General tasks**: gpt-4.1 (default)
- **Reasoning/math**: deepseek-r1, o3, o4-mini
- **Cost efficiency**: gpt-4.1-mini, gpt-4o-mini
- **Chinese language**: glm-4.6, glm-4.7
- **Latest capabilities**: gpt-5.5, gpt-5.4

## Available Models
Call `aichat_list_models` to see the full list of available models.
"""


@mcp.prompt()
def aichat_model_selection_guide() -> str:
    """Guide for selecting the right AI model for a task."""
    return """# AIChat Model Selection Guide

## For General Conversational Tasks
Use **gpt-4.1** (default) - balanced capability and cost.

## For Complex Reasoning and Math
Use **deepseek-r1**, **o3**, or **o4-mini** - these models excel at step-by-step reasoning.

## For Code Generation
Use **gpt-4.1**, **gpt-4o**, or **deepseek-v3** - strong coding capabilities.

## For Cost-Efficient Tasks
Use **gpt-4.1-mini** or **gpt-4o-mini** - faster and cheaper for simpler tasks.

## For Cutting-Edge Performance
Use **gpt-5.5**, **gpt-5.4**, or **gpt-5** - latest generation models.

## For Chinese Language Tasks
Use **glm-4.6**, **glm-4.7**, or **glm-5.1** - optimized for Chinese content.

## For Browsing/Search Tasks
Use **gpt-4o-search-preview** or **gpt-4o-mini-search-preview** - have web search access.

## Tips
- Always use `aichat_list_models` to get the current full list of available models
- For multi-turn conversations, set `stateful=True` and pass the conversation `id`
- Use `references` to provide URLs as context for the model
"""
