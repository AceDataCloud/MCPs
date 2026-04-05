# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2026.4.5.0] - 2026-04-05

### Added

- Initial release of MCP Hailuo Server
- Video generation tools:
  - `hailuo_generate_video` - Generate video from text prompts
  - `hailuo_generate_video_from_image` - Generate video from reference images
- Task tracking:
  - `hailuo_get_task` - Query single task status
  - `hailuo_get_tasks_batch` - Query multiple tasks
- Information tools:
  - `hailuo_list_models` - List available video models
  - `hailuo_list_actions` - List available actions
- Support for all MiniMax models (minimax-t2v, minimax-i2v, minimax-i2v-director)
- Text-to-video generation
- Image-to-video generation
- Director-mode image-to-video generation
- stdio and HTTP transport modes
- OAuth support for Claude.ai
- Comprehensive test suite
- Full documentation

[Unreleased]: https://github.com/AceDataCloud/HailuoMCP/compare/v2026.4.5.0...HEAD
[2026.4.5.0]: https://github.com/AceDataCloud/HailuoMCP/releases/tag/v2026.4.5.0
