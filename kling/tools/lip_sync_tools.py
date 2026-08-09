"""Lip-sync and talking-photo tools for Kling API."""

from typing import Annotated

from pydantic import Field

from core.client import client
from core.server import mcp
from core.types import (
    DEFAULT_TALKING_PHOTO_DURATION,
    DEFAULT_TALKING_PHOTO_MODE,
    DEFAULT_TALKING_PHOTO_MODEL,
    LipSyncAudioType,
    LipSyncMode,
    TalkingPhotoDuration,
    TalkingPhotoMode,
    TalkingPhotoModel,
    VoiceLanguage,
)
from core.utils import format_video_result


@mcp.tool()
async def kling_lip_sync(
    mode: Annotated[
        LipSyncMode,
        Field(
            description="Lip-sync mode. 'audio2video' to drive lips from an audio file or URL; 'text2video' to generate speech from text and drive the video."
        ),
    ],
    video_url: Annotated[
        str | None,
        Field(
            description="URL of the source video whose lip movements will be replaced. Provide either video_url or video_id."
        ),
    ] = None,
    video_id: Annotated[
        str | None,
        Field(
            description="Task ID of a previously generated video to use as the source. Provide either video_url or video_id."
        ),
    ] = None,
    audio_url: Annotated[
        str | None,
        Field(
            description="URL of the driving audio. Required when mode='audio2video' and audio_type='url'."
        ),
    ] = None,
    audio_type: Annotated[
        LipSyncAudioType,
        Field(
            description="Audio source type. 'url' (default) to supply audio_url; 'file' to supply audio_file as a base64-encoded string."
        ),
    ] = "url",
    audio_file: Annotated[
        str | None,
        Field(
            description="Base64-encoded audio file content. Required when mode='audio2video' and audio_type='file'."
        ),
    ] = None,
    text: Annotated[
        str | None,
        Field(description="Text to convert to speech. Required when mode='text2video'."),
    ] = None,
    voice_id: Annotated[
        str | None,
        Field(description="Voice ID to use for text-to-speech synthesis (mode='text2video')."),
    ] = None,
    voice_language: Annotated[
        VoiceLanguage,
        Field(
            description="Language of the TTS voice. 'zh' for Chinese (default), 'en' for English. Used when mode='text2video'."
        ),
    ] = "zh",
    voice_speed: Annotated[
        float | None,
        Field(
            ge=0.8,
            le=2.0,
            description="Speech speed multiplier from 0.8 to 2.0 (default 1.0). Used when mode='text2video'.",
        ),
    ] = None,
    callback_url: Annotated[
        str | None,
        Field(description="Webhook URL that receives a POST when the lip-sync task completes."),
    ] = None,
) -> str:
    """Synchronize lip movements in a video to match a given audio track or text.

    Takes an existing video (by URL or task ID) and replaces the speaker's lip
    movements so they match the provided audio. In 'text2video' mode the audio
    is generated from the supplied text via TTS.

    Use this when:
    - You want to dub a video into a different language
    - You want to replace the audio of a generated video with custom speech
    - You want to create a talking-head video from text

    Returns:
        Task ID and lip-sync video information.
    """
    if not video_url and not video_id:
        return '{"error": "Validation Error", "message": "Either video_url or video_id is required."}'
    if mode == "audio2video" and not audio_url and not audio_file:
        return '{"error": "Validation Error", "message": "audio_url or audio_file is required when mode=\'audio2video\'."}'
    if mode == "text2video" and not text:
        return '{"error": "Validation Error", "message": "text is required when mode=\'text2video\'."}'

    payload: dict = {"mode": mode}

    if video_url:
        payload["video_url"] = video_url
    if video_id:
        payload["video_id"] = video_id
    if audio_url:
        payload["audio_url"] = audio_url
    if audio_type != "url":
        payload["audio_type"] = audio_type
    if audio_file:
        payload["audio_file"] = audio_file
    if text:
        payload["text"] = text
    if voice_id:
        payload["voice_id"] = voice_id
    if voice_language != "zh":
        payload["voice_language"] = voice_language
    if voice_speed is not None:
        payload["voice_speed"] = voice_speed
    if callback_url:
        payload["callback_url"] = callback_url

    result = await client.lip_sync(**payload)
    return format_video_result(result)


@mcp.tool()
async def kling_talking_photo(
    image_url: Annotated[
        str,
        Field(
            description="URL of the portrait image to animate. Should be a clear frontal face photo."
        ),
    ],
    audio_url: Annotated[
        str,
        Field(description="URL of the audio file that drives the talking animation."),
    ],
    model: Annotated[
        TalkingPhotoModel,
        Field(
            description="Kling model version. Default is 'kling-v2-1-master'. Options: kling-v1, kling-v1-6, kling-v2-master, kling-v2-1-master, kling-v2-5-turbo, kling-v2-6."
        ),
    ] = DEFAULT_TALKING_PHOTO_MODEL,
    duration: Annotated[
        TalkingPhotoDuration,
        Field(description="Video duration in seconds. Options: 5 (default) or 10."),
    ] = DEFAULT_TALKING_PHOTO_DURATION,
    mode: Annotated[
        TalkingPhotoMode,
        Field(
            description="Generation quality mode. 'pro' (default) for higher quality; 'std' for faster generation."
        ),
    ] = DEFAULT_TALKING_PHOTO_MODE,
    prompt: Annotated[
        str | None,
        Field(description="Optional text description to guide the animation style or content."),
    ] = None,
    callback_url: Annotated[
        str | None,
        Field(
            description="Webhook URL that receives a POST when the talking-photo task completes."
        ),
    ] = None,
) -> str:
    """Animate a portrait photo to match a provided audio track (talking-photo).

    Given a face image and an audio file, generates a short video where the
    portrait's lips, expressions, and head movements are synchronized to the audio.

    Use this when:
    - You want to create a talking-head video from a static photo
    - You want to make a person in a photo appear to speak
    - You need a quick avatar video without real footage

    Returns:
        Task ID and talking-photo video information.
    """
    payload: dict = {
        "image_url": image_url,
        "audio_url": audio_url,
        "model": model,
        "duration": duration,
        "mode": mode,
    }

    if prompt:
        payload["prompt"] = prompt
    if callback_url:
        payload["callback_url"] = callback_url

    result = await client.talking_photo(**payload)
    return format_video_result(result)
