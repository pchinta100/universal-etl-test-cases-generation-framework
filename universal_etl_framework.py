import csv
import json
from typing import Dict, List, Any
from enum import Enum

class ETLStage(Enum):
    EXTRACTION = "extraction"
    TRANSFORMATION = "transformation"
    LOADING = "loading"

class UniversalETLTestFramework:
    """
    Universal framework for generating ETL test cases
    Supports multiple source/target types and all ETL stages
    """

    def __init__(self, config_file: str):
        """Initialize framework with project-specific configuration"""
        self.config = self.load_config(config_file)
        self.test_cases = []
        self.test_counter = {"extraction": 1000, "transformation": 2000, "loading": 3000}

    def load_config(self, config_file: str) -> Dict[str, Any]:
        """Load project configuration"""
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
            print(f"✓ Loaded configuration: {config.get('project_name', 'Unknown Project')}")
            return config
        except FileNotFoundError:
            print(f"✗ Config file not found: {config_file}")
            return {}

    def generate_extraction_tests(self) -> List[Dict[str, str]]:
        """Generate test cases for EXTRACTION stage"""
        tests = []
        schema = self.config.get('schema', {})
        source_type = self.config.get('source', {}).get('type', 'unknown')
        source_name = self.config.get('source', {}).get('name', 'Source')
        target_type = self.config.get('target', {}).get('type', 'unknown')
        target_name = self.config.get('target', {}).get('name', 'Target')

        # Row Count Tests
        tests.append({
            'Test Case ID': f'TC-{self.test_counter["extraction"]}',
            'Test Case Name': 'Row Count Validation',
            'ETL Stage': 'Extraction',
            'Test Type': 'Count',
            'Source': f'{source_type}',
            'Target': f'{target_type}',
            'Description': f'Verify correct number of rows extracted from {source_name} ({source_type})',
            'Expected Result': 'Row count matches expected value',
            'Status': 'Not Executed'
        })
        self.test_counter["extraction"] += 1

        # Field Completeness
        tests.append({
            'Test Case ID': f'TC-{self.test_counter["extraction"]}',
            'Test Case Name': 'Field Completeness',
            'ETL Stage': 'Extraction',
            'Test Type': 'Validation',
            'Source': f'{source_type}',
            'Target': f'{target_type}',
            'Description': f'Ensure all required fields from {source_type} are present',
            'Expected Result': f'All {len(schema)} columns present: {", ".join(schema.keys())}',
            'Status': 'Not Executed'
        })
        self.test_counter["extraction"] += 1

        # Data Type Validation Tests
        for field, dtype in schema.items():
            tests.append({
                'Test Case ID': f'TC-{self.test_counter["extraction"]}',
                'Test Case Name': f'Data Type Validation - {field}',
                'ETL Stage': 'Extraction',
                'Test Type': 'Validation',
                'Source': f'{source_type}',
                'Target': f'{target_type}',
                'Description': f'Verify field "{field}" is of type {dtype}',
                'Expected Result': f'Field "{field}" contains {dtype} values only',
                'Status': 'Not Executed'
            })
            self.test_counter["extraction"] += 1

        # Null/Empty Field Tests
        validation_rules = self.config.get('validation_rules', {})
        for field, rules in validation_rules.items():
            if rules.get('required'):
                tests.append({
                    'Test Case ID': f'TC-{self.test_counter["extraction"]}',
                    'Test Case Name': f'Non-Null Validation - {field}',
                    'ETL Stage': 'Extraction',
                    'Test Type': 'Validation',
                    'Source': f'{source_type}',
                    'Target': f'{target_type}',
                    'Description': f'Ensure required field "{field}" has no null/empty values',
                    'Expected Result': f'Field "{field}" has no null or empty values',
                    'Status': 'Not Executed'
                })
                self.test_counter["extraction"] += 1

        # Duplicate Detection
        primary_key = self.config.get('primary_key', 'id')
        tests.append({
            'Test Case ID': f'TC-{self.test_counter["extraction"]}',
            'Test Case Name': 'Exact Duplicate Detection',
            'ETL Stage': 'Extraction',
            'Test Type': 'Duplicate',
            'Source': f'{source_type}',
            'Target': f'{target_type}',
            'Description': 'Identify rows with identical data across all fields',
            'Expected Result': 'All duplicate rows are flagged and reported',
            'Status': 'Not Executed'
        })
        self.test_counter["extraction"] += 1

        tests.append({
            'Test Case ID': f'TC-{self.test_counter["extraction"]}',
            'Test Case Name': f'Key Duplicate Detection - {primary_key}',
            'ETL Stage': 'Extraction',
            'Test Type': 'Duplicate',
            'Source': f'{source_type}',
            'Target': f'{target_type}',
            'Description': f'Identify duplicate records on primary key "{primary_key}"',
            'Expected Result': f'No duplicate values in primary key "{primary_key}"',
            'Status': 'Not Executed'
        })
        self.test_counter["extraction"] += 1

        return tests

    def generate_transformation_tests(self) -> List[Dict[str, str]]:
        """Generate test cases for TRANSFORMATION stage"""
        tests = []
        schema = self.config.get('schema', {})
        source_type = self.config.get('source', {}).get('type', 'unknown')
        target_type = self.config.get('target', {}).get('type', 'unknown')

        # Data Quality Tests
        tests.append({
            'Test Case ID': f'TC-{self.test_counter["transformation"]}',
            'Test Case Name': 'Data Quality - Nulls After Transformation',
            'ETL Stage': 'Transformation',
            'Test Type': 'Data Quality',
            'Source': f'{source_type}',
            'Target': f'{target_type}',
            'Description': 'Verify no unexpected null values introduced during transformation',
            'Expected Result': 'All critical fields remain non-null after transformation',
            'Status': 'Not Executed'
        })
        self.test_counter["transformation"] += 1

        # Business Rule Tests
        validation_rules = self.config.get('validation_rules', {})
        for field, rules in validation_rules.items():
            if 'min' in rules or 'max' in rules:
                min_val = rules.get('min', 'N/A')
                max_val = rules.get('max', 'N/A')
                tests.append({
                    'Test Case ID': f'TC-{self.test_counter["transformation"]}',
                    'Test Case Name': f'Business Rule Validation - {field} Range',
                    'ETL Stage': 'Transformation',
                    'Test Type': 'Business Rule',
                    'Source': f'{source_type}',
                    'Target': f'{target_type}',
                    'Description': f'Validate {field} values are within acceptable range ({min_val}-{max_val})',
                    'Expected Result': f'All {field} values fall within range',
                    'Status': 'Not Executed'
                })
                self.test_counter["transformation"] += 1

        # Data Completeness
        tests.append({
            'Test Case ID': f'TC-{self.test_counter["transformation"]}',
            'Test Case Name': 'Data Completeness Percentage',
            'ETL Stage': 'Transformation',
            'Test Type': 'Data Quality',
            'Source': f'{source_type}',
            'Target': f'{target_type}',
            'Description': 'Calculate percentage of complete records after transformation',
            'Expected Result': 'Data completeness >= 95% (configurable)',
            'Status': 'Not Executed'
        })
        self.test_counter["transformation"] += 1

        # Referential Integrity
        tests.append({
            'Test Case ID': f'TC-{self.test_counter["transformation"]}',
            'Test Case Name': 'Referential Integrity - Lookup Validation',
            'ETL Stage': 'Transformation',
            'Test Type': 'Integrity',
            'Source': f'{source_type}',
            'Target': f'{target_type}',
            'Description': 'Validate all lookup/join keys have matching reference values',
            'Expected Result': 'No orphaned or unmatched reference keys',
            'Status': 'Not Executed'
        })
        self.test_counter["transformation"] += 1

        # Boundary Value Testing
        tests.append({
            'Test Case ID': f'TC-{self.test_counter["transformation"]}',
            'Test Case Name': 'Boundary Value Testing',
            'ETL Stage': 'Transformation',
            'Test Type': 'Edge Case',
            'Source': f'{source_type}',
            'Target': f'{target_type}',
            'Description': 'Test transformation logic with boundary and edge case values',
            'Expected Result': 'Transformation handles zero, negative, max values correctly',
            'Status': 'Not Executed'
        })
        self.test_counter["transformation"] += 1

        return tests

    def generate_loading_tests(self) -> List[Dict[str, str]]:
        """Generate test cases for LOADING stage"""
        tests = []
        target_type = self.config.get('target', {}).get('type', 'unknown')
        target_name = self.config.get('target', {}).get('name', 'Target')
        source_type = self.config.get('source', {}).get('type', 'unknown')
        schema = self.config.get('schema', {})

        # Row Count Validation at Target
        tests.append({
            'Test Case ID': f'TC-{self.test_counter["loading"]}',
            'Test Case Name': 'Target Row Count Validation',
            'ETL Stage': 'Loading',
            'Test Type': 'Count',
            'Source': f'{source_type}',
            'Target': f'{target_type}',
            'Description': f'Verify all transformed rows successfully loaded to {target_name} ({target_type})',
            'Expected Result': 'Source row count matches target row count',
            'Status': 'Not Executed'
        })
        self.test_counter["loading"] += 1

        # Data Accuracy at Target
        tests.append({
            'Test Case ID': f'TC-{self.test_counter["loading"]}',
            'Test Case Name': 'Data Accuracy - Source to Target Match',
            'ETL Stage': 'Loading',
            'Test Type': 'Accuracy',
            'Source': f'{source_type}',
            'Target': f'{target_type}',
            'Description': 'Verify data in target matches source after transformation',
            'Expected Result': 'All data values match expected transformations',
            'Status': 'Not Executed'
        })
        self.test_counter["loading"] += 1

        # Target Constraints
        tests.append({
            'Test Case ID': f'TC-{self.test_counter["loading"]}',
            'Test Case Name': 'Constraint Violation Detection',
            'ETL Stage': 'Loading',
            'Test Type': 'Integrity',
            'Source': f'{source_type}',
            'Target': f'{target_type}',
            'Description': f'Verify no {target_type} constraints violated during loading',
            'Expected Result': 'All records successfully loaded without constraint violations',
            'Status': 'Not Executed'
        })
        self.test_counter["loading"] += 1

        # Primary Key Validation at Target
        primary_key = self.config.get('primary_key', 'id')
        tests.append({
            'Test Case ID': f'TC-{self.test_counter["loading"]}',
            'Test Case Name': f'Primary Key Uniqueness at Target - {primary_key}',
            'ETL Stage': 'Loading',
            'Test Type': 'Integrity',
            'Source': f'{source_type}',
            'Target': f'{target_type}',
            'Description': f'Verify primary key "{primary_key}" is unique in target',
            'Expected Result': f'No duplicate primary key values in target',
            'Status': 'Not Executed'
        })
        self.test_counter["loading"] += 1

        # Data Type Validation at Target
        for field, dtype in schema.items():
            tests.append({
                'Test Case ID': f'TC-{self.test_counter["loading"]}',
                'Test Case Name': f'Target Data Type - {field}',
                'ETL Stage': 'Loading',
                'Test Type': 'Validation',
                'Source': f'{source_type}',
                'Target': f'{target_type}',
                'Description': f'Verify field "{field}" in target is of type {dtype}',
                'Expected Result': f'Field "{field}" has correct data type {dtype}',
                'Status': 'Not Executed'
            })
            self.test_counter["loading"] += 1

        # Null Values at Target
        validation_rules = self.config.get('validation_rules', {})
        for field, rules in validation_rules.items():
            if rules.get('required'):
                tests.append({
                    'Test Case ID': f'TC-{self.test_counter["loading"]}',
                    'Test Case Name': f'Target Non-Null Validation - {field}',
                    'ETL Stage': 'Loading',
                    'Test Type': 'Validation',
                    'Source': f'{source_type}',
                    'Target': f'{target_type}',
                    'Description': f'Verify required field "{field}" in target has no null values',
                    'Expected Result': f'No null values in required field "{field}"',
                    'Status': 'Not Executed'
                })
                self.test_counter["loading"] += 1

        # Duplicate Detection at Target
        tests.append({
            'Test Case ID': f'TC-{self.test_counter["loading"]}',
            'Test Case Name': 'Target Duplicate Detection',
            'ETL Stage': 'Loading',
            'Test Type': 'Duplicate',
            'Source': f'{source_type}',
            'Target': f'{target_type}',
            'Description': 'Verify no unintended duplicates loaded to target',
            'Expected Result': 'No duplicate rows in target (unless expected)',
            'Status': 'Not Executed'
        })
        self.test_counter["loading"] += 1

        return tests

    def generate_all_test_cases(self) -> List[Dict[str, str]]:
        """Generate test cases for all enabled ETL stages"""
        all_tests = []
        etl_stages = self.config.get('etl_stages', [])

        for stage_config in etl_stages:
            stage = stage_config.get('stage')
            if not stage_config.get('enabled', True):
                continue

            if stage == ETLStage.EXTRACTION.value:
                all_tests.extend(self.generate_extraction_tests())
            elif stage == ETLStage.TRANSFORMATION.value:
                all_tests.extend(self.generate_transformation_tests())
            elif stage == ETLStage.LOADING.value:
                all_tests.extend(self.generate_loading_tests())

        self.test_cases = all_tests
        return all_tests

    def export_to_csv(self, output_file: str) -> None:
        """Export test cases to CSV for Jira import"""
        if not self.test_cases:
            self.generate_all_test_cases()

        fieldnames = [
            'Test Case ID', 'Test Case Name', 'ETL Stage', 'Test Type',
            'Source', 'Target', 'Description', 'Expected Result', 'Status'
        ]

        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.test_cases)

        print(f"\n✓ Generated {len(self.test_cases)} test cases")
        print(f"✓ Exported to: {output_file}")

        # Print summary
        stages = {}
        for test in self.test_cases:
            stage = test.get('ETL Stage', 'Unknown')
            stages[stage] = stages.get(stage, 0) + 1

        print("\nTest Summary by Stage:")
        for stage, count in stages.items():
            print(f"  - {stage}: {count} tests")

    def print_summary(self) -> None:
        """Print framework summary"""
        if not self.test_cases:
            self.generate_all_test_cases()

        print("\n" + "="*80)
        print("UNIVERSAL ETL TEST FRAMEWORK - SUMMARY")
        print("="*80)
        print(f"\nProject: {self.config.get('project_name', 'Unknown')}")
        print(f"Source: {self.config.get('source', {}).get('type')} - {self.config.get('source', {}).get('name')}")
        print(f"Target: {self.config.get('target', {}).get('type')} - {self.config.get('target', {}).get('name')}")
        print(f"Primary Key: {self.config.get('primary_key', 'Not Set')}")
        print(f"\nTotal Test Cases Generated: {len(self.test_cases)}")

        stages = {}
        types = {}
        for test in self.test_cases:
            stage = test.get('ETL Stage', 'Unknown')
            test_type = test.get('Test Type', 'Unknown')
            stages[stage] = stages.get(stage, 0) + 1
            types[test_type] = types.get(test_type, 0) + 1

        print("\nBreakdown by ETL Stage:")
        for stage, count in sorted(stages.items()):
            print(f"  - {stage}: {count} tests")

        print("\nBreakdown by Test Type:")
        for test_type, count in sorted(types.items()):
            print(f"  - {test_type}: {count} tests")
        print("\n" + "="*80)

if __name__ == "__main__":
    # Example usage
    framework = UniversalETLTestFramework('etl_config_template.json')
    framework.generate_all_test_cases()
    framework.print_summary()
    framework.export_to_csv('Universal_ETL_Test_Cases.csv')

