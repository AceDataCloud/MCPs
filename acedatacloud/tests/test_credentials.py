"""Credential self-service tool contract tests."""

import json

import httpx
import pytest
import respx

from core.client import set_request_api_token
from tools.user.credentials import (
    acedatacloud_create_credential,
    acedatacloud_delete_credential,
    acedatacloud_get_credential,
    acedatacloud_list_credentials,
    acedatacloud_rotate_credential,
    acedatacloud_update_credential,
)

API = "https://platform.acedata.cloud/api/v1"
CREDENTIAL_ID = "22222222-2222-2222-2222-222222222222"


@respx.mock
@pytest.mark.asyncio
async def test_list_credentials_sends_repeated_filters_and_subject():
    respx.get(f"{API}/platform-tokens/me/").mock(
        return_value=httpx.Response(200, json={"id": "user-1"})
    )
    route = respx.get(f"{API}/credentials/").mock(
        return_value=httpx.Response(200, json={"count": 0, "items": []})
    )
    set_request_api_token("platform-token")
    try:
        await acedatacloud_list_credentials(
            application_id=["app-1", "app-2"],
            host=["a.example", "b.example"],
            granted=True,
            ordering="-created_at",
            offset=10,
        )
    finally:
        set_request_api_token(None)

    params = route.calls[0].request.url.params
    assert params.get_list("application_id") == ["app-1", "app-2"]
    assert params.get_list("host") == ["a.example", "b.example"]
    assert params["granted"] == "true"
    assert params["user_id"] == "user-1"
    assert params["offset"] == "10"


@respx.mock
@pytest.mark.asyncio
async def test_create_credential_full_contract_and_exact_disclosure():
    route = respx.post(f"{API}/credentials/").mock(
        return_value=httpx.Response(
            201,
            json={
                "id": CREDENTIAL_ID,
                "token": "new-token",
                "nested": {"token": "must-stay-masked"},
            },
        )
    )
    result = json.loads(
        await acedatacloud_create_credential(
            application_id="app-1",
            name="ci",
            limited_amount=12.5,
            expired_at="2026-12-31T00:00:00Z",
            host="api.example",
            for_user_id="user-2",
            metadata={"purpose": "grant"},
            allowed_api_ids=["api-1", "api-2"],
            confirm=True,
        )
    )
    assert result["token"] == "new-token"
    assert result["nested"]["token"] != "must-stay-masked"
    assert json.loads(route.calls[0].request.content) == {
        "application_id": "app-1",
        "name": "ci",
        "limited_amount": 12.5,
        "expired_at": "2026-12-31T00:00:00Z",
        "host": "api.example",
        "for_user_id": "user-2",
        "metadata": {"purpose": "grant"},
        "allowed_api_ids": ["api-1", "api-2"],
    }


@respx.mock
@pytest.mark.asyncio
async def test_credential_detail_masks_secret():
    respx.get(f"{API}/credentials/{CREDENTIAL_ID}").mock(
        return_value=httpx.Response(200, json={"id": CREDENTIAL_ID, "token": "existing-token"})
    )
    result = json.loads(await acedatacloud_get_credential(CREDENTIAL_ID))
    assert result["token"] != "existing-token"


@respx.mock
@pytest.mark.asyncio
async def test_update_credential_route_and_body():
    route = respx.patch(f"{API}/credentials/{CREDENTIAL_ID}").mock(
        return_value=httpx.Response(200, json={"id": CREDENTIAL_ID})
    )
    await acedatacloud_update_credential(
        CREDENTIAL_ID,
        name="limited",
        limited_amount=5,
        allowed_api_ids=["api-1"],
        confirm=True,
    )
    assert json.loads(route.calls[0].request.content) == {
        "name": "limited",
        "limited_amount": 5,
        "allowed_api_ids": ["api-1"],
    }


@respx.mock
@pytest.mark.asyncio
async def test_update_credential_can_clear_nullable_limits():
    route = respx.patch(f"{API}/credentials/{CREDENTIAL_ID}").mock(
        return_value=httpx.Response(200, json={"id": CREDENTIAL_ID})
    )
    await acedatacloud_update_credential(
        CREDENTIAL_ID,
        clear_limited_amount=True,
        clear_expired_at=True,
        confirm=True,
    )
    assert json.loads(route.calls[0].request.content) == {
        "limited_amount": None,
        "expired_at": None,
    }


@respx.mock
@pytest.mark.asyncio
async def test_rotate_discloses_only_rotated_secret():
    respx.post(f"{API}/credentials/{CREDENTIAL_ID}/rotate/").mock(
        return_value=httpx.Response(
            200,
            json={
                "id": CREDENTIAL_ID,
                "password": "rotated-password",
                "metadata": {"password": "masked-sibling"},
            },
        )
    )
    result = json.loads(await acedatacloud_rotate_credential(CREDENTIAL_ID, confirm=True))
    assert result["password"] == "rotated-password"
    assert result["metadata"]["password"] != "masked-sibling"


@respx.mock
@pytest.mark.asyncio
async def test_all_credential_mutation_previews_make_zero_http_calls():
    results = [
        await acedatacloud_create_credential(
            application_id="app-1", metadata={"api_key": "submitted-secret"}
        ),
        await acedatacloud_update_credential(CREDENTIAL_ID, name="new"),
        await acedatacloud_rotate_credential(CREDENTIAL_ID),
        await acedatacloud_delete_credential(CREDENTIAL_ID),
    ]
    assert all(json.loads(result)["status"] == "confirmation_required" for result in results)
    assert "submitted-secret" not in results[0]
    assert respx.calls.call_count == 0
