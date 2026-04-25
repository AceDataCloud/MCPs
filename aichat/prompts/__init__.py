"""Prompt templates for AiChat MCP server.

MCP Prompts provide guidance to LLMs on when and how to use the available tools.
These are exposed via the MCP protocol and help LLMs make better decisions.
"""

from core.server import mcp


@mcp.prompt()
def aichat_guide() -> str:
    """Guide for choosing the right AiChat tool and model for AI conversation tasks."""
    return """# AiChat Guide

When the user wants to have a conversation with an AI model or ask a question, use the appropriate tool:

## AI Conversation
**Tool:** `aichat_create_conversation`
**Use when:**
- User wants to ask an AI model a question
- User wants to continue an existing conversation
- User needs answers from specific models like DeepSeek, Grok, or GLM

**Example:** "Ask GPT-4.1 what the capital of France is"
→ Call `aichat_create_conversation` with question="What is the capital of France?", model="gpt-4.1"

## Model Selection Guidelines

### For general questions
Use `gpt-4.1` (default) or `gpt-4o` — fast and capable

### For complex reasoning / math / coding
Use `o3-mini`, `o3`, `o4-mini`, or `o1` — reasoning-optimized models

### For latest capabilities
Use `gpt-5`, `gpt-5.5` — most advanced models

### For DeepSeek models
Use `deepseek-r1` for reasoning, `deepseek-v3` for general tasks

### For Grok
Use `grok-3` for xAI's model

### For Chinese language tasks
Use `glm-4.7`, `glm-5.1` — Zhipu AI's GLM models

## Continuing a Conversation
If the user wants to continue a conversation, use the `id` field from the previous response
as the `conversation_id` parameter.

## Important Notes:
1. The `question` field is required
2. The `model` field is required (defaults to gpt-4.1)
3. Use `conversation_id` to maintain conversation context
4. Bearer token authentication is required
5. Use `aichat_list_models` to see all available models
"""


@mcp.prompt()
def aichat_workflow_examples() -> str:
    """Common workflow examples for AiChat tasks."""
    return """# AiChat Workflow Examples

## Workflow 1: Simple Q&A
1. User: "What is machine learning?"
2. Call `aichat_create_conversation(question="What is machine learning?", model="gpt-4.1")`
3. Return the answer to the user

## Workflow 2: Multi-turn Conversation
1. User: "Tell me about Paris"
2. Call `aichat_create_conversation(question="Tell me about Paris", model="gpt-4.1")`
3. Save the `id` from the response
4. User: "What is its population?"
5. Call `aichat_create_conversation(question="What is its population?", model="gpt-4.1", conversation_id=<saved_id>)`
6. The model responds with context from the previous turn

## Workflow 3: Complex Reasoning
1. User: "Solve this math problem step by step: ..."
2. Call `aichat_create_conversation(question=..., model="o3-mini")`
3. Return the step-by-step solution

## Workflow 4: Code Generation
1. User: "Write a Python function to sort a list of dictionaries by a key"
2. Call `aichat_create_conversation(question=..., model="gpt-4.1")`
3. Return the generated code

## Tips:
- Use o-series models for complex reasoning tasks
- Use search-preview models when the question requires up-to-date information
- Save the conversation `id` to enable multi-turn conversations
"""
