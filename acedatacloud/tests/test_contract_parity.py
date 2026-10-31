"""Regressions for the API/MCP contract audit, using actual dispatch and HTTP bodies."""

import base64
import json
from unittest.mock import AsyncMock

import pytest
import respx
from mcp.server.fastmcp.exceptions import ToolError

import tools  # noqa: F401
from contracts.management_surface import SURFACE_TOOLS
from contracts.tool_catalog import TOOL_CATALOG
from core.server import mcp
from core.visibility import list_visible_tools

API = "https://platform.acedata.cloud/api/v1"


async def call(name, arguments):
    content, _ = await mcp.call_tool(name, arguments)
    return json.loads(content[0].text)


@respx.mock
async def test_required_reward_compare_value_is_validated_and_forwarded():
    name = "acedatacloud_create_distribution_statuses_update_reward"
    with pytest.raises(ToolError):
        await call(name, {"id": "reward-1", "reward": "10.00", "confirm": True})
    assert not respx.calls
    route = respx.post(f"{API}/distribution-statuses/reward-1/update-reward/").respond(200, json={})
    await call(
        name, {"id": "reward-1", "reward": "10.00", "expected_reward": "9.00", "confirm": True}
    )
    assert json.loads(route.calls.last.request.content) == {
        "reward": "10.00",
        "expected_reward": "9.00",
    }


@respx.mock
async def test_manual_invoice_confirmation_is_forwarded_without_bypassing_preview():
    name = "acedatacloud_update_invoices_admin_id"
    arguments = {"id": "invoice-1", "status": "Voided", "manual_void_confirmed": True}
    result = await call(name, arguments)
    assert result["status"] == "confirmation_required"
    assert not respx.calls
    route = respx.patch(f"{API}/invoices/admin/invoice-1/").respond(200, json={})
    await call(name, {**arguments, "confirm": True})
    assert json.loads(route.calls.last.request.content) == {
        "status": "Voided",
        "manual_void_confirmed": True,
    }


@respx.mock
@pytest.mark.parametrize(
    "name,id_field",
    [
        ("acedatacloud_deploy_application", "application_id"),
        ("acedatacloud_create_applications_deployment_deploy", "id"),
    ],
)
async def test_deploy_secrets_are_redacted_in_preview_and_forwarded_only_on_confirmation(
    name, id_field
):
    secret = "example-credential-for-test-only"
    arguments = {id_field: "app-1", "secrets": {"access_password": secret}}
    result = await call(name, arguments)
    assert result["status"] == "confirmation_required"
    assert secret not in json.dumps(result)
    assert result["target"].get("body", result["target"])["secrets"] == "***"
    assert not respx.calls
    route = respx.post(f"{API}/applications/app-1/deployment-deploy/").respond(202, json={})
    await call(name, {**arguments, "confirm": True})
    assert json.loads(route.calls.last.request.content)["secrets"] == arguments["secrets"]


@respx.mock
@pytest.mark.parametrize("action", ["start", "stop"])
async def test_removed_power_actions_are_rejected_before_http(action):
    with pytest.raises(ToolError):
        await call(
            "acedatacloud_control_deployment",
            {"application_id": "app-1", "action": action, "confirm": True},
        )
    assert not respx.calls


def test_retired_email_actions_are_not_registered():
    names = {tool.name for tool in mcp._tool_manager.list_tools()}
    for suffix in [
        "activate",
        "prepare",
        "create_carryover",
        "prepare_carryover",
        "release_next_wave",
    ]:
        assert "acedatacloud_run_email_campaigns_" + suffix not in names


@respx.mock
async def test_new_category_creation_keeps_required_strings_and_publish_permission():
    name = "acedatacloud_create_blogs_admin_categories"
    assert TOOL_CATALOG[name].required_permissions == ("blog:publish",)
    with pytest.raises(ToolError):
        await call(name, {"slug": "sample", "name": 123, "name_en": "Sample", "confirm": True})
    assert not respx.calls
    args = {"slug": "sample", "name": "示例", "name_en": "Sample", "position": 0}
    route = respx.post(f"{API}/blogs/admin/categories/").respond(201, json={})
    await call(name, {**args, "confirm": True})
    assert json.loads(route.calls.last.request.content) == args


@respx.mock
async def test_new_manual_invoice_upload_uses_multipart_and_required_file():
    name = "acedatacloud_create_invoices_admin_orders_manual"
    assert TOOL_CATALOG[name].required_permissions == ("invoices:write:any",)
    with pytest.raises(ToolError):
        await call(name, {"order_id": "order-1", "confirm": True})
    assert not respx.calls
    route = respx.post(f"{API}/invoices/admin/orders/order-1/manual/").respond(201, json={})
    await call(
        name,
        {
            "order_id": "order-1",
            "filename": "invoice.pdf",
            "content_base64": base64.b64encode(b"%PDF-test").decode(),
            "content_type": "application/pdf",
            "confirmed_amount": "12.50",
            "confirm": True,
        },
    )
    request = route.calls.last.request
    assert request.headers["content-type"].startswith("multipart/form-data;")
    assert b"%PDF-test" in request.content
    assert b'name="confirmed_amount"' in request.content
    assert b"12.50" in request.content


@respx.mock
@pytest.mark.parametrize("allowed", [False, True])
async def test_health_tools_follow_authoritative_capability_in_discovery_and_dispatch(
    monkeypatch, allowed
):
    subject = {"id": "account", "permissions": [], "can_read_admin_health": allowed}
    monkeypatch.setattr("core.visibility.client.api_token", "platform-test")
    monkeypatch.setattr("core.visibility.get_request_subject", AsyncMock(return_value=subject))
    monkeypatch.setattr(
        "tools.management_tools.get_request_subject", AsyncMock(return_value=subject)
    )
    name = "acedatacloud_get_admin_health_summary"
    assert TOOL_CATALOG[name].audience == "admin"
    visible = {t.name for t in await list_visible_tools()}
    assert (name in visible) is allowed
    route = respx.get(f"{API}/admin/health/summary/").respond(200, json={"status": "ready"})
    result = await call(name, {})
    assert route.call_count == int(allowed)
    assert result == (
        {"status": "ready"}
        if allowed
        else {"error": "permission_denied", "message": "A superuser platform token is required"}
    )


def test_new_read_routes_and_corrected_field_shapes_are_in_the_contract():
    by_path = {(t["method"], t["path"]): t for t in SURFACE_TOOLS}
    for path in [
        "/applications/{id}/agent-setup/",
        "/orders/revenue-customers/",
        "/email-marketing/admin/sender-quotas/",
        "/email-marketing/admin/campaigns/{id}/analytics/",
        "/email-marketing/admin/campaigns/{id}/conversions/",
        "/email-marketing/admin/campaigns/{id}/delivery-plan/",
    ]:
        assert ("GET", path) in by_path
    fields = by_path[("POST", "/email-marketing/admin/campaigns/")]["body_schema"]["properties"]
    assert fields["daily_cap"]["type"] == "integer"
    assert fields["expires_at"]["type"] == "string"


@respx.mock
async def test_nullable_patch_distinguishes_omission_from_explicit_null():
    name = "acedatacloud_update_email_campaigns_id"
    route = respx.patch(f"{API}/email-marketing/admin/campaigns/campaign-1/").respond(200, json={})
    await call(name, {"id": "campaign-1", "confirm": True})
    assert json.loads(route.calls.last.request.content) == {}
    arguments = {"id": "campaign-1", "daily_cap": None, "expires_at": None}
    preview = await call(name, arguments)
    assert preview["target"]["body"] == {"daily_cap": None, "expires_at": None}
    await call(name, {**arguments, "confirm": True})
    assert json.loads(route.calls.last.request.content) == {"daily_cap": None, "expires_at": None}


@respx.mock
async def test_revenue_customer_dates_reach_the_backend():
    route = respx.get(f"{API}/orders/revenue-customers/").respond(200, json={})
    await call(
        "acedatacloud_get_orders_revenue_customers",
        {"start_date": "2026-10-01", "end_date": "2026-10-15"},
    )
    assert dict(route.calls.last.request.url.params) == {
        "start_date": "2026-10-01",
        "end_date": "2026-10-15",
    }
