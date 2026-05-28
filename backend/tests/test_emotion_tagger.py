"""Tests for emotion_tagger service — mock MiMo API calls."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import pytest
from unittest.mock import patch, MagicMock
from app.services.emotion_tagger import tag_emotions


MOCK_EMOTION_RESPONSE = json.dumps([
    {"line_number": 1, "emotion_tag": "喜悦", "tone": "欢快", "speech_rate": 1.2, "emotion_intensity": 0.8},
    {"line_number": 2, "emotion_tag": "平静", "tone": "温和", "speech_rate": 1.0, "emotion_intensity": 0.5},
    {"line_number": 3, "emotion_tag": "愤怒", "tone": "激昂", "speech_rate": 1.5, "emotion_intensity": 0.9},
])


SAMPLE_LINES = [
    {"line_number": 1, "role": "张三", "content": "今天天气真好！"},
    {"line_number": 2, "role": "李四", "content": "是啊，很适合出游。"},
    {"line_number": 3, "role": "张三", "content": "太过分了！"},
]

SAMPLE_ROLES = [
    {"name": "张三", "gender": "男"},
    {"name": "李四", "gender": "女"},
]


class TestTagEmotions:
    """Tests for tag_emotions function with mocked MiMo API."""

    @patch("app.services.emotion_tagger._call_mimo_chat")
    def test_basic_emotion_tagging(self, mock_call: MagicMock):
        """Test that emotion tags are correctly assigned to lines."""
        mock_call.return_value = MOCK_EMOTION_RESPONSE
        result = tag_emotions("dummy content", SAMPLE_LINES, SAMPLE_ROLES)

        assert len(result) == 3
        assert result[0]["emotion_tag"] == "喜悦"
        assert result[0]["tone"] == "欢快"
        assert result[0]["speech_rate"] == 1.2
        assert result[0]["emotion_intensity"] == 0.8

        assert result[1]["emotion_tag"] == "平静"
        assert result[1]["tone"] == "温和"

        assert result[2]["emotion_tag"] == "愤怒"
        assert result[2]["tone"] == "激昂"

    @patch("app.services.emotion_tagger._call_mimo_chat")
    def test_prompt_includes_role_names(self, mock_call: MagicMock):
        """Test that the prompt includes role names."""
        mock_call.return_value = MOCK_EMOTION_RESPONSE
        tag_emotions("dummy", SAMPLE_LINES, SAMPLE_ROLES)

        call_args = mock_call.call_args
        user_prompt = call_args[0][1]
        assert "张三" in user_prompt
        assert "李四" in user_prompt

    @patch("app.services.emotion_tagger._call_mimo_chat")
    def test_missing_line_number_gets_defaults(self, mock_call: MagicMock):
        """Test that lines not in LLM response get default emotion values."""
        mock_call.return_value = json.dumps([
            {"line_number": 1, "emotion_tag": "喜悦", "tone": "欢快", "speech_rate": 1.2, "emotion_intensity": 0.8},
        ])
        result = tag_emotions("dummy", SAMPLE_LINES, SAMPLE_ROLES)

        assert result[0]["emotion_tag"] == "喜悦"
        assert result[1]["emotion_tag"] == "中性"
        assert result[1]["tone"] == ""
        assert result[1]["speech_rate"] == 1.0
        assert result[1]["emotion_intensity"] == 0.5
        assert result[2]["emotion_tag"] == "中性"

    @patch("app.services.emotion_tagger._call_mimo_chat")
    def test_api_key_missing_raises_error(self, mock_call: MagicMock):
        """Test that missing API key raises ValueError."""
        mock_call.side_effect = ValueError("MOONSHOT_API_KEY not configured.")
        with pytest.raises(ValueError, match="MOONSHOT_API_KEY not configured"):
            tag_emotions("dummy", SAMPLE_LINES, SAMPLE_ROLES)

    @patch("app.services.emotion_tagger._call_mimo_chat")
    def test_empty_lines_list(self, mock_call: MagicMock):
        """Test that empty lines list returns empty list."""
        mock_call.return_value = "[]"
        result = tag_emotions("dummy", [], [])
        assert result == []

    @patch("app.services.emotion_tagger._call_mimo_chat")
    def test_response_with_markdown_fences(self, mock_call: MagicMock):
        """Test parsing when response includes markdown code fences."""
        mock_call.return_value = "```json\n" + MOCK_EMOTION_RESPONSE + "\n```"
        result = tag_emotions("dummy", SAMPLE_LINES, SAMPLE_ROLES)
        assert len(result) == 3
        assert result[0]["emotion_tag"] == "喜悦"

    @patch("app.services.emotion_tagger._call_mimo_chat")
    def test_malformed_json_with_fallback(self, mock_call: MagicMock):
        """Test that malformed JSON with extractable array uses fallback."""
        mock_call.return_value = 'prefix [{"line_number": 1, "emotion_tag": "悲伤", "tone": "低沉", "speech_rate": 0.8, "emotion_intensity": 0.7}] suffix'
        result = tag_emotions("dummy", SAMPLE_LINES[:1], SAMPLE_ROLES)
        assert result[0]["emotion_tag"] == "悲伤"

    @patch("app.services.emotion_tagger._call_mimo_chat")
    def test_lines_unaffected_by_tagging(self, mock_call: MagicMock):
        """Test that original line fields are preserved after tagging."""
        mock_call.return_value = MOCK_EMOTION_RESPONSE
        result = tag_emotions("dummy", SAMPLE_LINES, SAMPLE_ROLES)
        assert result[0]["line_number"] == 1
        assert result[0]["role"] == "张三"
        assert result[0]["content"] == "今天天气真好！"

    @patch("app.services.emotion_tagger._call_mimo_chat")
    def test_unparseable_response_raises_error(self, mock_call: MagicMock):
        """Test that completely unparseable response raises ValueError."""
        mock_call.return_value = "not json at all, no brackets either"
        with pytest.raises(ValueError, match="Failed to parse emotion response"):
            tag_emotions("dummy", SAMPLE_LINES, SAMPLE_ROLES)

    @patch("app.services.emotion_tagger._call_mimo_chat")
    def test_partial_emotion_fields_default(self, mock_call: MagicMock):
        """Test that missing emotion fields in response get defaults."""
        mock_call.return_value = json.dumps([
            {"line_number": 1, "emotion_tag": "喜悦"},
        ])
        result = tag_emotions("dummy", SAMPLE_LINES[:1], SAMPLE_ROLES)
        assert result[0]["emotion_tag"] == "喜悦"
        assert result[0]["tone"] == ""
        assert result[0]["speech_rate"] == 1.0
        assert result[0]["emotion_intensity"] == 0.5
