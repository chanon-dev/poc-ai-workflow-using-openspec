# Proposal: Add Product & Price Migration Pipeline

## Why

The "12_Product & Price" table is a Master data table required for the KPC TMS data migration to Salesforce. It contains ~164K records/year (~200K with growth) and has been confirmed ready for migration with field mappings defined in the data dictionary.

## What Changes

- Add field mapping configuration for `KPS_T_REQPROD_MD` (Product & Price) table
- Add SDL mapping file for Salesforce Data Loader
- Create a simple Airflow DAG to migrate Product & Price data to Salesforce `Product2` object
- Support the 11 confirmed fields from the sample CSV structure

## Impact

- Affected specs: None (new capability)
- Affected code:
  - `dags/config/field_mappings.py` - Add new mapping entry
  - `dags/migrate_product_price_dag.py` - New DAG file
  - `salesforce/dataloader_conf/mappings/KPS_T_REQPROD_MD.sdl` - New SDL file
  - `salesforce/dataloader_conf/process-conf.xml` - Add new process entry

## Field Mapping Summary

| Oracle Field | Salesforce Field | Type |
|--------------|-----------------|------|
| BARCODE | TMS_Bar_Code__c | Text(100) |
| UNIT_CODE | TMS_Unit__c | Picklist |
| KPS_EFF_SDATE | TMS_Start_Date__c | Date/Time |
| KPS_EFF_EDATE | TMS_End_Date__c | Date/Time |
| STD_CATE_CODE | TMS_Product_Category_Code__c | Text(100) |
| PROD_SERV_CODE | ProductCode | Text(255) |
| PROD_SERV_NAME | Name | Text(255) |
| (NEW) | TMS_Product_Name_TH__c | Text(255) |
| (NEW) | TMS_Product_Weight__c | Number(16,2) |
| KPS_PRICE_EXC_VAT | TMS_Price_EXC_VAT__c | Number(16,2) |
| KPS_PRICE_INC_VAT | TMS_Price_INC_VAT__c | Number(16,2) |

## Source Tables

- Primary: `KPS_T_REQPROD_MD` - Main product request data
- Secondary: `KPS_T_APPRV_M` - Approval data (joined for dates, document no)

## Target Object

- Salesforce Standard Object: `Product2`
- Uses standard `ProductCode` as External ID for upsert

## Data Volume

- ~164K records/year (estimated ~200K with growth factor)
- Low-priority table (compared to 87M+ sales tables)
- Suitable for simple single-batch migration
