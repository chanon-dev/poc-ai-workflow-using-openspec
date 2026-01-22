# Salesforce Requirements for Data Migration

เอกสารนี้ระบุสิ่งที่ต้องรู้และเตรียมจาก Salesforce สำหรับการ migrate ข้อมูลผ่าน Salesforce Data Loader

---

## สรุปสิ่งที่ต้องรู้จาก Salesforce (Quick Reference)

### ข้อมูลที่ต้องขอจาก Salesforce Admin / Developer

| หมวด | สิ่งที่ต้องรู้ | ทำไมต้องรู้ | วิธีหา |
|------|--------------|------------|--------|
| **🔐 Authentication** | | | |
| | Username | ใช้ login เข้า API | Salesforce Admin สร้างให้ |
| | Password | ใช้ login เข้า API | User ตั้งเอง |
| | Security Token | ต่อท้าย password สำหรับ API | Setup → Reset Security Token |
| | Environment (Sandbox/Prod) | กำหนด endpoint URL | ถาม Admin ว่า migrate ไปที่ไหน |
| **📦 Object Schema** | | | |
| | Object API Name | ระบุ target object | Setup → Object Manager |
| | Field API Names ทั้งหมด | สร้าง field mapping | Object Manager → Fields |
| | Field Data Types | แปลงข้อมูลให้ถูก format | Object Manager → Fields |
| | Field Length/Precision | ตรวจสอบข้อมูลไม่เกิน limit | Object Manager → Fields |
| | Required Fields | ต้องมีค่าในทุก record | Object Manager → Fields |
| | External ID Field | ใช้สำหรับ Upsert operation | ต้องสร้างถ้ายังไม่มี |
| **🔗 Relationships** | | | |
| | Lookup/Master-Detail Fields | รู้ dependency order | Object Manager → Fields |
| | Related Object External IDs | map relationship ด้วย External ID | ตรวจสอบ parent objects |
| | Record Types (ถ้ามี) | ระบุ RecordTypeId ใน data | Object Manager → Record Types |
| **⚙️ Business Logic** | | | |
| | Validation Rules | อาจ block insert/update | Setup → Object → Validation Rules |
| | Triggers | อาจ affect performance | Setup → Object → Triggers |
| | Flows/Process Builder | อาจ affect performance | Setup → Flows |
| | Duplicate Rules | อาจ block insert | Setup → Duplicate Rules |
| **📊 Limits & Quotas** | | | |
| | Salesforce Edition | กำหนด API limits | Setup → Company Information |
| | Daily API Limit | วางแผนจำนวน records/วัน | Setup → System Overview |
| | Data Storage Limit | ตรวจสอบพื้นที่เพียงพอ | Setup → Storage Usage |

### Checklist สิ่งที่ต้องได้รับจาก Salesforce Team

```
Authentication
├── [ ] Username สำหรับ Integration User
├── [ ] Password
├── [ ] Security Token
└── [ ] Environment URL (Sandbox/Production)

Object Information (สำหรับแต่ละ Object)
├── [ ] Object API Name
├── [ ] Field List พร้อม Data Types
├── [ ] Required Fields
├── [ ] External ID Field Name
├── [ ] Lookup Relationships
└── [ ] Record Types (ถ้ามี)

Business Rules
├── [ ] List ของ Validation Rules ที่ active
├── [ ] List ของ Triggers
├── [ ] List ของ Flows/Process Builder
└── [ ] แผนการ disable automation ระหว่าง migration

Limits
├── [ ] Salesforce Edition
├── [ ] Daily Bulk API Limit
├── [ ] Current API Usage
└── [ ] Available Data Storage
```

### ตัวอย่างข้อมูลที่ต้องรู้สำหรับ KPS_Sales__c

```yaml
Object: KPS_Sales__c
External_ID: External_ID__c
Fields:
  - Name: External_ID__c
    Type: Text(50)
    Required: Yes
    External ID: Yes

  - Name: Sales_Date__c
    Type: Date
    Required: Yes
    Format: yyyy-MM-dd

  - Name: Amount__c
    Type: Currency(16,2)
    Required: No

  - Name: Customer__c
    Type: Lookup(Account)
    Required: No
    Relationship: Customer__r.External_ID__c

  - Name: Status__c
    Type: Picklist
    Required: Yes
    Values: [Draft, Active, Closed]

Validation Rules:
  - Amount_Must_Be_Positive: Amount__c > 0

Triggers:
  - KPS_SalesTrigger: After Insert, After Update
```

---

## 1. Authentication & Connection

### 1.1 Credentials ที่ต้องการ

| รายการ | คำอธิบาย | ตัวอย่าง |
|--------|----------|----------|
| **Username** | Salesforce username ที่มีสิทธิ์ API | `user@company.com.sandbox` |
| **Password** | รหัสผ่านของ user | `MyPassword123` |
| **Security Token** | Token สำหรับ API access | `XXXXXXXXXXXXXXXXXX` |
| **Endpoint** | Login URL | Sandbox: `https://test.salesforce.com` <br> Production: `https://login.salesforce.com` |

### 1.2 Password Encryption

Data Loader ต้องการ encrypted password (Password + Security Token):

```bash
# สร้าง encryption key
java -cp dataloader-xx.x.x-uber.jar com.salesforce.dataloader.security.EncryptionUtil -k

# Encrypt password
java -cp dataloader-xx.x.x-uber.jar com.salesforce.dataloader.security.EncryptionUtil \
  -e "MyPassword123SecurityToken" key.txt
```

### 1.3 User Permissions Required

User ที่ใช้ต้องมี permissions:

- [ ] **API Enabled** - Profile setting
- [ ] **Bulk API Hard Delete** (ถ้าต้องการ hard delete)
- [ ] **Modify All Data** หรือ Object-level permissions
- [ ] **View All Data** (สำหรับ export)

---

## 2. Target Object Information

### 2.1 Object Schema ที่ต้องรู้

สำหรับแต่ละ Salesforce Object ที่จะ migrate ต้องรู้:

| รายการ | คำอธิบาย | ตัวอย่าง |
|--------|----------|----------|
| **Object API Name** | ชื่อ API ของ Object | `KPS_Sales__c` |
| **External ID Field** | Field สำหรับ Upsert | `External_ID__c` |
| **All Field API Names** | ชื่อ API ของทุก field | `Name`, `Amount__c`, `Date__c` |
| **Field Data Types** | ประเภทข้อมูลของแต่ละ field | Text, Number, Date, Lookup |
| **Required Fields** | Field ที่บังคับกรอก | `Name`, `RecordTypeId` |
| **Field Length/Precision** | ความยาว/ทศนิยม | Text(255), Number(18,2) |

### 2.2 Migration Objects

| Source Table | Target Object | External ID Field |
|--------------|---------------|-------------------|
| KPS_T_SALES_MD | `KPS_Sales__c` | `External_ID__c` |
| KPS_T_SALESPAY_MD | `KPS_SalesPay__c` | `External_ID__c` |
| KPS_T_SALES_M | `KPS_SalesM__c` | `External_ID__c` |

### 2.3 วิธีดู Object Schema

**Option 1: Workbench**
```
https://workbench.developerforce.com
→ Info → Standard & Custom Objects → Select Object
```

**Option 2: SOQL Query**
```sql
-- ดู Field ทั้งหมดของ Object
SELECT QualifiedApiName, DataType, Length, Precision, Scale, IsRequired
FROM FieldDefinition
WHERE EntityDefinition.QualifiedApiName = 'KPS_Sales__c'
```

**Option 3: Salesforce CLI**
```bash
sf sobject describe --sobject KPS_Sales__c --json
```

---

## 3. Field Mapping

### 3.1 Mapping File Format (.sdl)

```properties
# Format: SOURCE_COLUMN=SF_Field_API_Name
# ตัวอย่าง mapping file

SALES_ID=External_ID__c
SALES_DATE=Sales_Date__c
AMOUNT=Amount__c
CUSTOMER_ID=Customer__r.External_ID__c
STATUS=Status__c
```

### 3.2 Data Type Mapping

| Oracle Type | Salesforce Type | หมายเหตุ |
|-------------|-----------------|----------|
| VARCHAR2 | Text | ตรวจสอบ length limit |
| NUMBER | Number/Currency | ตรวจสอบ precision/scale |
| DATE | Date/DateTime | Format: `yyyy-MM-dd` หรือ `yyyy-MM-ddTHH:mm:ss.SSSZ` |
| CLOB | Long Text Area | Max 131,072 characters |
| BLOB | - | ต้องใช้วิธีอื่น (Content Version) |

### 3.3 Relationship Fields

```properties
# Lookup by External ID
CUSTOMER_ID=Customer__r.External_ID__c

# Lookup by Salesforce ID
CUSTOMER_SF_ID=Customer__c
```

---

## 4. API Limits & Quotas

### 4.1 Bulk API Limits

| Limit | ค่า | หมายเหตุ |
|-------|-----|----------|
| **Records per batch** | 10,000 | Max สำหรับ Bulk API |
| **Batches per job** | 10,000 | - |
| **Jobs per 24 hours** | Varies by edition | Enterprise: 15,000 |
| **File size per batch** | 10 MB | - |
| **Characters per field** | 32,768 | สำหรับ Text fields |

### 4.2 Daily API Limits

```sql
-- ตรวจสอบ API Limits
SELECT
    FullName,
    Remaining,
    Max
FROM OrgLimit
WHERE Name = 'DailyBulkApiRequests'
```

### 4.3 Recommended Settings

```xml
<!-- process-conf.xml -->
<entry key="sfdc.useBulkApi" value="true"/>
<entry key="sfdc.bulkApiSerialMode" value="false"/>  <!-- Parallel mode -->
<entry key="sfdc.loadBatchSize" value="10000"/>
<entry key="sfdc.timeoutSecs" value="600"/>
```

---

## 5. Validation & Business Logic

### 5.1 สิ่งที่อาจ Block การ Insert/Update

- [ ] **Validation Rules** - ตรวจสอบ active validation rules
- [ ] **Required Fields** - Field ที่ต้องมีค่า
- [ ] **Unique Fields** - Field ที่ต้องไม่ซ้ำ
- [ ] **Lookup Filters** - Filter บน relationship fields
- [ ] **Record Types** - ถ้ามีหลาย record types

### 5.2 Performance Considerations

- [ ] **Triggers** - อาจต้อง disable ระหว่าง migration
- [ ] **Workflow Rules** - อาจต้อง disable
- [ ] **Process Builder / Flows** - อาจต้อง disable
- [ ] **Duplicate Rules** - อาจต้อง disable

### 5.3 วิธี Disable Automation (ชั่วคราว)

```apex
// Custom Setting หรือ Custom Metadata
public class TriggerHandler {
    public static Boolean bypassAll = false;

    public static void run() {
        if (bypassAll) return;
        // trigger logic
    }
}
```

---

## 6. Pre-Migration Checklist

### 6.1 Salesforce Setup

- [ ] สร้าง Integration User สำหรับ Data Loader
- [ ] ตั้งค่า Profile permissions (API Enabled, Object permissions)
- [ ] Generate Security Token
- [ ] สร้าง External ID fields บนทุก Objects
- [ ] ตรวจสอบ API Limits เพียงพอ

### 6.2 Object Preparation

- [ ] Document Object Schema (all fields)
- [ ] ระบุ Required fields
- [ ] ระบุ Lookup relationships และ dependency order
- [ ] ตรวจสอบ Validation Rules
- [ ] Plan สำหรับ disable triggers/workflows

### 6.3 Data Preparation

- [ ] สร้าง Field Mapping files (.sdl)
- [ ] ทดสอบ Data Type conversion
- [ ] Handle NULL values
- [ ] Handle Date/DateTime formats
- [ ] Handle special characters (UTF-8)

---

## 7. Post-Migration Verification

### 7.1 Record Count Verification

```sql
-- นับ records ใน Salesforce
SELECT COUNT() FROM KPS_Sales__c
```

### 7.2 Sample Data Verification

```sql
-- ตรวจสอบ sample records
SELECT Id, External_ID__c, Name, CreatedDate
FROM KPS_Sales__c
WHERE External_ID__c IN ('TEST001', 'TEST002')
```

### 7.3 Error Handling

ตรวจสอบ error files:
- `*_success.csv` - Records ที่สำเร็จ
- `*_error.csv` - Records ที่ fail พร้อม error message

---

## 8. Useful Resources

- [Salesforce Data Loader Guide](https://developer.salesforce.com/docs/atlas.en-us.dataLoader.meta/dataLoader/)
- [Bulk API Developer Guide](https://developer.salesforce.com/docs/atlas.en-us.api_asynch.meta/api_asynch/)
- [API Limits](https://developer.salesforce.com/docs/atlas.en-us.salesforce_app_limits_cheatsheet.meta/salesforce_app_limits_cheatsheet/)
