"""Unit tests for image tools."""

import json
from pathlib import Path
from typing import Any

import pytest
from mcp.server.fastmcp.exceptions import ToolError

from core.server import mcp
from tools import image_tools


def test_openai_edit_image_schema_accepts_single_or_multiple_images():
    """The MCP schema must expose the API's string-or-array contract."""
    tool = next(tool for tool in mcp._tool_manager.list_tools() if tool.name == "openai_edit_image")
    image_schema = tool.parameters["properties"]["image"]

    assert image_schema["anyOf"] == [
        {"type": "string"},
        {
            "items": {"type": "string"},
            "maxItems": 16,
            "minItems": 1,
            "type": "array",
        },
    ]
    assert "Never join multiple URLs with commas" in image_schema["description"]
    assert "never JSON-stringify the array" in image_schema["description"]


@pytest.mark.asyncio
async def test_openai_edit_image_forwards_image_array(monkeypatch):
    """Multiple image URLs must remain an array in the API payload."""
    captured_payload: dict[str, object] = {}

    async def mock_images_edits(**kwargs):
        captured_payload.update(kwargs)
        return {"data": [{"url": "https://example.com/edited.png"}]}

    monkeypatch.setattr(image_tools.client, "images_edits", mock_images_edits)
    images = [
        "https://example.com/base.png",
        "https://example.com/logo.png",
    ]

    response = await image_tools.openai_edit_image(
        image=images,
        prompt="Replace the base image logo with the reference logo.",
        model="gpt-image-2",
    )

    assert captured_payload["image"] == images
    assert json.loads(response) == {"data": [{"url": "https://example.com/edited.png"}]}


@pytest.mark.asyncio
async def test_openai_edit_image_uses_auto_size_by_default(monkeypatch):
    """Image editing should preserve the reference image aspect ratio by default."""
    captured_payload: dict[str, object] = {}

    async def mock_images_edits(**kwargs):
        captured_payload.update(kwargs)
        return {"task_id": "t-0"}

    monkeypatch.setattr(image_tools.client, "images_edits", mock_images_edits)

    await image_tools.openai_edit_image(
        image="https://example.com/base.png",
        prompt="Remove the background.",
        model="gpt-image-2",
    )

    assert captured_payload["size"] == "auto"


@pytest.mark.asyncio
async def test_openai_generate_image_submits_async(monkeypatch):
    """Generation must be submitted asynchronously so slow models don't time out."""
    captured_payload: dict[str, object] = {}

    async def mock_images_generations(**kwargs):
        captured_payload.update(kwargs)
        return {"task_id": "t-1"}

    monkeypatch.setattr(image_tools.client, "images_generations", mock_images_generations)

    await image_tools.openai_generate_image(prompt="a panda", model="gpt-image-1")

    assert captured_payload["async"] is True


@pytest.mark.asyncio
async def test_openai_generate_image_uses_auto_size_by_default(monkeypatch):
    """Generation should let the model choose dimensions by default, as the API does."""
    captured_payload: dict[str, object] = {}

    async def mock_images_generations(**kwargs):
        captured_payload.update(kwargs)
        return {"task_id": "t-3"}

    monkeypatch.setattr(image_tools.client, "images_generations", mock_images_generations)

    await image_tools.openai_generate_image(prompt="a panda", model="gpt-image-1")

    assert captured_payload["size"] == "auto"


def test_openai_edit_image_schema_omits_partial_images():
    """JSON edits endpoint doesn't accept partial_images; tool schema must not expose it."""
    tool = next(tool for tool in mcp._tool_manager.list_tools() if tool.name == "openai_edit_image")
    assert "partial_images" not in tool.parameters["properties"]


@pytest.mark.asyncio
async def test_openai_generate_image_defers_to_explicit_callback_url(monkeypatch):
    """An explicit callback_url already implies async upstream — don't double-flag it."""
    captured_payload: dict[str, object] = {}

    async def mock_images_generations(**kwargs):
        captured_payload.update(kwargs)
        return {"task_id": "t-2"}

    monkeypatch.setattr(image_tools.client, "images_generations", mock_images_generations)

    await image_tools.openai_generate_image(
        prompt="a panda",
        model="gpt-image-1",
        callback_url="https://example.com/hook",
    )

    assert "async" not in captured_payload
    assert captured_payload["callback_url"] == "https://example.com/hook"


def test_openai_image_tools_expose_async_parameter():
    """The MCP schema should expose the API's async request-body parameter."""
    tools = {tool.name: tool for tool in mcp._tool_manager.list_tools()}

    assert "async" in tools["openai_generate_image"].parameters["properties"]
    assert "async" in tools["openai_edit_image"].parameters["properties"]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("tool_name", "arguments", "client_method"),
    [
        (
            "openai_generate_image",
            {"prompt": "a panda", "model": "gpt-image-1"},
            "images_generations_async",
        ),
        (
            "openai_edit_image",
            {
                "image": "https://example.com/base.png",
                "prompt": "Remove the background.",
                "model": "gpt-image-2",
            },
            "images_edits_async",
        ),
    ],
)
async def test_fastmcp_dispatch_maps_public_async_parameter(
    monkeypatch: pytest.MonkeyPatch,
    tool_name: str,
    arguments: dict[str, object],
    client_method: str,
) -> None:
    captured_payload: dict[str, object] = {}

    async def mock_request(**kwargs: Any) -> dict[str, list[dict[str, str]]]:
        captured_payload.update(kwargs)
        return {"data": [{"url": "https://example.com/image.png"}]}

    monkeypatch.setattr(image_tools.client, client_method, mock_request)
    tools = {tool.name: tool for tool in await mcp.list_tools()}
    properties = tools[tool_name].inputSchema["properties"]

    assert "async" in properties
    assert "async_" not in properties

    result = await mcp.call_tool(tool_name, {**arguments, "async": False})

    assert result
    assert captured_payload["async"] is False


@pytest.mark.asyncio
async def test_openai_generate_image_preserves_explicit_sync(monkeypatch):
    """Callers can opt out of the default async submission when the API supports it."""
    captured_payload: dict[str, object] = {}

    async def mock_images_generations(**kwargs):
        captured_payload.update(kwargs)
        return {"data": [{"url": "https://example.com/image.png"}]}

    monkeypatch.setattr(image_tools.client, "images_generations", mock_images_generations)

    await image_tools.openai_generate_image(
        prompt="a panda",
        model="gpt-image-1",
        async_=False,
    )

    assert captured_payload["async"] is False


@pytest.mark.asyncio
@pytest.mark.parametrize("quality", ["xhigh", "max"])
@pytest.mark.parametrize(
    "model",
    [
        "gpt-image-2.5-flare",
        "gpt-image-2.6-flare",
        "gpt-image-2.5-flare:reverse",
        "gpt-image-2.6-flare:reverse",
        "gpt-image-2.5-flare:official",
        "gpt-image-2.6-flare:official",
        "gpt-image-2.5-sunburst",
        "gpt-image-2.6-sunburst",
        "gpt-image-2.5-sunburst:reverse",
        "gpt-image-2.6-sunburst:reverse",
        "gpt-image-2.5-sunburst:official",
        "gpt-image-2.6-sunburst:official",
    ],
)
@pytest.mark.parametrize("tool_name", ["openai_generate_image", "openai_edit_image"])
async def test_image_quality_schema_and_dispatch(monkeypatch, tool_name, model, quality):
    captured = {}

    async def mock_request(endpoint, payload):
        expected_endpoint = (
            "/openai/images/generations"
            if tool_name == "openai_generate_image"
            else "/openai/images/edits"
        )
        assert endpoint == expected_endpoint
        captured.update(payload)
        return {"task_id": "test-task-123"}

    monkeypatch.setattr(image_tools.client, "request", mock_request)
    tool = next(tool for tool in await mcp.list_tools() if tool.name == tool_name)
    schema = tool.inputSchema["properties"]["quality"]
    assert {"auto", "high", "medium", "low", "xhigh", "max", "standard"} <= set(schema["enum"])
    assert ("hd" in schema["enum"]) == (tool_name == "openai_generate_image")
    assert "GPT Image 2.5 and 2.6 Flare/Sunburst" in schema["description"]
    assert "including ':reverse' and ':official'" in schema["description"]
    assert model in tool.inputSchema["properties"]["model"]["enum"]
    arguments = {"prompt": "test", "model": model, "quality": quality}
    if tool_name == "openai_edit_image":
        arguments["image"] = "https://example.com/base.png"
    await mcp.call_tool(tool_name, arguments)
    assert captured["model"] == model
    assert captured["quality"] == quality


def test_openai_image_tool_schemas_expose_exact_gpt_image_2_5_models():
    tools = {tool.name: tool for tool in mcp._tool_manager.list_tools()}
    expected = {
        "gpt-image-2.5-flare",
        "gpt-image-2.6-flare",
        "gpt-image-2.5-flare:reverse",
        "gpt-image-2.6-flare:reverse",
        "gpt-image-2.5-flare:official",
        "gpt-image-2.6-flare:official",
        "gpt-image-2.5-sunburst",
        "gpt-image-2.6-sunburst",
        "gpt-image-2.5-sunburst:reverse",
        "gpt-image-2.6-sunburst:reverse",
        "gpt-image-2.5-sunburst:official",
        "gpt-image-2.6-sunburst:official",
    }
    for name in ("openai_generate_image", "openai_edit_image"):
        model_schema = tools[name].parameters["properties"]["model"]
        models = set(model_schema["enum"])
        assert expected <= models
        assert "gpt-image-2.5" not in models
        assert "gpt-image-2.5:official" not in models
        assert "gpt-image-2.5:reverse" not in models
        manifest = json.loads((Path(__file__).parents[1] / "lobehub/lhm.plugin.json").read_text())
        listing = next(tool for tool in manifest["tools"] if tool["name"] == name)
        for field in ("model", "quality"):
            assert (
                listing["inputSchema"]["properties"][field]
                == tools[name].parameters["properties"][field]
            )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "model",
    [
        "gpt-image-2.5-flare",
        "gpt-image-2.6-flare",
        "gpt-image-2.5-flare:reverse",
        "gpt-image-2.6-flare:reverse",
        "gpt-image-2.5-flare:official",
        "gpt-image-2.6-flare:official",
        "gpt-image-2.5-sunburst",
        "gpt-image-2.6-sunburst",
        "gpt-image-2.5-sunburst:reverse",
        "gpt-image-2.6-sunburst:reverse",
        "gpt-image-2.5-sunburst:official",
        "gpt-image-2.6-sunburst:official",
    ],
)
async def test_openai_image_tools_forward_gpt_image_2_5_models(monkeypatch, model):
    generated: dict[str, object] = {}
    edited: dict[str, object] = {}

    async def mock_generate(**kwargs):
        generated.update(kwargs)
        return {"task_id": "generated"}

    async def mock_edit(**kwargs):
        edited.update(kwargs)
        return {"task_id": "edited"}

    monkeypatch.setattr(image_tools.client, "images_generations", mock_generate)
    monkeypatch.setattr(image_tools.client, "images_edits", mock_edit)
    await image_tools.openai_generate_image(prompt="a circle", model=model)
    await image_tools.openai_edit_image(
        image="https://example.com/source.png", prompt="make it red", model=model
    )
    assert generated["model"] == model
    assert edited["model"] == model


def test_image_tools_expose_nano_banana_2_1_without_official_variant():
    tools = {tool.name: tool for tool in mcp._tool_manager.list_tools()}
    for name in ("openai_generate_image", "openai_edit_image"):
        model = tools[name].parameters["properties"]["model"]
        assert "nano-banana-2.1" in model["enum"]
        assert "nano-banana-2.1:official" not in model["enum"]
        assert "nano-banana-2.1" in model["description"]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("tool_name", "endpoint", "extra_arguments"),
    [
        ("openai_generate_image", "/openai/images/generations", {}),
        (
            "openai_edit_image",
            "/openai/images/edits",
            {"image": ["https://example.com/base.png", "https://example.com/reference.png"]},
        ),
    ],
)
async def test_dispatch_forwards_nano_banana_2_1(monkeypatch, tool_name, endpoint, extra_arguments):
    captured_payload: dict[str, object] = {}

    async def mock_request(request_endpoint, payload):
        assert request_endpoint == endpoint
        captured_payload.update(payload)
        return {"task_id": "test-task-123"}

    monkeypatch.setattr(image_tools.client, "request", mock_request)
    result = await mcp.call_tool(
        tool_name,
        {
            "prompt": "test",
            "model": "nano-banana-2.1",
            "size": "2048x2048",
            "n": 2,
            **extra_arguments,
        },
    )

    assert result
    assert captured_payload["model"] == "nano-banana-2.1"
    assert captured_payload["size"] == "2048x2048"
    assert captured_payload["n"] == 2
    assert captured_payload["response_format"] == "url"
    assert captured_payload["async"] is True
    if "image" in extra_arguments:
        assert captured_payload["image"] == extra_arguments["image"]


@pytest.mark.asyncio
@pytest.mark.parametrize("tool_name", ["openai_generate_image", "openai_edit_image"])
@pytest.mark.parametrize(
    "model",
    [
        "nano-banana-2.1:official",
        "gpt-image-2.6",
        "gpt-image-2.6:reverse",
        "gpt-image-2.6:official",
    ],
)
async def test_dispatch_rejects_unsupported_image_models(monkeypatch, tool_name, model):
    async def unexpected_request(*_args, **_kwargs):
        pytest.fail("An unsupported model must not reach the API")

    monkeypatch.setattr(image_tools.client, "request", unexpected_request)
    arguments = {"prompt": "test", "model": model}
    if tool_name == "openai_edit_image":
        arguments["image"] = "https://example.com/base.png"
    with pytest.raises(ToolError):
        await mcp.call_tool(tool_name, arguments)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "model",
    [
        "gpt-image-2.6-flare",
        "gpt-image-2.6-flare:reverse",
        "gpt-image-2.6-flare:official",
        "gpt-image-2.6-sunburst:official",
    ],
)
@pytest.mark.parametrize("edit", [False, True])
async def test_native_gif_controls_reach_generation_and_edit(monkeypatch, model, edit):
    captured = {}

    async def submit(**kwargs):
        captured.update(kwargs)
        return {"task_id": "gif-task"}

    method = "images_edits_async" if edit else "images_generations_async"
    monkeypatch.setattr(image_tools.client, method, submit)
    tool = image_tools.openai_edit_image if edit else image_tools.openai_generate_image
    args = {
        "model": model,
        "prompt": "animate",
        "output_format": "gif",
        "frame_count": 9,
        "frame_duration_ms": 200,
    }
    if edit:
        args["image"] = "https://example.com/reference.png"
    await tool(**args)
    assert captured["output_format"] == "gif"
    assert captured["frame_count"] == 9
    assert captured["frame_duration_ms"] == 200
    assert captured["size"] == "auto"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "model", ["gpt-image-2.6-sunburst", "gpt-image-2.6-sunburst:reverse", "gpt-image-2.5-flare"]
)
async def test_unsupported_gif_model_is_rejected_without_generation(monkeypatch, model):
    async def unexpected(**_kwargs):
        pytest.fail("unsupported model must not submit a generation")

    monkeypatch.setattr(image_tools.client, "images_generations_async", unexpected)
    result = await image_tools.openai_generate_image(
        prompt="animate", model=model, output_format="gif"
    )
    assert json.loads(result)["code"] == "validation_error"


@pytest.mark.asyncio
async def test_frame_controls_require_gif(monkeypatch):
    async def unexpected(**_kwargs):
        pytest.fail("invalid frame settings must not submit a generation")

    monkeypatch.setattr(image_tools.client, "images_generations_async", unexpected)
    result = await image_tools.openai_generate_image(
        prompt="image", model="gpt-image-2.6-flare", frame_count=9
    )
    assert json.loads(result)["code"] == "validation_error"


def test_image_tool_schema_exposes_native_gif_controls():
    for tool in mcp._tool_manager.list_tools():
        if tool.name not in {"openai_generate_image", "openai_edit_image"}:
            continue
        fields = tool.parameters["properties"]
        assert "gif" in fields["output_format"]["enum"]
        assert "frame_count" in fields and "frame_duration_ms" in fields
