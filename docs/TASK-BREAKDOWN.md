# ScriptMind Helper - 项目任务拆解

> 基于架构设计 v3.0，按员工角色拆解交付内容
> 
> **技术栈**：React + Vite + MUI + Tailwind CSS + FastAPI + SQLite + MiMo API

---

## 一、项目结构总览

```
scriptmind-helper/
├── backend/                    # 后端（FastAPI + SQLite）
│   ├── app/
│   │   ├── main.py           # FastAPI 入口
│   │   ├── config.py         # 配置管理（MiMo API Key 等）
│   │   ├── database.py       # SQLite 连接初始化
│   │   ├── models/          # SQLAlchemy 模型
│   │   ├── schemas/         # Pydantic Schema
│   │   ├── api/endpoints/   # API 路由
│   │   ├── services/         # 业务逻辑层
│   │   └── tasks/           # 异步任务（Celery 或 asyncio）
│   ├── requirements.txt
│   └── tests/
├── frontend/                   # 前端（React + Vite）
│   ├── src/
│   │   ├── main.tsx         # 入口
│   │   ├── App.tsx          # 路由配置
│   │   ├── pages/           # 页面组件
│   │   ├── components/       # 通用组件
│   │   ├── services/        # API 调用层
│   │   ├── store/           # Zustand 状态管理
│   │   └── types/          # TypeScript 类型定义
│   ├── package.json
│   ├── vite.config.ts
│   └── tailwind.config.js
├── docs/                      # 设计文档
└── README.md
```

---

## 二、各员工交付内容

---

### 👩💼 许清楚（产品经理）

**交付目标**：确保开发团队对需求理解一致，提供可验证的功能标准

| 交付物 | 文件路径 | 内容说明 |
|---------|---------|---------|
| **功能需求规格** | `docs/PRD.md` | 已交付（v1.0）→ 需更新为 v3.0（MiMo 专属） |
| **台本格式规范** | `docs/script-format-spec.md` | txt 台本格式说明 + 示例台本（含角色名、台词、舞台说明） |
| **情感标签体系** | `docs/emotion-tags.md` | 完整情感标签清单 + 强度分级（1-5）+ SRT 字幕格式说明 |
| **用户旅程地图** | `docs/user-journey.md` | 台本爱好者完整使用流程（上传→分析→试听→导出） |
| **验收标准清单** | `docs/acceptance-criteria.md` | 每个 P0 功能的验收标准（Gherkin 格式） |

**具体交付内容**：

#### 1. `docs/script-format-spec.md`（台本格式规范）
```markdown
# 台本格式规范 v1.0

## 基本格式

台本为 UTF-8 编码的 .txt 文件，格式如下：

角色名：台词内容
角色名：（舞台说明）台词内容
【场景说明】（可选）

## 示例

狂飙 - 第 1 集片段：

安欣：李哥，这么晚还在忙？
安长林：（放下文件）嗯，你还没休息？
安欣：我刚巡逻回来，看到你办公室灯还亮着。
安长林：这块案子有点棘手，你先看看这个材料。
【两人低头看文件，办公室安静只有翻纸声】
安欣：（抬头）这...
```

#### 2. `docs/emotion-tags.md`（情感标签体系）
```markdown
# 情感标签体系 v1.0

## 基础情感标签（9 种）

| 标签 | 说明 | 推荐语气 | 推荐语速 |
|------|------|---------|---------|
| neutral | 中性 | calm | 1.0x |
| happy | 高兴 | cheerful | 1.1x |
| sad | 悲伤 | melancholic | 0.9x |
| angry | 愤怒 | fierce | 1.2x |
| surprised | 惊讶 | astonished | 1.15x |
| fearful | 害怕 | nervous | 0.85x |
| disgusted | 厌恶 | detestable | 1.0x |
| loving | 温柔 | gentle | 0.95x |
| commanding | 命令 | firm | 1.05x |

## 扩展情感标签（8 种）

confident, hesitant, sarcastic, anxious, relieved, curious, disappointed, determined

## 强度分级（1-5）

1 = 轻微, 3 = 中等, 5 = 强烈

## SRT 字幕格式

1
00:00:01,000 --> 00:00:03,500
安欣：李哥，这么晚还在忙？
```

#### 3. `docs/user-journey.md`（用户旅程地图）
```markdown
# 用户旅程地图 v1.0

## 用户：台本爱好者（业余/半专业）

### 阶段 1：首次接触
1. 访问 GitHub 项目页
2. 阅读 README，本地部署
3. 配置 MiMo API Key
4. 上传第一个台本（示例台本）

### 阶段 2：核心使用
1. 等待分析完成（异步通知）
2. 查看角色列表 + 性格分析
3. 试听单句台词（TTS）
4. 调整情感标签
5. 合并错误识别的角色
6. 生成完整音频 + SRT 字幕
7. 导出文件

### 阶段 3：深度使用
1. 上传自定义 MiMo TTS 音色
2. 批量处理多个台本
3. 分享配置文件（角色设定 + 音色选择）
```

---

### 👨🏻‍💻 高见远（架构师）

**交付目标**：提供可执行的数据库 Schema、API 接口定义、前端架构设计

| 交付物 | 文件路径 | 内容说明 |
|---------|---------|---------|
| **数据库 Schema** | `backend/app/models/*.py` + `docs/schema.sql` | 完整 SQL 建表语句 + SQLAlchemy 模型 |
| **API 接口定义** | `docs/api-spec.yaml` | OpenAPI 3.0 格式，含请求/响应示例 |
| **前端架构设计** | `docs/frontend-architecture.md` | 路由设计 + 状态管理设计 + 组件树 |
| **文件结构清单** | `docs/file-manifest.md` | 所有源代码文件 + 配置文件的用途说明 |
| **部署指南** | `docs/deployment.md` | 本地部署步骤 + 环境变量说明 |

**具体交付内容**：

#### 1. `backend/app/models/*.py`（数据库模型）

**交付文件**：
- `backend/app/models/script.py` - Script 模型
- `backend/app/models/role.py` - Role 模型
- `backend/app/models/line.py` - Line 模型
- `backend/app/models/tts_task.py` - TTSTask 模型
- `backend/app/models/custom_voice.py` - CustomVoice 模型（自定义音色）
- `backend/app/database.py` - SQLite 连接初始化

**核心模型定义**（示例）：

```python
# backend/app/models/script.py
class Script(Base):
    __tablename__ = "scripts"
    
    id = Column(String, primary_key=True)  # UUID
    user_id = Column(String)  # 暂不使用，后续扩展
    filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    content = Column(Text)  # 原始文本
    status = Column(String, default="uploaded")  # uploaded/parsing/analyzing/completed/failed
    progress = Column(Float, default=0.0)  # 0.0 - 100.0
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    
    # 关系
    roles = relationship("Role", back_populates="script", cascade="all, delete-orphan")
    lines = relationship("Line", back_populates="script", cascade="all, delete-orphan")
    tts_tasks = relationship("TTSTask", back_populates="script", cascade="all, delete-orphan")

# backend/app/models/role.py
class Role(Base):
    __tablename__ = "roles"
    
    id = Column(String, primary_key=True)
    script_id = Column(String, ForeignKey("scripts.id"), nullable=False)
    name = Column(String, nullable=False)  # 角色名
    gender = Column(String)  # male/female/unknown
    age_range = Column(String)  # "20-30" 等
    personality = Column(Text)  # JSON 字符串，存储性格特点列表
    voice_settings = Column(Text)  # JSON 字符串，存储推荐音色 + 参数
    confidence = Column(Float)  # 识别置信度 0.0-1.0
    is_merged = Column(Boolean, default=False)  # 是否被手动合并
    created_at = Column(DateTime, default=datetime.utcnow)
    
    script = relationship("Script", back_populates="roles")
    lines = relationship("Line", back_populates="role")
    custom_voice_id = Column(String, ForeignKey("custom_voices.id"))  # 可选，用户上传的音色

# backend/app/models/line.py
class Line(Base):
    __tablename__ = "lines"
    
    id = Column(String, primary_key=True)
    script_id = Column(String, ForeignKey("scripts.id"), nullable=False)
    role_id = Column(String, ForeignKey("roles.id"))
    line_number = Column(Integer)  # 台本中的行号
    content = Column(Text, nullable=False)  # 台词内容
    emotion_tag = Column(String)  # 情感标签（happy/sad 等）
    emotion_intensity = Column(Integer, default=3)  # 强度 1-5
    tone = Column(String)  # 语气（cheerful/melancholic 等）
    speed = Column(Float, default=1.0)  # 语速 0.5-2.0
    voice_id = Column(String)  # MiMo TTS 音色 ID
    voice_params = Column(Text)  # JSON，存储 pitch/speed/volume
    audio_path = Column(String)  # 生成的音频文件路径
    start_time = Column(Float)  # 在最终音频中的开始时间（秒）
    end_time = Column(Float)  # 结束时间
    created_at = Column(DateTime, default=datetime.utcnow)
    
    script = relationship("Script", back_populates="lines")
    role = relationship("Role", back_populates="lines")

# backend/app/models/tts_task.py
class TTSTask(Base):
    __tablename__ = "tts_tasks"
    
    id = Column(String, primary_key=True)
    script_id = Column(String, ForeignKey("scripts.id"), nullable=False)
    status = Column(String, default="pending")  # pending/processing/completed/failed
    progress = Column(Float, default=0.0)
    output_format = Column(String, default="wav")  # wav/mp3
    include_subtitle = Column(Boolean, default=True)
    output_path = Column(String)  # 最终音频文件路径
    subtitle_path = Column(String)  # SRT 字幕文件路径
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    
    script = relationship("Script", back_populates="tts_tasks")

# backend/app/models/custom_voice.py
class CustomVoice(Base):
    __tablename__ = "custom_voices"
    
    id = Column(String, primary_key=True)
    user_id = Column(String)  # 暂不使用
    name = Column(String, nullable=False)
    description = Column(Text)
    sample_audio_path = Column(String)  # 上传的音频样本路径
    mimo_voice_id = Column(String)  # MiMo 返回的音色 ID
    status = Column(String, default="training")  # training/ready/failed
    created_at = Column(DateTime, default=datetime.utcnow)
```

#### 2. `docs/api-spec.yaml`（API 接口定义）

**交付内容**：OpenAPI 3.0 格式，定义所有 RESTful API 端点

**核心端点列表**：

| 方法 | 路径 | 说明 | 请求体 | 响应 |
|------|------|------|--------|------|
| POST | `/api/v1/scripts/upload` | 上传台本 | `multipart/form-data` (file) | `{script_id, filename, status}` |
| GET | `/api/v1/scripts/{id}/status` | 查询分析进度 | - | `{status, progress, current_step}` |
| GET | `/api/v1/scripts/{id}/roles` | 获取角色列表 | - | `[{id, name, gender, age_range, personality}]` |
| PUT | `/api/v1/scripts/{id}/roles/merge` | 合并角色 | `{role_ids: [id1, id2]}` | `{merged_role_id}` |
| GET | `/api/v1/scripts/{id}/lines` | 获取台词列表 | `?role_id=xxx&page=1` | `[{id, content, emotion_tag, tone, speed}]` |
| PUT | `/api/v1/scripts/{id}/lines/{line_id}` | 更新台词情感标签 | `{emotion_tag, tone, speed}` | `{updated_line}` |
| POST | `/api/v1/scripts/{id}/tts/preview` | 单句试听 | `{line_id, voice_id, speed, pitch}` | `{audio_url}` |
| POST | `/api/v1/scripts/{id}/tts/generate` | 生成完整音频 | `{output_format, voice_mapping}` | `{task_id}` |
| GET | `/api/v1/scripts/{id}/tts/{task_id}/status` | 查询 TTS 进度 | - | `{status, progress, output_url}` |
| GET | `/api/v1/scripts/{id}/export` | 导出结果 | `?format=wav,srt` | 文件下载 |
| POST | `/api/v1/voices/custom` | 上传自定义音色 | `multipart/form-data` (audio) | `{voice_id, status}` |
| GET | `/api/v1/voices/mimo` | 获取 MiMo 音色列表 | - | `[{voice_id, name, gender, age_range}]` |
| PUT | `/api/v1/config/mimo-key` | 配置 MiMo API Key | `{api_key}` | `{status}` |

#### 3. `docs/frontend-architecture.md`（前端架构设计）

**交付内容**：

- **路由设计**：
  ```
  /                    → 首页（上传台本）
  /scripts/:id/analysis → 分析进度页
  /scripts/:id/roles    → 角色列表页
  /scripts/:id/lines    → 台词编辑页
  /scripts/:id/tts       → TTS 生成页
  /voices               → 音色管理页
  /config                → 配置页（MiMo API Key）
  ```

- **状态管理设计**（Zustand）：
  ```
  useScriptStore      → 台本状态（当前台本、上传进度）
  useRoleStore        → 角色状态（角色列表、合并操作）
  useLineStore        → 台词状态（台词列表、编辑状态）
  useTTSStore        → TTS 状态（生成任务、试听音频）
  useConfigStore      → 配置状态（MiMo API Key、默认音色）
  ```

- **组件树**：
  ```
  App
  ├── Layout（侧边栏 + 主内容区）
  ├── HomePage
  │   └── UploadArea（拖拽上传 + 进度条）
  ├── AnalysisPage
  │   └── ProgressIndicator（步骤条 + 百分比）
  ├── RoleListPage
  │   ├── RoleCard（角色卡片 + 性格标签）
  │   └── MergeDialog（合并角色对话框）
  ├── LineEditorPage
  │   ├── LineTable（台词表格 + 情感标签编辑）
  │   └── AudioPlayer（单句试听播放器）
  ├── TTSGeneratePage
  │   ├── VoiceSelector（音色选择器）
  │   └── TaskProgress（生成进度 + 下载按钮）
  └── ConfigPage
      └── ApiKeyForm（MiMo API Key 配置表单）
  ```

#### 4. `backend/app/api/endpoints/*.py`（API 路由实现）

**交付文件**：
- `backend/app/api/endpoints/upload.py` - 上传接口
- `backend/app/api/endpoints/analysis.py` - 分析状态接口
- `backend/app/api/endpoints/roles.py` - 角色管理接口
- `backend/app/api/endpoints/lines.py` - 台词管理接口
- `backend/app/api/endpoints/tts.py` - TTS 接口
- `backend/app/api/endpoints/voices.py` - 音色管理接口
- `backend/app/api/endpoints/config.py` - 配置接口

#### 5. `backend/app/services/*.py`（业务逻辑层）

**交付文件**：
- `backend/app/services/file_parser.py` - 文件解析服务（txt → 结构化数据）
- `backend/app/services/role_analyzer.py` - 角色分析服务（调用 MiMo LLM API）
- `backend/app/services/emotion_tagger.py` - 情感标注服务（调用 MiMo LLM API）
- `backend/app/services/tts_service.py` - TTS 编排服务（调用 MiMo TTS API）
- `backend/app/services/audio_processor.py` - 音频处理服务（pydub 拼接）
- `backend/app/services/subtitle_generator.py` - 字幕生成服务（pysrt 生成 SRT）

---

### 👨🏻‍💻 寇豆码（工程师）

**交付目标**：实现所有源代码，确保功能完整、代码可读、可扩展

| 交付物 | 文件路径 | 内容说明 |
|---------|---------|---------|
| **后端完整实现** | `backend/app/**/*.py` | 所有 API 端点 + 业务逻辑 + 模型定义 |
| **前端完整实现** | `frontend/src/**/*.tsx` | 所有页面 + 组件 + 状态管理 |
| **AI 服务集成** | `backend/app/services/*_service.py` | MiMo LLM API 集成 + MiMo TTS API 集成 |
| **文件解析服务** | `backend/app/services/file_parser.py` | .txt 台本解析（角色识别 + 台词提取） |
| **音频处理服务** | `backend/app/services/audio_processor.py` | pydub 拼接多句音频 → 完整文件 |
| **数据库迁移脚本** | `backend/alembic/` 或 `backend/create_tables.py` | SQLite 建表脚本 |
| **配置文件** | `backend/.env.example`, `frontend/.env.example` | 环境变量模板 |
| **README + 快速开始** | `README.md`, `docs/setup.md` | 本地部署完整指南 |

**具体交付内容（按优先级）**：

#### P0：核心功能（必须完成）

**后端**：

1. **台本上传 API**（`backend/app/api/endpoints/upload.py`）
   - 接收 .txt 文件上传
   - 保存到本地文件系统（`data/uploads/`）
   - 创建 Script 记录（SQLite）
   - 触发异步分析任务（asyncio Task）
   - 返回 `script_id`

2. **文件解析服务**（`backend/app/services/file_parser.py`）
   - 读取 .txt 文件（UTF-8）
   - 正则表达式识别角色名 + 台词
   - 支持舞台说明（括号内容）
   - 返回结构化数据：`[{"role": "安欣", "line": "李哥，这么晚还在忙？", "line_number": 1}]`

3. **角色分析服务**（`backend/app/services/role_analyzer.py`）
   - 调用 MiMo LLM API（`https://platform.xiaomimimo.com/v1/chat/completions`）
   - Prompt 工程：输入所有角色名 + 台词样本 → 输出角色性格分析（JSON）
   - 示例 Prompt：
     ```
     你是一个台本分析专家。请分析以下台本中的角色特点。
     
     台本内容：
     {script_content}
     
     角色列表：
     {role_names}
     
     请为每个角色输出以下信息（JSON 格式）：
     {
       "roles": [
         {
           "name": "角色名",
           "gender": "male/female/unknown",
           "age_range": "20-30",
           "personality": ["性格特点1", "性格特点2"],
           "recommended_voice": "推荐音色（MiMo TTS 音色 ID）",
           "voice_params": {"pitch": 0, "speed": 1.0, "volume": 50}
         }
       ]
     }
     ```
   - 解析 JSON 响应，保存 Role 记录

4. **情感标注服务**（`backend/app/services/emotion_tagger.py`）
   - 调用 MiMo LLM API
   - Prompt 工程：输入每句台词 → 输出情感标签 + 语气 + 语速
   - 示例 Prompt：
     ```
     请为以下台词标注情感标签。
     
     角色：{role_name}
     性格：{personality}
     台词：{line_content}
     
     请输出（JSON 格式）：
     {
       "emotion_tag": "happy/sad/angry/...",
       "emotion_intensity": 3,
       "tone": "cheerful/melancholic/...",
       "speed": 1.0,
       "pitch": 0
     }
     ```
   - 批量处理所有台词，保存 Line 记录

5. **TTS 生成服务**（`backend/app/services/tts_service.py`）
   - 调用 MiMo TTS API（`https://platform.xiaomimimo.com/v1/audio/speech`）
   - 请求参数：
     ```python
     {
       "model": "mimo-v2.5-tts",
       "input": "台词内容",
       "voice": "音色 ID",
       "speed": 1.0,
       "pitch": 0,
       "volume": 50,
       "response_format": "wav"
     }
     ```
   - 保存音频文件到 `data/audio/` 目录

6. **音频拼接服务**（`backend/app/services/audio_processor.py`）
   - 使用 pydub 库拼接多句音频
   - 添加静音间隔（0.5 秒）
   - 输出完整 wav 文件

7. **字幕生成服务**（`backend/app/services/subtitle_generator.py`）
   - 使用 pysrt 库生成 SRT 字幕
   - 根据每句音频时长计算时间轴

**前端**：

1. **首页上传组件**（`frontend/src/pages/Home/UploadArea.tsx`）
   - 拖拽上传区域（react-dropzone）
   - 显示上传进度
   - 上传成功后跳转到分析进度页

2. **分析进度页**（`frontend/src/pages/Analysis/index.tsx`）
   - 步骤条（上传完成 → 解析中 → 角色分析 → 情感标注 → 完成）
   - 实时进度百分比（轮询 `/api/v1/scripts/{id}/status`）
   - 完成后跳转到角色列表页

3. **角色列表页**（`frontend/src/pages/Result/RoleList.tsx`）
   - 卡片列表展示所有角色
   - 显示角色名 + 性别 + 年龄 + 性格标签
   - 支持手动合并角色（多选 → 合并按钮）
   - 点击角色卡片进入台词编辑页

4. **台词编辑页**（`frontend/src/pages/Result/LineEditor.tsx`）
   - 表格展示所有台词（角色名 + 台词内容 + 情感标签）
   - 支持编辑情感标签（下拉选择）
   - 支持单句试听（点击播放按钮 → 调用 TTS API → 播放音频）
   - 保存修改后更新 Line 记录

5. **TTS 生成页**（`frontend/src/pages/TTS/index.tsx`）
   - 音色选择器（下拉列表，调用 `/api/v1/voices/mimo`）
   - 为每个学生分配音色
   - 生成按钮 → 创建 TTS 任务 → 轮询进度
   - 完成后显示下载链接（音频 + 字幕）

6. **API 服务层**（`frontend/src/services/api.ts`）
   - axios 封装所有 API 调用
   - 错误处理（react-hot-toast 提示）

7. **状态管理**（`frontend/src/store/*.ts`）
   - Zustand store 定义

#### P1：增强功能（应该完成）

1. **自定义音色上传**（`backend/app/api/endpoints/voices.py` + 前端页面）
   - 用户上传音频样本（mp3/wav）
   - 调用 MiMo TTS API 训练自定义音色
   - 保存 `mimo_voice_id`，供 TTS 生成时使用

2. **角色性格可视化**（前端组件）
   - 使用雷达图展示性格特点（Recharts）

3. **台词批量编辑**（前端组件）
   - 批量修改情感标签

4. **导出功能增强**
   - 支持导出为 MP3 格式（ffmpeg）
   - 支持导出为 ZIP（音频 + 字幕 + 角色设定 JSON）

#### P2：高级功能（可以后续迭代）

1. **台本对比功能**
   - 上传两个版本台本，对比角色变化

2. **社区分享功能**
   - 分享角色设定 + 音色配置（JSON 文件）

3. **移动端适配**
   - 响应式布局

---

### 👨🔬 严过关（QA 工程师）

**交付目标**：确保所有功能按验收标准工作，捕获并报告缺陷

| 交付物 | 文件路径 | 内容说明 |
|---------|---------|---------|
| **后端单元测试** | `backend/tests/test_*.py` | pytest 测试所有 API 端点 + 业务逻辑 |
| **前端组件测试** | `frontend/src/**/*.test.tsx` | React Testing Library 测试所有组件 |
| **API 集成测试** | `backend/tests/integration/` | 测试完整业务流程（上传→分析→TTS→导出） |
| **E2E 测试** | `e2e/` | Playwright 测试关键用户旅程 |
| **性能测试脚本** | `tests/performance/` | 测试 TTS 生成速度（100 句台词） |
| **缺陷报告模板** | `docs/bug-report-template.md` | Bug 报告格式说明 |
| **测试计划** | `docs/test-plan.md` | 测试范围 + 策略 + 进度安排 |

**具体交付内容**：

#### 1. 后端单元测试（`backend/tests/`）

**测试文件清单**：

- `test_upload.py` - 测试上传接口（正常上传、格式错误、文件过大）
- `test_file_parser.py` - 测试文件解析服务（各种台本格式）
- `test_role_analyzer.py` - 测试角色分析服务（Mock MiMo API）
- `test_emotion_tagger.py` - 测试情感标注服务（Mock MiMo API）
- `test_tts_service.py` - 测试 TTS 生成服务（Mock MiMo API）
- `test_audio_processor.py` - 测试音频拼接服务（输入多个 wav，输出完整 wav）
- `test_database.py` - 测试数据库模型（CRUD 操作）

**示例测试**（角色分析服务）：

```python
# backend/tests/test_role_analyzer.py
import pytest
from unittest.mock import Mock, patch
from app.services.role_analyzer import RoleAnalyzerService

def test_analyze_roles_success():
    """测试角色分析成功"""
    # Mock MiMo API 响应
    mock_response = {
        "choices": [{
            "message": {
                "content": '{"roles": [{"name": "安欣", "gender": "male", "age_range": "20-30", "personality": ["正义", "执着"]}]}'
            }
        }]
    }
    
    with patch("requests.post") as mock_post:
        mock_post.return_value = Mock(status_code=200, json=lambda: mock_response)
        
        service = RoleAnalyzerService()
        result = service.analyze("安欣：你好\n李哥：你好", ["安欣", "李哥"])
        
        assert len(result["roles"]) == 2
        assert result["roles"][0]["name"] == "安欣"
        assert result["roles"][0]["gender"] == "male"

def test_analyze_roles_api_error():
    """测试 MiMo API 调用失败"""
    with patch("requests.post") as mock_post:
        mock_post.return_value = Mock(status_code=500, text="Internal Server Error")
        
        service = RoleAnalyzerService()
        with pytest.raises(Exception):
            service.analyze("安欣：你好", ["安欣"])
```

#### 2. 前端组件测试（`frontend/src/**/*.test.tsx`）

**测试文件清单**：

- `UploadArea.test.tsx` - 测试上传组件（拖拽、点击、进度显示）
- `RoleList.test.tsx` - 测试角色列表组件（渲染、合并操作）
- `LineEditor.test.tsx` - 测试台词编辑组件（编辑、试听）
- `TTSGenerate.test.tsx` - 测试 TTS 生成组件（音色选择、生成进度）

**示例测试**（上传组件）：

```typescript
// frontend/src/pages/Home/UploadArea.test.tsx
import { render, screen, fireEvent } from "@testing-library/react";
import UploadArea from "./UploadArea";

test("上传区域显示正确", () => {
  render(<UploadArea onUploadSuccess={jest.fn()} />);
  
  expect(screen.getByText("拖拽台本文件到此处")).toBeInTheDocument();
  expect(screen.getByText("或点击选择文件")).toBeInTheDocument();
});

test("点击上传按钮触发文件选择", () => {
  const mockFn = jest.fn();
  render(<UploadArea onUploadSuccess={mockFn} />);
  
  const input = screen.getByLabelText("file-input");
  fireEvent.change(input, { target: { files: [new File(["content"], "test.txt")] } });
  
  expect(mockFn).toHaveBeenCalled();
});
```

#### 3. API 集成测试（`backend/tests/integration/`）

**测试流程清单**：

1. **完整流程测试**：上传台本 → 解析 → 角色分析 → 情感标注 → TTS 生成 → 导出
2. **错误恢复测试**：MiMo API 调用失败 → 重试机制
3. **并发测试**：同时上传 3 个台本，验证异步任务隔离

#### 4. E2E 测试（`e2e/`）

**测试场景清单**（Playwright）：

```typescript
// e2e/upload-and-generate.spec.ts
import { test, expect } from "@playwright/test";

test("完整流程：上传台本 → 分析 → 生成 TTS", async ({ page }) => {
  // 1. 打开首页
  await page.goto("http://localhost:5173");
  
  // 2. 上传台本
  await page.setInputFiles('input[type="file"]', "test-script.txt");
  await expect(page.getByText("上传成功")).toBeVisible();
  
  // 3. 等待分析完成
  await page.waitForSelector('text=分析完成', { timeout: 60000 });
  
  // 4. 查看角色列表
  await page.click('text=查看角色');
  await expect(page.getByText("安欣")).toBeVisible();
  
  // 5. 生成 TTS
  await page.click('text=生成语音');
  await page.waitForSelector('text=生成完成', { timeout: 120000 });
  
  // 6. 下载音频
  const download = await page.waitForEvent("download");
  expect(download.suggestedFilename()).toContain(".wav");
});
```

#### 5. 性能测试（`tests/performance/`）

**测试脚本清单**：

- `test_tts_speed.py` - 测试生成 100 句台词的耗时（目标 < 5 分钟）
- `test_concurrent_upload.py` - 测试同时上传 5 个台本，验证并发处理能力

---

## 三、开发阶段划分（T01 - T05）

根据架构设计 v3.0，将开发分为 5 个阶段：

### T01：项目基础设施搭建（P0，3 天）

**负责人**：寇豆码

**交付内容**：

1. **后端项目结构**（`backend/`）
   - `backend/app/main.py` - FastAPI 入口
   - `backend/app/config.py` - 配置管理（读取 `.env`）
   - `backend/app/database.py` - SQLite 连接初始化
   - `backend/requirements.txt` - Python 依赖清单
   - `backend/.env.example` - 环境变量模板

2. **前端项目结构**（`frontend/`）
   - Vite + React + TypeScript 项目初始化（`npm create vite@latest`）
   - 安装依赖：MUI、Tailwind CSS、Zustand、axios、react-query
   - `frontend/vite.config.ts` - Vite 配置（代理后端 API）
   - `frontend/tailwind.config.js` - Tailwind 配置
   - `frontend/.env.example` - 环境变量模板

3. **Docker 配置**（可选，本地开发可不用）
   - `docker-compose.yml` - 仅用于生产部署

4. **Git 仓库初始化**
   - 提交所有配置文件到 GitHub
   - 创建 `.gitignore`（排除 `.env`、`data/`、`__pycache__/` 等）

**验收标准**：

- [ ] `cd backend && pip install -r requirements.txt` 成功
- [ ] `cd frontend && npm install` 成功
- [ ] `cd backend && uvicorn app.main:app --reload` 启动成功，访问 `http://localhost:8000/docs` 看到 Swagger UI
- [ ] `cd frontend && npm run dev` 启动成功，访问 `http://localhost:5173` 看到首页

---

### T02：数据层与核心模型实现（P0，4 天）

**负责人**：寇豆码（高见远提供 Schema 支持）

**交付内容**：

1. **数据库模型**（`backend/app/models/*.py`）
   - Script、Role、Line、TTSTask、CustomVoice 模型定义
   - SQLAlchemy Base 定义

2. **Pydantic Schema**（`backend/app/schemas/*.py`）
   - ScriptCreate、ScriptResponse
   - RoleCreate、RoleResponse
   - LineCreate、LineResponse
   - TTSTaskCreate、TTSTaskResponse

3. **数据库迁移脚本**
   - `backend/create_tables.py` - 首次建表脚本
   - 或配置 Alembic（可选）

4. **前端类型定义**（`frontend/src/types/*.ts`）
   - `Script.ts` - 台本类型
   - `Role.ts` - 角色类型
   - `Line.ts` - 台词类型
   - `TTSTask.ts` - TTS 任务类型

**验收标准**：

- [ ] 运行 `python backend/create_tables.py` 成功创建所有表
- [ ] SQLite 数据库文件（`data/scriptmind.db`）生成在正确位置
- [ ] 前端 TypeScript 编译通过（`npm run build` 无类型错误）

---

### T03：文件解析与 AI 分析服务（P0，7 天）

**负责人**：寇豆码（高见远提供 API 集成支持）

**交付内容**：

1. **文件解析服务**（`backend/app/services/file_parser.py`）
   - 读取 .txt 文件
   - 正则表达式识别角色名 + 台词
   - 返回结构化数据

2. **角色分析服务**（`backend/app/services/role_analyzer.py`）
   - 调用 MiMo LLM API
   - Prompt 工程（见架构师交付内容）
   - 解析 JSON 响应

3. **情感标注服务**（`backend/app/services/emotion_tagger.py`）
   - 调用 MiMo LLM API
   - Prompt 工程
   - 批量处理所有台词

4. **异步任务编排**（`backend/app/tasks/analysis_tasks.py`）
   - 使用 asyncio 创建后台任务
   - 更新 Script 状态 + 进度

5. **上传 API 端点**（`backend/app/api/endpoints/upload.py`）
   - POST `/api/v1/scripts/upload`
   - 触发异步分析任务

6. **分析状态 API 端点**（`backend/app/api/endpoints/analysis.py`）
   - GET `/api/v1/scripts/{id}/status`

7. **前端上传页面**（`frontend/src/pages/Home/UploadArea.tsx`）
   - 拖拽上传
   - 进度显示

8. **前端分析进度页面**（`frontend/src/pages/Analysis/index.tsx`）
   - 步骤条
   - 实时进度轮询

**验收标准**：

- [ ] 上传示例台本（狂飙片段），成功触发分析任务
- [ ] 轮询 `/api/v1/scripts/{id}/status`，能看到进度从 0% → 100%
- [ ] 分析完成后，数据库 `scripts` 表 `status` = `completed`
- [ ] `roles` 表有正确的角色记录（角色名、性别、年龄、性格）
- [ ] `lines` 表有正确的台词记录（情感标签、语气、语速）
- [ ] 前端分析进度页正确显示步骤条 + 百分比

---

### T04：TTS 集成与语音生成（P0，7 天）

**负责人**：寇豆码（高见远提供 MiMo TTS API 集成支持）

**交付内容**：

1. **TTS 生成服务**（`backend/app/services/tts_service.py`）
   - 调用 MiMo TTS API
   - 保存音频文件到 `data/audio/`

2. **音频拼接服务**（`backend/app/services/audio_processor.py`）
   - 使用 pydub 拼接多句音频
   - 添加静音间隔

3. **字幕生成服务**（`backend/app/services/subtitle_generator.py`）
   - 使用 pysrt 生成 SRT 字幕

4. **TTS 任务编排**（`backend/app/tasks/tts_tasks.py`）
   - 异步生成完整音频
   - 更新任务状态 + 进度

5. **TTS API 端点**（`backend/app/api/endpoints/tts.py`）
   - POST `/api/v1/scripts/{id}/tts/generate`
   - GET `/api/v1/scripts/{id}/tts/{task_id}/status`

6. **试听 API 端点**（`backend/app/api/endpoints/tts.py`）
   - POST `/api/v1/scripts/{id}/tts/preview`

7. **音色管理 API 端点**（`backend/app/api/endpoints/voices.py`）
   - GET `/api/v1/voices/mimo`
   - POST `/api/v1/voices/custom`

8. **前端角色列表页面**（`frontend/src/pages/Result/RoleList.tsx`）
   - 显示角色卡片
   - 支持手动合并

9. **前端台词编辑页面**（`frontend/src/pages/Result/LineEditor.tsx`）
   - 表格展示台词
   - 编辑情感标签
   - 单句试听

10. **前端 TTS 生成页面**（`frontend/src/pages/TTS/index.tsx`）
    - 音色选择器
    - 生成进度
    - 下载链接

**验收标准**：

- [ ] 在台词编辑页，点击"试听"按钮，能听到正确的语音（调用 MiMo TTS API）
- [ ] 在 TTS 生成页，点击"生成"按钮，成功创建 TTS 任务
- [ ] 轮询任务状态，能看到进度从 0% → 100%
- [ ] 生成完成后，能下载完整 wav 音频文件
- [ ] 同时下载 SRT 字幕文件，用播放器打开验证时间轴正确
- [ ] 自定义音色上传成功，MiMo 返回 `voice_id`，可用于 TTS 生成

---

### T05：结果展示与系统集成（P1，5 天）

**负责人**：寇豆码

**交付内容**：

1. **导出功能**（`backend/app/api/endpoints/export.py`）
   - GET `/api/v1/scripts/{id}/export?format=wav,srt`
   - 返回 ZIP 文件（音频 + 字幕）

2. **配置页面**（`frontend/src/pages/Config/index.tsx`）
   - MiMo API Key 配置表单
   - 保存到 `.env` 或数据库

3. **历史记录页面**（可选）
   - 显示所有上传的台本
   - 支持重新打开

4. **错误处理完善**
   - 所有 API 调用添加 try-except
   - 前端显示友好的错误提示（react-hot-toast）

5. **README + 快速开始指南**（`README.md`、`docs/setup.md`）
   - 详细的本地部署步骤
   - 截图示例

6. **Git 提交规范**
   - 所有提交遵循 `<type>(<scope>): <subject>` 格式

**验收标准**：

- [ ] 点击"导出"按钮，成功下载 ZIP 文件（包含 wav + srt）
- [ ] 配置页面正确保存 MiMo API Key，后续 API 调用使用配置的 Key
- [ ] 所有 P0 功能验收标准通过
- [ ] 前端 TypeScript 编译通过，无警告
- [ ] 后端 pytest 测试通过（覆盖率 > 70%）
- [ ] README 中的快速开始步骤能在新机器上成功运行

---

## 四、提交规范（每次修改都提交）

**分支策略**：

- `main` - 生产分支（仅接受 PR 合并）
- `dev` - 开发分支（功能分支合并到此）
- `feature/*` - 功能分支（如 `feature/upload-api`）
- `fix/*` - 修复分支（如 `fix/tts-error-handling`）

**提交格式**：

```
<type>(<scope>): <subject>

<body>

Footer:
- 关联 Issue: #123
- 测试结果: 通过 / 待修复
```

**类型（type）**：

- `feat` - 新功能
- `fix` - Bug 修复
- `docs` - 文档更新
- `style` - 代码格式（不影响功能）
- `refactor` - 重构
- `test` - 测试相关
- `chore` - 构建/工具相关

**示例提交**：

```
feat(backend): 实现台本上传 API

- 添加 POST /api/v1/scripts/upload 端点
- 支持 .txt 文件上传
- 保存到 data/uploads/ 目录
- 创建 Script 记录（SQLite）

测试:
- [x] 上传示例台本成功
- [x] 格式错误返回 400
- [x] 文件过大（>10MB）返回 413

关联 Issue: #1
```

---

## 五、团队协作流程

### 日常协作

1. **每日站会**（可选，远程可用文字代替）
   - 昨天完成了什么
   - 今天计划做什么
   - 遇到什么阻碍

2. **代码审查（PR）**
   - 所有合并到 `dev` 的 PR 需要至少 1 人审查
   - 审查重点：代码质量、测试覆盖率、是否符合架构设计

3. **沟通工具**
   - GitHub Issues - 任务分配 + Bug 跟踪
   - GitHub Projects - 看板（Kanban）管理任务状态
   - （可选）微信群/Slack - 实时沟通

### 任务分配（GitHub Issues）

**示例 Issue**：

```markdown
# Issue #1: 实现台本上传 API

**负责人**: @koudouma (寇豆码)

**优先级**: P0

**估算**: 3 天

**描述**:
实现后端上传 API，支持用户上传 .txt 台本文件。

**验收标准**:
- [ ] POST /api/v1/scripts/upload 端点可用
- [ ] 接收 .txt 文件，保存到 data/uploads/
- [ ] 创建 Script 记录（SQLite）
- [ ] 返回 script_id
- [ ] 文件格式错误返回 400
- [ ] 文件过大（>10MB）返回 413

**依赖**:
- 无

**交付文件**:
- `backend/app/api/endpoints/upload.py`
- `backend/tests/test_upload.py`

**提交信息**:
feat(backend): 实现台本上传 API
```

---

## 六、风险与应对

| 风险 | 影响 | 应对措施 |
|------|------|---------|
| MiMo API 调用失败（网络/配额） | 分析/生成功能不可用 | 添加重试机制（3次）+ 友好错误提示 + 用户可配置备用 API Key |
| 长台本处理超时（> 1000 句） | 分析任务失败 | 分批处理 + Celery 异步任务 + 进度持久化 |
| TTS 生成成本高（MiMo 按量计费） | 用户不愿付费 | 本地部署，用户自己提供 API Key，成本由用户承担 |
| 文件解析准确率低（非常规格式） | 角色识别错误 | 用户可手动合并/修改角色 + 提供格式说明文档 |
| 音频拼接质量差（静音间隔不自然） | 听觉体验差 | 使用 pydub 添加交叉渐入渐出（crossfade） |

---

## 七、总结

**项目总时间估算**：约 26 天（1 人全栈开发）

| 阶段 | 时间 | 负责人 |
|------|------|--------|
| T01: 基础设施 | 3 天 | 寇豆码 |
| T02: 数据层 | 4 天 | 寇豆码 |
| T03: AI 分析 | 7 天 | 寇豆码 |
| T04: TTS 生成 | 7 天 | 寇豆码 |
| T05: 集成测试 | 5 天 | 寇豆码 |

**并行任务**（可加速）：

- 许清楚（产品经理）在 T01-T02 期间完成 PRD v3.0 + 格式规范 + 情感标签体系
- 高见远（架构师）在 T01 期间完成数据库 Schema + API 接口定义
- 严过关（QA）在 T03 完成后开始测试 T01-T03 的功能

**加速方案**（2 人开发）：

- 寇豆码负责后端（T01-T04）
- 另一名前端工程师负责前端（T01-T05）
- 总时间可缩短至 **15-20 天**

---

**文档版本**: v1.0  
**最后更新**: 2026-05-28  
**维护者**: 齐活林（主理人）
