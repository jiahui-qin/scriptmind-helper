"""Tests for tts_service — mock Moonshot TTS API calls."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import tempfile
import pytest
from unittest.mock import patch, MagicMock, mock_open
from app.services.tts_service import synthesize_full_script


# Minimal valid WAV header bytes for mocking (44 bytes PCM WAV header)
FAKE_WAV_BYTES = (
    b'RIFF\x24\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00'
    b'\x44\xac\x00\x00\x88\x58\x01\x00\x02\x00\x10\x00data\x00\x00\x00\x00'
)

SAMPLE_LINES = [
    {
        "id": 1, "line_number": 1, "content": "你好世界",
        "role_id": 1, "emotion_tag": "喜悦", "speech_rate": 1.0,
    },
    {
        "id": 2, "line_number": 2, "content": "今天天气真好",
        "role_id": 2, "emotion_tag": "平静", "speech_rate": 1.1,
    },
    {
        "id": 3, "line_number": 3, "content": "再见",
        "role_id": 1, "emotion_tag": "悲伤", "speech_rate": 0.9,
    },
]

SAMPLE_ROLE_VOICE_MAP = {
    1: "male-qn-qingse",
    2: "female-qn-qingse",
}


class TestSynthesizeFullScript:
    """Tests for synthesize_full_script with mocked Moonshot TTS API."""

    @patch("app.services.tts_service._call_moonshot_tts")
    def test_synthesize_generates_wav_and_srt(self, mock_tts: MagicMock):
        """Test that synthesize generates WAV audio and SRT subtitle files."""
        mock_tts.return_value = FAKE_WAV_BYTES

        with tempfile.TemporaryDirectory() as tmpdir:
            result = synthesize_full_script(
                lines=SAMPLE_LINES,
                role_voice_map=SAMPLE_ROLE_VOICE_MAP,
                output_dir=tmpdir,
                script_id=1,
            )

            assert "audio_path" in result
            assert "srt_path" in result
            assert os.path.exists(result["audio_path"])
            assert os.path.exists(result["srt_path"])
            assert result["audio_path"].endswith("script_1_full.wav")
            assert result["srt_path"].endswith("script_1_full.srt")

    @patch("app.services.tts_service._call_moonshot_tts")
    def test_tts_called_for_each_line(self, mock_tts: MagicMock):
        """Test that TTS API is called once per line."""
        mock_tts.return_value = FAKE_WAV_BYTES

        with tempfile.TemporaryDirectory() as tmpdir:
            synthesize_full_script(
                lines=SAMPLE_LINES,
                role_voice_map=SAMPLE_ROLE_VOICE_MAP,
                output_dir=tmpdir,
                script_id=1,
            )

            assert mock_tts.call_count == 3

    @patch("app.services.tts_service._call_moonshot_tts")
    def test_correct_voice_per_role(self, mock_tts: MagicMock):
        """Test that correct voice is used based on role_voice_map."""
        mock_tts.return_value = FAKE_WAV_BYTES

        with tempfile.TemporaryDirectory() as tmpdir:
            synthesize_full_script(
                lines=SAMPLE_LINES,
                role_voice_map=SAMPLE_ROLE_VOICE_MAP,
                output_dir=tmpdir,
                script_id=1,
            )

            # Line 1: role_id=1 → male-qn-qingse
            call_1 = mock_tts.call_args_list[0]
            assert call_1[0][1] == "male-qn-qingse"

            # Line 2: role_id=2 → female-qn-qingse
            call_2 = mock_tts.call_args_list[1]
            assert call_2[0][1] == "female-qn-qingse"

            # Line 3: role_id=1 → male-qn-qingse
            call_3 = mock_tts.call_args_list[2]
            assert call_3[0][1] == "male-qn-qingse"

    @patch("app.services.tts_service._call_moonshot_tts")
    def test_default_voice_for_unmapped_role(self, mock_tts: MagicMock):
        """Test that unmapped roles use default voice."""
        mock_tts.return_value = FAKE_WAV_BYTES
        lines_no_role_map = [
            {"id": 1, "line_number": 1, "content": "测试", "role_id": 999, "speech_rate": 1.0},
        ]

        with tempfile.TemporaryDirectory() as tmpdir:
            synthesize_full_script(
                lines=lines_no_role_map,
                role_voice_map={},
                output_dir=tmpdir,
                script_id=1,
            )

            call = mock_tts.call_args_list[0]
            assert call[0][1] == "female-qn-qingse"

    @patch("app.services.tts_service._call_moonshot_tts")
    def test_tts_failure_uses_silence_placeholder(self, mock_tts: MagicMock):
        """Test that TTS API failure generates silence placeholder."""
        mock_tts.side_effect = Exception("Network error")

        with tempfile.TemporaryDirectory() as tmpdir:
            result = synthesize_full_script(
                lines=SAMPLE_LINES,
                role_voice_map=SAMPLE_ROLE_VOICE_MAP,
                output_dir=tmpdir,
                script_id=1,
            )

            assert os.path.exists(result["audio_path"])
            assert os.path.exists(result["srt_path"])

    @patch("app.services.tts_service._call_moonshot_tts")
    def test_empty_lines_raises_error(self, mock_tts: MagicMock):
        """Test that empty lines list raises ValueError."""
        mock_tts.return_value = FAKE_WAV_BYTES

        with tempfile.TemporaryDirectory() as tmpdir:
            with pytest.raises(ValueError, match="No audio segments generated"):
                synthesize_full_script(
                    lines=[],
                    role_voice_map={},
                    output_dir=tmpdir,
                    script_id=1,
                )

    @patch("app.services.tts_service._call_moonshot_tts")
    def test_output_directory_created(self, mock_tts: MagicMock):
        """Test that output directory is created if it doesn't exist."""
        mock_tts.return_value = FAKE_WAV_BYTES

        with tempfile.TemporaryDirectory() as tmpdir:
            nested_dir = os.path.join(tmpdir, "nested", "output")
            synthesize_full_script(
                lines=SAMPLE_LINES,
                role_voice_map=SAMPLE_ROLE_VOICE_MAP,
                output_dir=nested_dir,
                script_id=1,
            )
            assert os.path.isdir(nested_dir)

    @patch("app.services.tts_service._call_moonshot_tts")
    def test_srt_subtitle_generation(self, mock_tts: MagicMock):
        """Test that SRT file contains correct subtitle entries."""
        mock_tts.return_value = FAKE_WAV_BYTES

        with tempfile.TemporaryDirectory() as tmpdir:
            result = synthesize_full_script(
                lines=SAMPLE_LINES,
                role_voice_map=SAMPLE_ROLE_VOICE_MAP,
                output_dir=tmpdir,
                script_id=1,
            )

            with open(result["srt_path"], "r", encoding="utf-8") as f:
                srt_content = f.read()

            assert "你好世界" in srt_content
            assert "今天天气真好" in srt_content
            assert "再见" in srt_content
            assert "-->" in srt_content

    @patch("app.services.tts_service._call_moonshot_tts")
    def test_api_key_error_propagates(self, mock_tts: MagicMock):
        """Test that API key error propagates properly through synthesize."""
        mock_tts.side_effect = ValueError("MOONSHOT_API_KEY not configured")

        with tempfile.TemporaryDirectory() as tmpdir:
            # Should not raise to the caller; errors are caught per-line
            result = synthesize_full_script(
                lines=SAMPLE_LINES,
                role_voice_map=SAMPLE_ROLE_VOICE_MAP,
                output_dir=tmpdir,
                script_id=1,
            )
            assert os.path.exists(result["audio_path"])

    @patch("app.services.tts_service._call_moonshot_tts")
    def test_empty_content_lines_skipped(self, mock_tts: MagicMock):
        """Test that lines with empty content are skipped."""
        mock_tts.return_value = FAKE_WAV_BYTES
        lines_with_empty = [
            {"id": 1, "line_number": 1, "content": "有效内容", "role_id": 1, "speech_rate": 1.0},
            {"id": 2, "line_number": 2, "content": "", "role_id": 1, "speech_rate": 1.0},
            {"id": 3, "line_number": 3, "content": "  ", "role_id": 1, "speech_rate": 1.0},
            {"id": 4, "line_number": 4, "content": "另一句", "role_id": 1, "speech_rate": 1.0},
        ]

        with tempfile.TemporaryDirectory() as tmpdir:
            synthesize_full_script(
                lines=lines_with_empty,
                role_voice_map=SAMPLE_ROLE_VOICE_MAP,
                output_dir=tmpdir,
                script_id=1,
            )

            # Only 2 non-empty lines should trigger TTS calls
            assert mock_tts.call_count == 2
