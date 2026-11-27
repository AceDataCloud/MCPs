"""User-facing tools for Tripo's four JSON API resources."""

from typing import Any, Literal

from mcp.types import ToolAnnotations

from core.client import Resource, post
from core.options import (
    ConvertOptions,
    ExportFormat,
    GenerationModel,
    Motions,
    Prompt,
    RigFormat,
    TaskIds,
    TextureOptions,
    Views,
)
from core.server import mcp


def exactly_one(**values: object) -> None:
    if sum(value is not None for value in values.values()) != 1:
        raise ValueError("Provide exactly one of " + ", ".join(values))


async def submit(
    resource: Resource,
    action: str,
    callback_url: str | None,
    idempotency_key: str | None,
    **body: Any,
) -> dict[str, Any]:
    return await post(
        resource,
        {"action": action, "async": True, "callback_url": callback_url, **body},
        idempotency_key=idempotency_key,
    )


@mcp.tool()
async def tripo_generate_model(
    prompt: Prompt | None = None,
    image_url: str | None = None,
    image_urls: Views | None = None,
    model: GenerationModel = "v3.1-20260211",
    texture: Literal["none", "standard"] = "standard",
    callback_url: str | None = None,
    idempotency_key: str | None = None,
) -> dict[str, Any]:
    """Generate a 3D model from one prompt, one image, or ordered front/left/back/right views.
    For multiview include the front and at least one other image; null skips a side.
    This is a paid operation. Poll the returned task_id with tripo_get_task.
    """
    exactly_one(prompt=prompt, image_url=image_url, image_urls=image_urls)
    return await submit(
        "generations",
        "generate",
        callback_url,
        idempotency_key,
        prompt=prompt,
        image_url=image_url,
        image_urls=image_urls,
        model=model,
        texture=texture,
    )


@mcp.tool()
async def tripo_import_model(
    model_url: str, callback_url: str | None = None, idempotency_key: str | None = None
) -> dict[str, Any]:
    """Import a public HTTPS model file for free. Poll its task for the new model ID."""
    return await submit("models", "import", callback_url, idempotency_key, model_url=model_url)


@mcp.tool()
async def tripo_texture_model(
    model_id: str | None = None,
    model_url: str | None = None,
    prompt: Prompt | None = None,
    image_url: str | None = None,
    image_urls: Views | None = None,
    style_image_url: str | None = None,
    texture_quality: Literal["fast", "standard", "detailed", "extreme"] = "standard",
    options: TextureOptions | None = None,
    callback_url: str | None = None,
    idempotency_key: str | None = None,
) -> dict[str, Any]:
    """Apply a texture to an owned model ID or public URL. Use up to one text, image or multiview reference.
    A style image may accompany a text prompt. Texture quality determines the credit charge.
    """
    exactly_one(model_id=model_id, model_url=model_url)
    return await submit(
        "models",
        "texture",
        callback_url,
        idempotency_key,
        model_id=model_id,
        model_url=model_url,
        prompt=prompt,
        image_url=image_url,
        image_urls=image_urls,
        style_image_url=style_image_url,
        texture_quality=texture_quality,
        **(options.model_dump(exclude_none=True) if options else {}),
    )


@mcp.tool()
async def tripo_convert_model(
    format: ExportFormat,
    model_id: str | None = None,
    model_url: str | None = None,
    options: ConvertOptions | None = None,
    callback_url: str | None = None,
    idempotency_key: str | None = None,
) -> dict[str, Any]:
    """Convert an owned model ID or public URL. Non-default mesh or texture options can change the charge.
    Inspect the delivered format and optional ZIP container in the terminal task.
    """
    exactly_one(model_id=model_id, model_url=model_url)
    return await submit(
        "models",
        "convert",
        callback_url,
        idempotency_key,
        format=format,
        model_id=model_id,
        model_url=model_url,
        **(options.model_dump(exclude_none=True) if options else {}),
    )


@mcp.tool()
async def tripo_check_rig(
    model_id: str | None = None,
    model_url: str | None = None,
    callback_url: str | None = None,
    idempotency_key: str | None = None,
) -> dict[str, Any]:
    """Check riggability for free. A completed check returns riggable true or false."""
    exactly_one(model_id=model_id, model_url=model_url)
    return await submit(
        "animations",
        "rig_check",
        callback_url,
        idempotency_key,
        model_id=model_id,
        model_url=model_url,
    )


@mcp.tool()
async def tripo_rig_model(
    model_id: str | None = None,
    model_url: str | None = None,
    format: RigFormat = "GLB",
    model: Literal["v1.0-20240301", "v2.5-20260210", "v3.0-20260909"] | None = None,
    rig_type: Literal[
        "biped", "quadruped", "hexapod", "octopod", "avian", "serpentine", "aquatic", "others"
    ]
    | None = None,
    spec: Literal["tripo", "mixamo", "actorcore", "unity", "unreal", "vrm"] | None = None,
    callback_url: str | None = None,
    idempotency_key: str | None = None,
) -> dict[str, Any]:
    """Bind a skeleton to a model for a credit charge. Keep the rigged result ID for animation."""
    exactly_one(model_id=model_id, model_url=model_url)
    return await submit(
        "animations",
        "rig",
        callback_url,
        idempotency_key,
        model_id=model_id,
        model_url=model_url,
        format=format,
        model=model,
        rig_type=rig_type,
        spec=spec,
    )


@mcp.tool()
async def tripo_retarget_animation(
    model_id: str,
    animation: str | None = None,
    animations: Motions | None = None,
    format: RigFormat = "GLB",
    animate_in_place: bool | None = None,
    export_with_geometry: bool | None = None,
    callback_url: str | None = None,
    idempotency_key: str | None = None,
) -> dict[str, Any]:
    """Retarget an owned rigged asset using one preset or a list of up to five. Billed per preset.
    For example, use preset:walk or preset:idle. Poll the returned task ID for the exported animation.
    """
    exactly_one(animation=animation, animations=animations)
    return await submit(
        "animations",
        "retarget",
        callback_url,
        idempotency_key,
        model_id=model_id,
        animation=animation,
        animations=animations,
        format=format,
        animate_in_place=animate_in_place,
        export_with_geometry=export_with_geometry,
    )


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
async def tripo_get_task(id: str | None = None, trace_id: str | None = None) -> dict[str, Any]:
    """Read one existing task by its ID or trace ID for free. Missing tasks return an empty object."""
    exactly_one(id=id, trace_id=trace_id)
    return await post("tasks", {"id": id, "trace_id": trace_id})


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
async def tripo_get_tasks(
    ids: TaskIds | None = None, trace_ids: TaskIds | None = None
) -> dict[str, Any]:
    """Retrieve up to 100 task IDs or trace IDs for free. Items retain input order and missing slots are null."""
    exactly_one(ids=ids, trace_ids=trace_ids)
    return await post("tasks", {"action": "retrieve_batch", "ids": ids, "trace_ids": trace_ids})
