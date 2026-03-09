mental  incre# Universal ETL Test Framework - User Guide

## Overview
A comprehensive Python framework for generating ETL test cases automatically based on project configuration. Supports all ETL stages (Extraction, Transformation, Loading) and works with any source/target combination.

## Features
✓ Automatic test case generation from configuration files
✓ Supports all ETL stages: Extraction, Transformation, Loading
✓ Works with any source/target system combination
✓ Generates test cases optimized for Jira import
✓ Configurable validation rules and business rules
✓ Covers counts, data validation, duplicates, and integrity tests

## Quick Start

### Step 1: Create Configuration File
Create a JSON configuration file for your ETL project:

```json
{
  "project_name": "My_ETL_Project",
  "source": {
    "type": "CSV",
    "name": "Source System"
  },
  "target": {
    "type": "PostgreSQL",
    "name": "Target Database"
  },
  "primary_key": "id",
  "schema": {
    "id": "integer",
    "name": "string",
    "email": "string"
  },
  "validation_rules": {
    "id": {"required": true, "type": "integer", "min": 1},
    "name": {"required": true, "type": "string"}
  },
  "etl_stages": [
    {"stage": "extraction", "enabled": true},
    {"stage": "transformation", "enabled": true},
    {"stage": "loading", "enabled": true}
  ]
}
```

### Step 2: Run the Framework
```python
from universal_etl_framework import UniversalETLTestFramework

# Load configuration
framework = UniversalETLTestFramework('your_config.json')

# Generate test cases
framework.generate_all_test_cases()

# Display summary
framework.print_summary()

# Export to CSV for Jira
framework.export_to_csv('test_cases.csv')
```

### Step 3: Import to Jira
1. Open Jira
2. Go to Test Management or Xray
3. Import CSV file: `test_cases.csv`
4. Map columns as needed

## Configuration File Details

### Source/Target Configuration
```json
"source": {
  "type": "SAP_ERP | MySQL | Oracle | CSV | Hadoop | etc",
  "name": "Human readable name",
  "connection_details": {...}
}
```

### Schema Definition
Define all fields in your data:
```json
"schema": {
  "field_name": "data_type",
  "customer_id": "integer",
  "name": "string",
  "email": "string",
  "created_date": "date",
  "amount": "decimal"
}
```

Supported data types:
- integer, string, date, timestamp, decimal, boolean, float

### Validation Rules
Define business rules and constraints:
```json
"validation_rules": {
  "customer_id": {
    "required": true,
    "type": "integer",
    "min": 1,
    "max": 999999
  },
  "email": {
    "required": true,
    "format": "email"
  },
  "status": {
    "allowed_values": ["ACTIVE", "INACTIVE", "SUSPENDED"]
  }
}
```

### ETL Stages
Enable/disable specific stages:
```json
"etl_stages": [
  {
    "stage": "extraction",
    "enabled": true,
    "tests": ["row_count", "field_completeness", "data_types"]
  },
  {
    "stage": "transformation",
    "enabled": true,
    "tests": ["data_quality", "business_rules", "lookups"]
  },
  {
    "stage": "loading",
    "enabled": true,
    "tests": ["target_row_count", "data_accuracy", "constraints"]
  }
]
```

## Test Cases Generated

### Extraction Stage
- Row Count Validation
- Field Completeness
- Data Type Validation (per field)
- Non-Null Validation (per required field)
- Exact Duplicate Detection
- Primary Key Duplicate Detection

### Transformation Stage
- Data Quality - Nulls After Transformation
- Business Rule Validation (per validation rule)
- Data Completeness Percentage
- Referential Integrity - Lookup Validation
- Boundary Value Testing

### Loading Stage
- Target Row Count Validation
- Data Accuracy - Source to Target Match
- Constraint Violation Detection
- Primary Key Uniqueness at Target
- Target Data Type Validation (per field)
- Target Non-Null Validation (per required field)
- Target Duplicate Detection

## Example Configurations

### Example 1: ERP to Data Lake
See: `example_config_erp_to_datalake.json`
- Source: SAP ERP
- Target: Hadoop Data Lake
- Fields: Customer data with timestamps

### Example 2: Database to Snowflake
See: `example_config_orders_snowflake.json`
- Source: MySQL Database
- Target: Snowflake Warehouse
- Fields: Order data with status validations

## Output

### CSV Format for Jira
Columns:
- Test Case ID (TC-1000, TC-2000, etc)
- Test Case Name
- ETL Stage (Extraction, Transformation, Loading)
- Test Type (Count, Validation, Duplicate, etc)
- Description
- Expected Result
- Status (Not Executed)

### Summary Report
The framework prints:
- Total test cases count
- Breakdown by ETL stage
- Breakdown by test type
- Project source and target info

## Advanced Usage

### Customize Test Cases
```python
framework = UniversalETLTestFramework('config.json')
tests = framework.generate_all_test_cases()

# Modify or filter tests
filtered_tests = [t for t in tests if t['ETL Stage'] == 'Extraction']

# Export specific tests
framework.export_to_csv('extraction_only.csv')
```

### Generate for Multiple Projects
```python
projects = ['project1.json', 'project2.json', 'project3.json']

for project_config in projects:
    framework = UniversalETLTestFramework(project_config)
    framework.export_to_csv(f'{framework.config["project_name"]}_tests.csv')
```

## Best Practices

1. **Configuration Management**
   - Store configurations in version control
   - Use meaningful project names
   - Document custom validation rules

2. **Test Coverage**
   - Enable all ETL stages for comprehensive testing
   - Define all validation rules upfront
   - Include boundary values in validation rules

3. **Jira Integration**
   - Map test cases to requirements
   - Link to test execution plans
   - Update status as tests are executed

4. **Maintenance**
   - Review configuration when schema changes
   - Update validation rules based on business logic changes
   - Keep test cases in sync with ETL design

## Troubleshooting

### Config File Not Found
Make sure the JSON config file is in the same directory or provide full path

### Empty Test Cases
Verify `etl_stages` configuration has `"enabled": true`

### Missing Validations
Check `validation_rules` section defines all required fields

## Support

For issues or feature requests:
1. Check example configurations
2. Review ETL stage definitions
3. Verify schema and validation rules

## File Structure
```
Generate ETL Test cases/
├── universal_etl_framework.py       # Main framework
├── etl_config_template.json         # Template config
├── example_config_erp_to_datalake.json
├── example_config_orders_snowflake.json
└── Universal_ETL_Test_Cases.csv     # Generated output
```

