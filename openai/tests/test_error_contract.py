"""No-network contracts for HTTP metadata and safe tool error serialization."""

import json

import httpx
import pytest

from core.client import OpenAIClient
from core.exceptions import (
    OpenAIAPIError,
    OpenAIAuthError,
    OpenAIError,
    OpenAINetworkError,
    OpenAITimeoutError,
    format_tool_error,
)
from tools import (
    audio_tools,
    chat_tools,
    embedding_tools,
    image_tools,
    info_tools,
    responses_tools,
    tasks_tools,
)

_SECRET = "opaque-fixture-credential"
_PRIVATE = "supplier-private https://private.invalid/path?token=leak Bearer sensitive-body"


async def _request(client, mode):
    if mode == "get":
        return await client.request_get("/openai/models")
    if mode == "binary":
        return await client.request_binary("/v1/audio/speech", {"input": "fixture"})
    if mode == "multipart":
        return await client.request_multipart("/v1/audio/transcriptions", {"file": b"fixture"})
    return await client.request("/openai/chat/completions", {"messages": []})


def _install_transport(monkeypatch, handler):
    real = httpx.AsyncClient
    transport = httpx.MockTransport(handler)
    monkeypatch.setattr(httpx, "AsyncClient", lambda *_args, **_kwargs: real(transport=transport))


@pytest.mark.parametrize("mode", ["get", "post", "binary", "multipart"])
@pytest.mark.parametrize("status", [401, 403, 429, 500])
@pytest.mark.parametrize("body_kind", ["json", "html", "list", "string_error"])
async def test_http_errors_keep_status_and_correlation_without_body_leak(
    monkeypatch, mode, status, body_kind
):
    calls = []

    def handler(request):
        calls.append(request)
        headers = {"x-request-id": "req_fixture-123", "authorization": _SECRET}
        if body_kind == "json":
            return httpx.Response(
                status,
                headers=headers,
                json={
                    "error": {"code": "rate_limit_exceeded", "message": _PRIVATE},
                    "debug": _SECRET,
                },
            )
        if body_kind == "list":
            return httpx.Response(status, headers=headers, json=[_PRIVATE, _SECRET])
        if body_kind == "string_error":
            return httpx.Response(status, headers=headers, json={"error": _PRIVATE})
        return httpx.Response(status, headers=headers, text=f"<html>{_PRIVATE} {_SECRET}</html>")

    _install_transport(monkeypatch, handler)
    client = OpenAIClient(api_token=_SECRET, base_url="http://127.0.0.1:1")
    with pytest.raises(OpenAIError) as caught:
        await _request(client, mode)
    error = caught.value
    assert isinstance(error, OpenAIAuthError if status in (401, 403) else OpenAIAPIError)
    assert error.status_code == status
    assert error.request_id == "req_fixture-123"
    assert error.code == ("rate_limit_exceeded" if body_kind == "json" else f"http_{status}")
    result = json.loads(format_tool_error(error))
    assert result["status_code"] == status
    assert result["request_id"] == "req_fixture-123"
    assert result["code"] == error.code
    assert result["error"] == ("Authentication Error" if status in (401, 403) else "API Error")
    public = json.dumps(result)
    assert _PRIVATE not in public and _SECRET not in public and "private.invalid" not in public
    assert "responseBody" not in result and "headers" not in result
    assert len(calls) == 1


@pytest.mark.parametrize("mode", ["get", "post", "binary", "multipart"])
@pytest.mark.parametrize(
    "error_type",
    [
        httpx.ConnectTimeout,
        httpx.ReadTimeout,
        httpx.ConnectError,
        httpx.ReadError,
        httpx.RemoteProtocolError,
    ],
)
async def test_transport_failures_have_codes_without_fabricated_http_status(
    monkeypatch, mode, error_type
):
    def handler(request):
        raise error_type(f"{_PRIVATE} {_SECRET}", request=request)

    _install_transport(monkeypatch, handler)
    client = OpenAIClient(api_token=_SECRET, base_url="http://127.0.0.1:1")
    with pytest.raises(OpenAIError) as caught:
        await _request(client, mode)
    timeout = issubclass(error_type, httpx.TimeoutException)
    assert isinstance(caught.value, OpenAITimeoutError if timeout else OpenAINetworkError)
    result = json.loads(format_tool_error(caught.value))
    assert result["code"] == ("timeout_error" if timeout else "network_error")
    assert result["status_code"] is None and result["request_id"] is None
    assert "private.invalid" not in json.dumps(result)
    assert _SECRET not in json.dumps(result)


@pytest.mark.parametrize(
    "request_id",
    ["req_ok", "req.unsafe.host", "Bearer key", "sk-secret", "x" * 129, _SECRET, "req\nforged"],
)
@pytest.mark.parametrize(
    "code",
    [
        "content_policy_violation",
        "supplier_private_model",
        "https://private.invalid",
        {"secret": _SECRET},
    ],
)
def test_metadata_safety(request_id, code):
    client = OpenAIClient(api_token=_SECRET)
    response = httpx.Response(
        403,
        headers={"x-request-id": request_id},
        json={"error": {"code": code, "message": _PRIVATE}},
    )
    with pytest.raises(OpenAIError) as caught:
        client._handle_error_response(response)
    payload = json.loads(format_tool_error(caught.value))
    assert payload["request_id"] == ("req_ok" if request_id == "req_ok" else None)
    assert payload["code"] == (code if code == "content_policy_violation" else "http_403")
    assert _PRIVATE not in json.dumps(payload) and _SECRET not in json.dumps(payload)


_CASES = [
    (info_tools, "openai_get_models", "models", {}),
    (info_tools, "openai_get_realtime_connection_info", "realtime", {}),
    (chat_tools, "openai_chat_completion", "chat_completions", {"messages": []}),
    (responses_tools, "openai_create_response", "responses", {"input": "fixture"}),
    (embedding_tools, "openai_create_embedding", "embeddings", {"input": "fixture"}),
    (image_tools, "openai_generate_image", "images_generations_async", {"prompt": "fixture"}),
    (
        image_tools,
        "openai_edit_image",
        "images_edits_async",
        {"prompt": "fixture", "image": "https://example.test/i.png"},
    ),
    (audio_tools, "openai_text_to_speech", "audio_speech", {"input": "fixture"}),
    (
        audio_tools,
        "openai_transcribe_audio",
        "audio_transcriptions",
        {"url": "https://example.test/a.mp3"},
    ),
    (tasks_tools, "openai_get_task", "tasks", {"id": "fixture-id"}),
    (tasks_tools, "openai_list_tasks", "tasks", {}),
]


@pytest.mark.parametrize("module,name,method,kwargs", _CASES, ids=[item[1] for item in _CASES])
@pytest.mark.parametrize("status", [401, 403, 429, 500])
async def test_all_tools_use_the_shared_compatible_error_contract(
    monkeypatch, module, name, method, kwargs, status
):
    error_type = OpenAIAuthError if status in (401, 403) else OpenAIAPIError

    async def failed(*_args, **_kwargs):
        raise error_type(
            _PRIVATE, code="rate_limit_exceeded", status_code=status, request_id="req_all_tools"
        )

    monkeypatch.setattr(module.client, method, failed)
    if name == "openai_transcribe_audio":
        _install_transport(monkeypatch, lambda _req: httpx.Response(200, content=b"audio"))
    payload = json.loads(await getattr(module, name)(**kwargs))
    assert payload["status_code"] == status
    assert payload["request_id"] == "req_all_tools"
    assert payload["code"] == "rate_limit_exceeded"
    assert payload["error"] == ("Authentication Error" if status in (401, 403) else "API Error")
    assert "private.invalid" not in payload["message"]


async def test_unexpected_tool_exception_does_not_expose_details(monkeypatch):
    async def fail():
        raise RuntimeError(f"{_PRIVATE} {_SECRET}")

    monkeypatch.setattr(info_tools.client, "models", fail)
    payload = json.loads(await info_tools.openai_get_models())
    assert payload == {
        "error": "Error listing models",
        "message": "The operation failed.",
        "status_code": None,
        "code": "internal_error",
        "request_id": None,
    }


@pytest.mark.parametrize("status", [401, 403, 429, 500])
async def test_audio_download_error_is_safe_and_keeps_actual_status(monkeypatch, status):
    _install_transport(
        monkeypatch,
        lambda _req: httpx.Response(
            status, text=_PRIVATE, headers={"x-request-id": "req_download"}
        ),
    )
    payload = json.loads(
        await audio_tools.openai_transcribe_audio(url=f"https://example.test/audio?token={_SECRET}")
    )
    assert payload["error"] == "Failed to download audio file"
    assert payload["status_code"] == status
    assert payload["request_id"] == "req_download"
    assert "example.test" not in json.dumps(payload) and _SECRET not in json.dumps(payload)


def test_local_exception_message_is_never_public_diagnostics():
    error = OpenAIAPIError("undetectable-private-model-name opaque-credential")
    payload = json.loads(format_tool_error(error))
    assert payload["message"] == "The API request failed."
    assert "undetectable" not in json.dumps(payload)


def test_current_request_token_cannot_be_returned_as_correlation_id():
    from core.client import set_request_api_token

    client = OpenAIClient(api_token="configured-fixture")
    set_request_api_token(_SECRET)
    try:
        with pytest.raises(OpenAIError) as caught:
            client._handle_error_response(httpx.Response(401, headers={"x-request-id": _SECRET}))
        assert json.loads(format_tool_error(caught.value))["request_id"] is None
    finally:
        set_request_api_token(None)
