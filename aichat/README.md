# MCP AiChat Server

A Model Context Protocol (MCP) server for AI dialogue via the AceDataCloud platform.
Supports a wide range of models including GPT/o-series, Claude, Gemini, Grok, DeepSeek, Kimi, and GLM.

## Features

- **Multi-model support**: GPT/o-series, Claude, Gemini, Grok, DeepSeek, Kimi, GLM, and more
- **Multi-turn conversations**: Continue conversations using conversation IDs
- **Multimodal input**: Send text-only or structured message content blocks
- **Conversation actions**: Chat, retrieve, list, update, or delete conversations through one tool
- **Stateful mode**: Optional server-side conversation state management
- **Reference sources**: Include external references for context-aware responses

## Installation

```bash
pip install mcp-aichat
```

## Configuration

Set your AceDataCloud API token:

```bash
export ACEDATACLOUD_API_TOKEN=your_token_here
```

Get your token from [https://platform.acedata.cloud](https://platform.acedata.cloud).

## Usage

### stdio mode (default)

```bash
mcp-aichat
```

### HTTP mode

```bash
mcp-aichat --transport http --port 8000
```

## Available Tools

| Tool | Description |
|------|-------------|
| `aichat_create_conversation` | Create an AI conversation with any supported model |
| `aichat_list_models` | List all available AI models |
| `aichat_get_usage_guide` | Get API usage guide |

## Supported Models

### OpenAI
- GPT models: gpt-4, gpt-4.1, gpt-4.1-mini, gpt-4.1-nano, gpt-4o, gpt-4o-2024-05-13, gpt-4o-all, gpt-4o-image, gpt-4o-mini, gpt-5-all, gpt-5.1-all, gpt-5.2-pro, gpt-5.4-mini, gpt-5.4-nano, gpt-image-1
- Reasoning models: o1, o1-mini, o1-pro, o3, o3-mini, o3-pro, o4-mini

### Anthropic
- Claude models: claude-3-5-haiku-20241022, claude-3-5-sonnet-20240620, claude-3-5-sonnet-20241022, claude-3-7-sonnet-20250219, claude-3-haiku-20240307, claude-3-opus-20240229, claude-3-sonnet-20240229, claude-haiku-4-5-20251001, claude-opus-4-1-20250805, claude-opus-4-20250514, claude-opus-4-5-20251101, claude-opus-4-6, claude-opus-4-7, claude-sonnet-4-20250514, claude-sonnet-4-5-20250929, claude-sonnet-4-6

### Google
- Gemini models: gemini-2.0-flash-lite, gemini-2.5-flash-lite, gemini-3-pro-preview, gemini-3.1-flash-image-preview, gemini-3.1-flash-lite-preview, gemini-3.1-pro, gemini-3.1-pro-preview

### DeepSeek
- deepseek-chat, deepseek-r1, deepseek-r1-0528, deepseek-reasoner, deepseek-v3, deepseek-v3-250324, deepseek-v3.2-exp, deepseek-v4-flash

### xAI
- grok-2-vision, grok-2-vision-1212, grok-3, grok-3-fast, grok-3-mini, grok-3-mini-fast, grok-4, grok-4-0709, grok-4-1-fast, grok-4-1-fast-non-reasoning, grok-4-1-fast-reasoning

### Moonshot
- kimi-k2-0711-preview, kimi-k2-0905-preview, kimi-k2-instruct-0905, kimi-k2-thinking, kimi-k2-thinking-turbo, kimi-k2-turbo-preview, kimi-k2.5

### Zhipu AI
- glm-3-turbo, glm-4-air, glm-4-flash, glm-4-plus, glm-4.5, glm-4.5-air, glm-4.5v, glm-4.6, glm-4.7, glm-5, glm-5-turbo, glm-5.1

## License

MIT
