"""Script file parser — extract lines and roles from .txt script content."""
import re
from typing import List, Dict, Optional

LINE_PATTERN = re.compile(
    r'^(?:\s*(\d+)[\.\s、]\s*)?'          # line number (optional)
    r'(?:【?([^】:\n]+)】?\s*[:：]\s*)?'  # role name (optional)
    r'(.*)$',                                 # content
    re.MULTILINE | re.IGNORECASE
)

def parse_script_content(content: str) -> List[Dict]:
    """Parse raw script text into structured line dicts.
    
    Returns list of {role, content, line_number, raw}
    """
    lines: List[Dict] = []
    line_num = 0
    for raw_line in content.split('\n'):
        stripped = raw_line.strip()
        if not stripped:
            continue
        line_num += 1
        match = LINE_PATTERN.match(stripped)
        if match:
            _, role_raw, content_raw = match.groups()
            role = role_raw.strip() if role_raw else None
            text = content_raw.strip() if content_raw else stripped
        else:
            role = None
            text = stripped
        lines.append({
            'line_number': line_num,
            'role': role,
            'content': text,
            'raw': stripped,
        })
    return lines


def extract_roles(lines_dict: List[Dict]) -> List[str]:
    """Extract unique role names from parsed lines."""
    roles = set()
    for ld in lines_dict:
        if ld.get('role'):
            roles.add(ld['role'])
    return list(roles)


def detect_script_sections(content: str) -> Dict[str, str]:
    """Detect major sections: 人物介绍, 场景, 对话 etc."""
    sections: Dict[str, str] = {}
    current = 'default'
    for line in content.split('\n'):
        stripped = line.strip()
        if not stripped:
            continue
        # Detect section headers
        if re.match(r'^[一二三四五六七八九十]+[、\.、]', stripped):
            current = stripped[:20]
        if current not in sections:
            sections[current] = ''
        sections[current] += line + '\n'
    return sections
