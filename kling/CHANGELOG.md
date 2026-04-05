# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-04-05

### Added

- Initial release of MCP Kling Server
- Video generation tools:
  - `kling_generate_video` - Generate video from text prompts
  - `kling_generate_video_from_image` - Generate video using reference images
  - `kling_extend_video` - Extend existing videos
- Motion transfer:
  - `kling_generate_motion` - Transfer motion from video to image
- Task tracking:
  - `kling_get_task` - Query single task status
  - `kling_get_tasks_batch` - Query multiple tasks
- Information tools:
  - `kling_list_models` - List available models
  - `kling_list_actions` - List available actions
- Support for 6 models (kling-v1 through kling-video-o1)
- Standard and Pro generation modes
- Camera control support
- stdio and HTTP transport modes
- Comprehensive test suite
- Full documentation

[Unreleased]: https://github.com/AceDataCloud/KlingMCP/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/AceDataCloud/KlingMCP/releases/tag/v0.1.0
