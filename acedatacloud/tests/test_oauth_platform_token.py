"""Tests for the durable platform-token OAuth flow (mint / reuse / no-refresh)."""

import base64
import json

import httpx
import pytest
import respx
from mcp.server.auth.provider import RefreshToken, TokenError

from core.oauth import PLATFORM_TOKEN_TAG, AceDataCloudOAuthProvider

API = "https://platform.acedata.cloud/api/v1"


def _make_jwt(claims: dict) -> str:
    payload = base64.urlsafe_b64encode(json.dumps(claims).encode()).rstrip(b"=").decode()
    return f"aaa.{payload}.bbb"


@respx.mock
@pytest.mark.asyncio
async def test_get_platform_token_reuses_existing_tagged_token():
    provider = AceDataCloudOAuthProvider()
    jwt = _make_jwt({"user_id": "u1"})
    list_route = respx.get(f"{API}/platform-tokens/").mock(
        return_value=httpx.Response(
            200, json={"results": [{"token": "platform-existing", "tags": [PLATFORM_TOKEN_TAG]}]}
        )
    )
    create_route = respx.post(f"{API}/platform-tokens/").mock(
        return_value=httpx.Response(201, json={"token": "platform-new"})
    )

    token = await provider._get_platform_token(jwt)

    assert token == "platform-existing"
    assert list_route.called
    assert create_route.call_count == 0  # reuse must not mint a new token


@respx.mock
@pytest.mark.asyncio
async def test_get_platform_token_creates_when_none_exist():
    provider = AceDataCloudOAuthProvider()
    jwt = _make_jwt({"user_id": "u1"})
    respx.get(f"{API}/platform-tokens/").mock(
        return_value=httpx.Response(200, json={"results": []})
    )
    create_route = respx.post(f"{API}/platform-tokens/").mock(
        return_value=httpx.Response(201, json={"token": "platform-new"})
    )

    token = await provider._get_platform_token(jwt)

    assert token == "platform-new"
    # The created token must be tagged so future authorizations reuse it.
    body = json.loads(create_route.calls.last.request.content)
    assert PLATFORM_TOKEN_TAG in body["tags"]


@respx.mock
@pytest.mark.asyncio
async def test_get_platform_token_returns_none_on_create_failure():
    provider = AceDataCloudOAuthProvider()
    jwt = _make_jwt({"user_id": "u1"})
    respx.get(f"{API}/platform-tokens/").mock(
        return_value=httpx.Response(200, json={"results": []})
    )
    respx.post(f"{API}/platform-tokens/").mock(return_value=httpx.Response(403, text="forbidden"))

    assert await provider._get_platform_token(jwt) is None


def test_extract_token_handles_paginated_and_plain_list():
    provider = AceDataCloudOAuthProvider()
    assert provider._extract_token({"results": [{"token": "platform-a"}]}) == "platform-a"
    assert provider._extract_token([{"token": "platform-b"}]) == "platform-b"
    assert provider._extract_token({"results": []}) is None
    assert provider._extract_token([{"no_token": 1}]) is None


@pytest.mark.asyncio
async def test_exchange_refresh_token_is_unsupported():
    provider = AceDataCloudOAuthProvider()
    rt = RefreshToken(token="whatever", client_id="c1", scopes=["mcp:access"])
    with pytest.raises(TokenError) as exc:
        await provider.exchange_refresh_token(client=None, refresh_token=rt, scopes=[])
    assert exc.value.error == "invalid_grant"


@pytest.mark.asyncio
async def test_load_refresh_token_returns_none():
    provider = AceDataCloudOAuthProvider()
    assert await provider.load_refresh_token(client=None, refresh_token="x") is None
