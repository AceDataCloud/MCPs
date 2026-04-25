# MCP AiChat Server

A Model Context Protocol (MCP) server for AI dialogue via the AceDataCloud platform.
Supports a wide range of models including GPT-4/5, o-series, DeepSeek, Grok, and GLM.

## Features

- **Multi-model support**: GPT-4.1, GPT-4o, GPT-5, o1, o3, o4-mini, DeepSeek, Grok, GLM, and more
- **Multi-turn conversations**: Continue conversations using conversation IDs
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
- GPT-5 series: gpt-5.5, gpt-5.4, gpt-5.2, gpt-5.1, gpt-5, gpt-5-mini, gpt-5-nano
- GPT-4.1 series: gpt-4.1, gpt-4.1-mini, gpt-4.1-nano
- GPT-4o series: gpt-4o, gpt-4o-mini, gpt-4o-all, gpt-4o-image
- GPT-4 series: gpt-4, gpt-4-turbo, gpt-4-vision-preview
- o-series: o1, o1-mini, o1-pro, o3, o3-mini, o3-pro, o4-mini

### DeepSeek
- deepseek-r1, deepseek-r1-0528, deepseek-v3, deepseek-v3-250324

### xAI
- grok-3

### Zhipu AI
- glm-5.1, glm-4.7, glm-4.6, glm-4.5-air, glm-3-turbo

## License

MIT
