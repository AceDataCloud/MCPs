# MCP Claude Server

A Model Context Protocol (MCP) server for Claude AI via the AceDataCloud platform.
Supports all Claude models including Claude 3.5, Claude 3.7, Claude 4, and newer series.

## Features

- **Claude Chat Completion** (OpenAI-compatible format)
- **Claude Messages API** (Native Anthropic format)
- All Claude models supported

## Installation

```bash
pip install mcp-claude
```

## Configuration

Copy `.env.example` to `.env` and set your API token:

```bash
ACEDATACLOUD_API_TOKEN=your_api_token_here
```

Get your API token from [AceDataCloud Platform](https://platform.acedata.cloud).

## Usage

```bash
mcp-claude
```

## Available Tools

- `claude_chat_completion` - Chat with Claude using OpenAI-compatible format
- `claude_messages` - Chat with Claude using native Anthropic Messages API
- `claude_list_models` - List all available Claude models

## Supported Models

| Model | Description |
|-------|-------------|
| claude-sonnet-4-6 | Claude Sonnet 4.6 (latest, recommended) |
| claude-opus-4-7 | Claude Opus 4.7 |
| claude-opus-4-6 | Claude Opus 4.6 |
| claude-opus-4-5-20251101 | Claude Opus 4.5 |
| claude-haiku-4-5-20251001 | Claude Haiku 4.5 |
| claude-sonnet-4-5-20250929 | Claude Sonnet 4.5 |
| claude-opus-4-1-20250805 | Claude Opus 4.1 |
| claude-sonnet-4-20250514 | Claude Sonnet 4 |
| claude-opus-4-20250514 | Claude Opus 4 |
| claude-3-7-sonnet-20250219 | Claude 3.7 Sonnet |
| claude-3-5-sonnet-20241022 | Claude 3.5 Sonnet |
| claude-3-5-haiku-20241022 | Claude 3.5 Haiku |
| claude-3-5-sonnet-20240620 | Claude 3.5 Sonnet (June 2024) |
| claude-3-haiku-20240307 | Claude 3 Haiku |
| claude-3-sonnet-20240229 | Claude 3 Sonnet |
| claude-3-opus-20240229 | Claude 3 Opus |

## License

MIT
