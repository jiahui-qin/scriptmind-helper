"""Tests for file_parser service — no external API calls needed."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from app.services.file_parser import parse_script_content, extract_roles, detect_script_sections


class TestParseScriptContent:
    """Tests for parse_script_content function."""

    def test_standard_role_line_format(self):
        """Test parsing lines with standard 角色名：台词 format."""
        content = "张三：大家好，我是张三。\n李四：你好张三！"
        result = parse_script_content(content)
        assert len(result) == 2
        assert result[0]['role'] == '张三'
        assert result[0]['content'] == '大家好，我是张三。'
        assert result[0]['line_number'] == 1
        assert result[1]['role'] == '李四'
        assert result[1]['content'] == '你好张三！'
        assert result[1]['line_number'] == 2

    def test_colon_separator_english(self):
        """Test parsing with English colon separator."""
        content = "Alice: Hello everyone.\nBob: Hi Alice!"
        result = parse_script_content(content)
        assert len(result) == 2
        assert result[0]['role'] == 'Alice'
        assert result[0]['content'] == 'Hello everyone.'
        assert result[1]['role'] == 'Bob'
        assert result[1]['content'] == 'Hi Alice!'

    def test_bracket_role_format(self):
        """Test parsing with 【角色名】 bracket format."""
        content = "【张三】：今天天气真好。\n【李四】：是啊。"
        result = parse_script_content(content)
        assert len(result) == 2
        assert result[0]['role'] == '张三'
        assert result[0]['content'] == '今天天气真好。'
        assert result[1]['role'] == '李四'
        assert result[1]['content'] == '是啊。'

    def test_narration_no_role(self):
        """Test lines with no role prefix (narration/stage directions)."""
        content = "（幕启，灯光渐亮）\n张三：开始吧。"
        result = parse_script_content(content)
        assert len(result) == 2
        assert result[0]['role'] is None
        assert result[0]['content'] == '（幕启，灯光渐亮）'
        assert result[1]['role'] == '张三'
        assert result[1]['content'] == '开始吧。'

    def test_empty_lines_skipped(self):
        """Test that blank lines are skipped."""
        content = "张三：第一句\n\n\n李四：第二句"
        result = parse_script_content(content)
        assert len(result) == 2
        assert result[0]['line_number'] == 1
        assert result[1]['line_number'] == 2

    def test_line_number_preserved(self):
        """Test that line numbers are sequential and correct."""
        content = "A：行1\n\nB：行2\nC：行3"
        result = parse_script_content(content)
        assert len(result) == 3
        assert [r['line_number'] for r in result] == [1, 2, 3]

    def test_raw_field_preserved(self):
        """Test that the raw field stores original line text."""
        content = "张三：你好"
        result = parse_script_content(content)
        assert result[0]['raw'] == '张三：你好'

    def test_numbered_line_with_role(self):
        """Test parsing numbered lines like '1. 张三：台词'."""
        content = "1. 张三：第一句台词\n2. 李四：第二句台词"
        result = parse_script_content(content)
        assert len(result) == 2
        assert result[0]['role'] == '张三'
        assert result[0]['content'] == '第一句台词'
        assert result[1]['role'] == '李四'
        assert result[1]['content'] == '第二句台词'

    def test_empty_input(self):
        """Test empty content returns empty list."""
        result = parse_script_content("")
        assert result == []

    def test_whitespace_only_input(self):
        """Test whitespace-only content returns empty list."""
        result = parse_script_content("   \n  \n   ")
        assert result == []

    def test_role_with_special_characters(self):
        """Test role names with special characters."""
        content = "角色A-1：台词内容"
        result = parse_script_content(content)
        assert result[0]['role'] == '角色A-1'
        assert result[0]['content'] == '台词内容'


class TestExtractRoles:
    """Tests for extract_roles function."""

    def test_extract_unique_roles(self):
        """Test extracting unique role names from parsed lines."""
        lines = [
            {'line_number': 1, 'role': '张三', 'content': '你好'},
            {'line_number': 2, 'role': '李四', 'content': '你好'},
            {'line_number': 3, 'role': '张三', 'content': '再见'},
        ]
        roles = extract_roles(lines)
        assert sorted(roles) == ['张三', '李四']

    def test_extract_roles_skips_none(self):
        """Test that None roles (narration) are skipped."""
        lines = [
            {'line_number': 1, 'role': '张三', 'content': '你好'},
            {'line_number': 2, 'role': None, 'content': '旁白'},
            {'line_number': 3, 'role': '李四', 'content': '你好'},
        ]
        roles = extract_roles(lines)
        assert sorted(roles) == ['张三', '李四']

    def test_extract_roles_empty_list(self):
        """Test empty lines list returns empty role list."""
        roles = extract_roles([])
        assert roles == []

    def test_extract_roles_all_narration(self):
        """Test all narration lines returns empty role list."""
        lines = [
            {'line_number': 1, 'role': None, 'content': '旁白1'},
            {'line_number': 2, 'role': None, 'content': '旁白2'},
        ]
        roles = extract_roles(lines)
        assert roles == []

    def test_extract_roles_missing_role_key(self):
        """Test lines without role key are handled gracefully."""
        lines = [
            {'line_number': 1, 'content': '无角色键'},
        ]
        roles = extract_roles(lines)
        assert roles == []


class TestDetectScriptSections:
    """Tests for detect_script_sections function."""

    def test_detect_chinese_numbered_sections(self):
        """Test detecting sections with Chinese numbered headers."""
        content = "一、人物介绍\n张三：主角\n李四：配角\n二、第一幕\n张三：开始吧"
        sections = detect_script_sections(content)
        assert len(sections) > 1
        assert '一、人物介绍' in sections or any('一' in k for k in sections)

    def test_single_section_default(self):
        """Test content without section headers gets default section."""
        content = "张三：你好\n李四：你好"
        sections = detect_script_sections(content)
        assert 'default' in sections

    def test_empty_content(self):
        """Test empty content returns empty sections dict."""
        sections = detect_script_sections("")
        assert sections == {}
