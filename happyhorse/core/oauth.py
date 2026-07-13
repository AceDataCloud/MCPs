"""OAuth 2.1 provider for the hosted Happy Horse MCP server."""

import base64
import hashlib
import secrets
import time
from typing import Any
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
    """Delegate login to AceDataCloud and issue a durable API credential."""

    def __init__(self) -> None:
        self._clients: dict[str, OAuthClientInformationFull] = {}
        self._auth_codes: dict[str, tuple[AuthorizationCode, str]] = {}
        self._access_tokens: dict[str, AccessToken] = {}
        self._revoked_tokens: set[str] = set()
        self._pending_auth: dict[str, dict[str, Any]] = {}

    async def get_client(self, client_id: str) -> OAuthClientInformationFull | None:
        return self._clients.get(client_id)

    async def register_client(self, client_info: OAuthClientInformationFull) -> None:
        client_id = client_info.client_id
        if not client_id:
            raise ValueError("OAuth client_id is required")
        self._clients[client_id] = client_info

    async def authorize(
        self, client: OAuthClientInformationFull, params: AuthorizationParams
    ) -> str:
        """Redirect the MCP client to AceDataCloud consent."""
        redirect_uri = str(params.redirect_uri)
        if redirect_uri not in {str(uri) for uri in client.redirect_uris or []}:
            raise ValueError("OAuth redirect_uri is not registered for this client")
        mcp_state = secrets.token_urlsafe(32)
        code_verifier = secrets.token_urlsafe(48)
        digest = hashlib.sha256(code_verifier.encode("ascii")).digest()
        challenge = base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")
        self._pending_auth[mcp_state] = {
            "client_id": client.client_id,
            "redirect_uri": redirect_uri,
            "state": params.state,
            "code_challenge": params.code_challenge,
            "redirect_uri_provided_explicitly": params.redirect_uri_provided_explicitly,
            "scopes": _normalize_scopes(params.scopes),
            "resource": params.resource,
            "auth_code_verifier": code_verifier,
        }
        auth_params = {
            "client_id": settings.oauth_client_id,
            "redirect_uri": f"{settings.server_url}/oauth/callback",
            "response_type": "code",
            "scope": "profile platform",
            "state": mcp_state,
            "code_challenge": challenge,
            "code_challenge_method": "S256",
        }
        return f"{settings.auth_base_url}/oauth2/authorize?{urlencode(auth_params)}"

    async def handle_callback(self, request: Request) -> RedirectResponse | JSONResponse:
        """Exchange the AceDataCloud callback code and return to the MCP client."""
        mcp_state = request.query_params.get("state")
        upstream_code = request.query_params.get("code")
        if not mcp_state or not upstream_code:
            return JSONResponse({"error": "Missing state or code parameter"}, status_code=400)
        pending = self._pending_auth.pop(mcp_state, None)
        if not pending:
            return JSONResponse({"error": "Invalid or expired state"}, status_code=400)
        try:
            jwt_token = await self._exchange_code(
                upstream_code, str(pending.get("auth_code_verifier", ""))
            )
            if not jwt_token:
                return JSONResponse(
                    {"error": "Failed to exchange authorization code"}, status_code=502
                )
            api_token = await self._get_user_credential(jwt_token)
            if not api_token:
                return JSONResponse(
                    {
                        "error": (
                            "No API credential found. Create one at "
                            "https://platform.acedata.cloud/console/credentials"
                        )
                    },
                    status_code=403,
                )
            code_value = secrets.token_urlsafe(48)
            auth_code = AuthorizationCode(
                code=code_value,
                scopes=_normalize_scopes(pending.get("scopes")),
                expires_at=time.time() + 600,
                client_id=str(pending["client_id"]),
                code_challenge=pending["code_challenge"],
                redirect_uri=pending["redirect_uri"],
                redirect_uri_provided_explicitly=pending["redirect_uri_provided_explicitly"],
                resource=pending.get("resource"),
            )
            self._auth_codes[code_value] = (auth_code, api_token)
            redirect_params = {"code": code_value}
            if pending.get("state"):
                redirect_params["state"] = pending["state"]
            redirect_uri = str(pending["redirect_uri"])
            separator = "&" if "?" in redirect_uri else "?"
            return RedirectResponse(
                f"{redirect_uri}{separator}{urlencode(redirect_params)}", status_code=302
            )
        except Exception:
            logger.exception("OAuth callback failed")
            return JSONResponse({"error": "Internal server error"}, status_code=500)

    async def load_authorization_code(
        self,
        client: OAuthClientInformationFull,  # noqa: ARG002
        authorization_code: str,
    ) -> AuthorizationCode | None:
        data = self._auth_codes.get(authorization_code)
        if not data:
            return None
        if data[0].expires_at < time.time():
            self._auth_codes.pop(authorization_code, None)
            return None
        return data[0]

    async def exchange_authorization_code(
        self, client: OAuthClientInformationFull, authorization_code: AuthorizationCode
    ) -> OAuthToken:
        data = self._auth_codes.pop(authorization_code.code, None)
        if not data:
            raise ValueError("Authorization code not found or already used")
        api_token = data[1]
        client_id = client.client_id or ""
        self._revoked_tokens.discard(api_token)
        self._access_tokens[api_token] = AccessToken(
            token=api_token,
            client_id=client_id,
            scopes=_normalize_scopes(authorization_code.scopes),
            expires_at=None,
        )
        return OAuthToken(
            access_token=api_token,
            token_type="Bearer",
            scope=" ".join(_normalize_scopes(authorization_code.scopes)),
        )

    async def load_refresh_token(
        self,
        client: OAuthClientInformationFull,  # noqa: ARG002
        refresh_token: str,  # noqa: ARG002
    ) -> RefreshToken | None:
        return None

    async def exchange_refresh_token(
        self,
        client: OAuthClientInformationFull,  # noqa: ARG002
        refresh_token: RefreshToken,  # noqa: ARG002
        scopes: list[str],  # noqa: ARG002
    ) -> OAuthToken:
        from mcp.server.auth.provider import TokenError

        raise TokenError(
            error="invalid_grant",
            error_description="This server issues non-expiring tokens; refresh is not supported.",
        )

    async def load_access_token(self, token: str) -> AccessToken | None:
        if token in self._revoked_tokens:
            return None
        access_token = self._access_tokens.get(token)
        if access_token:
            set_request_api_token(token)
            return access_token
        set_request_api_token(token)
        return AccessToken(token=token, client_id="direct", scopes=[MCP_ACCESS_SCOPE])

    async def revoke_token(self, token: AccessToken | RefreshToken) -> None:
        if isinstance(token, AccessToken):
            self._access_tokens.pop(token.token, None)
            self._revoked_tokens.add(token.token)

    async def _exchange_code(self, code: str, code_verifier: str) -> str | None:
        try:
            async with httpx.AsyncClient(timeout=30) as http_client:
                response = await http_client.post(
                    f"{settings.auth_base_url}/oauth2/token",
                    data={
                        "grant_type": "authorization_code",
                        "code": code,
                        "client_id": settings.oauth_client_id,
                        "redirect_uri": f"{settings.server_url}/oauth/callback",
                        "code_verifier": code_verifier,
                    },
                )
            if response.status_code != 200:
                logger.error("OAuth token exchange failed: %s", response.text[:200])
                return None
            token = response.json().get("access_token")
            return token if isinstance(token, str) else None
        except Exception:
            logger.exception("OAuth token exchange failed")
            return None

    async def _get_user_credential(self, jwt_token: str) -> str | None:
        headers = {"Authorization": f"Bearer {jwt_token}"}
        try:
            async with httpx.AsyncClient(timeout=30) as http_client:
                credentials_url = f"{settings.platform_base_url}/api/v1/credentials/"
                response = await http_client.get(credentials_url, headers=headers)
                if response.status_code == 200:
                    data = response.json()
                    credentials = data.get("results", data) if isinstance(data, dict) else data
                    if isinstance(credentials, list):
                        for credential in credentials:
                            token = (
                                credential.get("token") if isinstance(credential, dict) else None
                            )
                            if isinstance(token, str) and token:
                                return token

                applications_url = f"{settings.platform_base_url}/api/v1/applications/"
                response = await http_client.get(
                    applications_url,
                    headers=headers,
                    params={
                        "limit": "10",
                        "ordering": "-created_at",
                        "type": "Usage",
                        "scope": "Global",
                    },
                )
                application_id: str | None = None
                if response.status_code == 200:
                    data = response.json()
                    items = (
                        data.get("items", data.get("results", [])) if isinstance(data, dict) else []
                    )
                    if isinstance(items, list) and items:
                        application_id = items[0].get("id")
                        app_credentials = items[0].get("credentials", [])
                        if isinstance(app_credentials, list) and app_credentials:
                            token = app_credentials[0].get("token")
                            if isinstance(token, str) and token:
                                return token
                if not application_id:
                    response = await http_client.post(
                        applications_url,
                        headers={**headers, "Content-Type": "application/json"},
                        json={"type": "Usage", "scope": "Global"},
                    )
                    if response.status_code not in (200, 201):
                        return None
                    application_id = response.json().get("id")
                if not application_id:
                    return None
                response = await http_client.post(
                    credentials_url,
                    headers={**headers, "Content-Type": "application/json"},
                    json={"application_id": application_id},
                )
                if response.status_code not in (200, 201):
                    return None
                token = response.json().get("token")
                return token if isinstance(token, str) and token else None
        except Exception:
            logger.exception("Credential fetch or provisioning failed")
            return None
