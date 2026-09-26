# MCP Digital Human Server

A [Model Context Protocol](https://modelcontextprotocol.io) (MCP) server for the
AceDataCloud Digital Human API.

<!-- canonical-acquisition -->
[Start with AceDataCloud](https://platform.acedata.cloud/?utm_source=github&utm_medium=repo&utm_campaign=mcp-digitalhuman)

## Features

- Create lip-synced digital human videos from a source face video or image
- Clone voices from short reference audio samples
- Poll, batch-retrieve, or delete Digital Human tasks

## Installation

```bash
pip install mcp-digitalhuman
```

## Configuration

```bash
export ACEDATACLOUD_API_TOKEN=your_token_here
```

## Usage

```bash
mcp-digitalhuman
```

## Development

```bash
pip install -e ".[dev,test]"
pytest -q
ruff check .
```

## Documentation

<!-- canonical-documentation -->
[Documentation](https://platform.acedata.cloud/documents/digitalhuman)
