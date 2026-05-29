"""Call MiMo (Xiaomi) API for role personality analysis via OpenAI SDK."""
import json
from typing import List, Dict, Any
from openai import OpenAI
from app.config import settings


def _get_client() -> OpenAI:
    return OpenAI(api_key=settings.MIMO_API_KEY, base_url=settings.MIMO_API_BASE)


SYSTEM_PROMPT = """你是一个专业的台本/剧本角色分析专家。
用户会提供一段台本文本，请识别出所有角色，并分析每个角色的性格特征。
输出严格符合 JSON，不要输出任何其他内容。"""


def analyze_roles(script_content: str, role_names: List[str]) -> List[Dict[str, Any]]:
    """Send entire script to MiMo LLM for role analysis."""
    if not settings.MIMO_API_KEY:
        raise ValueError("MIMO_API_KEY not configured")

    user_prompt = f"""台本内容如下：
{script_content}

已识别到的角色名：{", ".join(role_names)}

请分析每个角色的：
- name(姓名)
- gender(男/女/未知)
- age(整数)
- voice_type(音色推荐如温婉/沉稳/活泼等)
- personality(性格特征)
- description(详细描述)
- tone_style: 整体语调（可选：温柔/高冷/活泼/严肃/慵懒/俏皮/深沉/干练/凌厉，或null）
- voice_color: 音色定位（可选：磁性/醇厚/清亮/空灵/稚嫩/苍老/甜美/沙哑/醇雅，或null）
- persona_accent: 人设腔调（可选：夹子音/御姐音/正太音/大叔音/台湾腔，或null）
- dialect: 方言（可选：东北话/四川话/河南话/粤语，或null）
- roleplay: 角色扮演（可选：孙悟空/林黛玉，或null）
- singing: 唱歌风格（可选：唱歌，或null）

只输出 JSON，格式：
{{"roles": [{{"name": "角色名", "gender": "男", "age": 25, "voice_type": "温婉", "personality": "温柔善良", "description": "详细描述...", "tone_style": null, "voice_color": null, "persona_accent": null, "dialect": null, "roleplay": null, "singing": null}}]}}"""

    client = _get_client()
    resp = client.chat.completions.create(
        model=settings.MIMO_CHAT_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "role_analysis",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "roles": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "name": {"type": "string", "description": "角色名称"},
                                    "gender": {"type": "string", "enum": ["男", "女", "未知"]},
                                    "age": {"type": "integer", "minimum": 0, "maximum": 120},
                                    "voice_type": {"type": "string", "description": "音色推荐"},
                                    "personality": {"type": "string", "description": "性格特征"},
                                    "description": {"type": "string", "description": "详细描述"},
                                    "tone_style": {"anyOf": [{"type": "string", "enum": ["温柔", "高冷", "活泼", "严肃", "慵懒", "俏皮", "深沉", "干练", "凌厉"]}, {"type": "null"}]},
                                    "voice_color": {"anyOf": [{"type": "string", "enum": ["磁性", "醇厚", "清亮", "空灵", "稚嫩", "苍老", "甜美", "沙哑", "醇雅"]}, {"type": "null"}]},
                                    "persona_accent": {"anyOf": [{"type": "string", "enum": ["夹子音", "御姐音", "正太音", "大叔音", "台湾腔"]}, {"type": "null"}]},
                                    "dialect": {"anyOf": [{"type": "string", "enum": ["东北话", "四川话", "河南话", "粤语"]}, {"type": "null"}]},
                                    "roleplay": {"anyOf": [{"type": "string", "enum": ["孙悟空", "林黛玉"]}, {"type": "null"}]},
                                    "singing": {"anyOf": [{"type": "string", "enum": ["唱歌"]}, {"type": "null"}]},
                                },
                                "required": ["name", "gender", "age", "voice_type", "personality", "description"],
                                "additionalProperties": False,
                            },
                        },
                    },
                    "required": ["roles"],
                    "additionalProperties": False,
                },
            },
        },
        temperature=0.3,
        max_completion_tokens=4096,
    )
    content = resp.choices[0].message.content
    result = json.loads(content)
    return result.get("roles", [])
