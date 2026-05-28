"""Tests for role_analyzer service — mock MiMo API calls."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import pytest
from unittest.mock import patch, MagicMock
from app.services.role_analyzer import analyze_roles, RoleProfile, RoleAnalysisResponse


MOCK_LLM_RESPONSE = json.dumps({
    "roles": [
        {
            "name": "张三",
            "gender": "男",
            "age": 28,
            "voice_type": "青年男声",
            "personality": "热血,正义,冲动",
            "description": "主角，年轻有为的侠客"
        },
        {
            "name": "李四",
            "gender": "女",
            "age": 25,
            "voice_type": "清脆女声",
            "personality": "聪慧,冷静,温柔",
            "description": "女主角，医者"
        }
    ]
})


SAMPLE_SCRIPT = """张三：今天天气真好。
李四：是啊，我们去爬山吧。
张三：好主意！
李四：不过在去之前要先准备干粮。"""

SAMPLE_ROLE_NAMES = ["张三", "李四"]


class TestAnalyzeRoles:
    """Tests for analyze_roles function with mocked MiMo API."""

    @patch("app.services.role_analyzer._call_mimo_chat")
    def test_basic_role_analysis(self, mock_call: MagicMock):
        """Test that analyze_roles returns parsed role profiles."""
        mock_call.return_value = MOCK_LLM_RESPONSE
        result = analyze_roles(SAMPLE_SCRIPT, SAMPLE_ROLE_NAMES)

        assert len(result) == 2
        assert result[0]["name"] == "张三"
        assert result[0]["gender"] == "男"
        assert result[0]["age"] == 28
        assert result[0]["voice_type"] == "青年男声"
        assert result[1]["name"] == "李四"
        assert result[1]["gender"] == "女"
        assert result[1]["age"] == 25

    @patch("app.services.role_analyzer._call_mimo_chat")
    def test_prompt_includes_role_names(self, mock_call: MagicMock):
        """Test that the prompt sent to LLM includes role names."""
        mock_call.return_value = MOCK_LLM_RESPONSE
        analyze_roles(SAMPLE_SCRIPT, SAMPLE_ROLE_NAMES)

        call_args = mock_call.call_args
        user_prompt = call_args[0][1]
        assert "张三" in user_prompt
        assert "李四" in user_prompt

    @patch("app.services.role_analyzer._call_mimo_chat")
    def test_llm_response_with_markdown_fences(self, mock_call: MagicMock):
        """Test parsing when LLM response includes markdown code fences."""
        mock_call.return_value = "```json\n" + MOCK_LLM_RESPONSE + "\n```"
        result = analyze_roles(SAMPLE_SCRIPT, SAMPLE_ROLE_NAMES)
        assert len(result) == 2
        assert result[0]["name"] == "张三"

    @patch("app.services.role_analyzer._call_mimo_chat")
    def test_api_key_missing_raises_error(self, mock_call: MagicMock):
        """Test that missing API key raises ValueError."""
        mock_call.side_effect = ValueError(
            "MOONSHOT_API_KEY not configured. Please set it in .env or config page."
        )
        with pytest.raises(ValueError, match="MOONSHOT_API_KEY not configured"):
            analyze_roles(SAMPLE_SCRIPT, SAMPLE_ROLE_NAMES)

    @patch("app.services.role_analyzer._call_mimo_chat")
    def test_empty_script(self, mock_call: MagicMock):
        """Test analyzing an empty script returns empty roles list."""
        mock_call.return_value = json.dumps({"roles": []})
        result = analyze_roles("", [])
        assert result == []

    @patch("app.services.role_analyzer._call_mimo_chat")
    def test_empty_role_names(self, mock_call: MagicMock):
        """Test analyzing with empty role names list."""
        mock_call.return_value = MOCK_LLM_RESPONSE
        result = analyze_roles(SAMPLE_SCRIPT, [])
        assert len(result) == 2

    @patch("app.services.role_analyzer._call_mimo_chat")
    def test_malformed_json_with_fallback(self, mock_call: MagicMock):
        """Test that malformed JSON with extractable object uses fallback parsing."""
        mock_call.return_value = 'Some prefix text {"roles": [{"name": "张三","gender": "男","age": 20,"voice_type": "青年男声","personality": "勇敢","description": "主角"}]} some suffix'
        result = analyze_roles(SAMPLE_SCRIPT, SAMPLE_ROLE_NAMES)
        assert len(result) == 1
        assert result[0]["name"] == "张三"

    @patch("app.services.role_analyzer._call_mimo_chat")
    def test_completely_invalid_response_raises_error(self, mock_call: MagicMock):
        """Test that completely invalid LLM response raises ValueError."""
        mock_call.return_value = "This is not JSON at all, just random text without any braces."
        with pytest.raises(ValueError, match="Failed to parse LLM response"):
            analyze_roles(SAMPLE_SCRIPT, SAMPLE_ROLE_NAMES)

    @patch("app.services.role_analyzer._call_mimo_chat")
    def test_single_role_analysis(self, mock_call: MagicMock):
        """Test analyzing a script with a single role."""
        single_role_response = json.dumps({
            "roles": [
                {
                    "name": "旁白",
                    "gender": "未知",
                    "age": 0,
                    "voice_type": "中性旁白",
                    "personality": "客观,沉稳",
                    "description": "故事叙述者"
                }
            ]
        })
        mock_call.return_value = single_role_response
        result = analyze_roles("旁白：很久很久以前...", ["旁白"])
        assert len(result) == 1
        assert result[0]["name"] == "旁白"

    @patch("app.services.role_analyzer._call_mimo_chat")
    def test_validation_error_with_fallback(self, mock_call: MagicMock):
        """Test that validation error (missing field) triggers fallback JSON extraction."""
        # Send a response that is valid JSON but fails Pydantic validation (missing fields),
        # wrapped with extra text so regex fallback kicks in
        mock_call.return_value = (
            'Some introductory text.\n'
            '{"roles": [{"name": "张三","gender": "男","age": 20,'
            '"voice_type": "青年","personality": "勇敢","description": "主角"}]}\n'
            'Some trailing explanation.'
        )
        result = analyze_roles(SAMPLE_SCRIPT, SAMPLE_ROLE_NAMES)
        assert len(result) == 1
        assert result[0]["name"] == "张三"


class TestRoleProfileModel:
    """Tests for RoleProfile Pydantic model."""

    def test_role_profile_defaults(self):
        """Test RoleProfile default values."""
        rp = RoleProfile(name="Test")
        assert rp.gender == "未知"
        assert rp.age == 0
        assert rp.voice_type == "未知"
        assert rp.personality == ""
        assert rp.description == ""

    def test_role_profile_full(self):
        """Test RoleProfile with all fields set."""
        rp = RoleProfile(
            name="主角",
            gender="男",
            age=30,
            voice_type="青年男声",
            personality="勇敢,正直",
            description="主角描述"
        )
        assert rp.name == "主角"
        assert rp.gender == "男"
        assert rp.age == 30


class TestRoleAnalysisResponse:
    """Tests for RoleAnalysisResponse Pydantic model."""

    def test_valid_response(self):
        """Test that valid JSON validates correctly."""
        data = {
            "roles": [
                {"name": "A", "gender": "男", "age": 20, "voice_type": "x", "personality": "p", "description": "d"}
            ]
        }
        parsed = RoleAnalysisResponse(**data)
        assert len(parsed.roles) == 1

    def test_empty_roles(self):
        """Test that empty roles list is valid."""
        parsed = RoleAnalysisResponse(roles=[])
        assert parsed.roles == []
