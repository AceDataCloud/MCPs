# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-04-05

### Added

- Initial release of MCP Wan Server
- Video generation tools:
  - `wan_generate_video` - Generate video from text prompts
  - `wan_generate_video_from_image` - Generate video using reference images
- Task tracking:
  - `wan_get_task` - Query single task status
  - `wan_get_tasks_batch` - Query multiple tasks
- Information tools:
  - `wan_list_models` - List available models
  - `wan_list_resolutions` - List available resolutions
  - `wan_list_actions` - List available actions
- Support for 4 models (wan2.6-t2v, wan2.6-i2v, wan2.6-r2v, wan2.6-i2v-flash)
- Multiple resolutions (480P, 720P, 1080P)
- Audio generation support
- Character extraction via reference videos
- stdio and HTTP transport modes
- Comprehensive test suite
- Full documentation

[Unreleased]: https://github.com/AceDataCloud/WanMCP/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/AceDataCloud/WanMCP/releases/tag/v0.1.0
