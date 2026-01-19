## ADDED Requirements

### Requirement: Field Mapping

The system SHALL transform Oracle column names to Salesforce field names based on configuration.

#### Scenario: Column rename

- **GIVEN** a mapping configuration SALES_ID → External_ID__c
- **WHEN** transformation is applied to extracted data
- **THEN** the column is renamed from SALES_ID to External_ID__c

#### Scenario: Unmapped columns

- **GIVEN** a column that has no mapping defined
- **WHEN** transformation is applied
- **THEN** the column is excluded from the output

---

### Requirement: Type Conversion

The system SHALL convert Oracle data types to Salesforce-compatible formats.

#### Scenario: DateTime conversion

- **GIVEN** an Oracle TIMESTAMP value
- **WHEN** the to_sf_datetime transformation is applied
- **THEN** the value is formatted as ISO 8601 (YYYY-MM-DDTHH:MM:SS.000Z)

#### Scenario: Decimal conversion

- **GIVEN** an Oracle NUMBER value
- **WHEN** the to_decimal_2 transformation is applied
- **THEN** the value is rounded to 2 decimal places

#### Scenario: Boolean conversion

- **GIVEN** an Oracle value of '1', 'Y', 'YES', or 'TRUE'
- **WHEN** the to_sf_boolean transformation is applied
- **THEN** the value is converted to True

#### Scenario: Null handling

- **GIVEN** a NULL value in any column
- **WHEN** any transformation is applied
- **THEN** the value remains NULL (not converted to empty string)

---

### Requirement: Text Truncation

The system SHALL truncate text fields that exceed Salesforce field limits.

#### Scenario: Long text truncation

- **GIVEN** a text value longer than the configured max_length (default 255)
- **WHEN** the truncate_text transformation is applied
- **THEN** the text is truncated to max_length characters

---

### Requirement: Transformation Pipeline

The system SHALL apply transformations in a consistent, configurable order.

#### Scenario: Multiple transformations

- **GIVEN** a column with both rename and type conversion configured
- **WHEN** transformation is applied
- **THEN** rename is applied first, then type conversion
- **AND** the output DataFrame contains only mapped columns
