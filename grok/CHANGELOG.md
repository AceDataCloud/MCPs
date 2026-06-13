# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2026.6.13.0] - 2026-06-13

### Added

- Initial release of MCP Grok Server (Grok Imagine AI video generation)
- Video generation tools:
  - `grok_text_to_video` - Generate video from a text prompt
  - `grok_image_to_video` - Generate video from a reference image
- Task tracking:
  - `grok_get_task` - Query single task status
  - `grok_get_tasks_batch` - Query multiple tasks
- Information tools:
  - `grok_list_models` - List available models
  - `grok_list_actions` - List available actions
  - `grok_get_prompt_guide` - Prompt writing guide
- stdio and HTTP transport modes
- Test suite (config, client, utils, integration)

[Unreleased]: https://github.com/AceDataCloud/GrokMCP/compare/v2026.6.13.0...HEAD
[2026.6.13.0]: https://github.com/AceDataCloud/GrokMCP/releases/tag/v2026.6.13.0
