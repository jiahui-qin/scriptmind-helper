"""Call MiMo LLM API for emotion tagging per line."""
import json
import re
from typing import List, Dict, Any
from app.config import settings


EMOTION_SYSTEM = """你是一个专业的台本情感分析专家。
对每一句台词，给出最合适的情感标签、语气、语速和情绪强度。
输出严格符合 JSON Schema，不输出其他内容。"""


def _call_mimo_chat(system: str, user: str) -> str:
    import requests
    if not settings.MOONSHOT_API_KEY:
        raise ValueError("MOONSHOT_API_KEY not configured.")
    url = f"{settings.MIMO_API_BASE}/chat/completions"
    headers = {
        "Authorization": f"Bearer {settings.MOONSHOT_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "moonshot-v1-8k",
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "response_format": {"type": "json_object"},
        "temperature": 0.3,
    }
    resp = requests.post(url, headers=headers, json=payload, timeout=60)
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]


def tag_emotions(
    script_content: str,
    lines: List[Dict[str, Any]],
    roles: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """
    Send script + roles + lines to MiMo LLM for emotion tagging.
    Returns list of line dicts with emotion fields added.
    """
    # Build a compact representation of lines for the prompt
    lines_summary = "\n".join(
        f"{l['line_number']}. [{'无角色' if not l.get('role') else l['role']}] {l['content'][:80]}"
        for l in lines[:200]  # Limit to avoid token overflow
    )
    roles_summary = ", ".join(r["name"] for r in roles)

    user_prompt = f"""台本角色：{roles_summary}

台词列表（前200行）：
{lines_summary}

请为每一句台词标注情感信息，输出 JSON 数组，格式如下：
[
  {{
    "line_number": 1,
    "emotion_tag": "喜悦/悲伤/愤怒/平静/紧张/恐惧/厌恶/惊讶/中性（选一个）",
    "tone": "语气描述（如：轻柔、激昂、低沉等）",
    "speech_rate": 1.0,
    "emotion_intensity": 0.7
  }}
]

只输出 JSON 数组，不要输出其他内容。"""

    raw = _call_mimo_chat(EMOTION_SYSTEM, user_prompt)
    cleaned = re.sub(r"^```json\s*|\s*```$", "", raw.strip(), flags=re.MULTILINE).strip()
    try:
        tags = json.loads(cleaned)
    except json.JSONDecodeError:
        match = re.search(r"\[.*\]", raw, re.DOTALL)
        if match:
            tags = json.loads(match.group())
        else:
            raise ValueError(f"Failed to parse emotion response: {raw[:500]}")
    
    # Merge tags back into lines
    tag_map = {t["line_number"]: t for t in tags if "line_number" in t}
    for line in lines:
        t = tag_map.get(line["line_number"])
        if t:
            line["emotion_tag"] = t.get("emotion_tag", "中性")
            line["tone"] = t.get("tone", "")
            line["speech_rate"] = t.get("speech_rate", 1.0)
            line["emotion_intensity"] = t.get("emotion_intensity", 0.5)
        else:
            line["emotion_tag"] = "中性"
            line["tone"] = ""
            line["speech_rate"] = 1.0
            line["emotion_intensity"] = 0.5
    return lines
