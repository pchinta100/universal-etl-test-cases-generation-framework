#!/usr/bin/env python3
"""
Quick Script to Generate ETL Test Cases
Usage: python generate_test_cases.py <config_file> [output_file]
"""

import os
import sys
from universal_etl_framework import UniversalETLTestFramework


def _pick_default_config() -> str:
    """Pick a sensible default config when no CLI args are provided."""
    candidates = [
        "config_postgresql_bigquery.json",
        "config_oracle_snowflake.json",
        "config_csv_redshift.json",
        "etl_config_template.json",
    ]
    for cfg in candidates:
        if os.path.exists(cfg):
            return cfg
    return ""


def main():
    if len(sys.argv) < 2:
        default_config = _pick_default_config()
        if not default_config:
            print("Usage: python generate_test_cases.py <config_file> [output_file]")
            print("\nNo configuration file found in current directory.")
            print("Expected one of:")
            print("  - config_postgresql_bigquery.json")
            print("  - config_oracle_snowflake.json")
            print("  - config_csv_redshift.json")
            print("  - etl_config_template.json")
            sys.exit(1)
        config_file = default_config
        output_file = "ETL_Test_Cases.csv"
        print(f"No config argument provided. Using default config: {config_file}")
    else:
        config_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else "ETL_Test_Cases.csv"

    try:
        # Initialize framework
        print(f"\n{'='*80}")
        print("UNIVERSAL ETL TEST FRAMEWORK")
        print(f"{'='*80}\n")

        framework = UniversalETLTestFramework(config_file)

        # Generate test cases
        print("Generating test cases...")
        framework.generate_all_test_cases()

        # Print summary
        framework.print_summary()

        # Export to CSV
        print(f"\nExporting test cases to: {output_file}")
        framework.export_to_csv(output_file)

        print("\n✓ Test case generation completed successfully!")
        print(f"✓ Output file: {output_file}")
        print(f"\nNext steps:")
        print(f"1. Review the CSV file: {output_file}")
        print(f"2. Import into Jira for execution")
        print(f"3. Execute tests in your ETL pipeline")
        print(f"\n{'='*80}\n")

    except FileNotFoundError as e:
        print(f"\n✗ Error: {e}")
        print(f"✗ Configuration file not found: {config_file}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

