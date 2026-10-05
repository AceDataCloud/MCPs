"""Exercise the actual platform blog routes, payloads and write confirmation."""

import json
from uuid import UUID

import httpx
import respx

from core.client import set_request_api_token
from tools.blog_tools import (
    acedatacloud_approve_blog_post,
    acedatacloud_create_blog_draft,
    acedatacloud_delete_blog_post,
    acedatacloud_get_blog_draft,
    acedatacloud_get_blog_post,
    acedatacloud_list_blog_drafts,
    acedatacloud_list_blog_posts,
    acedatacloud_publish_blog_post,
    acedatacloud_unpublish_blog_post,
    acedatacloud_update_blog_post,
    acedatacloud_withdraw_blog_approval,
)

API = "https://platform.acedata.cloud/api/v1"
BLOG_ID = UUID("eaa18d3a-6ed9-40dd-8e73-5d6c67e00cc0")
DETAIL = f"{API}/blogs/admin/{BLOG_ID}/"


@respx.mock
async def test_public_blog_reads_do_not_forward_credentials():
    set_request_api_token("platform-private")
    listing = respx.get(f"{API}/blogs/").mock(return_value=httpx.Response(200, json={"items": []}))
    detail = respx.get(f"{API}/blogs/product-launch/").mock(
        return_value=httpx.Response(200, json={"content": "# 产品"})
    )
    await acedatacloud_list_blog_posts(category="product", lang="zh-cn", limit=5, offset=2)
    assert (
        json.loads(await acedatacloud_get_blog_post("product-launch", lang="en"))["content"]
        == "# 产品"
    )
    assert dict(listing.calls.last.request.url.params) == {
        "category": "product",
        "lang": "zh-cn",
        "limit": "5",
        "offset": "2",
    }
    for route in (listing, detail):
        assert "authorization" not in route.calls.last.request.headers


@respx.mock
async def test_editorial_reads_and_filters():
    listing = respx.get(f"{API}/blogs/admin/").mock(
        return_value=httpx.Response(200, json={"items": []})
    )
    detail = respx.get(DETAIL).mock(return_value=httpx.Response(200, json={"id": str(BLOG_ID)}))
    await acedatacloud_list_blog_drafts(query="launch", published=False)
    assert listing.calls.last.request.url.params["published"] == "false"
    assert listing.calls.last.request.url.params["q"] == "launch"
    assert "authorization" in listing.calls.last.request.headers
    await acedatacloud_list_blog_drafts(published=None)
    assert "published" not in listing.calls.last.request.url.params
    await acedatacloud_get_blog_draft(BLOG_ID)
    assert detail.called


@respx.mock
async def test_all_blog_mutations_preview_without_http():
    previews = [
        await acedatacloud_create_blog_draft("launch", "标题", "摘要", "# 正文"),
        await acedatacloud_update_blog_post(BLOG_ID, title="Changed"),
        await acedatacloud_publish_blog_post(BLOG_ID),
        await acedatacloud_approve_blog_post(BLOG_ID, expected_version=3),
        await acedatacloud_withdraw_blog_approval(BLOG_ID),
        await acedatacloud_unpublish_blog_post(BLOG_ID),
        await acedatacloud_delete_blog_post(BLOG_ID),
    ]
    assert all(json.loads(result)["status"] == "confirmation_required" for result in previews)
    assert not respx.calls


@respx.mock
async def test_create_draft_and_preserve_markdown():
    route = respx.post(f"{API}/blogs/admin/").mock(
        return_value=httpx.Response(201, json={"id": str(BLOG_ID), "published": False})
    )
    markdown = "# 新功能\n\n**博客**支持 Markdown。"
    await acedatacloud_create_blog_draft(
        "launch", "新功能", "功能介绍", markdown, category="product", tags=["MCP"], confirm=True
    )
    body = json.loads(route.calls.last.request.content)
    assert body["content"] == markdown
    assert body["published"] is False
    assert body["source_lang"] == "zh-cn"
    assert body["tags"] == ["MCP"]


@respx.mock
async def test_update_only_sends_supplied_fields():
    route = respx.patch(DETAIL).mock(return_value=httpx.Response(200, json={"id": str(BLOG_ID)}))
    await acedatacloud_update_blog_post(
        BLOG_ID, title="Changed", cover_url="", tags=[], confirm=True
    )
    assert json.loads(route.calls.last.request.content) == {
        "title": "Changed",
        "cover_url": "",
        "tags": [],
    }


@respx.mock
async def test_publication_actions_use_backend_permissions():
    route = respx.patch(DETAIL).mock(return_value=httpx.Response(200, json={"published": True}))
    await acedatacloud_publish_blog_post(BLOG_ID, confirm=True)
    assert json.loads(route.calls.last.request.content) == {"published": True}
    await acedatacloud_publish_blog_post(
        BLOG_ID, publish_at="2026-10-10T09:00:00+08:00", confirm=True
    )
    assert json.loads(route.calls.last.request.content)["publish_at"] == "2026-10-10T09:00:00+08:00"
    await acedatacloud_unpublish_blog_post(BLOG_ID, confirm=True)
    assert json.loads(route.calls.last.request.content) == {"published": False}
    route.mock(
        return_value=httpx.Response(
            403, json={"detail": "Missing required permission: blog:publish"}
        )
    )
    result = json.loads(await acedatacloud_publish_blog_post(BLOG_ID, confirm=True))
    assert result["error"] == "permission_denied"
    assert "blog:publish" in result["message"]


@respx.mock
async def test_approve_and_withdraw_blog_review():
    approval = f"{DETAIL}approval/"
    approve_route = respx.post(approval).mock(
        return_value=httpx.Response(200, json={"approved_by_id": "peer", "review_version": 3})
    )
    withdraw_route = respx.delete(approval).mock(
        return_value=httpx.Response(200, json={"approved_by_id": None})
    )
    result = json.loads(
        await acedatacloud_approve_blog_post(BLOG_ID, expected_version=3, confirm=True)
    )
    assert result["approved_by_id"] == "peer"
    assert json.loads(approve_route.calls.last.request.content) == {"expected_version": 3}
    assert (
        json.loads(await acedatacloud_withdraw_blog_approval(BLOG_ID, confirm=True))[
            "approved_by_id"
        ]
        is None
    )
    assert withdraw_route.called


@respx.mock
async def test_delete_blog_post():
    route = respx.delete(DETAIL).mock(return_value=httpx.Response(204))
    assert json.loads(await acedatacloud_delete_blog_post(BLOG_ID, confirm=True)) is None
    assert route.called
