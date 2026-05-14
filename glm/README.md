# MCP GLM Server

A Model Context Protocol (MCP) server for Zhipu GLM chat completions via the AceDataCloud platform.

## Features

- **GLM chat completions**: Call Zhipu GLM models through a uniform MCP tool
- **Model discovery**: List the GLM models exposed by AceDataCloud
- **Usage guide**: Inline tool returning the API usage guide

## Installation

```bash
pip install mcp-glm
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
mcp-glm
```

### HTTP mode

```bash
mcp-glm --transport http --port 8000
```

## Available Tools

| Tool | Description |
|------|-------------|
| `glm_chat_completions` | Run a GLM chat completion call |
| `glm_list_models` | List available GLM models |
| `glm_get_usage_guide` | Get the API usage guide |

## License

MIT — see [LICENSE](LICENSE).
