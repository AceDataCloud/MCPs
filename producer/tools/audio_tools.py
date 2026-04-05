"""Audio generation tools for Producer API."""

from typing import Annotated

from pydantic import Field

from core.client import client
from core.server import mcp
from core.types import DEFAULT_MODEL, ProducerModel
from core.utils import format_audio_result


@mcp.tool()
async def producer_generate_music(
    prompt: Annotated[
        str,
        Field(
            description="Description of the music to generate. Be descriptive about genre, mood, instruments, and theme. Examples: 'A happy birthday song with acoustic guitar', 'Epic orchestral battle music with dramatic choir', 'Chill lo-fi hip hop beat for studying'"
        ),
    ],
    model: Annotated[
        ProducerModel,
        Field(
            description="Producer model version. 'FUZZ-2.0' is the default and recommended for most use cases. 'FUZZ-2.0 Pro' offers the highest quality. 'FUZZ-2.0 Raw' provides raw unprocessed output."
        ),
    ] = DEFAULT_MODEL,
    instrumental: Annotated[
        bool,
        Field(
            description="If true, generate instrumental music without vocals. Default is false (with vocals)."
        ),
    ] = False,
    callback_url: Annotated[
        str | None,
        Field(
            description="Webhook callback URL for asynchronous notifications. When provided, the API will call this URL when the audio is generated."
        ),
    ] = None,
) -> str:
    """Generate AI music from a text prompt using Producer/Riffusion.

    This is the simplest way to create music - just describe what you want and
    Producer will automatically generate appropriate lyrics, melody, style, and
    arrangement.

    Use this when:
    - You want quick music generation with minimal input
    - You don't have specific lyrics in mind
    - You want the AI to be creative with the arrangement

    For full control over lyrics and style, use producer_generate_custom_music instead.

    Returns:
        Task ID and generated audio information including URLs, title, lyrics, and duration.
    """
    result = await client.generate_audio(
        action="generate",
        prompt=prompt,
        model=model,
        instrumental=instrumental,
        callback_url=callback_url,
    )
    return format_audio_result(result)


@mcp.tool()
async def producer_generate_custom_music(
    lyric: Annotated[
        str,
        Field(
            description="Song lyrics with section markers. Use [Verse], [Chorus], [Pre-Chorus], [Bridge], [Outro], [Intro] to structure the song. Example:\n[Verse 1]\nWalking down the empty street\nRain is falling at my feet\n\n[Chorus]\nBut I keep moving on\nUntil the break of dawn"
        ),
    ],
    title: Annotated[
        str,
        Field(description="Title of the song. Keep it concise and memorable."),
    ],
    style: Annotated[
        str,
        Field(
            description="Music style description. Be specific about genre, mood, tempo, and instruments. Examples: 'upbeat pop rock, energetic drums, electric guitar', 'acoustic folk, gentle, fingerpicking', 'dark electronic, synthwave, 80s retro'"
        ),
    ] = "",
    model: Annotated[
        ProducerModel,
        Field(
            description="Producer model version. 'FUZZ-2.0' or 'FUZZ-2.0 Pro' recommended for best quality."
        ),
    ] = DEFAULT_MODEL,
    instrumental: Annotated[
        bool,
        Field(
            description="If true, generate instrumental version (lyrics will be ignored). Default is false."
        ),
    ] = False,
    callback_url: Annotated[
        str | None,
        Field(description="Webhook callback URL for asynchronous notifications."),
    ] = None,
) -> str:
    """Generate AI music with full control over lyrics, title, and style.

    This gives you complete creative control over the song. You provide the lyrics
    with section markers, and Producer generates the melody and arrangement.

    Use this when:
    - You have specific lyrics you want to use
    - You want precise control over the music style
    - You need a specific song title

    For quick generation without writing lyrics, use producer_generate_music instead.

    Returns:
        Task ID and generated audio information including URLs, title, lyrics, and duration.
    """
    payload: dict = {
        "action": "generate",
        "custom": True,
        "lyric": lyric,
        "title": title,
        "model": model,
        "instrumental": instrumental,
        "callback_url": callback_url,
    }

    if style:
        payload["style"] = style

    result = await client.generate_audio(**payload)
    return format_audio_result(result)


@mcp.tool()
async def producer_extend_music(
    audio_id: Annotated[
        str,
        Field(
            description="ID of the audio to extend. This is the 'id' field from a previous generation result."
        ),
    ],
    continue_at: Annotated[
        float,
        Field(
            description="Timestamp in seconds where to start the extension. For example, 120.5 means continue from 2 minutes and 0.5 seconds into the song."
        ),
    ],
    lyric: Annotated[
        str,
        Field(
            description="Lyrics for the extended section. Use section markers like [Verse], [Chorus], [Bridge], [Outro]. The extension will continue from where the original song left off."
        ),
    ] = "",
    style: Annotated[
        str,
        Field(
            description="Music style for the extension. Leave empty to maintain the original style, or specify to change the style mid-song."
        ),
    ] = "",
    model: Annotated[
        ProducerModel,
        Field(description="Model version to use for the extension."),
    ] = DEFAULT_MODEL,
    callback_url: Annotated[
        str | None,
        Field(description="Webhook callback URL for asynchronous notifications."),
    ] = None,
) -> str:
    """Extend an existing song from a specific timestamp with new content.

    This allows you to continue a previously generated song, adding new sections
    like additional verses, a bridge, or an outro.

    Use this when:
    - A generated song is too short and you want to add more
    - You want to add a bridge or outro to an existing song
    - You're building a longer song piece by piece

    Returns:
        Task ID and the extended audio information.
    """
    payload: dict = {
        "action": "extend",
        "audio_id": audio_id,
        "continue_at": continue_at,
        "model": model,
        "callback_url": callback_url,
    }

    if lyric:
        payload["lyric"] = lyric
    if style:
        payload["style"] = style

    result = await client.generate_audio(**payload)
    return format_audio_result(result)


@mcp.tool()
async def producer_cover_music(
    audio_id: Annotated[
        str,
        Field(
            description="ID of the audio to create a cover of. This is the 'id' field from a previous generation."
        ),
    ],
    prompt: Annotated[
        str,
        Field(
            description="Description of how you want the cover to sound. Examples: 'acoustic unplugged version', 'jazz lounge style', '80s synthwave remix'"
        ),
    ] = "",
    style: Annotated[
        str,
        Field(
            description="Target music style for the cover. Examples: 'jazz, smooth, saxophone', 'acoustic folk, gentle guitar', 'electronic dance, high energy'"
        ),
    ] = "",
    model: Annotated[
        ProducerModel,
        Field(description="Model version to use for the cover."),
    ] = DEFAULT_MODEL,
    callback_url: Annotated[
        str | None,
        Field(description="Webhook callback URL for asynchronous notifications."),
    ] = None,
) -> str:
    """Create a cover or remix version of an existing song in a different style.

    This generates a new version of a song with a different arrangement, genre,
    or mood while keeping the core melody and lyrics.

    Use this when:
    - You want to hear a song in a different genre
    - You want an acoustic/unplugged version of an electronic song
    - You want to remix a song with a different vibe

    Returns:
        Task ID and the cover audio information.
    """
    payload: dict = {
        "action": "cover",
        "audio_id": audio_id,
        "model": model,
        "callback_url": callback_url,
    }

    if prompt:
        payload["prompt"] = prompt
    if style:
        payload["style"] = style

    result = await client.generate_audio(**payload)
    return format_audio_result(result)


@mcp.tool()
async def producer_variation_music(
    audio_id: Annotated[
        str,
        Field(description="ID of the audio to create a variation of."),
    ],
    prompt: Annotated[
        str,
        Field(
            description="Description of the desired variation. Examples: 'more upbeat tempo', 'darker mood', 'add more bass'"
        ),
    ] = "",
    style: Annotated[
        str,
        Field(
            description="Music style for the variation. Examples: 'faster tempo, more energy', 'softer, more intimate', 'heavier, more distortion'"
        ),
    ] = "",
    model: Annotated[
        ProducerModel,
        Field(description="Model version to use for the variation."),
    ] = DEFAULT_MODEL,
    callback_url: Annotated[
        str | None,
        Field(description="Webhook callback URL for asynchronous notifications."),
    ] = None,
) -> str:
    """Create a variation of an existing song with modifications.

    Generates a new version of the song with subtle changes to the arrangement,
    melody, or style while keeping the overall structure similar.

    Use this when:
    - You like a song but want a slightly different version
    - You want to explore different interpretations of the same idea
    - You need multiple takes of a similar song

    Returns:
        Task ID and the variation audio information.
    """
    payload: dict = {
        "action": "variation",
        "audio_id": audio_id,
        "model": model,
        "callback_url": callback_url,
    }

    if prompt:
        payload["prompt"] = prompt
    if style:
        payload["style"] = style

    result = await client.generate_audio(**payload)
    return format_audio_result(result)


@mcp.tool()
async def producer_swap_vocals(
    audio_id: Annotated[
        str,
        Field(description="ID of the base audio whose vocals will be replaced."),
    ],
    swap_audio_id: Annotated[
        str,
        Field(description="ID of the audio whose vocals to use as replacement."),
    ],
    callback_url: Annotated[
        str | None,
        Field(description="Webhook callback URL for asynchronous notifications."),
    ] = None,
) -> str:
    """Swap the vocals of one song with vocals from another song.

    Takes the instrumental track from the base audio and combines it with
    the vocal track from the swap audio.

    Use this when:
    - You want to combine vocals from one song with instrumentals from another
    - You want to hear how different vocals sound over the same beat
    - You're creating a vocal mashup

    Returns:
        Task ID and the swapped audio information.
    """
    result = await client.generate_audio(
        action="swap_vocals",
        audio_id=audio_id,
        swap_audio_id=swap_audio_id,
        callback_url=callback_url,
    )
    return format_audio_result(result)


@mcp.tool()
async def producer_swap_instrumentals(
    audio_id: Annotated[
        str,
        Field(description="ID of the base audio whose instrumentals will be replaced."),
    ],
    swap_audio_id: Annotated[
        str,
        Field(description="ID of the audio whose instrumentals to use as replacement."),
    ],
    callback_url: Annotated[
        str | None,
        Field(description="Webhook callback URL for asynchronous notifications."),
    ] = None,
) -> str:
    """Swap the instrumental track of one song with instrumentals from another.

    Takes the vocals from the base audio and combines them with the instrumental
    track from the swap audio.

    Use this when:
    - You want to combine instrumentals from one song with vocals from another
    - You want to hear how the same vocals sound over different music
    - You're creating an instrumental mashup

    Returns:
        Task ID and the swapped audio information.
    """
    result = await client.generate_audio(
        action="swap_instrumentals",
        audio_id=audio_id,
        swap_audio_id=swap_audio_id,
        callback_url=callback_url,
    )
    return format_audio_result(result)


@mcp.tool()
async def producer_replace_section(
    audio_id: Annotated[
        str,
        Field(description="ID of the audio to replace a section in."),
    ],
    replace_section_start: Annotated[
        float,
        Field(description="Start time in seconds of the section to replace."),
    ],
    replace_section_end: Annotated[
        float,
        Field(description="End time in seconds of the section to replace."),
    ],
    lyric: Annotated[
        str | None,
        Field(
            description="New lyrics for the replaced section. Use section markers like [Verse], [Chorus]."
        ),
    ] = None,
    style: Annotated[
        str,
        Field(description="Music style for the replaced section."),
    ] = "",
    model: Annotated[
        ProducerModel,
        Field(description="Model version to use."),
    ] = DEFAULT_MODEL,
    callback_url: Annotated[
        str | None,
        Field(description="Webhook callback URL for asynchronous notifications."),
    ] = None,
) -> str:
    """Replace a specific time range in a song with new generated content.

    Re-generates a portion of a song between the specified start and end times,
    keeping the rest of the song unchanged. Great for fixing sections you don't
    like.

    Use this when:
    - A specific section of a song needs improvement
    - You want to change lyrics in the middle of a song
    - You want to replace a verse or chorus with something different

    Returns:
        Task ID and the updated audio information.
    """
    payload: dict = {
        "action": "replace_section",
        "audio_id": audio_id,
        "replace_section_start": replace_section_start,
        "replace_section_end": replace_section_end,
        "model": model,
        "callback_url": callback_url,
    }

    if lyric:
        payload["lyric"] = lyric
    if style:
        payload["style"] = style

    result = await client.generate_audio(**payload)
    return format_audio_result(result)


@mcp.tool()
async def producer_stems_music(
    audio_id: Annotated[
        str,
        Field(description="ID of the audio to separate into stems."),
    ],
    callback_url: Annotated[
        str | None,
        Field(description="Webhook callback URL for asynchronous notifications."),
    ] = None,
) -> str:
    """Separate a song into individual stems (vocals and instruments).

    Splits the audio into separate tracks for vocals and instrumentals,
    useful for remixing, karaoke, or isolating specific parts.

    Use this when:
    - You want to separate vocals from instrumentals
    - You need individual stem tracks for mixing
    - You want to create a karaoke version

    Returns:
        Task ID and stem separation results with individual track URLs.
    """
    result = await client.generate_audio(
        action="stems",
        audio_id=audio_id,
        callback_url=callback_url,
    )
    return format_audio_result(result)
