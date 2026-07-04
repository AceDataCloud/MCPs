"""Unit tests for the MCP tools (read, write-confirm gate, masking)."""

import json

import httpx
import pytest
import respx

from tools.admin_tools import acedatacloud_create_announcement
from tools.read_tools import acedatacloud_get_balance, acedatacloud_list_services
from tools.write_tools import acedatacloud_create_credential, acedatacloud_delete_credential

API = "https://platform.acedata.cloud/api/v1"


@respx.mock
@pytest.mark.asyncio
async def test_list_services_filters_by_search(mock_services_page):
    respx.get(f"{API}/services/").mock(return_value=httpx.Response(200, json=mock_services_page))
    out = json.loads(await acedatacloud_list_services(search="suno"))
    assert out["count"] == 1
    assert out["items"][0]["alias"] == "suno"


@respx.mock
@pytest.mark.asyncio
async def test_list_services_multiword_search_ranks(mock_services_page):
    # "音乐生成" is split as "音乐 生成"; the old substring match ("音乐 生成" in
    # title) would find nothing, but the fan-out matches both keywords and ranks
    # Suno (both hit) above Flux (only "生成" hits).
    respx.get(f"{API}/services/").mock(return_value=httpx.Response(200, json=mock_services_page))
    out = json.loads(await acedatacloud_list_services(search="音乐 生成"))
    assert out["items"][0]["alias"] == "suno"
    assert {it["alias"] for it in out["items"]} == {"suno", "flux"}


@respx.mock
@pytest.mark.asyncio
async def test_get_balance_summarizes(mock_applications_page):
    respx.get(f"{API}/applications/").mock(
        return_value=httpx.Response(200, json=mock_applications_page)
    )
    out = json.loads(await acedatacloud_get_balance())
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
