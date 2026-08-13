# HermesGuard

HermesGuard 是一个基于确定性规则与 Hermes Agent 的电商智能巡检平台。规则引擎负责确认异常事实，Agent 负责查询上下文、解释原因并生成结构化报告。

## 当前进度

- 阶段 0：Hermes、DeepSeek、MCP 和结构化报告技术验证已完成。
- 阶段 1：Monorepo、API、Worker、Web、MySQL 和 Redis 基础框架。

## 环境要求

- Python 3.12
- uv
- Node.js 24
- Docker 与 Docker Compose

## 本地开发

安装依赖：

```bash
cp .env.example .env
make setup
```

启动 MySQL 和 Redis：

```bash
make infra-up
```

分别启动 API 与前端：

```bash
make api
make web
```

访问地址：

- 管理端：http://localhost:5173
- API 文档：http://localhost:8001/docs
- 存活检查：http://localhost:8001/health/live
- 就绪检查：http://localhost:8001/health/ready

启动完整容器环境：

```bash
make up
```

容器管理端地址为 http://localhost:8080。

## 质量检查

```bash
make check
```

该命令运行 Python 和前端的测试、Lint、类型检查及前端生产构建。

## 仓库结构

```text
apps/server      FastAPI、Celery Worker 与 Beat
apps/web         Vue 3 管理后台
apps/mcp-server  HermesGuard MCP Server
hermes/skills    Hermes Agent Skills
deploy           Docker Compose 与部署配置
docs             验证记录与设计文档
```
