# MCP WebExtrator Server

A Model Context Protocol (MCP) server for web rendering and structured content extraction
via the AceDataCloud WebExtrator platform.

## Features

- **Structured extraction**: Pull structured data out of any URL via WebExtrator
- **Web rendering**: Render dynamic JavaScript pages and capture the rendered output
- **Asynchronous tasks**: Submit extract / render jobs and poll for results
- **Batch task lookup**: Query multiple task results in one call

## Installation

```bash
pip install mcp-webextrator
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
mcp-webextrator
```

### HTTP mode

```bash
mcp-webextrator --transport http --port 8000
```

## Available Tools

| Tool | Description |
|------|-------------|
| `webextrator_extract` | Extract structured content from a URL |
| `webextrator_render` | Render a dynamic web page and return the rendered output |
| `webextrator_get_task` | Get the status / result of an extract or render task |
| `webextrator_get_tasks_batch` | Batch-fetch the status / result of multiple tasks |
| `webextrator_get_usage_guide` | Get the API usage guide |

## License

MIT — see [LICENSE](LICENSE).
