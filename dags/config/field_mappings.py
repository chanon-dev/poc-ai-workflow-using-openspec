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
            "SALE_NO": "External_ID__c",  # Assuming SALE_NO is unique ID for now, or composite
            "CO_TENT_CODE": "Tenant_Code__c",
            "SHOP_CODE": "Store_Code__c",
            "SALE_DATE": "Sales_Date__c",
            "TOTAL_AMT_EXC_VAT": "Sales_Amount__c",
            "TOTAL_AMT_VAT": "Tax_Amount__c",
            "TOTAL_DISC_AMT_EXC_VAT": "Discount_Amount__c",
            "TOTAL_NET_AMT_EXC_VAT": "Net_Amount__c",
            "SALE_TYPE": "Payment_Type__c",
            "CREATEDDATE": "Oracle_Created_Date__c",
            "UPDATEDDATE": "Oracle_Updated_Date__c",
        },
        transformations={
            "SALE_DATE": TRANSFORM_SF_DATETIME,
            "CREATEDDATE": TRANSFORM_SF_DATETIME,
            "UPDATEDDATE": TRANSFORM_SF_DATETIME,
            "TOTAL_AMT_EXC_VAT": TRANSFORM_DECIMAL_2,
            "TOTAL_AMT_VAT": TRANSFORM_DECIMAL_2,
            "TOTAL_DISC_AMT_EXC_VAT": TRANSFORM_DECIMAL_2,
            "TOTAL_NET_AMT_EXC_VAT": TRANSFORM_DECIMAL_2,
        },
        lookups={
            "CO_TENT_CODE": ("Account", "Tenant_Code__c", "Account__c"),
            "SHOP_CODE": ("Store__c", "Store_Code__c", "Store__c"),
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
    # Product & Price migration (Multi-table JOIN → Product2)
    # Source: KPS_T_REQPROD_MD + KPS_T_APPRV_M + Reference tables
    "Product2": FieldMapping(
        sf_object="Product2",
        external_id="ProductCode",
        mappings={
            # Lookups (from APPRV_M + Reference tables)
            "TMS_Concession__c": "TMS_Concession__c",
            "TMS_Company_Name__c": "TMS_Company_Name__c",
            "TMS_Shop_Name__c": "TMS_Shop_Name__c",
            "TMS_Unit__c": "TMS_Unit__c",
            # Approval Info (from APPRV_M)
            "TMS_Start_Date__c": "TMS_Start_Date__c",
            "TMS_End_Date__c": "TMS_End_Date__c",
            "TMS_Document_No_Ticket_No__c": "TMS_Document_No_Ticket_No__c",
            # Product Info (from REQPROD_MD)
            "TMS_Bar_Code__c": "TMS_Bar_Code__c",
            "TMS_Product_Category_Code__c": "TMS_Product_Category_Code__c",
            "ProductCode": "ProductCode",
            "Name": "Name",
            "TMS_Product_Type__c": "TMS_Product_Type__c",
            "TMS_Price_EXC_VAT__c": "TMS_Price_EXC_VAT__c",
            "TMS_Price_INC_VAT__c": "TMS_Price_INC_VAT__c",
            "TMS_Ref_Source__c": "TMS_Ref_Source__c",
            "TMS_Ref_Price__c": "TMS_Ref_Price__c",
        },
        transformations={
            "TMS_Start_Date__c": TRANSFORM_SF_DATETIME,
            "TMS_End_Date__c": TRANSFORM_SF_DATETIME,
            "TMS_Price_EXC_VAT__c": TRANSFORM_DECIMAL_2,
            "TMS_Price_INC_VAT__c": TRANSFORM_DECIMAL_2,
            "TMS_Ref_Price__c": TRANSFORM_DECIMAL_2,
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
