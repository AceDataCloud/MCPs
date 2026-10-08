"""Unit tests for the catalog, docs and model-catalog tools + public client path."""

import json

import httpx
import pytest
import respx

from core.client import PlatformClient
from tools.catalog_tools import (
    acedatacloud_get_api_spec,
    acedatacloud_get_pricing,
    acedatacloud_get_public_usage_packages,
    acedatacloud_get_service,
    acedatacloud_list_apis,
)
from tools.docs_tools import (
    acedatacloud_get_doc,
    acedatacloud_list_docs,
    acedatacloud_search_docs,
)
from tools.model_tools import acedatacloud_get_model, acedatacloud_list_model_catalog
from tools.read_tools import acedatacloud_list_distributions

API = "https://platform.acedata.cloud/api/v1"
UUID = "f1c66741-a488-43ca-91fc-e53fbbda639a"


@respx.mock
@pytest.mark.asyncio
async def test_get_service_by_id_uses_id_filter():
    route = respx.get(f"{API}/services/").mock(
        return_value=httpx.Response(
            200,
            json={
                "count": 1,
                "items": [{"id": UUID, "alias": "suno", "cost": [], "unit": "Credit"}],
            },
        )
    )
    out = json.loads(await acedatacloud_get_service(service=UUID))
    assert out["alias"] == "suno"
    assert route.calls[0].request.url.params["id"] == UUID


@respx.mock
@pytest.mark.asyncio
async def test_get_service_by_alias_paginates():
    respx.get(f"{API}/services/").mock(
        return_value=httpx.Response(
            200,
            json={"count": 1, "items": [{"id": "svc-1", "alias": "midjourney", "unit": "Count"}]},
        )
    )
    out = json.loads(await acedatacloud_get_service(service="midjourney"))
    assert out["id"] == "svc-1"


@respx.mock
@pytest.mark.asyncio
async def test_get_service_resolves_unique_exact_tag_when_alias_is_missing():
    respx.get(f"{API}/services/").mock(
        return_value=httpx.Response(
            200,
            json={
                "count": 1,
                "items": [
                    {
                        "id": "svc-chat",
                        "alias": None,
                        "title": "AI Dialogue",
                        "tags": ["aichat"],
                    }
                ],
            },
        )
    )
    out = json.loads(await acedatacloud_get_service(service="aichat"))
    assert out["id"] == "svc-chat"


@respx.mock
@pytest.mark.asyncio
async def test_get_service_rejects_ambiguous_tag():
    respx.get(f"{API}/services/").mock(
        return_value=httpx.Response(
            200,
            json={
                "count": 2,
                "items": [
                    {"id": "svc-chat", "title": "AI Dialogue", "tags": ["aichat"]},
                    {"id": "svc-deepseek", "alias": "deepseek", "tags": ["aichat"]},
                ],
            },
        )
    )
    out = json.loads(await acedatacloud_get_service(service="aichat"))
    assert out["error"] == "validation_error"
    assert "service UUID or exact alias" in out["message"]


@respx.mock
@pytest.mark.asyncio
async def test_get_pricing_returns_cost():
    respx.get(f"{API}/services/").mock(
        return_value=httpx.Response(
            200,
            json={
                "count": 1,
                "items": [
                    {
                        "id": UUID,
                        "alias": "suno",
                        "unit": "Credit",
                        "free_amount": 0,
                        "cost": [{"x": 1}],
                    }
                ],
            },
        )
    )
    out = json.loads(await acedatacloud_get_pricing(service=UUID))
    assert out["unit"] == "Credit"
    assert out["cost"] == [{"x": 1}]
    assert "pricing_mode" not in out
    assert "reference_quote" not in out


@respx.mock
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "alias,min_amount,max_amount,unit",
    [
        ("hacker-news", 8800, 8800, "full_package"),
        ("sketchfab-3d", 199000, 199000, "full_package"),
        ("spotify-podcasts", 1090000, 1090000, "full_package"),
        ("audible-audiobooks", 89000, 89000, "full_package"),
        ("asmr", 89000, 89000, "full_package"),
        ("youtube-video", 249, 329, "tb"),
        ("youtube-podcasts", 249, 329, "tb"),
        ("flickr", 189000, 189000, "full_package"),
    ],
)
async def test_get_pricing_preserves_public_dataset_reference_quotes(
    alias, min_amount, max_amount, unit
):
    quote = {
        "currency": "CNY",
        "min_amount": min_amount,
        "max_amount": max_amount,
        "unit": unit,
        "status": "reference",
    }
    route = respx.get(f"{API}/services/").mock(
        return_value=httpx.Response(
            200,
            json={
                "count": 1,
                "items": [
                    {
                        "id": UUID,
                        "alias": alias,
                        "type": "Dataset",
                        "private": False,
                        "unit": "Count",
                        "cost": [],
                        "packages": [],
                        "metadata": {
                            "pricing_mode": "contact_only",
                            "reference_quote": {**quote, "unrelated": "not-pricing"},
                            "unrelated": "not-pricing",
                        },
                    }
                ],
            },
        )
    )
    out = json.loads(await acedatacloud_get_pricing(service=alias))
    assert out["alias"] == alias
    assert out["pricing_mode"] == "contact_only"
    assert out["reference_quote"] == quote
    assert out["unit"] == "Count"
    assert out["cost"] == []
    assert "packages" not in out
    assert "metadata" not in out
    assert "not-pricing" not in json.dumps(out)
    assert "authorization" not in route.calls[0].request.headers
    assert len(respx.calls) == 1


@respx.mock
@pytest.mark.asyncio
async def test_get_pricing_does_not_invent_missing_dataset_quote():
    respx.get(f"{API}/services/").mock(
        return_value=httpx.Response(
            200,
            json={
                "count": 1,
                "items": [
                    {
                        "id": UUID,
                        "type": "Dataset",
                        "private": False,
                        "metadata": {"pricing_mode": "contact_only"},
                    }
                ],
            },
        )
    )
    out = json.loads(await acedatacloud_get_pricing(service=UUID))
    assert out["pricing_mode"] == "contact_only"
    assert "reference_quote" not in out


@respx.mock
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "service_type,private,pricing_mode",
    [
        ("Dataset", True, "contact_only"),
        ("Dataset", None, "contact_only"),
        ("Api", False, "contact_only"),
        ("Dataset", False, "other"),
    ],
)
async def test_get_pricing_only_adds_quotes_for_public_contact_datasets(
    service_type, private, pricing_mode
):
    respx.get(f"{API}/services/").mock(
        return_value=httpx.Response(
            200,
            json={
                "count": 1,
                "items": [
                    {
                        "id": UUID,
                        "type": service_type,
                        "private": private,
                        "metadata": {
                            "pricing_mode": pricing_mode,
                            "reference_quote": {
                                "currency": "CNY",
                                "min_amount": 8800,
                                "max_amount": 8800,
                                "unit": "full_package",
                                "status": "reference",
                            },
                        },
                    }
                ],
            },
        )
    )
    out = json.loads(await acedatacloud_get_pricing(service=UUID))
    assert "pricing_mode" not in out
    assert "reference_quote" not in out


@respx.mock
@pytest.mark.asyncio
async def test_get_public_usage_packages_returns_positive_raw_ladder():
    respx.get(f"{API}/services/").mock(
        return_value=httpx.Response(
            200, json={"count": 1, "items": [{"id": UUID, "alias": "suno"}]}
        )
    )
    respx.get(f"{API}/services/{UUID}/").mock(
        return_value=httpx.Response(
            200,
            json={
                "packages": [
                    {"type": "Usage", "private": False, "amount": 10000, "price": 9.99},
                    {"type": "Usage", "private": False, "amount": 20000, "price": 15.0},
                    {"type": "Usage", "private": True, "amount": 50000, "price": 1.0},
                    {"type": "Period", "private": False, "amount": 30000, "price": 10.0},
                ]
            },
        )
    )
    out = json.loads(await acedatacloud_get_public_usage_packages(service="suno"))
    assert out == {
        "source": "public_service_detail",
        "service_id": UUID,
        "packages": [
            {"amount": "10000", "price": "9.99"},
            {"amount": "20000", "price": "15.0"},
        ],
    }


@respx.mock
@pytest.mark.asyncio
async def test_get_public_usage_packages_fails_closed_on_missing_ladder():
    respx.get(f"{API}/services/").mock(
        return_value=httpx.Response(
            200, json={"count": 1, "items": [{"id": UUID, "alias": "suno"}]}
        )
    )
    respx.get(f"{API}/services/{UUID}/").mock(
        return_value=httpx.Response(200, json={"packages": []})
    )
    out = json.loads(await acedatacloud_get_public_usage_packages(service="suno"))
    assert out["error"] == "Unavailable"


@respx.mock
@pytest.mark.asyncio
async def test_list_apis_uses_server_side_service_filter():
    respx.get(f"{API}/services/").mock(
        return_value=httpx.Response(
            200,
            json={"count": 1, "items": [{"id": UUID, "alias": "suno"}]},
        )
    )
    route = respx.get(f"{API}/apis/").mock(
        return_value=httpx.Response(
            200,
            json={
                "count": 1,
                "items": [
                    {
                        "id": "api-1",
                        "service_id": UUID,
                        "path": "/suno/audios",
                        "definition": {"big": "blob"},
                        "cost": [],
                    },
                ],
            },
        )
    )
    out = json.loads(await acedatacloud_list_apis(service="suno", stage="Production"))
    assert out["count"] == 1
    assert out["items"][0]["path"] == "/suno/audios"
    assert "definition" not in out["items"][0]
    params = route.calls[0].request.url.params
    assert params["service"] == UUID
    assert params["stage"] == "Production"


@respx.mock
@pytest.mark.asyncio
async def test_get_api_spec_by_path():
    respx.get(f"{API}/apis/").mock(
        return_value=httpx.Response(
            200,
            json={
                "count": 1,
                "items": [
                    {
                        "id": "api-1",
                        "path": "/suno/audios",
                        "method": "POST",
                        "definition": {"openapi": "3.0"},
                        "cost": [],
                    }
                ],
            },
        )
    )
    out = json.loads(await acedatacloud_get_api_spec(path="/suno/audios"))
    assert out["definition"] == {"openapi": "3.0"}
    assert out["method"] == "POST"


@respx.mock
@pytest.mark.asyncio
async def test_search_docs_uses_query_param():
    route = respx.get(f"{API}/search/").mock(
        return_value=httpx.Response(
            200, json={"query": "suno", "lang": "en", "results": [{"alias": "x"}]}
        )
    )
    out = json.loads(await acedatacloud_search_docs(query="suno", lang="en", limit=5))
    assert out["results"][0]["alias"] == "x"
    params = route.calls[0].request.url.params
    assert params["query"] == "suno"
    assert params["limit"] == "5"


@respx.mock
@pytest.mark.asyncio
async def test_list_docs_passes_tag_and_private_filters():
    route = respx.get(f"{API}/documents/").mock(
        return_value=httpx.Response(
            200,
            json={"count": 1, "items": [{"id": UUID, "alias": "app-doc", "content": "x" * 500}]},
        )
    )
    out = json.loads(await acedatacloud_list_docs(tag="application", private=False, offset=10))
    assert out["count"] == 1
    # Long content is trimmed to a preview in the browse view.
    assert "content" not in out["items"][0]
    assert len(out["items"][0]["content_preview"]) == 200
    params = route.calls[0].request.url.params
    assert params["tag"] == "application"
    assert params["private"] == "false"
    assert params["offset"] == "10"


@pytest.mark.asyncio
async def test_get_doc_rejects_non_uuid():
    out = json.loads(await acedatacloud_get_doc(doc_id="../etc/passwd"))
    assert out["error"] == "Invalid Input"


@respx.mock
@pytest.mark.asyncio
async def test_get_doc_by_id():
    respx.get(f"{API}/documents/").mock(
        return_value=httpx.Response(
            200, json={"count": 1, "items": [{"id": UUID, "content": "# Hello"}]}
        )
    )
    out = json.loads(await acedatacloud_get_doc(doc_id=UUID))
    assert out["content"] == "# Hello"


@respx.mock
@pytest.mark.asyncio
async def test_model_catalog_filters_modality():
    respx.get(f"{API}/models/catalog/").mock(
        return_value=httpx.Response(
            200,
            json={
                "modalities": {"chat": 1, "video": 1},
                "items": [
                    {"id": "gpt-4.1", "modality": "chat", "provider": "OpenAI"},
                    {"id": "veo-3", "modality": "video", "provider": "Google"},
                ],
            },
        )
    )
    out = json.loads(await acedatacloud_list_model_catalog(modality="chat"))
    assert out["count"] == 1
    assert out["items"][0]["id"] == "gpt-4.1"


@respx.mock
@pytest.mark.asyncio
async def test_get_model_substring_match():
    respx.get(f"{API}/models/catalog/").mock(
        return_value=httpx.Response(
            200,
            json={
                "items": [
                    {"id": "claude-opus-4.8", "name": "Claude Opus 4.8"},
                    {"id": "gpt-4.1", "name": "GPT-4.1"},
                ]
            },
        )
    )
    out = json.loads(await acedatacloud_get_model(model="claude"))
    assert out["count"] == 1
    assert out["items"][0]["id"] == "claude-opus-4.8"


@respx.mock
@pytest.mark.asyncio
async def test_list_distributions_merges_status_and_history():
    respx.get(f"{API}/platform-tokens/me/").mock(
        return_value=httpx.Response(200, json={"id": "user-1"})
    )
    respx.get(f"{API}/distribution-statuses/").mock(
        return_value=httpx.Response(200, json={"count": 1, "items": [{"level": 2, "reward": 12.5}]})
    )
    respx.get(f"{API}/distribution-histories/").mock(
        return_value=httpx.Response(200, json={"count": 3, "items": [{"reward": 1.0}]})
    )
    out = json.loads(await acedatacloud_list_distributions())
    assert out["status"]["level"] == 2
    assert out["history_count"] == 3


@respx.mock
@pytest.mark.asyncio
async def test_public_get_omits_auth_header_when_no_token():
    route = respx.get(f"{API}/services/").mock(
        return_value=httpx.Response(200, json={"count": 0, "items": []})
    )
    public_client = PlatformClient(api_token="must-not-be-forwarded")
    await public_client.get_public("/services/")
    assert "authorization" not in {k.lower() for k in route.calls[0].request.headers}
