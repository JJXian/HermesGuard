#!/usr/bin/env python3
"""Validate a HermesGuard inspection report against the bundled JSON Schema."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as file:
        return json.load(file)


def validate_report(report_path: Path) -> list[str]:
    schema_path = Path(__file__).resolve().parent.parent / "references" / "report-schema.json"
    schema = load_json(schema_path)
    report = load_json(report_path)
    validator = Draft202012Validator(schema)
    return [
        f"{'.'.join(str(part) for part in error.absolute_path) or '<root>'}: {error.message}"
        for error in sorted(
            validator.iter_errors(report), key=lambda item: list(item.absolute_path)
        )
    ]


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_report.py <report-json-path>", file=sys.stderr)
        return 2

    try:
        errors = validate_report(Path(sys.argv[1]))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"unable to read report: {exc}", file=sys.stderr)
        return 2

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print("report schema validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
