import base64
import json

import pytest
import respx
from httpx import Response

from core.config import settings
from core.oauth import AceDataCloudOAuthProvider, _is_reusable_credential


def _jwt(user_id: str) -> str:
    payload = (
        base64.urlsafe_b64encode(json.dumps({"user_id": user_id}).encode()).rstrip(b"=").decode()
    )
    return f"header.{payload}.signature"


def test_reusable_credential_requires_owner_unlimited_and_unexpired():
    owner = "owner-1"
    assert _is_reusable_credential({"token": "ok", "user_id": owner, "limited_amount": None}, owner)
    assert not _is_reusable_credential(
        {"token": "grant", "user_id": "holder", "limited_amount": 1}, owner
    )
    assert not _is_reusable_credential(
        {"token": "limited", "user_id": owner, "limited_amount": 100}, owner
    )
    assert not _is_reusable_credential(
        {
            "token": "expired",
            "user_id": owner,
            "limited_amount": None,
            "expired_at": "2020-01-01T00:00:00Z",
        },
        owner,
    )


@pytest.mark.asyncio
@respx.mock
async def test_oauth_skips_grant_and_selects_owner_unlimited_credential():
    owner = "owner-1"
    credentials = respx.get(f"{settings.platform_base_url}/api/v1/credentials/").mock(
        return_value=Response(
            200,
            json={
                "results": [
                    {
                        "id": "grant",
                        "token": "grant-token",
                        "user_id": "holder",
                        "limited_amount": 1,
                    },
                    {
                        "id": "owner",
                        "token": "owner-token",
                        "user_id": owner,
                        "limited_amount": None,
                    },
                ]
            },
        )
    )

    token = await AceDataCloudOAuthProvider()._get_user_credential(_jwt(owner))

    assert credentials.called
    assert token == "owner-token"


@pytest.mark.asyncio
@respx.mock
async def test_oauth_creates_named_unlimited_credential_when_none_reusable():
    owner = "owner-1"
    respx.get(f"{settings.platform_base_url}/api/v1/credentials/").mock(
        return_value=Response(200, json={"results": []})
    )
    respx.get(f"{settings.platform_base_url}/api/v1/applications/").mock(
        return_value=Response(200, json={"items": [{"id": "app-1", "credentials": []}]})
    )
    create = respx.post(f"{settings.platform_base_url}/api/v1/credentials/").mock(
        return_value=Response(201, json={"token": "new-token"})
    )

    token = await AceDataCloudOAuthProvider()._get_user_credential(_jwt(owner))

    assert token == "new-token"
    payload = json.loads(create.calls.last.request.content)
    assert payload == {
        "application_id": "app-1",
        "name": "MiniMax MCP OAuth",
        "limited_amount": None,
    }
