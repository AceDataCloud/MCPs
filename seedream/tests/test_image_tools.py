"""Contract tests for Seedream image tools."""

import pytest

import tools.image_tools  # noqa: F401
from core.server import mcp


def test_image_tool_size_schemas_accept_api_string_contract() -> None:
    """Generate and edit tools should expose the API's string size contract."""
    for tool_name in ("seedream_generate_image", "seedream_edit_image"):
        tool = mcp._tool_manager._tools[tool_name]
        size_schema = tool.parameters["properties"]["size"]
        string_schema = next(option for option in size_schema["anyOf"] if option.get("type") == "string")

        assert "enum" not in string_schema
        assert string_schema["pattern"] == r"^(1K|1\.5K|2K|3K|4K|auto|[0-9]+x[0-9]+)$"
        assert "adaptive" not in size_schema["description"].lower()


def test_edit_image_schema_accepts_single_or_multiple_images() -> None:
    """The edit tool should expose the API's string-or-array image contract."""
    tool = mcp._tool_manager._tools["seedream_edit_image"]
    image_schema = tool.parameters["properties"]["image"]

    assert image_schema["anyOf"] == [
        {"type": "string"},
        {
            "items": {"type": "string"},
            "maxItems": 14,
            "type": "array",
        },
    ]
    assert "Never join multiple URLs with commas" in image_schema["description"]


def test_image_tools_expose_new_seedream_parameters() -> None:
    """The MCP schema should expose the latest Seedream request-body fields."""
    expected_model = "doubao-seedream-5-0-lite-260128"

    for tool_name in ("seedream_generate_image", "seedream_edit_image"):
        tool = mcp._tool_manager._tools[tool_name]
        properties = tool.parameters["properties"]

        assert expected_model in properties["model"]["enum"]
        assert "async" in properties
        assert "layer_decomposition" in properties
        assert properties["background"]["anyOf"][0]["enum"] == ["transparent", "opaque"]


@pytest.mark.asyncio
async def test_seedream_generate_image_forwards_new_parameters(monkeypatch) -> None:
    """New API fields should be forwarded to the Seedream images endpoint."""
    captured_payload: dict[str, object] = {}

    async def mock_generate_image(**kwargs):
        captured_payload.update(kwargs)
        return {"success": True, "task_id": "test-task", "data": []}

    monkeypatch.setattr(tools.image_tools.client, "generate_image", mock_generate_image)

    await tools.image_tools.seedream_generate_image(
        prompt="a panda",
        model="doubao-seedream-5-0-lite-260128",
        size="1024x1024",
        async_=False,
        layer_decomposition=True,
        background="transparent",
    )

    assert captured_payload["model"] == "doubao-seedream-5-0-lite-260128"
    assert captured_payload["size"] == "1024x1024"
    assert captured_payload["async"] is False
    assert captured_payload["layer_decomposition"] is True
    assert captured_payload["background"] == "transparent"
