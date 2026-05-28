"""Call MiMo LLM API for role personality analysis."""
import json
import re
import os
from typing import List, Dict, Any
from pydantic import BaseModel, ValidationError
from app.config import settings


class RoleProfile(BaseModel):
    name: str
    gender: str = "未知"
    age: int = 0
    voice_type: str = "未知"
    personality: str = ""
    description: str = ""


class RoleAnalysisResponse(BaseModel):
    roles: List[RoleProfile]


SYSTEM_PROMPT = """你是一个专业的台本/剧本角色分析专家。
用户会提供一段台本文本，请识别出所有角色，并分析每个角色的性格特征。
输出严格符合 JSON Schema，不要输出任何其他内容。"""


def _call_mimo_chat(system: str, user: str) -> str:
    """Call MiMo chat completions API with JSON object response format."""
    import requests
    if not settings.MOONSHOT_API_KEY:
        raise ValueError("MOONSHOT_API_KEY not configured. Please set it in .env or config page.")
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


def analyze_roles(script_content: str, role_names: List[str]) -> List[Dict[str, Any]]:
    """
    Send entire script to MiMo LLM for role analysis.
    Returns list of dicts matching RoleProfile schema.
    """
    user_prompt = f"""台本内容如下：
{script_content}

已识别到的角色名：{", ".join(role_names)}

请分析每个角色的性格特征，输出 JSON，格式如下：
{{
  "roles": [
    {{
      "name": "角色名（必须与输入一致）",
      "gender": "男/女/未知",
      "age": 25,
      "voice_type": "适合的音色描述（如：青年男声、沉稳女声等）",
      "personality": "性格特征关键词，用逗号分隔",
      "description": "角色简要描述"
    }}
  ]
}}

只输出 JSON，不要输出其他内容。"""
    raw = _call_mimo_chat(SYSTEM_PROMPT, user_prompt)
    # Strip markdown code fences if present
    cleaned = re.sub(r"^```json\s*|\s*```$", "", raw.strip(), flags=re.MULTILINE).strip()
    try:
        parsed = json.loads(cleaned)
        validated = RoleAnalysisResponse(**parsed)
        return [r.model_dump() for r in validated.roles]
    except (json.JSONDecodeError, ValidationError) as e:
        # Fallback: try to extract JSON from raw text
        match = re.search(r"\{.*\}", raw, re.DOTALL)
        if match:
            parsed = json.loads(match.group())
            validated = RoleAnalysisResponse(**parsed)
            return [r.model_dump() for r in validated.roles]
        raise ValueError(f"Failed to parse LLM response: {e}\nRaw: {raw[:500]}")
