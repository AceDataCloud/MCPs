"""Unit tests for the async HTTP client."""

import httpx
import pytest
import respx

from core.client import PlatformClient
from core.exceptions import PlatformAPIError, PlatformAuthError

BASE = "https://api.test.com"
API = f"{BASE}/api/v1"


@pytest.fixture
def client():
    return PlatformClient(api_token="test-token", base_url=BASE)


def test_init_strips_trailing_slash():
    c = PlatformClient(api_token="t", base_url="https://x.com/")
    assert c.base_url == "https://x.com"


def test_get_headers(client):
    headers = client._get_headers()
    assert headers["authorization"] == "Bearer test-token"
    assert headers["accept"] == "application/json"


def test_get_headers_no_token_raises():
    c = PlatformClient(api_token="", base_url=BASE)
    with pytest.raises(PlatformAuthError, match="not configured"):
        c._get_headers()


@respx.mock
@pytest.mark.asyncio
async def test_get_success(client):
    respx.get(f"{API}/services/").mock(
        return_value=httpx.Response(200, json={"count": 0, "items": []})
    )
    result = await client.get("/services/", {"limit": 10})
    assert result == {"count": 0, "items": []}


@respx.mock
@pytest.mark.asyncio
async def test_post_success(client):
    respx.post(f"{API}/credentials/").mock(
        return_value=httpx.Response(201, json={"id": "c1", "token": "secret"})
    )
    result = await client.post("/credentials/", {"application_id": "a1"})
    assert result["id"] == "c1"


@respx.mock
@pytest.mark.asyncio
async def test_delete_204_returns_none(client):
    respx.delete(f"{API}/credentials/c1").mock(return_value=httpx.Response(204))
    result = await client.delete("/credentials/c1")
    assert result is None


@respx.mock
@pytest.mark.asyncio
async def test_401_raises_auth_error(client):
    respx.get(f"{API}/applications/").mock(
        return_value=httpx.Response(401, json={"error": {"code": "x", "message": "bad token"}})
    )
    with pytest.raises(PlatformAuthError, match="bad token"):
        await client.get("/applications/")


@respx.mock
@pytest.mark.asyncio
async def test_400_raises_api_error(client):
    respx.post(f"{API}/orders/").mock(
        return_value=httpx.Response(400, json={"detail": "package_id is required"})
    )
    with pytest.raises(PlatformAPIError, match="package_id is required"):
        await client.post("/orders/", {})
