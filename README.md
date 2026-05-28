# ScriptMind Helper

台本智能分析助手 - 上传台本，AI 分析角色性格，生成 TTS 语音

## 技术栈

- 前端：React + Vite + MUI + Tailwind CSS
- 后端：FastAPI + SQLite
- AI：MiMo API（角色分析 + 情感标注）
- TTS：MiMo TTS v2.5

## 快速开始

```bash
# 后端
cd backend && pip install -r requirements.txt && uvicorn app.main:app --reload

# 前端
cd frontend && npm install && npm run dev
```

## 项目结构

```
scriptmind-helper/
├── backend/          # FastAPI 后端
├── frontend/         # React 前端
├── docs/            # 设计文档
└── README.md
```

