<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-0.115-009688?style=flat-square&logo=fastapi" alt="FastAPI">
  <img src="https://img.shields.io/badge/React-18-61DAFB?style=flat-square&logo=react" alt="React">
  <img src="https://img.shields.io/badge/TypeScript-5.6-3178C6?style=flat-square&logo=typescript" alt="TS">
  <img src="https://img.shields.io/badge/Tests-79%2F79-brightgreen?style=flat-square" alt="Tests">
  <img src="https://img.shields.io/badge/license-MIT-blue?style=flat-square" alt="License">
</p>

<h1 align="center">🎭 ScriptMind AI</h1>
<p align="center"><strong>AI 驱动的剧本角色分析与语音合成工具</strong></p>

---

## ✨ 功能特性

| 功能 | 描述 |
|------|------|
| 📄 **台本上传** | 拖拽上传 `.txt` 台本文件，支持 UTF-8 编码，最大 10MB |
| 🤖 **AI 角色分析** | 调用 MiMo (小米) `mimo-v2.5-pro` 大模型，自动识别角色并分析性格 |
| 💬 **情感标注** | 为每一句台词打上情感标签（开心/悲伤/愤怒/惊讶/中性等）和强度值 |
| 🎙️ **TTS 语音合成** | 调用 MiMo `mimo-v2.5-tts` 模型，支持 9 种音色，生成自然语音 |
| 🎬 **音频导出** | 合并全剧音频为单个 `.wav` 文件，同步生成 `.srt` 字幕 |

---

## 🧪 测试结果

### MiMo API 实测数据

使用以下台本实测 MiMo API（2026-05-28）：

<details>
<summary><b>📜 测试台本（点击展开）</b></summary>

```
第一幕：咖啡馆
服务员：欢迎光临，请问需要点什么？
李明：一杯美式咖啡，谢谢。
服务员：好的，请稍等。

第二幕：办公室
张总：李明，上次的方案客户很满意。
李明：（惊喜）真的吗？太好了！
张总：但是还有几个细节需要调整，今天能改完吗？
李明：（叹气）好吧，我今天加班。

第三幕：深夜
小红：这么晚还在加班？
李明：（疲惫）没办法，客户明天要看。
小红：我给你带了夜宵，先吃点吧。
李明：（感动）谢谢你，小红。
```

</details>

#### 角色分析结果

| 角色 | 性别 | 年龄 | 音色推荐 | 性格特征 |
|------|------|------|----------|----------|
| 服务员 | 未知 | 25 | 温和礼貌 | 专业、友好，展现职业化服务态度 |
| 李明 | 男 | 30 | 沉稳 | 勤奋认真，面对加班感疲惫，但仍负责到底 |
| 张总 | 男 | 45 | 成熟稳重 | 权威、注重细节和效率，下达任务直接果断 |
| 小红 | 女 | 28 | 温柔亲切 | 体贴温暖，深夜送夜宵展现细腻关怀 |

#### TTS 合成测试

```python
# MiMo TTS v2.5 调用示例
resp = client.chat.completions.create(
    model="mimo-v2.5-tts",
    messages=[...],
    audio={"format": "wav", "voice": "Chloe"}
)
# ✅ 成功生成 143KB WAV 音频
```

### 单元测试覆盖

```
79/79 passed (100%)
├── test_file_parser.py ........... 19 passed
├── test_role_analyzer.py ......... 14 passed
├── test_emotion_tagger.py ........ 10 passed
├── test_tts_service.py ........... 10 passed
└── test_api.py .................. 26 passed
```

---

## 🛠 技术栈

### 后端
- **框架**: FastAPI 0.115 + Uvicorn
- **ORM**: SQLAlchemy 2.0 + SQLite
- **AI**: MiMo (Xiaomi) API — OpenAI SDK 调用 `mimo-v2.5-pro` / `mimo-v2.5-tts`
- **音频**: pydub (拼接) + pysrt (字幕)
- **异步**: Celery + Redis (可选，MVP 使用 FastAPI BackgroundTasks)

### 前端
- **框架**: React 18 + Vite 5 + TypeScript 5.6
- **UI**: MUI v5 + Tailwind CSS v3
- **状态管理**: Zustand v5
- **数据获取**: TanStack React Query v5

---

## 🚀 快速开始

### 1. 克隆并配置

```bash
git clone https://github.com/jiahui-qin/scriptmind-helper.git
cd scriptmind-helper/backend
cp .env.example .env
```

编辑 `.env`，填入你的 MiMo API Key（[获取地址](https://platform.xiaomimimo.com)）:

```env
MIMO_API_KEY=sk-your-key-here
SQLITE_DB=scriptmind.db
```

### 2. 启动后端

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

访问 http://localhost:8000/docs 查看 Swagger API 文档。

### 3. 启动前端

```bash
cd frontend
npm install
npm run dev
```

访问 http://localhost:3000，上传台本开始使用。

### 4. Docker 部署

```bash
docker-compose up -d
# 前端: http://localhost:3000
# 后端: http://localhost:8000/docs
```

---

## 📡 API 端点

| 方法 | 路径 | 说明 |
|------|------|------|
| `POST` | `/api/v1/upload/script` | 上传台本文件 (multipart/form-data) |
| `GET` | `/api/v1/upload/script/{id}` | 获取台本信息 |
| `POST` | `/api/v1/analysis/{id}/analyze` | 触发 AI 角色分析（异步） |
| `GET` | `/api/v1/analysis/{id}` | 获取分析结果（角色+台词+情感） |
| `POST` | `/api/v1/tts/{id}/synthesize` | 触发 TTS 语音合成（异步） |
| `GET` | `/api/v1/tts/tasks/{id}` | 查询 TTS 任务状态 |
| `GET` | `/api/v1/config/status` | 检查 API Key 配置状态 |
| `POST` | `/api/v1/config/` | 更新 API Key 配置 |
| `GET` | `/health` | 健康检查 |

---

## 📁 项目结构

```
scriptmind-helper/
├── backend/                 # FastAPI 后端
│   ├── app/
│   │   ├── api/endpoints/   # REST API (upload/analysis/tts/config)
│   │   ├── models/          # SQLAlchemy 模型 (Script/Role/Line/TTSTask)
│   │   ├── schemas/         # Pydantic V2 校验
│   │   ├── services/        # 业务逻辑 (parser/analyzer/tagger/tts)
│   │   └── tasks/           # Celery 异步任务
│   ├── tests/               # 79 个单元+集成测试
│   ├── data/uploads/        # 上传文件存储
│   └── data/output/         # 音频/字幕输出
├── frontend/                # React + Vite 前端
│   └── src/
│       ├── pages/           # Home / Analysis / Result / Config
│       ├── components/      # ScriptUploader / RoleCard / AudioPlayer
│       ├── services/        # Axios API 封装
│       ├── store/           # Zustand 状态管理
│       └── types/           # TypeScript 类型定义
├── docs/                    # 设计文档 (PRD/Architecture/Task Breakdown)
├── docker-compose.yml       # Docker 编排
└── .env.example             # 环境变量模板
```

---

## 🔧 配置说明

| 环境变量 | 默认值 | 说明 |
|----------|--------|------|
| `MIMO_API_KEY` | (必填) | MiMo 平台 API Key |
| `MIMO_API_BASE` | `https://api.xiaomimimo.com/v1` | MiMo API 端点 |
| `MIMO_CHAT_MODEL` | `mimo-v2.5-pro` | 对话模型 |
| `MIMO_TTS_MODEL` | `mimo-v2.5-tts` | TTS 模型 |
| `SQLITE_DB` | `scriptmind.db` | 数据库文件路径 |
| `REDIS_URL` | `redis://localhost:6379/0` | Redis 连接（Celery 模式） |
| `MAX_FILE_SIZE` | `10485760` (10MB) | 上传文件大小限制 |

### 获取 MiMo API Key

1. 访问 [MiMo 开放平台](https://platform.xiaomimimo.com)
2. 注册/登录小米账号
3. 创建 API Key
4. 填入 `.env` 文件

> MiMo API 使用 OpenAI 兼容格式，可直接用 `openai` Python SDK 调用。

---

## 🗺 开发路线

- [x] **T01** — 项目脚手架 (FastAPI + React + Docker)
- [x] **T02** — 后端核心 API (文件上传 / 角色分析 / TTS)
- [x] **T03** — 前端核心页面 (拖拽上传 / 角色卡片 / 音频播放)
- [x] **T04** — 自动化测试 (79/79 通过)
- [x] **T05** — Docker 部署 + 文档
- [ ] **T06** — 后台任务迁移 Celery
- [ ] **T07** — 多格式台本支持 (PDF/Word/Markdown)
- [ ] **T08** — 用户系统 + 历史记录

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

```bash
# 运行测试
cd backend && python -m pytest tests/ -v --tb=short
```

## 📄 许可证

MIT License © 2025 [jiahui-qin](https://github.com/jiahui-qin)
