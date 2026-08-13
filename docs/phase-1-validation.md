# 阶段 1：项目框架与基础设施验证记录

## 当前结论

截至 2026-08-12，HermesGuard Monorepo 基础框架已经完成，以下进程可以通过 Docker Compose 一起启动：

```text
Vue 3 Web（Nginx）
→ FastAPI
→ MySQL 8.4
→ Redis 7.4

Celery Worker ─┐
Celery Beat ───┴→ Redis 7.4
```

原有 MCP Server 继续作为独立 uv workspace 包运行，不与业务 API 进程耦合。

## 已完成产物

- `apps/server`：FastAPI 应用工厂、配置、健康检查、Celery Worker 与 Beat 入口。
- `apps/web`：Vue 3、TypeScript、Vite、Element Plus 管理端骨架。
- `deploy/docker-compose.yml`：MySQL、Redis、API、Worker、Beat、Web 编排。
- `.env.example`：本地开发环境变量示例。
- `Makefile`：安装、启动、停止和全量质量检查命令。
- `.github/workflows/ci.yml`：后端、前端和 Compose 三组 CI 检查。
- `README.md`：本地开发与运行入口。

## 健康检查

### 存活检查

```http
GET http://localhost:8001/health/live
```

```json
{"status":"ok","service":"hermesguard-server"}
```

### 就绪检查

```http
GET http://localhost:8001/health/ready
```

```json
{"status":"ready","dependencies":{"mysql":"up","redis":"up"}}
```

Web 通过 Nginx 的 `/api` 反向代理访问同一接口，避免生产环境跨域依赖。

## 端口

| 组件 | 宿主机端口 | 容器端口 |
|---|---:|---:|
| Web | 8080 | 80 |
| API | 8001 | 8000 |
| MySQL | 3307 | 3306 |
| Redis | 6380 | 6379 |

宿主机已有服务使用 `8000`，首次启动时 `3306` 也发生绑定冲突，因此项目默认使用隔离端口。容器之间仍使用各组件的标准端口。

## 验证结果

```text
pytest:             8 passed
ruff:               All checks passed
mypy:               8 source files, no issues
ESLint:             passed
Vue TypeScript:     passed
Vite build:         passed
Docker Compose:     valid
MySQL health:       healthy
Redis health:       healthy
FastAPI health:     healthy
Celery Worker:      connected, ready
Celery Beat:        started
Web → API proxy:    ready
Browser rendering:  passed
```

前端生产构建按需引入 Element Plus 组件，最终 JavaScript 主要分包约为 56 KB 与 72 KB，CSS 约为 40 KB，均为构建后的未压缩大小。

## 本地复现

安装依赖并准备环境：

```bash
cp .env.example .env
make setup
```

启动完整环境：

```bash
make up
```

访问管理端：

```text
http://localhost:8080
```

执行全部本地质量检查：

```bash
make check
```

停止容器但保留数据库卷：

```bash
make down
```

## 当前边界

- 本阶段只验证框架和依赖连通性，尚未创建业务表或 Alembic 迁移。
- 健康检查捕获驱动异常并返回依赖状态；统一错误码、日志与 `traceId` 在阶段 2 实现。
- Celery 当前没有业务任务；定时巡检与幂等调度在阶段 4 实现。
- Docker Compose 中的默认密码仅用于本地开发，正式环境必须通过安全配置注入。
