# Spec: Data Transformation

## ADDED Requirements

### Requirement: Field Mapping

The system MUST transform source columns to target Salesforce fields based on a configurable mapping file.

#### Scenario: Rename Columns

Given a DataFrame with column `SALES_ID`
And a mapping config `{"SALES_ID": "External_ID__c"}`
When transformation runs
Then the output DataFrame should have column `External_ID__c` containing the values from `SALES_ID`

### Requirement: Data Formatting

The system MUST format data types (Date, DateTime, Boolean) to match Salesforce API requirements.

#### Scenario: Date Formatting

Given a date value `2024-01-01 12:00:00`
When `to_sf_datetime` transformer is applied
Then the result should be `2024-01-01T12:00:00.000Z`
