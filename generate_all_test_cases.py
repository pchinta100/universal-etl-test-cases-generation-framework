#!/usr/bin/env python3
"""Batch-generate ETL test case CSV files for all pipeline configs."""

import argparse
import glob
import os
import re
import sys
from typing import List

from universal_etl_framework import UniversalETLTestFramework


def _sanitize_filename(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "_", value.strip())
    cleaned = cleaned.strip("._-")
    return cleaned or "ETL_Pipeline"


def _discover_configs(include_template: bool) -> List[str]:
    patterns = ["config_*.json", "example_config_*.json"]
    found = set()
    for pattern in patterns:
        for path in glob.glob(pattern):
            if os.path.isfile(path):
                found.add(path)

    if include_template and os.path.isfile("etl_config_template.json"):
        found.add("etl_config_template.json")

    return sorted(found)


def _output_name(config_path: str, framework: UniversalETLTestFramework) -> str:
    project_name = framework.config.get("project_name", "")
    if project_name:
        return f"{_sanitize_filename(project_name)}_TestCases.csv"
    base = os.path.splitext(os.path.basename(config_path))[0]
    return f"{_sanitize_filename(base)}_TestCases.csv"


def _generate_one(config_path: str, output_dir: str) -> str:
    framework = UniversalETLTestFramework(config_path)
    framework.generate_all_test_cases()
    output_file = os.path.join(output_dir, _output_name(config_path, framework))
    framework.export_to_csv(output_file)
    return output_file


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate ETL test case CSVs for all pipeline configs."
    )
    parser.add_argument(
        "configs",
        nargs="*",
        help="Optional explicit config files. If omitted, auto-discovers config_*.json and example_config_*.json.",
    )
    parser.add_argument(
        "--output-dir",
        default=".",
        help="Directory to write CSV outputs (default: current directory).",
    )
    parser.add_argument(
        "--include-template",
        action="store_true",
        help="Also include etl_config_template.json in auto-discovery.",
    )
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    configs = args.configs or _discover_configs(include_template=args.include_template)
    if not configs:
        print("No config files found.")
        print("Expected files like config_*.json or example_config_*.json")
        return 1

    print(f"Found {len(configs)} config(s).")
    failures = []

    for config in configs:
        try:
            output = _generate_one(config, args.output_dir)
            print(f"OK: {config} -> {output}")
        except Exception as exc:
            failures.append((config, str(exc)))
            print(f"FAIL: {config} -> {exc}")

    print("\nBatch summary")
    print(f"  Success: {len(configs) - len(failures)}")
    print(f"  Failed:  {len(failures)}")

    if failures:
        print("\nFailures:")
        for config, message in failures:
            print(f"  - {config}: {message}")
        return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())

