# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Five new tools matching the platform's expanded `/veo/*` surface:
  - `veo_upsample` — upscale to 1080p / 4K or render an animated GIF preview (new dedicated `/veo/upsample` endpoint).
  - `veo_extend` — extend the duration of a previously generated video (`veo31` series only).
  - `veo_reshoot` — re-render with a different camera motion (15 motion-type aliases mapped to upstream `RESHOOT_MOTION_TYPE_*`).
  - `veo_object_insert` — insert an object/effect into an existing video, with optional image-mask placement.
  - `veo_object_remove` — erase a region defined by a white-pixel image mask.
- New `veo_ingredients_to_video` tool for the `veo31-fast-ingredients` multi-image fusion mode (previously had to be invoked through `veo_image_to_video` with implicit model selection).
- New types in `core/types.py`: `UpsampleAction`, `ExtendModel`, `ObjectAction`, `MotionType`.
- New client convenience methods in `core/client.py`: `upsample_video`, `extend_video`, `reshoot_video`, `manipulate_object`.

### Changed

- Updated `veo_list_actions` to document all 12 tools, the workflow examples, and the upstream constraint that extend outputs cannot be reshot / object-edited.

### Backward compatibility

- The legacy `veo_get_1080p` tool is preserved unchanged; it continues to call `/veo/videos` with `action=get1080p`, which the platform now aliases to `/veo/upsample` with `action=1080p`. New code should prefer `veo_upsample`.

## [0.1.0] - 2025-06-01

### Added

- Initial release of MCP Veo Server
- Video generation tools:
  - `veo_generate_video` - Generate video from text prompts
  - `veo_generate_video_from_image` - Generate video using reference images
- Task tracking:
  - `veo_get_task` - Query single task status
  - `veo_get_tasks_batch` - Query multiple tasks
- Information tools:
  - `veo_list_models` - List available models
  - `veo_list_actions` - List available actions
- stdio and HTTP transport modes
- Comprehensive test suite
- Full documentation

[Unreleased]: https://github.com/AceDataCloud/VeoMCP/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/AceDataCloud/VeoMCP/releases/tag/v0.1.0
