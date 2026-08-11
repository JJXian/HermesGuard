from __future__ import annotations

import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
VALIDATOR = (
    PROJECT_ROOT / "hermes/skills/ecommerce-inspection/scripts/validate_report.py"
)
FIXTURES = Path(__file__).parent / "fixtures"


def run_validator(fixture_name: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(VALIDATOR), str(FIXTURES / fixture_name)],
        check=False,
        capture_output=True,
        text=True,
    )


def test_valid_report_passes_schema_validation() -> None:
    result = run_validator("valid-report.json")

    assert result.returncode == 0
    assert "validation passed" in result.stdout


def test_invalid_report_fails_schema_validation() -> None:
    result = run_validator("invalid-report.json")

    assert result.returncode == 1
    assert "URGENT" in result.stderr
    assert "required property" in result.stderr

