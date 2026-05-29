<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-0.115-009688?style=flat-square&logo=fastapi" alt="FastAPI">
  <img src="https://img.shields.io/badge/React-18-61DAFB?style=flat-square&logo=react" alt="React">
  <img src="https://img.shields.io/badge/TypeScript-5.6-3178C6?style=flat-square&logo=typescript" alt="TS">
  <img src="https://img.shields.io/badge/license-MIT-blue?style=flat-square" alt="License">
</p>

<h1 align="center">🎭 ScriptMind AI</h1>
<p align="center"><strong>AI 驱动的剧本角色分析与语音合成工具</strong></p>

---

## ✨ 功能特性

### 核心流程

| 功能 | 描述 |
|------|------|
| 📄 **台本上传** | 拖拽上传 `.txt` 台本文件，支持 UTF-8 编码，最大 10MB |
| ✏️ **分析前编辑** | 上传后可直接编辑原文，修正角色名/格式后重新分析 |
| 🤖 **AI 角色分析** | MiMo `mimo-v2.5-pro` 识别角色，推断性别/年龄/性格/语调/音色/腔调/方言等属性 |
| 💬 **情感标注** | 每句台词标注基础情绪（14种）+ 复合情绪（9种）+ 强度值 |
| 🎙️ **TTS 语音合成** | MiMo `mimo-v2.5-tts`，9 种音色可选，逐行合成 + MD5 缓存 |
| 🎬 **音频导出** | 合并为单个 `.wav` + `.srt` 字幕，句间间隙可配置（0-2000ms） |

### 分析页编辑功能

| 功能 | 描述 |
|------|------|
| 🔄 **逐行编辑** | 每行下拉选择角色/基础情绪/复合情绪，即时保存 |
| ✅ **批量操作** | 勾选多行 → 统一修改角色/情绪 |
| ⚡ **快速转移** | 选来源角色 → 目标角色，一键转移全部对话（支持旁白） |
| 🎨 **风格标签** | 预置 + 自由输入，自定义值持久化跨脚本复用 |
| ➕ **在线创建角色** | 下拉选"创建新角色"，弹窗输入名称/性别即可 |
| 🔍 **按角色过滤** | 顶部下拉筛选，快速聚焦特定角色台词 |

### 角色属性体系

| 类别 | 可选值 |
|------|--------|
| 基础情绪 | 开心 / 悲伤 / 愤怒 / 恐惧 / 惊讶 / 兴奋 / 委屈 / 平静 / 冷漠 |
| 复合情绪 | 怅然 / 欣慰 / 无奈 / 愧疚 / 释然 / 嫉妒 / 厌倦 / 忐忑 / 动情 |
| 整体语调 | 温柔 / 高冷 / 活泼 / 严肃 / 慵懒 / 俏皮 / 深沉 / 干练 / 凌厉 |
| 音色定位 | 磁性 / 醇厚 / 清亮 / 空灵 / 稚嫩 / 苍老 / 甜美 / 沙哑 / 醇雅 |
| 人设腔调 | 夹子音 / 御姐音 / 正太音 / 大叔音 / 台湾腔 |
| 方言 | 东北话 / 四川话 / 河南话 / 粤语（可自由输入） |
| 角色扮演 | 孙悟空 / 林黛玉（可自由输入） |

### TTS 合成

| 功能 | 描述 |
|------|------|
| 🎵 **音色试听** | TTS 对话框每个音色旁有 ▶ 试听按钮，缓存到本地 |
| ⏱️ **句间间隙** | 滑块 0-2000ms，默认推荐 300ms |
| 📊 **合成进度** | 逐行合成实时进度条，ResultPage 显示百分比 |
| 🛡️ **容错跳过** | 单句失败自动跳过继续，最终标注失败行号 |
| 📋 **参数展示** | 结果页显示合成参数：间隙/总行数/旁白/角色音色配置 |
| 💾 **TTS 缓存** | 同文本+同音色 MD5 缓存，重复合成秒出，节省 API 额度 |

### 台本管理

| 功能 | 描述 |
|------|------|
| 📋 **台本列表** | 我的台本页展示所有上传记录，按时间排序 |
| 🔗 **TTS 关联** | 每条台本关联其 TTS 合成记录，点击 Chip 直接跳转结果页 |
| 🗑️ **删除** | 删除台本同时清理 TXT + 音频 + 字幕 |

---

## 🛠 技术栈

### 后端
- **框架**: FastAPI 0.115 + Uvicorn
- **ORM**: SQLAlchemy 2.0 + SQLite
- **AI**: MiMo (Xiaomi) API — OpenAI SDK 调用 `mimo-v2.5-pro` / `mimo-v2.5-tts`
- **Prompt**: JSON Schema (`response_format` strict mode) 约束输出格式
- **音频**: pydub (拼接/裁剪/静音裁剪) + pysrt (字幕)
- **异步**: FastAPI BackgroundTasks

### 前端
- **框架**: React 18 + Vite 5 + TypeScript 5.6
- **UI**: MUI v5 (支持暗色模式切换)
- **状态管理**: Zustand v5
- **数据获取**: TanStack React Query v5 + Axios

---

## 🚀 快速开始

### 1. 克隆并配置

```bash
git clone https://github.com/jiahui-qin/scriptmind-helper.git
cd scriptmind-helper/backend
cp .env.example .env
```

编辑 `.env`，填入 MiMo API Key：

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

访问 http://localhost:3000，拖拽/选择 `.txt` 台本即可开始。

---

## 📡 API 端点

| 方法 | 路径 | 说明 |
|------|------|------|
| `POST` | `/api/v1/upload/script` | 上传台本文件 |
| `PUT` | `/api/v1/upload/script/{id}/content` | 编辑台本原文 |
| `GET` | `/api/v1/upload/script/{id}` | 获取台本信息 |
| `DELETE` | `/api/v1/upload/script/{id}` | 删除台本 |
| `GET` | `/api/v1/upload/scripts` | 列出所有台本 |
| `POST` | `/api/v1/analysis/{id}/analyze` | 触发 AI 分析 |
| `GET` | `/api/v1/analysis/{id}` | 获取分析结果（含内容/角色/台词） |
| `PUT` | `/api/v1/lines/{id}` | 编辑单行（角色/情绪） |
| `POST` | `/api/v1/lines/batch` | 批量更新（by_ids / by_role） |
| `PUT` | `/api/v1/roles/{id}` | 编辑角色属性 |
| `POST` | `/api/v1/roles/scripts/{id}/roles` | 创建新角色 |
| `GET` | `/api/v1/styles/{category}` | 获取风格选项（内置+自定义） |
| `POST` | `/api/v1/styles/` | 添加自定义风格 |
| `POST` | `/api/v1/tts/{id}/synthesize` | 触发 TTS 合成 |
| `GET` | `/api/v1/tts/preview` | 音色试听（缓存 WAV） |
| `GET` | `/api/v1/tts/tasks/{id}` | 查询 TTS 任务状态 |
| `GET` | `/api/v1/tts/tasks/{id}/download` | 下载音频/字幕 |
| `GET` | `/api/v1/config/status` | 检查 API Key 配置状态 |
| `POST` | `/api/v1/config/` | 更新 API Key 配置 |
| `GET` | `/health` | 健康检查 |

---

## 📁 项目结构

```
scriptmind-helper/
├── backend/
│   ├── app/
│   │   ├── api/endpoints/   # upload / analysis / lines / roles / styles / tts / config
│   │   ├── models/          # Script / Role / Line / TTSTask / StylePreset
│   │   ├── schemas/         # Pydantic V2 校验
│   │   └── services/        # file_parser / role_analyzer / emotion_tagger / tts_service
│   ├── data/
│   │   ├── uploads/         # 上传 TXT
│   │   ├── output/          # WAV + SRT 输出
│   │   ├── preview/         # 音色试听缓存
│   │   └── tts_cache/       # TTS MD5 缓存
│   └── tests/
├── frontend/
│   └── src/
│       ├── pages/           # Home / Analysis / Result / Config / MyScripts
│       ├── components/      # LineRow / BatchActionBar / StyleSelector / RoleCard / CreateRoleDialog / AudioPlayer / ScriptUploader
│       ├── constants/       # emotions.ts 风格常量
│       ├── services/        # Axios API 封装
│       ├── store/           # Zustand
│       └── types/
├── docs/
├── docker-compose.yml
└── .env.example
```

---

## 🗺 开发路线

### ✅ 已完成

- **T01** 项目脚手架 (FastAPI + React + Docker)
- **T02** 后端核心 API (上传 / 角色分析 / TTS)
- **T03** 前端核心页面 (上传 / 分析 / 结果)
- **T04** 分析页可编辑功能 (逐行编辑 / 批量操作 / 快速转移)
- **T05** 风格标签体系 (预置 + 自定义 + 跨脚本复用)
- **T06** AI Prompt JSON Schema 严格约束
- **T07** TTS 优化 (音色试听 / 缓存 / 容错 / 逐行进度 / 间隙配置)
- **T08** 暗色模式 + 上传自动分析 + 分析前编辑
- **T09** 台本管理关联 TTS (我的台本页语音列)

### 📋 待优化 (P2)

| # | 优化点 | 说明 |
|---|--------|------|
| 1 | **音量归一化** | RMS 归一化统一响度，不同角色台词音量一致 |
| 2 | **MP3 导出** | 支持 `export(format="mp3")`，需要安装 ffmpeg |
| 3 | **批量下载** | 一键导出 WAV + SRT 压缩包 |
| 4 | **分析前角色预设** | 允许手动补充角色名单，提高 AI 识别准确度 |
| 5 | **多人协作** | 简单用户系统，共享台本 |
| 6 | **多格式台本** | 支持 PDF / Markdown 台本解析 |
| 7 | **TTS 语速控制** | 每句台词可配语速 (当前固定 1.0) |
| 8 | **TTS 情绪语音** | 根据 emotion_tag 调整 MiMo prompt 语调参数 |
| 9 | **背景音乐** | 允许上传 BGM，混音到最终音频 |
| 10 | **音频波形可视化** | ResultPage 音频播放器加波形图 |

---

## 🔧 配置说明

| 环境变量 | 默认值 | 说明 |
|----------|--------|------|
| `MIMO_API_KEY` | (必填) | MiMo 平台 API Key |
| `MIMO_API_BASE` | `https://api.xiaomimimo.com/v1` | MiMo API 端点 |
| `MIMO_CHAT_MODEL` | `mimo-v2.5-pro` | 对话模型 |
| `SQLITE_DB` | `scriptmind.db` | 数据库文件路径 |
| `MAX_FILE_SIZE` | `10485760` (10MB) | 上传文件大小限制 |

### 获取 MiMo API Key

1. 访问 [MiMo 开放平台](https://platform.xiaomimimo.com)
2. 注册/登录小米账号
3. 创建 API Key
4. 填入 `.env` 文件

> MiMo API 使用 OpenAI 兼容格式，可直接用 `openai` Python SDK 调用。

---

## 📄 许可证

MIT License © 2025 [jiahui-qin](https://github.com/jiahui-qin)
