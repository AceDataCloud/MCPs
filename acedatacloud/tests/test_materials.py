"""Unit tests for the marketing-material tools."""

import json

import httpx
import pytest
import respx

from tools.materials_tools import (
    acedatacloud_get_material,
    acedatacloud_list_publish_channels,
    acedatacloud_pick_random_materials,
    acedatacloud_search_materials,
)

API = "https://platform.acedata.cloud/api/v1"
MID = "f1c66741-a488-43ca-91fc-e53fbbda639a"
CHAN = "a2c66741-a488-43ca-91fc-e53fbbda6300"


def _materials(*items):
    return httpx.Response(200, json={"count": len(items), "items": list(items)})


@respx.mock
@pytest.mark.asyncio
async def test_search_keyword_matches_title_or_content():
    respx.get(f"{API}/publish-materials/").mock(
        return_value=_materials(
            {"id": "1", "title": "AAA", "content": "nothing", "metadata": {}},
            {"id": "2", "title": "BBB", "content": "has the keyword inside", "metadata": {}},
        )
    )
    out = json.loads(await acedatacloud_search_materials(keyword="keyword"))
    assert out["count"] == 1
    assert out["items"][0]["id"] == "2"
    # preview by default, not full content
    assert "content_preview" in out["items"][0]
    assert "content" not in out["items"][0]


@respx.mock
@pytest.mark.asyncio
async def test_channel_name_resolves_to_id_filter():
    respx.get(f"{API}/publish-channels/").mock(
        return_value=httpx.Response(
            200, json={"count": 1, "items": [{"id": CHAN, "name": "zhihu", "title": "知乎"}]}
        )
    )
    mat_route = respx.get(f"{API}/publish-materials/").mock(
        return_value=_materials({"id": "1", "title": "T", "content": "c", "metadata": {}})
    )
    out = json.loads(await acedatacloud_search_materials(channel="zhihu"))
    assert out["returned"] == 1
    assert mat_route.calls[0].request.url.params["channel_id"] == CHAN


@respx.mock
@pytest.mark.asyncio
async def test_channel_no_match_returns_empty_note():
    respx.get(f"{API}/publish-channels/").mock(
        return_value=httpx.Response(200, json={"count": 0, "items": []})
    )
    out = json.loads(await acedatacloud_search_materials(channel="nonexistent"))
    assert out["count"] == 0
    assert "note" in out


@respx.mock
@pytest.mark.asyncio
async def test_pick_random_returns_full_content():
    respx.get(f"{API}/publish-materials/").mock(
        return_value=_materials(
            {"id": "1", "title": "A", "content": "full one", "metadata": {}},
            {"id": "2", "title": "B", "content": "full two", "metadata": {}},
            {"id": "3", "title": "C", "content": "full three", "metadata": {}},
        )
    )
    out = json.loads(await acedatacloud_pick_random_materials(count=2))
    assert out["returned"] == 2
    assert all("content" in it for it in out["items"])


@respx.mock
@pytest.mark.asyncio
async def test_get_material_by_id():
    respx.get(f"{API}/publish-materials/{MID}/").mock(
        return_value=httpx.Response(200, json={"id": MID, "title": "X", "content": "body"})
    )
    out = json.loads(await acedatacloud_get_material(material_id=MID))
    assert out["id"] == MID
    assert out["content"] == "body"


@respx.mock
@pytest.mark.asyncio
async def test_list_publish_channels_search_filters():
    respx.get(f"{API}/publish-channels/").mock(
        return_value=httpx.Response(
            200,
            json={
                "count": 2,
                "items": [
                    {"id": CHAN, "name": "zhihu", "title": "知乎", "domain": "zhihu.com"},
                    {"id": "x", "name": "medium", "title": "Medium", "domain": "medium.com"},
                ],
            },
        )
    )
    out = json.loads(await acedatacloud_list_publish_channels(search="zhihu"))
    assert out["count"] == 1
    assert out["items"][0]["id"] == CHAN
