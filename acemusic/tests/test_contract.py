"""Verify wire mapping and terminal group behavior without paid API calls."""

import json
from unittest.mock import AsyncMock, patch

import httpx
import pytest
import respx

from core.client import AceMusicClient
from core.utils import format_result, task_state
from tools.audio_tools import acemusic_generate_custom_music, acemusic_generate_music
from tools.lyrics_tools import acemusic_generate_lyrics
from tools.task_tools import acemusic_get_task, acemusic_get_tasks_batch, acemusic_list_tasks


@pytest.mark.asyncio
@respx.mock
async def test_submit_once_async_and_auth():
    route = respx.post("https://api.acedata.cloud/acemusic/audios").mock(
        return_value=httpx.Response(200, json={"task_id": "one"})
    )
    result = await AceMusicClient(api_token="secret").generate_audio(
        prompt="folk", custom=False, action="generate"
    )
    assert result["task_id"] == "one"
    assert route.call_count == 1
    assert json.loads(route.calls[0].request.content)["async"] is True
    assert route.calls[0].request.headers["authorization"] == "Bearer secret"


@pytest.mark.asyncio
async def test_tools_map_only_supported_fields():
    mock = AsyncMock(return_value={"task_id": "one"})
    with patch("tools.audio_tools.client.generate_audio", mock):
        await acemusic_generate_music("folk")
        assert mock.call_args.kwargs == {
            "action": "generate",
            "model": "acemusic-v1.1",
            "custom": False,
            "prompt": "folk",
        }
        await acemusic_generate_custom_music("[Verse] Home", "folk", title="Home")
        assert mock.call_args.kwargs["lyric"] == "[Verse] Home"
        assert "lyrics" not in mock.call_args.kwargs
        assert mock.call_args.kwargs["custom"] is True


@pytest.mark.asyncio
async def test_lyrics_and_task_queries_preserve_identity():
    with patch(
        "tools.lyrics_tools.client.generate_lyrics",
        AsyncMock(return_value={"success": True, "data": [{"text": "words"}]}),
    ) as mock:
        await acemusic_generate_lyrics("home", "folk")
        mock.assert_awaited_once_with(prompt="home", style="folk")
    with patch(
        "tools.task_tools.client.query_task",
        AsyncMock(return_value={"id": "one", "state": "processing"}),
    ) as mock:
        assert json.loads(await acemusic_get_task("one"))["mcp_task_polling"]["should_poll"]
        mock.assert_awaited_with(action="retrieve", id="one")
        await acemusic_get_tasks_batch(["one", "two"])
        mock.assert_awaited_with(action="retrieve_batch", ids=["one", "two"])
        await acemusic_list_tasks(2, 10)
        mock.assert_awaited_with(action="list", limit=10, offset=10)


def test_group_state_overrides_media_and_partial_is_terminal():
    pending = {
        "id": "one",
        "state": "processing",
        "response": {"data": [{"audio_url": "https://cdn.acedata.cloud/preview.mp3"}]},
    }
    assert task_state(pending) == "processing"
    partial = {
        "id": "one",
        "state": "partial_failed",
        "response": {
            "success": False,
            "data": [{"audio_url": "https://cdn.acedata.cloud/one.mp3"}],
        },
    }
    guide = json.loads(format_result(partial))["mcp_task_polling"]
    assert guide["terminal_state_reached"] and not guide["should_poll"]
    assert guide["state"] == "partial_failed"


@pytest.mark.asyncio
@respx.mock
async def test_timeout_does_not_retry_paid_submission():
    route = respx.post("https://api.acedata.cloud/acemusic/audios").mock(
        side_effect=httpx.ReadTimeout("lost response")
    )
    from core.exceptions import AceMusicTimeoutError

    with pytest.raises(AceMusicTimeoutError):
        await AceMusicClient(api_token="secret").generate_audio(prompt="folk")
    assert route.call_count == 1


@pytest.mark.asyncio
async def test_custom_tool_schema_requires_title_before_submission():
    from core.server import mcp

    tools = await mcp.list_tools()
    tool = next(tool for tool in tools if tool.name == "acemusic_generate_custom_music")
    assert set(tool.inputSchema["required"]) == {"lyric", "style", "title"}
    assert tool.inputSchema["properties"]["title"]["minLength"] == 1


@pytest.mark.asyncio
async def test_reference_tools_map_public_ids_without_implicit_work():
    from tools.audio_tools import acemusic_cover_audio, acemusic_mashup_audio, acemusic_upload_audio

    mock = AsyncMock(return_value={"task_id": "one"})
    with patch("tools.audio_tools.client.generate_audio", mock):
        await acemusic_upload_audio("https://example.com/owned.mp3", audio_id="anchor")
        mock.assert_awaited_with(
            action="upload", audio_url="https://example.com/owned.mp3", audio_id="anchor"
        )
        await acemusic_cover_audio("audio-a", "words", "folk")
        mock.assert_awaited_with(
            action="cover",
            model="acemusic-v1.1",
            audio_id="audio-a",
            lyric="words",
            style="folk",
            audio_influence=60,
        )
        await acemusic_mashup_audio(["audio-a", "audio-b"], "words", "folk")
        mock.assert_awaited_with(
            action="mashup",
            model="acemusic-v1.1",
            mashup_audio_ids=["audio-a", "audio-b"],
            lyric="words",
            style="folk",
            audio_influence=60,
        )
        assert mock.await_count == 3


@pytest.mark.asyncio
async def test_invalid_reference_input_never_submits():
    from tools.audio_tools import acemusic_cover_audio, acemusic_mashup_audio, acemusic_upload_audio

    with patch("tools.audio_tools.client.generate_audio", AsyncMock()) as mock:
        with pytest.raises(ValueError):
            await acemusic_mashup_audio(["same", "same"], "words", "folk")
        with pytest.raises(ValueError):
            await acemusic_cover_audio("audio", "words", "folk", audio_influence=101)
        with pytest.raises(ValueError):
            await acemusic_upload_audio("http://example.com/audio.mp3")
        mock.assert_not_awaited()


@pytest.mark.asyncio
async def test_reference_schema_and_capability_discovery_agree():
    from core.server import mcp
    from tools.info_tools import acemusic_get_capabilities

    tools = {tool.name: tool for tool in await mcp.list_tools()}
    assert {
        "acemusic_upload_audio",
        "acemusic_cover_audio",
        "acemusic_mashup_audio",
    } <= tools.keys()
    schema = tools["acemusic_mashup_audio"].inputSchema["properties"]["mashup_audio_ids"]
    assert schema["minItems"] == schema["maxItems"] == 2
    capabilities = json.loads(acemusic_get_capabilities())
    assert capabilities["actions"] == ["generate", "upload", "cover", "mashup"]
    assert not {"upload", "cover", "mashup"} & set(capabilities["unsupported"])
