"""
KPC TMS Table Configuration

Defines all source tables with their migration properties.
REQ: openspec/specs/extraction/spec.md
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class TableConfig:
    """Configuration for a single table migration."""

    table_name: str
    sf_object: str
    external_id_field: str
    priority: str  # "critical", "medium", "low"
    records_per_year: int
    partition_column: str = "CREATED_DATE"
    order_by: Optional[str] = None

    @property
    def is_large_table(self) -> bool:
        """Tables with >10M records/year need chunking."""
        return self.records_per_year > 10_000_000


# All source tables for migration
TABLES = [
    # Critical priority - largest tables
    TableConfig(
        table_name="KPS_T_SALES_MD",
        sf_object="KPS_Sales__c",
        external_id_field="External_ID__c",
        priority="critical",
        records_per_year=86_957_568,
        order_by="SALES_ID",
    ),
    TableConfig(
        table_name="KPS_T_SALESPAY_MD",
        sf_object="KPS_SalesPay__c",
        external_id_field="External_ID__c",
        priority="critical",
        records_per_year=36_461_318,
        order_by="SALESPAY_ID",
    ),
    TableConfig(
        table_name="KPS_T_SALES_M",
        sf_object="KPS_SalesM__c",
        external_id_field="External_ID__c",
        priority="critical",
        records_per_year=36_164_974,
        order_by="SALES_M_ID",
    ),
    # Medium priority
    TableConfig(
        table_name="KPS_T_SALES_APPRV_DETAIL",
        sf_object="KPS_SalesApprvDetail__c",
        external_id_field="External_ID__c",
        priority="medium",
        records_per_year=178_716,
    ),
    TableConfig(
        table_name="KPS_T_SALESBANK_MD",
        sf_object="KPS_SalesBank__c",
        external_id_field="External_ID__c",
        priority="medium",
        records_per_year=164_120,
    ),
    TableConfig(
        table_name="KPS_T_PREINV_REVSALES_D",
        sf_object="KPS_PreinvRevsalesD__c",
        external_id_field="External_ID__c",
        priority="medium",
        records_per_year=155_830,
    ),
    # Low priority - smaller tables
    TableConfig(
        table_name="KPS_T_SALES_APPRV",
        sf_object="KPS_SalesApprv__c",
        external_id_field="External_ID__c",
        priority="low",
        records_per_year=44_560,
    ),
    TableConfig(
        table_name="KPS_WEB_SALES",
        sf_object="KPS_WebSales__c",
        external_id_field="External_ID__c",
        priority="low",
        records_per_year=13_882,
    ),
    TableConfig(
        table_name="KPS_T_PREINV",
        sf_object="KPS_Preinv__c",
        external_id_field="External_ID__c",
        priority="low",
        records_per_year=6_118,
    ),
    TableConfig(
        table_name="KPS_T_PREINV_DETAIL",
        sf_object="KPS_PreinvDetail__c",
        external_id_field="External_ID__c",
        priority="low",
        records_per_year=6_118,
    ),
    TableConfig(
        table_name="KPS_T_PREINV_MIN",
        sf_object="KPS_PreinvMin__c",
        external_id_field="External_ID__c",
        priority="low",
        records_per_year=3_098,
    ),
    TableConfig(
        table_name="KPS_T_PREINV_REVGUA",
        sf_object="KPS_PreinvRevgua__c",
        external_id_field="External_ID__c",
        priority="low",
        records_per_year=3_020,
    ),
    TableConfig(
        table_name="KPS_T_PREINV_REVSALES_M",
        sf_object="KPS_PreinvRevsalesM__c",
        external_id_field="External_ID__c",
        priority="low",
        records_per_year=3_093,
    ),
    TableConfig(
        table_name="KPS_R_EMAIL_TENANT",
        sf_object="KPS_EmailTenant__c",
        external_id_field="External_ID__c",
        priority="low",
        records_per_year=436,
    ),
    TableConfig(
        table_name="KPS_R_EMAIL_SUPPLIER",
        sf_object="KPS_EmailSupplier__c",
        external_id_field="External_ID__c",
        priority="low",
        records_per_year=4,
    ),
    TableConfig(
        table_name="KPS_R_POS_SUPPLIER",
        sf_object="KPS_PosSupplier__c",
        external_id_field="External_ID__c",
        priority="low",
        records_per_year=4,
    ),
    # Product & Price migration (Multi-table JOIN → Product2)
    TableConfig(
        table_name="Product2",
        sf_object="Product2",
        external_id_field="ProductCode",
        priority="medium",
        records_per_year=100_000,
    ),
]


def get_table_config(table_name: str) -> TableConfig | None:
    """Get configuration for a specific table."""
    for table in TABLES:
        if table.table_name == table_name:
            return table
    return None


def get_tables_by_priority(priority: str) -> list[TableConfig]:
    """Get all tables with a specific priority."""
    return [t for t in TABLES if t.priority == priority]


def get_large_tables() -> list[TableConfig]:
    """Get tables that require chunking (>10M records/year)."""
    return [t for t in TABLES if t.is_large_table]
