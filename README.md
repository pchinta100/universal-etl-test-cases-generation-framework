# Universal ETL Testing Framework

A comprehensive Python framework for automatically generating test cases for any ETL project, supporting all ETL stages (Extraction, Transformation, Loading) with any combination of sources and targets.

## 📋 Overview

This framework simplifies ETL testing by:
- **Automatically generating test cases** based on your data schema
- **Supporting all ETL stages**: Extraction, Transformation, Loading
- **Working with any source/target combination**: MySQL, PostgreSQL, Snowflake, Hadoop, SAP, Oracle, CSV, etc.
- **Exporting to Jira format** for seamless test management integration
- **Covering comprehensive test scenarios**: Row counts, data validation, duplicates, business rules, integrity checks

## ✨ Features

✅ **Extraction Stage Tests**
- Row count validation
- Field completeness checks
- Data type validation (per field)
- Non-null/empty field validation
- Exact and key-based duplicate detection

✅ **Transformation Stage Tests**
- Data quality checks
- Business rule validation
- Data completeness percentage
- Referential integrity validation
- Boundary value testing

✅ **Loading Stage Tests**
- Target row count validation
- Data accuracy validation
- Constraint violation detection
- Primary key uniqueness checks
- Target data type validation
- Null validation at target
- Duplicate detection at target

✅ **Universal Configuration**
- Define any source/target system
- Flexible schema definition
- Custom validation rules
- Per-field constraints
- Allowed values validation

## 🚀 Quick Start

### 1. Installation
```bash
# No external dependencies required beyond Python standard library
python --version  # Python 3.7+
```

### 2. Create Configuration File
Create a `my_project.json` file:

```json
{
  "project_name": "Sales_ETL",
  "source": {
    "type": "MySQL",
    "name": "Sales Production DB"
  },
  "target": {
    "type": "Snowflake",
    "name": "Sales Data Warehouse"
  },
  "primary_key": "sales_id",
  "schema": {
    "sales_id": "integer",
    "customer_id": "integer",
    "amount": "decimal",
    "sale_date": "date",
    "status": "string"
  },
  "validation_rules": {
    "sales_id": {"required": true, "type": "integer", "min": 1},
    "amount": {"required": true, "type": "decimal", "min": 0, "max": 999999.99},
    "status": {"required": true, "allowed_values": ["COMPLETED", "PENDING", "CANCELLED"]}
  },
  "etl_stages": [
    {"stage": "extraction", "enabled": true},
    {"stage": "transformation", "enabled": true},
    {"stage": "loading", "enabled": true}
  ]
}
```

### 3. Generate Test Cases
```bash
python generate_test_cases.py my_project.json
```

Or with custom output filename:
```bash
python generate_test_cases.py my_project.json my_test_cases.csv
```

### 4. Import to Jira
1. Open Jira
2. Go to Test Management
3. Click "Import" 
4. Select the generated CSV file
5. Map columns if needed
6. Click "Import"

## 📁 Project Structure

```
Generate ETL Test cases/
├── universal_etl_framework.py          # Core framework (main code)
├── generate_test_cases.py              # CLI tool for easy usage
├── FRAMEWORK_GUIDE.md                  # Detailed documentation
├── README.md                           # This file
│
├── etl_config_template.json            # Template configuration
├── example_config_erp_to_datalake.json # Example: ERP to Hadoop
├── example_config_orders_snowflake.json# Example: MySQL to Snowflake
│
├── Universal_ETL_Test_Cases.csv        # Generated test cases (template)
├── ETL_Test_Cases.csv                  # Generated test cases (ERP example)
├── Orders_Snowflake_TestCases.csv      # Generated test cases (Orders example)
└── ERP_to_DataLake_TestCases.csv      # Generated test cases (Data Lake example)
```

## 📖 Configuration Guide

### Project Details
```json
{
  "project_name": "Your_Project_Name",
  "description": "Optional description"
}
```

### Source Configuration
```json
"source": {
  "type": "MySQL | PostgreSQL | Oracle | SAP_ERP | Hadoop | CSV | etc",
  "name": "Source System Name",
  "connection_details": {
    "host": "hostname",
    "port": 3306,
    "database": "db_name"
  }
}
```

### Target Configuration
```json
"target": {
  "type": "Snowflake | BigQuery | Redshift | PostgreSQL | etc",
  "name": "Target System Name",
  "connection_details": {}
}
```

### Schema Definition
Supported data types:
- `integer` - Numeric whole numbers
- `string` - Text data
- `date` - Date values (YYYY-MM-DD)
- `timestamp` - Date and time values
- `decimal` - Numeric with decimals
- `boolean` - True/False values
- `float` - Floating point numbers

```json
"schema": {
  "field_name": "integer",
  "customer_name": "string",
  "created_date": "date",
  "amount": "decimal"
}
```

### Validation Rules
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
    "required": true,
    "allowed_values": ["ACTIVE", "INACTIVE", "SUSPENDED"]
  },
  "name": {
    "required": true,
    "type": "string",
    "min_length": 2,
    "max_length": 255
  }
}
```

### ETL Stages
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

## 🎯 Test Cases Generated

### Extraction Stage (13 test cases in example)
- TC-1000: Row Count Validation
- TC-1001: Field Completeness
- TC-1002-1010: Data Type Validation (per field)
- TC-1011-1016: Non-Null Validation (per required field)
- TC-1017: Exact Duplicate Detection
- TC-1018: Primary Key Duplicate Detection

### Transformation Stage (6 test cases in example)
- TC-2000: Data Quality - Nulls
- TC-2001-2002: Business Rule Validation (per rule)
- TC-2003: Data Completeness %
- TC-2004: Referential Integrity
- TC-2005: Boundary Value Testing

### Loading Stage (13 test cases in example)
- TC-3000: Target Row Count
- TC-3001: Data Accuracy
- TC-3002: Constraint Violations
- TC-3003: Primary Key Uniqueness
- TC-3004-3008: Target Data Type Validation (per field)
- TC-3009-3014: Target Non-Null Validation (per required field)
- TC-3015: Target Duplicate Detection

## 💻 Usage Examples

### Example 1: Simple CSV to Database
```python
from universal_etl_framework import UniversalETLTestFramework

framework = UniversalETLTestFramework('simple_config.json')
framework.generate_all_test_cases()
framework.export_to_csv('test_cases.csv')
```

### Example 2: Enterprise ERP to Data Lake
```bash
python generate_test_cases.py example_config_erp_to_datalake.json
```

### Example 3: Programmatic Access
```python
framework = UniversalETLTestFramework('config.json')
tests = framework.generate_all_test_cases()

# Filter only extraction tests
extraction_tests = [t for t in tests if t['ETL Stage'] == 'Extraction']

# Export specific tests
framework.test_cases = extraction_tests
framework.export_to_csv('extraction_tests.csv')
```

## 📊 Output Format

CSV columns for Jira import:
| Column | Description |
|--------|-------------|
| Test Case ID | Unique identifier (TC-1000, TC-2000, etc) |
| Test Case Name | Human-readable test name |
| ETL Stage | Extraction / Transformation / Loading |
| Test Type | Count / Validation / Duplicate / Integrity / etc |
| Description | Detailed test description |
| Expected Result | What success looks like |
| Status | Not Executed / Passed / Failed |

## 🔧 Advanced Usage

### Multiple Projects
```python
import os
from universal_etl_framework import UniversalETLTestFramework

config_files = ['project1.json', 'project2.json', 'project3.json']

for config in config_files:
    framework = UniversalETLTestFramework(config)
    project_name = framework.config.get('project_name')
    framework.export_to_csv(f'{project_name}_tests.csv')
```

### Custom Test Case Filtering
```python
framework = UniversalETLTestFramework('config.json')
tests = framework.generate_all_test_cases()

# Get only Count tests
count_tests = [t for t in tests if t['Test Type'] == 'Count']

# Get only Transformation stage
transform_tests = [t for t in tests if t['ETL Stage'] == 'Transformation']

# Custom export with filtered tests
framework.test_cases = count_tests
framework.export_to_csv('count_tests_only.csv')
```

## 📋 Jira Integration

### Mapping CSV to Jira
When importing CSV to Jira:
1. **Summary** → Test Case Name
2. **Description** → Description
3. **Expected Result** → Should match
4. **Status** → Test Execution Status

### Workflow
1. Generate CSV from framework
2. Import to Jira
3. Assign tests to team members
4. Execute tests in pipeline
5. Update status in Jira
6. Generate reports

## 🎓 Best Practices

✅ **DO**
- Create configuration files for each project
- Define all required fields in validation rules
- Enable all ETL stages for comprehensive coverage
- Review generated tests before importing to Jira
- Keep configurations in version control
- Document custom validation rules

❌ **DON'T**
- Manually edit generated CSV files (regenerate instead)
- Forget to update config when schema changes
- Disable stages unnecessarily
- Leave validation rules empty
- Mix multiple projects in one config

## 🐛 Troubleshooting

### Issue: Config file not found
**Solution:** Use full path or ensure file is in current directory
```bash
python generate_test_cases.py /full/path/to/config.json
```

### Issue: Empty CSV output
**Solution:** Check `etl_stages` have `"enabled": true`

### Issue: Missing test cases
**Solution:** Verify `schema` and `validation_rules` are populated

### Issue: CSV not importing to Jira
**Solution:** Check CSV is UTF-8 encoded and column names match exactly

## 📞 Support

For issues or questions:
1. Review FRAMEWORK_GUIDE.md
2. Check example configurations
3. Verify JSON syntax in config file
4. Ensure schema matches your ETL design

## 📝 License

This framework is provided as-is for internal use.

## 🚀 Future Enhancements

Potential improvements:
- Python test code generation
- Integration with test execution tools
- Performance test case generation
- Security/compliance test cases
- Custom test template support
- Test case versioning

---

**Version:** 1.0  
**Last Updated:** March 2026  
**Compatibility:** Python 3.7+

## Batch Generation (All Pipelines)

Use `generate_all_test_cases.py` to generate CSV test cases for all pipeline configs in one run.

```powershell
cd "C:\Users\pchin\IdeaProjects\Generate ETL Test cases"
python generate_all_test_cases.py
```

This auto-discovers:
- `config_*.json`
- `example_config_*.json`

Optional examples:

```powershell
# Include template config too
python generate_all_test_cases.py --include-template

# Write outputs to a separate folder
python generate_all_test_cases.py --output-dir generated_csv

<img width="1361" height="786" alt="image" src="https://github.com/user-attachments/assets/b25a5bea-efe2-4de9-b99b-7df2b51e280f" />


# Run specific configs only
python generate_all_test_cases.py config_postgresql_bigquery.json config_csv_redshift.json
```
<img width="1361" height="786" alt="image" src="https://github.com/user-attachments/assets/045a17ff-1102-4863-b8f6-875bad1c5bda" />



