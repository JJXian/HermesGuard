from __future__ import annotations

import pytest
from hermesguard_mcp.server import build_demo_execution, mcp
from mcp import Client

DEMO_EXECUTION_ID = "01JHERMESGUARDDEMO00000001"


def test_demo_execution_is_deterministic_and_redacted() -> None:
    execution = build_demo_execution(DEMO_EXECUTION_ID)

    assert execution["anomalyCount"] == 7
    assert execution["facts"]["over48HoursCount"] == 2
    assert sum(group["count"] for group in execution["facts"]["warehouseGroups"]) == 7
    assert "credential" not in execution


def test_unknown_execution_is_rejected() -> None:
    with pytest.raises(ValueError, match="EXECUTION_NOT_FOUND"):
        build_demo_execution("missing")


@pytest.mark.asyncio
async def test_get_execution_result_through_mcp() -> None:
    async with Client(mcp) as client:
        result = await client.call_tool(
            "get_execution_result",
            {"execution_id": DEMO_EXECUTION_ID},
        )

    assert result.structured_content is not None
    assert result.structured_content["executionId"] == DEMO_EXECUTION_ID
    assert result.structured_content["anomalyCount"] == 7
