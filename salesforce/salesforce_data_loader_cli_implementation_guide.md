# Proposal: Salesforce Data Loader CLI Implementation Guide

เอกสารนี้เสนอแนวทางการติดตั้งและกำหนดค่า Salesforce Data Loader ผ่าน Command Line Interface (CLI) เพื่อทำ Automation สำหรับการนำเข้า/ส่งออกข้อมูล

## 1. บทนำ (Overview)

การใช้งาน Data Loader ผ่าน CLI ช่วยให้สามารถตั้งเวลา (Schedule) การทำงานได้อัตโนมัติ ลดภาระงาน Manual และลดความผิดพลาดจากผู้ใช้งาน เหมาะสำหรับงานประเภท Nightly Job หรือ Data Migration ที่ต้องทำซ้ำๆ

## 2. สิ่งที่ต้องเตรียม (Prerequisites)

1. **JDK (Java Development Kit)**: เวอร์ชัน 11 หรือใหม่กว่า (รวมอยู่ใน Installer ของ Data Loader รุ่นใหม่แล้ว)
2. **Salesforce Data Loader**: ติดตั้งเวอร์ชันล่าสุด
3. **Salesforce Account**: Username, Password และ Security Token (ถ้ารันนอก Trusted IP Network)
4. **Directory Structure**: ควรจัดเตรียมโฟลเดอร์สำหรับเก็บไฟล์ต่างๆ ให้เป็นระเบียบ เช่น:

    ```
    /Users/chanon/dataloader/
    ├── bin/          (ไฟล์ program data loader)
    ├── conf/         (ไฟล์ config xml และ map sdl)
    ├── data/         (ไฟล์ csv ข้อมูลสำหรับ import)
    ├── log/          (ไฟล์ log output: success/error)
    └── certs/        (เก็บ key สำหรับ encrypt)
    ```

## 3. ขั้นตอนการดำเนินการ (Implementation Steps)

### Step 1: สร้าง Key สำหรับการเข้ารหัส (Encryption Key Generation)

เพื่อความปลอดภัยสูงที่สุด เราจะไม่เก็บ Password เป็น Plain Text ในไฟล์ Config

1. เปิด Terminal
2. ไปที่โฟลเดอร์ `bin` ของ Data Loader (เช่น `/Applications/Data Loader.app/Contents/MacOS/`)
3. รันคำสั่งสร้าง Key:

    ```bash
    ./encrypt.bat -k /Users/chanon/dataloader/certs/key.txt
    ```

    *(หมายเหตุ: บน Mac/Linux ใช้ `.sh` แทน `.bat`)*

### Step 2: เข้ารหัสรหัสผ่าน (Password Encryption)

นำ **Salesforce Password + Security Token** มาเข้ารหัสด้วย Key ที่สร้างไว้

1. รันคำสั่ง:

    ```bash
    ./encrypt.bat -e <MyPassword><MyToken> /Users/chanon/dataloader/certs/key.txt
    ```

2. คัดลอกรหัสที่ได้ (Output String) เก็บไว้ใช้งานในขั้นตอนถัดไป

### Step 3: สร้างไฟล์จับคู่ฟิลด์ (Create Mapping File - .sdl)

สร้างไฟล์ `.sdl` ในโฟลเดอร์ `conf` เพื่อกำหนดการ Map ระหว่าง CSV Header และ Salesforce API Name

**ตัวอย่าง: `accountInsertMap.sdl`**

```properties
#Mapping values
#Mon Jan 20 17:50:00 ICT 2026
Name=Name
Phone=Phone
BillingCity=BillingCity
External_Id__c=External_Id__c
```

### Step 4: สร้างไฟล์ Configuration (process-conf.xml)

สร้างไฟล์ `process-conf.xml` ในโฟลเดอร์ `conf` ไฟล์นี้คือกุญแจสำคัญในการควบคุมการทำงาน

**ตัวอย่าง Configuration:**

```xml
<!DOCTYPE beans PUBLIC "-//SPRING//DTD BEAN//EN" "http://www.springframework.org/dtd/spring-beans.dtd">
<beans>
    <bean id="accountUpsertProcess" class="com.salesforce.dataloader.process.ProcessRunner" scope="prototype">
        <description>Account Upsert Job</description>
        <property name="name" value="accountUpsertProcess"/>
        <property name="configOverrideMap">
            <map>
                <entry key="sfdc.endpoint" value="https://login.salesforce.com"/>
                <entry key="sfdc.username" value="chanon@kpc.com"/>
                <!-- ใส่รหัสผ่านที่เข้ารหัสแล้วจาก Step 2 -->
                <entry key="sfdc.password" value="e8a68b75c..."/>
                <entry key="process.encryptionKeyFile" value="/Users/chanon/dataloader/certs/key.txt"/>

                <entry key="sfdc.timeoutSecs" value="600"/>
                <entry key="sfdc.loadBatchSize" value="200"/>
                <entry key="sfdc.entity" value="Account"/>
                <entry key="process.operation" value="upsert"/>
                <entry key="sfdc.externalIdField" value="External_Id__c"/>
                
                <entry key="process.mappingFile" value="/Users/chanon/dataloader/conf/accountInsertMap.sdl"/>
                <entry key="dataAccess.name" value="/Users/chanon/dataloader/data/accounts.csv"/>
                <entry key="dataAccess.type" value="csvRead"/>
                
                <entry key="process.outputSuccess" value="/Users/chanon/dataloader/log/success.csv"/>
                <entry key="process.outputError" value="/Users/chanon/dataloader/log/error.csv"/>
                <entry key="dataAccess.writeUTF8" value="true"/>
            </map>
        </property>
    </bean>
</beans>
```

### Step 5: คำสั่งรัน (Execution Command)

รูปแบบคำสั่งในการสั่งรัน Process:

```bash
process.bat "<path_to_conf_dir>" <process_bean_id>
```

**ตัวอย่าง:**

```bash
/Applications/Data\ Loader.app/Contents/MacOS/process.sh "/Users/chanon/dataloader/conf" accountUpsertProcess
```

## 4. แผนการทำ Automation (Automation Strategy)

หลังจากทดสอบรัน Manual ผ่านแล้ว สามารถนำคำสั่งไปตั้งเวลาทำงานได้

* **Windows**: ใช้ **Task Scheduler** สร้าง Task ให้รันไฟล์ `.bat` ที่เขียน Script เรียก Data Loader ตามเวลาที่กำหนด
* **Linux/Mac**: ใช้ **Crontab**
  * Example Cron (ทุกตี 2): `0 2 * * * /path/to/script/run_dataloader.sh`

## 5. ข้อดี/ข้อควรระวัง

* **ข้อดี**:
  * ทำงานได้รวดเร็วและรองรับข้อมูลปริมาณมาก (Bulk API)
  * Secure เพราะ Password ถูกเข้ารหัส
  * ตรวจสอบผลได้ง่ายจากไฟล์ Log Success/Error
* **ข้อควรระวัง**:
  * ต้องคอยอัปเดต Password ใน Config หาก User มีการเปลี่ยนรหัสผ่าน (แนะนำให้ใช้ API User หรือตั้งค่า Password Never Expire ถ้าเป็นไปได้)
  * ต้องมั่นใจว่าเครื่อง Server มี Access ออกไปยัง Salesforce Endpoint ได้

---
**เอกสารอ้างอิง:**

* [Data Loader Command Line Introduction](https://developer.salesforce.com/docs/atlas.en-us.dataLoader.meta/dataLoader/command_line_chapter.htm)
