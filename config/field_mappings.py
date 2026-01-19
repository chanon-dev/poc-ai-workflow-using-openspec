# config/field_mappings.py

"""
Field mappings for Oracle to Salesforce transformation.
Format: "ORACLE_TABLE_NAME": {"ORACLE_COLUMN": "Salesforce_Field__c"}
"""

FIELD_MAPPINGS = {
    "KPS_T_SALES_MD": {
        "SALES_ID": "External_ID__c",
        "SALES_DATE": "Sales_Date__c",
        "AMOUNT": "Amount__c",
        # Add actual mappings here based on requirements
    },
    "KPS_R_POS_SUPPLIER": {
        "SUPPLIER_CODE": "Supplier_Code__c",
        "SUPPLIER_NAME": "Name",
    }
}
