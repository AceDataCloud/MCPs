# MCP DeepSeek Server

A Model Context Protocol (MCP) server for DeepSeek AI via the AceDataCloud platform.
Supports all DeepSeek models including DeepSeek-R1 and DeepSeek-V3.

## Features

- **DeepSeek Chat Completion** (OpenAI-compatible format)
- All DeepSeek models supported

## Installation

```bash
pip install mcp-deepseek
```

## Configuration

Copy `.env.example` to `.env` and set your API token:

```bash
ACEDATACLOUD_API_TOKEN=your_api_token_here
```

Get your API token from [AceDataCloud Platform](https://platform.acedata.cloud).

## Usage

```bash
mcp-deepseek
```

## Available Tools

- `deepseek_chat_completion` - Chat with DeepSeek models
- `deepseek_list_models` - List all available DeepSeek models

## Supported Models

| Model | Description |
|-------|-------------|
| deepseek-v3 | DeepSeek V3 (recommended default) |
| deepseek-v3-250324 | DeepSeek V3 (March 2025) |
| deepseek-v3.2-exp | DeepSeek V3.2 Experimental |
| deepseek-r1 | DeepSeek R1 reasoning model |
| deepseek-r1-0528 | DeepSeek R1 (May 2025) |

## License

MIT
