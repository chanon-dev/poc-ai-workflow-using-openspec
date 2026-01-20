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

# Default Credentials (Should be encrypted in production)
SF_ENDPOINT = "https://login.salesforce.com"
SF_USERNAME = "chanon@kpc.com" # Placeholder
SF_PASSWORD_ENCRYPTED = "e8a68b7..." # Placeholder
ENC_KEY_FILE = "/opt/dataloader/certs/key.txt"

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
    add_entry("sfdc.password", SF_PASSWORD_ENCRYPTED)
    add_entry("process.encryptionKeyFile", ENC_KEY_FILE)
    
    # Table Settings
    add_entry("sfdc.entity", table_config.sf_object)
    add_entry("process.operation", "upsert") # Default to Upsert
    add_entry("sfdc.externalIdField", table_config.external_id_field)
    
    # Paths (Using absolute paths or placeholders)
    # Note: In real setup, these paths should match the container/server paths.
    # Here we use relative paths for the generating machine context or placeholders.
    # Let's use the local output paths for now, or standardized /opt/ paths if strictly following the doc.
    # Following the strategy doc which suggests /opt/dataloader/
    
    base_path = "/opt/dataloader"
    add_entry("process.mappingFile", f"{base_path}/config/mappings/{table_config.table_name}.sdl")
    add_entry("dataAccess.name", f"{base_path}/data/{table_config.table_name}.csv")
    add_entry("dataAccess.type", "csvRead")
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

def generate_configs():
    ensure_dirs()
    
    # Init XML Root
    doctype = '<!DOCTYPE beans PUBLIC "-//SPRING//DTD BEAN//EN" "http://www.springframework.org/dtd/spring-beans.dtd">'
    root = ET.Element("beans")
    
    print(f"Found {len(TABLES)} tables configuration.")
    
    for table in TABLES:
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
    generate_configs()
