"""Styles API endpoints for style presets and built-in options."""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.style_preset import StylePreset

router = APIRouter()

# Built-in preset values per category
PRESETS = {
    "emotion_tag": ["平静", "开心", "悲伤", "愤怒", "恐惧", "惊讶", "兴奋", "委屈", "冷漠"],
    "complex_emotion": ["怅然", "欣慰", "无奈", "愧疚", "释然", "嫉妒", "厌倦", "忐忑", "动情"],
    "tone_style": ["温柔", "高冷", "活泼", "严肃", "慵懒", "俏皮", "深沉", "干练", "凌厉"],
    "voice_color": ["磁性", "醇厚", "清亮", "空灵", "稚嫩", "苍老", "甜美", "沙哑", "醇雅"],
    "persona_accent": ["夹子音", "御姐音", "正太音", "大叔音", "台湾腔"],
    "dialect": ["普通话", "东北话", "四川话", "河南话", "粤语"],
    "roleplay": ["无", "孙悟空", "林黛玉"],
    "singing": ["无", "唱歌"],
}


@router.get("/{category}")
async def get_styles(category: str, db: Session = Depends(get_db)):
    """Get all style options for a category (built-in + custom)."""
    builtin = PRESETS.get(category, [])
    customs = db.query(StylePreset).filter(StylePreset.category == category).all()
    custom_values = [s.value for s in customs]
    return {
        "category": category,
        "builtin": builtin,
        "custom": custom_values,
        "all": builtin + custom_values,
    }


@router.post("/")
async def add_style(
    category: str = Query(...),
    value: str = Query(...),
    db: Session = Depends(get_db),
):
    """Add a custom style preset value."""
    existing = db.query(StylePreset).filter(
        StylePreset.category == category,
        StylePreset.value == value,
    ).first()
    if existing:
        return {"id": existing.id, "category": existing.category, "value": existing.value}
    p = StylePreset(category=category, value=value)
    db.add(p)
    db.commit()
    db.refresh(p)
    return {"id": p.id, "category": p.category, "value": p.value}
