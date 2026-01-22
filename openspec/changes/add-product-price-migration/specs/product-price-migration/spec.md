# Capability: Product & Price Migration

## ADDED Requirements

### Requirement: Product Price Field Mapping

The system SHALL provide field mappings for `KPS_T_REQPROD_MD` table to Salesforce `Product2` object with the following fields:

- BARCODE → TMS_Bar_Code__c (Text)
- UNIT_CODE → TMS_Unit__c (Picklist)
- KPS_EFF_SDATE → TMS_Start_Date__c (DateTime)
- KPS_EFF_EDATE → TMS_End_Date__c (DateTime)
- STD_CATE_CODE → TMS_Product_Category_Code__c (Text)
- PROD_SERV_CODE → ProductCode (External ID)
- PROD_SERV_NAME → Name (Text)
- TMS_Product_Name_TH__c (Text, manual input)
- TMS_Product_Weight__c (Number)
- KPS_PRICE_EXC_VAT → TMS_Price_EXC_VAT__c (Number)
- KPS_PRICE_INC_VAT → TMS_Price_INC_VAT__c (Number)

#### Scenario: Extract product data from Oracle

- **WHEN** the extract task runs
- **THEN** data from `KPS_T_REQPROD_MD` joined with `KPS_T_APPRV_M` is exported to CSV
- **AND** date fields are formatted as ISO 8601 datetime strings
- **AND** numeric fields preserve 2 decimal places

### Requirement: Product Price Migration DAG

The system SHALL provide an Airflow DAG `migrate_product_price` that executes the following tasks in sequence:

1. Generate Data Loader configurations
2. Extract data from Oracle to CSV
3. Run Salesforce Data Loader
4. Audit results for errors

#### Scenario: Successful product migration

- **WHEN** the DAG completes successfully
- **THEN** Product2 records are created/updated in Salesforce
- **AND** success count is logged
- **AND** no errors appear in error log

#### Scenario: Data validation before load

- **WHEN** extracting product data
- **THEN** ProductCode (PROD_SERV_CODE) MUST NOT be null
- **AND** Name (PROD_SERV_NAME) MUST NOT be null
