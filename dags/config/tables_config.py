# dags/config/tables_config.py
"""
Table configuration for DAG Factory
แก้ไข config นี้เพื่อเพิ่ม/แก้ไข tables - ไม่ต้องเขียน DAG ใหม่
"""

TABLES_CONFIG = {
    # ==================== CRITICAL - Large Tables (Chunked) ====================
    "KPS_T_SALES_MD": {
        "sf_object": "KPS_Sales__c",
        "external_id": "External_ID__c",
        "priority": 1,
        "size_category": "critical",  # > 100M records
        "estimated_records": 261_000_000,
        "chunk_size": 500_000,
        "parallel_extract": 10,
        "parallel_load": 15,
        "schedule": None,  # Manual trigger only
        "dependencies": [],  # No dependencies
        "tags": ["critical", "sales"],
    },
    "KPS_T_SALESPAY_MD": {
        "sf_object": "KPS_SalesPay__c",
        "external_id": "External_ID__c",
        "priority": 2,
        "size_category": "critical",
        "estimated_records": 109_000_000,
        "chunk_size": 500_000,
        "parallel_extract": 8,
        "parallel_load": 15,
        "schedule": None,
        "dependencies": ["KPS_T_SALES_MD"],  # Must run after Sales
        "tags": ["critical", "payment"],
    },
    "KPS_T_SALES_M": {
        "sf_object": "KPS_SalesM__c",
        "external_id": "External_ID__c",
        "priority": 3,
        "size_category": "critical",
        "estimated_records": 108_000_000,
        "chunk_size": 500_000,
        "parallel_extract": 8,
        "parallel_load": 15,
        "schedule": None,
        "dependencies": [],
        "tags": ["critical", "sales"],
    },

    # ==================== MEDIUM - Medium Tables ====================
    "KPS_T_SALES_APPRV_DETAIL": {
        "sf_object": "KPS_Sales_Apprv_Detail__c",
        "external_id": "External_ID__c",
        "priority": 4,
        "size_category": "medium",  # 1M - 100M records
        "estimated_records": 536_000,
        "chunk_size": 500_000,
        "parallel_extract": 4,
        "parallel_load": 5,
        "schedule": None,
        "dependencies": ["KPS_T_SALES_APPRV"],
        "tags": ["medium", "approval"],
    },
    "KPS_T_SALESBANK_MD": {
        "sf_object": "KPS_SalesBank__c",
        "external_id": "External_ID__c",
        "priority": 4,
        "size_category": "medium",
        "estimated_records": 492_000,
        "chunk_size": 500_000,
        "parallel_extract": 4,
        "parallel_load": 5,
        "schedule": None,
        "dependencies": [],
        "tags": ["medium", "bank"],
    },
    "KPS_T_PREINV_REVSALES_D": {
        "sf_object": "KPS_PreInv_RevSales_D__c",
        "external_id": "External_ID__c",
        "priority": 5,
        "size_category": "medium",
        "estimated_records": 467_000,
        "chunk_size": 500_000,
        "parallel_extract": 4,
        "parallel_load": 5,
        "schedule": None,
        "dependencies": ["KPS_T_PREINV"],
        "tags": ["medium", "preinv"],
    },

    # ==================== LOW - Small Tables (Single Batch) ====================
    "KPS_T_SALES_APPRV": {
        "sf_object": "KPS_Sales_Apprv__c",
        "external_id": "External_ID__c",
        "priority": 6,
        "size_category": "small",  # < 1M records
        "estimated_records": 134_000,
        "chunk_size": None,  # Single batch
        "parallel_extract": 1,
        "parallel_load": 1,
        "schedule": None,
        "dependencies": [],
        "tags": ["small", "approval"],
    },
    "KPS_WEB_SALES": {
        "sf_object": "KPS_Web_Sales__c",
        "external_id": "External_ID__c",
        "priority": 6,
        "size_category": "small",
        "estimated_records": 42_000,
        "chunk_size": None,
        "parallel_extract": 1,
        "parallel_load": 1,
        "schedule": None,
        "dependencies": [],
        "tags": ["small", "web"],
    },
    "KPS_T_PREINV": {
        "sf_object": "KPS_PreInv__c",
        "external_id": "External_ID__c",
        "priority": 7,
        "size_category": "small",
        "estimated_records": 18_000,
        "chunk_size": None,
        "parallel_extract": 1,
        "parallel_load": 1,
        "schedule": None,
        "dependencies": [],
        "tags": ["small", "preinv"],
    },
    "KPS_T_PREINV_DETAIL": {
        "sf_object": "KPS_PreInv_Detail__c",
        "external_id": "External_ID__c",
        "priority": 8,
        "size_category": "small",
        "estimated_records": 18_000,
        "chunk_size": None,
        "parallel_extract": 1,
        "parallel_load": 1,
        "schedule": None,
        "dependencies": ["KPS_T_PREINV"],
        "tags": ["small", "preinv"],
    },
    "KPS_T_PREINV_MIN": {
        "sf_object": "KPS_PreInv_Min__c",
        "external_id": "External_ID__c",
        "priority": 8,
        "size_category": "small",
        "estimated_records": 9_000,
        "chunk_size": None,
        "parallel_extract": 1,
        "parallel_load": 1,
        "schedule": None,
        "dependencies": ["KPS_T_PREINV"],
        "tags": ["small", "preinv"],
    },
    "KPS_T_PREINV_REVGUA": {
        "sf_object": "KPS_PreInv_RevGua__c",
        "external_id": "External_ID__c",
        "priority": 8,
        "size_category": "small",
        "estimated_records": 9_000,
        "chunk_size": None,
        "parallel_extract": 1,
        "parallel_load": 1,
        "schedule": None,
        "dependencies": ["KPS_T_PREINV"],
        "tags": ["small", "preinv"],
    },
    "KPS_T_PREINV_REVSALES_M": {
        "sf_object": "KPS_PreInv_RevSales_M__c",
        "external_id": "External_ID__c",
        "priority": 8,
        "size_category": "small",
        "estimated_records": 9_000,
        "chunk_size": None,
        "parallel_extract": 1,
        "parallel_load": 1,
        "schedule": None,
        "dependencies": ["KPS_T_PREINV"],
        "tags": ["small", "preinv"],
    },

    # ==================== REFERENCE - Master Data ====================
    "KPS_R_EMAIL_TENANT": {
        "sf_object": "KPS_Email_Tenant__c",
        "external_id": "External_ID__c",
        "priority": 0,  # Load first (reference data)
        "size_category": "reference",
        "estimated_records": 1_308,
        "chunk_size": None,
        "parallel_extract": 1,
        "parallel_load": 1,
        "schedule": None,
        "dependencies": [],
        "tags": ["reference", "master"],
    },
    "KPS_R_EMAIL_SUPPLIER": {
        "sf_object": "KPS_Email_Supplier__c",
        "external_id": "External_ID__c",
        "priority": 0,
        "size_category": "reference",
        "estimated_records": 12,
        "chunk_size": None,
        "parallel_extract": 1,
        "parallel_load": 1,
        "schedule": None,
        "dependencies": [],
        "tags": ["reference", "master"],
    },
    "KPS_R_POS_SUPPLIER": {
        "sf_object": "KPS_POS_Supplier__c",
        "external_id": "External_ID__c",
        "priority": 0,
        "size_category": "reference",
        "estimated_records": 12,
        "chunk_size": None,
        "parallel_extract": 1,
        "parallel_load": 1,
        "schedule": None,
        "dependencies": [],
        "tags": ["reference", "master"],
    },

    # ==================== ADD MORE TABLES HERE ====================
    # Copy template below and fill in values
    # "TABLE_NAME": {
    #     "sf_object": "SF_Object__c",
    #     "external_id": "External_ID__c",
    #     "priority": 5,
    #     "size_category": "small",  # reference, small, medium, critical
    #     "estimated_records": 10_000,
    #     "chunk_size": None,  # None for single batch, number for chunking
    #     "parallel_extract": 1,
    #     "parallel_load": 1,
    #     "schedule": None,
    #     "dependencies": [],
    #     "tags": ["small"],
    # },
}

# ==================== Field Mappings ====================
FIELD_MAPPINGS = {
    "KPS_T_SALES_MD": {
        "SALES_ID": "External_ID__c",
        "TENANT_CODE": "Tenant_Code__c",
        "STORE_CODE": "Store_Code__c",
        "SALES_DATE": "Sales_Date__c",
        "SALES_AMOUNT": "Sales_Amount__c",
        "TAX_AMOUNT": "Tax_Amount__c",
        "DISCOUNT_AMOUNT": "Discount_Amount__c",
        "NET_AMOUNT": "Net_Amount__c",
        "PAYMENT_TYPE": "Payment_Type__c",
        "CREATED_DATE": "Oracle_Created_Date__c",
        "UPDATED_DATE": "Oracle_Updated_Date__c",
    },
    "KPS_T_SALESPAY_MD": {
        "SALESPAY_ID": "External_ID__c",
        "SALES_ID": "Sales_External_ID__c",  # Lookup reference
        "PAYMENT_METHOD": "Payment_Method__c",
        "PAYMENT_AMOUNT": "Payment_Amount__c",
        "PAYMENT_DATE": "Payment_Date__c",
        "CREATED_DATE": "Oracle_Created_Date__c",
    },
    # Add mappings for other tables...
    "DEFAULT": {
        # Default mapping: uppercase Oracle columns to SF convention
        # Will be auto-generated if not specified
    }
}

# ==================== Helper Functions ====================

def get_tables_by_priority() -> dict:
    """Group tables by priority for orchestration"""
    from collections import defaultdict
    priority_groups = defaultdict(list)
    for table, config in TABLES_CONFIG.items():
        priority_groups[config["priority"]].append(table)
    return dict(sorted(priority_groups.items()))


def get_tables_by_size() -> dict:
    """Group tables by size category"""
    from collections import defaultdict
    size_groups = defaultdict(list)
    for table, config in TABLES_CONFIG.items():
        size_groups[config["size_category"]].append(table)
    return dict(size_groups)


def get_dependencies_graph() -> dict:
    """Get dependency graph for topological ordering"""
    return {
        table: config["dependencies"]
        for table, config in TABLES_CONFIG.items()
    }


def get_total_estimated_records() -> int:
    """Get total estimated records across all tables"""
    return sum(config["estimated_records"] for config in TABLES_CONFIG.values())
