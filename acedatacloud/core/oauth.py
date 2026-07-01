"""OAuth 2.1 provider for AceDataCloud MCP servers.

Implements the MCP SDK's OAuthAuthorizationServerProvider interface,
delegating user authentication to AceDataCloud's OAuth 2.0 Authorization Server.

Flow:
1. Claude.ai redirects user to /authorize
2. MCP server redirects to auth.acedata.cloud/oauth2/authorize (consent page)
3. User logs in (if needed), sees consent page, approves
4. auth.acedata.cloud issues an authorization code, redirects to /oauth/callback
5. MCP server exchanges code for JWT via POST /oauth2/token (with PKCE)
6. MCP server uses JWT to fetch/create user's API credential
7. Issues the credential token as the OAuth access_token
8. Claude uses this token for all subsequent MCP requests
"""

import base64
import hashlib
import json
import secrets
import time
from urllib.parse import urlencode

import httpx
from loguru import logger
from mcp.server.auth.provider import (
    AccessToken,
    AuthorizationCode,
    AuthorizationParams,
    OAuthClientInformationFull,
    OAuthToken,
    RefreshToken,
)
from starlette.requests import Request
from starlette.responses import JSONResponse, RedirectResponse

from core.client import set_request_api_token
from core.config import settings

MCP_ACCESS_SCOPE = "mcp:access"


def _normalize_scopes(scopes: list[str] | None) -> list[str]:
    return scopes or [MCP_ACCESS_SCOPE]


class AceDataCloudOAuthProvider:
    """OAuth provider that delegates authentication to AceDataCloud platform.

    In-memory storage is used for auth state (suitable for single-replica K8s deployment).
    """

    def __init__(self) -> None:
        self._clients: dict[str, OAuthClientInformationFull] = {}
        self._auth_codes: dict[
            str, tuple[AuthorizationCode, str]
        ] = {}  # code → (AuthCode, api_token)
        self._access_tokens: dict[str, AccessToken] = {}
        self._refresh_tokens: dict[str, RefreshToken] = {}
        self._pending_auth: dict[str, dict] = {}  # mcp_state → {client_id, params}

    async def get_client(self, client_id: str) -> OAuthClientInformationFull | None:
        client = self._clients.get(client_id)
        if client:
            return client
        # After pod restart, registered clients are forgotten. Accept any
        # client_id so token/refresh calls don't get a hard 401 — the real
        # auth gate is load_access_token's Bearer validation on /mcp.
        synthetic = OAuthClientInformationFull(
            client_id=client_id,
            redirect_uris=["https://auth.acedata.cloud/user/connections"],
            token_endpoint_auth_method="none",
            grant_types=["authorization_code", "refresh_token"],
            response_types=["code"],
        )
        self._clients[client_id] = synthetic
        logger.debug(f"Synthesized client record for {client_id} (post-restart)")
        return synthetic

    async def register_client(self, client_info: OAuthClientInformationFull) -> None:
        client_id = client_info.client_id
        assert client_id is not None
        self._clients[client_id] = client_info
        logger.info(f"Registered OAuth client: {client_id}")

    async def authorize(
        self, client: OAuthClientInformationFull, params: AuthorizationParams
    ) -> str:
        """Redirect user to AceDataCloud OAuth 2.0 consent page."""
        # Generate state key for tracking this auth flow
        mcp_state = secrets.token_urlsafe(32)

        # Generate PKCE pair for auth.acedata.cloud token exchange
        code_verifier = secrets.token_urlsafe(48)
        digest = hashlib.sha256(code_verifier.encode("ascii")).digest()
        auth_code_challenge = base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")

        self._pending_auth[mcp_state] = {
            "client_id": client.client_id,
            "redirect_uri": str(params.redirect_uri),
            "state": params.state,
            "code_challenge": params.code_challenge,
            "redirect_uri_provided_explicitly": params.redirect_uri_provided_explicitly,
            "scopes": _normalize_scopes(params.scopes),
            "resource": params.resource,
            "auth_code_verifier": code_verifier,
        }

        # Build callback URL
        callback_url = f"{settings.server_url}/oauth/callback"

        # Build OAuth 2.0 authorize URL
        auth_params = {
            "client_id": settings.oauth_client_id,
            "redirect_uri": callback_url,
            "response_type": "code",
            "scope": "profile platform",
            "state": mcp_state,
            "code_challenge": auth_code_challenge,
            "code_challenge_method": "S256",
        }
        auth_url = f"{settings.auth_base_url}/oauth2/authorize?{urlencode(auth_params)}"
        logger.info(f"OAuth authorize: redirecting to consent page (mcp_state={mcp_state})")
        return auth_url

    async def handle_callback(self, request: Request) -> RedirectResponse | JSONResponse:
        """Handle the callback from AceDataCloud OAuth 2.0 after user consent.

        This is called as a Starlette route handler, not part of the SDK interface.
        """
        mcp_state = request.query_params.get("state")
        adc_code = request.query_params.get("code")

        logger.debug(
            f"handle_callback: state={mcp_state}, code={adc_code[:16] if adc_code else None}, "
            f"pending_auth_keys={list(self._pending_auth.keys())}"
        )

        if not mcp_state or not adc_code:
            logger.error(f"handle_callback: missing state={mcp_state} or code={adc_code}")
            return JSONResponse({"error": "Missing state or code parameter"}, status_code=400)

        pending = self._pending_auth.pop(mcp_state, None)
        if not pending:
            logger.error(
                f"handle_callback: state {mcp_state} not found in pending_auth. "
                f"Available states: {list(self._pending_auth.keys())}"
            )
            return JSONResponse({"error": "Invalid or expired state"}, status_code=400)

        try:
            # Exchange AceDataCloud OAuth 2.0 code for JWT (with PKCE)
            code_verifier = pending.get("auth_code_verifier", "")
            logger.debug(
                f"handle_callback: exchanging code for JWT, pending_keys={list(pending.keys())}"
            )
            jwt_token = await self._exchange_code_for_jwt(adc_code, code_verifier)
            logger.debug(
                f"handle_callback: JWT exchange returned "
                f"{'token=' + jwt_token[:32] + '...' if jwt_token else 'None'}"
            )
            if not jwt_token:
                logger.error("handle_callback: JWT exchange failed, returning 502")
                return JSONResponse(
                    {"error": "Failed to exchange authorization code"}, status_code=502
                )

            # Fetch user's API credential token from PlatformBackend
            logger.debug("handle_callback: fetching user credential...")
            api_token = await self._get_user_credential(jwt_token)
            logger.debug(
                f"handle_callback: _get_user_credential returned "
                f"{'token=' + api_token[:12] + '...' if api_token else 'None'}"
            )
            if not api_token:
                logger.error("handle_callback: credential fetch returned None, returning 403")
                return JSONResponse(
                    {
                        "error": "No API credential found. Please create an API key at "
                        "https://platform.acedata.cloud first."
                    },
                    status_code=403,
                )

            # Create MCP authorization code
            auth_code_str = secrets.token_urlsafe(48)
            auth_code = AuthorizationCode(
                code=auth_code_str,
                scopes=_normalize_scopes(pending.get("scopes")),
                expires_at=time.time() + 600,  # 10 minutes
                client_id=pending["client_id"],
                code_challenge=pending["code_challenge"],
                redirect_uri=pending["redirect_uri"],
                redirect_uri_provided_explicitly=pending["redirect_uri_provided_explicitly"],
                resource=pending.get("resource"),
            )
            self._auth_codes[auth_code_str] = (auth_code, api_token)

            # Redirect back to Claude with the MCP auth code
            redirect_uri = pending["redirect_uri"]
            params = {"code": auth_code_str}
            if pending.get("state"):
                params["state"] = pending["state"]

            separator = "&" if "?" in redirect_uri else "?"
            redirect_url = f"{redirect_uri}{separator}{urlencode(params)}"
            logger.info("OAuth callback: issuing auth code, redirecting to client")
            return RedirectResponse(url=redirect_url, status_code=302)

        except Exception:
            logger.exception("OAuth callback error")
            return JSONResponse({"error": "Internal server error"}, status_code=500)

    async def load_authorization_code(
        self,
        client: OAuthClientInformationFull,  # noqa: ARG002
        authorization_code: str,
    ) -> AuthorizationCode | None:
        data = self._auth_codes.get(authorization_code)
        if not data:
            return None
        auth_code, _ = data
        if auth_code.expires_at < time.time():
            self._auth_codes.pop(authorization_code, None)
            return None
        return auth_code

    async def exchange_authorization_code(
        self, client: OAuthClientInformationFull, authorization_code: AuthorizationCode
    ) -> OAuthToken:
        data = self._auth_codes.pop(authorization_code.code, None)
        if not data:
            raise ValueError("Authorization code not found or already used")
        _, api_token = data

        client_id = client.client_id or ""

        # Store access token mapping
        self._access_tokens[api_token] = AccessToken(
            token=api_token,
            client_id=client_id,
            scopes=_normalize_scopes(authorization_code.scopes),
            expires_at=None,  # API credential tokens don't expire by time
        )

        logger.info(f"OAuth token exchange: issued access token for client {client_id}")
        # No refresh_token: the access_token is a long-lived API credential
        # (~15 days). Issuing a refresh_token causes clients to attempt token
        # refresh after pod restarts, which fails because in-memory state is
        # lost — leading to cascading 401s. Without a refresh_token, clients
        # simply reuse the Bearer token (accepted by load_access_token's
        # direct fallback) until it naturally expires.
        return OAuthToken(
            access_token=api_token,
            token_type="Bearer",
            scope=" ".join(_normalize_scopes(authorization_code.scopes)),
        )

    async def load_refresh_token(
        self,
        client: OAuthClientInformationFull,
        refresh_token: str,
    ) -> RefreshToken | None:
        stored = self._refresh_tokens.get(refresh_token)
        if stored:
            return stored
        # After pod restart, refresh tokens are forgotten. Synthesize one so
        # exchange_refresh_token can proceed (it will re-issue the existing
        # access token via direct fallback).
        return RefreshToken(
            token=refresh_token,
            client_id=client.client_id or "",
            scopes=[MCP_ACCESS_SCOPE],
        )

    async def exchange_refresh_token(
        self,
        client: OAuthClientInformationFull,
        refresh_token: RefreshToken,
        scopes: list[str],
    ) -> OAuthToken:
        # For refresh, we reuse the same API credential token
        self._refresh_tokens.pop(refresh_token.token, None)

        client_id = client.client_id or ""

        # Find the access token for this client
        for token, at in self._access_tokens.items():
            if at.client_id == client_id:
                return OAuthToken(
                    access_token=token,
                    token_type="Bearer",
                    scope=" ".join(_normalize_scopes(scopes or refresh_token.scopes)),
                )

        # Post-restart: no access_tokens in memory. The token handler will
        # return invalid_grant; the client will fall back to using its stored
        # Bearer token directly (which load_access_token accepts).
        from mcp.server.auth.provider import TokenError

        raise TokenError(
            error="invalid_grant",
            error_description="Session expired, please use your existing access token directly",
        )

    async def load_access_token(self, token: str) -> AccessToken | None:
        """Validate an access token.

        Accepts both OAuth-issued tokens and direct API credential tokens.
        Direct tokens are accepted since the real validation happens at api.acedata.cloud.
        """
        # Check OAuth-issued tokens first
        if token in self._access_tokens:
            access_token = self._access_tokens[token]
            if access_token.expires_at and time.time() > access_token.expires_at:
                self._access_tokens.pop(token, None)
                return None
            set_request_api_token(token)
            return access_token

        # Accept direct API credential tokens (for VS Code, Cursor, etc.)
        set_request_api_token(token)
        return AccessToken(token=token, client_id="direct", scopes=[MCP_ACCESS_SCOPE])

    async def revoke_token(self, token: AccessToken | RefreshToken) -> None:
        if isinstance(token, AccessToken):
            self._access_tokens.pop(token.token, None)
        elif isinstance(token, RefreshToken):
            self._refresh_tokens.pop(token.token, None)
        logger.info(f"Revoked token: {token.token[:8]}...")

    # --- Internal helpers ---

    @staticmethod
    def _decode_jwt_payload(token: str) -> dict | None:
        """Decode JWT payload without verification (for debug logging only)."""
        try:
            parts = token.split(".")
            if len(parts) != 3:
                logger.debug(f"JWT has {len(parts)} parts, expected 3")
                return None
            payload_b64 = parts[1]
            # Add padding
            padding = 4 - len(payload_b64) % 4
            if padding != 4:
                payload_b64 += "=" * padding
            payload_bytes = base64.urlsafe_b64decode(payload_b64)
            payload: dict = json.loads(payload_bytes)
            return payload
        except Exception as e:
            logger.debug(f"Failed to decode JWT payload: {e}")
            return None

    async def _exchange_code_for_jwt(self, code: str, code_verifier: str) -> str | None:
        """Exchange AceDataCloud OAuth 2.0 authorization code for JWT."""
        callback_url = f"{settings.server_url}/oauth/callback"
        token_url = f"{settings.auth_base_url}/oauth2/token"
        logger.debug(
            f"Exchanging code for JWT: token_url={token_url}, "
            f"client_id={settings.oauth_client_id}, "
            f"redirect_uri={callback_url}, "
            f"code={code[:16]}..., "
            f"code_verifier={code_verifier[:16]}..."
        )
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.post(
                    token_url,
                    data={
                        "grant_type": "authorization_code",
                        "code": code,
                        "client_id": settings.oauth_client_id,
                        "redirect_uri": callback_url,
                        "code_verifier": code_verifier,
                    },
                )
                logger.debug(
                    f"Token exchange response: status={response.status_code}, "
                    f"body={response.text[:500]}"
                )
                if response.status_code == 200:
                    data = response.json()
                    access_token: str | None = data.get("access_token")
                    if access_token:
                        # Decode and log JWT claims for debugging
                        claims = self._decode_jwt_payload(access_token)
                        if claims:
                            logger.debug(
                                f"JWT claims: user_id={claims.get('user_id')}, "
                                f"scope={claims.get('scope')}, "
                                f"permissions={claims.get('permissions')}, "
                                f"is_superuser={claims.get('is_superuser')}, "
                                f"is_verified={claims.get('is_verified')}, "
                                f"exp={claims.get('exp')}, "
                                f"iat={claims.get('iat')}, "
                                f"token_type={claims.get('token_type')}, "
                                f"all_keys={list(claims.keys())}"
                            )
                        else:
                            logger.warning("Could not decode JWT payload for debug")
                    else:
                        logger.error(
                            f"Token exchange 200 but no access_token in response. "
                            f"Keys: {list(data.keys())}"
                        )
                    return access_token
                logger.error(f"OAuth token exchange failed: {response.status_code} {response.text}")
        except Exception:
            logger.exception("OAuth token exchange error")
        return None

    async def _get_user_credential(self, jwt_token: str) -> str | None:
        """Return the access token to use against the management API.

        Unlike the per-service MCP servers (which mint an api.acedata.cloud
        credential), this management MCP talks to platform.acedata.cloud, whose
        JWTAuthentication accepts the AceDataCloud JWT directly (valid ~15 days).
        So the JWT itself becomes the access token — no provisioning needed.
        """
        claims = self._decode_jwt_payload(jwt_token)
        if claims:
            logger.info(
                f"OAuth: issuing JWT as access token "
                f"(user_id={claims.get('user_id')}, exp={claims.get('exp')})"
            )
        else:
            logger.warning("_get_user_credential: could not decode JWT (issuing as-is)")
        return jwt_token
