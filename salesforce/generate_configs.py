import os
import sys
import xml.etree.ElementTree as ET
from xml.dom import minidom
from pathlib import Path

# Add project root to sys.path to allow importing from dags.config
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

try:
    from dags.config.tables_config import TABLES, TableConfig
    from dags.config.field_mappings import FIELD_MAPPINGS, FieldMapping
except ImportError as e:
    print(f"Error importing config: {e}")
    print("Please run this script from the 'salesforce' directory or ensure 'dags' is in PYTHONPATH.")
    sys.exit(1)

OUTPUT_DIR = PROJECT_ROOT / "salesforce" / "dataloader_conf"
MAPPING_DIR = OUTPUT_DIR / "mappings"
LOG_DIR = PROJECT_ROOT / "salesforce" / "logs"
DATA_DIR = PROJECT_ROOT / "salesforce" / "data"

# Salesforce Credentials - loaded at runtime via function
# to ensure we get the latest values from Airflow Variables
SF_ENDPOINT = ""
SF_USERNAME = ""
SF_PASSWORD = ""

def load_sf_credentials():
    """Load Salesforce credentials from Airflow Variables at runtime."""
    global SF_ENDPOINT, SF_USERNAME, SF_PASSWORD
    try:
        from airflow.models import Variable
        import json
        sf_config = json.loads(Variable.get("salesforce_config", default_var="{}"))
        SF_ENDPOINT = sf_config.get("endpoint", "https://test.salesforce.com")
        SF_USERNAME = sf_config.get("username", "")
        SF_PASSWORD = sf_config.get("encrypted_password", "")  # Use encrypted password
        print(f"DEBUG: Loaded SF_PASSWORD from 'encrypted_password': {SF_PASSWORD[:20] if SF_PASSWORD else 'EMPTY'}...")
        print(f"DEBUG: Full SF_CONFIG keys: {list(sf_config.keys())}")
        
        if not SF_PASSWORD:
            SF_PASSWORD = sf_config.get("password", "")
            print(f"DEBUG: Fallback to 'password' (plain text)")
    except Exception as e:
        print(f"⚠️ Failed to load Airflow Variable: {e}")
        # Fallback for non-Airflow context (e.g., testing)
        SF_ENDPOINT = os.getenv("SF_ENDPOINT", "https://test.salesforce.com")
        SF_USERNAME = os.getenv("SF_USERNAME", "")
        SF_PASSWORD = os.getenv("SF_PASSWORD", "")

# Encryption key path (not needed for plain text password)
ENC_KEY_FILE = f"{os.getenv('AIRFLOW_HOME', '/opt/airflow')}/salesforce/certs/key.txt"

def ensure_dirs():
    os.makedirs(MAPPING_DIR, exist_ok=True)
    os.makedirs(LOG_DIR, exist_ok=True)
    os.makedirs(DATA_DIR, exist_ok=True)
    print(f"Created directories at {OUTPUT_DIR}")

def generate_sdl(table_name: str, field_mapping: FieldMapping):
    """Generates .sdl mapping file content."""
    lines = [f"# Mapping for {table_name}"]
    
    for oracle_col, sf_field in field_mapping.mappings.items():
        lines.append(f"{oracle_col}={sf_field}")
    
    return "\n".join(lines)

def create_process_bean(table_config: TableConfig, field_mapping: FieldMapping, root: ET.Element):
    """Creates a bean element for the process-conf.xml"""
    bean = ET.SubElement(root, "bean", id=f"{table_config.table_name}_Process", 
                         attrib={"class": "com.salesforce.dataloader.process.ProcessRunner", "scope": "prototype"})
    
    description = ET.SubElement(bean, "description")
    description.text = f"Migration for {table_config.table_name}"
    
    prop_name = ET.SubElement(bean, "property", name="name", value=f"{table_config.table_name}_Process")
    
    # Config Override Map
    prop_config = ET.SubElement(bean, "property", name="configOverrideMap")
    map_elem = ET.SubElement(prop_config, "map")
    
    def add_entry(key, value):
        ET.SubElement(map_elem, "entry", key=key, value=str(value))

    # Connection Settings
    add_entry("sfdc.endpoint", SF_ENDPOINT)
    add_entry("sfdc.username", SF_USERNAME)
    add_entry("sfdc.password", SF_PASSWORD)  # Plain text password from env
    add_entry("sfdc.timeoutSecs", "600")
    add_entry("sfdc.loadBatchSize", "200")
    # Encryption needed for encrypted password
    add_entry("process.encryptionKeyFile", ENC_KEY_FILE)
    
    # Table Settings
    add_entry("sfdc.entity", table_config.sf_object)
    # add_entry("process.operation", "upsert") # Default to Upsert
    add_entry("process.operation", "insert") # Default to Upsert
    add_entry("sfdc.externalIdField", table_config.external_id_field)
    
    # Paths
    # Use AIRFLOW_HOME environment variable to determine absolute paths
    airflow_home = os.getenv("AIRFLOW_HOME", "/opt/airflow")
    base_path = f"{airflow_home}/salesforce"
    
    # process.mappingFile points to the .sdl file
    add_entry("process.mappingFile", f"{base_path}/dataloader_conf/mappings/{table_config.table_name}.sdl")
    
    # dataAccess.name points to the input CSV
    add_entry("dataAccess.name", f"{base_path}/data/{table_config.table_name}.csv")
    add_entry("dataAccess.type", "csvRead")
    
    # Output logs
    add_entry("process.outputSuccess", f"{base_path}/logs/{table_config.table_name}_success.csv")
    add_entry("process.outputError", f"{base_path}/logs/{table_config.table_name}_error.csv")
    
    # Priority & Performance Settings
    is_bulk = table_config.priority in ["critical", "medium"] or table_config.is_large_table
    add_entry("sfdc.useBulkApi", "true" if is_bulk else "false")
    
    if is_bulk:
        add_entry("sfdc.bulkApiSerialMode", "false")
        add_entry("sfdc.loadBatchSize", "10000")
    else:
        add_entry("sfdc.loadBatchSize", "200")

    add_entry("dataAccess.writeUTF8", "true")
    add_entry("dataAccess.readUTF8", "true")
    add_entry("sfdc.timezone", "Asia/Bangkok")
    add_entry("sfdc.debugMessages", "false")

import argparse

def generate_configs(table_name: str = None):
    """Generate Data Loader configs for all tables or a specific table.
    
    Args:
        table_name: Optional specific table name to generate config for.
                   If None, generates for all tables.
    """
    ensure_dirs()
    
    # Load credentials fresh from Airflow Variable
    load_sf_credentials()
    
    # Init XML Root
    doctype = '<!DOCTYPE beans PUBLIC "-//SPRING//DTD BEAN//EN" "http://www.springframework.org/dtd/spring-beans.dtd">'
    root = ET.Element("beans")
    
    # Filter tables if argument provided
    target_tables = TABLES
    if table_name:
        target_tables = [t for t in TABLES if t.table_name == table_name]
        if not target_tables:
            print(f"Error: Table {table_name} not found in configuration.")
            return False
            
    print(f"Found {len(target_tables)} tables configuration.")
    
    for table in target_tables:
        print(f"Processing {table.table_name}...")
        
        # 1. Generate SDL
        mapping = FIELD_MAPPINGS.get(table.table_name)
        if not mapping:
            print(f"Warning: No field mapping found for {table.table_name}. Skipping SDL generation.")
            continue
            
        sdl_content = generate_sdl(table.table_name, mapping)
        sdl_path = MAPPING_DIR / f"{table.table_name}.sdl"
        
        with open(sdl_path, "w", encoding="utf-8") as f:
            f.write(sdl_content)
            
        # 2. Add Bean to XML
        create_process_bean(table, mapping, root)
        
    # Write Process-conf.xml
    xml_str = minidom.parseString(ET.tostring(root)).toprettyxml(indent="    ")
    # Remove the default <?xml ...?> and add the DOCTYPE
    xml_str = xml_str.split("\n", 1)[1] 
    final_xml = doctype + "\n" + xml_str
    
    xml_path = OUTPUT_DIR / "process-conf.xml"
    with open(xml_path, "w", encoding="utf-8") as f:
        f.write(final_xml)

    print(f"\nSuccessfully generated configuration at: {OUTPUT_DIR}")
    print(f"- process-conf.xml")
    print(f"- {len(list(MAPPING_DIR.glob('*.sdl')))} mapping files (.sdl)")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Data Loader Configs")
    parser.add_argument("--table", help="Specific table to generate config for", default=None)
    args = parser.parse_args()
    generate_configs(table_name=args.table)
