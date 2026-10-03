"""Curated discovery, legacy compatibility and account boundaries."""

import asyncio
import json
from unittest.mock import AsyncMock

import httpx
import pytest
import respx
from mcp.types import ListToolsRequest, Tool

import tools  # noqa: F401
from contracts.management_surface import SURFACE_TOOLS
from contracts.render import registered_contract_tools
from contracts.tool_catalog import (
    CATEGORIES,
    CLIENT_HELPERS,
    CROSS_ACCOUNT_TOOLS,
    INFO_TOOL,
    TOOL_CATALOG,
    advertised_tools,
)
from core.client import get_request_api_token, reset_request_api_token, set_request_api_token
from core.config import Settings, settings
from core.exceptions import PlatformAuthError
from core.server import mcp
from core.visibility import list_visible_tools
from tools.info_tools import acedatacloud_get_usage_guide


@pytest.fixture(autouse=True)
def discovery_context(monkeypatch):
    set_request_api_token(None)
    monkeypatch.setattr("core.visibility.client.api_token", "platform-test")
    monkeypatch.setattr(settings, "tool_profile", "curated")
    yield
    set_request_api_token(None)


def test_every_legacy_tool_has_an_explainable_discovery_policy():
    assert set(TOOL_CATALOG) | {INFO_TOOL} == registered_contract_tools()
    assert set(CROSS_ACCOUNT_TOOLS) <= set(TOOL_CATALOG)
    assert set(TOOL_CATALOG) >= CLIENT_HELPERS
    assert len(advertised_tools()) < len(registered_contract_tools()) * 0.7
    for name, entry in TOOL_CATALOG.items():
        assert entry.category in CATEGORIES
        assert entry.audience in {"public", "account", "workspace", "admin"}
        assert entry.reason
        if entry.replacement:
            assert entry.replacement in advertised_tools()
            assert name != entry.replacement


def test_generated_business_workflows_are_not_removed_with_aliases():
    retained = {
        "acedatacloud_create_files",
        "acedatacloud_create_sites",
        "acedatacloud_create_datasets_download",
        "acedatacloud_create_recharge_cards_allocations",
        "acedatacloud_run_email_campaigns_send",
        "acedatacloud_create_orders_refund",
        "acedatacloud_create_webhooks",
        "acedatacloud_create_access_grants",
        "acedatacloud_update_feature_flags_id",
        "acedatacloud_create_configuration_providers",
    }
    assert retained <= advertised_tools()
    assert "acedatacloud_create_blog_draft" in advertised_tools()
    assert "acedatacloud_publish_blog_post" in advertised_tools()
    assert "acedatacloud_create_platform_token" in advertised_tools()
    assert "acedatacloud_create_platform_tokens" not in advertised_tools()


def test_versioned_model_list_is_removed_from_all_registries():
    legacy = "acedatacloud_list_configuration_models_v2"
    current = "acedatacloud_list_configuration_models"
    assert legacy not in TOOL_CATALOG
    assert TOOL_CATALOG[current].required_permissions == ("provider-routing:read",)
    assert legacy not in advertised_tools()
    assert current in advertised_tools()
    assert legacy not in advertised_tools("full")
    assert legacy not in registered_contract_tools()
    assert current in registered_contract_tools()


@pytest.mark.parametrize("profile", ["curated", "full"])
async def test_model_discovery_and_guide_only_expose_canonical_tool_with_exact_grants(
    monkeypatch, profile
):
    legacy = "acedatacloud_list_configuration_models_v2"
    current = "acedatacloud_list_configuration_models"
    subject = {"id": "routing-admin", "permissions": ["provider-routing:read"]}
    monkeypatch.setattr(settings, "tool_profile", profile)
    monkeypatch.setattr("core.visibility.get_request_subject", AsyncMock(return_value=subject))
    result = await mcp._mcp_server.request_handlers[ListToolsRequest](ListToolsRequest())
    visible = {tool.name: tool for tool in result.root.tools}
    assert current in visible
    assert "health cards" in visible[current].description
    assert "q, status and provider filters" in visible[current].description
    assert "acedatacloud/deprecated" not in visible[current].meta
    guide = await acedatacloud_get_usage_guide()
    assert f"- {current} —" in guide
    assert legacy not in visible
    assert f"- {legacy} —" not in guide
    subject["permissions"] = ["orders:read:any"]
    assert not {legacy, current} & {tool.name for tool in await list_visible_tools()}
    revoked_guide = await acedatacloud_get_usage_guide()
    assert f"- {legacy} —" not in revoked_guide
    assert f"- {current} —" not in revoked_guide


async def test_protocol_handler_uses_curated_catalog_without_changing_registry(monkeypatch):
    monkeypatch.setattr("core.visibility.client.api_token", "")
    registered = {tool.name for tool in await mcp.list_tools()}
    result = await mcp._mcp_server.request_handlers[ListToolsRequest](ListToolsRequest())
    assert {tool.name for tool in result.root.tools} == advertised_tools()
    for tool in result.root.tools:
        if tool.name != INFO_TOOL:
            assert tool.meta["acedatacloud/category"] == TOOL_CATALOG[tool.name].category
            assert tool.meta["acedatacloud/audience"] == TOOL_CATALOG[tool.name].audience
    assert registered == registered_contract_tools()
    monkeypatch.setattr(settings, "tool_profile", "full")
    assert {tool.name for tool in await list_visible_tools()} == registered


async def test_personal_and_delegated_accounts_do_not_discover_admin_tools(monkeypatch):
    subject = {
        "id": "account",
        "permissions": ["applications:read", "blog:read", "blog:write", "sites:write"],
    }
    monkeypatch.setattr("core.visibility.get_request_subject", AsyncMock(return_value=subject))
    visible = {tool.name for tool in await list_visible_tools()}
    assert "acedatacloud_list_applications" in visible
    assert "acedatacloud_create_blog_draft" in visible
    assert "acedatacloud_update_site" in visible
    assert not {
        name for name in visible if name != INFO_TOOL and TOOL_CATALOG[name].audience == "admin"
    }
    guide = await acedatacloud_get_usage_guide()
    assert "acedatacloud_create_blog_draft" in guide
    assert "acedatacloud_create_configuration_providers" not in guide
    assert "acedatacloud_create_platform_tokens" not in guide


async def test_cross_account_alias_requires_its_exact_permission_and_tracks_revocation(monkeypatch):
    subject = {"id": "account", "permissions": ["applications:read", "orders:read:any"]}
    monkeypatch.setattr("core.visibility.get_request_subject", AsyncMock(return_value=subject))
    assert "acedatacloud_list_applications_detail" not in {
        tool.name for tool in await list_visible_tools()
    }
    subject["permissions"].append("applications:read:any")
    assert "acedatacloud_list_applications_detail" in {
        tool.name for tool in await list_visible_tools()
    }
    tool = next(
        tool
        for tool in await list_visible_tools()
        if tool.name == "acedatacloud_list_applications_detail"
    )
    assert "Administrative cross-account" in tool.description
    assert "applications:read:any" in tool.description
    subject["permissions"].remove("applications:read:any")
    assert "acedatacloud_list_applications_detail" not in {
        tool.name for tool in await list_visible_tools()
    }


async def test_concurrent_request_permissions_do_not_leak_between_accounts(monkeypatch):
    subjects = {
        "personal": {"id": "personal", "permissions": ["blog:read", "blog:write"]},
        "admin": {"id": "admin", "permissions": ["email-marketing:read"]},
    }

    async def subject():
        return subjects[get_request_api_token()]

    async def visible(token):
        context = set_request_api_token(token)
        try:
            return {tool.name for tool in await list_visible_tools()}
        finally:
            reset_request_api_token(context)

    monkeypatch.setattr("core.visibility.get_request_subject", subject)
    personal, admin = await asyncio.gather(visible("personal"), visible("admin"))
    assert "acedatacloud_create_blog_draft" in personal
    assert "acedatacloud_list_email_campaigns" not in personal
    assert "acedatacloud_create_blog_draft" not in admin
    assert "acedatacloud_list_email_campaigns" in admin


@pytest.mark.parametrize("profile", ["curated", "full"])
async def test_unresolved_subject_fails_closed_even_in_full_profile(monkeypatch, profile):
    monkeypatch.setattr(settings, "tool_profile", profile)
    monkeypatch.setattr(
        "core.visibility.get_request_subject", AsyncMock(side_effect=PlatformAuthError("expired"))
    )
    visible = {tool.name for tool in await list_visible_tools()}
    assert "acedatacloud_list_services" in visible
    assert INFO_TOOL in visible
    assert "acedatacloud_get_user_info" not in visible
    assert "acedatacloud_create_blog_draft" not in visible
    assert "acedatacloud_create_platform_token" not in visible


async def test_unclassified_registration_is_not_implicitly_advertised(monkeypatch):
    monkeypatch.setattr("core.visibility.client.api_token", "")
    unknown = Tool(name="unclassified-tool", inputSchema={"type": "object"})
    monkeypatch.setattr(mcp, "list_tools", AsyncMock(return_value=[unknown]))
    assert await list_visible_tools() == []


@respx.mock
async def test_hidden_alias_keeps_its_original_schema_route_and_preview():
    name = "acedatacloud_create_platform_tokens"
    schema = next(tool.inputSchema for tool in await mcp.list_tools() if tool.name == name)
    assert "confirm" in schema["properties"]
    assert name not in advertised_tools()
    preview = await mcp.call_tool(name, {})
    preview_content = preview[0] if isinstance(preview, tuple) else preview
    assert "confirmation_required" in preview_content[0].text
    assert not respx.calls
    route = respx.post("https://platform.acedata.cloud/api/v1/platform-tokens/").mock(
        return_value=httpx.Response(201, json={"token": "platform-new"})
    )
    result = await mcp.call_tool(name, {"confirm": True})
    result_content = result[0] if isinstance(result, tuple) else result
    assert json.loads(result_content[0].text)["token"] == "platform-new"
    assert route.call_count == 1
    assert {spec["name"] for spec in SURFACE_TOOLS} <= registered_contract_tools()


def test_profile_setting_is_explicit_and_validated(monkeypatch):
    monkeypatch.delenv("ACEDATACLOUD_TOOL_PROFILE", raising=False)
    assert Settings().tool_profile == "curated"
    monkeypatch.setenv("ACEDATACLOUD_TOOL_PROFILE", "full")
    assert Settings().tool_profile == "full"
    monkeypatch.setenv("ACEDATACLOUD_TOOL_PROFILE", "unknown")
    with pytest.raises(ValueError, match="ACEDATACLOUD_TOOL_PROFILE"):
        Settings()
