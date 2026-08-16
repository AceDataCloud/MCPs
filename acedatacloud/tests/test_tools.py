"""Unit tests for the MCP tools (read, write-confirm gate, masking)."""

import json

import httpx
import pytest
import respx

from core.client import set_request_api_token
from tools.admin_tools import acedatacloud_create_announcement
from tools.info_tools import acedatacloud_get_user_info
from tools.read_tools import acedatacloud_get_balance, acedatacloud_list_services
from tools.write_tools import (
    acedatacloud_create_credential,
    acedatacloud_create_order,
    acedatacloud_create_platform_token,
    acedatacloud_delete_credential,
    acedatacloud_delete_platform_token,
    acedatacloud_pay_order,
)

API = "https://platform.acedata.cloud/api/v1"


@respx.mock
@pytest.mark.asyncio
async def test_get_user_info_uses_current_request_token():
    route = respx.get(f"{API}/platform-tokens/me/").mock(
        return_value=httpx.Response(
            200,
            json={
                "id": "user-1",
                "username": "testuser",
                "email": "test@example.com",
                "nickname": "Test",
                "avatar": None,
            },
        )
    )
    set_request_api_token("platform-request-token")
    try:
        out = json.loads(await acedatacloud_get_user_info())
    finally:
        set_request_api_token(None)

    assert out["id"] == "user-1"
    assert out["username"] == "testuser"
    assert route.calls[0].request.headers["authorization"] == "Bearer platform-request-token"


@respx.mock
@pytest.mark.asyncio
async def test_get_user_info_maps_authentication_errors():
    respx.get(f"{API}/platform-tokens/me/").mock(
        return_value=httpx.Response(401, json={"detail": "Invalid platform token"})
    )
    set_request_api_token("platform-request-token")
    try:
        out = json.loads(await acedatacloud_get_user_info())
    finally:
        set_request_api_token(None)

    assert out == {"error": "auth_error", "message": "Invalid platform token"}


@respx.mock
@pytest.mark.asyncio
async def test_get_user_info_fails_closed_on_empty_subject():
    respx.get(f"{API}/platform-tokens/me/").mock(return_value=httpx.Response(204))
    set_request_api_token("platform-request-token")
    try:
        out = json.loads(await acedatacloud_get_user_info())
    finally:
        set_request_api_token(None)

    assert out["error"] == "auth_error"
    assert "subject" in out["message"]


@respx.mock
@pytest.mark.asyncio
async def test_permission_denied_is_distinct_from_authentication_error():
    respx.get(f"{API}/platform-tokens/me/").mock(
        return_value=httpx.Response(403, json={"detail": "You do not have permission"})
    )
    set_request_api_token("platform-request-token")
    try:
        out = json.loads(await acedatacloud_get_user_info())
    finally:
        set_request_api_token(None)

    assert out["error"] == "permission_denied"


@respx.mock
@pytest.mark.asyncio
async def test_list_services_filters_by_search(mock_services_page):
    respx.get(f"{API}/services/").mock(return_value=httpx.Response(200, json=mock_services_page))
    out = json.loads(await acedatacloud_list_services(search="suno"))
    assert out["count"] == 1
    assert out["items"][0]["alias"] == "suno"


@respx.mock
@pytest.mark.asyncio
async def test_list_services_searches_tags_without_forwarding_credentials():
    route = respx.get(f"{API}/services/").mock(
        return_value=httpx.Response(
            200,
            json={
                "count": 1,
                "items": [
                    {
                        "id": "svc-chat",
                        "alias": None,
                        "title": "AI Dialogue",
                        "tags": ["aichat"],
                    }
                ],
            },
        )
    )
    out = json.loads(await acedatacloud_list_services(search="aichat"))
    assert out["count"] == 1
    assert out["items"][0]["id"] == "svc-chat"
    assert "authorization" not in {key.lower() for key in route.calls[0].request.headers}


@respx.mock
@pytest.mark.asyncio
async def test_get_balance_summarizes(mock_applications_page):
    respx.get(f"{API}/platform-tokens/me/").mock(
        return_value=httpx.Response(200, json={"id": "user-1"})
    )
    respx.get(f"{API}/applications/").mock(
        return_value=httpx.Response(200, json=mock_applications_page)
    )
    set_request_api_token("platform-request-token")
    try:
        out = json.loads(await acedatacloud_get_balance())
    finally:
        set_request_api_token(None)
    assert out["total_remaining"] == 100.5
    assert out["unit"] == "Credit"
    assert out["applications"][0]["service_id"] == "svc-1"


@respx.mock
@pytest.mark.asyncio
async def test_create_credential_confirm_gate_no_http():
    # Register the route so any accidental call is observable, then assert the
    # confirm gate short-circuited and made ZERO HTTP calls.
    route = respx.post(f"{API}/credentials/").mock(
        return_value=httpx.Response(201, json={"id": "x"})
    )
    out = json.loads(await acedatacloud_create_credential(application_id="app-1", name="ci"))
    assert out["status"] == "confirmation_required"
    assert out["action"] == "POST /credentials/"
    assert out["target"]["application_id"] == "app-1"
    assert route.call_count == 0
    assert respx.calls.call_count == 0


@respx.mock
@pytest.mark.asyncio
async def test_create_credential_confirmed_reveals_token(mock_credential):
    respx.post(f"{API}/credentials/").mock(return_value=httpx.Response(201, json=mock_credential))
    out = json.loads(await acedatacloud_create_credential(application_id="app-1", confirm=True))
    # Freshly minted token must be returned in full so the caller can store it.
    assert out["token"] == mock_credential["token"]


@pytest.mark.asyncio
async def test_delete_credential_confirm_gate():
    out = json.loads(await acedatacloud_delete_credential(credential_id="cred-1"))
    assert out["status"] == "confirmation_required"
    assert out["target"]["id"] == "cred-1"


@pytest.mark.asyncio
async def test_create_announcement_confirm_gate():
    out = json.loads(await acedatacloud_create_announcement(title="T", content="C"))
    assert out["status"] == "confirmation_required"
    assert "superuser" in out["action"]


@respx.mock
@pytest.mark.asyncio
async def test_registered_mutations_require_confirmation():
    calls = [
        acedatacloud_create_order(application_id="app-1", package_id="pkg-1"),
        acedatacloud_pay_order(order_id="order-1"),
        acedatacloud_create_platform_token(),
        acedatacloud_delete_platform_token(token_id="token-1"),
    ]
    results = [json.loads(await call) for call in calls]
    assert all(result["status"] == "confirmation_required" for result in results)
    assert respx.calls.call_count == 0
