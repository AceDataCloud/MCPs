# MCP Digital Human Server

A [Model Context Protocol](https://modelcontextprotocol.io) (MCP) server for the
AceDataCloud Digital Human API.

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
