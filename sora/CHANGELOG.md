# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-01-22

### Added

- Initial release of MCP Sora server
- Text-to-video generation with `sora_generate_video`
- Image-to-video generation with `sora_generate_video_from_image`
- Character-based video generation with `sora_generate_video_with_character`
- Async generation with callback support via `sora_generate_video_async`
- Task status queries with `sora_get_task` and `sora_get_tasks_batch`
- Information tools: `sora_list_models`, `sora_list_actions`
- MCP prompts for LLM guidance
- Support for sora-2 and sora-2-pro models
- Multiple video orientations (landscape, portrait, square)
- Multiple durations (10s, 15s, 25s)
- Claude Desktop integration support
- HTTP and stdio transport modes
