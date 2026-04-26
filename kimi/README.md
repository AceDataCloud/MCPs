# MCP Kimi Server

A Model Context Protocol (MCP) server for Kimi AI via the AceDataCloud platform.
Supports all Kimi models including Kimi K2 and K2.5 series.

## Features

- **Kimi Chat Completion** (OpenAI-compatible format)
- All Kimi models supported

## Installation

```bash
pip install mcp-kimi
```

## Configuration

Copy `.env.example` to `.env` and set your API token:

```bash
ACEDATACLOUD_API_TOKEN=your_api_token_here
```

Get your API token from [AceDataCloud Platform](https://platform.acedata.cloud).

## Usage

```bash
mcp-kimi
```

## Available Tools

- `kimi_chat_completion` - Chat with Kimi models
- `kimi_list_models` - List all available Kimi models

## Supported Models

| Model | Description |
|-------|-------------|
| kimi-k2.5 | Kimi K2.5 (recommended default) |
| kimi-k2-thinking-turbo | Kimi K2 Thinking Turbo |
| kimi-k2-thinking | Kimi K2 Thinking |
| kimi-k2-instruct-0905 | Kimi K2 Instruct (Sep 2025) |
| kimi-k2-0905-preview | Kimi K2 Preview (Sep 2025) |
| kimi-k2-turbo-preview | Kimi K2 Turbo Preview |
| kimi-k2-0711-preview | Kimi K2 Preview (Jul 2025) |

## License

MIT
