import base64
import json

import pytest
import respx
from httpx import Response

from core.config import settings
from core.oauth import AceDataCloudOAuthProvider


def _jwt(user_id: str) -> str:
    payload = (
        base64.urlsafe_b64encode(json.dumps({"user_id": user_id}).encode()).rstrip(b"=").decode()
    )
    return f"header.{payload}.signature"


@pytest.mark.asyncio
@respx.mock
async def test_oauth_gets_only_its_managed_credential():
    owner = "owner-1"
    respx.get(f"{settings.platform_base_url}/api/v1/applications/").mock(
        return_value=Response(200, json={"items": [{"id": "app-1"}]})
    )
    get_creds = respx.get(
        f"{settings.platform_base_url}/api/v1/credentials/",
        params={"application_id": "app-1", "name": "OAuth MCP"},
    ).mock(return_value=Response(200, json={"items": []}))
    create_cred = respx.post(f"{settings.platform_base_url}/api/v1/credentials/").mock(
        return_value=Response(201, json={"id": "credential-1", "token": "managed-token"})
    )

    token = await AceDataCloudOAuthProvider()._get_user_credential(_jwt(owner))

    assert token == "managed-token"
    assert get_creds.called
    assert create_cred.called
    assert json.loads(create_cred.calls.last.request.content) == {
        "application_id": "app-1",
        "name": "OAuth MCP",
    }


@pytest.mark.asyncio
@respx.mock
async def test_oauth_reuses_retrieved_credential_without_creating():
    owner = "owner-1"
    respx.get(f"{settings.platform_base_url}/api/v1/applications/").mock(
        return_value=Response(200, json={"items": [{"id": "app-1"}]})
    )
    get_creds = respx.get(
        f"{settings.platform_base_url}/api/v1/credentials/",
        params={"application_id": "app-1", "name": "OAuth MCP"},
    ).mock(
        return_value=Response(
            200,
            json={"items": [{"id": "credential-1", "token": "existing-token"}]},
        )
    )
    create_cred = respx.post(f"{settings.platform_base_url}/api/v1/credentials/").mock(
        return_value=Response(201, json={"id": "unexpected", "token": "new-token"})
    )

    token = await AceDataCloudOAuthProvider()._get_user_credential(_jwt(owner))

    assert token == "existing-token"
    assert get_creds.called
    assert not create_cred.called


@pytest.mark.asyncio
@respx.mock
async def test_oauth_creates_global_application_before_managed_credential():
    owner = "owner-1"
    respx.get(f"{settings.platform_base_url}/api/v1/applications/").mock(
        return_value=Response(200, json={"items": []})
    )
    create_app = respx.post(f"{settings.platform_base_url}/api/v1/applications/").mock(
        return_value=Response(201, json={"id": "app-1"})
    )
    get_creds = respx.get(
        f"{settings.platform_base_url}/api/v1/credentials/",
        params={"application_id": "app-1", "name": "OAuth MCP"},
    ).mock(return_value=Response(200, json={"items": []}))
    create_credential = respx.post(f"{settings.platform_base_url}/api/v1/credentials/").mock(
        return_value=Response(201, json={"id": "credential-1", "token": "managed-token"})
    )

    token = await AceDataCloudOAuthProvider()._get_user_credential(_jwt(owner))

    assert token == "managed-token"
    assert json.loads(create_app.calls.last.request.content) == {"type": "Usage", "scope": "Global"}
    assert get_creds.called
    assert json.loads(create_credential.calls.last.request.content)["name"] == "OAuth MCP"
