"""Lines API endpoints for updating line properties."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.line import Line
from app.schemas.line import LineUpdate, LineBatchUpdate

router = APIRouter()


@router.put("/{line_id}")
async def update_line(line_id: int, body: LineUpdate, db: Session = Depends(get_db)):
    """Update a single line's properties."""
    line = db.query(Line).filter(Line.id == line_id).first()
    if not line:
        raise HTTPException(status_code=404, detail="Line not found")
    if body.role_id is not None:
        line.role_id = body.role_id
    if body.emotion_tag is not None:
        line.emotion_tag = body.emotion_tag
    if body.complex_emotion is not None:
        line.complex_emotion = body.complex_emotion
    if body.emotion_intensity is not None:
        line.emotion_intensity = body.emotion_intensity
    db.commit()
    db.refresh(line)
    return {
        "id": line.id,
        "line_number": line.line_number,
        "role_id": line.role_id,
        "emotion_tag": line.emotion_tag,
        "complex_emotion": line.complex_emotion,
        "emotion_intensity": line.emotion_intensity,
    }


@router.post("/batch")
async def batch_update_lines(body: LineBatchUpdate, db: Session = Depends(get_db)):
    """Batch update lines by IDs or by role in a script."""
    if body.mode == "by_ids":
        if not body.line_ids:
            raise HTTPException(status_code=400, detail="line_ids required for by_ids mode")
        lines = db.query(Line).filter(Line.id.in_(body.line_ids)).all()
    elif body.mode == "by_role":
        if not body.script_id:
            raise HTTPException(status_code=400, detail="script_id required for by_role mode")
        lines = db.query(Line).filter(
            Line.script_id == body.script_id,
            Line.role_id == body.from_role_id,
        ).all()
    else:
        raise HTTPException(status_code=400, detail="Invalid mode")

    count = 0
    for line in lines:
        changed = False
        u = body.updates
        if u.role_id is not None:
            line.role_id = u.role_id
            changed = True
        if u.emotion_tag is not None:
            line.emotion_tag = u.emotion_tag
            changed = True
        if u.complex_emotion is not None:
            line.complex_emotion = u.complex_emotion
            changed = True
        if u.emotion_intensity is not None:
            line.emotion_intensity = u.emotion_intensity
            changed = True
        if changed:
            count += 1
    db.commit()
    return {"updated_count": count}
