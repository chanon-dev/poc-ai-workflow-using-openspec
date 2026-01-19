# OpenSpec Playbook: From Zero to Hero

คู่มือการใช้งาน OpenSpec ฉบับสมบูรณ์ สำหรับทีม KPC TMS Data Migration ครอบคลุมตั้งแต่เริ่มติดตั้งจนถึงการแก้ไขงานประจำวัน

> **⚠️ Important:** ทุกคำสั่ง (Commands) ต้องรันที่ **Project Root** (`/Users/chanon/Desktop/kpc-tms-data-migration`) เสมอ

---

## 🏗️ Use Case 1: เริ่มต้นโปรเจกต์ (Project Setup)

*ทำครั้งเดียวตอนเริ่มโปรเจกต์ หรือเมื่อ Developer คนใหม่เข้าทีม*

1. **ติดตั้ง OpenSpec (Global)**

    ```bash
    npm install -g @fission-ai/openspec
    ```

2. **Initialize Project**

    ```bash
    openspec init
    # เลือก Configuration ตามที่ต้องการ (ส่วนใหญ่กด Enter ผ่านได้เลย)
    ```

    *ผลลัพธ์:* จะได้โฟลเดอร์ `openspec/` ที่มี `specs/` (ว่างเปล่า) และ `changes/`

---

## ✨ Use Case 2: เริ่มทำฟีเจอร์ใหม่ (Add New Feature)

*เช่น: ต้องการเพิ่มระบบแจ้งเตือนผ่าน Email*

**Step 1: สร้าง Change Workspace**
ตั้งชื่อให้สื่อความหมาย (kebab-case) และมี verb นำหน้า

```bash
# Pattern: openspec/changes/<change-id>/specs/<capability-name>
mkdir -p openspec/changes/add-email-notification/specs/notification
```

**Step 2: เขียน Proposal (`proposal.md`)**
สร้างไฟล์ `openspec/changes/add-email-notification/proposal.md`

```markdown
# Change: Add Email Notification

## Why
User ต้องการทราบเมื่อ Migration เสร็จสิ้นโดยไม่ต้องเฝ้าหน้าจอ

## What Changes
- เพิ่มระบบส่ง Email เมื่อ DAG ทำงานจบ
- รองรับการ Config ผู้รับผ่าน Variable

## Impact
- New Capability: `notification`
```

**Step 3: เขียน Spec ใหม่ (`spec.md`)**
สร้างไฟล์ `openspec/changes/add-email-notification/specs/notification/spec.md`
> ใช้ `## ADDED Requirements` สำหรับฟีเจอร์ใหม่

```markdown
## ADDED Requirements

### Requirement: Completion Email
The system SHALL send an email summary upon migration completion.

#### Scenario: All Success
- **WHEN** all DAGs finished successfully
- **THEN** send email with subject "Migration Success" to configured recipients

#### Scenario: Partial Failure
- **WHEN** any DAG fails
- **THEN** send email with subject "Migration Logic Failed"
```

**Step 4: ตรวจสอบความถูกต้อง (Validate)**

```bash
openspec validate add-email-notification --strict
```

---

## 🔧 Use Case 3: แก้ไขฟีเจอร์เดิม (Modify Existing Feature)

*เช่น: ต้องการเปลี่ยน Subject Email จาก "Migration Success" เป็น "KPC Migration Done"*

**Step 1: สร้าง Change Workspace ใหม่**
ทำเหมือนฟีเจอร์ใหม่ แต่ตั้งชื่อให้ตรงกับสิ่งที่แก้

```bash
mkdir -p openspec/changes/update-email-subject/specs/notification
```

*สังเกต: โฟลเดอร์ปลายทางคือ `specs/notification` เหมือนเดิม เพราะเรากำลังแก้ capability เดิม*

**Step 2: เขียน Delta Spec (`spec.md`)**
สร้างไฟล์ `openspec/changes/update-email-subject/specs/notification/spec.md`
> ใช้ `## MODIFIED Requirements` และต้องก๊อปปี้ Requirement เดิมมาแก้

```markdown
## MODIFIED Requirements

### Requirement: Completion Email
The system SHALL send an email summary upon migration completion.

#### Scenario: All Success
- **WHEN** all DAGs finished successfully
- **THEN** send email with subject "KPC Migration Done" to configured recipients
```

**Step 3: ตรวจสอบ (Validate)**

```bash
openspec validate update-email-subject --strict
```

---

## 🏁 Use Case 4: จบงานและรวมโค้ด (Finish & Archive)

*ทำเมื่อ Code ถูก Merge และ Deploy เรียบร้อยแล้ว*

เมื่อฟีเจอร์เสร็จสิ้น เราต้องอัปเดต "ความจริง" (Source of Truth) ในโฟลเดอร์ `specs/`

```bash
openspec archive add-email-notification
```

**สิ่งที่เกิดขึ้น:**

1. OpenSpec จะย้าย Change ไปเก็บที่ `openspec/archive/` (เป็น History)
2. OpenSpec จะเอาเนื้อหาใน `spec.md` ของเรา ไปรวมร่างกับ `openspec/specs/notification/spec.md` ให้เองอัตโนมัติ!

---

## ❌ Common Mistakes (ข้อควรระวัง)

1. **ลืม Validate:** ถ้า Spec ผิด Format จะ Archive ไม่ผ่าน
2. **แก้ Spec ใน `specs/` โดยตรง:** ห้ามทำ! ต้องแก้ผ่าน `changes/` เสมอ เพื่อให้มี Audit Log
3. **ตั้งชื่อ Change ซ้ำ:** ชื่อโฟลเดอร์ใน `changes/` ห้ามซ้ำกับที่มีอยู่ (หรือที่ Archive ไปแล้ว)
4. **ลืม Root Directory:** รันคำสั่งผิดที่ OpenSpec จะหาไฟล์ไม่เจอ
