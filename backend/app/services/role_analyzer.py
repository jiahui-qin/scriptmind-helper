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

请分析每个角色的：name(姓名), gender(男/女/未知), age(整数), voice_type(音色推荐如温婉/沉稳/活泼等), personality(性格特征), description(详细描述)。

只输出 JSON，格式：
{{"roles": [{{"name": "角色名", "gender": "男", "age": 25, "voice_type": "温婉", "personality": "温柔善良", "description": "详细描述..."}}]}}"""

    client = _get_client()
    resp = client.chat.completions.create(
        model=settings.MIMO_CHAT_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        response_format={"type": "json_object"},
        temperature=0.3,
        max_completion_tokens=4096,
    )
    content = resp.choices[0].message.content
    result = json.loads(content)
    return result.get("roles", [])
