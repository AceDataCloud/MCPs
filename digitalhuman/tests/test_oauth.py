"""Security tests for the Digital Human OAuth provider."""

from types import SimpleNamespace
from unittest.mock import AsyncMock
from urllib.parse import parse_qs, urlparse

import fakeredis
import fakeredis.aioredis
import pytest
from mcp.server.auth.provider import (
    AccessToken,
    AuthorizationParams,
    OAuthClientInformationFull,
)
from pydantic import AnyUrl
from starlette.requests import Request

from core.config import settings
from core.oauth import AceDataCloudOAuthProvider


def test_decode_jwt_payload_extracts_owner() -> None:
    import base64
    import json

    payload = base64.urlsafe_b64encode(json.dumps({"user_id": "owner-1"}).encode()).rstrip(b"=")
    token = f"header.{payload.decode()}.signature"
    assert AceDataCloudOAuthProvider._decode_jwt_payload(token) == {"user_id": "owner-1"}


def _client() -> OAuthClientInformationFull:
    return OAuthClientInformationFull(
        client_id="client-1",
        redirect_uris=[AnyUrl("https://client.example.com/callback")],
        token_endpoint_auth_method="none",
        grant_types=["authorization_code"],
        response_types=["code"],
    )


async def test_authorize_rejects_unregistered_redirect_uri() -> None:
    provider = AceDataCloudOAuthProvider()
    params = SimpleNamespace(
        redirect_uri=AnyUrl("https://attacker.example.com/callback"),
        state="state",
        code_challenge="challenge",
        redirect_uri_provided_explicitly=True,
        scopes=["mcp:access"],
        resource=None,
    )

    with pytest.raises(ValueError, match="not registered"):
        await provider.authorize(_client(), params)  # type: ignore[arg-type]


async def test_revoked_token_is_not_accepted_as_direct_bearer() -> None:
    provider = AceDataCloudOAuthProvider()
    token = AccessToken(token="credential-token", client_id="client-1", scopes=["mcp:access"])

    assert await provider.load_access_token(token.token) is not None
    await provider.revoke_token(token)

    assert await provider.load_access_token(token.token) is None


async def test_oauth_state_and_revocation_cross_replicas(monkeypatch) -> None:
    monkeypatch.setattr(settings, "server_url", "https://video.mcp.acedata.cloud")
    monkeypatch.setattr(settings, "oauth_client_id", "upstream-client")
    redis_server = fakeredis.FakeServer()
    first_redis = fakeredis.aioredis.FakeRedis(server=redis_server, decode_responses=True)
    second_redis = fakeredis.aioredis.FakeRedis(server=redis_server, decode_responses=True)
    first = AceDataCloudOAuthProvider(first_redis, "0" * 64)
    second = AceDataCloudOAuthProvider(second_redis, "0" * 64)
    await first.register_client(_client())
    client = await second.get_client("client-1")
    assert client.redirect_uris == _client().redirect_uris

    auth_url = await second.authorize(
        client,
        AuthorizationParams(
            state="client-state",
            scopes=["mcp:access"],
            code_challenge="client-challenge",
            redirect_uri=client.redirect_uris[0],
            redirect_uri_provided_explicitly=True,
        ),
    )
    state = parse_qs(urlparse(auth_url).query)["state"][0]
    first._exchange_code = AsyncMock(return_value="upstream-jwt")
    first._get_user_credential = AsyncMock(return_value="durable-token")
    response = await first.handle_callback(
        Request(
            {
                "type": "http",
                "query_string": f"state={state}&code=upstream-code".encode(),
            }
        )
    )
    assert response.status_code == 302
    code = parse_qs(urlparse(response.headers["location"]).query)["code"][0]
    loaded = await second.load_authorization_code(client, code)
    token = await second.exchange_authorization_code(client, loaded)
    assert token.access_token == "durable-token"
    await first.revoke_token(
        AccessToken(token=token.access_token, client_id="client-1", scopes=["mcp:access"])
    )
    assert await second.load_access_token(token.access_token) is None
