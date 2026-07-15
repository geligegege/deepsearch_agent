<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=700&size=34&duration=2800&pause=900&color=6C63FF&center=true&vCenter=true&width=760&lines=DeepSearch;Multi-Agent+Research+Assistant" alt="DeepSearch animated title" />

### 一个人提问题，一支 AI 研究小队替你查资料

有人查数据库、有人翻企业知识库、有人搜索互联网，最后由主智能体把零散线索整理成一份像样的研究结果。

<p>
  <img src="https://img.shields.io/badge/Python-3.13+-3776AB?logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Deep_Agents-Multi--Agent-6C63FF" alt="Deep Agents" />
  <img src="https://img.shields.io/badge/FastAPI-WebSocket-009688?logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/RAGFlow-Knowledge_Base-1677FF" alt="RAGFlow" />
  <img src="https://img.shields.io/badge/Tavily-Web_Search-black" alt="Tavily" />
  <img src="https://img.shields.io/badge/Status-Developing-orange" alt="Status" />
</p>

<p>
  <a href="#-核心能力">核心能力</a> ·
  <a href="#-系统架构">系统架构</a> ·
  <a href="#-快速开始">快速开始</a> ·
  <a href="#-api">API</a>
</p>

</div>

---

> **它不像一个聊天机器人，更像一支临时组建的研究小队。**  
> 数据库专员负责找数字，知识库专员负责翻内部材料，网络搜索专员负责补充外部信息；主智能体负责分工、核对和交付报告。

## ✨ 核心能力

当一个问题无法靠“搜一下”解决时，就把它拆给不同的专业智能体：

- 多智能体协作：数据库、RAGFlow 知识库和 Tavily 联网搜索各司其职。
- 深度研究流程：主智能体拆解任务、选择数据源、整合证据并生成结果。
- 文件处理：支持用户上传文件，读取 Word、PDF、Markdown 等内容。
- 报告生成：可生成 Markdown，并转换为 PDF。
- 实时反馈：FastAPI 提供任务接口，WebSocket 推送执行状态。
- 会话隔离：每个任务使用独立的上传目录和输出目录。

## 🧭 系统架构

```text
用户任务 / 上传文件
        ↓
     主智能体
  ┌─────┼──────────┐
  ↓     ↓          ↓
数据库  RAGFlow   Tavily 联网搜索
  └─────┼──────────┘
        ↓
  Markdown / PDF 报告
        ↓
 WebSocket 实时反馈
```

## 🧰 技术栈

| 模块 | 技术 |
| --- | --- |
| 智能体 | Deep Agents、LangGraph、LangChain |
| API | FastAPI、WebSocket、Uvicorn |
| 知识库 | RAGFlow |
| 网络搜索 | Tavily |
| 数据库 | MySQL、SQLAlchemy |
| 文档 | python-docx、PyPDF、Markdown、WeasyPrint |
| 环境管理 | uv |

## 📁 目录结构

```text
deepsearch/
├── agent/              # 主智能体、提示词与专业子智能体
├── api/                # FastAPI、WebSocket 与进度监控
├── tools/              # 数据库、RAGFlow、搜索和文档工具
├── ragflow/            # RAGFlow SDK 示例与配置
├── prompt/             # YAML 提示词
├── sql/                # 示例数据库脚本
├── docker/
│   └── ragflow-main/   # 空占位目录，按说明下载官方 RAGFlow
├── .env.example        # 配置模板
└── pyproject.toml      # Python 依赖
```

## 🚀 快速开始

要求 Python 3.13+ 与 uv：

```bash
uv sync
cp .env.example .env
```

在 `.env` 中填写大模型、RAGFlow、Tavily 与 MySQL 配置。

### 获取 RAGFlow

RAGFlow 是独立的开源项目，不需要把它的完整源码和数 GB 离线镜像重复上传到本仓库。GitHub 包中的 `docker/ragflow-main/` 只是一个空占位目录。

在项目根目录运行：

```bash
rm -f docker/ragflow-main/.gitkeep
git clone --depth 1 https://github.com/infiniflow/ragflow.git docker/ragflow-main
```

随后使用官方 Docker Compose 方式启动：

```bash
cd docker/ragflow-main/docker
docker compose -f docker-compose.yml up -d
```

Docker 会自动拉取 RAGFlow、MySQL、MinIO、Elasticsearch/Infinity 和 Redis 等所需镜像，因此不需要仓库中原来的 `mysql.tar`、`minio.tar`、`elasticsearch.tar`、`infinity.tar` 和 `valkey.tar`。

启动 RAGFlow 后：

1. 打开 RAGFlow 页面并创建知识库。
2. 上传需要检索的企业文档。
3. 创建 API Key。
4. 将服务地址和密钥写入项目根目录的 `.env`：

```env
RAGFLOW_API_URL=http://127.0.0.1:9380
RAGFLOW_API_KEY=your-ragflow-api-key
```

如果 RAGFlow 部署在其他服务器，只需修改 API URL，不需要把它放在 DeepSearch 同一台机器上。

### 准备 MySQL

DeepSearch 的数据库子智能体需要单独配置业务数据库。可以导入项目提供的示例：

```bash
mysql -u root -p < sql/company_data.sql
```

然后修改 `.env` 中的 `MYSQL_HOST`、`MYSQL_PORT`、`MYSQL_USER`、`MYSQL_PASSWORD` 和 `MYSQL_DATABASE`。

### 启动 DeepSearch

```bash
uv run uvicorn api.server:app --host 0.0.0.0 --port 8000
```

OpenAPI 文档：`http://127.0.0.1:8000/docs`。

## 🔌 API

```http
POST /api/task
Content-Type: application/json

{"query": "分析公司经营数据并生成一份研究报告"}
```

返回 `thread_id` 后，连接 `WS /ws/{thread_id}` 接收实时进度。文件上传使用 `POST /api/upload`，结果文件可通过 `GET /api/files` 和 `GET /api/download` 获取。

## 🔐 安全建议

- 不要提交 `.env`、上传文件、生成报告、RAGFlow 官方源码和离线 Docker 镜像。
- 生产环境应限制 CORS、启用认证并限制上传文件格式与大小。
- 数据库账户应采用最小权限，研究型查询建议使用只读账户。
- 对联网搜索内容保留来源引用，并对生成报告进行人工复核。

## 📌 项目状态

项目处于开发阶段，适合作为多智能体研究与企业数据分析原型。

## 📦 GitHub 包说明

上传包只保留 DeepSearch 自身代码：

- 主智能体和三个专业子智能体
- FastAPI 与 WebSocket 服务
- RAGFlow、Tavily、MySQL 连接工具
- 文档读取与报告生成工具
- 示例 SQL、提示词和环境变量模板

以下内容均可重新获取或由运行过程生成，因此不会进入上传包：

| 省略内容 | 获取方式 |
| --- | --- |
| RAGFlow 官方源码 | 从官方 GitHub 仓库克隆 |
| MySQL、MinIO、ES、Infinity、Valkey 镜像 tar | 由 Docker Compose 在线拉取 |
| Python 虚拟环境 | 使用 `uv sync` 重新创建 |
| 上传文件与生成报告 | 运行时自动写入 `updated/`、`output/` |
| API Key 和数据库密码 | 复制 `.env.example` 后自行配置 |
