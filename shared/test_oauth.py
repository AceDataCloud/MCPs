"""Behavior of the shared provider; all platform traffic is mocked."""

import base64
import hashlib
import json
from types import SimpleNamespace
from unittest.mock import AsyncMock
from urllib.parse import parse_qs, urlsplit

import fakeredis
import fakeredis.aioredis
import pytest
from mcp.server.auth.provider import (
    AuthorizationParams,
    OAuthClientInformationFull,
    TokenError,
)
from pydantic import AnyUrl
from starlette.requests import Request

from shared import oauth


@pytest.fixture
def provider(monkeypatch):
    monkeypatch.setattr(
        oauth,
        "settings",
        SimpleNamespace(
            server_name="suno",
            server_url="https://mcp.example.com",
            auth_base_url="https://auth.example.com",
            platform_base_url="https://platform.example.com",
            oauth_client_id="upstream-client",
        ),
    )
    monkeypatch.setattr(oauth, "set_request_api_token", lambda token: None)
    return oauth.AceDataCloudOAuthProvider()


@pytest.fixture
def client():
    return OAuthClientInformationFull(
        client_id="mcp-client",
        redirect_uris=[AnyUrl("https://client.example.com/callback?existing=1")],
        token_endpoint_auth_method="none",
        grant_types=["authorization_code"],
        response_types=["code"],
    )


def params(client):
    return AuthorizationParams(
        redirect_uri=client.redirect_uris[0],
        state="client-state",
        code_challenge="client-pkce-challenge",
        redirect_uri_provided_explicitly=True,
        scopes=[],
        resource="https://mcp.example.com/mcp",
    )


def callback(state, code="upstream-code"):
    return Request(
        {"type": "http", "query_string": f"state={state}&code={code}".encode()}
    )


def jwt():
    payload = base64.urlsafe_b64encode(json.dumps({"user_id": "owner"}).encode())
    return f"header.{payload.decode().rstrip('=')}.signature"


@pytest.mark.asyncio
async def test_pkce_callback_and_single_use_durable_token(provider, client, respx_mock):
    url = await provider.authorize(client, params(client))
    query = parse_qs(urlsplit(url).query)
    state = query["state"][0]
    verifier = provider._pending_auth[state]["auth_code_verifier"]
    expected = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest())
    assert query["code_challenge"] == [expected.decode().rstrip("=")]
    assert query["code_challenge_method"] == ["S256"]
    assert set(query["scope"][0].split()) == {
        "profile:read",
        "applications:read",
        "applications:write",
        "credentials:read",
        "credentials:write",
    }
    assert query["redirect_uri"] == ["https://mcp.example.com/oauth/callback"]

    exchange = respx_mock.post("https://auth.example.com/oauth2/token").respond(
        200, json={"access_token": jwt()}
    )
    respx_mock.get("https://platform.example.com/api/v1/applications/").respond(
        200, json={"items": [{"id": "global-app"}]}
    )
    respx_mock.get("https://platform.example.com/api/v1/credentials/").respond(
        200, json={"items": [{"id": "credential", "token": "durable-token"}]}
    )
    response = await provider.handle_callback(callback(state))
    assert response.status_code == 302
    redirect = parse_qs(urlsplit(response.headers["location"]).query)
    assert redirect["existing"] == ["1"]
    assert redirect["state"] == ["client-state"]
    assert parse_qs(exchange.calls.last.request.content.decode())["code_verifier"] == [
        verifier
    ]
    assert (await provider.handle_callback(callback(state))).status_code == 400

    code = await provider.load_authorization_code(client, redirect["code"][0])
    assert code.code_challenge == "client-pkce-challenge"
    assert code.resource == "https://mcp.example.com/mcp"
    token = await provider.exchange_authorization_code(client, code)
    assert token.access_token == "durable-token"
    assert token.scope == "mcp:access"
    assert token.refresh_token is None
    assert (await provider.load_access_token(token.access_token)).expires_at is None
    with pytest.raises(ValueError, match="already used"):
        await provider.exchange_authorization_code(client, code)


@pytest.mark.asyncio
async def test_credential_creation_uses_global_usage_and_shared_name(
    provider, respx_mock
):
    apps = "https://platform.example.com/api/v1/applications/"
    credentials = "https://platform.example.com/api/v1/credentials/"
    lookup = respx_mock.get(apps).respond(200, json={"results": []})
    create_app = respx_mock.post(apps).respond(201, json={"id": "new-app"})
    credential_lookup = respx_mock.get(credentials).respond(200, json={"results": []})
    create_credential = respx_mock.post(credentials).respond(
        201, json={"token": "new-credential"}
    )
    assert await provider._get_user_credential(jwt()) == "new-credential"
    assert lookup.calls.last.request.url.params["user_id"] == "owner"
    assert json.loads(create_app.calls.last.request.content) == {
        "type": "Usage",
        "scope": "Global",
    }
    assert dict(credential_lookup.calls.last.request.url.params) == {
        "application_id": "new-app",
        "name": "OAuth MCP",
    }
    assert json.loads(create_credential.calls.last.request.content) == {
        "application_id": "new-app",
        "name": "OAuth MCP",
    }


@pytest.mark.asyncio
async def test_callback_preserves_exchange_and_credential_errors(
    provider, client, respx_mock
):
    async def authorize():
        url = await provider.authorize(client, params(client))
        return parse_qs(urlsplit(url).query)["state"][0]

    exchange = respx_mock.post("https://auth.example.com/oauth2/token").respond(400)
    response = await provider.handle_callback(callback(await authorize()))
    assert response.status_code == 502
    exchange.respond(200, json={"access_token": jwt()})
    respx_mock.get("https://platform.example.com/api/v1/applications/").respond(
        200, json={"items": []}
    )
    respx_mock.post("https://platform.example.com/api/v1/applications/").respond(403)
    response = await provider.handle_callback(callback(await authorize()))
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_expired_code_and_unsupported_refresh(provider, client, monkeypatch):
    code = oauth.AuthorizationCode(
        code="expired",
        scopes=["mcp:access"],
        expires_at=10,
        client_id=client.client_id,
        code_challenge="pkce",
        redirect_uri=client.redirect_uris[0],
        redirect_uri_provided_explicitly=True,
    )
    provider._auth_codes[code.code] = (code, "credential")
    monkeypatch.setattr(oauth.time, "time", lambda: 11)
    assert await provider.load_authorization_code(client, code.code) is None
    assert code.code not in provider._auth_codes
    assert await provider.load_refresh_token(client, "old-refresh") is None
    with pytest.raises(TokenError) as error:
        await provider.exchange_refresh_token(client, None, [])
    assert error.value.error == "invalid_grant"


@pytest.mark.asyncio
async def test_direct_credential_context_and_post_restart_client(provider, monkeypatch):
    captured = []
    monkeypatch.setattr(oauth, "set_request_api_token", captured.append)
    token = await provider.load_access_token("direct-credential")
    assert token.client_id == "direct"
    assert token.scopes == ["mcp:access"]
    assert captured == ["direct-credential"]
    assert await provider.get_client("previous-client") is None


@pytest.mark.asyncio
async def test_oauth_flow_and_revocation_work_across_replicas(provider, client):
    redis_server = fakeredis.FakeServer()
    first_redis = fakeredis.aioredis.FakeRedis(
        server=redis_server, decode_responses=True
    )
    second_redis = fakeredis.aioredis.FakeRedis(
        server=redis_server, decode_responses=True
    )
    first = oauth.AceDataCloudOAuthProvider(first_redis, "0" * 64)
    second = oauth.AceDataCloudOAuthProvider(second_redis, "0" * 64)
    await first.register_client(client)

    registered = await second.get_client(client.client_id)
    assert registered.redirect_uris == client.redirect_uris
    assert await second.get_client("unregistered") is None

    upstream_url = await second.authorize(registered, params(registered))
    state = parse_qs(urlsplit(upstream_url).query)["state"][0]
    first._exchange_code_for_tokens = AsyncMock(return_value={"access_token": "jwt"})
    first._get_user_credential = AsyncMock(return_value="durable-test-token")
    response = await first.handle_callback(callback(state))
    assert response.status_code == 302
    redirected = parse_qs(urlsplit(response.headers["location"]).query)
    assert redirected["existing"] == ["1"]
    assert redirected["state"] == ["client-state"]
    code = redirected["code"][0]
    assert "durable-test-token" not in await second_redis.get(
        first._state._key("code", code)
    )

    loaded = await second.load_authorization_code(registered, code)
    token = await second.exchange_authorization_code(registered, loaded)
    assert token.access_token == "durable-test-token"
    assert await first.load_authorization_code(registered, code) is None
    await first.revoke_token(await second.load_access_token(token.access_token))
    assert await second.load_access_token(token.access_token) is None
