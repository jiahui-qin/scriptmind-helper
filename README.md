# ScriptMind AI — 台本分析助手

ScriptMind AI 是一款智能台本分析工具，帮助编剧、配音导演和内容创作者快速分析台本角色、标注情感并生成 TTS 语音预览。

## 功能特性

- 📄 **台本上传**：支持 `.txt` 格式台本文件上传与解析
- 🤖 **AI 角色分析**：基于 MiMo LLM 自动识别角色并分析性格特征
- 🎭 **情感标注**：为每句台词自动标注情感标签、语气、语速和情绪强度
- 🔊 **TTS 语音合成**：调用 MiMo TTS API 生成完整音频预览，附带 SRT 字幕

## 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | React 18 + Vite + TypeScript + MUI (Material UI) + Tailwind CSS |
| 后端 | Python 3.11+ / FastAPI + SQLAlchemy + Pydantic v2 |
| 数据库 | SQLite (开发) / PostgreSQL (生产推荐) |
| 缓存 | Redis (可选) |
| AI | Moonshot (MiMo) API — Chat Completions + TTS v2.5 |
| 部署 | Docker + Docker Compose + Nginx |

## 项目结构

```
scriptmind-helper/
├── backend/                    # FastAPI 后端
│   ├── app/
│   │   ├── api/endpoints/      # API 路由 (upload/analysis/tts/config)
│   │   ├── models/             # SQLAlchemy 数据模型
│   │   ├── schemas/            # Pydantic 请求/响应模型
│   │   ├── services/           # 业务逻辑层
│   │   │   ├── file_parser.py   # 台本文件解析
│   │   │   ├── role_analyzer.py # AI 角色分析
│   │   │   ├── emotion_tagger.py# 情感标注
│   │   │   └── tts_service.py  # TTS 合成
│   │   ├── config.py           # 应用配置
│   │   ├── database.py         # 数据库配置
│   │   └── main.py             # FastAPI 应用入口
│   ├── tests/                  # 单元测试 & 集成测试
│   ├── Dockerfile
│   ├── requirements.txt
│   └── create_tables.py
├── frontend/                   # React 前端
│   ├── src/
│   │   ├── pages/              # 页面组件
│   │   ├── components/         # 公共组件
│   │   ├── services/           # API 调用封装
│   │   └── App.tsx             # 应用入口
│   ├── Dockerfile
│   ├── nginx.conf
│   └── package.json
├── docs/                       # 设计文档 (PRD / 架构设计)
├── data/                       # 上传文件存储
├── docker-compose.yml          # Docker 编排配置
├── .env.example                # 环境变量模板
└── README.md
```

## 快速开始

### 环境要求

- Python 3.11+
- Node.js 18+
- npm 9+

### 本地开发

```bash
# 1. 克隆项目
git clone <repo-url>
cd scriptmind-helper

# 2. 配置环境变量
cp .env.example .env
# 编辑 .env，填入你的 Moonshot API Key

# 3. 启动后端
cd backend
pip install -r requirements.txt
python create_tables.py
uvicorn app.main:app --reload --port 8000

# 4. 启动前端（新终端）
cd frontend
npm install
npm run dev
```

前端访问：http://localhost:5173
后端 API 文档：http://localhost:8000/docs

### Docker 部署

```bash
# 1. 配置环境变量
cp .env.example .env
# 编辑 .env，填入你的 Moonshot API Key

# 2. 构建并启动
docker compose up -d

# 3. 查看日志
docker compose logs -f

# 4. 停止
docker compose down
```

前端访问：http://localhost:3000
后端 API 文档：http://localhost:8000/docs

## API 文档

启动后端后访问 http://localhost:8000/docs 查看 Swagger UI 交互式文档。

主要接口：

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/health` | 健康检查 |
| POST | `/api/v1/upload/script` | 上传台本文件 |
| GET | `/api/v1/upload/scripts` | 台本列表 |
| GET | `/api/v1/upload/script/{id}` | 获取台本详情 |
| POST | `/api/v1/analysis/{id}/analyze` | 触发 AI 分析 |
| GET | `/api/v1/analysis/{id}` | 获取分析结果 |
| POST | `/api/v1/tts/{id}/synthesize` | 触发 TTS 合成 |
| GET | `/api/v1/tts/tasks` | TTS 任务列表 |
| GET | `/api/v1/tts/tasks/{task_id}` | TTS 任务状态 |
| GET | `/api/v1/config/status` | 配置状态 |
| POST | `/api/v1/config/` | 更新配置 |

## 配置说明

### 获取 Moonshot API Key

1. 访问 [Moonshot AI 开放平台](https://platform.moonshot.cn/)
2. 注册/登录账号
3. 在控制台创建 API Key
4. 将 Key 填入 `.env` 文件或通过 `/api/v1/config/` 接口配置

### 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `MOONSHOT_API_KEY` | Moonshot API 密钥 | 必填 |
| `SQLITE_DB` | SQLite 数据库文件 | `scriptmind.db` |
| `REDIS_URL` | Redis 连接地址 | `redis://redis:6379/0` |
| `MAX_FILE_SIZE` | 上传文件大小限制 (字节) | `10485760` (10MB) |

## 运行测试

```bash
cd backend
pip install pytest pytest-mock httpx
python -m pytest tests/ -v
```

## License

MIT

---

Made with ❤️ by ScriptMind Team
