"""Prompt templates for GLM MCP server.

MCP Prompts provide guidance to LLMs on when and how to use the available tools.
These are exposed via the MCP protocol and help LLMs make better decisions.
"""

from core.server import mcp


@mcp.prompt()
def glm_guide() -> str:
    """Guide for choosing the right GLM tool and model for chat completion tasks."""
    return """# GLM Guide

When the user wants to chat with a GLM model or generate text, use the appropriate tool:

## Chat Completion
**Tool:** `glm_chat_completions`
**Use when:**
- User wants to chat with a GLM model
- User needs Chinese language understanding or generation
- User wants to use Zhipu AI's models

**Example:** "Ask GLM-4.7 to explain machine learning"
→ Call `glm_chat_completions` with messages=[{"role": "user", "content": "Explain machine learning"}], model="glm-4.7"

## Model Selection Guidelines

### For best quality
Use `glm-5.1` — the most capable GLM model

### For general tasks (default)
Use `glm-4.7` — strong general-purpose model

### For balanced performance
Use `glm-4.6` — good balance of speed and quality

### For quick, simple tasks
Use `glm-3-turbo` — efficient previous-generation model

## Chinese Language Tasks
GLM models are particularly strong for Chinese language tasks:
- Use `glm-4.7` or `glm-5.1` for complex Chinese NLP tasks
- All models support both Chinese and English

## Important Notes:
1. The `messages` field is required
2. The `model` field defaults to glm-4.7
3. Use `glm_list_models` to see all available models
4. Bearer token authentication is required
"""


@mcp.prompt()
def glm_workflow_examples() -> str:
    """Common workflow examples for GLM tasks."""
    return """# GLM Workflow Examples

## Workflow 1: Simple Q&A
1. User: "What is machine learning?"
2. Call `glm_chat_completions(messages=[{"role": "user", "content": "What is machine learning?"}], model="glm-4.7")`
3. Return the answer to the user

## Workflow 2: Multi-turn Conversation
1. User: "Tell me about Python programming"
2. Call `glm_chat_completions(messages=[{"role": "user", "content": "Tell me about Python programming"}], model="glm-4.7")`
3. Save the assistant response
4. User: "How does it compare to Java?"
5. Call `glm_chat_completions` with the full conversation history including the previous exchange
6. The model responds with context from the previous turn

## Workflow 3: Chinese Language Task
1. User: "请帮我用中文写一篇关于人工智能的简短介绍"
2. Call `glm_chat_completions(messages=[{"role": "user", "content": "请帮我用中文写一篇关于人工智能的简短介绍"}], model="glm-4.7")`
3. Return the Chinese response

## Workflow 4: Code Generation
1. User: "Write a Python function to calculate Fibonacci numbers"
2. Call `glm_chat_completions(messages=[{"role": "user", "content": "Write a Python function to calculate Fibonacci numbers"}], model="glm-5.1")`
3. Return the generated code

## Tips:
- GLM models excel at Chinese-English bilingual tasks
- Use glm-5.1 for the most complex reasoning tasks
- Include system messages for better task framing
- Adjust temperature for creativity vs. consistency
"""
