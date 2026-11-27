"""Offline checks for MCP schema, payload and caller identity."""

import json
from unittest.mock import patch

import httpx
import pytest
import respx
from mcp.shared.memory import create_connected_server_and_client_session

import tools  # noqa: F401
from core import client
from core.config import settings
from core.server import mcp

URL = "https://api.acedata.cloud"
TASK = "2265d92c-5775-466e-a6f2-27debe7194a1"
MODEL = "803137da-96bd-4eb9-822f-ae63c153e480"


@pytest.mark.parametrize(
    ("tool", "params", "resource", "body"),
    [
        (
            "tripo_generate_model",
            {"prompt": "chair", "texture": "none", "idempotency_key": "retry-1"},
            "generations",
            {
                "action": "generate",
                "prompt": "chair",
                "model": "v3.1-20260211",
                "texture": "none",
                "async": True,
            },
        ),
        (
            "tripo_generate_model",
            {"image_urls": ["https://images.test/front.png", None, "https://images.test/back.png"]},
            "generations",
            {
                "action": "generate",
                "image_urls": [
                    "https://images.test/front.png",
                    None,
                    "https://images.test/back.png",
                ],
                "model": "v3.1-20260211",
                "texture": "standard",
                "async": True,
            },
        ),
        (
            "tripo_import_model",
            {"model_url": "https://models.test/chair.glb"},
            "models",
            {"action": "import", "model_url": "https://models.test/chair.glb", "async": True},
        ),
        (
            "tripo_texture_model",
            {
                "model_id": MODEL,
                "texture_quality": "detailed",
                "options": {"pbr": False, "texture_seed": 0},
            },
            "models",
            {
                "action": "texture",
                "model_id": MODEL,
                "texture_quality": "detailed",
                "pbr": False,
                "texture_seed": 0,
                "async": True,
            },
        ),
        (
            "tripo_convert_model",
            {
                "model_id": MODEL,
                "format": "FBX",
                "options": {"texture_packaging": "zip", "quad": True},
            },
            "models",
            {
                "action": "convert",
                "model_id": MODEL,
                "format": "FBX",
                "texture_packaging": "zip",
                "quad": True,
                "async": True,
            },
        ),
        (
            "tripo_check_rig",
            {"model_id": MODEL},
            "animations",
            {"action": "rig_check", "model_id": MODEL, "async": True},
        ),
        (
            "tripo_rig_model",
            {"model_url": "https://models.test/man.glb", "rig_type": "biped"},
            "animations",
            {
                "action": "rig",
                "model_url": "https://models.test/man.glb",
                "rig_type": "biped",
                "format": "GLB",
                "async": True,
            },
        ),
        (
            "tripo_retarget_animation",
            {
                "model_id": MODEL,
                "animations": ["preset:walk", "preset:idle"],
                "export_with_geometry": False,
            },
            "animations",
            {
                "action": "retarget",
                "model_id": MODEL,
                "animations": ["preset:walk", "preset:idle"],
                "export_with_geometry": False,
                "format": "GLB",
                "async": True,
            },
        ),
        ("tripo_get_task", {"id": TASK}, "tasks", {"id": TASK}),
        (
            "tripo_get_tasks",
            {"trace_ids": ["example", "example"]},
            "tasks",
            {"action": "retrieve_batch", "trace_ids": ["example", "example"]},
        ),
    ],
)
async def test_mcp_call(tool, params, resource, body):
    response = (
        {"items": [None, None], "count": 2} if tool == "tripo_get_tasks" else {"task_id": TASK}
    )
    with respx.mock() as router:
        route = router.post(URL + "/tripo/" + resource).mock(
            return_value=httpx.Response(200, json=response)
        )
        async with create_connected_server_and_client_session(mcp) as session:
            result = await session.call_tool(tool, params)
            assert not result.isError
            assert result.structuredContent == response
        assert route.call_count == 1
        request = route.calls.last.request
        assert request.headers["authorization"] == "Bearer test-token"
        assert json.loads(request.content) == body
        assert request.headers.get("idempotency-key") == params.get("idempotency_key")


async def test_discovery_and_invalid_selection():
    async with create_connected_server_and_client_session(mcp) as session:
        listing = await session.list_tools()
        assert len(listing.tools) == 9
        assert {t.name for t in listing.tools if t.annotations and t.annotations.readOnlyHint} == {
            "tripo_get_task",
            "tripo_get_tasks",
        }
        with respx.mock() as router:
            for name, args in [
                ("tripo_generate_model", {}),
                ("tripo_generate_model", {"prompt": "a", "image_url": "b"}),
                ("tripo_texture_model", {}),
                ("tripo_get_task", {"id": "a", "trace_id": "b"}),
                ("tripo_retarget_animation", {"model_id": MODEL, "animations": ["a"] * 6}),
            ]:
                result = await session.call_tool(name, args)
                assert result.isError
            assert len(router.calls) == 0


async def test_http_request_token_isolation_and_api_error():
    with (
        patch.object(settings, "server_url", "https://tripo.mcp.acedata.cloud"),
        respx.mock() as router,
    ):
        client.set_request_api_token(None)
        with pytest.raises(ValueError, match="token is required"):
            await client.post("tasks", {"id": TASK})
        client.set_request_api_token("caller-token")
        try:
            r = router.post(URL + "/tripo/tasks").mock(
                return_value=httpx.Response(
                    403, json={"error": {"code": "forbidden", "message": "Access denied"}}
                )
            )
            with pytest.raises(ValueError, match="HTTP 403: Access denied"):
                await client.post("tasks", {"id": TASK})
            assert r.calls.last.request.headers["authorization"] == "Bearer caller-token"
        finally:
            client.set_request_api_token(None)
