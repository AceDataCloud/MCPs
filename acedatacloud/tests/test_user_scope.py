"""Account tools must scope every query to the platform-token subject."""

import asyncio

import httpx
import pytest
import respx

from core.client import get_request_subject, get_request_user_id, set_request_api_token
from tools.read_tools import (
    acedatacloud_get_balance,
    acedatacloud_list_applications,
    acedatacloud_list_credentials,
    acedatacloud_list_distributions,
    acedatacloud_list_orders,
    acedatacloud_list_platform_tokens,
    acedatacloud_list_usage,
    acedatacloud_usage_summary,
)

API = "https://platform.acedata.cloud/api/v1"
USER_ID = "b87f67c1-b04f-4332-99a1-7a5e651331c6"


def _mock_subject(user_id: str = USER_ID):
    return respx.get(f"{API}/platform-tokens/me/").mock(
        return_value=httpx.Response(200, json={"id": user_id, "username": "subject"})
    )


@respx.mock
@pytest.mark.asyncio
async def test_get_request_user_id_resolves_opaque_token_subject():
    subject = _mock_subject()
    set_request_api_token("platform-opaque-token")
    try:
        assert await get_request_user_id() == USER_ID
        assert await get_request_subject() == {"id": USER_ID, "username": "subject"}
    finally:
        set_request_api_token(None)
    assert subject.call_count == 1


@respx.mock
@pytest.mark.asyncio
async def test_subject_cache_is_isolated_by_request_context():
    route = respx.get(f"{API}/platform-tokens/me/").mock(
        side_effect=[
            httpx.Response(200, json={"id": "user-a"}),
            httpx.Response(200, json={"id": "user-b"}),
        ]
    )

    async def resolve(token: str) -> str:
        set_request_api_token(token)
        try:
            return await get_request_user_id()
        finally:
            set_request_api_token(None)

    assert await asyncio.gather(resolve("platform-a"), resolve("platform-b")) == [
        "user-a",
        "user-b",
    ]
    assert route.call_count == 2


@respx.mock
@pytest.mark.asyncio
async def test_list_applications_scopes_user_id():
    _mock_subject()
    route = respx.get(f"{API}/applications/").mock(
        return_value=httpx.Response(200, json={"count": 0, "items": []})
    )
    set_request_api_token("platform-request-token")
    try:
        await acedatacloud_list_applications()
    finally:
        set_request_api_token(None)
    assert route.calls[0].request.url.params["user_id"] == USER_ID


@respx.mock
@pytest.mark.asyncio
async def test_get_balance_scopes_user_id():
    _mock_subject()
    route = respx.get(f"{API}/applications/").mock(
        return_value=httpx.Response(200, json={"count": 0, "items": []})
    )
    set_request_api_token("platform-request-token")
    try:
        await acedatacloud_get_balance()
    finally:
        set_request_api_token(None)
    assert route.calls[0].request.url.params["user_id"] == USER_ID


@respx.mock
@pytest.mark.asyncio
async def test_credentials_and_orders_scope_user_id_with_one_subject_lookup():
    subject = _mock_subject()
    credentials = respx.get(f"{API}/credentials/").mock(
        return_value=httpx.Response(200, json={"count": 0, "items": []})
    )
    orders = respx.get(f"{API}/orders/").mock(
        return_value=httpx.Response(200, json={"count": 0, "items": []})
    )
    set_request_api_token("platform-request-token")
    try:
        await acedatacloud_list_credentials()
        await acedatacloud_list_orders()
    finally:
        set_request_api_token(None)
    assert credentials.calls[0].request.url.params["user_id"] == USER_ID
    assert orders.calls[0].request.url.params["user_id"] == USER_ID
    assert subject.call_count == 1


@respx.mock
@pytest.mark.asyncio
async def test_registered_account_tools_are_subject_scoped():
    subject = _mock_subject()
    routes = {
        "/usage/apis/": respx.get(f"{API}/usage/apis/").mock(
            return_value=httpx.Response(200, json={"count": 0, "items": []})
        ),
        "/usage/apis/aggregate/": respx.get(f"{API}/usage/apis/aggregate/").mock(
            return_value=httpx.Response(200, json={"total": 0, "items": [], "apis": {}})
        ),
        "/platform-tokens/": respx.get(f"{API}/platform-tokens/").mock(
            return_value=httpx.Response(200, json={"count": 0, "items": []})
        ),
        "/distribution-statuses/": respx.get(f"{API}/distribution-statuses/").mock(
            return_value=httpx.Response(200, json={"count": 0, "items": []})
        ),
        "/distribution-histories/": respx.get(f"{API}/distribution-histories/").mock(
            return_value=httpx.Response(200, json={"count": 0, "items": []})
        ),
    }
    set_request_api_token("platform-request-token")
    try:
        await acedatacloud_list_usage()
        await acedatacloud_usage_summary()
        await acedatacloud_list_platform_tokens()
        await acedatacloud_list_distributions()
    finally:
        set_request_api_token(None)

    assert subject.call_count == 1
    for route in routes.values():
        assert route.calls[0].request.url.params["user_id"] == USER_ID


@respx.mock
@pytest.mark.asyncio
async def test_missing_subject_fails_closed_without_account_query():
    _mock_subject(user_id="")
    applications = respx.get(f"{API}/applications/").mock(
        return_value=httpx.Response(200, json={"count": 0, "items": []})
    )
    set_request_api_token("platform-opaque-token")
    try:
        result = await acedatacloud_list_applications()
    finally:
        set_request_api_token(None)
    assert "auth_error" in result
    assert applications.call_count == 0
