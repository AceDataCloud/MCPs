"""Media conversion and upload tools for Producer API."""

from typing import Annotated

from pydantic import Field

from core.client import client
from core.server import mcp
from core.utils import format_upload_result, format_video_result, format_wav_result


@mcp.tool()
async def producer_upload_audio(
    audio_url: Annotated[
        str,
        Field(
            description="Public URL of the audio file to upload. The URL must be directly accessible (CDN link, cloud storage URL, etc.)."
        ),
    ],
) -> str:
    """Upload an external audio file for use in subsequent operations.

    Uploads audio from a URL so it can be used with actions like extend,
    cover, variation, swap_vocals, and swap_instrumentals.

    Use this when:
    - You have your own music you want to process with Producer
    - You want to use an external audio as a base for operations
    - You need to import audio into Producer's system

    After uploading, use the returned audio_id with other Producer tools.

    Returns:
        Upload result with audio ID for use in subsequent operations.
    """
    result = await client.upload_audio(audio_url=audio_url)
    return format_upload_result(result)


@mcp.tool()
async def producer_generate_video(
    audio_id: Annotated[
        str,
        Field(
            description="ID of the audio to generate a video for. This is the 'id' field from a previous generation result."
        ),
    ],
    callback_url: Annotated[
        str | None,
        Field(description="Webhook callback URL for asynchronous notifications."),
    ] = None,
) -> str:
    """Generate a video for a previously generated song.

    Creates a video with visualizations for a generated audio track.
    Useful for sharing on social media or video platforms.

    Use this when:
    - You want a video version of a generated song
    - You need to share the song on video platforms
    - You want a visual representation of the audio

    Returns:
        Task ID and video generation information.
    """
    result = await client.generate_video(
        audio_id=audio_id,
        callback_url=callback_url,
    )
    return format_video_result(result)


@mcp.tool()
async def producer_generate_wav(
    audio_id: Annotated[
        str,
        Field(description="ID of the audio to get the WAV format for."),
    ],
    callback_url: Annotated[
        str | None,
        Field(description="Webhook callback URL for asynchronous notifications."),
    ] = None,
) -> str:
    """Get the lossless WAV format of a generated song.

    Converts the song to high-quality uncompressed WAV format.
    WAV files are larger but have no quality loss compared to MP3.

    Use this when:
    - You need a lossless audio format for production
    - You want the highest quality audio output
    - You need uncompressed audio for further processing

    Returns:
        Task ID and WAV audio information.
    """
    result = await client.generate_wav(
        audio_id=audio_id,
        callback_url=callback_url,
    )
    return format_wav_result(result)
