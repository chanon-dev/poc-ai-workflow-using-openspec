"""
Script สำหรับดึงข้อมูล Sample Data 20 records จากทุกตารางใน Oracle Database KPSDB
Output: แต่ละตารางจะถูกบันทึกเป็นไฟล์ CSV แยกกันใน folder 'database'

หมายเหตุ: ใช้ Thick Mode เพื่อรองรับ password verifier type 0x939
ต้องติดตั้ง Oracle Instant Client ก่อน:
  - macOS: brew install instantclient-basic
  - หรือ download จาก: https://www.oracle.com/database/technologies/instant-client/downloads.html
"""

import oracledb
import csv
import os
from datetime import datetime

# =============================================
# Initialize Thick Mode (ต้องทำก่อน connect)
# =============================================
ORACLE_CLIENT_PATH = "/Users/chanon/Desktop/TMS/files/instantclient_macos"

try:
    # พยายาม init thick mode ด้วย local path
    oracledb.init_oracle_client(lib_dir=ORACLE_CLIENT_PATH)
    print(f"✅ Oracle Thick Mode initialized from: {ORACLE_CLIENT_PATH}")
except oracledb.DatabaseError as e:
    print(f"⚠️  Could not initialize thick mode: {e}")
    print("   Script will try thin mode (may fail with some Oracle versions)")

# =============================================
# Database Connection Configuration
# =============================================
DB_CONFIG = {
    "host": "10.0.0.23",
    "port": 1521,
    "service_name": "KPSDB",
    "user": "kpsadmin",
    "password": "kpsadmin"
}

# จำนวน records ที่ต้องการดึง
SAMPLE_SIZE = 20

# Output folder
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "database")


def get_connection():
    """สร้าง connection ไปยัง Oracle Database"""
    dsn = oracledb.makedsn(
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"],
        service_name=DB_CONFIG["service_name"]
    )
    connection = oracledb.connect(
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        dsn=dsn
    )
    return connection


def get_all_tables(connection, owner="KPSADMIN"):
    """ดึงรายชื่อทุกตารางจาก database"""
    cursor = connection.cursor()
    
    # Query เพื่อดึงชื่อตารางทั้งหมด
    query = """
        SELECT table_name 
        FROM all_tables 
        WHERE owner = :owner
        ORDER BY table_name
    """
    cursor.execute(query, {"owner": owner.upper()})
    tables = [row[0] for row in cursor.fetchall()]
    cursor.close()
    
    return tables


def get_table_columns(connection, table_name, owner="KPSADMIN"):
    """ดึงชื่อ columns ของตาราง"""
    cursor = connection.cursor()
    
    query = """
        SELECT column_name 
        FROM all_tab_columns 
        WHERE owner = :owner AND table_name = :table_name
        ORDER BY column_id
    """
    cursor.execute(query, {"owner": owner.upper(), "table_name": table_name})
    columns = [row[0] for row in cursor.fetchall()]
    cursor.close()
    
    return columns


def extract_sample_data(connection, table_name, owner="KPSADMIN", sample_size=20):
    """ดึง sample data จากตาราง"""
    cursor = connection.cursor()
    
    # ใช้ FETCH FIRST สำหรับ Oracle 12c+
    # ถ้าใช้ Oracle เวอร์ชันเก่ากว่า ให้เปลี่ยนเป็น ROWNUM
    query = f"""
        SELECT * FROM {owner}.{table_name}
        FETCH FIRST {sample_size} ROWS ONLY
    """
    
    try:
        cursor.execute(query)
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        cursor.close()
        return columns, rows
    except oracledb.Error as e:
        print(f"  ⚠️  Error reading {table_name}: {e}")
        cursor.close()
        return [], []


def save_to_csv(table_name, columns, rows, output_dir):
    """บันทึกข้อมูลลง CSV file"""
    if not columns:
        return False
    
    filepath = os.path.join(output_dir, f"{table_name}.csv")
    
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(columns)  # Header
        
        for row in rows:
            # แปลง datetime objects เป็น string
            processed_row = []
            for value in row:
                if isinstance(value, datetime):
                    processed_row.append(value.isoformat())
                elif isinstance(value, bytes):
                    # แปลง bytes เป็น hex string (สำหรับ BLOB/RAW columns)
                    processed_row.append(value.hex() if len(value) <= 100 else f"[BLOB:{len(value)} bytes]")
                elif value is None:
                    processed_row.append("")
                else:
                    try:
                        processed_row.append(str(value))
                    except:
                        processed_row.append("[UNCONVERTIBLE]")
            writer.writerow(processed_row)
    
    return True


def main():
    """Main function"""
    print("=" * 60)
    print("🔄 KPSDB Sample Data Extractor")
    print("=" * 60)
    
    # สร้าง output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"📁 Output directory: {OUTPUT_DIR}")
    
    # Connect to database
    print(f"\n🔌 Connecting to {DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['service_name']}...")
    
    try:
        connection = get_connection()
        print("✅ Connected successfully!")
    except oracledb.Error as e:
        print(f"❌ Connection failed: {e}")
        return
    
    # Get all tables
    print("\n📋 Fetching table list...")
    tables = get_all_tables(connection)
    print(f"   Found {len(tables)} tables")
    
    # Extract data from each table
    print(f"\n📥 Extracting {SAMPLE_SIZE} records from each table...")
    print("-" * 60)
    
    success_count = 0
    error_count = 0
    empty_count = 0
    
    for i, table_name in enumerate(tables, 1):
        print(f"[{i}/{len(tables)}] {table_name}...", end=" ")
        
        columns, rows = extract_sample_data(connection, table_name, sample_size=SAMPLE_SIZE)
        
        if not columns:
            error_count += 1
            continue
        
        if not rows:
            print(f"(empty table)")
            empty_count += 1
            # Still save empty CSV with headers
            save_to_csv(table_name, columns, rows, OUTPUT_DIR)
            continue
        
        if save_to_csv(table_name, columns, rows, OUTPUT_DIR):
            print(f"✅ {len(rows)} records")
            success_count += 1
        else:
            print("❌ Failed to save")
            error_count += 1
    
    # Close connection
    connection.close()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Summary:")
    print(f"   ✅ Successfully extracted: {success_count} tables")
    print(f"   📭 Empty tables: {empty_count}")
    print(f"   ❌ Errors: {error_count}")
    print(f"   📁 Output: {OUTPUT_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    main()
