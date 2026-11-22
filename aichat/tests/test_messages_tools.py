"""Native Messages transport and model-discovery coverage."""

import ast
import hashlib
import json
from typing import get_args

import pytest
import respx
from mcp.server.fastmcp.exceptions import ToolError

from core.client import get_request_api_token, set_request_api_token
from core.messages_models import MessagesModel
from core.server import mcp
from scripts.sync_messages_models import render_models
from tools.info_tools import aichat_list_models


@pytest.fixture
def native_token():
    previous = get_request_api_token()
    set_request_api_token("native-fixture-token")
    try:
        yield
    finally:
        set_request_api_token(previous)


def text_result(result):
    content = result[0] if isinstance(result, tuple) else result
    return json.loads(content[0].text)


@pytest.mark.asyncio
@pytest.mark.usefixtures("native_token")
@pytest.mark.parametrize("model", ["claude-opus-5-5", "claude-sonnet-5-5"])
async def test_native_messages_preserve_payload_and_response(model):
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": [{"type": "text", "text": "Hello"}]}],
        "max_tokens": 64,
        "system": "Be concise",
        "tools": [{"name": "lookup", "input_schema": {"type": "object", "properties": {}}}],
        "thinking": {"type": "disabled"},
    }
    answer = {
        "id": "msg_fixture",
        "type": "message",
        "model": model,
        "content": [{"type": "text", "text": "Hello"}],
        "usage": {"input_tokens": 3, "output_tokens": 1},
    }
    with respx.mock() as upstream:
        route = upstream.post("https://api.acedata.cloud/v1/messages").respond(200, json=answer)
        result = await mcp.call_tool("aichat_create_message", payload)
    assert text_result(result) == answer
    assert route.call_count == 1
    request = route.calls.last.request
    assert request.headers["authorization"] == "Bearer native-fixture-token"
    assert request.headers["anthropic-version"] == "2023-06-01"
    assert "x-api-key" not in request.headers
    assert json.loads(request.content) == {**payload, "stream": False}


@pytest.mark.asyncio
@pytest.mark.usefixtures("native_token")
@pytest.mark.parametrize("max_tokens", [None, 0])
async def test_output_budget_is_required_before_request(max_tokens):
    payload = {"model": "claude-sonnet-5-5", "messages": [{"role": "user", "content": "Hello"}]}
    if max_tokens is not None:
        payload["max_tokens"] = max_tokens
    with respx.mock() as upstream:
        with pytest.raises(ToolError, match="max_tokens"):
            await mcp.call_tool("aichat_create_message", payload)
        assert not upstream.calls


@pytest.mark.asyncio
@pytest.mark.usefixtures("native_token")
@pytest.mark.parametrize("status", [400, 403, 429])
async def test_native_errors_are_tool_errors_without_retry(status):
    with respx.mock() as upstream:
        route = upstream.post("https://api.acedata.cloud/v1/messages").respond(
            status, json={"error": {"code": "native_error", "message": "native request rejected"}}
        )
        with pytest.raises(ToolError, match="native request rejected"):
            await mcp.call_tool(
                "aichat_create_message",
                {
                    "model": "claude-sonnet-5-5",
                    "messages": [{"role": "user", "content": "Hello"}],
                    "max_tokens": 64,
                },
            )
    assert route.call_count == 1


@pytest.mark.asyncio
async def test_native_discovery_matches_tool_choices():
    listing = await aichat_list_models()
    section = listing.split("## aichat_create_message", 1)[1].split(
        "## Gemini endpoint coverage", 1
    )[0]
    assert {line[2:] for line in section.splitlines() if line.startswith("- ")} == set(
        get_args(MessagesModel)
    )
    assert {"claude-opus-5-5", "claude-sonnet-5-5"} <= set(get_args(MessagesModel))


@pytest.mark.asyncio
@pytest.mark.usefixtures("native_token")
async def test_non_object_response_is_reported_as_a_tool_error():
    with respx.mock() as upstream:
        upstream.post("https://api.acedata.cloud/v1/messages").respond(200, json=[])
        with pytest.raises(ToolError, match="non-object response"):
            await mcp.call_tool(
                "aichat_create_message",
                {
                    "model": "claude-sonnet-5-5",
                    "messages": [{"role": "user", "content": "Hello"}],
                    "max_tokens": 64,
                },
            )


def test_generator_reads_only_native_request_models(tmp_path):
    models = ["new-native-model"]
    schema = {
        "required": ["model", "messages", "max_tokens"],
        "properties": {"model": {"enum": models}},
    }
    spec = {
        "paths": {
            "/v1/messages": {
                "post": {
                    "requestBody": {
                        "content": {
                            "application/json": {"schema": {"$ref": "#/components/schemas/Request"}}
                        }
                    },
                    "responses": {"200": {"model": {"enum": ["response-only"]}}},
                }
            }
        },
        "components": {"schemas": {"Request": schema}},
    }
    raw = json.dumps(spec).encode()
    (tmp_path / "openapi").mkdir()
    (tmp_path / "openapi/claude.json").write_bytes(raw)
    (tmp_path / "manifest.json").write_text(
        json.dumps(
            {
                "source_sha": "fixture",
                "files": {"openapi/claude.json": "sha256:" + hashlib.sha256(raw).hexdigest()},
            }
        )
    )
    tree = ast.parse(render_models(tmp_path))
    declaration = next(node for node in tree.body if isinstance(node, ast.Assign))
    assert ast.literal_eval(declaration.value.slice) == ("new-native-model",)
