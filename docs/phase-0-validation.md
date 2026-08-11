# 阶段 0：Hermes 与 MCP 最小技术验证记录

## 当前结论

截至 2026-08-11，本地链路已经完成以下验证：

```text
ecommerce-inspection Skill
→ Hermes 发现项目 MCP Server
→ MCP 内存客户端调用 get_execution_result
→ 生成/读取固定模拟事实
→ 报告 JSON Schema 正反例校验
```

真实 LLM 调用尚未执行。原因是调用会把 Skill 上下文和模拟巡检数据发送到 Anthropic，并产生少量 API 费用，需要用户明确授权。

## 环境

| 组件 | 当前状态 |
|---|---|
| 项目 Python | 3.12.13，由项目 `.venv` 隔离 |
| uv | 0.11.28 |
| Node.js | 24.14.0 |
| Docker | 29.5.3 |
| Docker Compose | 5.1.4 |
| Hermes Agent | 0.19.0，PyPI 安装 |
| Hermes Python | 3.11.15，与项目 Python 隔离 |
| MCP Python SDK | 项目端 2.0.0；Hermes 客户端 1.26.0 |

MCP SDK v2 服务端与 Hermes 当前使用的 v1 客户端已完成协议连接和工具发现。

## 已完成产物

- `hermes/skills/ecommerce-inspection/SKILL.md`
- `hermes/skills/ecommerce-inspection/references/report-schema.json`
- `hermes/skills/ecommerce-inspection/references/tool-usage-policy.md`
- `hermes/skills/ecommerce-inspection/references/anomaly-severity.md`
- `hermes/skills/ecommerce-inspection/scripts/validate_report.py`
- `apps/mcp-server/src/hermesguard_mcp/server.py`
- MCP 调用、未知执行和报告 Schema 自动化测试。
- Hermes MCP 配置：仅启用 `get_execution_result`。
- Hermes 外部 Skill 目录：`hermes/skills`。

## 验证结果

```text
pytest:          5 passed
ruff:            All checks passed
Skill validator: Skill is valid
Hermes MCP:      connected, 1/1 read-only tool enabled
```

有效报告通过 Schema 校验；非法严重级别、空 facts 和缺少必要字段的报告会被拒绝。

## 本地复现

安装依赖：

```bash
uv sync --all-packages
```

运行自动化测试：

```bash
.venv/bin/pytest -q
.venv/bin/ruff check .
```

验证报告：

```bash
.venv/bin/python \
  hermes/skills/ecommerce-inspection/scripts/validate_report.py \
  apps/mcp-server/tests/fixtures/valid-report.json
```

查看 Hermes MCP 状态：

```bash
~/.local/bin/hermes mcp list
```

## 待完成验收

在用户明确同意发送模拟数据并接受模型 API 费用后：

1. 使用 Hermes 预加载 `ecommerce-inspection` Skill。
2. 指定一个已配置的模型。
3. 分析 `01JHERMESGUARDDEMO00000001`。
4. 确认 Hermes 先调用 `get_execution_result`。
5. 保存模型返回 JSON 并运行 Schema 校验。
6. 检查报告数量、严重级别和仓库分组与工具事实一致。

