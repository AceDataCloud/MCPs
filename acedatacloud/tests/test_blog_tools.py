"""Exercise the actual platform blog routes, payloads and write confirmation."""

import json
from uuid import UUID

import httpx
import pytest
import respx
from mcp.server.fastmcp.exceptions import ToolError

from core.client import set_request_api_token
from core.server import mcp
from tools.blog_tools import (
    acedatacloud_add_blog_comment,
    acedatacloud_approve_blog_post,
    acedatacloud_create_blog_draft,
    acedatacloud_delete_blog_post,
    acedatacloud_get_blog_draft,
    acedatacloud_get_blog_post,
    acedatacloud_list_blog_comments,
    acedatacloud_list_blog_drafts,
    acedatacloud_list_blog_posts,
    acedatacloud_publish_blog_post,
    acedatacloud_reject_blog_post,
    acedatacloud_reply_blog_comment,
    acedatacloud_resolve_blog_comment,
    acedatacloud_submit_blog_post,
    acedatacloud_unpublish_blog_post,
    acedatacloud_update_blog_post,
    acedatacloud_withdraw_blog_approval,
    acedatacloud_withdraw_blog_submission,
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
    await acedatacloud_list_blog_posts(category="product-updates", lang="zh-cn", limit=5, offset=2)
    assert (
        json.loads(await acedatacloud_get_blog_post("product-launch", lang="en"))["content"]
        == "# 产品"
    )
    assert dict(listing.calls.last.request.url.params) == {
        "category": "product-updates",
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
async def test_review_comments():
    comment_id = UUID("1c7e95a7-04c0-47b6-9620-51b108bdfbb2")
    base = f"{DETAIL}comments/"
    listing = respx.get(base).mock(
        return_value=httpx.Response(200, json=[{"id": str(comment_id), "replies": []}])
    )
    create = respx.post(base).mock(return_value=httpx.Response(201, json={"id": str(comment_id)}))
    reply = respx.post(f"{base}{comment_id}/replies/").mock(
        return_value=httpx.Response(201, json={"body": "Fixed"})
    )
    resolution = respx.patch(f"{base}{comment_id}/").mock(
        return_value=httpx.Response(200, json={"resolved_at": "now"})
    )
    assert json.loads(await acedatacloud_list_blog_comments(BLOG_ID))[0]["id"] == str(comment_id)
    assert listing.called
    preview = await acedatacloud_add_blog_comment(
        BLOG_ID, 4, "Clarify", field="content", start_offset=1, end_offset=3, quote="😀"
    )
    assert json.loads(preview)["status"] == "confirmation_required"
    assert not create.called
    await acedatacloud_add_blog_comment(
        BLOG_ID,
        4,
        "Clarify",
        field="content",
        start_offset=1,
        end_offset=3,
        quote="😀",
        confirm=True,
    )
    assert json.loads(create.calls.last.request.content) == {
        "expected_version": 4,
        "body": "Clarify",
        "field": "content",
        "start_offset": 1,
        "end_offset": 3,
        "quote": "😀",
    }
    await acedatacloud_reply_blog_comment(BLOG_ID, comment_id, "Fixed", confirm=True)
    assert json.loads(reply.calls.last.request.content) == {"body": "Fixed"}
    await acedatacloud_resolve_blog_comment(BLOG_ID, comment_id, True, confirm=True)
    assert json.loads(resolution.calls.last.request.content) == {"resolved": True}


@respx.mock
async def test_all_blog_mutations_preview_without_http():
    previews = [
        await acedatacloud_create_blog_draft("launch", "标题", "摘要", "# 正文"),
        await acedatacloud_update_blog_post(BLOG_ID, title="Changed"),
        await acedatacloud_publish_blog_post(BLOG_ID),
        await acedatacloud_approve_blog_post(BLOG_ID, expected_version=3),
        await acedatacloud_submit_blog_post(BLOG_ID, expected_version=3),
        await acedatacloud_reject_blog_post(BLOG_ID, expected_version=3, comment="Needs sources"),
        await acedatacloud_withdraw_blog_submission(BLOG_ID, expected_version=3),
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
        "launch",
        "新功能",
        "功能介绍",
        markdown,
        category="product-updates",
        tags=["MCP"],
        confirm=True,
    )
    body = json.loads(route.calls.last.request.content)
    assert body["content"] == markdown
    assert body["published"] is False
    assert body["source_lang"] == "zh-cn"
    assert body["tags"] == ["MCP"]
    assert body["category"] == "product-updates"


CATEGORIES = [
    "product-updates",
    "tech-sharing",
    "product-recommendations",
    "industry-insights",
    "community-news",
    "product",
    "engineering",
    "model-news",
    "comparison",
]


@respx.mock
@pytest.mark.parametrize("category", CATEGORIES)
async def test_mcp_category_filters_preserve_slugs_and_aliases(category):
    public = respx.get(f"{API}/blogs/").mock(return_value=httpx.Response(200, json={}))
    editorial = respx.get(f"{API}/blogs/admin/").mock(return_value=httpx.Response(200, json={}))
    for name in (
        "acedatacloud_list_blog_posts",
        "acedatacloud_list_blog_drafts",
        "acedatacloud_list_blogs",
        "acedatacloud_list_blogs_admin",
    ):
        await mcp.call_tool(name, {"category": category})
    assert public.calls.last.request.url.params["category"] == category
    assert editorial.calls.last.request.url.params["category"] == category
    assert "authorization" not in public.calls.last.request.headers
    assert "authorization" in editorial.calls.last.request.headers


@respx.mock
@pytest.mark.parametrize("category", CATEGORIES)
@pytest.mark.parametrize(
    ("name", "method", "endpoint", "arguments"),
    [
        (
            "acedatacloud_create_blog_draft",
            "POST",
            f"{API}/blogs/admin/",
            {"slug": "launch", "title": "Title", "summary": "Summary", "content": "# Article"},
        ),
        ("acedatacloud_update_blog_post", "PATCH", DETAIL, {"blog_id": str(BLOG_ID)}),
        (
            "acedatacloud_create_blogs_admin",
            "POST",
            f"{API}/blogs/admin/",
            {"slug": "launch", "title": "Title", "summary": "Summary", "content": "# Article"},
        ),
        (
            "acedatacloud_replace_blogs_admin_id",
            "PUT",
            DETAIL,
            {
                "id": str(BLOG_ID),
                "slug": "launch",
                "title": "Title",
                "summary": "Summary",
                "content": "# Article",
            },
        ),
        ("acedatacloud_update_blogs_admin_id", "PATCH", DETAIL, {"id": str(BLOG_ID)}),
    ],
)
async def test_mcp_category_writes_preserve_slugs_and_aliases(
    category, name, method, endpoint, arguments
):
    preview, _ = await mcp.call_tool(name, {**arguments, "category": category})
    assert json.loads(preview[0].text)["status"] == "confirmation_required"
    assert not respx.calls
    route = respx.request(method, endpoint).mock(return_value=httpx.Response(200, json={}))
    await mcp.call_tool(name, {**arguments, "category": category, "confirm": True})
    assert json.loads(route.calls.last.request.content)["category"] == category


@respx.mock
async def test_mcp_draft_default_and_category_validation():
    arguments = {"slug": "launch", "title": "Title", "summary": "Summary", "content": "# Article"}
    content, _ = await mcp.call_tool("acedatacloud_create_blog_draft", arguments)
    assert json.loads(content[0].text)["target"]["category"] == "tech-sharing"
    for name in ("acedatacloud_create_blog_draft", "acedatacloud_create_blogs_admin"):
        for category in ("x" * 33, 123, ["tech-sharing"]):
            with pytest.raises(ToolError):
                await mcp.call_tool(name, {**arguments, "category": category})
    assert not respx.calls


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
async def test_review_submission_and_rejection():
    submit = respx.post(f"{DETAIL}submit/").mock(
        return_value=httpx.Response(200, json={"status": "pending"})
    )
    withdraw = respx.delete(f"{DETAIL}submit/").mock(
        return_value=httpx.Response(200, json={"status": "draft"})
    )
    reject = respx.post(f"{DETAIL}reject/").mock(
        return_value=httpx.Response(200, json={"status": "rejected"})
    )

    assert (
        json.loads(await acedatacloud_submit_blog_post(BLOG_ID, expected_version=4, confirm=True))[
            "status"
        ]
        == "pending"
    )
    assert json.loads(submit.calls.last.request.content) == {"expected_version": 4}
    assert (
        json.loads(
            await acedatacloud_reject_blog_post(
                BLOG_ID, expected_version=4, comment="Needs sources", confirm=True
            )
        )["status"]
        == "rejected"
    )
    assert json.loads(reject.calls.last.request.content) == {
        "expected_version": 4,
        "comment": "Needs sources",
    }
    assert (
        json.loads(
            await acedatacloud_withdraw_blog_submission(BLOG_ID, expected_version=4, confirm=True)
        )["status"]
        == "draft"
    )
    assert withdraw.called
    assert json.loads(withdraw.calls.last.request.content) == {"expected_version": 4}


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
    assert json.loads(approve_route.calls.last.request.content) == {
        "expected_version": 3,
        "comment": "",
    }
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
