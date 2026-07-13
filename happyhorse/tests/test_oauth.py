"""Security tests for the Happy Horse OAuth provider."""

from types import SimpleNamespace

import pytest
from mcp.server.auth.provider import AccessToken, OAuthClientInformationFull
from pydantic import AnyUrl

from core.oauth import AceDataCloudOAuthProvider


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
