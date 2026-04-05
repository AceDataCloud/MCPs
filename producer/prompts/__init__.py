"""Prompt templates for Producer MCP server.

MCP Prompts provide guidance to LLMs on when and how to use the available tools.
These are exposed via the MCP protocol and help LLMs make better decisions.
"""

from core.server import mcp


@mcp.prompt()
def producer_music_generation_guide() -> str:
    """Guide for choosing the right Producer tool for music generation."""
    return """# Producer Music Generation Guide

When the user wants to generate music, choose the appropriate tool based on their needs:

## Quick Generation
**Tool:** `producer_generate_music`
**Use when:**
- User gives a simple description: "make me a birthday song"
- User wants Producer to handle lyrics and arrangement
- Quick, low-effort music creation

**Example:** "Create an upbeat pop song about summer"
-> Call `producer_generate_music` with prompt="An upbeat pop song about summer, fun, beach vibes, catchy melody"

## Custom Generation (Full Control)
**Tool:** `producer_generate_custom_music`
**Use when:**
- User provides specific lyrics
- User wants control over title and style

**Example:** "Here are my lyrics: [Verse] Walking in the rain..."
-> Call `producer_generate_custom_music` with the provided lyrics, a title, and appropriate style

## Extending Songs
**Tool:** `producer_extend_music`
**Use when:**
- User wants to make a song longer
- User wants to add more sections to an existing song
- Building a multi-part composition

## Creating Covers
**Tool:** `producer_cover_music`
**Use when:**
- User wants a different version of an existing song
- "Make it jazz", "acoustic version", "remix"

## Creating Variations
**Tool:** `producer_variation_music`
**Use when:**
- User wants a slightly different version of a song
- User wants to explore alternatives

## Vocal/Instrumental Swapping
**Tools:** `producer_swap_vocals`, `producer_swap_instrumentals`
**Use when:**
- User wants to combine vocals from one song with instrumentals from another
- Creating mashups between songs

## Generating Lyrics Only
**Tool:** `producer_generate_lyrics`
**Use when:**
- User wants lyrics without music yet
- User wants to review/edit lyrics before generating music

## Checking Status
**Tool:** `producer_get_task`
**Use when:**
- Generation takes time and user wants to check if it's ready
- User asks "is my song done?"
- A generation tool returned only a task_id and you need the final audio URLs

## Important Notes:
1. Music generation is async in MCP - generation tools should return quickly with a task_id
2. After any generate/extend/cover/variation/stems/media call, use `producer_get_task` to poll for the final result
3. Default model is FUZZ-2.0 (good balance of quality and speed)
4. For best quality, use FUZZ-2.0 Pro
"""


@mcp.prompt()
def producer_workflow_examples() -> str:
    """Common workflow examples for Producer music generation."""
    return """# Producer Workflow Examples

## Workflow 1: Quick Song Generation
1. User: "Make me a rock song about freedom"
2. Call `producer_generate_music(prompt="Rock song about freedom, electric guitars, powerful drums, anthemic")`
3. Return the task_id from the submission response
4. Poll with `producer_get_task(task_id)` until the task finishes and audio URLs appear

## Workflow 2: Custom Song with User's Lyrics
1. User provides lyrics
2. Ask for title and style preferences if not provided
3. Call `producer_generate_custom_music(lyric=user_lyrics, title="...", style="...")`
4. Poll with `producer_get_task(task_id)` for the completed audio

## Workflow 3: Creating a Long Song
1. Generate initial song with `producer_generate_music`
2. Get the audio_id from the result
3. Call `producer_extend_music(audio_id, lyric=new_lyrics, continue_at=song_duration)`
4. Repeat step 3 as needed

## Workflow 4: Cover/Remix
1. User has a song_id they want to remix
2. User describes the new style
3. Call `producer_cover_music(audio_id, prompt="jazz version", style="smooth jazz, saxophone")`
4. Poll with `producer_get_task(task_id)` for the completed cover

## Workflow 5: Vocal Mashup
1. Generate or identify two songs
2. Call `producer_swap_vocals(audio_id=song_a, swap_audio_id=song_b)` to put song_b's vocals on song_a's music
3. Poll with `producer_get_task(task_id)` for the result

## Workflow 6: Fix a Section
1. User doesn't like a part of a song
2. Call `producer_replace_section(audio_id, replace_section_start=30, replace_section_end=60)`
3. Poll with `producer_get_task(task_id)` for the updated song

## Tips:
- Always be descriptive in prompts - include genre, mood, instruments, tempo
- For lyrics, use section markers like [Verse], [Chorus], [Bridge]
- Use `producer_list_models` to see all available models
"""


@mcp.prompt()
def producer_prompt_suggestions() -> str:
    """Style and prompt writing suggestions for Producer."""
    return """# Producer Style Prompt Guide

## Effective Prompt Writing

Good prompts include:
- **Genre:** pop, rock, jazz, classical, electronic, hip-hop, country, R&B, metal, folk
- **Mood:** happy, sad, energetic, calm, dark, uplifting, romantic, aggressive
- **Instruments:** guitar, piano, drums, synthesizer, violin, saxophone, bass
- **Tempo:** slow, mid-tempo, fast, upbeat, ballad
- **Era/Style:** 80s, 90s, modern, vintage, retro, futuristic

## Example Prompts by Genre

**Pop:**
"Catchy pop song, upbeat, synth hooks, danceable, modern production"

**Rock:**
"Hard rock anthem, electric guitars, powerful drums, stadium rock feel"

**Jazz:**
"Smooth jazz, saxophone solo, walking bass, brushed drums, late night vibe"

**Electronic:**
"EDM banger, heavy bass drops, synth arpeggios, festival energy"

**Classical:**
"Orchestral piece, strings, dramatic, cinematic, emotional crescendo"

**Folk:**
"Acoustic folk, fingerpicking guitar, gentle vocals, storytelling"

**Hip-Hop:**
"Trap beat, 808 bass, hi-hats, confident flow, modern hip-hop"

## Model Selection Guide

- **FUZZ-2.0 Pro:** Best quality, ideal for final production
- **FUZZ-2.0:** Great default, good balance of quality and variety
- **FUZZ-2.0 Raw:** Unprocessed output, use when you plan to post-process
- **FUZZ-1.x:** Legacy models, use for specific sonic characteristics

## Lyric Section Tips

Each section has a purpose:
- **[Intro]:** Set the mood, can be instrumental
- **[Verse]:** Tell the story, build narrative
- **[Pre-Chorus]:** Build tension before the hook
- **[Chorus]:** The catchiest, most memorable part
- **[Bridge]:** Contrast, often emotional peak
- **[Outro]:** Wind down, resolve the song
"""
