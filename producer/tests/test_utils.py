"""Unit tests for utility functions."""

import json

from core.utils import (
    format_audio_result,
    format_lyrics_result,
    format_task_result,
    format_upload_result,
    format_video_result,
    format_wav_result,
)


class TestFormatAudioResult:
    """Tests for format_audio_result function."""

    def test_format_success(self, mock_audio_response):
        """Test formatting successful audio response."""
        result = format_audio_result(mock_audio_response)
        data = json.loads(result)
        assert data["success"] is True
        assert data["task_id"] == "test-task-123"
        assert data["trace_id"] == "test-trace-456"
        assert len(data["data"]) == 1
        assert data["data"][0]["title"] == "Test Song"
        assert data["data"][0]["duration"] == 120.5
        assert data["data"][0]["state"] == "succeeded"
        assert "audio_url" in data["data"][0]
        assert data["mcp_async_submission"]["poll_tool"] == "producer_get_task"

    def test_format_error(self, mock_error_response):
        """Test formatting error response."""
        result = format_audio_result(mock_error_response)
        data = json.loads(result)
        assert data["success"] is False
        assert data["error"]["code"] == "invalid_request"

    def test_format_empty_data(self):
        """Test formatting response with no audio data."""
        response = {"success": True, "task_id": "123", "data": []}
        result = format_audio_result(response)
        data = json.loads(result)
        assert data["task_id"] == "123"
        assert data["data"] == []


class TestFormatLyricsResult:
    """Tests for format_lyrics_result function."""

    def test_format_success(self, mock_lyrics_response):
        """Test formatting successful lyrics response."""
        result = format_lyrics_result(mock_lyrics_response)
        data = json.loads(result)
        assert data["success"] is True
        assert data["task_id"] == "lyrics-task-123"
        assert data["data"]["title"] == "Test Song Title"
        assert data["data"]["status"] == "complete"
        assert "Generated lyrics here" in data["data"]["text"]

    def test_format_error(self, mock_error_response):
        """Test formatting error response."""
        result = format_lyrics_result(mock_error_response)
        data = json.loads(result)
        assert data["success"] is False


class TestFormatTaskResult:
    """Tests for format_task_result function."""

    def test_format_success(self, mock_task_response):
        """Test formatting successful task response."""
        result = format_task_result(mock_task_response)
        data = json.loads(result)
        assert data["id"] == "task-123"
        assert data["request"]["action"] == "generate"
        assert data["response"]["success"] is True
        assert data["response"]["data"][0]["title"] == "Test Song"
        assert data["mcp_task_polling"]["poll_tool"] == "producer_get_task"

    def test_format_error(self):
        """Test formatting error response."""
        error_response = {"error": {"code": "not_found", "message": "Task not found"}}
        result = format_task_result(error_response)
        data = json.loads(result)
        assert data["error"]["code"] == "not_found"


class TestFormatUploadResult:
    """Tests for format_upload_result function."""

    def test_format_success(self):
        """Test formatting successful upload response."""
        response = {
            "success": True,
            "task_id": "upload-task-123",
            "data": {"audio_id": "uploaded-id-1"},
        }
        result = format_upload_result(response)
        data = json.loads(result)
        assert data["success"] is True
        assert data["task_id"] == "upload-task-123"


class TestFormatVideoResult:
    """Tests for format_video_result function."""

    def test_format_success(self):
        """Test formatting successful video response."""
        response = {
            "success": True,
            "task_id": "video-task-123",
            "data": {"video_url": "https://cdn.example.com/video.mp4"},
        }
        result = format_video_result(response)
        data = json.loads(result)
        assert data["success"] is True
        assert data["task_id"] == "video-task-123"


class TestFormatWavResult:
    """Tests for format_wav_result function."""

    def test_format_success(self):
        """Test formatting successful WAV response."""
        response = {
            "success": True,
            "task_id": "wav-task-123",
            "data": {"audio_url": "https://cdn.example.com/audio.wav"},
        }
        result = format_wav_result(response)
        data = json.loads(result)
        assert data["success"] is True
        assert data["task_id"] == "wav-task-123"
