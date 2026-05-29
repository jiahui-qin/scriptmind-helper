"""Call MiMo (Xiaomi) API for emotion tagging per line via OpenAI SDK."""
import json
from typing import List, Dict, Any
from openai import OpenAI
from app.config import settings


def _get_client() -> OpenAI:
    return OpenAI(api_key=settings.MIMO_API_KEY, base_url=settings.MIMO_API_BASE)


EMOTION_SYSTEM = """你是一个专业的台本情感分析专家。
对每一句台词，给出最合适的情感标签、语气、语速和情绪强度。
输出严格符合 JSON，不输出其他内容。"""


EMOTION_TAGS = ["开心", "悲伤", "愤怒", "惊讶", "中性", "恐惧", "厌恶", "感动", "疲惫", "严肃"]


def tag_emotions(
    script_content: str,
    lines: List[Dict],
    roles_data: List[Dict],
) -> List[Dict[str, Any]]:
    """Tag emotions for each line via MiMo LLM."""
    if not settings.MIMO_API_KEY:
        raise ValueError("MIMO_API_KEY not configured")

    lines_text = "\n".join(
        f"#{l['line_number']} [{l.get('role', '旁白')}] {l['content']}"
        for l in lines
    )

    user_prompt = f"""台本概要：
{script_content[:500]}

全部台词：
{lines_text}

情感标签可选：{", ".join(EMOTION_TAGS)}

为每句台词标注：
- line_number(整数)
- emotion_tag(情感标签)
- tone(语气如平静/激动/温和/严厉)
- speech_rate(语速0.5-2.0)
- emotion_intensity(强度0.0-1.0)
- complex_emotion: 复合情绪（可选：怅然/欣慰/无奈/愧疚/释然/嫉妒/厌倦/忐忑/动情，或其他复合情绪，或null）

只输出 JSON：
{{"tags": [{{"line_number": 1, "emotion_tag": "中性", "tone": "平静", "speech_rate": 1.0, "emotion_intensity": 0.5, "complex_emotion": null}}]}}"""

    client = _get_client()
    resp = client.chat.completions.create(
        model=settings.MIMO_CHAT_MODEL,
        messages=[
            {"role": "system", "content": EMOTION_SYSTEM},
            {"role": "user", "content": user_prompt},
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "emotion_tagging",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "tags": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "line_number": {"type": "integer", "minimum": 1},
                                    "emotion_tag": {"type": "string", "enum": ["开心", "悲伤", "愤怒", "惊讶", "中性", "恐惧", "厌恶", "感动", "疲惫", "严肃", "兴奋", "委屈", "平静", "冷漠"]},
                                    "tone": {"type": "string", "description": "语气"},
                                    "speech_rate": {"type": "number", "minimum": 0.5, "maximum": 2.0},
                                    "emotion_intensity": {"type": "number", "minimum": 0.0, "maximum": 1.0},
                                    "complex_emotion": {"anyOf": [{"type": "string", "enum": ["怅然", "欣慰", "无奈", "愧疚", "释然", "嫉妒", "厌倦", "忐忑", "动情"]}, {"type": "null"}]},
                                },
                                "required": ["line_number", "emotion_tag", "tone", "speech_rate", "emotion_intensity"],
                                "additionalProperties": False,
                            },
                        },
                    },
                    "required": ["tags"],
                    "additionalProperties": False,
                },
            },
        },
        temperature=0.3,
        max_completion_tokens=4096,
    )
    content = resp.choices[0].message.content
    result = json.loads(content)
    return result.get("tags", [])
