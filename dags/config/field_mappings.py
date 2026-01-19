"""
Field Mappings Configuration

Defines Oracle→Salesforce field mappings and transformations.
REQ: openspec/specs/transformation/spec.md#field-mapping
REQ: openspec/specs/transformation/spec.md#type-conversion
"""

from dataclasses import dataclass, field
from typing import Callable

# Transformation function names (resolved at runtime)
TRANSFORM_SF_DATETIME = "to_sf_datetime"
TRANSFORM_DECIMAL_2 = "to_decimal_2"
TRANSFORM_BOOLEAN = "to_sf_boolean"
TRANSFORM_TRUNCATE_255 = "truncate_255"


@dataclass
class FieldMapping:
    """Mapping configuration for a single table."""

    sf_object: str
    external_id: str
    mappings: dict[str, str]  # Oracle column → SF field
    transformations: dict[str, str] = field(default_factory=dict)  # Column → transform func
    lookups: dict[str, tuple[str, str, str]] = field(default_factory=dict)


FIELD_MAPPINGS: dict[str, FieldMapping] = {
    "KPS_T_SALES_MD": FieldMapping(
        sf_object="KPS_Sales__c",
        external_id="External_ID__c",
        mappings={
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
        transformations={
            "SALES_DATE": TRANSFORM_SF_DATETIME,
            "CREATED_DATE": TRANSFORM_SF_DATETIME,
            "UPDATED_DATE": TRANSFORM_SF_DATETIME,
            "SALES_AMOUNT": TRANSFORM_DECIMAL_2,
            "TAX_AMOUNT": TRANSFORM_DECIMAL_2,
            "DISCOUNT_AMOUNT": TRANSFORM_DECIMAL_2,
            "NET_AMOUNT": TRANSFORM_DECIMAL_2,
        },
        lookups={
            "TENANT_CODE": ("Account", "Tenant_Code__c", "Account__c"),
            "STORE_CODE": ("Store__c", "Store_Code__c", "Store__c"),
        },
    ),
    "KPS_T_SALESPAY_MD": FieldMapping(
        sf_object="KPS_SalesPay__c",
        external_id="External_ID__c",
        mappings={
            "SALESPAY_ID": "External_ID__c",
            "SALES_ID": "Sales__c",  # Lookup to KPS_Sales__c
            "PAYMENT_METHOD": "Payment_Method__c",
            "PAYMENT_AMOUNT": "Payment_Amount__c",
            "CARD_NUMBER": "Card_Number__c",
            "CREATED_DATE": "Oracle_Created_Date__c",
        },
        transformations={
            "CREATED_DATE": TRANSFORM_SF_DATETIME,
            "PAYMENT_AMOUNT": TRANSFORM_DECIMAL_2,
        },
    ),
    "KPS_T_SALES_M": FieldMapping(
        sf_object="KPS_SalesM__c",
        external_id="External_ID__c",
        mappings={
            "SALES_M_ID": "External_ID__c",
            "TENANT_CODE": "Tenant_Code__c",
            "STORE_CODE": "Store_Code__c",
            "SALES_MONTH": "Sales_Month__c",
            "TOTAL_AMOUNT": "Total_Amount__c",
            "TOTAL_TRANSACTIONS": "Total_Transactions__c",
            "CREATED_DATE": "Oracle_Created_Date__c",
        },
        transformations={
            "CREATED_DATE": TRANSFORM_SF_DATETIME,
            "SALES_MONTH": TRANSFORM_SF_DATETIME,
            "TOTAL_AMOUNT": TRANSFORM_DECIMAL_2,
        },
    ),
    # Reference tables with simple mappings
    "KPS_R_EMAIL_TENANT": FieldMapping(
        sf_object="KPS_EmailTenant__c",
        external_id="External_ID__c",
        mappings={
            "TENANT_CODE": "External_ID__c",
            "EMAIL_ADDRESS": "Email_Address__c",
            "TENANT_NAME": "Tenant_Name__c",
            "ACTIVE": "Is_Active__c",
        },
        transformations={
            "ACTIVE": TRANSFORM_BOOLEAN,
        },
    ),
    "KPS_R_EMAIL_SUPPLIER": FieldMapping(
        sf_object="KPS_EmailSupplier__c",
        external_id="External_ID__c",
        mappings={
            "SUPPLIER_CODE": "External_ID__c",
            "EMAIL_ADDRESS": "Email_Address__c",
            "SUPPLIER_NAME": "Supplier_Name__c",
        },
    ),
    "KPS_R_POS_SUPPLIER": FieldMapping(
        sf_object="KPS_PosSupplier__c",
        external_id="External_ID__c",
        mappings={
            "SUPPLIER_CODE": "External_ID__c",
            "POS_ID": "POS_ID__c",
            "SUPPLIER_NAME": "Supplier_Name__c",
        },
    ),
}


def get_field_mapping(table_name: str) -> FieldMapping | None:
    """Get field mapping configuration for a table."""
    return FIELD_MAPPINGS.get(table_name)


def get_sf_object(table_name: str) -> str | None:
    """Get Salesforce object name for a table."""
    mapping = get_field_mapping(table_name)
    return mapping.sf_object if mapping else None
