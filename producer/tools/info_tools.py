"""Informational tools for Producer API."""

from core.server import mcp


@mcp.tool()
async def producer_list_models() -> str:
    """List all available Producer/FUZZ models and their capabilities.

    Shows all available model versions with their features and
    recommended use cases. Use this to understand which model to choose
    for your music generation.

    Returns:
        Table of all models with their version and features.
    """
    # Last updated: 2026-04-05
    return """Available Producer/FUZZ Models:

| Model            | Tier    | Description                                      |
|------------------|---------|--------------------------------------------------|
| FUZZ-2.0 Pro     | Pro     | Highest quality, best for professional production |
| FUZZ-2.0         | Default | Recommended for most use cases (default)          |
| FUZZ-2.0 Raw     | Raw     | Unprocessed output, for custom post-processing    |
| FUZZ-1.1 Pro     | Pro     | High quality legacy model                         |
| FUZZ-1.0 Pro     | Pro     | Professional legacy model                         |
| FUZZ-1.0         | Default | Stable legacy model                               |
| FUZZ-1.1         | Default | Improved legacy model                              |
| FUZZ-0.8         | Legacy  | Original model, basic quality                      |

Recommended: FUZZ-2.0 for general use, FUZZ-2.0 Pro for best quality.
"""


@mcp.tool()
async def producer_list_actions() -> str:
    """List all available Producer API actions and corresponding tools.

    Reference guide for what each action does and which tool to use.
    Helpful for understanding the full capabilities of the Producer MCP.

    Returns:
        Categorized list of all actions and their corresponding tools.
    """
    # Last updated: 2026-04-05
    return """Available Producer Actions and Tools:

Music Generation:
- producer_generate_music: Create music from a simple text prompt
- producer_generate_custom_music: Create music with custom lyrics and style
- producer_extend_music: Continue an existing song from a specific timestamp
- producer_cover_music: Create a cover/remix version of a song
- producer_variation_music: Create a variation of an existing song

Vocal & Instrumental Manipulation:
- producer_swap_vocals: Swap vocals from one song onto another
- producer_swap_instrumentals: Swap instrumentals from one song onto another

Editing:
- producer_replace_section: Replace a specific time range with new content

Stems & Extraction:
- producer_stems_music: Separate a song into vocal and instrumental stems

Upload:
- producer_upload_audio: Upload external audio for processing

Media Conversion:
- producer_generate_video: Generate video for a song
- producer_generate_wav: Get lossless WAV format of a song

Lyrics:
- producer_generate_lyrics: Generate song lyrics from a prompt

Task Management:
- producer_get_task: Check status of a single generation
- producer_get_tasks_batch: Check status of multiple generations

Information:
- producer_list_models: Show available models and their capabilities
- producer_list_actions: Show this action reference (you are here)
- producer_get_lyric_format_guide: Show how to format lyrics

Workflow Examples:
1. Quick song: producer_generate_music -> producer_get_task
2. Custom song: producer_generate_lyrics -> producer_generate_custom_music -> producer_get_task
3. Long song: producer_generate_music -> producer_extend_music (repeat)
4. Cover: producer_cover_music -> producer_get_task
5. Mashup: producer_swap_vocals or producer_swap_instrumentals
6. Fix section: producer_replace_section -> producer_get_task
7. Your own music: producer_upload_audio -> producer_extend_music or producer_cover_music
"""


@mcp.tool()
async def producer_get_lyric_format_guide() -> str:
    """Get guidance on formatting lyrics for Producer music generation.

    Shows how to structure lyrics with section markers for best results.
    Following this format helps Producer understand the song structure and
    generate appropriate melodies for each section.

    Returns:
        Complete guide with section markers, examples, and tips.
    """
    # Last updated: 2026-04-05
    return """Lyric Format Guide for Producer:

Section Markers (use square brackets):
- [Verse] or [Verse 1], [Verse 2]: Main storytelling sections
- [Chorus]: Repeated catchy section (the hook)
- [Pre-Chorus]: Build-up before chorus
- [Bridge]: Contrasting section, usually near the end
- [Outro]: Ending section
- [Intro]: Opening instrumental or vocals

Example Structure:
```
[Verse 1]
First verse lyrics here
Setting up the story

[Pre-Chorus]
Building anticipation
Leading to the hook

[Chorus]
The main hook goes here
Most memorable part
Repeat this section

[Verse 2]
Second verse continues
The narrative unfolds

[Chorus]
The main hook goes here
Most memorable part
Repeat this section

[Bridge]
Something different here
A twist or climax

[Chorus]
The main hook goes here
Most memorable part
Final repetition

[Outro]
Winding down
Fade out
```

Tips for Best Results:
- Keep lines concise (4-8 words) for better singing flow
- Use simple, clear language that's easy to sing
- Include rhymes for catchiness (especially in chorus)
- Leave some creative freedom for the AI
- Use consistent line lengths within sections
- End verses with a lead-in to the chorus
"""
