# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2025-01-22

### Added

- Initial release of MCP Luma Server
- Video generation tools:
  - `luma_generate_video` - Generate video from text prompts
  - `luma_generate_video_from_image` - Generate video using reference images
  - `luma_extend_video` - Extend existing videos by ID
  - `luma_extend_video_from_url` - Extend existing videos by URL
- Task tracking:
  - `luma_get_task` - Query single task status
  - `luma_get_tasks_batch` - Query multiple tasks
- Information tools:
  - `luma_list_aspect_ratios` - List available aspect ratios
  - `luma_list_actions` - List available actions
- Support for all aspect ratios (16:9, 9:16, 1:1, 4:3, 3:4, 21:9, 9:21)
- Loop video generation
- Video clarity enhancement
- Start/end image frame support
- stdio and HTTP transport modes
- Comprehensive test suite
- Full documentation

[Unreleased]: https://github.com/AceDataCloud/LumaMCP/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/AceDataCloud/LumaMCP/releases/tag/v0.1.0
