<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-0.115-009688?style=flat-square&logo=fastapi" alt="FastAPI">
  <img src="https://img.shields.io/badge/React-18-61DAFB?style=flat-square&logo=react" alt="React">
  <img src="https://img.shields.io/badge/TypeScript-5.6-3178C6?style=flat-square&logo=typescript" alt="TS">
  <img src="https://img.shields.io/badge/Docker-ghcr.io-blue?style=flat-square&logo=docker" alt="Docker">
  <img src="https://img.shields.io/badge/license-MIT-blue?style=flat-square" alt="License">
</p>

<h1 align="center">🎭 ScriptMind AI</h1>
<p align="center">
  <strong>AI-Powered Script Character Analysis & Text-to-Speech Tool</strong><br>
  <sub>AI 驱动的剧本角色分析与语音合成工具</sub>
</p>

---

> 📖 [English version below](#english) | 中文说明见上方

---

## ✨ 功能特性 / Features

### 核心流程 / Core Workflow

| 功能 Feature | 描述 Description |
|-------------|-----------------|
| 📄 **台本上传 Upload** | 拖拽上传 `.txt` 台本文件，支持 UTF-8 编码，最大 10MB |
| ✏️ **分析前编辑 Pre-analysis Edit** | 上传后可直接编辑原文，修正角色名/格式后重新分析 / Edit raw script before AI analysis |
| 🤖 **AI 角色分析 Role Analysis** | MiMo `mimo-v2.5-pro` 识别角色，推断性别/年龄/性格/语调/音色/腔调/方言 / AI infers gender, age, personality, tone, voice color, dialect, etc. |
| 💬 **情感标注 Emotion Tagging** | 每句台词标注基础情绪(14种) + 复合情绪(9种) + 强度值 / Basic emotions (14) + complex emotions (9) + intensity |
| 🎙️ **TTS 语音合成 Voice Synthesis** | MiMo `mimo-v2.5-tts`，9 种音色可选，逐行合成 + MD5 缓存 / 9 voices, per-line synthesis with disk cache |
| 🎬 **音频导出 Export** | 合并为单个 `.wav` + `.srt` 字幕，句间间隙可配置 0-2000ms / Single WAV + SRT, configurable gap |

### 分析页编辑 / Analysis Editing

| 功能 Feature | 描述 Description |
|-------------|-----------------|
| 🔄 **逐行编辑 Line Edit** | 每行下拉选择角色/基础情绪/复合情绪，即时保存 / Inline role & emotion editing |
| ✅ **批量操作 Batch Edit** | 勾选多行 → 统一修改角色/情绪 / Multi-line batch update |
| ⚡ **快速转移 Quick Transfer** | 选来源角色 → 目标角色，一键转移全部对话 / One-click role reassignment |
| 🎨 **风格标签 Style Tags** | 预置 + 自由输入，自定义值持久化跨脚本复用 / Presets + free input, persistent |
| ➕ **在线创建角色 Create Role** | 下拉选"创建新角色"，弹窗输入名称/性别即可 / Create roles on the fly |
| 🔍 **按角色过滤 Role Filter** | 顶部下拉筛选，快速聚焦特定角色台词 / Filter lines by character |

### 角色属性 / Character Attributes

| 类别 Category | 可选值 Options |
|--------------|---------------|
| 基础情绪 Basic Emotions | 开心 / 悲伤 / 愤怒 / 恐惧 / 惊讶 / 兴奋 / 委屈 / 平静 / 冷漠 |
| 复合情绪 Complex Emotions | 怅然 / 欣慰 / 无奈 / 愧疚 / 释然 / 嫉妒 / 厌倦 / 忐忑 / 动情 |
| 整体语调 Tone Style | 温柔 / 高冷 / 活泼 / 严肃 / 慵懒 / 俏皮 / 深沉 / 干练 / 凌厉 |
| 音色定位 Voice Color | 磁性 / 醇厚 / 清亮 / 空灵 / 稚嫩 / 苍老 / 甜美 / 沙哑 / 醇雅 |
| 人设腔调 Persona Accent | 夹子音 / 御姐音 / 正太音 / 大叔音 / 台湾腔 |
| 方言 Dialect | 东北话 / 四川话 / 河南话 / 粤语 (自由输入 / free input) |
| 角色扮演 Roleplay | 孙悟空 / 林黛玉 (自由输入 / free input) |

### TTS 合成 / TTS Synthesis

| 功能 Feature | 描述 Description |
|-------------|-----------------|
| 🎵 **音色试听 Voice Preview** | TTS 对话框每个音色旁有 ▶ 试听按钮，缓存到本地 / Sample playback with disk cache |
| ⏱️ **句间间隙 Line Gap** | 滑块 0-2000ms，默认推荐 300ms / Configurable gap with slider |
| 📊 **合成进度 Progress** | 逐行合成实时进度条 / Real-time per-line progress bar |
| 🛡️ **容错跳过 Fault Tolerance** | 单句失败自动跳过继续，最终标注失败行号 / Skip failed lines, report at end |
| 📋 **参数展示 Params Display** | 结果页显示合成参数：间隙/总行数/旁白/角色音色配置 / View synthesis params in result page |
| 💾 **TTS 缓存 Cache** | 同文本+同音色 MD5 缓存，重复合成秒出，节省 API 额度 / MD5 cache saves API cost |

### 台本管理 / Script Management

| 功能 Feature | 描述 Description |
|-------------|-----------------|
| 📋 **台本列表 Script List** | 我的台本页展示所有上传记录，按时间排序 / Manage all uploaded scripts |
| 🔗 **TTS 关联 TTS Link** | 每条台本关联其 TTS 合成记录，点击 Chip 直接跳转结果页 / Linked TTS tasks |
| 🗑️ **删除 Delete** | 删除台本同时清理 TXT + 音频 + 字幕 / Cascade delete |

---

## 🛠 技术栈 / Tech Stack

### 后端 / Backend
- **Framework**: FastAPI 0.115 + Uvicorn
- **ORM**: SQLAlchemy 2.0 + SQLite
- **AI**: MiMo (Xiaomi) API — OpenAI SDK → `mimo-v2.5-pro` / `mimo-v2.5-tts`
- **Prompt**: JSON Schema `strict: true` response format
- **Audio**: pydub + pysrt
- **Async**: FastAPI BackgroundTasks

### 前端 / Frontend
- **Framework**: React 18 + Vite 5 + TypeScript 5.6
- **UI**: MUI v5 (暗色模式 / dark mode)
- **State**: Zustand v5
- **Data**: TanStack React Query v5 + Axios

---

## 🚀 快速开始 / Quick Start

### 1. 克隆并配置 / Clone & Config

```bash
git clone https://github.com/jiahui-qin/scriptmind-helper.git
cd scriptmind-helper/backend
cp .env.example .env
```

Edit `.env` with your MiMo API Key ([获取地址 / Get Key](https://platform.xiaomimimo.com)):

```env
MIMO_API_KEY=sk-your-key-here
SQLITE_DB=scriptmind.db
```

### 2. 本地开发 / Local Dev

**后端 Backend:**
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
# Swagger: http://localhost:8000/docs
```

**前端 Frontend:**
```bash
cd frontend
npm install
npm run dev
# http://localhost:3000
```

### 3. Docker 部署 / Docker Deploy

```bash
# Backend
docker pull ghcr.io/jiahui-qin/scriptmind-backend:latest
docker run -d -p 8000:8000 -e MIMO_API_KEY=sk-xxx ghcr.io/jiahui-qin/scriptmind-backend:latest

# Frontend
docker pull ghcr.io/jiahui-qin/scriptmind-frontend:latest
docker run -d -p 3000:80 ghcr.io/jiahui-qin/scriptmind-frontend:latest
```

Or use docker-compose:

```yaml
# docker-compose.yml
services:
  backend:
    image: ghcr.io/jiahui-qin/scriptmind-backend:latest
    ports: ["8000:8000"]
    env_file: .env
    volumes:
      - ./data:/app/data

  frontend:
    image: ghcr.io/jiahui-qin/scriptmind-frontend:latest
    ports: ["3000:80"]
    depends_on: [backend]
```

---

## 📡 API 端点 / API Endpoints

| 方法 Method | 路径 Path | 说明 Description |
|------------|----------|-----------------|
| `POST` | `/api/v1/upload/script` | 上传台本 / Upload script |
| `PUT` | `/api/v1/upload/script/{id}/content` | 编辑台本原文 / Edit raw content |
| `GET` | `/api/v1/upload/script/{id}` | 获取台本信息 / Get script info |
| `DELETE` | `/api/v1/upload/script/{id}` | 删除台本 / Delete script |
| `GET` | `/api/v1/upload/scripts` | 列出所有台本 / List scripts |
| `POST` | `/api/v1/analysis/{id}/analyze` | 触发 AI 分析 / Trigger analysis |
| `GET` | `/api/v1/analysis/{id}` | 获取分析结果 / Get analysis result |
| `PUT` | `/api/v1/lines/{id}` | 编辑单行 / Update line |
| `POST` | `/api/v1/lines/batch` | 批量更新 / Batch update (by_ids / by_role) |
| `PUT` | `/api/v1/roles/{id}` | 编辑角色 / Update role |
| `POST` | `/api/v1/roles/scripts/{id}/roles` | 创建新角色 / Create role |
| `GET` | `/api/v1/styles/{category}` | 获取风格选项 / Get style options |
| `POST` | `/api/v1/styles/` | 添加自定义风格 / Add custom style |
| `POST` | `/api/v1/tts/{id}/synthesize` | 触发 TTS 合成 / Trigger TTS |
| `GET` | `/api/v1/tts/preview` | 音色试听 / Voice preview (cached) |
| `GET` | `/api/v1/tts/tasks/{id}` | 查询 TTS 状态 / TTS task status |
| `GET` | `/api/v1/tts/tasks/{id}/download` | 下载音频/字幕 / Download audio/SRT |
| `GET` | `/api/v1/config/status` | 检查配置 / Check API key |
| `POST` | `/api/v1/config/` | 更新配置 / Update config |
| `GET` | `/health` | 健康检查 / Health check |

---

## 📁 项目结构 / Project Structure

```
scriptmind-helper/
├── backend/
│   ├── app/
│   │   ├── api/endpoints/   # upload / analysis / lines / roles / styles / tts / config
│   │   ├── models/          # Script / Role / Line / TTSTask / StylePreset
│   │   ├── schemas/         # Pydantic V2 validation
│   │   └── services/        # file_parser / role_analyzer / emotion_tagger / tts_service
│   ├── Dockerfile
│   └── data/                # uploads / output / preview / tts_cache
├── frontend/
│   ├── src/
│   │   ├── pages/           # Home / Analysis / Result / Config / MyScripts
│   │   ├── components/      # LineRow / BatchActionBar / StyleSelector / RoleCard / etc.
│   │   ├── constants/       # emotions.ts
│   │   └── services/        # Axios API client
│   ├── Dockerfile
│   └── nginx.conf
├── .github/workflows/       # Docker build & push CI
│   └── docker-build.yml
└── README.md                # 中英双语 / Bilingual
```

---

## 🗺 开发路线 / Roadmap

### ✅ 已完成 / Completed

- **T01** 项目脚手架 / Project scaffold (FastAPI + React + Docker)
- **T02** 后端核心 API / Core backend API
- **T03** 前端核心页面 / Core frontend pages
- **T04** 分析页可编辑功能 / Analysis editing (line/batch/transfer)
- **T05** 风格标签体系 / Style tag system (presets + custom)
- **T06** AI Prompt JSON Schema 严格约束 / Strict schema constraints
- **T07** TTS 优化 / TTS optimization (preview/cache/fault-tolerance/progress/gap)
- **T08** 暗色模式 + 上传自动分析 + 分析前编辑 / Dark mode + auto-analysis + pre-edit
- **T09** 台本管理关联 TTS / Script management with TTS links
- **T10** GitHub Actions Docker 自动构建 / Docker CI/CD to GHCR

### 📋 待优化 / Backlog

| # | 优化点 Item | 说明 Description |
|---|-----------|-----------------|
| 1 | 音量归一化 / Loudness normalization | RMS 归一化统一响度 / Normalize loudness across roles |
| 2 | MP3 导出 / MP3 export | 支持 `export(format="mp3")` / Need ffmpeg |
| 3 | 批量下载 / Batch download | 一键导出 WAV + SRT 压缩包 / ZIP export |
| 4 | 分析前角色预设 / Role presets | 手动补充角色名单提高 AI 识别准确度 / Improve recognition |
| 5 | 多格式台本 / Multi-format | 支持 PDF / Markdown 台本解析 |
| 6 | TTS 语速控制 / Speech rate control | 每句台词可配语速 / Per-line speed control |
| 7 | TTS 情绪语音 / Emotional TTS | 根据 emotion_tag 调整 MiMo prompt / Emotion-aware prompting |
| 8 | 背景音乐 / Background music | 上传 BGM 混音到最终音频 / Mix BGM into final audio |
| 9 | 用户系统 / User system | 简单登录 + 私有台本 / Auth + private scripts |
| 10 | 音频波形可视化 / Waveform visualizer | ResultPage 加波形图 / Audio waveform display |

---

## 🔧 配置 / Configuration

| 环境变量 Env Var | 默认值 Default | 说明 Description |
|-----------------|---------------|-----------------|
| `MIMO_API_KEY` | (必填 required) | MiMo 平台 API Key |
| `MIMO_API_BASE` | `https://api.xiaomimimo.com/v1` | MiMo API endpoint |
| `MIMO_CHAT_MODEL` | `mimo-v2.5-pro` | 对话模型 / Chat model |
| `SQLITE_DB` | `scriptmind.db` | 数据库路径 / DB path |
| `MAX_FILE_SIZE` | `10485760` (10MB) | 上传大小限制 / Upload limit |

---

## 📄 许可证 / License

MIT License © 2025 [jiahui-qin](https://github.com/jiahui-qin)
