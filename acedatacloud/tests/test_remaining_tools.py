"""Remaining ordinary-user self-service tool contracts."""

import json

import httpx
import pytest
import respx

from core.client import set_request_api_token
from tools.user.community import (
    acedatacloud_cancel_access_request,
    acedatacloud_confirm_wallet_challenge,
    acedatacloud_create_access_request,
    acedatacloud_create_wallet_challenge,
    acedatacloud_get_access_request,
    acedatacloud_get_distribution_rank,
    acedatacloud_get_distribution_trend,
    acedatacloud_get_platform_distribution_rank,
    acedatacloud_get_survey,
    acedatacloud_get_survey_response,
    acedatacloud_get_wallet_summary,
    acedatacloud_initialize_distribution,
    acedatacloud_list_access_requests,
    acedatacloud_list_coin_info,
    acedatacloud_list_distribution_levels,
    acedatacloud_list_surveys,
    acedatacloud_refresh_coin_info,
    acedatacloud_submit_survey,
)
from tools.user.preferences import (
    acedatacloud_disable_translation,
    acedatacloud_enable_translation,
    acedatacloud_get_translation_capabilities,
    acedatacloud_list_email_preferences,
    acedatacloud_report_content,
    acedatacloud_update_email_preference,
)
from tools.user.x402 import (
    acedatacloud_confirm_x402_authorization,
    acedatacloud_confirm_x402_revocation,
    acedatacloud_disable_x402_authorization,
    acedatacloud_enable_x402_authorization,
    acedatacloud_get_x402_authorization,
    acedatacloud_setup_x402_authorization,
)

API = "https://platform.acedata.cloud/api/v1"
ID = "44444444-4444-4444-4444-444444444444"


@respx.mock
@pytest.mark.asyncio
async def test_remaining_contracts():
    subject = respx.get(f"{API}/platform-tokens/me/").mock(
        return_value=httpx.Response(200, json={"id": "user-1"})
    )
    cases = [
        ("/distribution-levels/", acedatacloud_list_distribution_levels, ()),
        ("/distribution-histories/rank/", acedatacloud_get_distribution_rank, ()),
        ("/distribution-histories/platform-rank/", acedatacloud_get_platform_distribution_rank, ()),
        ("/distribution-histories/trend/", acedatacloud_get_distribution_trend, ()),
        ("/coin-infos/", acedatacloud_list_coin_info, ()),
        ("/coin-wallet/summary/", acedatacloud_get_wallet_summary, ()),
        ("/access-requests/", acedatacloud_list_access_requests, ()),
        (f"/access-requests/{ID}", acedatacloud_get_access_request, (ID,)),
        ("/surveys/templates/", acedatacloud_list_surveys, ()),
        ("/surveys/templates/onboarding/", acedatacloud_get_survey, ("onboarding",)),
        ("/surveys/responses/me/", acedatacloud_get_survey_response, ("onboarding",)),
        ("/translations/capabilities/", acedatacloud_get_translation_capabilities, ()),
        ("/email-marketing/preferences/", acedatacloud_list_email_preferences, ()),
        ("/x402/payment-authorization/", acedatacloud_get_x402_authorization, ()),
    ]
    set_request_api_token("platform-token")
    try:
        for path, function, args in cases:
            route = respx.get(f"{API}{path}").mock(
                return_value=httpx.Response(200, json={"ok": True})
            )
            result = json.loads(await function(*args))
            assert result["ok"] is True
            assert route.call_count == 1
    finally:
        set_request_api_token(None)
    assert subject.call_count == 1


@respx.mock
@pytest.mark.asyncio
async def test_remaining_mutation_previews_zero_calls_and_redact_signatures():
    results = [
        await acedatacloud_initialize_distribution(),
        await acedatacloud_refresh_coin_info(ID),
        await acedatacloud_create_wallet_challenge("bind", "wallet-address"),
        await acedatacloud_confirm_wallet_challenge(ID, "wallet-signature"),
        await acedatacloud_create_access_request(service="private-service"),
        await acedatacloud_cancel_access_request(ID),
        await acedatacloud_submit_survey("onboarding", {"answer": True}),
        await acedatacloud_enable_translation("site", ID, "title", "Source"),
        await acedatacloud_disable_translation("site", ID, "title"),
        await acedatacloud_update_email_preference("newsletter", "Unsubscribed"),
        await acedatacloud_report_content("chat", ID, "unsafe"),
        await acedatacloud_setup_x402_authorization("wallet", 100, 2_000_000_000),
        await acedatacloud_confirm_x402_authorization(
            "setup-secret", "delegation", "delegation-tx", "setup-tx"
        ),
        await acedatacloud_disable_x402_authorization(),
        await acedatacloud_enable_x402_authorization(),
        await acedatacloud_confirm_x402_revocation("revoked-tx"),
    ]
    assert all(json.loads(item)["status"] == "confirmation_required" for item in results)
    combined = "\n".join(results)
    for secret in ("wallet-signature", "setup-secret", "delegation-tx", "setup-tx", "revoked-tx"):
        assert secret not in combined
    assert respx.calls.call_count == 0


@respx.mock
@pytest.mark.asyncio
async def test_remaining_confirmed_mutation_routes():
    cases = [
        ("POST", "/distribution-statuses/initialize/", acedatacloud_initialize_distribution, ()),
        ("POST", f"/coin-infos/{ID}/update-balance/", acedatacloud_refresh_coin_info, (ID,)),
        (
            "POST",
            "/coin-wallet/challenge/",
            acedatacloud_create_wallet_challenge,
            ("bind", "wallet"),
        ),
        ("POST", "/coin-wallet/confirm/", acedatacloud_confirm_wallet_challenge, (ID, "sig")),
        ("POST", "/access-requests/", acedatacloud_create_access_request, ("service",)),
        ("DELETE", f"/access-requests/{ID}", acedatacloud_cancel_access_request, (ID,)),
        ("POST", "/surveys/responses/", acedatacloud_submit_survey, ("onboarding", {"a": 1})),
        (
            "POST",
            "/translations/enable",
            acedatacloud_enable_translation,
            ("site", ID, "title", "source"),
        ),
        ("POST", "/translations/disable", acedatacloud_disable_translation, ("site", ID, "title")),
        (
            "PUT",
            "/email-marketing/preferences/newsletter/",
            acedatacloud_update_email_preference,
            ("newsletter", "Subscribed"),
        ),
        ("POST", "/content-reports/", acedatacloud_report_content, ("chat", ID, "unsafe")),
        (
            "POST",
            "/x402/payment-authorization/setup/",
            acedatacloud_setup_x402_authorization,
            ("wallet", 100, 2_000_000_000),
        ),
        (
            "POST",
            "/x402/payment-authorization/confirm/",
            acedatacloud_confirm_x402_authorization,
            ("token", "delegation", "tx"),
        ),
        (
            "POST",
            "/x402/payment-authorization/disable/",
            acedatacloud_disable_x402_authorization,
            (),
        ),
        ("POST", "/x402/payment-authorization/enable/", acedatacloud_enable_x402_authorization, ()),
        (
            "POST",
            "/x402/payment-authorization/revoke-confirm/",
            acedatacloud_confirm_x402_revocation,
            ("tx",),
        ),
    ]
    for method, path, function, args in cases:
        route = respx.request(method, f"{API}{path}").mock(
            return_value=httpx.Response(200, json={"ok": True})
        )
        result = json.loads(await function(*args, confirm=True))
        assert result["ok"] is True
        assert route.call_count == 1


@respx.mock
@pytest.mark.asyncio
async def test_x402_setup_discloses_only_setup_token():
    respx.post(f"{API}/x402/payment-authorization/setup/").mock(
        return_value=httpx.Response(
            200,
            json={"setup_token": "once", "nested": {"setup_token": "masked"}},
        )
    )
    result = json.loads(
        await acedatacloud_setup_x402_authorization("wallet", 100, 2_000_000_000, confirm=True)
    )
    assert result["setup_token"] == "once"
    assert result["nested"]["setup_token"] != "masked"
