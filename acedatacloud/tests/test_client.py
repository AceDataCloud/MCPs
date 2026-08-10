"""Unit tests for the async HTTP client."""

import httpx
import pytest
import respx

from core.client import PlatformClient
from core.exceptions import PlatformAPIError, PlatformAuthError, PlatformTimeoutError

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
async def test_patch_and_put_success(client):
    patch = respx.patch(f"{API}/credentials/c1").mock(
        return_value=httpx.Response(200, json={"id": "c1", "name": "new"})
    )
    put = respx.put(f"{API}/preferences/topic").mock(
        return_value=httpx.Response(200, json={"state": "unsubscribed"})
    )
    assert (await client.patch("/credentials/c1", {"name": "new"}))["name"] == "new"
    assert (await client.put("/preferences/topic", {"state": "unsubscribed"}))[
        "state"
    ] == "unsubscribed"
    assert patch.calls[0].request.method == "PATCH"
    assert put.calls[0].request.method == "PUT"


@respx.mock
@pytest.mark.asyncio
async def test_repeated_query_values(client):
    route = respx.get(f"{API}/applications/").mock(
        return_value=httpx.Response(200, json={"items": []})
    )
    await client.get(
        "/applications/",
        {"service_id": ["svc-1", "svc-2"], "scope": ["Individual", "Global"]},
    )
    params = route.calls[0].request.url.params
    assert params.get_list("service_id") == ["svc-1", "svc-2"]
    assert params.get_list("scope") == ["Individual", "Global"]


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


@respx.mock
@pytest.mark.asyncio
async def test_403_raises_permission_denied(client):
    respx.get(f"{API}/admin/").mock(return_value=httpx.Response(403, json={"detail": "forbidden"}))
    with pytest.raises(PlatformAPIError) as caught:
        await client.get("/admin/")
    assert caught.value.code == "permission_denied"
    assert caught.value.status_code == 403


@respx.mock
@pytest.mark.asyncio
async def test_timeout_raises_timeout_error(client):
    respx.get(f"{API}/slow/").mock(side_effect=httpx.ReadTimeout("slow"))
    with pytest.raises(PlatformTimeoutError):
        await client.get("/slow/")


@respx.mock
@pytest.mark.asyncio
async def test_bounded_text_response(client):
    route = respx.get(f"{API}/usage/apis/export/").mock(
        return_value=httpx.Response(
            200,
            content=b"id,status\n1,200\n",
            headers={
                "content-type": "text/csv; charset=utf-8",
                "content-disposition": 'attachment; filename="usage.csv"',
            },
        )
    )
    result = await client.request_text("/usage/apis/export/", max_bytes=100)
    assert result.filename == "usage.csv"
    assert result.content_type == "text/csv"
    assert result.size_bytes == len(result.content.encode())
    assert route.call_count == 1


@respx.mock
@pytest.mark.asyncio
async def test_text_response_size_is_bounded(client):
    respx.get(f"{API}/usage/apis/export/").mock(
        return_value=httpx.Response(
            200, content=b"0123456789", headers={"content-type": "text/csv"}
        )
    )
    with pytest.raises(PlatformAPIError) as caught:
        await client.request_text("/usage/apis/export/", max_bytes=5)
    assert caught.value.code == "response_too_large"
