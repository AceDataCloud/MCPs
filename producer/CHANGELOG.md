# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-04-05

### Added

- Initial release of MCP Producer Server
- Audio generation tools:
  - `producer_generate_music` - Generate music from text prompts
  - `producer_generate_custom_music` - Generate with custom lyrics and style
  - `producer_extend_music` - Extend songs from a timestamp
  - `producer_cover_music` - Create covers in different styles
  - `producer_variation_music` - Create variations of songs
  - `producer_swap_vocals` - Swap vocals between songs
  - `producer_swap_instrumentals` - Swap instrumentals between songs
  - `producer_replace_section` - Replace a section of a song
  - `producer_stems_music` - Separate into vocal/instrumental stems
- Lyrics generation:
  - `producer_generate_lyrics` - Generate structured lyrics from prompt
- Media tools:
  - `producer_upload_audio` - Upload external audio for processing
  - `producer_generate_video` - Generate video for a song
  - `producer_generate_wav` - Get lossless WAV format
- Task tracking:
  - `producer_get_task` - Query single task status
  - `producer_get_tasks_batch` - Query multiple tasks
- Information tools:
  - `producer_list_models` - List available FUZZ models
  - `producer_list_actions` - List available actions
  - `producer_get_lyric_format_guide` - Lyric formatting guide
- Support for all FUZZ models (2.0 Pro, 2.0, 2.0 Raw, 1.1 Pro, 1.0 Pro, 1.0, 1.1, 0.8)
- stdio and HTTP transport modes
- OAuth 2.1 support for hosted mode
- Comprehensive test suite
- Full documentation

[Unreleased]: https://github.com/AceDataCloud/ProducerMCP/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/AceDataCloud/ProducerMCP/releases/tag/v0.1.0
