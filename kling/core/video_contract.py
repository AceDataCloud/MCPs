"""Shared validation for Kling video, storyboard and asset tool requests."""

from core.types import (
    Duration,
    KlingCameraControl,
    KlingModel,
    KlingReferenceImage,
    KlingReferenceVideo,
    Mode,
)


def validate_video_request(
    *,
    model: KlingModel,
    mode: Mode,
    duration: Duration,
    generate_audio: bool | None,
    negative_prompt: str | None,
    cfg_scale: float | None,
    camera_control: KlingCameraControl | None,
    image_list: list[KlingReferenceImage] | None,
    video_list: list[KlingReferenceVideo] | None,
    element_count: int = 0,
    start_image_url: str | None = None,
    end_image_url: str | None = None,
) -> str | None:
    has_references = bool(image_list or video_list)
    uses_omni = model in ("kling-o1", "kling-v3-omni") or has_references

    if model == "kling-v3-turbo":
        if not 3 <= duration <= 15 or mode not in ("std", "pro"):
            return "Error: Turbo supports std/pro and integer durations 3–15."
        if generate_audio is False:
            return "Error: Turbo includes native audio with no off switch."
        if (
            has_references
            or end_image_url
            or any(value is not None for value in (negative_prompt, cfg_scale, camera_control))
        ):
            return "Error: Turbo does not support Omni references, tail frames, negative_prompt, cfg_scale or camera_control."
    elif model == "kling-o1":
        if duration != 5:
            return "Error: kling-o1 supports duration=5 only."
        if mode not in ("std", "pro"):
            return "Error: kling-o1 supports std and pro modes only."
        if generate_audio:
            return "Error: generate_audio is not supported by kling-o1."
    elif model in ("kling-v3", "kling-v3-omni"):
        if not 3 <= duration <= 15:
            return f"Error: {model} duration must be an integer from 3 to 15."
    elif duration not in (5, 10):
        return f"Error: {model} duration must be 5 or 10."

    if has_references and model not in ("kling-o1", "kling-v3-omni"):
        return f"Error: image_list and video_list are not supported by {model}."
    if uses_omni and any(
        value is not None for value in (negative_prompt, cfg_scale, camera_control)
    ):
        return "Error: negative_prompt, cfg_scale, and camera_control are not supported by Omni generation."
    if has_references and mode == "4k":
        return "Error: mode=4k is not supported with image_list or video_list."

    frame_count = int(bool(start_image_url)) + int(bool(end_image_url))
    reference_image_count = frame_count + len(image_list or []) + element_count
    max_images = 4 if video_list else 7
    if reference_image_count > max_images:
        return f"Error: this request supports at most {max_images} reference images including first/end frames."

    first_frame_count = int(bool(start_image_url)) + sum(
        item.type == "first_frame" for item in image_list or []
    )
    end_frame_count = int(bool(end_image_url)) + sum(
        item.type == "end_frame" for item in image_list or []
    )
    if first_frame_count > 1 or end_frame_count > 1:
        return "Error: provide at most one first frame and one end frame."
    if end_frame_count and not first_frame_count:
        return "Error: a first frame is required when an end frame is provided."

    if video_list:
        if len(video_list) != 1:
            return "Error: video_list must contain exactly one reference video."
        if generate_audio:
            return "Error: generate_audio cannot be used with video_list."
        if video_list[0].refer_type == "base" and (first_frame_count or end_frame_count):
            return "Error: an editable base video cannot be combined with first or end frames."

    return None
