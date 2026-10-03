"""Contract coverage and security boundaries for fixed management operations."""

import base64
import json
import re
from unittest.mock import AsyncMock

import httpx
import pytest
import respx
from mcp.server.fastmcp.exceptions import ToolError

from contracts.management_surface import BACKEND_OPERATIONS, SURFACE_TOOLS
from contracts.platform_operations import OPERATIONS
from core.client import set_request_api_token
from core.server import mcp
from core.visibility import list_visible_tools
from tools.management_tools import REGISTERED_TOOLS

API = "https://platform.acedata.cloud/api/v1"


def test_complete_backend_coverage_has_no_unclassified_business_routes():
    assert len(BACKEND_OPERATIONS) > 400
    assert len(SURFACE_TOOLS) > 350
    contract = {operation.tool for operation in OPERATIONS if operation.tool}
    for route in BACKEND_OPERATIONS:
        assert route["coverage"] in {"covered", "excluded"}
        if route["coverage"] == "covered":
            assert route["tool"] in contract
        else:
            assert route["rationale"]
    assert not any(
        "/events/tencent/" in s["path"] or "/webhook/" in s["path"] for s in SURFACE_TOOLS
    )
    assert all(re.fullmatch(r"[a-zA-Z0-9_.-]{1,64}", s["name"]) for s in SURFACE_TOOLS)
    assert not any("blog_editor" in operation.required_permissions for operation in OPERATIONS)


@respx.mock
async def test_every_new_write_preview_has_zero_http_calls_and_masks_secrets():
    for spec in SURFACE_TOOLS:
        if not spec["confirm"]:
            continue
        result = await REGISTERED_TOOLS[spec["name"]](
            **dict.fromkeys(spec["path_parameters"], "identifier")
        )
        assert json.loads(result)["status"] == "confirmation_required"
    name = "acedatacloud_create_configuration_providers"
    result = json.loads(
        await REGISTERED_TOOLS[name](domain="llm", api_key="secret-do-not-disclose")
    )
    assert "secret-do-not-disclose" not in json.dumps(result)
    assert not respx.calls


@respx.mock
async def test_confirmed_fixed_routes():
    route = respx.patch(f"{API}/feature-flags/test-id").mock(
        return_value=httpx.Response(200, json={"enabled": True})
    )
    await REGISTERED_TOOLS["acedatacloud_update_feature_flags_id"](
        id="test-id", enabled=True, confirm=True
    )
    assert json.loads(route.calls.last.request.content) == {"enabled": True}
    assert route.calls.last.request.headers["authorization"].startswith("Bearer ")


@respx.mock
async def test_canonical_model_list_and_compatibility_alias_share_health_contract():
    payload = {"data": [{"model": "test-model", "status": "degraded", "latency": 1.5}]}
    current_route = respx.get(f"{API}/admin/upstreams/llm/models/").mock(
        return_value=httpx.Response(200, json=payload)
    )
    legacy_route = respx.get(f"{API}/admin/upstreams/llm/models-v2/").mock(
        return_value=httpx.Response(200, json=payload)
    )
    arguments = {
        "domain": "llm",
        "q": "test-model",
        "status": "attention",
        "provider": "test-provider",
    }
    current_content, _ = await mcp.call_tool("acedatacloud_list_configuration_models", arguments)
    legacy_content, _ = await mcp.call_tool("acedatacloud_list_configuration_models_v2", arguments)
    assert json.loads(legacy_content[0].text) == payload
    assert json.loads(current_content[0].text) == payload
    assert legacy_route.call_count == current_route.call_count == 1
    expected_query = {
        "q": "test-model",
        "status": "attention",
        "provider": "test-provider",
    }
    assert dict(current_route.calls.last.request.url.params) == expected_query
    assert dict(legacy_route.calls.last.request.url.params) == expected_query


@respx.mock
async def test_actual_mcp_schema_validates_required_allocation_fields():
    with pytest.raises(ToolError):
        await mcp.call_tool(
            "acedatacloud_create_recharge_cards_allocations", {"quantity": 1, "confirm": True}
        )
    assert not respx.calls


@respx.mock
async def test_generated_public_reads_do_not_forward_credentials():
    set_request_api_token("platform-private")
    route = respx.get(f"{API}/showcases/").mock(
        return_value=httpx.Response(200, json={"items": []})
    )
    await REGISTERED_TOOLS["acedatacloud_list_showcases"](limit=5)
    assert "authorization" not in route.calls.last.request.headers
    assert route.calls.last.request.url.params["limit"] == "5"


@respx.mock
async def test_generated_tool_preserves_backend_permission_denial():
    respx.post(f"{API}/email-marketing/admin/campaigns/test-id/send/").mock(
        return_value=httpx.Response(
            403, json={"detail": "Missing required permission: email-marketing:send"}
        )
    )
    result = await REGISTERED_TOOLS["acedatacloud_run_email_campaigns_send"](
        id="test-id", confirm=True
    )
    assert json.loads(result)["error"] == "permission_denied"


@respx.mock
async def test_path_values_are_encoded_and_traversal_rejected():
    result = await REGISTERED_TOOLS["acedatacloud_get_feature_flags_id"](id="../orders")
    assert json.loads(result)["error"] == "validation_error"
    assert not respx.calls


@respx.mock
async def test_csv_and_wallet_artifacts_are_bounded_downloads():
    csv = b"code,amount\nSECRET-CARD,100\n"
    respx.post(f"{API}/recharge-cards/admin/issue/").mock(
        return_value=httpx.Response(
            200,
            content=csv,
            headers={
                "content-type": "text/csv",
                "content-disposition": 'attachment; filename="cards.csv"',
            },
        )
    )
    result = json.loads(
        await REGISTERED_TOOLS["acedatacloud_create_recharge_cards_admin_issue"](
            amount=100, quantity=1, confirm=True
        )
    )
    assert base64.b64decode(result["content_base64"]) == csv
    assert result["filename"] == "cards.csv"


@respx.mock
async def test_multipart_upload_requires_confirmation_and_uses_file_field():
    route = respx.post(f"{API}/files/").mock(
        return_value=httpx.Response(200, json={"file_id": "file-1"})
    )
    result = await REGISTERED_TOOLS["acedatacloud_create_files"](
        filename="article.png", content_base64=base64.b64encode(b"png").decode(), confirm=True
    )
    assert json.loads(result)["file_id"] == "file-1"
    assert "multipart/form-data" in route.calls.last.request.headers["content-type"]
    assert b'name="file"' in route.calls.last.request.content


async def test_visible_tools_follow_current_account_permissions(monkeypatch):
    set_request_api_token("platform-test")
    subject = {"id": "account", "permissions": ["blog:read", "blog:write"]}
    monkeypatch.setattr("core.visibility.get_request_subject", AsyncMock(return_value=subject))
    names = {tool.name for tool in await list_visible_tools()}
    assert "acedatacloud_create_blog_draft" in names
    assert "acedatacloud_publish_blog_post" not in names
    assert "acedatacloud_run_email_campaigns_send" not in names
    subject["permissions"].append("blog:publish")
    assert "acedatacloud_publish_blog_post" in {tool.name for tool in await list_visible_tools()}
    subject["permissions"] = []
    assert "acedatacloud_create_blog_draft" not in {
        tool.name for tool in await list_visible_tools()
    }


@respx.mock
@pytest.mark.parametrize("permissions", [[], ["orders:read:any"]])
@pytest.mark.parametrize(
    ("user_ids", "allowed"),
    [
        (None, True),
        ([], True),
        (["current-user"], True),
        (["current-user", "current-user"], True),
        (["other-user"], False),
        (["current-user", "other-user"], False),
    ],
)
async def test_account_query_arrays_respect_owner_and_exact_admin_grants(
    monkeypatch, permissions, user_ids, allowed
):
    monkeypatch.setattr(
        "tools.management_tools.get_request_subject",
        AsyncMock(
            return_value={
                "id": "current-user",
                "permissions": permissions,
            }
        ),
    )
    route = respx.get(f"{API}/applications/").mock(
        return_value=httpx.Response(200, json={"items": []})
    )
    arguments = {} if user_ids is None else {"user_id": user_ids}
    content, _ = await mcp.call_tool("acedatacloud_list_applications_detail", arguments)
    result = json.loads(content[0].text)
    if allowed:
        assert route.call_count == 1
        assert route.calls.last.request.url.params.get_list("user_id") == ["current-user"]
    else:
        assert result["error"] == "permission_denied"
        assert not respx.calls


@respx.mock
async def test_exact_cross_account_grant_preserves_multi_user_filter(monkeypatch):
    monkeypatch.setattr(
        "tools.management_tools.get_request_subject",
        AsyncMock(return_value={"id": "current-user", "permissions": ["applications:read:any"]}),
    )
    route = respx.get(f"{API}/applications/").mock(return_value=httpx.Response(200, json={}))
    await mcp.call_tool(
        "acedatacloud_list_applications_detail",
        {"user_id": ["current-user", "other-user"]},
    )
    assert route.call_count == 1
    assert route.calls.last.request.url.params.get_list("user_id") == ["current-user", "other-user"]


@respx.mock
async def test_native_token_creation_discloses_only_the_new_token():
    respx.post(f"{API}/platform-tokens/").mock(
        return_value=httpx.Response(
            201,
            json={
                "token": "platform-new-token",
                "metadata": {"other_token": "secret-sibling-value"},
            },
        )
    )
    result = json.loads(await REGISTERED_TOOLS["acedatacloud_create_platform_tokens"](confirm=True))
    assert result["token"] == "platform-new-token"
    assert result["metadata"]["other_token"] != "secret-sibling-value"
