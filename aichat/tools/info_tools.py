"""Informational tools for AIChat API."""

from core.server import mcp


@mcp.tool()
async def aichat_list_models() -> str:
    """List all available AI chat models.

    Shows all models available for the aichat conversations endpoint,
    including GPT, o-series, DeepSeek, Grok, and GLM models.

    Returns:
        Table of all available models with descriptions.
    """
    # Last updated: 2026-04-25
    return """Available AIChat Models:

## GPT-5 Series
| Model         | Description                              |
|---------------|------------------------------------------|
| gpt-5.5       | Latest GPT-5.5 model                     |
| gpt-5.5-pro   | GPT-5.5 Pro variant                      |
| gpt-5.4       | GPT-5.4 model                            |
| gpt-5.4-pro   | GPT-5.4 Pro variant                      |
| gpt-5.2       | GPT-5.2 model                            |
| gpt-5.1       | GPT-5.1 model                            |
| gpt-5.1-all   | GPT-5.1 all-access variant               |
| gpt-5         | GPT-5 standard                           |
| gpt-5-mini    | GPT-5 Mini - cost efficient              |
| gpt-5-nano    | GPT-5 Nano - ultra cost efficient        |
| gpt-5-all     | GPT-5 all-access variant                 |

## GPT-4 Series
| Model                          | Description                              |
|--------------------------------|------------------------------------------|
| gpt-4                          | GPT-4 standard                           |
| gpt-4-all                      | GPT-4 all-access                         |
| gpt-4-turbo                    | GPT-4 Turbo                              |
| gpt-4-turbo-preview            | GPT-4 Turbo Preview                      |
| gpt-4-vision-preview           | GPT-4 Vision Preview                     |
| gpt-4.1                        | GPT-4.1 (recommended default)            |
| gpt-4.1-2025-04-14             | GPT-4.1 dated variant                    |
| gpt-4.1-mini                   | GPT-4.1 Mini - cost efficient            |
| gpt-4.1-mini-2025-04-14        | GPT-4.1 Mini dated variant               |
| gpt-4.1-nano                   | GPT-4.1 Nano - ultra cost efficient      |
| gpt-4.1-nano-2025-04-14        | GPT-4.1 Nano dated variant               |
| gpt-4.5-preview                | GPT-4.5 Preview                          |
| gpt-4.5-preview-2025-02-27     | GPT-4.5 Preview dated variant            |
| gpt-4o                         | GPT-4o multimodal                        |
| gpt-4o-2024-05-13              | GPT-4o dated variant                     |
| gpt-4o-2024-08-06              | GPT-4o dated variant                     |
| gpt-4o-2024-11-20              | GPT-4o dated variant                     |
| gpt-4o-all                     | GPT-4o all-access                        |
| gpt-4o-image                   | GPT-4o with image capabilities           |
| gpt-4o-mini                    | GPT-4o Mini                              |
| gpt-4o-mini-2024-07-18         | GPT-4o Mini dated variant                |
| gpt-4o-mini-search-preview     | GPT-4o Mini with search                  |
| gpt-4o-search-preview          | GPT-4o with search                       |

## Reasoning (o-series)
| Model                    | Description                               |
|--------------------------|-------------------------------------------|
| o1                       | o1 - original reasoning model             |
| o1-2024-12-17            | o1 dated variant                          |
| o1-all                   | o1 all-access                             |
| o1-mini                  | o1 Mini                                   |
| o1-mini-2024-09-12       | o1 Mini dated variant                     |
| o1-mini-all              | o1 Mini all-access                        |
| o1-preview               | o1 Preview                                |
| o1-pro                   | o1 Pro                                    |
| o1-pro-2025-03-19        | o1 Pro dated variant                      |
| o1-pro-all               | o1 Pro all-access                         |
| o3                       | o3 - advanced reasoning                   |
| o3-2025-04-16            | o3 dated variant                          |
| o3-all                   | o3 all-access                             |
| o3-mini                  | o3 Mini                                   |
| o3-mini-high             | o3 Mini (high effort)                     |
| o3-mini-low              | o3 Mini (low effort)                      |
| o3-mini-medium           | o3 Mini (medium effort)                   |
| o3-pro                   | o3 Pro                                    |
| o3-pro-2025-06-10        | o3 Pro dated variant                      |
| o4-mini                  | o4 Mini - fast reasoning                  |
| o4-mini-2025-04-16       | o4 Mini dated variant                     |
| o4-mini-all              | o4 Mini all-access                        |
| o4-mini-high-all         | o4 Mini high-access                       |

## DeepSeek Models
| Model              | Description                              |
|--------------------|------------------------------------------|
| deepseek-r1        | DeepSeek R1 reasoning model              |
| deepseek-r1-0528   | DeepSeek R1 dated variant                |
| deepseek-v3        | DeepSeek V3 general model                |
| deepseek-v3-250324 | DeepSeek V3 dated variant                |

## Other Models
| Model        | Description                              |
|--------------|------------------------------------------|
| grok-3       | Grok 3 by xAI                            |
| glm-5.1      | GLM-5.1 by Zhipu AI                      |
| glm-4.7      | GLM-4.7 by Zhipu AI                      |
| glm-4.6      | GLM-4.6 by Zhipu AI                      |
| glm-4.5-air  | GLM-4.5 Air by Zhipu AI                  |
| glm-3-turbo  | GLM-3 Turbo by Zhipu AI                  |
"""


@mcp.tool()
async def aichat_get_usage_guide() -> str:
    """Get a comprehensive guide for using the AIChat tools.

    Provides detailed information on how to use all available AIChat tools
    effectively, including examples and best practices.

    Returns:
        Complete usage guide for AIChat tools.
    """
    # Last updated: 2026-04-25
    return """# AIChat Tools Usage Guide

## Available Tools

### Conversation
**aichat_conversation** - Send a question to an AI model and get an answer
- question: The prompt or question (required)
- model: AI model to use (default: gpt-4.1)
- conversation_id: Existing conversation ID for stateful continuation
- stateful: Enable conversation memory across turns
- preset: Preset model configuration
- references: List of reference URLs for context

### Information Tools
- **aichat_list_models** - List all available AI models
- **aichat_get_usage_guide** - This guide

## Example Usage

### Basic Question
```
aichat_conversation(
    question="What is machine learning?"
)
```

### Using a Specific Model
```
aichat_conversation(
    question="Explain quantum entanglement",
    model="gpt-4o"
)
```

### Multi-Turn Stateful Conversation
```
# First turn - start a conversation
result = aichat_conversation(
    question="What is Python?",
    model="gpt-4.1",
    stateful=True
)
# Extract conversation id from result["id"]

# Second turn - continue the conversation
aichat_conversation(
    question="Show me a simple example",
    model="gpt-4.1",
    stateful=True,
    conversation_id="<id from previous result>"
)
```

### Using DeepSeek for Reasoning
```
aichat_conversation(
    question="Solve this step by step: A train travels 120km in 2 hours...",
    model="deepseek-r1"
)
```

### With References
```
aichat_conversation(
    question="Summarize the content at this URL",
    model="gpt-4.1",
    references=["https://example.com/article"]
)
```

## Best Practices

1. **Model selection**: Use gpt-4.1 for general tasks, deepseek-r1 for complex reasoning
2. **Stateful conversations**: Use stateful=True and pass conversation_id for multi-turn chats
3. **References**: Provide URLs as references when you want the model to consider external content
4. **Preset**: Use preset to configure the model with specific behavior settings
"""
