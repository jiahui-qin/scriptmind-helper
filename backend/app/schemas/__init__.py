"""Pydantic schemas package."""
from app.schemas.script import ScriptBase, ScriptCreate, ScriptResponse, ScriptAnalysisResponse
from app.schemas.role import RoleBase, RoleCreate, RoleResponse, RoleAnalysis
from app.schemas.line import LineBase, LineCreate, LineResponse, LineWithEmotion, LineUpdate, LineBatchUpdate
from app.schemas.tts_task import TTSTaskBase, TTSTaskCreate, TTSTaskResponse, TTSTaskStatus

__all__ = [
    "ScriptBase", "ScriptCreate", "ScriptResponse", "ScriptAnalysisResponse",
    "RoleBase", "RoleCreate", "RoleResponse", "RoleAnalysis",
    "LineBase", "LineCreate", "LineResponse", "LineWithEmotion", "LineUpdate", "LineBatchUpdate",
    "TTSTaskBase", "TTSTaskCreate", "TTSTaskResponse", "TTSTaskStatus"
]
