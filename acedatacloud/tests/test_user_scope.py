"""Account tools must scope every query to the caller's user_id (from the JWT).

Without this the management API returns the whole table to a superuser (→ OOM)
or 403s a regular user. See PlatformBackend ApplicationViewSet.get_queryset.
"""

import base64
import json

import httpx
import pytest
import respx

from core.client import get_request_user_id, set_request_api_token
from tools.read_tools import (
    acedatacloud_get_balance,
    acedatacloud_list_applications,
    acedatacloud_list_credentials,
    acedatacloud_list_orders,
)

API = "https://platform.acedata.cloud/api/v1"
USER_ID = "b87f67c1-b04f-4332-99a1-7a5e651331c6"


def _fake_jwt(user_id: str) -> str:
    payload = (
        base64.urlsafe_b64encode(json.dumps({"user_id": user_id}).encode()).rstrip(b"=").decode()
    )
    return f"hdr.{payload}.sig"


def test_get_request_user_id_decodes_jwt():
    set_request_api_token(_fake_jwt(USER_ID))
    try:
        assert get_request_user_id() == USER_ID
    finally:
        set_request_api_token(None)


def test_get_request_user_id_none_for_opaque_token():
    set_request_api_token("platform-opaque-token")
    try:
        assert get_request_user_id() is None
    finally:
        set_request_api_token(None)


@respx.mock
@pytest.mark.asyncio
async def test_list_applications_scopes_user_id():
    route = respx.get(f"{API}/applications/").mock(
        return_value=httpx.Response(200, json={"count": 0, "items": []})
    )
    set_request_api_token(_fake_jwt(USER_ID))
    try:
        await acedatacloud_list_applications()
    finally:
        set_request_api_token(None)
    assert route.calls[0].request.url.params["user_id"] == USER_ID


@respx.mock
@pytest.mark.asyncio
async def test_get_balance_scopes_user_id():
    route = respx.get(f"{API}/applications/").mock(
        return_value=httpx.Response(200, json={"count": 0, "items": []})
    )
    set_request_api_token(_fake_jwt(USER_ID))
    try:
        await acedatacloud_get_balance()
    finally:
        set_request_api_token(None)
    assert route.calls[0].request.url.params["user_id"] == USER_ID


@respx.mock
@pytest.mark.asyncio
async def test_credentials_and_orders_scope_user_id():
    cred = respx.get(f"{API}/credentials/").mock(
        return_value=httpx.Response(200, json={"count": 0, "items": []})
    )
    orders = respx.get(f"{API}/orders/").mock(
        return_value=httpx.Response(200, json={"count": 0, "items": []})
    )
    set_request_api_token(_fake_jwt(USER_ID))
    try:
        await acedatacloud_list_credentials()
        await acedatacloud_list_orders()
    finally:
        set_request_api_token(None)
    assert cred.calls[0].request.url.params["user_id"] == USER_ID
    assert orders.calls[0].request.url.params["user_id"] == USER_ID


@respx.mock
@pytest.mark.asyncio
async def test_no_user_id_param_when_opaque_token():
    route = respx.get(f"{API}/applications/").mock(
        return_value=httpx.Response(200, json={"count": 0, "items": []})
    )
    set_request_api_token("platform-opaque")
    try:
        await acedatacloud_list_applications()
    finally:
        set_request_api_token(None)
    assert "user_id" not in route.calls[0].request.url.params
