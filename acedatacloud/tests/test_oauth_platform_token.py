"""Tests for the durable platform-token OAuth flow (mint / reuse / no-refresh)."""

import base64
import json
from unittest.mock import AsyncMock
from urllib.parse import parse_qs, urlparse

import fakeredis.aioredis
import httpx
import pytest
import respx
from mcp.server.auth.provider import (
    AuthorizationParams,
    OAuthClientInformationFull,
    RefreshToken,
    TokenError,
)
from pydantic import AnyUrl
from starlette.requests import Request

from core.config import settings
from core.oauth import PLATFORM_TOKEN_TAG, AceDataCloudOAuthProvider

API = "https://platform.acedata.cloud/api/v1"


@pytest.mark.asyncio
async def test_authorize_requests_account_derived_scopes(monkeypatch):
    monkeypatch.setattr(settings, "server_url", "https://mcp.acedata.cloud")
    monkeypatch.setattr(settings, "oauth_client_id", "platform-mcp")
    provider = AceDataCloudOAuthProvider()
    client = OAuthClientInformationFull(
        client_id="mcp-client", redirect_uris=[AnyUrl("https://client.example/callback")]
    )
    params = AuthorizationParams(
        state="client-state",
        scopes=["mcp:access"],
        code_challenge="client-challenge",
        redirect_uri=AnyUrl("https://client.example/callback"),
        redirect_uri_provided_explicitly=True,
    )

    query = parse_qs(urlparse(await provider.authorize(client, params)).query)

    assert query["scope"] == ["account"]
    assert query["client_id"] == ["platform-mcp"]
    assert query["redirect_uri"] == ["https://mcp.acedata.cloud/oauth/callback"]
    assert query["code_challenge_method"] == ["S256"]
    pending = provider._pending_auth[query["state"][0]]
    assert pending["scopes"] == ["mcp:access"]
    assert pending["state"] == "client-state"


def _make_jwt(claims: dict) -> str:
    payload = base64.urlsafe_b64encode(json.dumps(claims).encode()).rstrip(b"=").decode()
    return f"aaa.{payload}.bbb"


@respx.mock
@pytest.mark.asyncio
@pytest.mark.parametrize("pagination_key", ["items", "results"])
async def test_get_platform_token_reuses_existing_tagged_token(pagination_key):
    provider = AceDataCloudOAuthProvider()
    jwt = _make_jwt({"user_id": "u1"})
    list_route = respx.get(f"{API}/platform-tokens/").mock(
        return_value=httpx.Response(
            200,
            json={pagination_key: [{"token": "platform-existing", "tags": [PLATFORM_TOKEN_TAG]}]},
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
    assert provider._extract_token({"count": 1, "items": [{"token": "platform-a"}]}) == "platform-a"
    assert provider._extract_token({"results": [{"token": "platform-a"}]}) == "platform-a"
    assert provider._extract_token([{"token": "platform-b"}]) == "platform-b"
    assert provider._extract_token({"results": []}) is None
    assert provider._extract_token({"count": 0, "items": []}) is None
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


@pytest.mark.asyncio
async def test_oauth_registration_callback_and_code_exchange_cross_replicas(monkeypatch):
    monkeypatch.setattr(settings, "server_url", "https://mcp.acedata.cloud")
    monkeypatch.setattr(settings, "oauth_client_id", "platform-mcp")
    redis_server = fakeredis.FakeServer()
    first_redis = fakeredis.aioredis.FakeRedis(server=redis_server, decode_responses=True)
    second_redis = fakeredis.aioredis.FakeRedis(server=redis_server, decode_responses=True)
    first = AceDataCloudOAuthProvider(redis_client=first_redis, state_key="0" * 64)
    second = AceDataCloudOAuthProvider(redis_client=second_redis, state_key="0" * 64)
    redirect_uri = "https://auth.acedata.cloud/user/connections/callback?connection_id=abc"
    client = OAuthClientInformationFull(
        client_id="dcr-client",
        redirect_uris=[AnyUrl(redirect_uri)],
        token_endpoint_auth_method="client_secret_post",
        client_secret="dcr-secret",
    )

    await first.register_client(client)
    registered = await second.get_client("dcr-client")
    assert registered is not None
    assert registered.redirect_uris == [AnyUrl(redirect_uri)]
    assert await second.get_client("unknown-client") is None
    assert "dcr-secret" not in await second_redis.get("mcp:acedatacloud:oauth:client:dcr-client")

    upstream_url = await second.authorize(
        registered,
        AuthorizationParams(
            state="studio-state",
            scopes=["mcp:access"],
            code_challenge="studio-challenge",
            redirect_uri=AnyUrl(redirect_uri),
            redirect_uri_provided_explicitly=True,
        ),
    )
    upstream_state = parse_qs(urlparse(upstream_url).query)["state"][0]
    first._exchange_code_for_tokens = AsyncMock(return_value={"access_token": "account-jwt"})
    first._get_platform_token = AsyncMock(return_value="platform-test-token")
    request = Request(
        {
            "type": "http",
            "method": "GET",
            "path": "/oauth/callback",
            "query_string": f"state={upstream_state}&code=upstream-code".encode(),
            "headers": [],
        }
    )
    response = await first.handle_callback(request)
    assert response.status_code == 302
    redirected = urlparse(response.headers["location"])
    assert (
        f"{redirected.scheme}://{redirected.netloc}{redirected.path}" == redirect_uri.split("?")[0]
    )
    assert parse_qs(redirected.query)["connection_id"] == ["abc"]
    assert parse_qs(redirected.query)["state"] == ["studio-state"]
    code = parse_qs(redirected.query)["code"][0]
    assert "platform-test-token" not in await second_redis.get(
        f"mcp:acedatacloud:oauth:code:{code}"
    )

    loaded = await second.load_authorization_code(registered, code)
    assert loaded is not None
    token = await second.exchange_authorization_code(registered, loaded)
    assert token.access_token == "platform-test-token"
    assert await first.load_authorization_code(registered, code) is None
    with pytest.raises(ValueError, match="already used"):
        await first.exchange_authorization_code(registered, loaded)
