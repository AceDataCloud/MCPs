"""Site-admin and white-label tool contracts."""

import json

import httpx
import pytest
import respx

from tools.user.sites import (
    acedatacloud_check_frame_ancestor,
    acedatacloud_check_site_domain,
    acedatacloud_create_site_banner,
    acedatacloud_create_site_capability_override,
    acedatacloud_create_site_document_override,
    acedatacloud_create_site_domain,
    acedatacloud_create_site_service_override,
    acedatacloud_delete_site_banner,
    acedatacloud_delete_site_capability_override,
    acedatacloud_delete_site_document_override,
    acedatacloud_delete_site_domain,
    acedatacloud_delete_site_service_override,
    acedatacloud_get_site,
    acedatacloud_get_site_banner,
    acedatacloud_get_site_capability_override,
    acedatacloud_get_site_document_override,
    acedatacloud_get_site_domain,
    acedatacloud_get_site_service_override,
    acedatacloud_initialize_site,
    acedatacloud_list_site_banners,
    acedatacloud_list_site_capability_overrides,
    acedatacloud_list_site_document_overrides,
    acedatacloud_list_site_domains,
    acedatacloud_list_site_service_overrides,
    acedatacloud_list_sites,
    acedatacloud_set_site_menu_translation,
    acedatacloud_update_site,
    acedatacloud_update_site_banner,
    acedatacloud_update_site_capability_override,
    acedatacloud_update_site_document_override,
    acedatacloud_update_site_domain,
    acedatacloud_update_site_service_override,
    acedatacloud_verify_site_domain,
)

API = "https://platform.acedata.cloud/api/v1"
ID = "55555555-5555-5555-5555-555555555555"


@respx.mock
@pytest.mark.asyncio
async def test_site_contracts():
    cases = [
        ("/sites/", acedatacloud_list_sites, ()),
        (f"/sites/{ID}", acedatacloud_get_site, (ID,)),
        ("/site-domains/", acedatacloud_list_site_domains, ()),
        (f"/site-domains/{ID}/", acedatacloud_get_site_domain, (ID,)),
        ("/site-domains/check", acedatacloud_check_site_domain, ("example.com",)),
        (
            "/site-domains/frame-ancestors",
            acedatacloud_check_frame_ancestor,
            ("https://example.com",),
        ),
        ("/site-banners/", acedatacloud_list_site_banners, ()),
        (f"/site-banners/{ID}/", acedatacloud_get_site_banner, (ID,)),
        ("/site-capability-overrides/", acedatacloud_list_site_capability_overrides, ()),
        (f"/site-capability-overrides/{ID}/", acedatacloud_get_site_capability_override, (ID,)),
        ("/site-service-overrides/", acedatacloud_list_site_service_overrides, ()),
        (f"/site-service-overrides/{ID}/", acedatacloud_get_site_service_override, (ID,)),
        ("/site-document-overrides/", acedatacloud_list_site_document_overrides, ()),
        (f"/site-document-overrides/{ID}/", acedatacloud_get_site_document_override, (ID,)),
    ]
    for path, function, args in cases:
        route = respx.get(f"{API}{path}").mock(return_value=httpx.Response(200, json={"ok": True}))
        assert json.loads(await function(*args))["ok"] is True
        assert route.call_count == 1

    public = respx.get(f"{API}/site-banners/public/").mock(
        return_value=httpx.Response(200, json={"items": []})
    )
    await acedatacloud_list_site_banners(public=True)
    assert public.call_count == 1


@respx.mock
@pytest.mark.asyncio
async def test_site_mutation_previews_zero_calls_and_redact_auth_secret():
    results = [
        await acedatacloud_initialize_site("https://example.com"),
        await acedatacloud_update_site(ID, auth={"sms": {"secret": "sms-secret"}}),
        await acedatacloud_set_site_menu_translation(ID, "nav", "item", True, "Title"),
        await acedatacloud_create_site_domain(ID, "brand.example.com"),
        await acedatacloud_update_site_domain(ID, tags=["brand"]),
        await acedatacloud_delete_site_domain(ID),
        await acedatacloud_verify_site_domain(ID),
        await acedatacloud_create_site_banner(ID, title="Hello"),
        await acedatacloud_update_site_banner(ID, visible=False),
        await acedatacloud_delete_site_banner(ID),
        await acedatacloud_create_site_capability_override(ID, "chat"),
        await acedatacloud_update_site_capability_override(ID, display_name="Chat"),
        await acedatacloud_delete_site_capability_override(ID),
        await acedatacloud_create_site_service_override(ID, "service"),
        await acedatacloud_update_site_service_override(ID, visible=False),
        await acedatacloud_delete_site_service_override(ID),
        await acedatacloud_create_site_document_override(ID, "document"),
        await acedatacloud_update_site_document_override(ID, visible=False),
        await acedatacloud_delete_site_document_override(ID),
    ]
    assert all(json.loads(result)["status"] == "confirmation_required" for result in results)
    assert "sms-secret" not in "\n".join(results)
    assert respx.calls.call_count == 0


@respx.mock
@pytest.mark.asyncio
async def test_override_confirmed_methods_and_bodies():
    cases = [
        (
            "POST",
            "/site-capability-overrides/",
            acedatacloud_create_site_capability_override,
            (ID, "chat"),
        ),
        (
            "PATCH",
            f"/site-capability-overrides/{ID}/",
            acedatacloud_update_site_capability_override,
            (ID,),
        ),
        (
            "DELETE",
            f"/site-capability-overrides/{ID}/",
            acedatacloud_delete_site_capability_override,
            (ID,),
        ),
        (
            "POST",
            "/site-service-overrides/",
            acedatacloud_create_site_service_override,
            (ID, "service"),
        ),
        (
            "PATCH",
            f"/site-service-overrides/{ID}/",
            acedatacloud_update_site_service_override,
            (ID,),
        ),
        (
            "DELETE",
            f"/site-service-overrides/{ID}/",
            acedatacloud_delete_site_service_override,
            (ID,),
        ),
        (
            "POST",
            "/site-document-overrides/",
            acedatacloud_create_site_document_override,
            (ID, "document"),
        ),
        (
            "PATCH",
            f"/site-document-overrides/{ID}/",
            acedatacloud_update_site_document_override,
            (ID,),
        ),
        (
            "DELETE",
            f"/site-document-overrides/{ID}/",
            acedatacloud_delete_site_document_override,
            (ID,),
        ),
    ]
    for method, path, function, args in cases:
        route = respx.request(method, f"{API}{path}").mock(
            return_value=httpx.Response(200, json={"ok": True})
        )
        assert json.loads(await function(*args, confirm=True))["ok"] is True
        assert route.call_count == 1
