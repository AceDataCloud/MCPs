"""Orders, invoices, auto-recharge, and usage tool contracts."""

import json

import httpx
import pytest
import respx

from core.client import set_request_api_token
from tools.user.auto_recharge import (
    acedatacloud_confirm_auto_recharge_setup,
    acedatacloud_create_auto_recharge,
    acedatacloud_delete_auto_recharge,
    acedatacloud_disable_auto_recharge,
    acedatacloud_get_auto_recharge,
    acedatacloud_list_auto_recharges,
    acedatacloud_quote_auto_recharge,
    acedatacloud_setup_auto_recharge,
    acedatacloud_update_auto_recharge,
)
from tools.user.invoices import (
    acedatacloud_apply_invoice,
    acedatacloud_cancel_invoice,
    acedatacloud_get_invoice,
    acedatacloud_get_invoice_download,
    acedatacloud_get_order_invoice,
    acedatacloud_list_billing_profiles,
    acedatacloud_list_invoices,
    acedatacloud_preview_invoice,
)
from tools.user.orders import (
    acedatacloud_create_order,
    acedatacloud_export_orders,
    acedatacloud_get_order,
    acedatacloud_get_order_summary,
    acedatacloud_pay_order,
    acedatacloud_refresh_order,
    acedatacloud_verify_apple_order,
)
from tools.user.usage import (
    acedatacloud_export_usage,
    acedatacloud_get_proxy_usage,
    acedatacloud_get_usage,
    acedatacloud_list_proxy_usage,
    acedatacloud_list_usage_status_codes,
)

API = "https://platform.acedata.cloud/api/v1"
ID = "33333333-3333-3333-3333-333333333333"


@respx.mock
@pytest.mark.asyncio
async def test_billing_read_routes():
    subject = respx.get(f"{API}/platform-tokens/me/").mock(
        return_value=httpx.Response(200, json={"id": "user-1"})
    )
    set_request_api_token("platform-token")
    routes = [
        ("GET", f"/orders/{ID}", acedatacloud_get_order, (ID,)),
        ("GET", "/orders/summary/", acedatacloud_get_order_summary, ()),
        ("GET", "/billing-profiles/", acedatacloud_list_billing_profiles, ()),
        ("GET", "/invoices/", acedatacloud_list_invoices, ()),
        ("GET", f"/invoices/{ID}/", acedatacloud_get_invoice, (ID,)),
        ("GET", f"/orders/{ID}/invoice/", acedatacloud_get_order_invoice, (ID,)),
        ("GET", f"/auto-recharge-configs/{ID}", acedatacloud_get_auto_recharge, (ID,)),
        ("GET", f"/usage/apis/{ID}", acedatacloud_get_usage, (ID,)),
        ("GET", "/usage/apis/status-codes/", acedatacloud_list_usage_status_codes, ()),
        ("GET", f"/usage/proxies/{ID}", acedatacloud_get_proxy_usage, (ID,)),
    ]
    try:
        for method, path, function, args in routes:
            route = respx.request(method, f"{API}{path}").mock(
                return_value=httpx.Response(200, json={"id": ID})
            )
            result = json.loads(await function(*args))
            assert result["id"] == ID
            assert route.call_count == 1
    finally:
        set_request_api_token(None)
    assert subject.call_count == 1

    auto_list = respx.get(f"{API}/auto-recharge-configs/").mock(
        return_value=httpx.Response(200, json={"items": []})
    )
    proxy_list = respx.get(f"{API}/usage/proxies/").mock(
        return_value=httpx.Response(200, json={"items": []})
    )
    set_request_api_token("platform-token")
    try:
        await acedatacloud_list_auto_recharges()
        await acedatacloud_list_proxy_usage()
    finally:
        set_request_api_token(None)
    assert auto_list.calls[0].request.url.params["user_id"] == "user-1"
    assert proxy_list.calls[0].request.url.params["user_id"] == "user-1"


@pytest.mark.asyncio
async def test_order_modes_validate_before_http():
    both = json.loads(
        await acedatacloud_create_order(
            application_id="a", package_id="p", application_ids=["a"], package_ids=["p"]
        )
    )
    mismatch = json.loads(
        await acedatacloud_create_order(application_ids=["a", "b"], package_ids=["p"])
    )
    assert both["error"] == "validation_error"
    assert mismatch["error"] == "validation_error"


@respx.mock
@pytest.mark.asyncio
async def test_billing_mutation_previews_zero_calls():
    results = [
        await acedatacloud_create_order(application_id="a", package_id="p"),
        await acedatacloud_pay_order(ID),
        await acedatacloud_refresh_order(ID),
        await acedatacloud_verify_apple_order(ID, "transaction-secret"),
        await acedatacloud_apply_invoice("china", "profile", [ID]),
        await acedatacloud_cancel_invoice(ID),
        await acedatacloud_create_auto_recharge("a", "p"),
        await acedatacloud_update_auto_recharge(ID, package_id="p"),
        await acedatacloud_delete_auto_recharge(ID),
        await acedatacloud_setup_auto_recharge(ID),
        await acedatacloud_confirm_auto_recharge_setup(ID, "setup-secret"),
        await acedatacloud_disable_auto_recharge(ID),
    ]
    assert all(json.loads(result)["status"] == "confirmation_required" for result in results)
    assert respx.calls.call_count == 0
    assert "transaction-secret" not in results[3]
    assert "setup-secret" not in results[10]


@respx.mock
@pytest.mark.asyncio
async def test_invoice_preview_route():
    route = respx.post(f"{API}/invoices/preview/").mock(
        return_value=httpx.Response(200, json={"amount": "10.00", "currency": "USD"})
    )
    result = json.loads(await acedatacloud_preview_invoice([ID]))
    assert result["currency"] == "USD"
    assert json.loads(route.calls[0].request.content) == {"order_ids": [ID]}


@respx.mock
@pytest.mark.asyncio
async def test_auto_recharge_quote_route():
    route = respx.post(f"{API}/auto-recharge-configs/quote/").mock(
        return_value=httpx.Response(200, json={"quotes": []})
    )
    await acedatacloud_quote_auto_recharge("app", ["p1", "p2"])
    assert json.loads(route.calls[0].request.content) == {
        "application_id": "app",
        "package_ids": ["p1", "p2"],
    }


@respx.mock
@pytest.mark.asyncio
async def test_invoice_download_json_url():
    route = respx.get(f"{API}/invoices/{ID}/download/").mock(
        return_value=httpx.Response(200, json={"url": "https://signed.example/invoice"})
    )
    result = json.loads(await acedatacloud_get_invoice_download(ID))
    assert result["url"] == "https://signed.example/invoice"
    assert route.calls[0].request.url.params["response"] == "json"


@respx.mock
@pytest.mark.asyncio
async def test_setup_exact_secret_disclosure():
    respx.post(f"{API}/auto-recharge-configs/{ID}/setup/").mock(
        return_value=httpx.Response(
            200,
            json={
                "id": "seti_1",
                "client_secret": "seti-secret",
                "nested": {"client_secret": "must-mask"},
            },
        )
    )
    result = json.loads(await acedatacloud_setup_auto_recharge(ID, confirm=True))
    assert result["id"] == "seti_1"
    assert result["client_secret"] == "seti-secret"
    assert result["nested"]["client_secret"] != "must-mask"


@respx.mock
@pytest.mark.asyncio
async def test_bounded_exports():
    orders = respx.get(f"{API}/orders/export/").mock(
        return_value=httpx.Response(
            200, content=b"Order ID\n1\n", headers={"content-type": "text/csv"}
        )
    )
    usage = respx.get(f"{API}/usage/apis/export/").mock(
        return_value=httpx.Response(
            200, content=b"Usage ID\n1\n", headers={"content-type": "text/csv"}
        )
    )
    # Subject lookup for order export only.
    respx.get(f"{API}/platform-tokens/me/").mock(
        return_value=httpx.Response(200, json={"id": "user-1"})
    )
    set_request_api_token("platform-token")
    try:
        order_result = json.loads(await acedatacloud_export_orders(max_bytes=1024))
        usage_result = json.loads(await acedatacloud_export_usage(max_bytes=1024))
    finally:
        set_request_api_token(None)
    assert order_result["size_bytes"] > 0
    assert usage_result["size_bytes"] > 0
    assert orders.calls[0].request.url.params["user_id"] == "user-1"
    assert usage.call_count == 1
