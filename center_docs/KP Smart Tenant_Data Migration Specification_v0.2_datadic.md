# KP Smart Tenant Data Migration Specification

> Data Migration Specification
>
> Source: KP Smart Tenant_Data Migration Specification_v0.2.xlsx
>
> Generated: 2026-01-21 16:27:26

---

## Summary Mapping

| Unnamed: 0 | Unnamed: 1 | 573 | 96 | 13 | 159 | 841 | Unnamed: 7 | Unnamed: 8 | Unnamed: 9 | Unnamed: 10 | Unnamed: 11 | Unnamed: 12 | 586 | 414 | 0.4922711058 | 0.722513089 | 0.7064846416 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  |  | Ready | Not Ready | TBC | New | Total | Initial | Complete | Remark |  |  |  |  |  |  | N/C*100 |  |
| No | Table | BE8 fields ready | BE8 fields not ready | BE8 fields TBC | BE8 fields New | Total Fields | BE8 fields ready | % BE8 fields ready | Remark | KP Confirm | % KP Complete | sheet_name | # (Ready + TBC) | KP mapping | %KP mapping  เมื่อเทียบกับ Total | %KP mapping  เมื่อเทียบกับ Ready | %KP mapping complete เมื่อเทียบกับ Ready+ TBC |
| 1 | Account (Tenant Profile) | 31 | 0 | 12 | 3 | 46 | 34 | 0.7391304348 |  | 35 | 1.029411765 | 01_Account | 43 | 37 | 0.8043478261 | 1.193548387 | 0.8604651163 |
| 2 | Concession | 28 | 0 | 1 | 35 | 64 | 63 | 0.984375 |  | 3 | 0.04761904762 | 02_Concession | 29 | 24 | 0.375 | 0.8571428571 | 0.8275862069 |
| 3 | Category | 5 | 0 | 0 | 0 | 5 | 5 | 1 |  | 0 | 0 | 03_Shop Category | 5 | 4 | 0.8 | 0.8 | 0.8 |
| 4 | Shop Brand | 22 | 0 | 0 | 0 | 22 | 22 | 1 |  | 0 | 0 | 04_Shop Brand | 22 | 17 | 0.7727272727 | 0.7727272727 | 0.7727272727 |
| 5 | Shop Branch | 14 | 2 | 0 | 9 | 25 | 23 | 0.92 |  | 0 | 0 | 05_Shop Branch | 14 | 18 | 0.72 | 1.285714286 | 1.285714286 |
| 6 | Contract | 34 | 0 | 0 | 67 | 101 | 101 | 1 |  | 101 | 1 | 06_Contract | 34 | 32 | 0.3168316832 | 0.9411764706 | 0.9411764706 |
| 7 | Sub-Contract | 9 | 0 | 0 | 39 | 48 | 48 | 1 |  | 0 | 0 | 07_Sub Contract | 9 | 44 | 0.9166666667 | 4.888888889 | 4.888888889 |
| 8 | Contact Point | 15 | 0 | 0 | 0 | 15 | 15 | 1 |  | 0 | 0 | 08_Contact | 15 | 13 | 0.8666666667 | 0.8666666667 | 0.8666666667 |
| 9 | Case (ทะเบียนคุมประวัติ) | 16 | 0 | 0 | 0 | 16 | 16 | 1 | ไม่ต้อง map เนื่องจากไม่มี table ที่เกี่ยวข้อง | 0 | 0 | 09_Case | 16 | 0 | 0 | 0 | 0 |
| 10 | Reference Product | 24 | 0 | 0 | 0 | 24 | 24 | 1 |  | 0 | 0 | 10_Reference Products | 24 | 12 | 0.5 | 0.5 | 0.5 |
| 11 | Product Category | 0 | 0 | 0 | 0 | 0 | 0 | 1 | ไม่พบฟิวด์ตั้งต้น BE8 เพิ่ม 20-Jan-26 | 0 | 1 | 11_Product Cat_ Starbucks | 0 | 0 | 0 | 0 | 0 |
| 12 | Product & Price  - Category Product  - Unit Product | 41 | 0 | 0 | 5 | 46 | 46 | 1 |  | 0 | 0 | 12_Product & Price | 41 | 36 | 0.7826086957 | 0.8780487805 | 0.8780487805 |
| 13 | Shop Inspection | 36 | 0 | 0 | 0 | 36 | 36 | 1 |  | 0 | 0 | 13_Shop Inspection | 36 | 19 | 0.5277777778 | 0.5277777778 | 0.5277777778 |
| 14 | Form Template  (การตรวจร้าน) | 10 | 0 | 0 | 0 | 10 | 10 | 1 |  | 0 | 0 | 14_Form Template(New) | 10 | 7 | 0.7 | 0.7 | 0.7 |
| 15 | Location | 5 | 0 | 0 | 0 | 5 | 5 | 1 |  | 0 | 0 | 15_Location | 5 | 11 | 2.2 | 2.2 | 2.2 |
| 16 | Floor | 0 | 10 | 0 | 0 | 10 | 0 | 0 | Schema ไม่ชัดเจน | 0 | 1 | 16_Floor | 0 | 2 | 0.2 | 0 | 0 |
| 17 | Unit (Space) | 53 | 0 | 0 | 1 | 54 | 54 | 1 |  | 51 | 0.9444444444 | 17_Shop Units | 53 | 20 | 0.3703703704 | 0.3773584906 | 0.3773584906 |
| 18 | Technical Provisions and others | 0 | 0 | 0 | 0 | 0 | 0 | 1 | ไม่มีในระบบTMS (Excel) | 0 | 1 |  | 0 | 8 | 0 | 0 | 0 |
| 19 | POS | 20 | 2 | 0 | 0 | 22 | 20 | 0.9090909091 |  | 0 | 0 | 19_POS | 20 | 6 | 0.2727272727 | 0.3 | 0.3 |
| 20 | Sales Transaction | 10 | 62 | 0 | 0 | 72 | 10 | 0.1388888889 |  | 0 | 0 | 20_Sales Transaction_User | 10 | 46 | 0.6388888889 | 4.6 | 4.6 |
| 21 | Supplier (Contact Point) | 0 | 10 | 0 | 0 | 10 | 0 | 0 | ไม่พบฟิวด์ตั้งต้น | 0 | 1 | 21_Supplier | 0 | 14 | 1.4 | 0 | 0 |
| 22 | Invoice | 0 | 10 | 0 | 0 | 10 | 0 | 0 | ไม่พบฟิวด์ตั้งต้น | 0 | 1 | 22_Invoice | 0 | 0 | 0 | 0 | 0 |
| 23 | Promotion - Target Sales | 17 | 0 | 0 | 0 | 17 | 17 | 1 |  | 0 | 0 | 23_Promotion | 17 | 17 | 1 | 1 | 1 |
| 24 | Airline | 25 | 0 | 0 | 0 | 25 | 25 | 1 |  | 0 | 0 | 24_Airline | 25 | 12 | 0.48 | 0.48 | 0.48 |
| 25 | Flight Delay Contract | 44 | 0 | 0 | 0 | 44 | 44 | 1 |  | 0 | 0 | 25_Flight Delay contract | 44 | 3 | 0.06818181818 | 0.06818181818 | 0.06818181818 |
| 26 | Actual Passenger | 39 | 0 | 0 | 0 | 39 | 39 | 1 |  | 0 | 0 | 26_Act. Passenger | 39 | 0 | 0 | 0 | 0 |
| 27 | Target Passenger | 18 | 0 | 0 | 0 | 18 | 18 | 1 |  | 0 | 0 | 27_Tar. Passenger | 18 | 1 | 0.05555555556 | 0.05555555556 | 0.05555555556 |
| 28 | Actual Nationality | 14 | 0 | 0 | 0 | 14 | 14 | 1 |  | 0 | 0 | 28_Act. Nationality | 14 | 4 | 0.2857142857 | 0.2857142857 | 0.2857142857 |
| 29 | By Concourse | 31 | 0 | 0 | 0 | 31 | 31 | 1 |  | 0 | 0 | 29_By concourse | 31 | 3 | 0.09677419355 | 0.09677419355 | 0.09677419355 |
| 30 | Holiday | 4 | 0 | 0 | 0 | 4 | 4 | 1 | ไม่มีในระบบ TMS | 0 | 0 | 30_Holiday | 4 | 0 | 0 | 0 | 0 |
| 31 | Master Table Nation | 5 | 0 | 0 | 0 | 5 | 5 | 1 |  | 0 | 0 | 31_Master Table Nation | 5 | 3 | 0.6 | 0.6 | 0.6 |
| 32 | Master Table By Con. | 3 | 0 | 0 | 0 | 3 | 3 | 1 |  | 0 | 0 | 32_Master Table By Con. | 3 | 1 | 0.3333333333 | 0.3333333333 | 0.3333333333 |
| 20 | Sales Transaction (Details) |  |  |  |  |  |  |  | BE8 เพิ่งเพิ่มเข้ามา 20/01/2026 |  |  | 20_Sales Transaction (Details) | 0 | 0 | 0 | 0 | 0 |
| 20 | Sales Transaction (Summary) |  |  |  |  |  |  |  | BE8 เพิ่งเพิ่มเข้ามา 20/01/2026 |  |  | 20_Sales Transaction (Summary) | 0 | 0 | 0 | 0 | 0 |

---

## Screen

*No data available*

## SUM

| # | Data Name | BU Owner | Type | Is Ready for Mapping
(Yes/No) | Plan Target Date
(Ready for Mapping) 
ใส่เพื่อให้พี่เก่ง Priority Table ได้ | Target Date 
(Mapping Complete) | Status | Next Action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1.0 | Account (Tenant Profile) | CAD | Master | Yes | 23-Jan'26 | 30-Jan'26 | KP Complete | BE8 recheck field |
| 2.0 | Concession | CAD | Master | Yes | 23-Jan'26 | 30-Jan'26 | Pending KP |  |
| 3.0 | Shop Category | CAD | Master |  | 23-Jan'26 | 30-Jan'26 | Pending KP |  |
| 4.0 | Shop Brand | CAD | Master |  | 23-Jan'26 | 30-Jan'26 | KP Complete | BE8 recheck field |
| 5.0 | Shop Branch | CAD | Operational | Yes | 30-Jan'26 | 6-Feb'26 | KP Complete | BE8 recheck field |
| 6.0 | Contract | CAD | Operational |  | 30-Jan'26 | 6-Feb'26 | KP Complete | BE8 recheck field |
| 7.0 | Sub-Contract | CAD | Operational |  | 30-Jan'26 | 6-Feb'26 | Pending KP |  |
| 8.0 | Contact | CAD | Master | Yes | 23-Jan'26 | 30-Jan'26 | KP Complete | BE8 recheck field |
| 9.0 | Case (ทะเบียนคุมประวัติ) | CAD | Operational | Yes | 30-Jan'26 | 6-Feb'26 | Pending KP |  |
| 10.0 | Reference Product | CAC | Master |  | 23-Jan'26 | 30-Jan'26 | Pending KP |  |
| 11.0 | Product Category | CAC | Master |  | 23-Jan'26 | 30-Jan'26 | Pending KP |  |
| 12.0 | Product & Price  - Category Product  - Unit Product | CAC, MKA | Master  (For POC) | Yes | 21-Jan'26 | 30-Jan'26 | KP Complete | BE8 recheck field |
| 13.0 | Shop Inspection | CAC | Operational | Yes | 30-Jan'26 | 6-Feb'26 | KP Complete | BE8 recheck field |
| 14.0 | Form Template  (การตรวจร้าน) | CAC | Master | Yes | 23-Jan'26 | 30-Jan'26 | KP Complete | BE8 recheck field |
| 15.0 | Location | FAM | Master |  | 23-Jan'26 | 30-Jan'26 | Pending KP |  |
| 16.0 | Floor | FAM | Master |  | 23-Jan'26 | 30-Jan'26 | Pending KP |  |
| 17.0 | Unit (Space) | FAM | Master |  | 23-Jan'26 | 30-Jan'26 | KP Complete | BE8 recheck field |
| 18.0 | Technical Provisions and others | FAM | Master | No | 30-Jan'26 | 6-Feb'26 | Pending BE8 | Manual Excel - BE8 สร้าง field ตั้งต้น |
| 19.0 | POS | REV | Master |  | 23-Jan'26 | 30-Jan'26 | KP Complete |  |
| 20.0 | Sales Transaction | REV | Operational | No | 30-Jan'26 | 6-Feb'26 | Pending BE8 | BE8 สร้าง field ตั้งต้น |
| 21.0 | Supplier (Contact Point) | REV |  |  |  |  | Cancelled | ย้ายไปรวมอยู่ใน Contact |
| 22.0 | Invoice | REV | Operational | No | 30-Jan'26 | 6-Feb'26 | Pending BE8 | BE8 สร้าง field ตั้งต้น |
| 23.0 | Promotion - Target Sales | MKA | Master |  | 23-Jan'26 | 30-Jan'26 | KP Complete | BE8 recheck field |
| 24.0 | Airline | MKA | Master |  | 23-Jan'26 | 30-Jan'26 | KP Complete | BE8 recheck field |
| 25.0 | Flight Delay Contract | MKA | Master |  | 23-Jan'26 | 30-Jan'26 | Pending BE8 |  |
| 26.0 | Actual Passenger | DAS |  |  | 30-Jan'26 | 6-Feb'26 | Pending BE8 |  |
| 27.0 | Target Passenger | DAS |  |  | 30-Jan'26 | 6-Feb'26 | Pending BE8 |  |
| 28.0 | Actual Nationality | DAS |  |  | 30-Jan'26 | 6-Feb'26 | Pending BE8 |  |
| 29.0 | By Concourse | DAS |  |  | 30-Jan'26 | 6-Feb'26 | Pending BE8 |  |
| 30.0 | Holiday | DAS | Master |  |  |  | Cancelled |  |
| 31.0 | Master Table Nation | DAS |  |  | 30-Jan'26 | 6-Feb'26 | Pending BE8 |  |
| 32.0 | Master Table By Con. | DAS |  |  | 30-Jan'26 | 6-Feb'26 | Pending BE8 |  |
|  |  |  |  |  |  |  | 12 |  |
|  |  |  |  |  |  |  | 0.375 |  |

---

## Overview

| # | Data Name | BU Owner | Source | Table API | Description | Migration Criteria | Total Amount | Estimated Amount | Growth Rate | Transaction Amount | User/KP Feedback |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ตัวอย่าง | Data Name 1 | CAD |  |  |  | All (Active) |  | 1,000 Records | 17-19% | 10 record per month |  |
| ตัวอย่าง | Data Name 2 | CAD |  |  |  | ย้อนหลัง 2 ปี  (1/2025) |  | 1,000 Records | 8-10% | 5 records per day | เพิ่ม Data Name 2 ใช้สำหรับแสดงข้อมูลที่เกี่ยวข้องกับ Data Name 1 |
| 1 | Account (Tenant Profile) | CAD | Oracle | KPS_R_SHOP |  | All |  | 104 records per year | 0.2857 | 72 records per year |  |
|  |  | CAD | External | KPS_R_SHOP_COMMITTEE | Committee by shop |  |  | 1040 (104*10) records per year |  | 0 records per year |  |
|  |  | CAD |  | KPS_R_SHOP_CONT_PER | Contact Person |  |  |  |  | 0 records per year |  |
| 2 | Concession | CAD | Oracle | KPS_R_CONCESS |  | All (00-11) |  |  |  | 0 records per year |  |
| 3 | Category | CAD | Oracle | KPS_R_AOT_SHOP_CATE |  | All (Active) |  |  |  | 0 records per year |  |
|  |  | CAD |  | KPS_R_AOT_RENTAL_CAT |  |  |  |  |  | 0 records per year |  |
|  |  | CAD |  | KPS_R_AOT_RENTAL_TYPE |  |  |  |  |  | 0 records per year |  |
| 4 | Shop Brand | CAD | Oracle | KPS_R_SHOP_BRAND |  | All (Active) |  | 81 records per year | 0.3721 | 51 records per year |  |
|  |  | CAD |  | KPS_T_PROD_COMPARE |  |  |  | 153061 records per year | -0.1354 | 190901 records per year |  |
| 5 | Shop Branch | CAD | Oracle | KPS_R_BRANCH |  | All (Active) |  | 188 records per year | 0.156 | 152 records per year |  |
|  |  | CAD |  | KPS_T_CONT_SHOP_UNIT |  |  |  | 338 records per year | -0.1793 | 457 records per year |  |
|  |  | CAD |  | KPS_R_SHOPUNIT |  |  |  | 78 records per year | -0.5372 | 266 records per year |  |
|  |  | CAD |  | KPS_R_POS |  |  |  | 1202 records per year | 1.0791 | 428 records per year |  |
|  |  | CAD |  | KPS_R_SHOP_CONT_PER |  |  |  |  |  | 0 records per year |  |
| 6 | Contract | CAD | Oracle | KPS_T_AOT_CONTRACT |  | All Active -  Attachment Inactive - No Attachment |  | 3 records per year | 0 | 0 records per year |  |
|  |  | CAD |  | KPS_T_CONTRACT |  |  |  | 80 records per year | -0.2353 | 120 records per year |  |
|  |  | CAD |  | KPS_T_CONTRACT_REVISE (เก็บ History Contract Change)  |  |  |  | 80 records per year | -0.2353 | 120 records per year |  |
|  |  | CAD |  | KPS_R_PERIOD_CONT |  |  |  | 0 records per year | -1 | 30 records per year |  |
|  |  | CAD |  | KPS_T_CONT_SHOP_UNIT |  |  |  | 338 records per year | -0.1793 | 457 records per year |  |
|  |  | CAD |  | KPS_R_SHOPUNIT |  |  |  | 78 records per year | -0.5372 | 266 records per year |  |
| 7 | Sub-Contract | CAD | Oracle | KPS_T_CONT_SUB_CONT (อยู่ภายใต้สัญญาแม่ Contract) |  | All (Active) |  | 0 records per year | -0.5 | 2 records per year |  |
| 8 | Contact Point | CAD | Oracle | KPS_R_SHOP_CONT_PER |  | All (Active) |  |  |  | 0 records per year |  |
|  | Contact Point  - ร้องเรียน  - ตรวจร้าน  - ราคา | CAC | Oracle | KPS_CAC_INSPECTION_INFORM_SEND |  | All |  | 3854 records per year | 0.0922 | 3380 records per year |  |
|  | Contact Point | FAM | ไม่มีข้อมูลในระบบ TMS | KPS_R_SHOP_CONT_PER |  | All (Active) |  | 0 records | 0 | 0 record per month |  |
|  | Contact Point - ผู้ติดตาม Text File - ผู้ติดตามยอดขายวัน - ฝ่ายบัญชีของผู้ประกอบการ | REV |  | KPS_R_EMAIL_SUPPLIER |  | All (Active) |  | 18 records per year | 2 | 4 records per year |  |
|  |  | REV |  | KPS_R_EMAIL_TENANT |  | All (Active) |  | 399 records per year | -0.0579 | 436 records per year |  |
|  | Contact Point | MKA |  |  |  | All (Active) |  |  |  |  |  |
| 9 | Case (ทะเบียนคุมประวัติ) | CAD | Manual Excel |  |  | All (Active) |  |  |  |  |  |
|  | Case (ทะเบียนคุมประวัติ) | MKA | Manual Excel |  |  | ย้อนหลัง 2 ปี (1/2025) |  |  |  |  |  |
| 10 | Reference Product | CAC | Manual Excel | KPS_T_REQPROD_MD_ORG |  | All (Active) |  | 82430 records per year | -0.1561 | 106707 records per year |  |
| 11 | Product Category |  |  |  |  |  |  |  |  |  |  |
| 12 | Product & Price  - Category Product  - Unit Product | CAC |  | KPS_T_REQPROD_MD |  | All |  | 163819 records per year | -0.1208 | 199139 records per year |  |
|  |  | CAC |  | KPS_T_APPRV_M |  |  |  | 164093 records per year | -0.1144 | 197251 records per year |  |
| 13 | Shop Inspection | CAC |  | KPS_CAC_INSPECTION_FORM |  | ย้อนหลัง 2 ปี  (1/2025: เฉพาะเชิงพาณิชย์) |  | 1721 records per year | 0.3939 | 1060 records per year |  |
|  |  | CAC |  | KPS_CAC_INSPECTION_TOPIC_M |  |  |  | 5 records per year | 0.3333 | 4 records per year |  |
|  |  | CAC |  | KPS_CAC_INSPECTION_TOPIC_MD |  |  |  | 228 records per year | 5.1667 | 22 records per year |  |
|  |  | CAC |  | KPS_CAC_INSP_DOC_DETAIL |  |  |  | 28272 records per year | -0.1059 | 33496 records per year |  |
|  |  | CAC |  | KPS_CAC_INSPECTION_DOCUMENT |  |  |  | 3066 records per year | 0.088 | 2704 records per year |  |
|  |  | CAC |  | KPS_CAC_INSP_FORM_UNIT_M |  |  |  | 95 records per year | -0.2558 | 150 records per year |  |
|  |  | CAC |  | KPS_CAC_INSP_FORM_UNIT_MD |  |  |  | 149 records per year | -0.1802 | 202 records per year |  |
|  |  | CAC |  | KPS_CAC_INSPECTOR |  |  |  | 0 records per year | -1 | 0 records per year |  |
|  |  | CAC |  | KPS_CAC_INSPECTION_PERIOD |  |  |  |  |  | 0 records per year |  |
|  |  | CAC |  | KPS_R_SHOP |  |  |  | 104 records per year | 0.2857 | 72 records per year |  |
| 14 | Form Template  (การตรวจร้าน) | CAC |  | KPS_CAC_INSPECTION_TEMPLATE |  | All  *Recheck email from 11-Dec |  | 3158 records per year | 7.3778 | 211 records per year |  |
| 15 | Location | FAM | Oracle | KPS_R_LOCATION |  | All (Active) |  |  |  | 0 records per year |  |
|  |  | FAM | Oracle | KPS_R_BUILDING |  |  |  |  |  | 0 records per year |  |
|  |  | FAM | Oracle | KPS_R_ZONE |  |  |  |  |  | 0 records per year |  |
|  |  | FAM | Oracle | KPS_R_WING |  |  |  |  |  | 0 records per year |  |
|  |  | FAM | Oracle | KPS_R_LEVEL |  |  |  |  |  | 0 records per year |  |
|  |  | FAM | Oracle | KPS_R_AREA >> ไม่ได้อยู่ใต้อะไรเลย |  |  |  |  |  | 0 records per year |  |
| 16 | Floor | FAM | Oracle | KPS_R_LEVEL |  | All (Active) |  |  |  | 0 records per year |  |
| 17 | Unit (Space) | FAM | Oracle | KPS_R_SHOPUNIT |  | All  (ย้อนหลัง 2 ปี) |  | 78 records per year | -0.5372 | 266 records per year |  |
| 18 | Technical Provisions and others | FAM | Manual Excel |  |  | All (Active) |  |  |  |  |  |
|  | - Meter Mapping Master | FAM | Manual Excel | KPS_R_ELECTRIC |  | All (Active) |  | -  | -  | - |  |
|  |  | FAM | Manual Excel | KPS_R_WATER_METER |  | All (Active) |  | 0 records | 0 | 0 record per month |  |
|  | - Source Electrical Meter Reading Record | FAM | Manual Excel | KPS_R_POWER_METER |  | All (Active) |  | 0 records | 0 | 0 record per month |  |
|  |  | FAM | Manual Excel | KPS_T_POWER_USAGE |  | All (Active) |  | 0 records | 0 | 0 record per month |  |
|  |  | FAM | Manual Excel | KPS_T_POWER_USAGE_SHOPUNIT |  | All (Active) |  | 0 records | 0 | 0 record per month |  |
|  | - Electrical Meter Reading Record | FAM | Manual Excel | KPS_R_POWER_METER |  | All (Active) |  | 0 records | 0 | 0 record per month |  |
|  |  | FAM | Manual Excel | KPS_T_POWER_USAGE |  | All (Active) |  | 0 records | 0 | 0 record per month |  |
|  |  | FAM | Manual Excel | KPS_T_POWER_USAGE_SHOPUNIT |  | All (Active) |  | 0 records | 0 | 0 record per month |  |
|  | - Source Water Meter Reading Record | FAM | Manual Excel | KPS_R_WATER_METER |  | All (Active) |  | 0 records | 0 | 0 record per month |  |
|  |  | FAM | Manual Excel | KPS_T_WATER_USAGE |  | All (Active) |  | 0 records | 0 | 0 record per month |  |
|  |  | FAM | Manual Excel | KPS_T_WATER_USAGE_SHOPUNIT |  | All (Active) |  | 0 records | 0 | 0 record per month |  |
|  | - Water Meter Reading Record | FAM | Manual Excel | KPS_R_WATER_METER |  | All (Active) |  | 0 records | 0 | 0 record per month |  |
|  |  | FAM | Manual Excel | KPS_T_WATER_USAGE |  | All (Active) |  | 0 records | 0 | 0 record per month |  |
|  |  | FAM | Manual Excel | KPS_T_WATER_USAGE_SHOPUNIT |  | All (Active) |  | 0 records | 0 | 0 record per month |  |
| 19 | POS | REV |  | KPS_R_POS |  | All (Active) |  | 1202 records per year | 1.0791 | 428 records per year |  |
|  |  | REV |  | KPS_T_CONT_SHOP_UNIT |  | All (Active) |  | 338 records per year | -0.1793 | 457 records per year |  |
|  |  | REV |  | KPS_R_SHOP |  | All (Active) |  | 104 records per year | 0.2857 | 72 records per year |  |
|  |  | REV |  | KPS_R_SHOPUNIT |  | All (Active) |  | 78 records per year | -0.5372 | 266 records per year |  |
|  |  | REV |  | KPS_T_POS_REGISTER_HISTORY |  | All (Active) |  | 2158 records per year | 1.438 | 624 records per year |  |
|  |  | REV |  | KPS_R_POS_SUPPLIER |  | All (Active) |  | 2 records per year | -0.25 | 4 records per year |  |
| 20 | Sales Transaction | REV |  | KPS_T_SALES_M | Sales Transaction Details  - Sales Master/Header | ย้อนหลัง 5 ปี <TBD with ACC> *เอา Remark Table มาด้วย |  | 51127576 records per year | 0.2655 | 36164974 records per year |  |
|  |  | REV |  | KPS_T_SALES_MD | Sales Transaction Details  - Sales Details/Line Items | ย้อนหลัง 5 ปี <TBD with ACC> *เอา Remark Table มาด้วย |  | 121722301 records per year | 0.2568 | 86957568 records per year |  |
|  |  | REV |  | KPS_T_SALESPAY_MD | Sales Transaction Details - Sales Payment | ย้อนหลัง 5 ปี <TBD with ACC> *เอา Remark Table มาด้วย |  | 51702195 records per year | 0.2681 | 36461318 records per year |  |
|  |  | REV |  | KPS_T_SALESBANK_MD | Sales Transaction Details  - Bank Detail | ย้อนหลัง 5 ปี <TBD with ACC> *เอา Remark Table มาด้วย |  | 163641 records per year | -0.0019 | 164120 records per year |  |
|  |  | REV |  | KPS_WEB_SALES | Sales Transaction Summary | ย้อนหลัง 5 ปี <TBD with ACC> *เอา Remark Table มาด้วย |  | 16656 records per year | 0.1305 | 13882 records per year |  |
|  |  | REV |  | KPS_T_SALES_APPRV | Sales Transaction Summary | ย้อนหลัง 5 ปี <TBD with ACC> *เอา Remark Table มาด้วย |  | 56491 records per year | 0.1739 | 44560 records per year |  |
|  |  | REV |  | KPS_T_SALES_APPRV_DETAIL | Sales Transaction Summary | ย้อนหลัง 5 ปี <TBD with ACC> *เอา Remark Table มาด้วย |  | 229433 records per year | 0.184 | 178716 records per year |  |
| 21 | Supplier (Contact Point) | REV |  | KPS_R_POS_SUPPLIER |  | All (Active) |  | 2 records per year | -0.25 | 4 records per year |  |
|  |  | REV |  | KPS_R_EMAIL_SUPPLIER |  | All (Active) |  | 18 records per year | 2 | 4 records per year |  |
| 22 | Invoice | REV |  | KPS_T_PREINV |  | ย้อนหลัง 2 ปี (1/2025) *Refer Sales Transaction <TBD with ACC> |  | 9391 records per year | 0.3403 | 6118 records per year |  |
|  |  | REV |  | KPS_T_PREINV_DETAIL |  | ย้อนหลัง 2 ปี (1/2025) *Refer Sales Transaction <TBD with ACC> |  | 9391 records per year | 0.3403 | 6118 records per year |  |
|  |  | REV |  | KPS_T_PREINV_MIN |  | ย้อนหลัง 2 ปี (1/2025) *Refer Sales Transaction <TBD with ACC> |  | 5018 records per year | 0.3919 | 3098 records per year |  |
|  |  | REV |  | KPS_T_PREINV_REVGUA |  | ย้อนหลัง 2 ปี (1/2025) *Refer Sales Transaction <TBD with ACC> |  | 4387 records per year | 0.2896 | 3020 records per year |  |
|  |  | REV |  | KPS_T_PREINV_REVSALES_D |  | ย้อนหลัง 2 ปี (1/2025) *Refer Sales Transaction <TBD with ACC> |  | 189097 records per year | 0.1393 | 155830 records per year |  |
|  |  | REV |  | KPS_T_PREINV_REVSALES_M |  | ย้อนหลัง 2 ปี (1/2025) *Refer Sales Transaction <TBD with ACC> |  | 4400 records per year | 0.2709 | 3093 records per year |  |
| 23 | Promotion - Target Sales | MKA |  | KPS_R_PROMOTION |  | All (Active) |  | 225 records per year | 0.1093 | 193 records per year |  |
|  |  |  |  | KPS_R_PROMOTION_TYPE |  |  |  |  |  | 0 records per year |  |
|  |  |  |  | KPS_R_PROMOTION_OWNER |  |  |  |  |  | 0 records per year |  |
|  |  |  |  | KPS_R_PROMOTION_CATG |  |  |  |  |  | 0 records per year |  |
|  |  |  |  | KPS_R_PRO_LAUNCH |  |  |  | 202 records per year | 0.0615 | 184 records per year |  |
|  |  |  |  | KPS_R_PRO_SHOP |  |  |  | 353 records per year | 0.0028 | 352 records per year |  |
|  |  |  |  | KPS_R_PRO_SHOPBRANCH |  |  |  | 4502 records per year | 0.5277 | 2438 records per year |  |
|  | Product & Price (Product Promotion) | MKA |  | KPS_T_APPRV_M |  | All  (Approved, Pending) |  | 164093 records per year | -0.1144 | 197251 records per year |  |
| 24 | Airline | MKA |  | KPS_R_AIRLINE |  | All  (Active, Inactive, Expired, Suspended) |  |  |  | 0 records per year |  |
| 25 | Flight Delay Contract | MKA |  | KPS_R_FLIGHT |  | All (Active) |  |  |  |  |  |
| 26 | Actual Passenger |  |  |  |  |  |  |  |  |  |  |
| 27 | Target Passenger |  |  |  |  |  |  |  |  |  |  |
| 28 | Actual Nationality |  |  |  |  |  |  |  |  |  |  |
| 29 | By Concourse |  |  |  |  |  |  |  |  |  |  |
| 30 | Holiday |  |  |  |  |  |  |  |  |  |  |
| 31 | Master Table Nation |  |  |  |  |  |  |  |  |  |  |
| 32 | Master Table By Con. |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  | KPS_T_REQPROD_MD |  |  |  | 163819 records per year | -0.1208 | 199139 records per year |  |
|  |  |  |  | KPS_T_PROD_COMPARE |  |  |  | 153061 records per year | -0.1354 | 190901 records per year |  |
|  |  |  |  | KPS_T_PROD_CATE_MPP |  |  |  | 62691 records per year | -0.0532 | 68079 records per year |  |

---

## Spec

| No. | SFDC Field Name (EN) | SFDC Field Name (TH) | Type | Required | Sample Data | Description | Status | Remark | Help Text | Track History | External ID | Track History.1 | Encrypted | Page Layout | Length | Source Field API Name |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Header |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 1 | Consession No. | Concession No. | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 2 | Unit No. | เลขที่ยูนิต | Text(XX) |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 3 | Start Date | วันที่เริ่ม | Date |  |  |  |  |  |  |  |  |  |  |  |  |  |

---

## 01_Account

| No. | SFDC Field Name (EN) | SFDC Field Name (TH) | Source Field API Name | Source Field Type | Source Field Length | VULLABLE (N=Required) | KP Table | KP Field Name | KP Field Type | KP Field Length | VULLABLE (N=Required).1 | Progress | Confirm | Type | Required | Sample Data | Description | Status | User/KP Feedback | Remark | Help Text | Track History | External ID | Track History.1 | Encrypted | Page Layout | Length |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Tenant Profile |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 1 | Concession |  | CON_CODE |  | 2 | N | KPS_R_SHOP | CON_CODE | CHAR | 2 | N | Ready | Y | Text (100) | Yes | 09 | เลขที่รหัสสัมปทาน | Confirmed |  | - เลือกข้อมูลตามตัวเลือกที่กำหนด โดยเป็นข้อมูลจาก “การบันทึกข้อมูลสัมปทาน” (Concession) |  |  |  |  |  |  |  |
| 2 | Tenant Code |  | SHOP_CODE | VARCHAR2 | 20 | N | KPS_R_SHOP | SHOP_CODE | VARCHAR2 | 20 | N | Ready | Y | Text (100) | Yes | 0902029 | รหัสบริษัทผู้ประกอบการ | Confirmed |  | - ระบบสร้างให้อัตโนมัติเมื่อได้รับการอนุมัติจัดทำสัญญาครั้งแรก จากระบบ Workflow Logic: (Concession Code)(2 หลัก) + (Business Type)(2 หลัก) + (Tenant Running No.)(3 หลัก) |  |  |  |  |  |  |  |
| 3 | Tenant Name |  | REGISTERED_NAME | VARCHAR2 | 200 |  | KPS_R_SHOP | REGISTERED_NAME | VARCHAR2 | 200 | Y | Ready | Y | Text (100) | Yes |  |  | Confirmed |  | - ความยาวสูงสุด 100 ตัวอักษร |  |  |  |  |  |  |  |
| 4 | Tenant Name - TH |  | SHOP_NAME_T | VARCHAR2 | 200 |  | KPS_R_SHOP | SHOP_NAME_T | VARCHAR2 | 200 | Y | Ready | Y | Text (100) | Yes | บริษัท อิมเพรสซีฟ สุวรรณภูมิ จำกัด | ชื่อผู้ประกอบการภาษาไทย | Confirmed |  | " |  |  |  |  |  |  |  |
| 5 | Tenant Name - EN |  | SHOP_NAME_E | VARCHAR2 | 200 |  | KPS_R_SHOP | SHOP_NAME_E | VARCHAR2 | 200 | Y | Ready | Y | Text (100) | Yes | Impressive Suvarnabhumi Co., Ltd. | ชื่อผู้ประกอบการภาษาอังกฤษ | Confirmed |  | " |  |  |  |  |  |  |  |
| 6 | Short Name |  | SHORT_NAME | VARCHAR2 | 50 |  | KPS_R_SHOP | SHORT_NAME | VARCHAR2 | 50 | Y | Ready | Y | Text (100) | Yes | Impressive Suvarnabhumi | ชื่อย่อผู้ประกอบการ | Confirmed |  | " |  |  |  |  |  |  |  |
| 7 | Business Type |  | <TBC> |  |  |  |  |  |  |  |  | TBC |  | Picklist (Multi-Select) | Yes | 01 - F&B 02 - Service 03 - Retails 04 - Bank | ประเภทธุรกิจ | Confirmed |  | - เลือกข้อมูลตามตัวเลือกที่กำหนด - เลือกได้ 1 ตัวเลือก  |  |  |  |  |  |  |  |
| 8 | Registration Date |  | REG_DATE | DATE | 7 |  | KPS_R_SHOP | REG_DATE | DATE | 7 | Y | Ready | Y | Date | Yes |  | วันที่จดทะเบียนผู้ประกอบการ | Confirmed |  |  |  |  |  |  |  |  |  |
| 9 | Registration No. |  | <TBC> |  |  |  | KPS_R_SHOP | REG_COMM_NO | VARCHAR2 | 30 | Y | TBC | Y | Text (100) | Yes |  | เลขจดทะเบียนผู้ประกอบการ | Confirmed |  |  |  |  |  |  |  |  |  |
| 10 | Registered Capital |  | <TBC> |  |  |  | KPS_R_SHOP | REG_CAP_AMT | NUMBER | 22 | Y | TBC | Y | Number(16,2) | No |  | ทุนจดทะเบียน | Confirmed |  | - กรอกได้เฉพาะตัวเลขเท่านั้น - รูปแบบ: #,###,###.## บาท |  |  |  |  |  |  |  |
| 11 | Registered Currency |  | <TBC> |  |  |  | KPS_R_SHOP | CURRENCY_CODE | VARCHAR2 | 5 | Y | TBC | Y |  | No |  | หน่วย | Confirmed |  | - เลือกข้อมูลตามตัวเลือกจาก Currency Master |  |  |  |  |  |  |  |
| 12 | Commercial |  | COMMERCIAL_FLAG | NUMBER | 22 |  | KPS_R_SHOP | COMMERCIAL_FLAG (1 = Commercial, 0 = Government) | NUMBER | 22 | Y | Ready | Y | Checkbox | Yes | - Yes - No  | เป็น commercial หรือไม่ | Confirmed |  |  |  |  |  |  |  |  |  |
| 13 | Government |  | <New> |  |  |  | KPS_R_SHOP | COMMERCIAL_FLAG (1 = Commercial, 0 = Government) | NUMBER | 22 | Y | New | Y | Checkbox | Yes | - Yes - No  | เป็น government หรือไม่ | Confirmed |  |  |  |  |  |  |  |  |  |
| 14 | Tax ID |  | <TBC> |  |  |  | KPS_R_SHOP | REG_VAT_NO | VARCHAR2 | 30 | Y | TBC |  | Number(13,0) | Yes |  | เลขประจำตัวผู้เสียภาษีอากร | Confirmed |  | - กรอกได้เฉพาะตัวเลขเท่านั้น - กรอกข้อมูลได้สูงสุด 13 หลัก  |  |  |  |  |  |  |  |
| 15 | Business Group |  | <New> |  |  |  | KPS_R_SHOP | TEXT_BU_TYPE | VARCHAR2 | 20 | Y | New | Y | Picklist | Yes | - KPS - KPT - BU | ประเภท text file business group | Confirmed |  | - เลือกข้อมูลตามตัวเลือกที่กำหนด - ตัวอย่าง KPS => “Primo Food and Beverage” KPT => “King Power Tax Free Co.,Ltd.” BU => “Boots”  |  |  |  |  |  |  |  |
| 16 | SAP Customer Code |  | BLL_SAP_CUSCODE | VARCHAR2 | 30 |  | KPS_R_SHOP | BLL_SAP_CUSCODE | VARCHAR2 | 30 | Y | Ready | Y | Text (100) | No | 2070346 | เลข Customer Code จากระบบ SAP | Confirmed |  | - เลข Customer Code ที่ได้รับกลับมาจาก SAP |  |  |  |  |  |  |  |
| 17 | Accounting Information |  | <New> |  |  |  | KPS_R_SHOP KPS_R_SHOP KPS_R_SHOP KPS_R_SHOP KPS_R_SHOP | CONTRACTOR_FLAG TENANT_FLAG OTH_CUST_FLAG KPG_FLAG HAS_SALES_FLAG | NUMBER NUMBER NUMBER NUMBER NUMBER | 22 22 22 22 22 | Y Y Y Y Y | New | Y | Picklist (Multi-Select) | No | - Contractor - Tenant - Other Customer - King Power Group - Sales/Revenue  | ข้อมูลบัญชีผู้ใช้งาน | Confirmed |  | - เลือกข้อมูลตามตัวเลือกที่กำหนด - เลือกได้มากกว่า 1 ตัวเลือก  |  |  |  |  |  |  |  |
| Authorized Committee |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 18 | Name-Surname |  | COMM_NAME | VARCHAR2 | 50 |  | KPS_R_SHOP_COMMITTEE | COMM_NAME | VARCHAR2 | 50 | Y | Ready | Y | Text (255) |  |  |  | Confirmed |  |  |  |  |  |  |  |  |  |
| 19 | Position |  | COMM_POSITION | VARCHAR2 | 30 |  | KPS_R_SHOP_COMMITTEE | COMM_POSITION | VARCHAR2 | 30 | Y | Ready | Y | Text (255) |  |  |  | Confirmed |  |  |  |  |  |  |  |  |  |
| 20 | ID Card No. |  | <TBC> |  |  |  | KPS_R_SHOP_COMMITTEE | COMM_ID_NO | VARCHAR2 | 40 | Y | TBC | Y | Text (255) |  |  |  | Confirmed |  |  |  |  |  |  |  |  |  |
| 21 | Mobile No. |  | <TBC> |  |  |  |  |  |  |  |  | TBC |  | Phone |  |  |  | Confirmed |  |  |  |  |  |  |  |  |  |
| 22 | Email Address |  | <TBC> |  |  |  |  |  |  |  |  | TBC |  | Email |  |  |  | Confirmed |  |  |  |  |  |  |  |  |  |
| Location Address |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 23 | Building / Village |  | LOC_BUILDING LOC_VILLAGE | VARCHAR2 VARCHAR2 | 60 60 |  | KPS_R_SHOP KPS_R_SHOP | LOC_BUILDING LOC_VILLAGE | VARCHAR2 VARCHAR2 | 60 60 | Y Y | Ready | Y | Text (255) | Yes |  |  | Confirmed |  |  |  |  |  |  |  |  |  |
| 24 | Address No. |  | LOC_ADDRESS_NO | VARCHAR2 | 50 |  | KPS_R_SHOP | LOC_ADDRESS_NO | VARCHAR2 | 50 | Y | Ready | Y | Text (255) | Yes |  |  | Confirmed |  |  |  |  |  |  |  |  |  |
| 25 | Soi |  | LOC_SOI | VARCHAR2 | 50 |  | KPS_R_SHOP | LOC_SOI | VARCHAR2 | 50 | Y | Ready | Y | Text (255) | Yes |  |  | Confirmed |  |  |  |  |  |  |  |  |  |
| 26 | Street |  | LOC_STREET | VARCHAR2 | 50 |  | KPS_R_SHOP | LOC_STREET | VARCHAR2 | 50 | Y | Ready | Y | Text (255) | Yes |  |  | Confirmed |  |  |  |  |  |  |  |  |  |
| 27 | Sub-District |  | LOC_SUB_DISTRICT | VARCHAR2 | 50 |  | KPS_R_SHOP | LOC_SUB_DISTRICT | VARCHAR2 | 50 | Y | Ready | Y | Text (255) | Yes |  |  | Confirmed |  |  |  |  |  |  |  |  |  |
| 28 | District |  | LOC_DISTRICT_CODE | VARCHAR2 | 3 |  | KPS_R_SHOP | LOC_DISTRICT_CODE | VARCHAR2 | 3 | Y | Ready | Y | Text (255) | Yes |  |  | Confirmed |  |  |  |  |  |  |  |  |  |
| 29 | Province |  | LOC_PROV_CODE | VARCHAR2 | 2 |  | KPS_R_SHOP | LOC_PROV_CODE | VARCHAR2 | 2 | Y | Ready | Y | Text (255) | Yes |  |  | Confirmed |  |  |  |  |  |  |  |  |  |
| 30 | Zip Code |  | LOC_ZIPCODE | CHAR | 5 |  | KPS_R_SHOP | LOC_ZIPCODE | CHAR | 5 | Y | Ready | Y | Number(5,0) | Yes |  |  | Confirmed |  |  |  |  |  |  |  |  |  |
| 31 | Contact Channel |  | <TBC> |  |  |  |  |  |  |  |  | TBC |  | Picklist | Yes | 1. Primary Contact No. 2. Secondary Contact No. 3. Fax No. |  | Confirmed |  |  |  |  |  |  |  |  |  |
| 32 | Contact No. |  | LOC_PHONE_NO | VARCHAR2 | 100 |  | KPS_R_SHOP | LOC_PHONE_NO | VARCHAR2 | 100 | Y | Ready | ? | Phone | Yes |  |  | Confirmed |  |  |  |  |  |  |  |  |  |
| 33 | Email Address |  |  |  |  |  |  |  |  |  |  | Ready |  | Email | Yes |  |  | Confirmed |  |  |  |  |  |  |  |  |  |
| 34 | Country |  | LOC_COUNTRY_CODE | VARCHAR2 | 3 |  | KPS_R_SHOP | LOC_COUNTRY_CODE | VARCHAR2 | 3 | Y | Ready | Y | Text (255) | Yes |  |  | Confirmed |  |  |  |  |  |  |  |  |  |
| 35 | Website |  | LOC_WEBSITE LOC_WEBSITE_2 | VARCHAR2 VARCHAR2 | 50 50 |  | KPS_R_SHOP KPS_R_SHOP | LOC_WEBSITE LOC_WEBSITE_2 | VARCHAR2 VARCHAR2 | 50 50 | Y Y | Ready | Y | Text (255) | Yes | 1. Primary 2. Secondary |  | Confirmed |  |  |  |  |  |  |  |  |  |
| 36 | Billing Address |  | BLL_ADDRESS1 BLL_ADDRESS2 BLL_CITY BLL_ZIP BLL_COUNTRY_CODE BLL_TEL BLL_FAX | VARCHAR2 VARCHAR2 VARCHAR2 VARCHAR2 VARCHAR2 VARCHAR2 VARCHAR2 | 120 120 60 10 3 100 30 |  | KPS_R_SHOP KPS_R_SHOP KPS_R_SHOP KPS_R_SHOP KPS_R_SHOP KPS_R_SHOP KPS_R_SHOP | BLL_ADDRESS1 BLL_ADDRESS2 BLL_CITY BLL_ZIP BLL_COUNTRY_CODE BLL_TEL BLL_FAX | VARCHAR2 VARCHAR2 VARCHAR2 VARCHAR2 VARCHAR2 VARCHAR2 VARCHAR2 | 120 120 60 10 3 100 30 | Y Y Y Y Y Y Y | Ready | Y | Picklist | Yes | 1. ที่อยู่เดียวกันกับที่อยู่ปัจจุบัน 2. ที่อยู่เดียวกันกับที่อยู่จัดส่งเอกสาร | ที่อยู่วางบิล  | Confirmed |  | - กรอกข้อมูลที่อยู่ หรือเลือกข้อมูลจากตัวเลือก |  |  |  |  |  |  |  |
| 37 | Document Address |  | <TBC> |  |  |  |  |  |  |  |  | TBC |  | Picklist | Yes | 1. ที่อยู่เดียวกันกับที่อยู่ปัจจุบัน 2. ที่อยู่เดียวกันกับที่อยู่วางบิล | ที่อยู่จัดส่งเอกสาร | Confirmed |  | - กรอกข้อมูลที่อยู่ หรือเลือกข้อมูลจากตัวเลือก |  |  |  |  |  |  |  |
| 38 | Tenant Grade/Assessment |  | <TBC> |  |  |  |  |  |  |  |  | TBC |  | Picklist |  | - A - B - C - D | ผลประเมินผู้ประกอบการ  | Confirmed |  |  |  |  |  |  |  |  |  |
| 39 | Closure Opportunity |  | <TBC> |  |  |  |  |  |  |  |  | TBC |  | Picklist |  | - สูง - กลาง - ต่ำ | โอกาสในการปิดสัญญา | Confirmed |  |  |  |  |  |  |  |  |  |
| 40 | Tenant Status |  | STATUS | NUMBER | 22 |  | KPS_R_SHOP | STATUS | NUMBER | 22 | Y | Ready | Y | Picklist | Yes | - New - Waiting list - Under discussion - Contracted - Inactive | สถานะผู้ประกอบการ | Confirmed |  |  |  |  |  |  |  |  |  |
| Contact Person |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 41 | Name-Surname |  |  |  |  |  | KPS_R_SHOP_CONT_PER | CONT_NAME | VARCHAR2 | 50 | N | Ready | Y | Text (255) | Yes |  |  | Confirmed |  |  |  |  |  |  |  |  |  |
| 42 | Position |  |  |  |  |  | KPS_R_SHOP_CONT_PER | CONT_POST | VARCHAR2 | 50 | Y | Ready | Y | Text (255) | Yes |  |  | Confirmed |  |  |  |  |  |  |  |  |  |
| 43 | Mobile no. |  |  |  |  |  | KPS_R_SHOP_CONT_PER | CONT_PHONE_NO | VARCHAR2 | 30 | Y | Ready | Y | Phone | Yes |  |  | Confirmed |  |  |  |  |  |  |  |  |  |
| 44 | Email Address |  |  |  |  |  | KPS_R_SHOP_CONT_PER | CONT_EMAIL_ADDR | VARCHAR2 | 50 | Y | Ready | Y | Email | Yes |  |  | Confirmed |  |  |  |  |  |  |  |  |  |
| 45 | Subject to Contact |  |  |  |  |  | KPS_R_SHOP_CONT_PER | SUBJECT | VARCHAR2 | 150 | Y | Ready | Y | Picklist | Yes | - สนใจพื้นที่ (Prospect) - สัญญา (Contract) - ออกแบบ (Design) - การตกแต่งร้านค้า (Onsite construction) - ระบบงานขาย POS และส่งยอดขาย (Revenue) - ราคาสินค้า (Price) - การส่งเสริมการขาย (Promotion) - Automated call | ส่วนงาน | Confirmed |  |  |  |  |  |  |  |  |  |
| 46 | Preferred contact channel |  |  |  |  |  |  |  |  |  |  | Ready |  | Picklist | Yes | - Mobile - Email  | ช่องทางที่สะดวกให้ติดต่อ | Confirmed |  |  |  |  |  |  |  |  |  |

---

## 02_Concession

|   | SFDC Field Name (EN) | SFDC Field Name (TH) | Source Field API Name | Source Field Type | Source Field Length | VULLABLE (N=Required) | KP Table | KP Field Name | KP Field Type | KP Field Length | VULLABLE (N=Required).1 | Progress | Confirm | Type | Required | Sample Data | Description | Status | User/KP Feedback | Remark | Help Text | Track History | External ID | Track History.1 | Encrypted | Page Layout | Length |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Concession Information |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 1 | Concession No. |  | CON_CODE | CHAR | 2 | N | KPS_R_CONCESS | CON_CODE | CHAR | 2.0 | N | Ready | Y | Text | Yes | 09 | เลขที่รหัสสัมปทาน | Confirmed |  |  |  |  |  |  |  |  |  |
| 2 | Concession Type |  |  |  |  |  |  |  |  |  |  | Ready |  | Text | Yes | - Airport - Non-airport | ประเภทของสัมปทาน | Confirmed |  |  |  |  |  |  |  |  |  |
| 3 | Description |  | CON_DESC | VARCHAR2 | 100 | N | KPS_R_CONCESS | CON_DESC | VARCHAR2 | 100.0 | N | Ready | Y | Text | Yes |  | รายละเอียดสัมปทาน | Confirmed |  |  |  |  |  |  |  |  |  |
| 4 | ชื่อผู้ให้สัมปทาน |  | CON_SNAME CON_LNAME | VARCHAR2 VARCHAR2 | 10 100 | N N | KPS_R_CONCESS | CON_LNAME | VARCHAR2 | 100.0 | N | Ready | Y | Text | Yes | SVB - Terminal 1 |  | Confirmed |  |  |  |  |  |  |  |  |  |
| 5 | ชื่อย่อผู้ให้สัมปทาน |  |  |  |  |  | KPS_R_CONCESS | CON_SNAME | VARCHAR2 | 10.0 | N | Ready |  | Text | Yes | AOT |  | Confirmed |  |  |  |  |  |  |  |  |  |
| 6 | ชื่อผู้รับสัมปทาน |  | RCON_SNAME RCON_LNAME | VARCHAR2 VARCHAR2 | 10 100 | N N | KPS_R_CONCESS | RCON_LNAME | VARCHAR2 | 100.0 | N | Ready |  | Text | Yes | บริษัท คิงเพาเวอร์ สุวรรณภูมิ จำกัด |  | Confirmed |  |  |  |  |  |  |  |  |  |
| 7 | ชื่อย่อผู้รับสัมปทาน |  |  |  |  |  | KPS_R_CONCESS | RCON_SNAME | VARCHAR2 | 10.0 | N | Ready |  | Text | Yes | KPS |  | Confirmed |  |  |  |  |  |  |  |  |  |
| 8 | Location |  | LOCATION | VARCHAR2 | 60 | N | KPS_R_CONCESS | LOCATION | VARCHAR2 | 60.0 | N | Ready |  | Text | Yes | ท่าอากาศยานสุวรรณภูมิ |  | Confirmed |  |  |  |  |  |  |  |  |  |
| 9 | Start Date |  | BEGIN_DATE | VARCHAR2 | 10 | Y | KPS_R_CONCESS | BEGIN_DATE | VARCHAR2 | 10.0 | Y | Ready |  | Date | Yes |  |  | Confirmed |  | - Start Date ต้องไม่มากกว่า End Date - รูปแบบ: DD/MM/YYYY เป็น คริสต์ศักราช |  |  |  |  |  |  |  |
| 10 | End Date |  | END_DATE | VARCHAR2 | 10 | Y | KPS_R_CONCESS | END_DATE | VARCHAR2 | 10.0 | Y | Ready |  | Date | Yes |  |  | Confirmed |  | - End Date ต้องไม่น้อยกว่า Start Date - รูปแบบ: DD/MM/YYYY เป็น คริสต์ศักราช |  |  |  |  |  |  |  |
| 11 | Concession Status |  |  |  |  |  | KPS_R_CONCESS | ACTIVE_FLAG | NUMBER | 22.0 | Y | Ready |  | Picklist | Yes | - Active - Inactive | สถานะสัมปทาน | Confirmed |  | - เลือกข้อมูลตามตัวเลือกที่กำหนด - ข้อมูลจะถูกปรับอัตโนมัติหลังจากที่หมดอายุสัญญา  |  |  |  |  |  |  |  |
| 12 | รอบปีงบประมาณ (From) |  | ACT_DATE_AS_OF | DATE | 7 | Y |  |  |  |  |  | Ready |  | Date | Yes |  |  | Confirmed |  | SVB:               01/July - 30/June DMK & HKT:  01/October - 30/September |  |  |  |  |  |  |  |
| 13 | รอบปีงบประมาณ (To) |  |  |  |  |  |  |  |  |  |  | Ready |  | Date | Yes |  |  | Confirmed |  |  |  |  |  |  |  |  |  |
|  | การปรับส่วนแบ่งรายได้ตามมาตรการช่วยเหลือตามที่ ทอท. กำหนด (ผู้โดยสารจะมากกว่าปี 2562) |  | <New> |  |  |  |  |  |  |  |  | New |  |  |  | ปัจจุบันคือการปรับส่วนแบ่งรายได้ขั้นต่ำของ  - ใช่ = DMK, HKT - ไม่ใช่ = SVB |  |  |  |  |  |  |  |  |  |  |  |
| Concession Area |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 14 | Total Area |  | CON_TOTAL_AREA | NUMBER | 22 | Y | KPS_R_CONCESS | CON_TOTAL_AREA | NUMBER | 22.0 | Y | Ready |  | Number(1,3) | Yes | 5.000 |  | Confirmed |  | - กรอกได้เฉพาะตัวเลขเท่านั้น - รูปแบบ: #.### |  |  |  |  |  |  |  |
| 15 | Commercial Area |  | CON_COMM_AREA | NUMBER | 22 | Y | KPS_R_CONCESS | CON_COMM_AREA | NUMBER | 22.0 | Y | Ready |  | Number(1,3) | Yes | 5.000 |  | Confirmed |  | " |  |  |  |  |  |  |  |
| 16 | M&E Area |  | CON_ME_AREA | NUMBER | 22 | Y | KPS_R_CONCESS | CON_ME_AREA | NUMBER | 22.0 | Y | Ready |  | Number(1,3) | Yes | 0.000 |  | Confirmed |  | " |  |  |  |  |  |  |  |
| 17 | Store Area |  | CON_STORE_AREA | NUMBER | 22 | Y | KPS_R_CONCESS | CON_STORE_AREA | NUMBER | 22.0 | Y | Ready |  | Number(1,3) | Yes | 0.000 |  | Confirmed |  | " |  |  |  |  |  |  |  |
| 18 | Other Area |  |  |  |  |  |  |  |  |  |  | Ready |  | Number(1,3) | Yes | 0.000 |  | Confirmed |  | " |  |  |  |  |  |  |  |
| Actual Area |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 19 | Total Area |  | ACT_TOT_AREA | NUMBER | 22 | Y | KPS_R_CONCESS | ACT_TOT_AREA | NUMBER | 22.0 | Y | Ready |  | Number(1,3) | Yes | 5.000 |  | Confirmed |  | " |  |  |  |  |  |  |  |
| 20 | Commercial Area |  | ACT_COMM_AREA | NUMBER | 22 | Y | KPS_R_CONCESS | ACT_COMM_AREA | NUMBER | 22.0 | Y | Ready |  | Number(1,3) | Yes | 5.000 |  | Confirmed |  | " |  |  |  |  |  |  |  |
| 21 | M&E Area |  | ACT_ME_AREA | NUMBER | 22 | Y | KPS_R_CONCESS | ACT_ME_AREA | NUMBER | 22.0 | Y | Ready |  | Number(1,3) | Yes | 0.000 |  | Confirmed |  | " |  |  |  |  |  |  |  |
| 22 | Store Area |  | ACT_STORE_AREA | NUMBER | 22 | Y | KPS_R_CONCESS | ACT_STORE_AREA | NUMBER | 22.0 | Y | Ready |  | Number(1,3) | Yes | 0.000 |  | Confirmed |  | " |  |  |  |  |  |  |  |
| 23 | Other Area |  | <TBC> |  |  |  |  |  |  |  |  | TBC |  | Number(1,3) | Yes | 0.000 |  | Confirmed |  | " |  |  |  |  |  |  |  |
| Occupied Area |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 24 | Total Area |  | <New> |  |  |  |  |  |  |  |  | New |  | Number(1,3) | Yes | 5.000 |  | Confirmed |  | " |  |  |  |  |  |  |  |
| 25 | Commercial Area |  | <New> |  |  |  |  |  |  |  |  | New |  | Number(1,3) | Yes | 5.000 |  | Confirmed |  | " |  |  |  |  |  |  |  |
| 26 | M&E Area |  | <New> |  |  |  |  |  |  |  |  | New |  | Number(1,3) | Yes | 0.000 |  | Confirmed |  | " |  |  |  |  |  |  |  |
| 27 | Store Area |  | <New> |  |  |  |  |  |  |  |  | New |  | Number(1,3) | Yes | 0.000 |  | Confirmed |  | " |  |  |  |  |  |  |  |
| 28 | Other Area |  | <New> |  |  |  |  |  |  |  |  | New |  | Number(1,3) | Yes | 0.000 |  | Confirmed |  | " |  |  |  |  |  |  |  |
| Vacant Area |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 29 | Total Area |  | <New> |  |  |  |  |  |  |  |  | New |  | Number(1,3) | Yes | 5.000 |  | Connfirmed |  | " |  |  |  |  |  |  |  |
| 30 | Commercial Area |  | <New> |  |  |  |  |  |  |  |  | New |  | Number(1,3) | Yes | 5.000 |  | Connfirmed |  | " |  |  |  |  |  |  |  |
| 31 | M&E Area |  | <New> |  |  |  |  |  |  |  |  | New |  | Number(1,3) | Yes | 0.000 |  | Connfirmed |  | " |  |  |  |  |  |  |  |
| 32 | Store Area |  | <New> |  |  |  |  |  |  |  |  | New |  | Number(1,3) | Yes | 0.000 |  | Connfirmed |  | " |  |  |  |  |  |  |  |
| 33 | Other Area |  | <New> |  |  |  |  |  |  |  |  | New |  | Number(1,3) | Yes | 0.000 |  | Connfirmed |  | " |  |  |  |  |  |  |  |
| SAP Information |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 34 | SAP Company Code |  | SAP_COMPANY_CODE | VARCHAR2 | 4 | Y | KPS_R_CONCESS | SAP_COMPANY_CODE | VARCHAR2 | 4.0 | Y | Ready |  | Number(4,0) | Yes | 6000 |  | Confirmed |  |  |  |  |  |  |  |  |  |
| 35 | SAP Business Place |  | SAP_BUSINESS_PLACE | VARCHAR2 | 4 | Y | KPS_R_CONCESS | SAP_BUSINESS_PLACE | VARCHAR2 | 4.0 | Y | Ready |  | Number(4,0) | Yes | 0001 |  | Confirmed |  |  |  |  |  |  |  |  |  |
| 36 | SAP Business Area |  | SAP_BUSINESS_AREA | VARCHAR2 | 4 | Y | KPS_R_CONCESS | SAP_BUSINESS_AREA | VARCHAR2 | 4.0 | Y | Ready |  | Number(4,0) | Yes | 2111 |  | Confirmed |  |  |  |  |  |  |  |  |  |
| 37 | SAP Cost Center |  | SAP_COST_CENTER | VARCHAR2 | 10 | Y | KPS_R_CONCESS | SAP_COST_CENTER | VARCHAR2 | 10.0 | Y | Ready |  | Number(10,0) | Yes | 6211100000 |  | Confirmed |  |  |  |  |  |  |  |  |  |
| 38 | SAP Funds Center |  | SAP_FUNDS_CENTER | VARCHAR2 | 10 | Y | KPS_R_CONCESS | SAP_FUNDS_CENTER | VARCHAR2 | 10.0 | Y | Ready |  | Number(10,0) | Yes | 6211100000 |  | Confirmed |  |  |  |  |  |  |  |  |  |
| 39 | SAP Airport |  | SAP_TEXT_AIRPORT | VARCHAR2 | 20 | Y | KPS_R_CONCESS | SAP_TEXT_AIRPORT | VARCHAR2 | 20.0 | Y | Ready |  | Text | Yes | SVB |  | Confirmed |  |  |  |  |  |  |  |  |  |
| Concession Contract |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Concession Contract No. |  | <New> |  |  |  |  |  |  |  |  | New |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Contract Date |  | <New> |  |  |  |  |  |  |  |  | New |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Minimum Guarantee |  | <New> |  |  |  |  |  |  |  |  | New |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Upfront Amount |  | <New> |  |  |  |  |  |  |  |  | New |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Reference Year |  | <New> |  |  |  |  |  |  |  |  | New |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Revenue Sharing Fixed Amount |  | <New> |  |  |  |  |  |  |  |  | New |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | - Number of Installment |  | <New> |  |  |  |  |  |  |  |  | New |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | - Total Revenue Sharing |  | <New> |  |  |  |  |  |  |  |  | New |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | - Due Date |  | <New> |  |  |  |  |  |  |  |  | New |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | - Amount |  | <New> |  |  |  |  |  |  |  |  | New |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Revenue Sharing - % per month |  | <New> |  |  |  |  |  |  |  |  | New |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Minimum Guarantee |  | <New> |  |  |  |  |  |  |  |  | New |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | - Contract Start Date |  | <New> |  |  |  |  |  |  |  |  | New |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | - Contract End Date |  | <New> |  |  |  |  |  |  |  |  | New |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | - No. of Day(s) |  | <New> |  |  |  |  |  |  |  |  | New |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | - Minimum Guarantee (per day) |  | <New> |  |  |  |  |  |  |  |  | New |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | - Total Area |  | <New> |  |  |  |  |  |  |  |  | New |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | - Commercial Area |  | <New> |  |  |  |  |  |  |  |  | New |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | - M&E Area |  | <New> |  |  |  |  |  |  |  |  | New |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | - Other Area |  | <New> |  |  |  |  |  |  |  |  | New |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | - Cost per SQM |  | <New> |  |  |  |  |  |  |  |  | New |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | - Passenger Growth (%) |  | <New> |  |  |  |  |  |  |  |  | New |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | - Inflation Rate (%) |  | <New> |  |  |  |  |  |  |  |  | New |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | - Remark |  | <New> |  |  |  |  |  |  |  |  | New |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |

---

## 03_Shop Category

| No. | SFDC Field Name (EN) | SFDC Field Name (TH) | Source Field API Name | Source Field Type | Source Field Length | VULLABLE (N=Required) | KP Table | KP Field Name | KP Field Type | KP Field Length | VULLABLE (N=Required).1 | Progress | Confirm | Type | Required | Sample Data | Description | Status | User/KP Feedback | Remark | Help Text | Track History | External ID | Track History.1 | Encrypted | Page Layout | Length | Source Field API Name.1 | Source Field Type.1 | Source Field Length.1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Category |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 1 | Space Owner |  |  |  |  |  | KPS_R_SHOPUNIT KPS_R_SHOPUNIT | OWNER_CODE USG_CODE | VARCHAR2 VARCHAR2 | 30 5 | Y Y | Ready |  |  |  |  |  | New |  |  |  |  |  |  |  |  |  | PROD_CATE_CODE | CHAR | 1.0 |
| 2 | AOT Rental Type |  |  |  |  |  | KPS_R_AOT_RENTAL_TYPE | RNT_CODE | VARCHAR2 | 5 | N | Ready |  |  |  |  |  | New |  |  |  |  |  |  |  |  |  | STD_CATE_ID | NUMBER | 22.0 |
| 3 | Space Usage Type |  |  |  |  |  | KPS_R_SPACE_USAGE KPS_R_SPACE_USAGE | USG_CODE USG_DESC | VARCHAR2 VARCHAR2 | 5 50 | N Y | Ready |  |  |  |  |  | New |  |  |  |  |  |  |  |  |  | STD_CATE_DESC | VARCHAR2 | 200.0 |
| 4 | AOT Shop Category |  |  |  |  |  | KPS_R_AOT_SHOP_CATE | AOT_CATE_CODE | CHAR | 4 | N | Ready |  |  |  |  |  | New |  |  |  |  |  |  |  |  |  | STATUS | NUMBER | 22.0 |
|  | AOT Shop Sub-Category |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  | - Office, LWC, Store, etc. |  | New |  |  |  |  |  |  |  |  |  | CREATEDBY | VARCHAR2 | 30.0 |
|  |  |  | PROD_CATE_CODE | CHAR | 1.0 | N |  |  |  |  |  |  |  |  |  |  |  | New |  |  |  |  |  |  |  |  |  | CREATEDDATE | DATE | 7.0 |
|  |  |  | STD_CATE_ID | NUMBER | 22.0 | N |  |  |  |  |  |  |  |  |  |  |  | New |  |  |  |  |  |  |  |  |  | UPDATEDBY | VARCHAR2 | 30.0 |
|  |  |  | STD_CATE_DESC | VARCHAR2 | 200.0 | Y |  |  |  |  |  |  |  |  |  |  |  | New |  |  |  |  |  |  |  |  |  | UPDATEDDATE | DATE | 7.0 |
|  |  |  | STATUS | NUMBER | 22.0 | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | CREATEDBY | VARCHAR2 | 30.0 | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | CREATEDDATE | DATE | 7.0 | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | UPDATEDBY | VARCHAR2 | 30.0 | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | UPDATEDDATE | DATE | 7.0 | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |

---

## 04_Shop Brand

| No. | SFDC Field Name (EN) | SFDC Field Name (TH) | Source Field API Name | Source Field Type | Source Field Length | VULLABLE (N=Required) | KP Table | KP Field Name | KP Field Type | KP Field Length | VULLABLE (N=Required).1 | Progress | Confirm | Type | Required | Sample Data | Description | Status | User/KP Feedback | Remark | Help Text | Track History | External ID | Track History.1 | Encrypted | Page Layout | Length | Source Field API Name.1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Information |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 1 | Shop Brand Code | SHPBND_CODE | VARCHAR2 | 4.0 | N |  | KPS_R_SHOP_BRAND | SHPBND_CODE | VARCHAR2 | 4.0 | N | Ready |  | Number (4,0) | Yes |  0001 | รหัสแบรนด์ | Confirmed |  | - กรอกได้สูงสุด 4 หลัก - กรอกได้เฉพาะตัวเลขเท่านั้น |  |  |  |  |  |  |  |  |
| 2 | Brand Reputation | <New> |  |  |  |  |  |  |  |  |  | Ready |  | Picklist (Multi-Select) | Yes | - Inter - Local | ชื่อเสียงแบรนด์ | Confirmed |  | - เลือกข้อมูลตามตัวเลือกที่กำหนด - เลือกได้ 1 ตัวเลือก  |  |  |  |  |  |  |  |  |
| 3 | Shop Brand Name - TH | SHPBND_NAME_T | VARCHAR2 | 60.0 | Y |  | KPS_R_SHOP_BRAND | SHPBND_NAME_T | VARCHAR2 | 60.0 | Y | Ready |  | Text | Yes | อิมเพรสซีฟ สุวรรณภูมิ | ชื่อแบรนด์ ภาษาไทย | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 4 | Shop Brand Name - EN | SHPBND_NAME_E | VARCHAR2 | 60.0 | Y |  | KPS_R_SHOP_BRAND | SHPBND_NAME_E | VARCHAR2 | 60.0 | Y | Ready |  | Text | Yes | Impressive Suvarnabhumi | ชื่อแบรนด์ ภาษาอังกฤษ | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 5 | Shop Brand Status | STATUS | NUMBER | 22.0 | Y |  | KPS_R_SHOP_BRAND | STATUS | NUMBER | 22.0 | Y | Ready |  | Picklist | Yes | - Active - Inactive  |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| Product |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Product Category Code |  |  |  |  |  | KPS_T_REQPROD_MD | STD_CATE_CODE | VARCHAR2 | 4.0 | N | Ready |  | Text |  | 5ABD | ประเภท product code   | Confirmed |  |  |  |  |  |  |  |  |  |  |
|  | Product Category |  |  |  |  |  | KPS_R_PROD_SUBCATE1 | PROD_SUBCAT1_DESC | VARCHAR2 | 200.0 | Y | Ready |  | Text |  | Halal food | ประเภท product   | Confirmed |  |  |  |  |  |  |  |  |  |  |
|  | Product Code |  |  |  |  |  | KPS_T_PROD_COMPARE | PROD_SERV_CODE | VARCHAR2 | 100.0 | N | Ready |  | Text |  | 9781801081795 | รหัส product   | Confirmed |  |  |  |  |  |  |  |  |  |  |
|  | Product Name |  |  |  |  |  | KPS_T_PROD_COMPARE | PROD_SERV_NAME | VARCHAR2 | 200.0 | Y | Ready |  | Text |  | ก๋วยเตี๋ยวแห้ง | ชื่อ product   | Confirmed |  |  |  |  |  |  |  |  |  |  |
|  | Sub Product Code |  |  |  |  |  |  |  |  |  |  | Ready |  | Text |  | 9781801081795 | รหัส product ย่อย สำหรับกรณี bundle product   | Confirmed |  |  |  |  |  |  |  |  |  |  |
|  | Sub Product Name |  |  |  |  |  |  |  |  |  |  | Ready |  | Text |  | ก๋วยเตี๋ยวแห้ง มินิ | ชื่อ product ย่อย สำหรับกรณี bundle product   | Confirmed |  |  |  |  |  |  |  |  |  |  |
|  | Sell Price (include VAT) |  |  |  |  |  | KPS_T_PROD_COMPARE | REQ_PRICE_INC_VAT | NUMBER | 22.0 | Y | Ready |  | Number(16,2) |  | 1,070.00 | ราคาขาย รวม VAT   | Confirmed |  |  |  |  |  |  |  |  |  |  |
|  | Previous Sell Price (include VAT) |  |  |  |  |  | KPS_T_PROD_COMPARE | OLD_PRICE_INC_VAT | NUMBER | 22.0 | Y | Ready |  | Number(16,2) |  | 1,000.00 | ราคาขายก่อนหน้า รวม VAT   | Confirmed |  |  |  |  |  |  |  |  |  |  |
|  | Reference Price (include VAT) |  |  |  |  |  | KPS_T_PROD_COMPARE | REF_PRICE_INC_VAT | NUMBER | 22.0 | Y | Ready |  | Number(16,2) |  | 895.00 | ราคาเปรียบเทียบ รวม VAT   | Confirmed |  |  |  |  |  |  |  |  |  |  |
|  | % Different |  |  |  |  |  | KPS_T_PROD_COMPARE | REF_PRICE_EXC_DIFF | NUMBER | 22.0 | Y | Ready |  | Number(16,2) |  | 19.55 | % ความแตกต่างของราคา   | Confirmed |  |  |  |  |  |  |  |  |  |  |
|  | Reference Leading Hotel/Mall |  |  |  |  |  | KPS_T_PROD_COMPARE | REF_SHOP | VARCHAR2 | 100.0 | Y | Ready |  | Text |  | Central World | สถานที่ที่ใช้ในการเปรียบเทียบล่าสุด   | Confirmed |  |  |  |  |  |  |  |  |  |  |
|  | Reference Shop |  |  |  |  |  | KPS_T_PROD_COMPARE | REF_SHOP | VARCHAR2 | 100.0 | Y | Ready |  | Text |  | Asia Books | ร้านค้าที่ใช้ในการเปรียบเทียบล่าสุด   | Confirmed |  |  |  |  |  |  |  |  |  |  |
|  | Remark |  |  |  |  |  | KPS_T_PROD_COMPARE | REMARKS | VARCHAR2 | 200.0 | Y | Ready |  | Text (255) |  |  |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
|  | Related Request No. |  |  |  |  |  |  |  |  |  |  | Ready |  | Text |  |  | เลขที่การขออนุมัติ product ล่าสุด | Confirmed |  |  |  |  |  |  |  |  |  |  |
|  | Related Request Type |  |  |  |  |  | KPS_T_PROD_COMPARE | TRANS_TYPE | NUMBER | 22.0 | Y | Ready |  | Picklist |  | - New Product - Price Increase - Price Decrease - Cancel Product - Promotion | รูปแบบการขออนุมัติปรับปรุงข้อมูลผลิตภัณฑ์ล่าสุด | Confirmed |  |  |  |  |  |  |  |  |  |  |
|  | Tenant Product Reference |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  | ภาพประกอบสินค้า ที่ใช้ในการเปรียบเทียบ | Confirmed |  |  |  |  |  |  |  |  |  |  |
|  | Promotion Code |  |  |  |  |  | KPS_T_APPRV_M | PRO_CODE | VARCHAR2 | 10.0 | Y | Ready |  | Text |  | 010009 | โปรโมชั่นโค้ดของผลิตภัณฑ์   | Confirmed |  |  |  |  |  |  |  |  |  |  |
|  |  | CON_CODE | CHAR | 2.0 | N |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  | SHOP_CODE | VARCHAR2 | 20.0 | N |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |

---

## 05_Shop Branch

| No. | SFDC Field Name (EN) | SFDC Field Name (TH) | Source Field API Name | Source Field Type | Source Field Length | VULLABLE (N=Required) | KP Table | KP Field Name | KP Field Type | KP Field Length | VULLABLE (N=Required).1 | Progress | Confirm | Type | Required | Sample Data | Description | Status | User/KP Feedback | Remark | Help Text | Track History | External ID | Track History.1 | Encrypted | Page Layout | Length | Source Field API Name.1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Information |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 1 | Shop Branch No. |  | BRANCH_NO | NUMBER | 22.0 | N | KPS_R_BRANCH | BRANCH_NO | NUMBER | 22.0 | N | Ready |  | Text (255) | Yes |  |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 2 | Shop Branch Code |  | BRANCH_CODE | VARCHAR2 | 20.0 | N | KPS_R_BRANCH | BRANCH_CODE | VARCHAR2 | 20.0 | N | Ready |  | Text (255) | Yes |  |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 3 | Shop Branch Name - TH |  | BRANCH_NAME_T | VARCHAR2 | 200.0 | Y | KPS_R_BRANCH | BRANCH_NAME_T | VARCHAR2 | 200.0 | Y | Ready |  | Text (255) | Yes |  |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 4 | Shop Branch Name - EN |  | BRANCH_NAME_E | VARCHAR2 | 200.0 | Y | KPS_R_BRANCH | BRANCH_NAME_E | VARCHAR2 | 200.0 | Y | Ready |  | Text (255) | Yes |  |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 5 | Shop Branch Short Name |  | BRANCH_SHOTNAME | VARCHAR2 | 100.0 | Y | KPS_R_BRANCH | BRANCH_SHOTNAME | VARCHAR2 | 100.0 | Y | Ready |  | Text (255) | Yes |  |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 6 | Shop Category (AOT) |  | AOT_CATE_CODE | CHAR | 4.0 | N | KPS_R_BRANCH | AOT_CATE_CODE | CHAR | 4.0 | N | Ready |  | Picklist (Multi-Select) | Yes | - Bank - Communication - F&B - Restaurant - Healthy - Entertainment - Others - Lounge - Travel | ประเภทร้านค้าของ AOT | Confirmed |  | - เลือกข้อมูลตามตัวเลือกที่กำหนด - เลือกได้มากกว่า 1 ตัวเลือก  |  |  |  |  |  |  |  |  |
| 7 | Service Time (Start) |  | <New> |  |  |  |  |  |  |  |  | New |  | Time | No |  | เวลาเปิด ปิด ร้าน เช่น 06:00 - 19:00 | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 8 | Service Time (End) |  | <New> |  |  |  |  |  |  |  |  | New |  | Time | No |  |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| Shop Unit |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 9 | Unit No. |  | SHOP_UNIT | VARCHAR2 | 15.0 | Y | KPS_R_BRANCH | SHOP_UNIT | VARCHAR2 | 15.0 | Y | Ready |  | Text (255) | No |  |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 10 | Total Area |  | AREA | NUMBER | 22.0 | Y | KPS_R_BRANCH | AREA | NUMBER | 22.0 | Y | Ready |  | Number (1,3) | No | 5.000 |  | Confirmed |  | - กรอกได้เฉพาะตัวเลขเท่านั้น - รูปแบบ: #.###  |  |  |  |  |  |  |  |  |
| 11 | Commercial Area |  | COMM_AREA | NUMBER | 22.0 | Y | KPS_R_BRANCH | COMM_AREA | NUMBER | 22.0 | Y | Ready |  | Number (1,3) | No | 5.000 |  | Confirmed |  | " |  |  |  |  |  |  |  |  |
| 12 | Store Area |  | STORE_AREA | NUMBER | 22.0 | Y | KPS_R_BRANCH | STORE_AREA | NUMBER | 22.0 | Y | Ready |  | Number (1,3) | No | 0.000 |  | Confirmed |  | " |  |  |  |  |  |  |  |  |
| 13 | M&E Area |  | MNE_AREA | NUMBER | 22.0 | Y | KPS_R_BRANCH | MNE_AREA | NUMBER | 22.0 | Y | Ready |  | Number (1,3) | No | 0.000 |  | Confirmed |  | " |  |  |  |  |  |  |  |  |
| 14 | Other Area |  | OTH_AREA | NUMBER | 22.0 | Y | KPS_R_BRANCH | OTH_AREA | NUMBER | 22.0 | Y | Ready |  | Number (1,3) | No | 0.000 |  | Confirmed |  | " |  |  |  |  |  |  |  |  |
| POS |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 15 | POS No. |  | <New> |  |  |  | KPS_R_POS | POS_NO | VARCHAR2 | 50.0 | N | New |  | Text (255) |  | E05112000200866 | หมายเลขเครื่อง POS | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 16 | POS Status |  | <New> |  |  |  | KPS_R_POS | STATUS | NUMBER | 22.0 | Y | New |  | Picklist | - Active - Inactive  |  | สถานะเครื่อง POS | Confirmed |  |  |  |  |  |  |  |  |  |  |
| Shop Holiday/Event  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 17 | Date Period (From) |  | <New> |  |  |  |  |  |  |  |  | New |  | Date |  |  | ช่วงวันที่ปิดร้าน (ปี คศ.) Format: DD/MM/YYYY | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 18 | Date Period (To) |  | <New> |  |  |  |  |  |  |  |  | New |  | Date |  |  |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 19 | Shop Holiday/Event - Reason |  | <New> |  |  |  |  |  |  |  |  | New |  | Text |  | งานเลี้ยงปีใหม่ | หมายเหตุ | Confirmed |  |  |  |  |  |  |  |  |  |  |
| Shop Contact Person |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 20 | Name-Surname |  | BLL_NAME | VARCHAR2 | 200.0 | Y | KPS_R_SHOP_CONT_PER | CONT_NAME | VARCHAR2 | 50.0 | N | Ready |  | Text |  |  |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 21 | Position |  | <New> |  |  |  | KPS_R_SHOP_CONT_PER | CONT_POST | VARCHAR2 | 50.0 | Y | New |  | Text |  |  |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 22 | Mobile No. |  | BLL_TEL | VARCHAR2 | 100.0 | Y | KPS_R_SHOP_CONT_PER | CONT_PHONE_NO | VARCHAR2 | 30.0 | Y | Ready |  | Phone |  |  |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 23 | Email Address |  | <New> |  |  |  | KPS_R_SHOP_CONT_PER | CONT_EMAIL_ADDR | VARCHAR2 | 50.0 | Y | New |  | Email |  |  |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
|  |  |  | CON_CODE | CHAR | 2.0 | N |  |  |  |  |  | Not Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | SHOP_CODE | VARCHAR2 | 20.0 | N |  |  |  |  |  | Not Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |

---

## 06_Contract

| No. | SFDC Field Name (EN) | SFDC Field Name (TH) | Source Field API Name | Source Field Type | Source Field Length | VULLABLE (N=Required) | KP Table | KP Field Name | KP Field Type | KP Field Length | VULLABLE (N=Required).1 | Progress | Confirm | Type | Required | Sample Data | Description | Status | User/KP Feedback | Remark | Help Text | Track History | External ID | Track History.1 | Encrypted | Page Layout | Length | Source Field API Name.1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Information |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 1 | Contract No. |  | CONT_NO | VARCHAR2 | 30.0 | N | KPS_T_CONTRACT | CONT_NO | VARCHAR2 | 30 | N | Ready | Y | Text | Yes | KPS 14/2564 | เลขที่สัญญา | Confirmed |  |  |  |  |  |  |  |  |  |  |
| Contract Period |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 2 | Period |  |  |  |  |  | Hard code  -Year |  |  |  |  | Ready | Y | Picklist | Yes | - Month - Year | ช่วงสัญญา | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 3 | Value |  |  |  |  |  | KPS_T_CONTRACT | CONT_PERIOD_YEAR | NUMBER | 22 | N | Ready | Y | Number | Yes | 10 เดือน | จำนวน | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 4 | Contract Sign Date |  |  |  |  |  | KPS_T_CONTRACT | CONT_DATE | DATE | 7 | Y | Ready | Y | Date | Yes | 28/09/2020 | วันที่เซ็นสัญญา เช่น  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 5 | Contract Start Date |  |  |  |  |  | KPS_T_CONTRACT | CONT_STR_DATE | DATE | 7 | N | Ready | Y | Date | Yes | 28/09/2020 | วันที่จดทะเบียนผู้ประกอบการ | Confirmed |  | - รูปแบบ: DD/MM/YYYY เป็น คริสต์ศักราช |  |  |  |  |  |  |  |  |
| 6 | Contract End Date |  |  |  |  |  | KPS_T_CONTRACT | CONT_END_DATE | DATE | 7 | N | Ready | Y | Date | Yes | 28/09/2020 | วันที่จดทะเบียนผู้ประกอบการ | Confirmed |  | - รูปแบบ: DD/MM/YYYY เป็น คริสต์ศักราช |  |  |  |  |  |  |  |  |
| Shop |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 7 | Shop Branch Code |  |  |  |  |  | KPS_T_CONT_SHOP_UNIT | BRANCH_CODE | VARCHAR2 | 20 | N | Ready | Y | Text | Yes |  | รหัสร้านค้าผู้ประกอบการ | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 8 | Shop Branch Name |  |  |  |  |  | KPS_R_BRANCH | BRANCH_NAME_T | VARCHAR2 | 200 | Y | Ready | Y | Text | Yes |  | ชื่อร้านค้าผู้ประกอบการ | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 9 | Open Date |  |  |  |  |  | KPS_T_CONT_SHOP_UNIT | SHOP_STR_DATE | DATE | 7 | Y | Ready | Y | Date | Yes |  | วันที่เปิดร้าน | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 10 | Closed |  |  |  |  |  | KPS_T_CONT_SHOP_UNIT | SHOP_END_DATE | DATE | 7 | Y | Ready | Y | Date | Yes |  | วันที่ปิดร้าน | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 11 | Shop Brand Code |  |  |  |  |  | KPS_T_CONT_TENT_SHOPBRAND | SHPBND_CODE | VARCHAR2 | 4 | N | Ready | Y | Text | Yes |  | รหัสแบรนด์ของผู้ประกอบการ | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 12 | Shop Brand Name - TH |  |  |  |  |  | KPS_T_CONT_TENT_SHOPBRAND.KPS_R_SHOP_BRAND | SHPBND_NAME_T | VARCHAR2 | 60 | Y | Ready | Y | Text | Yes |  | ชื่อแบรนด์ ภาษาไทย | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 13 | Shop Brand Name - EN |  |  |  |  |  | KPS_T_CONT_TENT_SHOPBRAND.KPS_R_SHOP_BRAND | SHPBND_NAME_E | VARCHAR2 | 60 | Y | Ready | Y | Text | Yes |  | ชื่อแบรนด์ ภาษาอังกฤษ | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 14 | Brand Status |  |  |  |  |  | KPS_T_CONT_TENT_SHOPBRAND.KPS_R_SHOP_BRAND | STATUS(1=Active,2=Inactive) | NUMBER | 22 | Y | Ready | Y | Text | Yes | - Active - Inactive |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 15 | Remark |  |  |  |  |  | KPS_T_CONTRACT | CONT_REMARK | VARCHAR2 | 500 | Y | Ready | Y | Text |  |  | หมายเหตุ | Confirmed |  |  |  |  |  |  |  |  |  |  |
| Contract Unit |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 16 | Original Unit No. |  |  |  |  |  | ไม่มีใน TMS  | SRC_UNIT | VARCHAR2 | 15 | N | Ready | Y | Text | Yes |  | เลขที่ Unit จากแหล่งข้อมูล | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 17 | KPS Unit No. |  |  |  |  |  | KPS_T_CONT_SHOP_UNIT | SHOP_UNIT | VARCHAR2 | 15 | N | Ready | Y | Text | Yes |  | เลขที่ Unit ของ KPS | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 18 | Floor |  |  |  |  |  | KPS_R_SHOPUNIT | LEVEL_CODE | VARCHAR2 | 3 | Y | Ready | Y | Text | Yes |  | ชั้น | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 19 | Building |  |  |  |  |  | KPS_R_SHOPUNIT | B_CODE | VARCHAR2 | 3 | Y | Ready | Y | Text | Yes |  | ตึก | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 20 | Wing |  |  |  |  |  | KPS_R_SHOPUNIT | W_CODE | VARCHAR2 | 3 | Y | Ready | Y | Text | Yes |  | วิง | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 21 | Zone |  |  |  |  |  | KPS_R_SHOPUNIT | ZONE_CODE | VARCHAR2 | 3 | Y | Ready | Y | Text | Yes |  | โซน | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 22 | Start Date |  |  |  |  |  | KPS_R_SHOPUNIT | START_DATE | DATE | 7 | Y | Ready | Y | Date | Yes |  |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 23 | Cancel Date |  |  |  |  |  | KPS_R_SHOPUNIT | END_DATE | DATE | 7 | Y | Ready | Y | Date | No |  |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 24 | Cancel Remark |  |  |  |  |  | KPS_R_SHOPUNIT | END_REASON | VARCHAR2 | 200 | Y | Ready | Y | Text | No |  |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| Actual Area |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 25 | Total Area |  |  |  |  |  | KPS_R_SHOPUNIT | ACT_TOT_AREA | NUMBER | 22 | Y | Ready | Y | Number(1,3) | Yes | 5.000 |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 26 | Commercial Area |  |  |  |  |  | KPS_R_SHOPUNIT | ACT_COMM_AREA | NUMBER | 22 | Y | Ready | Y | Number(1,3) | Yes | 5.000 |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 27 | M&E Area |  |  |  |  |  | KPS_R_SHOPUNIT | ACT_ME_AREA | NUMBER | 22 | Y | Ready | Y | Number(1,3) | Yes | 0.000 |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 28 | Store Area |  |  |  |  |  | KPS_R_SHOPUNIT | ACT_STORE_AREA | NUMBER | 22 | Y | Ready | Y | Number(1,3) | Yes | 0.000 |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 29 | Other Area |  |  |  |  |  | ไม่มีใน TMS |  |  |  |  | Ready | Y | Number(1,3) | Yes | 0.000 |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| Contract Area |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 30 | Total Area |  |  |  |  |  | KPS_R_BRANCH | AREA | NUMBER | 16,3 | Y | Ready | Y | Number(1,3) | Yes | 5.000 |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 31 | Commercial Area |  |  |  |  |  | KPS_R_BRANCH | COMM_AREA | NUMBER | 16,3 | Y | Ready | Y | Number(1,3) | Yes | 5.000 |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 32 | M&E Area |  |  |  |  |  | KPS_R_BRANCH | MNE_AREA | NUMBER | 16,3 | Y | Ready | Y | Number(1,3) | Yes | 0.000 |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 33 | Store Area |  |  |  |  |  | KPS_R_BRANCH | STORE_AREA | NUMBER | 16,3 | Y | Ready | Y | Number(1,3) | Yes | 0.000 |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 34 | Other Area |  |  |  |  |  | KPS_R_BRANCH | OTH_AREA | NUMBER | 16,3 | Y | Ready | Y | Number(1,3) | Yes | 0.000 |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| Information |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Shop Open Date Criteria |  | <New> |  |  |  |  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Expected Open Date |  | <New> |  |  |  |  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Deposit for reservation (inc. VAT) |  | <New> |  |  |  |  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Minimum Guarantee Adjustment Condition |  | <New> |  |  |  |  |  |  |  |  | New | Y |  |  | - % Passenger Growth - Fixed Rate - Fixed Amount | เงื่อนไขการปรับฐานส่วนแบ่งรายได้ขั้นต่ำ |  |  |  |  |  |  |  |  |  |  |  |
|  | Inflation Rate |  | <New> |  |  |  |  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Criteria |  | <New> |  |  |  |  |  |  |  |  | New | Y |  |  | วันที่เริ่มปรับส่วนแบ่งรายได้ขั้นต่ำ - วันที่เปิดร้านครบ 12 เดือน - วันที่ครบรอบปีงบประมาณ - วันที่ … (ระบุ) | วันที่เริ่มปรับฐานส่วนแบ่งรายได้ขั้นต่ำ |  |  |  |  |  |  |  |  |  |  |  |
|  | จำนวนเงินชำระล่วงหน้า (Upfront) |  | <New> |  |  |  |  |  |  |  |  | New | Y |  |  |  | จำนวนเงินชำระล่วงหน้า |  |  |  |  |  |  |  |  |  |  |  |
|  | - เงื่อนไขการตัดชำระ |  | <New> |  |  |  |  |  |  |  |  | New | Y |  |  | - ค่าเช่า - ส่วนแบ่งรายได้ |  |  |  |  |  |  |  |  |  |  |  |  |
|  | - ช่วงเวลาการตัดชำระ (from-to) |  | <New> |  |  |  |  |  |  |  |  | New | Y |  |  | 07/25 - 12/25 |  |  |  |  |  |  |  |  |  |  |  |  |
|  | - จำนวนเงิน |  | <New> |  |  |  |  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | - จำนวนเงินคงเหลือ |  | <New> |  |  |  |  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Discount |  | <New> |  |  |  |  |  |  |  |  | New | Y |  |  | - บาท / % | ส่วนลด |  |  |  |  |  |  |  |  |  |  |  |
|  | - เงือนไข |  | <New> |  |  |  |  |  |  |  |  | New | Y |  |  | - ค่าเช่า - ส่วนแบ่งรายได้ |  |  |  |  |  |  |  |  |  |  |  |  |
|  | - จำนวน (เงิน/%) |  | <New> |  |  |  |  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | - ช่วงเวลาการให้ส่วนลด (from-to) |  | <New> |  |  |  |  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | หลักประกันสัญญาอนุญาติ |  | <New> |  |  |  |  |  |  |  |  | New | Y |  |  | - Bank Guarantee - Cash  - Cheque |  |  |  |  |  |  |  |  |  |  |  |  |
|  | - Period |  | <New> |  |  |  |  |  |  |  |  | New | Y |  |  | - เดือน - ปี |  |  |  |  |  |  |  |  |  |  |  |  |
|  | - ระยะเวลา |  | <New> |  |  |  |  |  |  |  |  | New | Y |  |  | - 1 - 2 |  |  |  |  |  |  |  |  |  |  |  |  |
|  | - No. |  | <New> |  |  |  |  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | - Bank Name |  | <New> |  |  |  |  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | - Start Date |  | <New> |  |  |  |  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | - End Date |  | <New> |  |  |  |  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | - Amount |  | <New> |  |  |  |  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | - Remark |  | <New> |  |  |  |  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Rental Rate |  | <New> |  |  |  |  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | ค่าบริการการใช้อาคาร |  | <New> |  |  |  |  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | ภาษีที่ดิน และสิ่งปลูกสร้าง |  | <New> |  |  |  |  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  หลักประกันสัญญาอนุญาติ - เงินสด ก่อน VAT |  | <New> |  |  |  |  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  VAT |  | <New> |  |  |  |  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  หลักประกันสัญญาอนุญาติ - เงินสด รวม VAT |  | <New> |  |  |  |  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | เงินประกันค่าเช่าพื้นที่ ก่อน VAT |  | <New> |  |  |  |  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | VAT |  | <New> |  |  |  |  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | เงินประกันค่าเช่าพื้นที่ รวม VAT |  | <New> |  |  |  |  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | เงินประกันค่าบริการใช้อาคาร ก่อน VAT |  | <New> |  |  |  |  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | VAT |  | <New> |  |  |  |  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | เงินประกันค่าบริการใช้อาคาร รวม VAT |  | <New> |  |  |  |  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | เงินประกันภาษีที่ดินและสิ่งปลูกสร้าง ก่อน VAT |  | <New> |  |  |  |  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | VAT |  | <New> |  |  |  |  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | เงินประกันภาษีที่ดินและสิ่งปลูกสร้าง รวม VAT |  | <New> |  |  |  |  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | รวมหลักประกันสัญญาเช่า |  | <New> |  |  |  |  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | รวมเงินทำสัญญา ก่อน VAT |  | <New> |  |  |  |  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | VAT |  | <New> |  |  |  |  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | รวมเงินทำสัญญา รวม VAT |  | <New> |  |  |  |  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Minimum Guarantee (excl. VAT) |  | <New> |  |  |  |  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | VAT |  | <New> |  |  |  |  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Minimum Guarantee (incl. VAT) |  | <New> |  |  |  |  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Rental Fee (exc. VAT) |  | <New> |  |  |  |  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | VAT |  | <New> |  |  |  |  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Rental Fee (incl. VAT) |  | <New> |  |  |  |  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Service Fee (exc. VAT) |  | <New> |  |  |  |  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | VAT |  | <New> |  |  |  |  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Service Fee (incl. VAT) |  | <New> |  |  |  |  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Total Monthly Fee (exc. VAT) |  | <New> |  |  |  |  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | VAT |  | <New> |  |  |  |  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Total Monthly Fee (incl. VAT) |  | <New> |  |  |  |  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Contract Status |  | <New> |  |  |  |  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | LG Contract No. |  | <New> |  |  |  |  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Shop Layout |  | <New> |  |  |  |  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Shop Image |  | <New> |  |  |  |  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | เงินประกันตกแต่ง |  | <New> |  |  |  |  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Shop Handover Date |  | <New> |  |  |  |  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Shop Open Date (Protocol) |  | <New> |  |  |  |  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Shop Open Date (Actual) |  | <New> |  |  |  |  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Last Revenue Sharing Date |  | <New> |  |  |  |  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Shop Return Date |  | <New> |  |  |  |  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Shop Closure Date |  | <New> |  |  |  |  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Shop Closed Reason |  | <New> |  |  |  |  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |

---

## 07_Sub Contract

| No. | SFDC Field Name (EN) | SFDC Field Name (TH) | Source Field API Name | Source Field Type | Source Field Length | VULLABLE (N=Required) | KP Table | KP Field Name | KP Field Type | KP Field Length | VULLABLE (N=Required).1 | Progress | Confirm | Type | Required | Sample Data | Description | Status | User/KP Feedback | Remark | Help Text | Track History | External ID | Track History.1 | Encrypted | Page Layout | Length | Source Field API Name.1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Information |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 1 | Concession No. |  | CON_CODE | CHAR | 2.0 | N | KPS_T_CONT_SUB_CONT | CON_CODE | CHAR | 2 | N | Ready |  |  | Yes | 09 – SVB Terminal 1 | เลขสัมปทาน  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 2 | Master Contract No. |  | CONT_NO | VARCHAR2 | 30.0 | N | KPS_T_CONT_SUB_CONT | CONT_NO | VARCHAR2 | 30 | N | Ready |  |  | Yes | KPS 14/2564 | เลขที่สัญญาหลัก | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 3 | Company Code |  | SHOP_CODE | CHAR | 18.0 | Y | KPS_T_CONTRACT | SHOP_CODE | VARCHAR2 | 20 | Y | Ready |  |  | Yes | 0903001 | รหัสบริษัทตามสัญญาหลัก | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 4 | Company Name |  | <New> |  |  |  | KPS_R_SHOP | REGISTERED_NAME | VARCHAR2 | 200 | Y | New |  |  | Yes | บริษัท คิง พาวเวอร์ แท็กซ์ฟรี จำกัด | ชื่อบริษัทตามสัญญาหลัก | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 5 | Sub-Contract No. |  | SUB_CONT_NO | CHAR | 18.0 | Y | KPS_T_CONT_SUB_CONT | SUBCONT_NO | VARCHAR2 | 30 | N | Ready |  |  | Yes | KPT-S-14/2564 | เลขที่สัญญา Sub Contract | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 6 | Sub-Contractor - Company Code |  | <New> |  |  |  | KPS_T_CONT_SUB_CONT | SHOP_CODE | VARCHAR2 | 20 | Y | New |  |  | Yes | 0903012 | เลขที่ผู้ประกอบการ | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 7 | Sub-Contractor - Company Name |  | <New> |  |  |  | KPS_R_SHOP | REGISTERED_NAME | VARCHAR2 | 200 | Y | New |  |  | Yes | บริษัท ซีพี ออลล์ จำกัด (มหาชน) | ชื่อผู้ประกอบการ  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 8 | Contract Area |  | <New> |  |  |  | KPS_T_CONT_SUB_CONT | SUBCONT_AREA | NUMBER | 22 | Y | New |  |  |  |  |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 9 | Sub-Contract Status |  | <New> |  |  |  |  |  |  |  |  | New |  |  |  |  | สถานะสัญญา Sub-Contract | Confirmed |  |  |  |  |  |  |  |  |  |  |
| Contract Period |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 10 | Period |  | CONT_DATE | CHAR | 10.0 | Y | Fix - Year |  |  |  |  | Ready |  | Picklist | Yes | - Month - Year | ช่วงสัญญา | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 11 | Value |  | NUM_YEAR | NUMBER | 22.0 | Y | KPS_T_CONT_SUB_CONT | SUBCONT_PERIOD | NUMBER | 22 | Y | Ready |  | Number | Yes | 10 เดือน | จำนวน | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 12 | Contract Sign Date |  | CONT_DATE | CHAR | 10.0 | Y | KPS_T_CONT_SUB_CONT | SUBCONT_SIGN_DATE | DATE | 7 | Y | Ready |  | Date | Yes | 28/09/2020 | วันที่เซ็นสัญญา เช่น  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 13 | Contract Start Date |  | CONT_STR_DATE | CHAR | 10.0 | Y | KPS_T_CONT_SUB_CONT | SUBCONT_STR_DATE | DATE | 7 | Y | Ready |  | Date | Yes | 28/09/2020 | วันที่จดทะเบียนผู้ประกอบการ | Confirmed |  | - รูปแบบ: DD/MM/YYYY เป็น คริสต์ศักราช |  |  |  |  |  |  |  |  |
| 14 | Contract End Date |  | CONT_END_DATE | CHAR | 10.0 | Y | KPS_T_CONT_SUB_CONT | SUBCONT_END_DATE | DATE | 7 | Y | Ready |  | Date | Yes | 28/09/2020 | วันที่จดทะเบียนผู้ประกอบการ | Confirmed |  | - รูปแบบ: DD/MM/YYYY เป็น คริสต์ศักราช |  |  |  |  |  |  |  |  |
| Shop |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 15 | Shop Branch Code |  | <New> |  |  |  | KPS_T_CONT_SHOP_UNIT | BRANCH_CODE | VARCHAR2 | 20 | N | New |  | Text | Yes |  | รหัสร้านค้าผู้ประกอบการ | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 16 | Shop Branch Name |  | <New> |  |  |  | KPS_R_BRANCH | BRANCH_NAME_T | VARCHAR2 | 200 | Y | New |  | Text | Yes |  | ชื่อร้านค้าผู้ประกอบการ | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 17 | Open Date |  | <New> |  |  |  | KPS_T_CONT_SHOP_UNIT | SHOP_STR_DATE | DATE | 7 | Y | New |  | Date | Yes |  | วันที่เปิดร้าน | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 18 | Closed |  | <New> |  |  |  | KPS_T_CONT_SHOP_UNIT | SHOP_END_DATE | DATE | 7 | Y | New |  | Date | Yes |  | วันที่ปิดร้าน | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 19 | Shop Brand Code |  | <New> |  |  |  | KPS_T_CONT_TENT_SHOPBRAND | SHPBND_CODE | VARCHAR2 | 4 | N | New |  | Text | Yes |  | รหัสแบรนด์ของผู้ประกอบการ | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 20 | Shop Brand Name - TH |  | <New> |  |  |  | KPS_R_SHOP_BRAND | SHPBND_NAME_T | VARCHAR2 | 60 | Y | New |  | Text | Yes |  | ชื่อแบรนด์ ภาษาไทย | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 21 | Shop Brand Name - EN |  | <New> |  |  |  | KPS_R_SHOP_BRAND | SHPBND_NAME_E | VARCHAR2 | 60 | Y | New |  | Text | Yes |  | ชื่อแบรนด์ ภาษาอังกฤษ | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 22 | Brand Status |  | <New> |  |  |  | KPS_R_SHOP_BRAND | STATUS | NUMBER | 22 | Y | New |  | Text | Yes | - Active - Inactive |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 23 | Remark |  | <New> |  |  |  | KPS_T_CONT_SHOP_UNIT | REMARK_T | VARCHAR2 | 100 | Y | New |  | Text |  |  | หมายเหตุ | Confirmed |  |  |  |  |  |  |  |  |  |  |
| Contract Unit |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 24 | Original Unit No. |  | <New> |  |  |  | KPS_T_CONT_SHOP_UNIT | SHOP_UNIT | VARCHAR2 | 15 | N | New |  | Text | Yes |  | เลขที่ Unit จากแหล่งข้อมูล | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 25 | KPS Unit No. |  | <New> |  |  |  | KPS_T_SRC_UNIT | SRC_UNIT | VARCHAR2 | 15 | N | New |  | Text | Yes |  | เลขที่ Unit ของ KPS | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 26 | Floor |  | <New> |  |  |  | KPS_R_SHOPUNIT | LEVEL_CODE | VARCHAR2 | 3 | Y | New |  | Text | Yes |  | ชั้น | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 27 | Building |  | <New> |  |  |  | KPS_R_SHOPUNIT | B_CODE | VARCHAR2 | 3 | Y | New |  | Text | Yes |  | ตึก | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 28 | Wing |  | <New> |  |  |  | KPS_R_SHOPUNIT | W_CODE | VARCHAR2 | 3 | Y | New |  | Text | Yes |  | วิง | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 29 | Zone |  | <New> |  |  |  | KPS_R_SHOPUNIT | ZONE_CODE | VARCHAR2 | 3 | Y | New |  | Text | Yes |  | โซน | Confirmed |  |  |  |  |  |  |  |  |  |  |
| Address |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 30 | Building / Village |  | <New> |  |  |  | KPS_R_SHOP KPS_R_SHOP | LOC_BUILDING LOC_VILLAGE | VARCHAR2 VARCHAR2 | 60 60 | Y Y | New |  |  | Yes |  | หมู่บ้าน | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 31 | Address No. |  | <New> |  |  |  | KPS_R_SHOP | LOC_ADDRESS_NO | VARCHAR2 | 50 | Y | New |  |  | Yes |  | เลขที่ | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 32 | Soi |  | <New> |  |  |  | KPS_R_SHOP | LOC_SOI | VARCHAR2 | 50 | Y | New |  |  | Yes |  | ซอย | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 33 | Street |  | <New> |  |  |  | KPS_R_SHOP | LOC_STREET | VARCHAR2 | 50 | Y | New |  |  | Yes |  | ถนน | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 34 | Sub-District |  | <New> |  |  |  | KPS_R_SHOP | LOC_SUB_DISTRICT | VARCHAR2 | 50 | Y | New |  |  | Yes |  | ตำบล | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 35 | District |  | <New> |  |  |  | KPS_R_SHOP | LOC_DISTRICT_CODE | VARCHAR2 | 3 | Y | New |  |  | Yes |  | อำเภอ | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 36 | Province |  | <New> |  |  |  | KPS_R_SHOP | LOC_PROV_CODE | VARCHAR2 | 2 | Y | New |  |  | Yes |  | จังหวัด | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 37 | Zip Code |  | <New> |  |  |  | KPS_R_SHOP | LOC_ZIPCODE | CHAR | 5 | Y | New |  |  | Yes |  | รหัสไปรษณีย์ | Confirmed |  |  |  |  |  |  |  |  |  |  |
| Revenue Sharing |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 38 | Revenue Sharing |  | <New> |  |  |  | KPS_T_CONTRACT KPS_T_SUB_CONT_REV | REVISE_NO REV_SHARE_RATE | VARCHAR2 NUMBER | 10 22 | Y Y | New |  |  |  |  | ส่วนแบ่งรายได้จากการประกอบกิจการ | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 39 | Effective Start Date |  | <New> |  |  |  | KPS_T_SUB_CONT_REV | REV_STR_DATE | DATE | 7 | Y | New |  |  |  |  | วันที่เริ่มต้น | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 40 | Effective End Date |  | <New> |  |  |  | KPS_T_SUB_CONT_REV | REV_END_DATE | DATE | 7 | Y | New |  |  |  |  | วันที่สิ้นสุด | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 41 | Remark |  | <New> |  |  |  | KPS_T_SUB_CONT_REV | REMARK_T | VARCHAR2 | 100 | Y | New |  |  |  |  | หมายเหตุ | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 42 | Minimum Guarantee per SQM. |  | <New> |  |  |  |  |  |  |  |  | New |  |  |  |  | ส่วนแบ่งรายได้ขั้นต่ำ ต่อ ตารางเมตร | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 43 | Contract Year Start |  | <New> |  |  |  | KPS_T_CONT_SUB_CONT | SUBCONT_STR_DATE | DATE | 7 | Y | New |  |  |  |  | วันที่เริ่มต้นปีงบประมาณ | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 44 | Contract Year End |  | <New> |  |  |  | KPS_T_CONT_SUB_CONT | SUBCONT_END_DATE | DATE | 7 | Y | New |  |  |  |  | วันที่สิ้นสุดปีงบประมาณ | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 45 | No. of Day |  | <New> |  |  |  | KPS_T_SUB_CONT_MIN | NUM_DAY | NUMBER | 22 | Y | New |  |  |  |  | จำนวนวัน | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 46 | Minimum Guarantee per day |  | <New> |  |  |  | KPS_T_SUB_CONT_MIN | MIN_GUAR_D_AMT | NUMBER | 22 | Y | New |  |  |  |  | ส่วนแบ่งรายได้ขั้นต่ำ ต่อ ตารางเมตร ต่อวัน | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 47 | Minimum Guarantee Month Rate |  | <New> |  |  |  |  |  |  |  |  | New |  |  |  |  | อัตราสัดส่วนวันที่ประกอบกิจการ | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 48 | Remark |  | <New> |  |  |  | KPS_T_SUB_CONT_MIN | REMARK_T | VARCHAR2 | 100 | Y | New |  |  |  |  | หมายเหตุ | Confirmed |  |  |  |  |  |  |  |  |  |  |
|  |  |  | SEQ | NUMBER | 22.0 | N |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |

---

## 08_Contact

| No. | SFDC Field Name (EN) | SFDC Field Name (TH) | Source Field API Name | Source Field Type | Source Field Length | VULLABLE (N=Required) | KP Table | KP Field Name | KP Field Type | KP Field Length | VULLABLE (N=Required).1 | Progress | Confirm | Type | Required | Sample Data | Description | Status | User/KP Feedback | Help Text | Track History | External ID | Track History.1 | Encrypted | Page Layout | Length |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Information |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 1 | Concession | สัมปทาน | CON_CODE | CHAR | 2.0 | N | KPS_R_SHOP_CONT_PER | CON_CODE | CHAR | 2 | N | Ready |  |  | Yes | 09 : SVB 05 : DMK (Inter) 10 : DMK (DOM) 08 : HKT |  | Confirmed |  |  |  |  |  |  |  |  |
| 2 | Company Name | ชื่อบริษัท |  |  |  |  | KPS_R_SHOP_CONT_PER KPS_R_SHOP | SHOP_CODE REGISTERED_NAME | VARCHAR2 VARCHAR2 | 20 200 | N Y | Ready |  |  | Yes | After You Public Company Limited |  | Confirmed |  |  |  |  |  |  |  |  |
| 3 | Shop Name | ชื่อร้านค้า |  |  |  |  | KPS_R_SHOP | SHORT_NAME | VARCHAR2 | 50 | Y | Ready |  |  | Yes | After You |  | Confirmed |  |  |  |  |  |  |  |  |
| 4 | Unit No. |  |  |  |  |  |  |  |  |  |  |  |  |  |  | T1ME2-24 |  |  |  |  |  |  |  |  |  |  |
| 5 | Type of Contact | ประเภทของเรื่องที่ต้องติดต่อ |  |  |  |  | KPS_R_SHOP_CONT_PER | SUBJECT | VARCHAR2 | 150 | Y | Ready |  |  | Yes | - ข้อร้องเรียน (CAC) - การขออนุมัติราคาสินค้าและบริการ (CAC)  - การตรวจร้านค้า (CAC) - การเข้าก่อสร้าง/เงิน (FAM) - หน้าร้าน Operation (FAM) - F&B (CAD) - Service (CAD) - Bank (CAD) - Airline Operations Contact (MKA) - Airline Finance Contact (MKA) - Merchant Operations Contact (MKA) - Merchant Finance Contact (MKA) - Passengers Complaint - Product & Price  - Shop Inspection - Supplier |  | Confirmed |  |  |  |  |  |  |  |  |
| 6 | Contact Person | ข้อมูลผู้ติดต่อ |  |  |  |  | KPS_R_SHOP_CONT_PER | CONT_NAME | VARCHAR2 | 50 | N | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 7 | Mobile | เบอร์โทรศัพท์ |  |  |  |  | KPS_R_SHOP_CONT_PER | CONT_PHONE_NO | VARCHAR2 | 30 | Y | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 8 | E-mail | อีเมล |  |  |  |  | KPS_R_SHOP_CONT_PER | CONT_EMAIL_ADDR | VARCHAR2 | 50 | Y | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 9 | Job Title | ตำแหน่ง |  |  |  |  | KPS_R_SHOP_CONT_PER | CONT_POST | VARCHAR2 | 50 | Y | Ready |  |  |  | - เจ้าของ - หุ้นส่วน |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Passengers Complaint |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 10 | Contact Person | ข้อมูลผู้ติดต่อ | CONT_NAME | VARCHAR2 | 50.0 | N | KPS_CAC_INSPECTION_INFORM_SEND | CONT_NAME | VARCHAR2 | 50 | N | Ready |  |  | No | วรนุช สุขสันติภาพ Senior Officer - Price Control | ข้อมูล ชื่อ - นามสกุล และตำแหน่งของผู้ติดต่อ | Confirmed |  |  |  |  |  |  |  |  |
| 11 | Mobile | เบอร์โทรศัพท์ |  |  |  |  |  |  |  |  |  | Ready |  |  | Yes | 081-234-5678 |  | Confirmed |  |  |  |  |  |  |  |  |
| 12 | E-mail | อีเมล | CONT_EMAIL | VARCHAR2 | 200.0 | Y | KPS_CAC_INSPECTION_INFORM_SEND | CONT_EMAIL | VARCHAR2 | 200 | Y | Ready |  |  | Yes | woranuch_s@kingpower.com |  | Confirmed |  |  |  |  |  |  |  |  |
| 13 | Record Date | วันที่บันทึกข้อมูล |  |  |  |  | KPS_CAC_INSPECTION_INFORM_SEND | CREATEDDATE | TIMESTAMP(6) | 11 | Y | Ready |  |  | Yes | 2025-12-18 00:00:00 |  | Confirmed |  |  |  |  |  |  |  |  |
| 14 | ผู้ติดตาม Text File |  |  |  |  |  | KPS_R_EMAIL_TENANT (ACTIVE = '1') | EMAIL | VARCHAR2 | 100 | N | Ready |  |  |  | Wipavan.Sangjeed@th.mcd.com |  |  |  |  |  |  |  |  |  |  |
| 15 | ผู้ติดตามยอดขายวัน |  |  |  |  |  | KPS_R_EMAIL_TENANT (CONFFLAG = '1' ) | EMAIL | VARCHAR2 | 100 | N | Ready |  |  |  | rungthip.roithosai@th.mcd.com |  |  |  |  |  |  |  |  |  |  |
| 16 | ฝ่ายบัญชีของผู้ประกอบการ |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  | rungthip.roithosai@th.mcd.com |  |  |  |  |  |  |  |  |  |  |

---

## 09_Case

| No. | SFDC Field Name (EN) | SFDC Field Name (TH) | Unnamed: 3 | Unnamed: 4 | Unnamed: 5 | Unnamed: 6 | KP Table | KP Field Name | KP Field Type | KP Field Length | VULLABLE (N=Required) | Progress | Confirm | Type | Required | Sample Data | Source Field API Name | Description | Status | User/KP Feedback | Help Text | Track History | External ID | Encrypted | Page Layout | Length |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Information |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 1 | Concession | สัมปทาน |  |  |  |  |  |  |  |  |  | Ready |  |  | Yes | 09 : SVB 05 : DMK (Inter) 10 : DMK (DOM) 08 : HKT |  |  | Confirmed |  |  |  |  |  |  |  |
| 2 | Company Name | ชื่อบริษัท |  |  |  |  |  |  |  |  |  | Ready |  |  | Yes | After You Public Company Limited |  |  | Confirmed |  |  |  |  |  |  |  |
| 3 | Shop Name | ชื่อร้านค้า |  |  |  |  |  |  |  |  |  | Ready |  |  | Yes | After You |  |  | Confirmed |  |  |  |  |  |  |  |
| 4 | Branch Code & Unit No. | เลขสาขาของร้านค้า และเลขที่ยูนิต |  |  |  |  |  |  |  |  |  | Ready |  |  | Yes | 001 - T1ME2-24 |  |  | Confirmed |  |  |  |  |  |  |  |
| 5 | Level | ชั้น |  |  |  |  |  |  |  |  |  | Ready |  |  | Yes | 2 |  |  | Confirmed |  |  |  |  |  |  |  |
| 6 | Location | สถานที่ตั้งของร้าน |  |  |  |  |  |  |  |  |  | Ready |  |  | Yes | Terminal , Conocurse A (แสดงข้อมูลตามแต่ละ Location ของร้านค้า) |  |  | Confirmed |  |  |  |  |  |  |  |
| 7 | Warning Date | วันที่แจ้งเตือน |  |  |  |  |  |  |  |  |  | Ready |  |  | Yes | 2025-06-05 00:00:00 |  |  | Confirmed |  |  |  |  |  |  |  |
| 8 | Warning Subject | หัวข้อการแจ้งเตือน |  |  |  |  |  |  |  |  |  | Ready |  |  | Yes | - ทำผิดข้อกำหนดด้านราคา - ทำผิดข้อกำหนดด้านสุขาภิบาล - ทำผิดข้อกำหนดด้านข้อร้องเรียน |  |  | Confirmed |  |  |  |  |  |  |  |
| 9 | Warning Topic | เรื่องที่แจ้งเตือน |  |  |  |  |  |  |  |  |  | Ready |  |  | Yes | แจ้งผลการตรวจสุขาภิบาลร้านอาหารภายในอาคารผู้โดยสาร ท่าอากาศยานสุวรรณภูมิ |  |  | Confirmed |  |  |  |  |  |  |  |
| 10 | Warning Detail | รายละเอียดการแจ้งเตือน |  |  |  |  |  |  |  |  |  | Ready |  |  | Yes | 1. พบการปนเปื้อนเชื้อ Coliforms และ Escherichia coli ในน้ำแข็งสำหรับบริโภคเกินเกณฑ์ที่กำหนด 2. พบการปนเปื้อนเชื้อ Coliforms ในอาหารเกินเกณฑ์ที่กำหนด |  |  | Confirmed |  |  |  |  |  |  |  |
| 11 | Cause of Problem | การวิเคราะห์สาเหตุของปัญหา |  |  |  |  |  |  |  |  |  | Ready |  |  | Yes | การจัดเก็บน้ำแข็งและอาหารไม่สะอาด |  |  | Confirmed |  |  |  |  |  |  |  |
| 12 | Problem Resolution | แนวทางการแก้ไขในระยะสั้นและระยะยาว |  |  |  |  |  |  |  |  |  | Ready |  |  | Yes | แจ้งเตือนเป็นลายลักษณ์อักษรผ่านอีเมล |  |  | Confirmed |  |  |  |  |  |  |  |
| 13 | Resolution Status | สถานะการแก้ไข |  |  |  |  |  |  |  |  |  | Ready |  |  | Yes | - อยู่ระหว่างดำเนินการ - แก้ไขแล้วเสร็จ |  |  | Confirmed |  |  |  |  |  |  |  |
| 14 | Completion Date | วันที่ที่แก้ไขแล้วเสร็จ |  |  |  |  |  |  |  |  |  | Ready |  |  | Yes | 2025-06-05 00:00:00 |  |  | Confirmed |  |  |  |  |  |  |  |
| 15 | Owner | ผู้ดำเนินการ |  |  |  |  |  |  |  |  |  | Ready |  |  | Yes | CAC |  |  | Confirmed |  |  |  |  |  |  |  |
| 16 | Remarks | หมายเหตุ |  |  |  |  |  |  |  |  |  | Ready |  |  | No | ร้านค้าปิดให้บริการในวันที่ 31/12/2025 |  |  | Confirmed |  |  |  |  |  |  |  |

---

## 10_Reference Products

| No. | SFDC Field Name (EN) | SFDC Field Name (TH) | Unnamed: 3 | Unnamed: 4 | Unnamed: 5 | Unnamed: 6 | KP Table | KP Field Name | KP Field Type | KP Field Length | VULLABLE (N=Required) | Progress | Confirm | Type | Required | Sample Data | Description | Status | User/KP Feedback | Remark | Help Text | Track History | External ID | Track History.1 | Encrypted | Page Layout | Length | Source Field API Name |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Header |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 1 | Reference Product Source | แหล่งที่มาของสินค้าอ้างอิง |  |  |  |  | KPS_R_PROD_REF_SRC | REF_SRC_NAME | VARCHAR2 | 150 | N | Ready |  |  | Yes | - Reference จาก Mall/Hotel - Under bundle/set | ประเภทของ reference product เช่น  ** “Under bundle/set” หมายถึง ข้อมูลที่เกิดจากการกรอกในกรณีที่ user เพิ่ม เพื่อใส่ใน set bundle หรือรายการที่ไม่ขายหน้าร้าน | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 2 | Product Type | ประเภทของสินค้า |  |  |  |  | KPS_T_REQPROD_MD_ORG KPS_R_CATEGORY | STD_CATE_CODE  STD_CATE_DESC  Note: STD_CATE_CODE  เลขตำแหน่ง 0 เป็น PROD_CATE_CODE | VARCHAR2 VARCHAR2 | 4 200 | N N | Ready |  |  | No | 2 - Services 3 - Retails 5 - Food & Beverages | ปัจจุบันฝ่าย CAC ใช้แค่เลข 2, 3 และ 5 เท่านั้น | Confirmed |  | ขอให้สามารถกรอกได้ภายหลัง |  |  |  |  |  |  |  |  |
| 3 | Product Category Code | รหัสประเภทสินค้า |  |  |  |  | KPS_T_REQPROD_MD_ORG | STD_CATE_CODE  Note: STD_CATE_CODE = PROD_CATE_CODE + PROD_SUBCAT1_CODE + PROD_SUBCAT2_CODE (รวม 4 ตัวอักษร) | VARCHAR2 | 4 | N | Ready |  |  | No | 5ACC |  | Confirmed |  | 1. ร้าน Starbucks มี Product Category Code ไม่เหมือนร้านค้าอื่นบางประเภท (โปรดดูชีท Product Cat_ Starbucks) 2. ขอให้สามารถกรอกได้ภายหลัง |  |  |  |  |  |  |  |  |
| 4 | Product Sub Type | ประเภทย่อยของสินค้า |  |  |  |  | KPS_T_REQPROD_MD_ORG KPS_R_PROD_SUBCATE1 | STD_CATE_CODE  PROD_SUBCAT1_DESC  Note: STD_CATE_CODE  เลขตำแหน่ง 1 เป็น PROD_SUBCAT1_CODE | VARCHAR2 VARCHAR2 | 4 200 | N Y | Ready |  |  | No | Thai Food |  | Confirmed |  | ขอให้สามารถกรอกได้ภายหลัง |  |  |  |  |  |  |  |  |
| 5 | Product Category Name - EN | ชื่อหมวดหมู่สินค้าภาษาอังกฤษ |  |  |  |  | KPS_T_REQPROD_MD_ORG KPS_R_PROD_SUBCATE2 | STD_CATE_CODE  PROD_SUBCAT2_DESC_EN   Note: STD_CATE_CODE  เลขตำแหน่ง 2-3  เป็น PROD_SUBCAT2_CODE | VARCHAR2 VARCHAR2 | 4 200 | N Y | Ready |  |  | No | Noodle - Fried |  | Confirmed |  | ขอให้สามารถกรอกได้ภายหลัง |  |  |  |  |  |  |  |  |
| 6 | Product Category Name - TH | ชื่อหมวดหมู่สินค้าภาษาไทย |  |  |  |  | KPS_R_PROD_SUBCATE2 | PROD_SUBCAT2_DESC | VARCHAR2 | 200 | Y | Ready |  |  | No | ก๋วยเตี๋ยวผัด |  | Confirmed |  | ขอให้สามารถกรอกได้ภายหลัง |  |  |  |  |  |  |  |  |
| 7 | Product Status | สถานะของสินค้า |  |  |  |  | KPS_R_PROD_SUBCATE2 | STATUS | NUMBER | 1,0 | Y | Ready |  |  | Yes | - Active - Inactive |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 8 | Attachment/Reference | ไฟล์รูปภาพเมนูสินค้าและข้อมูลอ้างอิง |  |  |  |  |  |  |  |  |  | Ready |  |  | No | - Menu and Price |  | Confirmed |  | ขอให้สามารถเพิ่มได้ภายหลัง |  |  |  |  |  |  |  |  |
| Source of Product - Leading Department Store |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 9 | Product Name - TH | ชื่อสินค้าภาษาไทย |  |  |  |  |  |  |  |  |  | Ready |  |  | No | ผัดไทยกุ้งสด | ถ้ามีชื่อสินค้าภาษาไทย ไม่ต้องมีชื่อสินค้าภาษาอังกฤษก็ได้ | Confirmed |  | ขอให้สามารถกรอกได้ภายหลัง |  |  |  |  |  |  |  |  |
| 10 | Product Name - EN | ชื่อสินค้าภาษาอังกฤษ |  |  |  |  | KPS_T_REQPROD_MD_ORG | PROD_SERV_NAME | VARCHAR2 | 200 | N | Ready |  |  | No | Pad Thai Rice Noodle & Shrimp | ถ้ามีชื่อสินค้าภาษาอังกฤษ ไม่ต้องมีชื่อสินค้าภาษาไทยก็ได้ | Confirmed |  | ขอให้สามารถกรอกได้ภายหลัง |  |  |  |  |  |  |  |  |
| 11 | Reference Source | ชื่อร้านค้าและห้างสรรพสินค้าที่ใช้อ้างอิง |  |  |  |  | KPS_T_REQPROD_MD_ORG KPS_T_REQPROD_MD_ORG   KPS_T_REQPROD_MD_ORG | CON_CODE SHOP_CODE เอา 2 ค่าบนไปหาค่า SHORT_NAME ใน KPS_R_SHOP  REF_SOURCE | CHAR VARCHAR2   VARCHAR2 | 2 20   100 | N N   Y | Ready |  |  | Yes | Coffee Beans by Dao - Siam Paragon |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 12 | Sale Price (Exclude VAT) | ราคาขายไม่รวมภาษีมูลค่าเพิ่ม |  |  |  |  | KPS_T_APPRV_M | KPS_PRICE_EXC_VAT | NUMBER | 16,2 | Y | Ready |  |  | Yes | 261.682243 | กรณีระบุ Sell Price (Exclude VAT) ให้ระบบคำนวณ Sell Price (Include VAT) อัตโนมัติ | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 13 | VAT | ภาษีมูลค่าเพิ่ม |  |  |  |  | KPS_T_REQPROD_MD_ORG | VAT_RATE | NUMBER | 22 | N | Ready |  |  | No |  | คำนวนโดยใช้  | Cancelled |  |  |  |  |  |  |  |  |  |  |
| 14 | Sale Price (Include VAT) | ราคาขายรวมภาษีมูลค่าเพิ่ม |  |  |  |  | KPS_T_APPRV_M | KPS_PRICE_INC_VAT | NUMBER | 16,2 | Y | Ready |  |  | Yes | 280 | กรณีระบุ Sell Price (Include VAT) ให้ระบบคำนวณ Sell Price (Exclude VAT) อัตโนมัติ | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 15 | Survey Date | วันที่สำรวจราคา |  |  |  |  |  |  |  |  |  | Ready |  |  | Yes | 2025-12-18 00:00:00 |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 16 | Reference Date for Approved Product | วันที่อนุมัติราคาสินค้าในระบบ |  |  |  |  |  |  |  |  |  | Ready |  |  | Yes | 2025-12-20 00:00:00 | กรณีมีการพิมพ์ Reference Source เองในหน้าทำงาน ขอให้ระบบจัดเก็บข้อมูลใน Reference Product หลังจาก VP อนุมัติใบงานการขออนุมัติรายการสินค้า | Confirmed |  |  |  |  |  |  |  |  |  |  |
| Source of Product - Hotel |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 16 | Product Name - TH | ชื่อสินค้าภาษาไทย |  |  |  |  |  |  |  |  |  | Ready |  |  | No |  | ถ้ามีชื่อสินค้าภาษาไทย ไม่ต้องมีชื่อสินค้าภาษาอังกฤษก็ได้ | Confirmed |  | ขอให้สามารถกรอกได้ภายหลัง |  |  |  |  |  |  |  |  |
| 17 | Product Name - EN | ชื่อสินค้าภาษาอังกฤษ |  |  |  |  |  |  |  |  |  | Ready |  |  | No | Pad Thai Prawn | ถ้ามีชื่อสินค้าภาษาอังกฤษ ไม่ต้องมีชื่อสินค้าภาษาไทยก็ได้ | Confirmed |  | ขอให้สามารถกรอกได้ภายหลัง |  |  |  |  |  |  |  |  |
| 18 | Reference Source | ชื่อร้านค้าและโรงแรมที่ใช้อ้างอิง |  |  |  |  |  |  |  |  |  | Ready |  |  | Yes | Lakorn European Brasserie - The Rosewood Hotel Bangkok |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 19 | Sale Price (Exclude VAT) | ราคาขายไม่รวมภาษีมูลค่าเพิ่ม |  |  |  |  |  |  |  |  |  | Ready |  |  | Yes | 550 | กรณีระบุ Sell Price (Exclude VAT) ให้ระบบคำนวณ Sell Price (Include VAT) อัตโนมัติ | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 20 | VAT |  |  |  |  |  |  |  |  |  |  | Ready |  |  | No |  |  | Cancelled |  |  |  |  |  |  |  |  |  |  |
| 21 | Sale Price (Include VAT) | ราคาขายรวมภาษีมูลค่าเพิ่ม |  |  |  |  |  |  |  |  |  | Ready |  |  | Yes | 588.5 | กรณีระบุ Sell Price (Include VAT) ให้ระบบคำนวณ Sell Price (Exclude VAT) อัตโนมัติ | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 22 | Survey Date | วันที่สำรวจราคา |  |  |  |  |  |  |  |  |  | Ready |  |  | Yes | 2025-12-18 00:00:00 |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 23 | Reference Date for Approved Product | วันที่อนุมัติราคาสินค้าในระบบ |  |  |  |  |  |  |  |  |  | Ready |  |  | Yes | 2025-12-20 00:00:00 | กรณีมีการพิมพ์ Reference Source เองในหน้าทำงาน ขอให้ระบบจัดเก็บข้อมูลใน Reference Product หลังจาก VP อนุมัติใบงานการขออนุมัติรายการสินค้า | Confirmed |  |  |  |  |  |  |  |  |  |  |

---

## 11_Product Category

| No. | SFDC Field Name (EN) | SFDC Field Name (TH) | KP Table | KP Field Name | KP Field Type | KP Field Length | VULLABLE (N=Required) | Progress | Confirm | Type | Required | Sample Data | Description | Status | User/KP Feedback | Remark | Help Text | Track History | External ID | Track History.1 | Encrypted | Page Layout | Length | Source Field API Name |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Product  Category  Code |  |  |  |  |  |  |  |  |  |  | 5B01 |  |  |  |  |  |  |  |  |  |  |  |  |
| 2 | ประเภท |  |  |  |  |  |  |  |  |  |  | Food & Beverages |  |  |  |  |  |  |  |  |  |  |  |  |
| 3 | Product Category |  |  |  |  |  |  |  |  |  |  | Italian Food |  |  |  |  |  |  |  |  |  |  |  |  |
| 4 | Product Category |  |  |  |  |  |  |  |  |  |  | Prepared Food |  |  |  |  |  |  |  |  |  |  |  |  |
| 5 | ความหมาย |  |  |  |  |  |  |  |  |  |  | อาหารอิตาเลี่ยนสำเร็จรูป |  |  |  |  |  |  |  |  |  |  |  |  |

---

## 12_Product & Price

| No. | SFDC Field Name (EN) | SFDC Field Name (TH) | Source Field API Name | Source Field Type | Source Field Length | VULLABLE (N=Required) | KP Table | KP Field Name | KP Field Type | KP Field Length | VULLABLE (N=Required).1 | Progress | Confirm | Type | Required | Sample Data | Source Field API Name.1 | Description | Status | User/KP Feedback | Help Text | Track History | External ID | Encrypted | Page Layout | SFDC Table | SFDC API Name | SFDC Type |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Product & Price |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 1 | Concession | สัมปทาน | CON_CODE | CHAR | 2.0 |  | KPS_T_APPRV_M KPS_R_CONCESS | CON_CODE CON_LNAME | CHAR | 2 | N | Ready |  |  | Yes | 09 : SVB 05 : DMK (Inter) 10 : DMK (Dom) 08 : HKT |  |  | Confirmed |  |  |  |  |  |  | Product2 | TMS_Concession__c | Lookup(Concession)	 |
| 2 | Company Code & Company Name | รหัสบริษัท และชื่อบริษัท | SHOP_CODE | VARCHAR2 | 20.0 | N | KPS_T_APPRV_M KPS_R_SHOP | SHOP_CODE SHOP_NAME_E | VARCHAR2 VARCHAR2 | 20 200 | N Y | Ready |  |  | Yes | 0901075 APT FOODS CO., LTD.  |  |  | Confirmed |  |  |  |  |  |  | Product2 | TMS_Company_Name__c | Lookup(Account) |
| 3 | Shop Brand Code & Shop Name | รหัสร้านค้า และชื่อร้านค้า | SHPBND_CODE | VARCHAR2 | 4.0 | Y | KPS_T_APPRV_M KPS_R_BRAND | SHPBND_CODE SHPBND_NAME_E | VARCHAR2 VARCHAR2 | 4 60 | N N | Ready |  |  | Yes | 0001 - Burger King |  |  | Confirmed |  |  |  |  |  |  | Product2 | TMS_Shop_Name__c | Lookup(Shop Brand) |
| 4 | Bar Code |  | KPS_T_REQPROD_MD.BARCODE | VARCHAR2 | 30.0 | Y | KPS_T_REQPROD_MD | BARCODE | VARCHAR2 | 30 | Y | Ready |  |  | No | 12345678 |  |  | Confirmed |  |  |  |  |  |  | Product2 | TMS_Bar_Code__c | Text(100) |
| 5 | Unit Code | หน่วยนับสินค้า | UNIT_CODE | VARCHAR2 | 10.0 | Y | KPS_T_APPRV_M KPS_R_UNIT | UNIT_CODE UNIT_DESC | VARCHAR2 VARCHAR2 | 10 50 | N Y | Ready |  |  | Yes | 0012 - Each |  |  | Confirmed |  |  |  |  |  |  | Product2 | TMS_Unit__c | Picklist |
| 6 | Start Date | วันที่ผู้ประกอบการต้องการเริ่มจำหน่ายสินค้า | KPS_EFF_SDATE | VARCHAR2 | 19.0 | Y | KPS_T_APPRV_M | KPS_EFF_SDATE | VARCHAR2 | 19 | Y | Ready |  |  | Yes | 09/12/2025 00:00:00 |  |  | Confirmed |  |  |  |  |  |  | Product2 | TMS_Start_Date__c | Date/Time |
| 7 | End Date | วันที่สิ้นสุดสัญญา | KPS_EFF_EDATE | VARCHAR2 | 19.0 | Y | KPS_T_APPRV_M | KPS_EFF_EDATE | VARCHAR2 | 19 | Y | Ready |  |  | Yes | 31/03/2028 23:59:59 |  |  | Confirmed |  |  |  |  |  |  | Product2 | TMS_End_Date__c | Date/Time |
| 8 | Document No. / Ticket No. | เลขที่เอกสาร | KPS_REASON | VARCHAR2 | 200.0 | Y | KPS_T_APPRV_M | KPS_REASON | VARCHAR2 | 200 | Y | Ready |  |  | Yes | KPS/TEN 1058/2568  |  |  | Confirmed |  |  |  |  |  |  | Product2 | TMS_Document_No_Ticket_No__c | Text(100) |
| 9 | Created Date | วันที่ส่งใบงานขออนุมัติราคาสินค้ามายังฝ่าย CAC | CREATEDDATE | DATE | 7.0 | Y | KPS_T_REQPROD_MD | REQUEST_DATE | CHAR | 10 | N | Ready |  |  | Yes | 2025-12-04 00:00:00 |  |  | Confirmed |  |  |  |  |  |  | Previous | CreatedDate | Date/Time |
| Tenant Product comparison (KPS_T_REQPROD_MD) |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 10 | Product Category Code | รหัสหมวดหมู่สินค้า | STD_CATE_CODE | VARCHAR2 | 4.0 | Y | KPS_T_REQPROD_MD | STD_CATE_CODE | VARCHAR2 | 4 | N | Ready |  |  | Yes | 5NKA |  |  | Confirmed |  |  |  |  |  |  | Previous | TMS_Product_Category_Code__c | Text(100) |
| 11 | Product Code | รหัสสินค้า | PROD_SERV_CODE | VARCHAR2 | 100.0 | N | KPS_T_REQPROD_MD | PROD_SERV_CODE | VARCHAR2 | 100 | N | Ready |  |  | Yes | BK 660000227 |  |  | Confirmed |  |  |  |  |  |  | Previous | ProductCode | Text(255) |
| 12 | Product Name - EN | ชื่อสินค้าภาษาอังกฤษ | PROD_SERV_NAME | VARCHAR2 | 200.0 | Y | KPS_T_REQPROD_MD | PROD_SERV_NAME | VARCHAR2 | 200 | N | Ready |  |  | Yes | Nestle Pure Life Water (Pet) |  |  | Confirmed |  |  |  |  |  |  | Previous | Name | Text(255) |
| 13 | Product Name - TH | ชื่อสินค้าภาษาไทย | <New> |  |  |  |  |  |  |  |  | New |  |  | No | น้ำดื่มเนสท์เล่ เพียวไลฟ์  |  |  | Confirmed |  |  |  |  |  |  | Previous | TMS_Product_Name_TH__c | Text(255) |
| 14 | Product Weight (g. / ml. / oz.) | น้ำหนัก / ปริมาตรสินค้า (กรัม / มิลลิลิตร / ออนซ์) | <New> |  |  |  |  |  |  |  |  | New |  |  | No | 600 ml. |  |  |  |  |  |  |  |  |  | Previous | TMS_Product_Weight__c | Number(16, 2) |
| 15 | Transaction Type | ประเภทสินค้าที่ขออนุม้ติ | TRANS_TYPE | NUMBER | 22.0 | Y | KPS_T_REQPROD_MD | TRANS_TYPE | NUMBER | 22 | N | Ready |  |  | Yes | New, Update, Cancel |  |  | Confirmed |  |  |  |  |  |  | Previous | TMS_Product_Type__c | Picklist |
| 16 | Sale Price (Exclude VAT) | ราคาขายไม่รวมภาษีมูลค่าเพิ่ม | KPS_PRICE_EXC_VAT | NUMBER | 22.0 | Y | KPS_T_REQPROD_MD | KPS_PRICE_EXC_VAT | NUMBER | 22 | Y | Ready |  |  | Yes | 9.35 |  | 1. ขอให้มีจุดทศนิยม 2 ตำแหน่ง 2. สำหรับสินค้าที่ขออนุมัติใหม่ และสินค้าที่เกิดจากการกระทำผิดข้อกำหนดด้านราคาและต้องการยกเลิก | Confirmed |  |  |  |  |  |  | Previous | TMS_Price_EXC_VAT__c | Number(16, 2) |
| 17 | Sale Price (Include VAT) | ราคาขายรวมภาษีมูลค่าเพิ่ม | KPS_PRICE_INC_VAT | NUMBER | 22.0 | Y | KPS_T_REQPROD_MD | KPS_PRICE_INC_VAT | NUMBER | 22 | Y | Ready |  |  | Yes | 10 |  | 1. ขอให้มีจุดทศนิยม 2 ตำแหน่ง 2. สำหรับสินค้าที่ขออนุมัติใหม่ และสินค้าที่เกิดจากการกระทำผิดข้อกำหนดด้านราคา (ขายสินค้าก่อนได้รับการอนุมัติ) และต้องการยกเลิก | Confirmed |  |  |  |  |  |  | Previous | TMS_Price_INC_VAT__c | Number(16, 2) |
| 18 | Previous Sale Price (Exclude VAT) | ราคาขายเดิมไม่รวมภาษีมูลค่าเพิ่ม | <New> |  |  |  |  |  |  |  |  | New |  |  | Yes | 8.411214953 |  | 1. ขอให้มีจุดทศนิยม 2 ตำแหน่ง 2. สำหรับสินค้าที่ขออนุมัติปรับราคา และสินค้าที่มีในระบบ แต่ผู้ประกอบการต้องการยกเลิกจำหน่าย | Confirmed |  |  |  |  |  |  |  |  |  |
| 19 | Previous Sale Price (Include VAT) | ราคาขายเดิมรวมภาษีมูลค่าเพิ่ม | <New> |  |  |  |  |  |  |  |  | New |  |  | Yes | 9 |  | 1. ขอให้มีจุดทศนิยม 2 ตำแหน่ง 2. สำหรับสินค้าที่ขออนุมัติปรับราคา และสินค้าที่มีในระบบ แต่ผู้ประกอบการต้องการยกเลิกจำหน่าย | Confirmed |  |  |  |  |  |  |  |  |  |
| 20 | Reference Source | ชื่อร้านค้า - สถานที่ที่ใช้อ้างอิง | KPS_T_REQPROD_MD.REF_SOURCE | VARCHAR2 | 100.0 | Y | KPS_T_REQPROD_MD | REF_SOURCE | VARCHAR2 | 100 | Y | Ready |  |  | Yes | Burger King - Siam Paragon  |  |  | Confirmed |  |  |  |  |  |  |  |  |  |
| 21 | Reference Price (Exclude VAT) | ราคาอ้างอิงไม่รวมภาษีมูลค่าเพิ่ม | KPS_T_REQPROD_MD.REQ_PRICE_EXC_VAT | NUMBER | 22.0 | N |  |  |  |  |  | Ready |  |  | Yes | 18.69 |  | ขอให้มีจุดทศนิยม 2 ตำแหน่ง | Confirmed |  |  |  |  |  |  |  |  |  |
| 22 | Reference Price (Include VAT) | ราคาอ้างอิงรวมภาษีมูลค่าเพิ่ม | KPS_T_REQPROD_MD.REQ_PRICE_INC_VAT | NUMBER | 22.0 | N | KPS_T_REQPROD_MD | REF_PRICE | NUMBER | 22 | Y | Ready |  |  | Yes | 19.9983 |  | ขอให้มีจุดทศนิยม 2 ตำแหน่ง | Confirmed |  |  |  |  |  |  |  |  |  |
| 23 | % Different | ส่วนต่างราคาสินค้า (Sale Price (Include VAT) - Reference Price (Include VAT)) / Reference Price (Include VAT) x 100 | KPS_T_PROD_COMPARE.REF_PRICE_EXC_DIFF | NUMBER | 22.0 | Y |  |  |  |  |  | Ready |  |  | Yes | -49.99574964 |  | ไม่เกิน 20.00% | Confirmed |  |  |  |  |  |  |  |  |  |
| 24 | Remarks | หมายเหตุ | <New> |  |  |  |  |  |  |  |  | New |  |  | No | เทียบกับ Bottle of Water  |  |  | Confirmed |  |  |  |  |  |  |  |  |  |
| 25 | Request No. | เลขที่เอกสารขออนุมัติราคาสินค้า | KPS_REASON | VARCHAR2 | 200.0 | Y | KPS_T_REQPROD_MD | KPS_REASON | VARCHAR2 | 200 | Y | Ready |  |  | Yes | 111-2568 |  |  | Confirmed |  |  |  |  |  |  |  |  |  |
| Internal Product comparison (KPS_T_PROD_COMPARE) |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 26 | Product Category Code | รหัสหมวดหมู่สินค้า |  |  |  |  | KPS_T_REQPROD_MD | STD_CATE_CODE | VARCHAR2 | 4 | N | Ready |  |  | Yes | 5NKA |  |  | Confirmed |  |  |  |  |  |  |  |  |  |
| 27 | Product Code | รหัสสินค้า |  |  |  |  | KPS_T_PROD_COMPARE | PROD_SERV_CODE | VARCHAR2 | 100 | N | Ready |  |  | Yes | BK 660000227 |  |  | Confirmed |  |  |  |  |  |  |  |  |  |
| 28 | Product Name - EN | ชื่อสินค้าภาษาอังกฤษ |  |  |  |  | KPS_T_PROD_COMPARE | PROD_SERV_NAME | VARCHAR2 | 200 | Y | Ready |  |  | Yes | Nestle Pure Life Water (Pet) |  |  | Confirmed |  |  |  |  |  |  |  |  |  |
| 29 | Product Name - TH | ชื่อสินค้าภาษาไทย |  |  |  |  |  |  |  |  |  | Ready |  |  | No | น้ำดื่มเนสท์เล่ เพียวไลฟ์ |  |  | Confirmed |  |  |  |  |  |  |  |  |  |
| 30 | Sub Product Name - EN / TH | ชื่อสินค้าย่อยใน Combo ภาษาอังกฤษ / ภาษาไทย |  |  |  |  |  |  |  |  |  | Ready |  |  | Yes |  |  |  | Confirmed |  |  |  |  |  |  |  |  |  |
| 31 | Product Weight (g. / ml. / oz.) | น้ำหนัก / ปริมาตรสินค้า / ขนาด (กรัม / มิลลิลิตร / ออนซ์ / S, M, L, XL) |  |  |  |  |  |  |  |  |  | Ready |  |  | No | 600 ml. |  |  |  |  |  |  |  |  |  |  |  |  |
| 32 | Transaction Type | ประเภทสินค้า |  |  |  |  | KPS_T_PROD_COMPARE | TRANS_TYPE | NUMBER | 22 | Y | Ready |  |  | Yes | New, Update, Cancel |  |  | Confirmed |  |  |  |  |  |  |  |  |  |
| 33 | Sale Price (Exclude VAT) | ราคาขายรวมภาษีมูลค่าเพิ่ม |  |  |  |  | KPS_T_PROD_COMPARE | REQ_PRICE_EXC_VAT | NUMBER | 22 | Y | Ready |  |  | Yes | 9.35 |  | 1. ขอให้มีจุดทศนิยม 2 ตำแหน่ง 2. สำหรับสินค้าที่ขออนุมัติใหม่ และสินค้าที่เกิดจากการกระทำผิดข้อกำหนดด้านราคาและต้องการยกเลิก | Confirmed |  |  |  |  |  |  |  |  |  |
| 34 | Sale Price (Include VAT) | ราคาขายรวมภาษีมูลค่าเพิ่ม |  |  |  |  | KPS_T_PROD_COMPARE | REQ_PRICE_INC_VAT | NUMBER | 22 | Y | Ready |  |  | Yes | 10 |  | 1. ขอให้มีจุดทศนิยม 2 ตำแหน่ง 2. สำหรับสินค้าที่ขออนุมัติใหม่ และสินค้าที่เกิดจากการกระทำผิดข้อกำหนดด้านราคา (ขายสินค้าก่อนได้รับการอนุมัติ) และต้องการยกเลิก | Confirmed |  |  |  |  |  |  |  |  |  |
| 35 | Previous Sale Price (Exclude VAT) | ราคาขายเดิมรวมภาษีมูลค่าเพิ่ม |  |  |  |  | KPS_T_PROD_COMPARE | OLD_PRICE_EXC_VAT | NUMBER | 22 | Y | Ready |  |  | Yes | 8.411214953 |  | 1. ขอให้มีจุดทศนิยม 2 ตำแหน่ง 2. สำหรับสินค้าที่ขออนุมัติปรับราคา และสินค้าที่มีในระบบ แต่ผู้ประกอบการต้องการยกเลิกจำหน่าย | Confirmed |  |  |  |  |  |  |  |  |  |
| 36 | Previous Sale Price (Include VAT) | ราคาขายเดิมรวมภาษีมูลค่าเพิ่ม |  |  |  |  | KPS_T_PROD_COMPARE | OLD_PRICE_INC_VAT | NUMBER | 22 | Y | Ready |  |  | Yes | 9 |  | 1. ขอให้มีจุดทศนิยม 2 ตำแหน่ง 2. สำหรับสินค้าที่ขออนุมัติปรับราคา และสินค้าที่มีในระบบ แต่ผู้ประกอบการต้องการยกเลิกจำหน่าย | Confirmed |  |  |  |  |  |  |  |  |  |
| 37 | Reference Source | ชื่อร้านค้า - สถานที่ที่ใช้อ้างอิง |  |  |  |  | KPS_T_PROD_COMPARE | REF_SHOP | VARCHAR2 | 100 | Y | Ready |  |  | Yes | Burger King - Siam Paragon  |  |  | Confirmed |  |  |  |  |  |  |  |  |  |
| 38 | Reference Price (Exclude VAT) | ราคาอ้างอิงรวมภาษีมูลค่าเพิ่ม |  |  |  |  | KPS_T_PROD_COMPARE | REF_PRICE_EXC_VAT | NUMBER | 22 | Y | Ready |  |  | Yes | 18.69 |  | ขอให้มีจุดทศนิยม 2 ตำแหน่ง | Confirmed |  |  |  |  |  |  |  |  |  |
| 39 | Reference Price (Include VAT) | ราคาอ้างอิงรวมภาษีมูลค่าเพิ่ม |  |  |  |  | KPS_T_PROD_COMPARE | REF_PRICE_INC_VAT | NUMBER | 22 | Y | Ready |  |  | Yes | 19.9983 |  | ขอให้มีจุดทศนิยม 2 ตำแหน่ง | Confirmed |  |  |  |  |  |  |  |  |  |
| 40 | % Different | ส่วนต่างราคาสินค้า (Sale Price (Include VAT) - Reference Price (Include VAT)) / Reference Price (Include VAT) x 100 |  |  |  |  | KPS_T_PROD_COMPARE | REF_PRICE_EXC_DIFF | NUMBER | 22 | Y | Ready |  |  | Yes | 11.11111111 |  | ไม่เกิน 20.00% | Confirmed |  |  |  |  |  |  |  |  |  |
| 41 | Remarks | หมายเหตุ |  |  |  |  | KPS_T_PROD_COMPARE | REMARKS | VARCHAR2 | 200 | Y | Ready |  |  | No | เทียบกับ Bottle of Water  |  |  | Confirmed |  |  |  |  |  |  |  |  |  |
| 42 | Approved Date | วันที่อนุมัติราคาสินค้า |  |  |  |  | KPS_T_APPRV_M | KPS_APPROVE_DATE | CHAR | 10 | Y | Ready |  |  | Yes | 2025-12-08 00:00:00 |  |  | Confirmed |  |  |  |  |  |  |  |  |  |
| 43 | Start Date | วันที่ผู้ประกอบการต้องการเริ่มจำหน่ายสินค้า |  |  |  |  | KPS_T_PROD_COMPARE | START_DATE | CHAR | 10 | Y | Ready |  |  | Yes | 09/12/2025 00:00:00 |  |  | Confirmed |  |  |  |  |  |  |  |  |  |
| 44 | End Date | วันที่สิ้นสุดสัญญา |  |  |  |  | KPS_T_APPRV_M | KPS_EFF_EDATE | VARCHAR2 | 19 | Y | Ready |  |  | Yes | 31/03/2028 23:59:59 |  |  | Confirmed |  |  |  |  |  |  |  |  |  |
| 45 | Document No. / Ticket No. | เลขที่เอกสาร |  |  |  |  | KPS_T_APPRV_M | KPS_REASON | VARCHAR2 | 200 | Y | Ready |  |  | Yes | KPS/TEN 1058/2568  |  |  | Confirmed |  |  |  |  |  |  |  |  |  |
| 46 | Owner | ผู้รับผิดชอบ |  |  |  |  | KPS_T_PROD_COMPARE | CREATEDBY | VARCHAR2 | 30 | Y | Ready |  |  | Yes | Woranuch |  |  |  |  |  |  |  |  |  |  |  |  |

---

## 11_Product Cat_ Starbucks

| Product Category Code : Starbucks Coffee | Unnamed: 1 | Unnamed: 2 | Unnamed: 3 | Unnamed: 4 | Unnamed: 5 |
| --- | --- | --- | --- | --- | --- |
| No. | Product  Category  Code | ประเภท | Product Category |  | ความหมาย |
| 1 | 5B01 | Food & Beverages | Italian Food | Prepared Food | อาหารอิตาเลี่ยนสำเร็จรูป |
| 2 | 5FFA | Food & Beverages | Fast Food | Snack | ขนมบรรจุซอง, หมากฝรั่ง, ลูกอม |
| 3 | 5K01 | Food & Beverages | Bakery | Bakery | เบเกอรี่ |
| 4 | 5N01 | Food & Beverages | Beverage | Tea | ชา |
| 5 | 5N02 | Food & Beverages | Beverage | Coffee  | กาแฟ |
| 6 | 5N03 | Food & Beverages | Beverage | Milk, Chocolate | นม, ช็อกโกแลต |
| 7 | 5NMA | Food & Beverages | Beverage | Beverage - Toppings | ท็อปปิ้ง |
| 8 | 5N04 | Food & Beverages | Beverage | Blended Beverage | เครื่องดื่มปั่น (กาแฟปั่น, ชาปั่น, นมปั่น) |
| 9 | 5N05 | Food & Beverages | Beverage | Bottle, Can Beverage | เครื่องดื่มบรรจุขวด,กระป๋อง |
| 10 | 3906 | Retails | Other Retails | Restaurant  Accessories | เครื่องชงกาแฟ, เมล็ดกาแฟคั่ว, กาแฟสำเร็จรูป, แก้วกาแฟ, กระเป๋า, ของที่ละรึก, บัตรสตาร์บัคส์ |

---

## 13_Shop Inspection

| No. | SFDC Field Name (EN) | SFDC Field Name (TH) | Source Field API Name | Source Field Type | Source Field Length | VULLABLE (N=Required) | KP Table | KP Field Name | KP Field Type | KP Field Length | VULLABLE (N=Required).1 | Progress | Confirm | Type | Required | Sample Data | Source Field API Name.1 | Description | Status | User/KP Feedback | Help Text | Track History | External ID | Encrypted | Page Layout |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Information |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 1 | Year | ปี | PERIOD | NUMBER | 22.0 | N | KPS_CAC_INSPECTION_DOCUMENT | INS_YEAR | CHAR | 4 | Y | Ready |  |  | Yes | 2025 |  |  | Confirmed |  |  |  |  |  |  |
| 2 | Period | เดือนที่ตรวจ | S_MONTH_CODE | CHAR | 2.0 | N | KPS_CAC_INSPECTION_DOCUMENT KPS_CAC_INSPECTION_PERIOD DB_TABLE_ATTRIBUTE | PERIOD PERIOD KEY_VALUE | NUMBER NUMBER VARCHAR2 | 2 2 30 | Y N N | Ready |  |  | Yes | November - December |  |  | Confirmed |  |  |  |  |  |  |
| 3 | Concession | สัมปทาน |  |  |  |  | KPS_CAC_INSPECTION_DOCUMENT KPS_R_CONCESS | CON_CODE CON_LNAME | CHAR VARCHAR2 | 2 100 | N Y | Ready |  |  | Yes | 09 : SVB |  |  | Confirmed |  |  |  |  |  |  |
| 4 | Company Code & Company Name | รหัสบริษัท และชื่อบริษัท |  |  |  |  | KPS_CAC_INSPECTION_DOCUMENT KPS_R_SHOP | SHOP_CODE SHOP_NAME_E | VARCHAR2 VARCHAR2 | 20 200 | Y Y | Ready |  |  | Yes | 0901049 - After You Public Company Limited |  |  | Confirmed |  |  |  |  |  |  |
| 5 | Shop Brand Code & Shop Name | รหัสร้านค้า และชื่อร้านค้า |  |  |  |  | KPS_CAC_INSPECTION_DOCUMENT KPS_R_SHOP_BRAND |  SHPBND_NAME_E | VARCHAR2 VARCHAR2 | 20 60 | Y Y | Ready |  |  | Yes | 0002 - After You |  |  | Confirmed |  |  |  |  |  |  |
| 6 | Branch Code & Unit No. | เลขสาขาของร้านค้า และเลขที่ยูนิต |  |  |  |  | KPS_CAC_INSPECTION_DOCUMENT KPS_CAC_INSPECTION_DOCUMENT | BRANCH_CODE SHOP_UNIT | VARCHAR2 VARCHAR2 | 20 15 | Y Y | Ready |  |  | Yes | 001 - T1ME2-24 |  |  | Confirmed |  |  |  |  |  |  |
| 7 | Level | ชั้น |  |  |  |  | KPS_CAC_INSPECTION_DOCUMENT KPS_CAC_INSPECTION_DOCUMENT KPS_R_SHOPUNIT KPS_R_LEVEL | CON_CODE SHOP_UNIT LEVEL_CODE LEVEL_DESC | CHAR VARCHAR2 VARCHAR2 VARCHAR2 | 2 15 3 30 | N Y Y N | Ready |  |  | Yes | 2 |  |  | Confirmed |  |  |  |  |  |  |
| 8 | Location | สถานที่ตั้งของร้าน |  |  |  |  | KPS_CAC_INSPECTION_DOCUMENT KPS_CAC_INSPECTION_DOCUMENT KPS_R_SHOPUNIT KPS_R_BUILDING  | CON_CODE SHOP_UNIT B_CODE B_DESC | CHAR VARCHAR2 VARCHAR2 VARCHAR2 | 2 15 3 30 | N Y Y Y | Ready |  |  | Yes | Terminal , Concourse A (แสดงข้อมูลตามแต่ละ Location ของร้านค้า) |  |  | Confirmed |  |  |  |  |  |  |
| 9 | Inspection Type | ประเภทการตรวจร้านค้า |  |  |  |  |  |  |  |  |  | Ready |  |  | Yes | การตรวจเมนูหน้าร้านค้า การตรวจร้านค้าเชิงพาณิชย์ การตรวจใบอนุญาต การตรวจสุขภาพพนักงาน |  |  | Confirmed |  |  |  |  |  |  |
| 10 | Shop Category | ประเภทของร้านค้า |  |  |  |  | KPS_CAC_INSPECTION_DOCUMENT DB_TABLE_ATTRIBUTE | FROM_CATE_CODE VALUE_DATA | VARCHAR2 NVARCHAR2 | 10 2000 | Y N | Ready |  |  | Yes | Restaurant |  |  | Confirmed |  |  |  |  |  |  |
| 11 | Institution | ผู้แจ้งปัญหาจากการตรวจ |  |  |  |  | KPS_CAC_INSP_DOC_DETAIL |  |  |  |  | Ready |  |  | Yes | KPS / AOT / ด่านควบคุมโรคติดต่อระหว่างประเทศ ฯลฯ |  |  | Confirmed |  |  |  |  |  |  |
| 12 | Inspector | ผู้เข้าตรวจ |  |  |  |  | KPS_CAC_INSPECTION_DOCUMENT | INS_CODE | VARCHAR2 | 4 | Y | Ready |  |  | Yes | Panisa |  |  | Confirmed |  |  |  |  |  |  |
| 13 | Main Topic | หัวข้อหลัก | KEY_VALUE | VARCHAR2 | 30.0 | N | KPS_CAC_INSP_DOC_DETAIL KPS_CAC_INSPECTION_TOPIC_M DB_TABLE_ATTRIBUTE | TOPIC_CODE KEY_VALUE VALUE_DATA | VARCHAR2 VARCHAR2 NVARCHAR2 | 4 30 2000 | N N N | Ready |  |  | Yes | สถานที่ (F&B) |  |  | Confirmed |  |  |  |  |  |  |
| 14 | Sub Topic | หัวข้อ |  |  |  |  | KPS_CAC_INSP_DOC_DETAIL KPS_CAC_INSP_DOC_DETAIL KPS_CAC_INSPECTION_TOPIC_MD DB_TABLE_ATTRIBUTE | TOPIC_CODE TOPIC_DTL_CODE KEY_VALUE VALUE_DATA | VARCHAR2 NUMBER VARCHAR2 NVARCHAR2 | 4 9 30 2000 | N N N N | Ready |  |  | Yes | สถานที่รับประทานอาหาร : โต๊ะหรือเก้าอี้ ที่จัดไว้สำหรับบริโภคอาหาร สะอาด มีสภาพดี ไม่ชำรุด และมีการทำความสะอาดเป็นประจำ |  |  | Confirmed |  |  |  |  |  |  |
| 15 | Main Reason | ปัญหาหลัก |  |  |  |  |  |  |  |  |  | Ready |  |  | Yes | ความสะอาด |  |  | Confirmed |  |  |  |  |  |  |
| 16 | Sub Reason | ปัญหา |  |  |  |  |  |  |  |  |  | Ready |  |  | Yes | พื้นไม่สะอาด |  |  | Confirmed |  |  |  |  |  |  |
| 17 | Form Template  | แบบตรวจของร้านค้า | FORM_ID | VARCHAR2 | 10.0 | N | KPS_CAC_INSPECTION_DOCUMENT | FORM_ID | VARCHAR2 | 10 | N | Ready |  |  | Yes | Form Template ตามข้อมูล Master Data |  |  | Confirmed |  |  |  |  |  |  |
| 18 | Additional Problem from Government Sectors | ปัญหาการตรวจสุขาภิบาลโดยหน่วยงานราชการ / รัฐวิสาหกิจ |  |  |  |  | KPS_CAC_INSPECTION_PROBLEM | REMARK | VARCHAR2 |  |  | Ready |  |  | Yes | พื้นไม่สะอาด |  |  | Confirmed |  |  |  |  |  |  |
| 19 | Suggestion from Government Sectors | ข้อแนะนำเพิ่มเติมจากหน่วยงานราชการ / รัฐวิสาหกิจ |  |  |  |  | KPS_CAC_INSPECTION_SUGGESTION | REMARK | VARCHAR2 | 2000 | Y | Ready |  |  | Yes | ข้อเสนอแนะจากการตรวจร้านค้า |  |  | Confirmed |  |  |  |  |  |  |
| 20 | Inspection Document  | ข้อมูลรายละเอียดผลตรวจ (ขั้นตอนการบันทึกผล) |  |  |  |  |  |  |  |  |  | Ready |  |  | Yes | แสดงข้อมูลรายละเอียดผลตรวจร้านค้า |  |  | Confirmed |  |  |  |  |  |  |
| 21 | KPS Inspection Checklist | หัวข้อการตรวจ |  |  |  |  |  |  |  |  |  | Ready |  |  | Yes | สถานที่รับประทานอาหาร : โต๊ะหรือเก้าอี้ ที่จัดไว้สำหรับบริโภคอาหาร สะอาด มีสภาพดี ไม่ชำรุด และมีการทำความสะอาดเป็นประจำ |  |  | Confirmed |  |  |  |  |  |  |
| 22 | Result | ผลการตรวจ |  |  |  |  | KPS_CAC_INSP_DOC_DETAIL | WEIGHT_RESULT | NUMBER | (10,2) |  | Ready |  |  | Yes | - Pass - Not Pass  |  | ผลการตรวจแต่ละหัวข้อ | Confirmed |  |  |  |  |  |  |
| 23 | Final Result | สรุปผลการตรวจ |  |  |  |  | KPS_CAC_INSPECTION_DOCUMENT |  |  |  |  | Ready |  |  | Yes | Pass |  | สรุปผลกาตรวจของร้านค้า | Confirmed |  |  |  |  |  |  |
| 24 | Summary Result (%) | สรุปผลการตรวจ (%) |  |  |  |  | KPS_CAC_INSPECTION_DOCUMENT | RESULT | NUMBER | (10,2) |  | Ready |  |  | Yes | 1 |  | แสดง % ผลการตรวจร้านค้า | Confirmed |  |  |  |  |  |  |
| 25 | Problem | ปัญหา |  |  |  |  |  |  |  |  |  | Ready |  |  | No | พื้นไม่สะอาด |  | เลือกจาก Reason | Confirmed |  |  |  |  |  |  |
| 26 | Picture | ภาพปัญหา |  |  |  |  |  |  |  |  |  | Ready |  |  | No | แสดงภาพปัญหาที่พบจากการตรวจร้านค้า |  | CAC แนบภาพปัญหาที่พบจากการตรวจร้านค้า และระบบแสดงภาพ | Confirmed |  |  |  |  |  |  |
| 27 | Suggestion | ข้อเสอนแนะ |  |  |  |  |  |  |  |  |  | Ready |  |  | No | ข้อเสนอแนะจากการตรวจร้านค้า |  |  | Confirmed |  |  |  |  |  |  |
| 28 | Approve Inspection Results | การอนุมัติผลตรวจร้าน |  |  |  |  | KPS_CAC_INSPECTION_DOCUMENT | ISCRITICAL (Critical = 1, Not Critical = null ) | NUMBER | 1 | Y | Ready |  |  | Yes | แสดงข้อมูลสำหรับอนุมัติผลการตรวจ |  | แสดงข้อมูลรายละเอียดผลการตรวจ,ข้อมูล Score (%) ของแต่ละร้านค้า ผลการตรวจร้านค้า (Preview) และเอกสารแนบ (Preview) โดยสามารถเลือกข้อมูลจากผลการตรวจได้  - ALL - Critical - Non Critical | Confirmed |  |  |  |  |  |  |
| 29 | Inspection Approval Status | สถานะการอนุมัติ |  |  |  |  | KPS_CAC_INSPECTION_DOCUMENT | APPROVE_STATUS | NUMBER | 1 |  | Ready |  |  | Yes | Approve |  | แสดงหัวข้อสำหรับการอนุมัติผลตรวจ | Confirmed |  |  |  |  |  |  |
| 30 | Inspection Result (Preview) | ผลการตรวจร้าน (Preview) |  |  |  |  | KPS_CAC_INSPECTION_DOCUMENT KPS_CAC_INSPECTION_DOCUMENT | DOC_NO FORM_ID | VARCHAR2 VARCHAR2 | 10 10 | N N | Ready |  |  | Yes | แสดงข้อมูลรายละเอียดผลตรวจร้านค้า |  |  | Confirmed |  |  |  |  |  |  |
| 31 | Attachment | เอกสารแนบ |  |  |  |  |  |  |  |  |  | Ready |  |  | No | แสดงรายละเอียดของเอกสารแนบ |  | CAC แนบเอกสารที่เกี่ยวข้องกับตรวจร้านค้า Attached, KPS Document, AOT Result และเอกสารอื่นๆ และสามารถเปิดไฟล์เพื่อดูข้อมูลได้ | Confirmed |  |  |  |  |  |  |
| 32 | Contact Person | ข้อมูลผู้ติดต่อ |  |  |  |  | KPS_CAC_INSPECTION_INFORM KPS_CAC_INSPECTION_INFORM_SEND KPS_CAC_INSPECTION_INFORM_SEND | INFORM_NO MAIL_TYPE CONT_NAME | NUMBER VARCHAR2 VARCHAR2 | 22 10 50 | N N Y | Ready |  |  | No | ภาณิศา ชิณเครือ KPS |  | ข้อมูล ชื่อ - นามสกุล และตำแหน่งของผู้ติดต่อ | Confirmed |  |  |  |  |  |  |
| 33 | Recipient Email | ข้อมูล Email สำหรับจัดส่งผลการตรวจร้านค้า (TO) |  |  |  |  | KPS_CAC_INSPECTION_INFORM KPS_CAC_INSPECTION_INFORM_SEND KPS_CAC_INSPECTION_INFORM_SEND | INFORM_NO MAIL_TYPE CONT_EMAIL | NUMBER VARCHAR2 VARCHAR2 | 22 10 200 | N N Y | Ready |  |  | Yes | panisa_ch@kingpower.com |  |  | Confirmed |  |  |  |  |  |  |
| 34 | CC/BCC | ข้อมูล Email สำหรับจัดส่งผลการตรวจร้านค้า (CC/BCC) |  |  |  |  | KPS_CAC_INSPECTION_INFORM KPS_CAC_INSPECTION_INFORM_SEND KPS_CAC_INSPECTION_INFORM_SEND | INFORM_NO MAIL_TYPE CONT_EMAIL | NUMBER VARCHAR2 VARCHAR2 | 22 10 200 | N N Y | Ready |  |  | No | panisa_ch@kingpower.com |  |  | Confirmed |  |  |  |  |  |  |
| 35 | Email Result Sending Status | สถานะการส่ง Email ถึงผู้ประกอบการ |  |  |  |  | KPS_CAC_INSPECTION_DOCUMENT | STATUS_MAIL | NUMBER | 1 |  | Ready |  |  | Yes | Yes/No |  |  | Confirmed |  |  |  |  |  |  |
| 36 | Problem Solving Status | สถานะการแก้ไขของผู้ประกอบการ |  |  |  |  |  |  |  |  |  | Ready |  |  | Yes | ผู้ประกอบการส่งข้อมูลการแก้ไข ในวันที่ 18/12/2025 |  |  | Confirmed |  |  |  |  |  |  |

---

## 14_Form Template(New)

| No. | SFDC Field Name (EN) | SFDC Field Name (TH) | Unnamed: 3 | Unnamed: 4 | Unnamed: 5 | Unnamed: 6 | KP Table | KP Field Name | KP Field Type | KP Field Length | VULLABLE (N=Required) | Progress | Confirm | Type | Required | Sample Data | Source Field API Name | Description | Status | User/KP Feedback | Help Text | Track History | External ID | Encrypted | Page Layout |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Information |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 1 | Template Code | รหัสแบบฟอร์ม |  |  |  |  | KPS_CAC_INSPECTION_TEMPLATE | TEMP_ID | VARCHAR2 | 10 | N | Ready |  |  | Yes |  |  |  | Confirmed |  |  |  |  |  |  |
| 2 | Shop Category | ประเภทของร้านค้า |  |  |  |  |  |  |  |  |  | Ready |  |  | Yes | Restaurant |  |  | Confirmed |  |  |  |  |  |  |
| 3 | Main Topic | หัวข้อหลัก |  |  |  |  | KPS_CAC_INSPECTION_TEMPLATE KPS_CAC_INSPECTION_TOPIC_M DB_TABLE_ATTRIBUTE | TOPIC_CODE KEY_VALUE VALUE_DATA | VARCHAR2 VARCHAR2 NVARCHAR2 | 4 30 2000 | N N Y | Ready |  |  | Yes | สถานที่ (F&B) |  |  | Confirmed |  |  |  |  |  |  |
| 4 | Sub Topic | หัวข้อย่อย |  |  |  |  | KPS_CAC_INSPECTION_TEMPLATE KPS_CAC_INSPECTION_TOPIC_MD DB_TABLE_ATTRIBUTE | TOPIC_DTL_CODE KEY_VALUE VALUE_DATA | NUMBER VARCHAR2 NVARCHAR2  | 22 30 2000 | N N Y | Ready |  |  | Yes | สถานที่รับประทานอาหาร : โต๊ะหรือเก้าอี้ ที่จัดไว้สำหรับบริโภคอาหาร สะอาด มีสภาพดี ไม่ชำรุด และมีการทำความสะอาดเป็นประจำ |  |  | Confirmed |  |  |  |  |  |  |
| 5 | Status | สถานะ |  |  |  |  | KPS_CAC_INSPECTION_TEMPLATE | ACTIVE_FLAG | NUMBER | 22 | Y | Ready |  |  | Yes | - Active  - Inactive |  | สถานะของแบบตรวจ,หัวข้อการตรวจ, ปัญหา | Confirmed |  |  |  |  |  |  |
| 6 | Problem | ปัญหา |  |  |  |  | KPS_CAC_INSP_DOC_DETAIL KPS_CAC_INSP_DOC_DETAIL | COLUMN_ID VALUE_DATA | VARCHAR2 NVARCHAR2 | 10 2000 | N Y | Ready |  |  | No | พื้นไม่สะอาด |  | เลือกจาก Reason | Confirmed |  |  |  |  |  |  |
| 7 | Result | ผลการตรวจ |  |  |  |  | KPS_CAC_INSP_DOC_DETAIL | WEIGHT_RESULT | NUMBER | 1 | Y | Ready |  |  | Yes | - Pass - Not Pass  |  |  | Confirmed |  |  |  |  |  |  |
| 8 | Form Name | ชื่อฟอร์ม |  |  |  |  | KPS_CAC_INSPECTION_FORM DB_TABLE_ATTRIBUTE | KEY_VALUE VALUE_DATA | VARCHAR2 NVARCHAR2  | 30 2000 | Y Y | Ready |  |  | Yes |  |  |  | Confirmed |  |  |  |  |  |  |
| 9 | Final Result | สรุปผลการตรวจ |  |  |  |  |  |  |  |  |  | Ready |  |  | Yes | Pass |  | สรุปผลกาตรวจของร้านค้า | Confirmed |  |  |  |  |  |  |
| 10 | Summary Result (%) | สรุปผลการตรวจ (%) |  |  |  |  |  |  |  |  |  | Ready |  |  | Yes | 1 |  | แสดง % ผลการตรวจร้านค้า | Confirmed |  |  |  |  |  |  |

---

## 15_Location

| No. | SFDC Field Name (EN) | SFDC Field Name (TH) | Source Field API Name | Source Field Type | Source Field Length | VULLABLE (N=Required) | KP Table | KP Field Name | KP Field Type | KP Field Length | VULLABLE (N=Required).1 | Progress | Confirm | Type | Required | Sample Data | Description | Status | User/KP Feedback | Remark | Help Text | Track History | External ID | Track History.1 | Encrypted | Page Layout | Length | Source Field API Name.1 | Source Field Type.1 | Source Field Length.1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Location |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 1 | Site |  |  |  |  |  |  |  |  |  |  | Ready |  | Text | Yes | ท่าอากาศยานสุวรรณภูมิ | สถานที่ | New |  |  |  |  |  |  |  |  |  |  |  |  |
| 2 | Level |  |  |  |  |  |  |  |  |  |  | Ready |  | Text | Yes | Level 4 | ชั้น | New |  |  |  |  |  |  |  |  |  |  |  |  |
| 3 | Building |  |  |  |  |  |  |  |  |  |  | Ready |  | Text | Yes | Concourse | ตึก/อาคาร | New |  |  |  |  |  |  |  |  |  |  |  |  |
| 4 | Wing |  |  |  |  |  |  |  |  |  |  | Ready |  | Text | Yes | DE  | ปีกอาคาร | New |  |  |  |  |  |  |  |  |  |  |  |  |
| 5 | Zone |  |  |  |  |  |  |  |  |  |  | Ready |  | Text | Yes | Junction East | โซน | New |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | LOC_CODE | VARCHAR2 | 3.0 | N | KPS_R_LOCATION | LOC_CODE | VARCHAR2 | 3.0 | N |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | B_CODE | VARCHAR2 | 3.0 | N | KPS_R_BUILDING | B_CODE | VARCHAR2 | 3.0 | N |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | B_DESC | VARCHAR2 | 30.0 | N | KPS_R_BUILDING | B_DESC | VARCHAR2 | 30.0 | N |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | ZONE_CODE | VARCHAR2 | 3.0 | N | KPS_R_ZONE | ZONE_CODE | VARCHAR2 | 3.0 | N |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | ZONE_DESC | VARCHAR2 | 30.0 | N | KPS_R_ZONE | ZONE_DESC | VARCHAR2 | 30.0 | N |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | W_CODE | VARCHAR2 | 3.0 | N | KPS_R_WING | W_CODE | VARCHAR2 | 3.0 | N |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | W_DESC | VARCHAR2 | 30.0 | N | KPS_R_WING | W_DESC | VARCHAR2 | 30.0 | N |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | LEVEL_CODE | VARCHAR2 | 3.0 | N | KPS_R_LEVEL | LEVEL_CODE | VARCHAR2 | 3.0 | N |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | LEVEL_DESC | VARCHAR2 | 30.0 | N | KPS_R_LEVEL | LEVEL_DESC | VARCHAR2 | 30.0 | N |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | AREA_CODE | VARCHAR2 | 3.0 | N | KPS_R_AREA | AREA_CODE | VARCHAR2 | 3.0 | N |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | AREA_NAME | VARCHAR2 | 40.0 | N | KPS_R_AREA | AREA_NAME | VARCHAR2 | 40.0 | N |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |

---

## 16_Floor

| No. | SFDC Field Name (EN) | SFDC Field Name (TH) | Source Field API Name | Source Field Type | Source Field Length | VULLABLE (N=Required) | KP Table | KP Field Name | KP Field Type | KP Field Length | VULLABLE (N=Required).1 | Progress | Confirm | Type | Required | Sample Data | Description | Status | User/KP Feedback | Remark | Help Text | Track History | External ID | Track History.1 | Encrypted | Page Layout | Length | Source Field API Name.1 | Source Field Type.1 | Source Field Length.1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Location |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 1 | Basement |  |  |  |  |  |  |  |  |  |  | Not Ready |  | Text | Yes | B1 | ชั้นใต้ดิน | New |  |  |  |  |  |  |  |  |  |  |  |  |
| 2 | sorting Area |  |  |  |  |  |  |  |  |  |  | Not Ready |  | Text | Yes | Sotting | ชั้นสายพาน | New |  |  |  |  |  |  |  |  |  |  |  |  |
| 3 | Level 1 |  |  |  |  |  |  |  |  |  |  | Not Ready |  | Text | Yes | 1 |  | New |  |  |  |  |  |  |  |  |  |  |  |  |
| 4 | Level 2 |  |  |  |  |  |  |  |  |  |  | Not Ready |  | Text | Yes | 2 |  | New |  |  |  |  |  |  |  |  |  |  |  |  |
| 5 | Level 3 |  |  |  |  |  |  |  |  |  |  | Not Ready |  | Text | Yes | 3 |  | New |  |  |  |  |  |  |  |  |  |  |  |  |
| 6 | Level 3 M | Level 3 Mezzanine |  |  |  |  |  |  |  |  |  | Not Ready |  |  |  | 3M | ชั้นลอย | New |  |  |  |  |  |  |  |  |  |  |  |  |
| 7 | Level 4 |  |  |  |  |  |  |  |  |  |  | Not Ready |  | Text | Yes | 4 |  | New |  |  |  |  |  |  |  |  |  |  |  |  |
| 8 | Level 5 |  |  |  |  |  |  |  |  |  |  | Not Ready |  | Text | Yes | 5 |  | New |  |  |  |  |  |  |  |  |  |  |  |  |
| 9 | Level 6 |  |  |  |  |  |  |  |  |  |  | Not Ready |  | Text | Yes | 6 |  | New |  |  |  |  |  |  |  |  |  |  |  |  |
| 10 | Rooftop |  |  |  |  |  |  |  |  |  |  | Not Ready |  | Text | Yes | Roof | ดาดฟ้า | New |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | LEVEL_CODE | VARCHAR2 | 3.0 | N | KPS_R_LEVEL | LEVEL_CODE | VARCHAR2 | 3.0 | N |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | LEVEL_DESC | VARCHAR2 | 30.0 | N | KPS_R_LEVEL | LEVEL_DESC | VARCHAR2 | 30.0 | N |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | STATUS | NUMBER | 22.0 | Y | KPS_R_LEVEL | STATUS | NUMBER | 22.0 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | USER_NAME | VARCHAR2 | 15.0 | Y | KPS_R_LEVEL | USER_NAME | VARCHAR2 | 15.0 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | DATE_STAMP | VARCHAR2 | 10.0 | Y | KPS_R_LEVEL | DATE_STAMP | VARCHAR2 | 10.0 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | TIME_STAMP | VARCHAR2 | 10.0 | Y | KPS_R_LEVEL | TIME_STAMP | VARCHAR2 | 10.0 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |

---

## 17_Shop Units

| No. | SFDC Field Name (EN) | SFDC Field Name (TH) | Source Field API Name | Source Field Type | Source Field Length | VULLABLE (N=Required) | KP Table | KP Field Name | KP Field Type | KP Field Length | VULLABLE (N=Required).1 | Progress | Confirm | Type | Required | Sample Data | Description | Status | User/KP Feedback | Remark | Help Text | Track History | External ID | Track History.1 | Encrypted | Page Layout | Length | Source Field API Name.1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Information |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 1 | Concession No. |  |  |  |  |  | KPS_R_SHOPUNIT | CON_CODE | CHAR | 2 | N | Ready | Y | Text | Yes | 09 | เลขที่รหัสสัมปทาน | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 2 | KPS Unit No. |  |  |  |  |  | KPS_R_SHOPUNIT | SHOP_UNIT | VARCHAR2 | 15 | N | Ready | Y |  | Yes | T2MTE3-01 | เลขที่ KP กำหนด ขายให้ลูกค้า | Confirmed |  |  |  |  |  |  |  |  |  |  |
|  | AOT Unit No. |  |  |  |  |  | ไม่มีฐานข้อมูลใน TMS |  |  |  |  | Ready | Y |  | Yes | ADD-301-01 | เลขที่ที่ได้จากทอท. และต้องใช้ในการทำหนังสือควบคู่กับเลขที่ KP | New |  |  |  |  |  |  |  |  |  |  |
| 3 | Source Unit No. |  |  |  |  |  | ไม่มีฐานข้อมูลใน TMS |  |  |  |  | Ready | Y |  | No |  |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 4 | Unit Description |  |  |  |  |  | KPS_R_BRANCH | BRANCH_NAME_T | VARCHAR2 | 200 |  | Ready | Y |  |  | รายละเอียดเพิ่มเติม |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 5 | Usage Type |  | USG_CODE | VARCHAR2 | 5.0 | Y | KPS_R_SHOPUNIT KPS_R_SPACE_USAGE | USG_CODE USG_DESC | VARCHAR2 VARCHAR2 | 5 50 |  | Ready | Y |  |  | - Commercial Area - Office Area - Common Area - Advertising |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 6 | Concession Revenue |  |  |  |  |  | KPS_R_SHOPUNIT KPS_R_AOT_RENTAL_TYPE | RNT_CODE RNT_DESC | VARCHAR2 VARCHAR2 | 5 50 | N N  | Ready | Y |  |  | - จำหน่ายอาหารและเครื่องดื่ม - บริการอื่น ๆ - ธุรกิจธนาคาร - จำหน่ายสินค้าและของที่ระลึก - บริกํารเพื่อสุขภาพ - บริการรับจองทัวร์และโรงแรม |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 7 | Unit Category |  |  |  |  |  | KPS_R_SHOPUNIT KPS_R_AOT_RENTAL_CATE KPS_R_AOT_RENTAL_CATE | RNTCAT_CODE RNTCAT_CODE RNTCAT_DESC | CHAR CHAR VARCHAR2 | 5 5 100 | N N N | Ready | Y |  |  | - Retail - Bank - F&B, Other, Health - Restaurant / Dayroom / Reception / Entertainment - Office Room |  | Confirmed |  | - Start Date ต้องไม่มํากกว่ํา End Date - รูปแบบ: DD/MM/YYYY เป็น คริสต์ศักรําช |  |  |  |  |  |  |  |  |
| 8 | Owner |  |  |  |  |  | KPS_R_SHOPUNIT | OWNER_CODE | VARCHAR2 | 30 |  | Ready | Y |  |  | - KPS - KPI - KPD |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 9 | Unit Sub-Category |  |  |  |  |  | KPS_R_SHOPUNIT | SHOP_CATE_AND_SUB_CATE | CHAR | 4 |  | Ready | Y |  |  |  |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 10 | Inter/Domestic |  |  |  |  |  | KPS_R_SHOPUNIT | FLAG_INT_DMS (INTERNATIONAL,DOMESTIC,NONCLASSIFIED) | VARCHAR2 | 30 |  | Ready | Y | Picklist |  | - International - Domestic - Non-Classified |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 11 | Departure/Arrival |  |  |  |  |  | KPS_R_SHOPUNIT | FLAG_DPR_ARR (DEPARTURE,ARRIVAL,TRANSIT,NONCLASSIFIED) | VARCHAR2 | 30 |  | Ready | Y | Picklist |  | - Departure - Arrival - Transit - Non-Classified |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 12 | Start Date |  |  |  |  |  | KPS_R_SHOPUNIT | START_DATE | DATE | 7 |  | Ready | Y | Date |  | 28/09/2020 |  | Confirmed |  | รูปแบบ: DD/MM/YYYY เป็น คริสต์ศักราช |  |  |  |  |  |  |  |  |
| 13 | End Date |  |  |  |  |  | KPS_R_SHOPUNIT | END_DATE | DATE | 7 |  | Ready | Y | Date |  | 28/09/2020 |  | Confirmed |  | รูปแบบ: DD/MM/YYYY เป็น คริสต์ศักราช |  |  |  |  |  |  |  |  |
| 14 | Reason |  |  |  |  |  | KPS_R_SHOPUNIT | END_REASON | VARCHAR2 | 200 |  | Ready | Y |  |  |  | หมายเหตุ ของการปิดพื้นที่ | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 15 | Rental Type |  |  |  |  |  | KPS_R_SHOPUNIT KPS_R_AOT_RENTAL_TYPE | RNT_CODE RNT_DESC | VARCHAR2 VARCHAR2 | 5 50 |  | Ready | Y |  |  | - จำหน่ายอาหารและเครื่องดื่ม - บริการอื่น ๆ - ธุรกิจธนาคาร - จำหน่ายสินค้าและของที่ระลึก - บริการเพื่อสุขภาพ - บริการรับจองทัวร์และโรงแรม | ประเภทการเช่า | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 16 | Rental Rate |  |  |  |  |  | ไม่มี TMS KPS_R_AOT_RENTAL_RATE | RNTCAT_RATE | NUMBER | 22 | N | Ready | Y |  |  |  | เรทค่าเช่า | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 17 | Middle Rate |  |  |  |  |  | ไม่มีใน TMS |  |  |  |  | Ready | Y |  |  |  | เรทราคากลาง | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 18 | Unit Grade |  |  |  |  |  | ไม่มีใน TMS |  |  |  |  | Ready | Y |  |  | - A - B - C - D | ระดับพื้นที่ | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 19 | Unit Status |  |  |  |  |  | KPS_R_SHOPUNIT | STATUS | NUMBER | 22 | N | Ready | Y |  |  |  | สถานะ Unit | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 20 | Last Modified - Action |  |  |  |  |  | KPS_T_SRC_UNIT | ถ้าเจอ SHOPUNIT เดียวกันบน Table นี้ |  |  |  | Ready |  |  |  | - Merge - Split - Sway | ปรับปรุงล่าสุดด้วยวิธีการ | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 21 | Last Modified By |  |  |  |  |  | KPS_R_SHOPUNIT | UPDATEDBY | VARCHAR2 | 30 |  | Ready | Y |  |  |  | ปรับปรุงล่าสุดโดย | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 22 | การแนบไฟล์ |  | <New> |  |  |  |  |  |  |  |  | New | Y |  |  | เอกสารรังวัดพื้นที่จาก AOT |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| Actual Area |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 23 | Total Area |  |  |  |  |  | KPS_R_SHOPUNIT | ACT_TOT_AREA | NUMBER | 22 |  | Ready | Y | Number(1,3) | Yes | 5.000 |  | Confirmed |  | " |  |  |  |  |  |  |  |  |
| 24 | Commercial Area |  |  |  |  |  | KPS_R_SHOPUNIT | ACT_COMM_AREA | NUMBER | 22 |  | Ready | Y | Number(1,3) | Yes | 5.000 |  | Confirmed |  | " |  |  |  |  |  |  |  |  |
| 25 | M&E Area |  |  |  |  |  | KPS_R_SHOPUNIT | ACT_ME_AREA | NUMBER | 22 |  | Ready | Y | Number(1,3) | Yes | 0.000 |  | Confirmed |  | " |  |  |  |  |  |  |  |  |
| 26 | Store Area |  |  |  |  |  | KPS_R_SHOPUNIT | ACT_STORE_AREA | NUMBER | 22 |  | Ready | Y | Number(1,3) | Yes | 0.000 |  | Confirmed |  | " |  |  |  |  |  |  |  |  |
| 27 | Other Area |  |  |  |  |  | ไม่มีใน TMS |  |  |  |  | Ready | Y | Number(1,3) | Yes | 0.000 |  | Confirmed |  | " |  |  |  |  |  |  |  |  |
| Unit Location |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 28 | Site |  |  |  |  |  | KPS_R_CONCESS | LOCATION | VARCHAR2 | 60 | N | Ready | Y |  | Yes | ท่าอากาศยานสุวรรณภูมิ | สถานที่ | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 29 | Level |  | LEVEL_CODE | VARCHAR2 | 3.0 | Y | KPS_R_SHOPUNIT | LEVEL_CODE | VARCHAR2 | 3 |  | Ready | Y |  | Yes | Level 4 | ชั้น | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 30 | Building |  | B_CODE | VARCHAR2 | 3.0 | Y | KPS_R_SHOPUNIT | B_CODE | VARCHAR2 | 3 |  | Ready | Y |  | Yes |  | ตึก/อาคาร | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 31 | Wing |  | W_CODE | VARCHAR2 | 3.0 | Y | KPS_R_SHOPUNIT | W_CODE | VARCHAR2 | 3 |  | Ready | Y |  | Yes |  | ปีกอาคาร | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 32 | Zone |  | ZONE_CODE | VARCHAR2 | 3.0 | Y | KPS_R_SHOPUNIT | ZONE_CODE | VARCHAR2 | 3 |  | Ready | Y |  | Yes |  | โซน | Confirmed |  |  |  |  |  |  |  |  |  |  |
| ข้อมูลการเช่าพื้นที่ |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 33 | ลำดับ |  |  |  |  |  | ไม่มีใน TMS (Running ASC) |  |  |  |  | Ready | Y |  | No |  | เลขลำดับที่ | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 34 | Tenant |  |  |  |  |  | KPS_T_CONT_SHOP_UNIT | SHOP_CODE | VARCHAR2 | 20 | N | Ready | Y |  | No |  | รหัสผู้ประกอบการ | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 35 | Tenant Name |  |  |  |  |  | KPS_R_SHOP | REGISTERED_NAME | VARCHAR2 |  |  | Ready | Y |  | No |  | ชื่อผู้ประกอบการ | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 36 | Shop |  |  |  |  |  | KPS_T_CONT_SHOP_UNIT | BRANCH_CODE | VARCHAR2 | 20 | N | Ready | Y |  | No |  | รหัส Shop | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 37 | Shop Name |  |  |  |  |  | KPS_R_BRANCH | BRANCH_NAME_T | VARCHAR2 | 200 |  | Ready | Y |  | No |  | ชื่อ Shop | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 38 | วันที่ส่งมอบพื้นที่ |  |  |  |  |  | KPS_T_CONTRACT | CONT_DATE |  |  |  | Ready | Y |  | No | 28/09/2020 |  | Confirmed |  | รูปแบบ: DD/MM/YYYY เป็น คริสต์ศักราช |  |  |  |  |  |  |  |  |
| 39 | วันที่เปิดร้าน |  |  |  |  |  | KPS_T_CONT_SHOP_UNIT | SHOP_STR_DATE | DATE | 7 | Y | Ready | Y |  | No | 28/09/2020 |  | Confirmed |  | รูปแบบ: DD/MM/YYYY เป็น คริสต์ศักราช |  |  |  |  |  |  |  |  |
| 40 | Contract No. |  |  |  |  |  | KPS_T_CONTRACT | CONT_NO | VARCHAR2 | 30 | N | Ready | Y |  | No |  | เลขที่สัญญา | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 41 | Contract Start Date |  |  |  |  |  | KPS_T_CONTRACT | CONT_STR_DATE | DATE | 7 | N | Ready | Y |  | No |  | วันที่สัญญาเริ่มต้น | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 42 | Contract End Date |  |  |  |  |  | KPS_T_CONTRACT | CONT_END_DATE | DATE | 7 | N | Ready | Y |  | No |  | วันที่สิ้นสุดสัญญา | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 43 | Total Area |  |  |  |  |  | KPS_R_BRANCH | AREA | NUMBER | 22 | Y | Ready | Y | Number(1,3) | Yes | 5.000 |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 44 | Commercial Area |  |  |  |  |  | KPS_R_BRANCH | COMM_AREA | NUMBER | 22 | Y | Ready | Y | Number(1,3) | Yes | 5.000 |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 45 | M&E Area |  |  |  |  |  | KPS_R_BRANCH | STORE_AREA | NUMBER | 22 | Y | Ready | Y | Number(1,3) | Yes | 0.000 |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 46 | Store Area |  |  |  |  |  | KPS_R_BRANCH | MNE_AREA | NUMBER | 22 | Y | Ready | Y | 3 | Yes | 0.000 |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 47 | Other Area |  |  |  |  |  | KPS_R_BRANCH | OTH_AREA | NUMBER | 22 | Y | Ready | Y | Number(1,3) | Yes | 0.000 |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| การปรับปรุง Unit |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 48 | ลำดับ |  |  |  |  |  | ไม่มีใน TMS (Running ASC) |  |  |  |  | Ready | Y |  |  |  | เลขลำดับที่ | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 49 | Action |  |  |  |  |  | Hardcode "Merge" |  |  |  |  | Ready | Y |  |  | - Merge - Swap - Split - Unit No. - วันที่เริ่มต้น - etc. |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 50 | Source Value |  |  |  |  |  | KPS_T_CONTRACT | CONT_AREA | NUMBER | 22 | Y | Ready | Y |  |  |  | ค่า ก่อนแก้ไข | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 51 | New Value |  |  |  |  |  | KPS_T_CONTRACT_REVISE | CONT_AREA | NUMBER | 22 | Y | Ready | Y |  |  |  | ค่าใหม่หลังแก้ไข | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 52 | Updated Date |  |  |  |  |  | KPS_T_CONTRACT_REVISE | REVISE_DATE | DATE |  |  | Ready |  |  |  | 28/09/2020 |  | Confirmed |  | รูปแบบ: DD/MM/YYYY เป็น คริสต์ศักราช |  |  |  |  |  |  |  |  |
| 53 | Updated By |  |  |  |  |  | KPS_T_CONTRACT_REVISE | UPDATEDBY | VARCHAR2 | 30 |  | Ready |  |  |  |  | ชื่อผู้ใช้ที่ update ข้อมูล | Confirmed |  |  |  |  |  |  |  |  |  |  |

---

## 18_Technical Provisions

| No. | SFDC Field Name (EN) | SFDC Field Name (TH) | Type | Required | Sample Data | Description | Status | User/KP Feedback | Remark | Help Text | Track History | External ID | Track History.1 | Encrypted | Page Layout | Length | Source Field API Name | Source Field Type | Source Field Length |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Location |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 1 | Doc.No. |  | Text | Yes |  | เลขที่เอกสาร | New |  |  |  |  |  |  |  |  |  |  |  |  |
| 2 | Unit No. |  | Text | Yes |  | หมายเลข Unit | New |  |  |  |  |  |  |  |  |  |  |  |  |
| 3 | Shop Name |  | Text | Yes |  | ชื่อร้าน | New |  |  |  |  |  |  |  |  |  |  |  |  |
| 4 | Tenant Name |  | Text | Yes |  | บริษัทผู้เช่าคู่สัญญา | New |  |  |  |  |  |  |  |  |  |  |  |  |
| 5 | Occupant |  | Text | Yes | KPS/KPD/KPDC | เจ้าของพื้นที่ | New |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Activity |  | Text | Yes | F&B | ประเภทพื้นที่ | New |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Floor |  | Text | Yes | 4 | ชั้น | New |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Building |  | Text | Yes | Concourse/Main Terminal | อาคาร | New |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Location |  | Text | Yes | DE, Domestic | พื้นที่อาคาร | New |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Airport |  | Text | Yes | สุวรรณภูมิ | สนามบิน | New |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Commercial Area (m2) |  | Text | Yes |  | พื้นที่ขาย | New |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Storage Area (m2) |  | Text | Yes |  | พื้นที่สโตร์ | New |  |  |  |  |  |  |  |  |  |  |  |  |
|  | M&E Area (m2) |  | Text | Yes |  | พื้นที่ห้องเครื่อง | New |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Total Area (m2) |  | Text | Yes |  | อื่นๆ | New |  |  |  |  |  |  |  |  |  |  |  |  |
|  | EE-Connect by |  | Text | Yes | AOT(1:1) /KP (1:M) | การเชื่อมต่อไฟ | New |  |  |  |  |  |  |  |  |  |  |  |  |
|  | EE-Power(Phase)/Main Breaker(AT) |  | Text | Yes | 3P/80AT | ขนาดเบรคเกอร์ | New |  |  |  |  |  |  |  |  |  |  |  |  |
|  | EE-Wire & Conduit |  | Text | Yes | 4x16 / 6 G.  IEC01. in Ø 1 1/2" IMC | ขนาดสายและท่อ | New |  |  |  |  |  |  |  |  |  |  |  |  |
|  | EE-Power Source |  | Text | Yes | SS5-4A-2DPM-A1 (NEW) in  LWC L2-A1/A2/8 | ตู้ที่เชื่อมต่อ | New |  |  |  |  |  |  |  |  |  |  |  |  |
|  | AC-Brand |  | Text | Yes | TARNE | ยี่ห้อแอร์ | New |  |  |  |  |  |  |  |  |  |  |  |  |
|  | AC-Model |  | Text | Yes | BDHA204RA1 | รุ่นของแอร์ | New |  |  |  |  |  |  |  |  |  |  |  |  |
|  | AC-Air Flow Rate (CFM) |  | Text | Yes | 1600 | แรงลม | New |  |  |  |  |  |  |  |  |  |  |  |  |
|  | AC-Capacity (BTU) |  | Text | Yes | 54000 | ขนาด | New |  |  |  |  |  |  |  |  |  |  |  |  |
|  | AC-Chilled Water Supply(inch) |  | Text | Yes | 1.1/4" | ขนาดท่อน้ำเย็นเข้า | New |  |  |  |  |  |  |  |  |  |  |  |  |
|  | AC-Chilled Water Return(inch) |  | Text | Yes | 1.1/4" | ขนาดท่อน้ำเย็นออก | New |  |  |  |  |  |  |  |  |  |  |  |  |
|  | AC-Drain Pipe(inch) |  | Text | Yes | 1.1/4" | ขนาดท่อน้ำทิ้งแอร์ | New |  |  |  |  |  |  |  |  |  |  |  |  |
|  | AC-Radiant Floor Cooling |  | Text | Yes | No. | ท่อแอร์แบบฝังพื้น | New |  |  |  |  |  |  |  |  |  |  |  |  |
|  | SN-Cold Water-Connect by |  | Text | Yes | By AOT | ประเภทการเชื่อมต่อน้ำประปา | New |  |  |  |  |  |  |  |  |  |  |  |  |
|  | SN-Cold Water-Main Pipe (inch) |  | Text | Yes | 1" | ขนาดท่อเมนประปา | New |  |  |  |  |  |  |  |  |  |  |  |  |
|  | SN-Cold Water-Meter (inch) |  | Text | Yes | 1" | ขนาดมิเตอร์น้ำ | New |  |  |  |  |  |  |  |  |  |  |  |  |
|  | SN-Waste Water-Drain Pipe (inch) |  | Text | Yes | 3" | ขนาดท่อน้ำทิ้งภายในร้าน | New |  |  |  |  |  |  |  |  |  |  |  |  |
|  | SN-Waste Water-Grease Trap (Set) |  | Text | Yes | By Tenant | ถังดักไขมัน | New |  |  |  |  |  |  |  |  |  |  |  |  |
|  | SN-Waste Water-Gravity (Yes/No.) |  | Text | Yes | Gravity | การต่อท่อน้ำทิ้งตรง(ไม่มีปั๊มน้ำ) | New |  |  |  |  |  |  |  |  |  |  |  |  |
|  | SN-Waste Water-Plumbing (Set) |  | Text | Yes | - | ปั๊มน้ำ | New |  |  |  |  |  |  |  |  |  |  |  |  |
|  | VN-Kitchen Exhaust Air Flow Rate (CFM) |  | Text | Yes | 1300 | แรงลมสำหรับ Hood ดูดควัน | New |  |  |  |  |  |  |  |  |  |  |  |  |
|  | VN-Electrostatic Precipitation (EP) |  | Text | Yes | Follow Tenant design | เครื่องขจัดละอองน้ำมัน | New |  |  |  |  |  |  |  |  |  |  |  |  |
|  | VN-Fire Suppression |  | Text | Yes | Must by Tenant | ระบบดับเพลิงใน Hood ดูดควัน | New |  |  |  |  |  |  |  |  |  |  |  |  |
|  | VN-KMA Flow |  | Text | Yes | 1000 | แรงลมระบบเติมอากาศดีของ Hood ดูดควัน | New |  |  |  |  |  |  |  |  |  |  |  |  |
|  | VN-Fresh Air (CFM) |  | Text | Yes | 150 | ระบบเติมอากาศดี | New |  |  |  |  |  |  |  |  |  |  |  |  |
|  | FP-Main Wet Pipe(inch) |  | Text | Yes | 21/2" | ท่อเมนระบบดับเพลิง | New |  |  |  |  |  |  |  |  |  |  |  |  |
|  | FP-Sprinkler head (Set) |  | Text | Yes | By Tenant | หัวฉีดน้ำดับเพลิงอัตโนมัติ | New |  |  |  |  |  |  |  |  |  |  |  |  |
|  | FP-Main Dry Pipe (Inch) |  | Text | Yes |  | ระบบเมนท่อแห้งของระบบดับเพลิง | New |  |  |  |  |  |  |  |  |  |  |  |  |
|  | FP-Deluge Valve(Set) |  | Text | Yes |  | ระบบดับเพลิงชนิด Deluge Valve | New |  |  |  |  |  |  |  |  |  |  |  |  |
|  | FP-Fire Extinguisher(Set) |  | Text | Yes |  | ถังดับเพลิง | New |  |  |  |  |  |  |  |  |  |  |  |  |
|  | FA-Fire Alarm Terminal(FA Box) |  | Text | Yes | 1 | กล่องเชื่อมต่อระบบสัญญาณแจ้งเหตุเพลิงไหม้ | New |  |  |  |  |  |  |  |  |  |  |  |  |
|  | FA-Smoke Detector(Set) |  | Text | Yes | 4 | อุปกรณ์ตรวจจับควัน | New |  |  |  |  |  |  |  |  |  |  |  |  |
|  | FA-Heat Detector(Set) |  | Text | Yes |  | อุปกรณ์ตรวจจับความร้อน | New |  |  |  |  |  |  |  |  |  |  |  |  |
|  | FA-Monitor Module(Set) |  | Text | Yes |  | อุปกรณ์ส่งสัญญาณระบบแจ้งเหตุเพลิงไหม้ | New |  |  |  |  |  |  |  |  |  |  |  |  |
|  | FA-Control Module(Set) |  | Text | Yes |  | อุปกรณ์ควบคุมระบบแจ้งเหตุเพลิงไหม้ | New |  |  |  |  |  |  |  |  |  |  |  |  |
|  | ICT-POS/COM/IP Phone(Point) |  | Text | Yes | 3 | จุดเชื่อมต่อระบบ POS,คอมพิวเตอร์,โทรศัพท์ | New |  |  |  |  |  |  |  |  |  |  |  |  |
|  | ICT-CCTV(Point) |  | Text | Yes | 1 | จุดเชื่อมต่อระบบกล้อง CCTV | New |  |  |  |  |  |  |  |  |  |  |  |  |
|  | ICT-CCTV(IP.Address) |  | Text | Yes | 176.12.2.123 | หมายเลข Address ของกล้อง | New |  |  |  |  |  |  |  |  |  |  |  |  |
|  | ICT-Access Point(Point) |  | Text | Yes |  | จุดเชื่อมต่อระบบ Access | New |  |  |  |  |  |  |  |  |  |  |  |  |
|  | ICT-Digital Signage(Point) |  | Text | Yes | 1 | จุดเชื่อมต่อป้าย | New |  |  |  |  |  |  |  |  |  |  |  |  |
|  | ST&AR-Shell&Core |  | Text | Yes | YES | โครงหน้าร้าน | New |  |  |  |  |  |  |  |  |  |  |  |  |
|  | ST&AR-Floor |  | Text | Yes | Terrazzo | พื้น | New |  |  |  |  |  |  |  |  |  |  |  |  |
|  | ST&AR-Wall |  | Text | Yes | Sandwich Panel | ผนัง | New |  |  |  |  |  |  |  |  |  |  |  |  |
|  | ST&AR-Ceiling |  | Text | Yes | Exposed | ฝ้า | New |  |  |  |  |  |  |  |  |  |  |  |  |
|  | EE Suggestion |  | Text | Yes |  |  | New |  |  |  |  |  |  |  |  |  |  |  |  |
|  | AC Suggestion |  | Text | Yes |  |  | New |  |  |  |  |  |  |  |  |  |  |  |  |
|  | SN Suggestion |  | Text | Yes |  |  | New |  |  |  |  |  |  |  |  |  |  |  |  |
|  | VN Suggestion |  | Text | Yes |  |  | New |  |  |  |  |  |  |  |  |  |  |  |  |
|  | FP Suggestion |  | Text | Yes |  |  | New |  |  |  |  |  |  |  |  |  |  |  |  |
|  | FA Suggestion |  | Text | Yes | กรณีที่มีการกั้นแบ่งพื้นที่ ต้องทำการติดตั้ง Smoke/Heat Detector |  | New |  |  |  |  |  |  |  |  |  |  |  |  |
|  | ICT Suggestion |  | Text | Yes |  |  | New |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Shell&Core Suggestion |  | Text | Yes |  |  | New |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Floor Suggestion |  | Text | Yes | Ritta รื้อพื้นเดิมออกส่งมอบให้ ID |  | New |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Wall Suggestion |  | Text | Yes | Ritta กั้นผนังระหว่างร้าน |  | New |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Ceiling Suggestion |  | Text | Yes | ออกแบบฝ้าเป็นลักษณะปิดทึบ ใช้วัสดุไม่ติดลามไฟ |  | New |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Safety Suggestion |  | Text | Yes |  |  | New |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Other Suggestion |  | Text | Yes |  |  | New |  |  |  |  |  |  |  |  |  |  |  |  |

---

## 18_Meter

| TABLE_NAME | COLUMN_ID | COLUMN_NAME | DATA_TYPE | DATA_LENGTH | DATA_PRECISION | DATA_SCALE | NULLABLE
N = Required | DATA_DEFAULT | COMMENT |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| KPS_R_ELECTRIC | 1 | CON_CODE | CHAR | 2 |  |  | N |  |  |
| KPS_R_ELECTRIC | 2 | EMETER_NO | VARCHAR2 | 18 |  |  | N |  |  |
| KPS_R_ELECTRIC | 3 | EMETER_DESC | VARCHAR2 | 60 |  |  | Y |  |  |
| KPS_R_WATER_METER | 1 | METER_CODE | VARCHAR2 | 30 |  |  | N |  |  |
| KPS_R_WATER_METER | 2 | SERIAL_NO | VARCHAR2 | 30 |  |  | Y |  |  |
| KPS_R_WATER_METER | 3 | METER_STATUS | VARCHAR2 | 10 |  |  | Y |  |  |
| KPS_R_WATER_METER | 4 | START_DATE | DATE | 7 |  |  | Y |  |  |
| KPS_R_WATER_METER | 5 | START_METER_NO | NUMBER | 22 | 10.0 | 0.0 | Y |  |  |
| KPS_R_WATER_METER | 6 | END_METER_NO | NUMBER | 22 | 10.0 | 0.0 | Y |  |  |
| KPS_R_WATER_METER | 7 | CREATEDBY | VARCHAR2 | 30 |  |  | Y |  |  |
| KPS_R_WATER_METER | 8 | CREATEDDATE | DATE | 7 |  |  | Y |  |  |
| KPS_R_WATER_METER | 9 | UPDATEDBY | VARCHAR2 | 30 |  |  | Y |  |  |
| KPS_R_WATER_METER | 10 | UPDATEDDATE | DATE | 7 |  |  | Y |  |  |
| KPS_R_WATER_METER | 11 | SIZE_CODE | VARCHAR2 | 30 |  |  | N |  |  |
| KPS_R_WATER_METER | 12 | RU | VARCHAR2 | 30 |  |  | Y |  |  |
| KPS_R_WATER_METER | 13 | REMARK | VARCHAR2 | 200 |  |  | Y |  |  |
| KPS_R_POWER_METER | 1 | METER_CODE | VARCHAR2 | 30 |  |  | N |  | Meter Code |
| KPS_R_POWER_METER | 2 | SERIAL_NO | VARCHAR2 | 30 |  |  | Y |  | Serial No |
| KPS_R_POWER_METER | 3 | METER_STATUS | VARCHAR2 | 10 |  |  | Y |  | Meter Status : ON/OFF |
| KPS_R_POWER_METER | 4 | START_DATE | DATE | 7 |  |  | Y |  |  |
| KPS_R_POWER_METER | 5 | START_METER_NO | NUMBER | 22 | 10.0 | 0.0 | Y |  |  |
| KPS_R_POWER_METER | 6 | END_METER_NO | NUMBER | 22 | 10.0 | 0.0 | Y |  |  |
| KPS_R_POWER_METER | 7 | CREATEDBY | VARCHAR2 | 30 |  |  | Y |  |  |
| KPS_R_POWER_METER | 8 | CREATEDDATE | DATE | 7 |  |  | Y |  |  |
| KPS_R_POWER_METER | 9 | UPDATEDBY | VARCHAR2 | 30 |  |  | Y |  |  |
| KPS_R_POWER_METER | 10 | UPDATEDDATE | DATE | 7 |  |  | Y |  |  |
| KPS_R_POWER_METER | 11 | METER_TYPE | NUMBER | 22 |  |  | Y |  | Meter Type :  1=DIGITAL , 2=ANALOG |
| KPS_R_POWER_METER | 12 | REMARK | VARCHAR2 | 500 |  |  | Y |  | Remark |
| KPS_R_POWER_METER | 13 | VOLTAGE_CODE | VARCHAR2 | 30 |  |  | Y |  | VolTage Code: 1=High VolTage , 2=Low Voltage |
| KPS_R_POWER_METER | 14 | METER_TYPE2 | NUMBER | 22 |  |  | Y |  |  |
| KPS_T_POWER_USAGE | 1 | USAGE_CODE | VARCHAR2 | 30 |  |  | N |  |  |
| KPS_T_POWER_USAGE | 2 | PERIOD_CODE | VARCHAR2 | 10 |  |  | N |  |  |
| KPS_T_POWER_USAGE | 3 | METER_CODE | VARCHAR2 | 30 |  |  | N |  |  |
| KPS_T_POWER_USAGE | 4 | INS_CODE | VARCHAR2 | 30 |  |  | N |  |  |
| KPS_T_POWER_USAGE | 5 | ASOF_DATE | DATE | 7 |  |  | Y |  |  |
| KPS_T_POWER_USAGE | 6 | START_DATE | DATE | 7 |  |  | Y |  |  |
| KPS_T_POWER_USAGE | 7 | END_DATE | DATE | 7 |  |  | Y |  |  |
| KPS_T_POWER_USAGE | 8 | START_METER_NO | NUMBER | 22 | 10.0 | 0.0 | Y |  |  |
| KPS_T_POWER_USAGE | 9 | END_METER_NO | NUMBER | 22 | 10.0 | 0.0 | Y |  |  |
| KPS_T_POWER_USAGE | 10 | IMPORT_FLAG | NUMBER | 22 | 1.0 | 0.0 | Y |  |  |
| KPS_T_POWER_USAGE | 11 | CREATEDDATE | DATE | 7 |  |  | Y |  |  |
| KPS_T_POWER_USAGE | 12 | CREATEDBY | VARCHAR2 | 30 |  |  | Y |  |  |
| KPS_T_POWER_USAGE | 13 | UPDATEDDATE | DATE | 7 |  |  | Y |  |  |
| KPS_T_POWER_USAGE | 14 | UPDATEDBY | VARCHAR2 | 30 |  |  | Y |  |  |
| KPS_T_POWER_USAGE | 15 | BILLING_FLAG | NUMBER | 22 | 1.0 | 0.0 | Y |  |  |
| KPS_T_POWER_USAGE | 16 | AOT_EXPENSE_FLAG | NUMBER | 22 | 1.0 | 0.0 | Y |  |  |
| KPS_T_POWER_USAGE | 17 | POWER_USAGE | NUMBER | 22 |  |  | Y |  |  |
| KPS_T_POWER_USAGE | 18 | END_METER_FLAG | NUMBER | 22 |  |  | Y |  |  |
| KPS_T_POWER_USAGE | 19 | SERIAL_NO | VARCHAR2 | 30 |  |  | Y |  |  |
| KPS_T_POWER_USAGE_SHOPUNIT | 1 | USAGE_CODE | VARCHAR2 | 30 |  |  | N |  |  |
| KPS_T_POWER_USAGE_SHOPUNIT | 2 | PERIOD_CODE | VARCHAR2 | 10 |  |  | N |  |  |
| KPS_T_POWER_USAGE_SHOPUNIT | 3 | METER_CODE | VARCHAR2 | 30 |  |  | N |  |  |
| KPS_T_POWER_USAGE_SHOPUNIT | 4 | INS_CODE | VARCHAR2 | 30 |  |  | N |  |  |
| KPS_T_POWER_USAGE_SHOPUNIT | 5 | INS_SEQ | NUMBER | 22 | 2.0 | 0.0 | N |  |  |
| KPS_T_POWER_USAGE_SHOPUNIT | 6 | SHOP_UNIT | VARCHAR2 | 15 |  |  | Y |  |  |
| KPS_T_POWER_USAGE_SHOPUNIT | 7 | START_METER_NO | NUMBER | 22 | 10.0 | 0.0 | Y |  |  |
| KPS_T_POWER_USAGE_SHOPUNIT | 8 | END_METER_NO | NUMBER | 22 | 10.0 | 0.0 | Y |  |  |
| KPS_T_POWER_USAGE_SHOPUNIT | 9 | POWER_USAGE | NUMBER | 22 | 10.0 | 0.0 | Y |  |  |
| KPS_T_POWER_USAGE_SHOPUNIT | 10 | BILLING_FLAG | NUMBER | 22 | 10.0 | 0.0 | Y |  |  |
| KPS_T_POWER_USAGE_SHOPUNIT | 11 | AOT_EXPENSE_FLAG | NUMBER | 22 | 10.0 | 0.0 | Y |  |  |
| KPS_T_POWER_USAGE_SHOPUNIT | 12 | FTRATE | NUMBER | 22 | 10.0 | 4.0 | Y |  |  |
| KPS_T_POWER_USAGE_SHOPUNIT | 13 | FTCHARGE_AMT | NUMBER | 22 | 10.0 | 2.0 | Y |  |  |
| KPS_T_POWER_USAGE_SHOPUNIT | 14 | TRRATE | NUMBER | 22 | 10.0 | 4.0 | Y |  |  |
| KPS_T_POWER_USAGE_SHOPUNIT | 15 | TRCHARGE_AMT | NUMBER | 22 | 10.0 | 2.0 | Y |  |  |
| KPS_T_POWER_USAGE_SHOPUNIT | 16 | MTRATE | NUMBER | 22 | 10.0 | 4.0 | Y |  |  |
| KPS_T_POWER_USAGE_SHOPUNIT | 17 | MTCHARGE_AMT | NUMBER | 22 | 10.0 | 2.0 | Y |  |  |
| KPS_T_POWER_USAGE_SHOPUNIT | 18 | SERVICE_CHARGE | NUMBER | 22 | 10.0 | 2.0 | Y |  |  |
| KPS_T_POWER_USAGE_SHOPUNIT | 19 | TOTAL_AMT | NUMBER | 22 | 10.0 | 2.0 | Y |  |  |
| KPS_T_POWER_USAGE_SHOPUNIT | 20 | CREATEDBY | VARCHAR2 | 30 |  |  | Y |  |  |
| KPS_T_POWER_USAGE_SHOPUNIT | 21 | CREATEDDATE | DATE | 7 |  |  | Y |  |  |
| KPS_T_POWER_USAGE_SHOPUNIT | 22 | UPDATEDBY | VARCHAR2 | 30 |  |  | Y |  |  |
| KPS_T_POWER_USAGE_SHOPUNIT | 23 | UPDATEDDATE | DATE | 7 |  |  | Y |  |  |
| KPS_T_POWER_USAGE_SHOPUNIT | 24 | START_DATE | DATE | 7 |  |  | Y |  |  |
| KPS_T_POWER_USAGE_SHOPUNIT | 25 | END_DATE | DATE | 7 |  |  | Y |  |  |
| KPS_T_POWER_USAGE_SHOPUNIT | 26 | REMARK | VARCHAR2 | 500 |  |  | Y |  |  |
| KPS_T_POWER_USAGE_SHOPUNIT | 27 | SERIAL_NO | VARCHAR2 | 30 |  |  | Y |  |  |
| KPS_T_POWER_USAGE_SHOPUNIT | 28 | SHOP_NAME | VARCHAR2 | 200 |  |  | Y |  |  |
| KPS_T_POWER_USAGE_SHOPUNIT | 29 | CON_CODE | CHAR | 2 |  |  | Y |  |  |
| KPS_T_WATER_USAGE | 1 | USAGE_CODE | VARCHAR2 | 30 |  |  | N |  |  |
| KPS_T_WATER_USAGE | 2 | PERIOD_CODE | VARCHAR2 | 10 |  |  | N |  |  |
| KPS_T_WATER_USAGE | 3 | METER_CODE | VARCHAR2 | 30 |  |  | Y |  |  |
| KPS_T_WATER_USAGE | 4 | INS_CODE | VARCHAR2 | 30 |  |  | Y |  |  |
| KPS_T_WATER_USAGE | 5 | ASOF_DATE | DATE | 7 |  |  | Y |  |  |
| KPS_T_WATER_USAGE | 6 | START_DATE | DATE | 7 |  |  | Y |  |  |
| KPS_T_WATER_USAGE | 7 | END_DATE | DATE | 7 |  |  | Y |  |  |
| KPS_T_WATER_USAGE | 8 | START_METER_NO | NUMBER | 22 | 10.0 | 0.0 | Y |  |  |
| KPS_T_WATER_USAGE | 9 | END_METER_NO | NUMBER | 22 | 10.0 | 0.0 | Y |  |  |
| KPS_T_WATER_USAGE | 10 | IMPORT_FLAG | NUMBER | 22 | 1.0 | 0.0 | Y |  |  |
| KPS_T_WATER_USAGE | 11 | CREATEDDATE | DATE | 7 |  |  | Y |  |  |
| KPS_T_WATER_USAGE | 12 | CREATEDBY | VARCHAR2 | 30 |  |  | Y |  |  |
| KPS_T_WATER_USAGE | 13 | UPDATEDDATE | DATE | 7 |  |  | Y |  |  |
| KPS_T_WATER_USAGE | 14 | UPDATEDBY | VARCHAR2 | 30 |  |  | Y |  |  |
| KPS_T_WATER_USAGE | 15 | BILLING_FLAG | NUMBER | 22 | 1.0 | 0.0 | Y |  |  |
| KPS_T_WATER_USAGE | 16 | AOT_EXPENSE_FLAG | NUMBER | 22 | 1.0 | 0.0 | Y |  |  |
| KPS_T_WATER_USAGE | 17 | WATER_USAGE | NUMBER | 22 |  |  | Y |  |  |
| KPS_T_WATER_USAGE | 18 | END_METER_FLAG | NUMBER | 22 |  |  | Y |  |  |
| KPS_T_WATER_USAGE_SHOPUNIT | 1 | USAGE_CODE | VARCHAR2 | 30 |  |  | N |  |  |
| KPS_T_WATER_USAGE_SHOPUNIT | 2 | PERIOD_CODE | CHAR | 7 |  |  | N |  |  |
| KPS_T_WATER_USAGE_SHOPUNIT | 3 | METER_CODE | VARCHAR2 | 30 |  |  | Y |  |  |
| KPS_T_WATER_USAGE_SHOPUNIT | 4 | INS_CODE | VARCHAR2 | 30 |  |  | Y |  |  |
| KPS_T_WATER_USAGE_SHOPUNIT | 5 | INS_SEQ | NUMBER | 22 | 2.0 | 0.0 | Y |  |  |
| KPS_T_WATER_USAGE_SHOPUNIT | 6 | SHOP_UNIT | VARCHAR2 | 15 |  |  | N |  |  |
| KPS_T_WATER_USAGE_SHOPUNIT | 7 | START_METER_NO | NUMBER | 22 | 10.0 | 0.0 | Y |  |  |
| KPS_T_WATER_USAGE_SHOPUNIT | 8 | END_METER_NO | NUMBER | 22 | 10.0 | 0.0 | Y |  |  |
| KPS_T_WATER_USAGE_SHOPUNIT | 9 | WATER_USAGE | NUMBER | 22 | 10.0 | 0.0 | Y |  |  |
| KPS_T_WATER_USAGE_SHOPUNIT | 10 | BILLING_FLAG | NUMBER | 22 | 10.0 | 0.0 | Y |  |  |
| KPS_T_WATER_USAGE_SHOPUNIT | 11 | AOT_EXPENSE_FLAG | NUMBER | 22 | 10.0 | 0.0 | Y |  |  |
| KPS_T_WATER_USAGE_SHOPUNIT | 12 | TREAT_RATE | NUMBER | 22 | 10.0 | 4.0 | Y |  |  |
| KPS_T_WATER_USAGE_SHOPUNIT | 13 | TREAT_AMT | NUMBER | 22 | 10.0 | 2.0 | Y |  |  |
| KPS_T_WATER_USAGE_SHOPUNIT | 14 | TARIFF_RATE | NUMBER | 22 | 10.0 | 4.0 | Y |  |  |
| KPS_T_WATER_USAGE_SHOPUNIT | 15 | TARIFF_AMT | NUMBER | 22 | 10.0 | 2.0 | Y |  |  |
| KPS_T_WATER_USAGE_SHOPUNIT | 16 | MTRATE | NUMBER | 22 | 10.0 | 4.0 | Y |  |  |
| KPS_T_WATER_USAGE_SHOPUNIT | 17 | MTCHARGE_AMT | NUMBER | 22 | 10.0 | 2.0 | Y |  |  |
| KPS_T_WATER_USAGE_SHOPUNIT | 18 | VAT_AMT | NUMBER | 22 | 10.0 | 4.0 | Y |  |  |
| KPS_T_WATER_USAGE_SHOPUNIT | 19 | TOTAL_AMT | NUMBER | 22 | 10.0 | 2.0 | Y |  |  |
| KPS_T_WATER_USAGE_SHOPUNIT | 20 | CREATEDBY | VARCHAR2 | 30 |  |  | Y |  |  |
| KPS_T_WATER_USAGE_SHOPUNIT | 21 | CREATEDDATE | DATE | 7 |  |  | Y |  |  |
| KPS_T_WATER_USAGE_SHOPUNIT | 22 | UPDATEDBY | VARCHAR2 | 30 |  |  | Y |  |  |
| KPS_T_WATER_USAGE_SHOPUNIT | 23 | UPDATEDDATE | DATE | 7 |  |  | Y |  |  |
| KPS_T_WATER_USAGE_SHOPUNIT | 24 | START_DATE | DATE | 7 |  |  | Y |  |  |
| KPS_T_WATER_USAGE_SHOPUNIT | 25 | END_DATE | DATE | 7 |  |  | Y |  |  |
| KPS_T_WATER_USAGE_SHOPUNIT | 26 | TOTAL_VAT_AMT | NUMBER | 22 |  |  | Y |  |  |
| KPS_T_WATER_USAGE_SHOPUNIT | 27 | SERIAL_NO | VARCHAR2 | 30 |  |  | Y |  |  |
| KPS_T_WATER_USAGE_SHOPUNIT | 28 | REMARK | VARCHAR2 | 500 |  |  | Y |  |  |
| KPS_T_WATER_USAGE_SHOPUNIT | 29 | SHOP_NAME | VARCHAR2 | 200 |  |  | Y |  |  |
| KPS_T_WATER_USAGE_SHOPUNIT | 30 | INS_LOCATION | VARCHAR2 | 100 |  |  | Y |  |  |
| KPS_T_WATER_USAGE_SHOPUNIT | 31 | RU | VARCHAR2 | 30 |  |  | Y |  |  |
| KPS_T_WATER_USAGE_SHOPUNIT | 32 | SIZE_DESC | VARCHAR2 | 100 |  |  | Y |  |  |
| KPS_T_WATER_USAGE_SHOPUNIT | 33 | COURSE | VARCHAR2 | 30 |  |  | Y |  |  |
| KPS_T_WATER_USAGE_SHOPUNIT | 34 | METER_COUNT | VARCHAR2 | 30 |  |  | Y |  |  |
| KPS_T_WATER_USAGE_SHOPUNIT | 35 | METER_SIZE | VARCHAR2 | 30 |  |  | Y |  |  |
| KPS_T_WATER_USAGE_SHOPUNIT | 36 | INS_LEVEL | VARCHAR2 | 30 |  |  | Y |  |  |
| KPS_T_WATER_USAGE_SHOPUNIT | 37 | CON_CODE | CHAR | 2 |  |  | Y |  |  |

---

## 19_POS

| No. | SFDC Field Name (EN) | SFDC Field Name (TH) | Source Field API Name | Source Field Type | Source Field Length | VULLABLE (N=Required) | KP Table | KP Field Name | KP Field Type | KP Field Length | VULLABLE (N=Required).1 | Progress | Confirm | Type | Required | Sample Data | Description | Status | User/KP Feedback | Remark | Help Text | Track History | External ID | Track History.1 | Encrypted | Page Layout | Length | Source Field API Name.1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Information |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 1 | Concession No. |  | CON_CODE | CHAR | 2.0 | N | KPS_R_POS | CON_CODE | CHAR | 2.0 | N | Ready |  | Text | Yes | 09 - SVB - Terminal 1 | เลขที่รหัสสัมปทาน | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 2 | Tenant |  |  |  |  |  | KPS_R_POS | SHOP_CODE | VARCHAR2 | 20.0 | N | Ready |  |  | Yes | 0902101 | รหัสผู้ประกอบการ | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 3 | Tenant Name |  |  |  |  |  | KPS_R_SHOP | SHOP_NAME_E | VARCHAR2 | 200.0 |  | Ready |  |  | Yes |  | ชื่อผู้ประกอบการ | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 4 | Shop |  | SHOP_CODE | VARCHAR2 | 20.0 | N | KPS_R_POS | BRANCH_CODE | VARCHAR2 | 20.0 | N | Ready |  |  | Yes |  | รหัสร้านค้าผู้ประกอบการ | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 5 | Shop Name |  |  |  |  |  | KPS_R_SHOP | SHORT_NAME | VARCHAR2 | 50.0 |  | Ready |  |  | Yes |  | ชื่อร้านค้าผู้ประกอบการ | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 6 | Unit No. |  |  |  |  |  | KPS_T_POS_REGISTER_HISTORY | AOT_UNIT_POS | VARCHAR2 | 15.0 |  | Ready |  |  | Yes |  | เลข unit ที่ตั้ง ของร้านค้า | Confirmed |  |  |  |  |  |  |  |  |  |  |
| POS Registration |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 7 | POS Registration No. |  | POS_NO | VARCHAR2 | 50.0 | N | KPS_R_POS | POS_NO | VARCHAR2 | 50.0 | N | Ready |  |  | No | E051120002A9144 | เลขที่จดทะเบียนเครื่อง POS เช่น  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 8 | Revenue ID |  |  |  |  |  | KPS_T_POS_REGISTER_HISTORY | REVENUE_ID | VARCHAR2 | 20.0 |  | Ready |  |  | No | E051120002A9144 | เลข Revenue ID เช่น  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 9 | CPU Serial No. |  |  |  |  |  | KPS_T_POS_REGISTER_HISTORY | CPU_SERIAL_NO | VARCHAR2 | 20.0 |  | Ready |  |  | No | 4CE406B317 | เลขที่ CPU serial no. เช่น  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 10 | Start Date |  | SDATE | DATE | 7.0 | Y | KPS_T_POS_REGISTER_HISTORY | START_DATE | DATE | 7.0 |  | Ready |  |  | No | 28/09/2020 |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 11 | End Date |  | EDATE | DATE | 7.0 | Y | KPS_T_POS_REGISTER_HISTORY | END_DATE | DATE | 7.0 |  | Ready |  |  | No | 28/09/2020 |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 12 | Status |  | STATUS | NUMBER | 22.0 | Y | KPS_R_POS | STATUS | NUMBER | 1.0 |  | Ready |  |  | No | - Active - Inactive | สถานะการใช้งาน เครื่อง POS | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 13 | IP Address |  |  |  |  |  |  |  |  |  |  | Ready |  |  | No | 172.21.13.999 | เลข IP address ของเครื่อง POS | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 14 | Mac Address |  |  |  |  |  |  |  |  |  |  | Ready |  |  | No | 2C-58-B9-0F-1C-03 | เลข MAC address ของเครื่อง POS | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 15 | Supplier Code |  | POS_SUPPLIER_CODE | VARCHAR2 | 3.0 | Y | KPS_R_POS | POS_SUPPLIER_CODE | VARCHAR2 | 3.0 | Y | Ready |  |  | No | 075 |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 16 | Supplier Name |  |  |  |  |  | KPS_R_POS_SUPPLIER | NAME_E | VARCHAR2 | 100.0 |  | Ready |  |  | No | akksofttech |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 17 | Remark |  |  |  |  |  | KPS_T_POS_REGISTER_HISTORY | REMARK | VARCHAR2 | 50.0 |  | Ready |  |  | No | ยกเลิก ตั้งแต่เวลา 23.30 น. |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 18 | Action |  |  |  |  |  |  |  |  |  |  | Ready |  |  | No | - Add - Update - Delete | การจัดการข้อมูลล่าสุด | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 19 | Attachment - ภพ.06 |  | FILE_NAME | VARCHAR2 | 60.0 | Y | KPS_R_POS | FILE_NAME | VARCHAR2 | 60.0 |  | Ready |  |  | No |  | เอกสาร ภพ.06 ที่แนบมา | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 20 | Attachment - คก.2 |  |  |  |  |  |  |  |  |  |  | Ready |  |  | No |  | เอกสาร คก.2 ที่แนบมา | Confirmed |  |  |  |  |  |  |  |  |  |  |
|  |  |  | BRANCH_CODE | VARCHAR2 | 20.0 | N | KPS_R_POS | BRANCH_CODE | VARCHAR2 | 20.0 | N | Not Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | TYPE_SEND_MAIL | VARCHAR2 | 4.0 | Y | KPS_R_POS | TYPE_SEND_MAIL | VARCHAR2 | 4.0 |  | Not Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | Contract? |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |

---

## 20_Sales Transaction_User

| No. | SFDC Field Name (EN) | SFDC Field Name (TH) | Source Field API Name | Source Field Type | Source Field Length | VULLABLE (N=Required) | KP Table | KP Field Name | KP Field Type | KP Field Length | VULLABLE (N=Required).1 | Progress | Confirm | Type | Required | Sample Data | Description | Status | User/KP Feedback | Remark | Help Text | Track History | External ID | Track History.1 | Encrypted | Page Layout | Length | Source Field API Name.1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  ปริมาณการแลกเปลี่ยน ตราสารและเงินตรา ต่างประเทศ |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 1 | Concession No. |  | CON_CODE | CHAR | 2.0 | N | KPS_R_CONCESS | CON_CODE | CHAR | 2.0 | N | Ready |  | Text | Yes | 09 - SVB - Terminal 1 | เลขที่รหัสสัมปทาน | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 2 | Tenant |  |  |  |  |  | KPS_R_SHOP | SHOP_CODE | VARCHAR2 | 20.0 | N | Ready |  |  | Yes | 0902101 | รหัสผู้ประกอบการ | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 3 | Tenant Name |  |  |  |  |  | KPS_R_SHOP | SHOP_NAME_E | VARCHAR2 | 200.0 |  | Ready |  |  | Yes |  | ชื่อผู้ประกอบการ | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 4 | Sales Date |  | SALE_DATE | CHAR | 10.0 | N | KPS_T_SALESBANK_MD | SALE_DATE | CHAR | 10.0 | N | Ready |  |  | Yes |  | วันที่ของยอดขาย | Confirmed |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | ***ตัวอย่างตามรูปค่ะ*** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| รายงานยอดรายรับเบื้องต้นของ tenant (SVB / HKT DMK)  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 1 | Concession No. |  |  |  |  |  | KPS_R_CONCESS | CON_CODE | CHAR | 2.0 | N | Ready |  | Text | Yes | 09 - SVB - Terminal 1 | เลขที่รหัสสัมปทาน | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 2 | Sales Date From |  |  |  |  |  | KPS_T_SALES_M | SALE_DATE | CHAR | 10.0 | N | Ready |  |  | Yes |  | วันที่ของยอดขาย | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 3 | Sales Date To |  |  |  |  |  | KPS_T_SALES_M | SALE_DATE | CHAR | 10.0 | N | Ready |  |  | Yes |  | วันที่สุดท้ายของยอดขายที่ต้องการเรียกข้อมูล | Confirmed |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | ***ตัวอย่างตามรูปค่ะ*** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| ยอดจำหน่ายสินค้าและบริการ และกำไรขั้นต้นจากการแลกเปลี่ยน ตราสารและเงินตราต่างประเทศ |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 1 | Concession No. |  |  |  |  |  | KPS_R_CONCESS | CON_CODE | CHAR | 2.0 | N | Ready |  | Text | Yes | 09 - SVB - Terminal 1 | เลขที่รหัสสัมปทาน | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 2 | Sales Date From |  |  |  |  |  | KPS_T_SALES_M | SALE_DATE | CHAR | 10.0 | N | Ready |  |  | Yes |  | วันที่ของยอดขาย | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 3 | Sales Date To |  |  |  |  |  | KPS_T_SALES_M | SALE_DATE | CHAR | 10.0 | N | Ready |  |  | Yes |  | วันที่สุดท้ายของยอดขายที่ต้องการเรียกข้อมูล | Confirmed |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | ***ตัวอย่างตามรูปค่ะ*** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | CON_CODE | CHAR | 2.0 | N | KPS_T_SALES_M | CON_CODE | CHAR | 2.0 | N | Not Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | SHOP_CODE | VARCHAR2 | 20.0 | N | KPS_T_SALES_M | SHOP_CODE | VARCHAR2 | 20.0 | N | Not Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | BRANCH_CODE | VARCHAR2 | 20.0 | N | KPS_T_SALES_M | BRANCH_CODE | VARCHAR2 | 20.0 | N | Not Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | POS_NO | VARCHAR2 | 50.0 | N | KPS_T_SALES_M | POS_NO | VARCHAR2 | 50.0 | N | Not Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | SALE_NO | VARCHAR2 | 50.0 | N | KPS_T_SALES_M | SALE_NO | VARCHAR2 | 50.0 | N | Not Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | SALE_DATE | CHAR | 10.0 | N | KPS_T_SALES_M | SALE_DATE | CHAR | 10.0 | N | Not Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | SALE_TYPE | NUMBER | 22.0 | N | KPS_T_SALES_M | SALE_TYPE | NUMBER | 22.0 | N | Not Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | SHIFT_NO | NUMBER | 22.0 | N | KPS_T_SALES_M | SHIFT_NO | NUMBER | 22.0 | N | Not Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | DOC_DATE | CHAR | 19.0 | N | KPS_T_SALES_M | DOC_DATE | CHAR | 19.0 | N | Not Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | CREATE_DATE | CHAR | 19.0 | N | KPS_T_SALES_M | CREATE_DATE | CHAR | 19.0 | N | Not Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | TRANS_DATE | CHAR | 19.0 | N | KPS_T_SALES_M | TRANS_DATE | CHAR | 19.0 | N | Not Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | VAT_TYPE | NUMBER | 22.0 | N | KPS_T_SALES_M | VAT_TYPE | NUMBER | 22.0 | N | Not Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | VAT_AMT | NUMBER | 22.0 | N | KPS_T_SALES_M | VAT_AMT | NUMBER | 22.0 | N | Not Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | AMT_EXC_VAT | NUMBER | 22.0 | N | KPS_T_SALES_M | AMT_EXC_VAT | NUMBER | 22.0 | N | Not Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | AMT_INC_VAT | NUMBER | 22.0 | N | KPS_T_SALES_M | AMT_INC_VAT | NUMBER | 22.0 | N | Not Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | EXTRA_DISC_VAT_AMT | NUMBER | 22.0 | N | KPS_T_SALES_M | EXTRA_DISC_VAT_AMT | NUMBER | 22.0 | N | Not Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | EXTRA_DISC_AMT_EXC_VAT | NUMBER | 22.0 | N | KPS_T_SALES_M | EXTRA_DISC_AMT_EXC_VAT | NUMBER | 22.0 | N | Not Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | EXTRA_DISC_AMT_INC_VAT | NUMBER | 22.0 | N | KPS_T_SALES_M | EXTRA_DISC_AMT_INC_VAT | NUMBER | 22.0 | N | Not Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | DISC_AVG_PERCENTAGE | NUMBER | 22.0 | N | KPS_T_SALES_M | DISC_AVG_PERCENTAGE | NUMBER | 22.0 | N | Not Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | SERVICE_CHARGE_TYPE | NUMBER | 22.0 | N | KPS_T_SALES_M | SERVICE_CHARGE_TYPE | NUMBER | 22.0 | N | Not Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | SERVICE_CHARGE_EXC_VAT | NUMBER | 22.0 | N | KPS_T_SALES_M | SERVICE_CHARGE_EXC_VAT | NUMBER | 22.0 | N | Not Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | SERVICE_CHARGE_VAT | NUMBER | 22.0 | N | KPS_T_SALES_M | SERVICE_CHARGE_VAT | NUMBER | 22.0 | N | Not Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | SERVICE_CHARGE_INC_VAT | NUMBER | 22.0 | N | KPS_T_SALES_M | SERVICE_CHARGE_INC_VAT | NUMBER | 22.0 | N | Not Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | NET_EXC_VAT | NUMBER | 22.0 | N | KPS_T_SALES_M | NET_EXC_VAT | NUMBER | 22.0 | N | Not Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | NET_VAT | NUMBER | 22.0 | N | KPS_T_SALES_M | NET_VAT | NUMBER | 22.0 | N | Not Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | NET_INC_VAT | NUMBER | 22.0 | N | KPS_T_SALES_M | NET_INC_VAT | NUMBER | 22.0 | N | Not Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | CON_CODE | CHAR | 2.0 | N | KPS_T_SALES_MD | CON_CODE | CHAR | 2.0 | N | Not Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | SHOP_CODE | VARCHAR2 | 20.0 | N | KPS_T_SALES_MD | SHOP_CODE | VARCHAR2 | 20.0 | N | Not Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | BRANCH_CODE | VARCHAR2 | 20.0 | N | KPS_T_SALES_MD | BRANCH_CODE | VARCHAR2 | 20.0 | N | Not Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | POS_NO | VARCHAR2 | 50.0 | N | KPS_T_SALES_MD | POS_NO | VARCHAR2 | 50.0 | N | Not Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | SALE_NO | VARCHAR2 | 50.0 | N | KPS_T_SALES_MD | SALE_NO | VARCHAR2 | 50.0 | N | Not Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | SALE_DATE | CHAR | 10.0 | N | KPS_T_SALES_MD | SALE_DATE | CHAR | 10.0 | N | Not Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | SEQ | NUMBER | 22.0 | N | KPS_T_SALES_MD | SEQ | NUMBER | 22.0 | Y | Not Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | PROD_SERV_CODE | VARCHAR2 | 100.0 | N | KPS_T_SALES_MD | PROD_SERV_CODE | VARCHAR2 | 100.0 | N | Not Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | PROD_SERV_QTY | NUMBER | 22.0 | N | KPS_T_SALES_MD | PROD_SERV_QTY | NUMBER | 22.0 | N | Not Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | AMT_EXC_VAT | NUMBER | 22.0 | N | KPS_T_SALES_MD | AMT_EXC_VAT | NUMBER | 22.0 | N | Not Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | AMT_INC_VAT | NUMBER | 22.0 | N | KPS_T_SALES_MD | AMT_INC_VAT | NUMBER | 22.0 | N | Not Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | VAT_RATE | NUMBER | 22.0 | N | KPS_T_SALES_MD | VAT_RATE | NUMBER | 22.0 | N | Not Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | VAT_AMT | NUMBER | 22.0 | N | KPS_T_SALES_MD | VAT_AMT | NUMBER | 22.0 | N | Not Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | AOT_PRICE_EXC_VAT | NUMBER | 22.0 | N | KPS_T_SALES_MD | AOT_PRICE_EXC_VAT | NUMBER | 22.0 | N | Not Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | AOT_PRICE_INC_VAT | NUMBER | 22.0 | N | KPS_T_SALES_MD | AOT_PRICE_INC_VAT | NUMBER | 22.0 | N | Not Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | SALE_TYPE | NUMBER | 22.0 | N | KPS_T_SALES_MD | SALE_TYPE | NUMBER | 22.0 | Y | Not Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | UNIT_DISC_PERCENTAGE | NUMBER | 22.0 | N | KPS_T_SALES_MD | UNIT_DISC_PERCENTAGE | NUMBER | 22.0 | N | Not Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | UNIT_AMT_EXC_VAT | NUMBER | 22.0 | N | KPS_T_SALES_MD | UNIT_AMT_EXC_VAT | NUMBER | 22.0 | N | Not Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | UNIT_AMT_VAT | NUMBER | 22.0 | N | KPS_T_SALES_MD | UNIT_AMT_VAT | NUMBER | 22.0 | N | Not Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | UNIT_AMT_INC_VAT | NUMBER | 22.0 | N | KPS_T_SALES_MD | UNIT_AMT_INC_VAT | NUMBER | 22.0 | N | Not Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | UNIT_DISC_AMT_EXC_VAT | NUMBER | 22.0 | N | KPS_T_SALES_MD | UNIT_DISC_AMT_EXC_VAT | NUMBER | 22.0 | N | Not Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | UNIT_DISC_VAT_AMT | NUMBER | 22.0 | N | KPS_T_SALES_MD | UNIT_DISC_VAT_AMT | NUMBER | 22.0 | N | Not Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | UNIT_DISC_INC_VAT_AMT | NUMBER | 22.0 | N | KPS_T_SALES_MD | UNIT_DISC_INC_VAT_AMT | NUMBER | 22.0 | N | Not Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | UNIT_NET_AMT_EXC_VAT | NUMBER | 22.0 | N | KPS_T_SALES_MD | UNIT_NET_AMT_EXC_VAT | NUMBER | 22.0 | N | Not Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | UNIT_NET_AMT_VAT | NUMBER | 22.0 | N | KPS_T_SALES_MD | UNIT_NET_AMT_VAT | NUMBER | 22.0 | N | Not Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | UNIT_NET_AMT_INC_VAT | NUMBER | 22.0 | N | KPS_T_SALES_MD | UNIT_NET_AMT_INC_VAT | NUMBER | 22.0 | N | Not Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | TOTAL_AMT_EXC_VAT | NUMBER | 22.0 | N | KPS_T_SALES_MD | TOTAL_AMT_EXC_VAT | NUMBER | 22.0 | N | Not Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | TOTAL_AMT_VAT | NUMBER | 22.0 | N | KPS_T_SALES_MD | TOTAL_AMT_VAT | NUMBER | 22.0 | N | Not Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | TOTAL_AMT_INC_VAT | NUMBER | 22.0 | N | KPS_T_SALES_MD | TOTAL_AMT_INC_VAT | NUMBER | 22.0 | N | Not Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | TOTAL_DISC_AMT_EXC_VAT | NUMBER | 22.0 | N | KPS_T_SALES_MD | TOTAL_DISC_AMT_EXC_VAT | NUMBER | 22.0 | N | Not Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | TOTAL_DISC_VAT_AMT | NUMBER | 22.0 | N | KPS_T_SALES_MD | TOTAL_DISC_VAT_AMT | NUMBER | 22.0 | N | Not Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | TOTAL_DISC_AMT_INC_VAT | NUMBER | 22.0 | N | KPS_T_SALES_MD | TOTAL_DISC_AMT_INC_VAT | NUMBER | 22.0 | N | Not Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | TOTAL_NET_AMT_EXC_VAT | NUMBER | 22.0 | N | KPS_T_SALES_MD | TOTAL_NET_AMT_EXC_VAT | NUMBER | 22.0 | N | Not Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | TOTAL_NET_AMT_VAT | NUMBER | 22.0 | N | KPS_T_SALES_MD | TOTAL_NET_AMT_VAT | NUMBER | 22.0 | N | Not Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | TOTAL_NET_AMT_INC_VAT | NUMBER | 22.0 | N | KPS_T_SALES_MD | TOTAL_NET_AMT_INC_VAT | NUMBER | 22.0 | N | Not Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | TOTAL_DISPLAY_AMT | NUMBER | 22.0 | N | KPS_T_SALES_MD | TOTAL_DISPLAY_AMT | NUMBER | 22.0 | N | Not Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |

---

## 20_Financial Transaction (Detai

| No. | SFDC Field Name (EN) | SFDC Field Name (TH) | Source Field API Name | Source Field Type | Source Field Length | VULLABLE (N=Required) | KP Table | KP Field Name | KP Field Type | KP Field Length | VULLABLE (N=Required).1 | Progress | Confirm | Type | Required | Sample Data | Description | Status | User/KP Feedback | Remark | Help Text | Track History | External ID | Track History.1 | Encrypted | Page Layout | Length | Source Field API Name.1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Rental |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Rental Fee Per Month | ค่าเช่าต่อเดือน |  |  |  |  |  |  |  |  |  |  |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Days Per Month | จำนวนวันที่คำนวณค่าเช่า |  |  |  |  |  |  |  |  |  |  |  | Number |  |  |  |  |  | จำนวนวันที่คำนวณค่าเช่า = (จำนวนวันในเดือน – จำนวนวันที่นับจำกวันส่งมอบพื้นที่ + 1) |  |  |  |  |  |  |  |  |
|  | Day Since Handover | จำนวนวันที่นับจากวันส่งมอบพื้นที่ |  |  |  |  |  |  |  |  |  |  |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Building Land Tax | ค่าภาษีโรงเรือน และที่ดิน |  |  |  |  |  |  |  |  |  |  |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Service Fee | ค่าธรรมเนียมการใช้บริการ |  |  |  |  |  |  |  |  |  |  |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Amount charge | จำนวนเงินที่เรียกเก็บ |  |  |  |  |  |  |  |  |  |  |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Monthly Rental Fee Charge | ค่าเช่าพื้นที่รายเดือนที่เรียกเก็บ |  |  |  |  |  |  |  |  |  |  |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Monthly Rental Fee Charge If Discount | ค่าเช่าพื้นที่รายเดือนที่เรียกเก็บทั้งหมด ถ้ามีส่วนลด |  |  |  |  |  |  |  |  |  |  |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Minimum Guarantee |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Concession | สนามบิน |  |  |  |  |  |  |  |  |  |  |  | Text |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Contract No. | เลขสัญญาเช่า |  |  |  |  |  |  |  |  |  |  |  | Text |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Minimum Guarantee | ส่วนแบ่งรายได้ขั้นต่ำ |  |  |  |  |  |  |  |  |  |  |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Days Per Month | จำนวนวันที่คำนวณค่าเช่า |  |  |  |  |  |  |  |  |  |  |  | Number |  |  |  |  |  | จำนวนวันที่คำนวณค่าเช่า = (จำนวนวันในเดือน – จำนวนวันที่นับจำกวันส่งมอบพื้นที่ + 1) |  |  |  |  |  |  |  |  |
|  | Day Since Handover | จำนวนวันที่นับจากวันส่งมอบพื้นที่ |  |  |  |  |  |  |  |  |  |  |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Amount charge | จำนวนเงินออกใบแจ้งหนี้ |  |  |  |  |  |  |  |  |  |  |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Invoice Amount |  |  |  |  |  |  |  |  |  |  |  |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | New Minimum Guarantee | ส่วนแบ่งรายได้ขั้นต่ำ ใหม่ |  |  |  |  |  |  |  |  |  |  |  | Number |  |  |  |  |  | มีการคำนวณได้ 3 ประเภทขึ้นอยู่กับสัญญา |  |  |  |  |  |  |  |  |
|  | Whichever Higher Minimum Guarantee Estimate | ยอดที่สูงกว่าสำหรับกรณีคำนวณ Minimum Guarantee Estimate |  |  |  |  |  |  |  |  |  |  |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Whichever Higher Minimum Guarantee Actual | ยอดที่สูงกว่าสำหรับกรณีคำนวณ Minimum Guarantee Actual |  |  |  |  |  |  |  |  |  |  |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Estimate Month End Adjust Amount | ยอดที่ปรับปรุงตอนสิ้นเดือน |  |  |  |  |  |  |  |  |  |  |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Monthly Accounting Adjustment | ยอดที่ต้องปรับปรุงทางบัญชีเพิ่มเติมในเดือนประกอบการนั้นๆ |  |  |  |  |  |  |  |  |  |  |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Adjusted Invoice Amount | ยอดที่ต้องออกใบแจ้งหนี้ |  |  |  |  |  |  |  |  |  |  |  | Number |  |  |  |  |  | ยอดที่ต้องปรับปรุงทางบัญชีเพิ่มเติมในเดือนประกอบการนั้นๆ = Whichever Higher (Actual) - Whichever Higher (Estimate) |  |  |  |  |  |  |  |  |
|  | Adjusted Credit Amount | ยอดที่ต้องออกใบลดหนี้ |  |  |  |  |  |  |  |  |  |  |  | Number |  |  |  |  |  | ยอดที่ต้องออกใบแจ้งหนี้ / ใบลดหนี้ เพิ่มเติม = Whichever Higher (Actual) - Whichever Higher (Revenue Sharing) |  |  |  |  |  |  |  |  |
|  | Final Adjusted Invoice Amount | ยอดสุทธิที่ต้องออกใบแจ้งหนี้ เพิ่มเติม |  |  |  |  |  |  |  |  |  |  |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Final Adjusted Credit Amount | ยอดสุทธิที่ต้องออกใบลดหนี้ เพิ่มเติม |  |  |  |  |  |  |  |  |  |  |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | New Minimum Guarantee Fixed Amount | ส่วนแบ่งรายได้ขั้นต่ำรายปี กรณี Fixed Amount |  |  |  |  |  |  |  |  |  |  |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | New Minimum Guarantee PG | ส่วนแบ่งรายได้ขั้นต่ำรายปี กรณีปรับตาม PG |  |  |  |  |  |  |  |  |  |  |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | New Minimum Guarantee Fixed Rate | ส่วนแบ่งรายได้ขั้นต่ำรายปี กรณี Fixed Rate |  |  |  |  |  |  |  |  |  |  |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | New Minimum Guarantee MAGi | ส่วนแบ่งรายได้ขั้นต่ำรายปี กรณี MAG(i) |  |  |  |  |  |  |  |  |  |  |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Passenger Growth |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Estimate Passenger Growth Rate Per Month | อัตราการเติบโตผู้โดยสารต่อเดือนโดยประมาณ |  |  |  |  |  |  |  |  |  |  |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Estimate Passenger Growth Rate Per Year | อัตราการเติบโตผู้โดยสารต่อปีโดยประมาณ |  |  |  |  |  |  |  |  |  |  |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Actual Passenger Growth Rate Per Month | อัตราการเติบโตผู้โดยสารต่อเดือน |  |  |  |  |  |  |  |  |  |  |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Actual Passenger Growth Rate Per Year | อัตราการเติบโตผู้โดยสารต่อปี |  |  |  |  |  |  |  |  |  |  |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Estimate Current Passenger Amount | จำนวนผู้โดยสารรอบปัจจุบันโดยประมาณ |  |  |  |  |  |  |  |  |  |  |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Estimate Previous Passenger Amount | จำนวนผู้โดยสารรอบก่อนหน้าโดยประมาณ |  |  |  |  |  |  |  |  |  |  |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Concession | สนามบิน |  |  |  |  |  |  |  |  |  |  |  | Text |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Whichever Higher Estimate | ยอดที่สูงกว่าโดยประมาณ |  |  |  |  |  |  |  |  |  |  |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Whichever Higher Actual | ยอดที่สูงกว่า |  |  |  |  |  |  |  |  |  |  |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Avg Passenger | จำนวนผู้โดยสารโดยเฉลี่ย |  |  |  |  |  |  |  |  |  |  |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Passenger Growth Rate | อัตราการเติบโตผู้โดยสาร |  |  |  |  |  |  |  |  |  |  |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Revenue Sharing |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Whichever Higher Revenue Sharing | ยอดที่สูงกว่าสำหรับกรณีคำนวณ Revenue Sharing |  |  |  |  |  |  |  |  |  |  |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Charged_Revenue_Sharing_Amount__c | ยอดที่เรียกเก็บส่วนแบ่งรายได้จากการประกอบกิจการ |  |  |  |  |  |  |  |  |  |  |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Invoice_Charged_Amount__c | ยอดที่เรียกเก็บตามใบแจ้งหนี้ |  |  |  |  |  |  |  |  |  |  |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Electric |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Concession | สนามบิน |  |  |  |  |  |  |  |  |  |  |  | Text |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Usage Unit | จำนวนหน่วยที่ใช้จริง |  |  |  |  |  |  |  |  |  |  |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Current Meter Reading | หน่วยมิเตอร์ปัจจุบัน |  |  |  |  |  |  |  |  |  |  |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Last Meter Reading | หน่วยมิเตอร์ครั้งก่อนหน้า |  |  |  |  |  |  |  |  |  |  |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | TOU Current Meter Reading | หน่วยมิเตอร์ปัจจุบัน TOU |  |  |  |  |  |  |  |  |  |  |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | TOU Last Meter Reading | หน่วยมิเตอร์ครั้งก่อนหน้า TOU |  |  |  |  |  |  |  |  |  |  |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Electrical Charge Per Unit | ค่าไฟต่อหน่วย |  |  |  |  |  |  |  |  |  |  |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Service Meter | ค่ารักษามิเตอร์ |  |  |  |  |  |  |  |  |  |  |  | Number |  |  | Service Meter SVB & DMK = 33.29 บาท Service Meter HKT = 46.16 บาท |  |  |  |  |  |  |  |  |  |  |  |
|  | FT Charge | ค่า FT |  |  |  |  |  |  |  |  |  |  |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Service Charge | ค่าบริการ |  |  |  |  |  |  |  |  |  |  |  | Number |  |  | Service Charge = (รวมค่ำพลังงำนไฟฟ้ำ) + Service Meter + FT  * 0.1 ปัดทศนิยม 2 ตำแหน่ง |  |  |  |  |  |  |  |  |  |  |  |
|  | Total Electrical Bill | ค่าไฟทั้งสิ้น |  |  |  |  |  |  |  |  |  |  |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Total Electrical AOT | ค่าไฟทั้งสิ้นจาก AOT |  |  |  |  |  |  |  |  |  |  |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Electrical Charge Variance | ส่วนต่างของค่าไฟ |  |  |  |  |  |  |  |  |  |  |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Difference Ratio | สัดส่วนส่วนต่าง |  |  |  |  |  |  |  |  |  |  |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Electrical Bill Adjustment Amount | ยอดปรับปรุงค่าไฟ |  |  |  |  |  |  |  |  |  |  |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Electrical Monthly Adjusted Invoice Amount | ยอดปรับปรุงค่าไฟที่ต้องออกใบแจ้งหนี้ |  |  |  |  |  |  |  |  |  |  |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Electrical Monthly Adjusted Credit Amount | ยอดปรับปรุงค่าไฟที่ต้องออกใบลดหนี้ |  |  |  |  |  |  |  |  |  |  |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Invoice Owner | owner ตาม invoice |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Owner | owner ตามเรียกเก็บจริง |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Water |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Concession | สนามบิน |  |  |  |  |  |  |  |  |  |  |  | Text |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Usage Unit | จำนวนหน่วยที่ใช้จริง |  |  |  |  |  |  |  |  |  |  |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Current Meter Reading Value | หน่วยมิเตอร์ปัจจุบัน |  |  |  |  |  |  |  |  |  |  |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Last Meter Reading Value | หน่วยมิเตอร์ครั้งก่อนหน้า |  |  |  |  |  |  |  |  |  |  |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Water Charge Per Unit | ค่าน้ําต่อหน่วย |  |  |  |  |  |  |  |  |  |  |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Wastewater Treatment Fee | ค่าบำบัดน้ำ |  |  |  |  |  |  |  |  |  |  |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Maintenance Fee | ค่าบำรุงรักษามาตร |  |  |  |  |  |  |  |  |  |  |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Total Water Bill | ค่าน้ํ้ำทั้งสิ้น |  |  |  |  |  |  |  |  |  |  |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Total Water AOT | ค่าน้ํ้ำทั้งสิ้นจาก AOT |  |  |  |  |  |  |  |  |  |  |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Water Charge Variance | ส่วนต่างของค่าน้ำ |  |  |  |  |  |  |  |  |  |  |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Difference Ratio | สัดส่วนส่วนต่าง |  |  |  |  |  |  |  |  |  |  |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Water Bill Adjustment Amount | ยอดปรับปรุงค่าน้ำ |  |  |  |  |  |  |  |  |  |  |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Water Monthly Adjusted Invoice Amount | ยอดปรับปรุงค่าน้ำยอดที่ต้องออกใบแจ้งหนี้ |  |  |  |  |  |  |  |  |  |  |  | Number |  |  |  |  |  | ยอดที่ต้องปรับปรุงทางบัญชีเพิ่มเติมในเดือนประกอบการนั้นๆ = Whichever Higher (Actual) - Whichever Higher (Estimate) |  |  |  |  |  |  |  |  |
|  | Water Monthly Adjusted Credit Amount | ยอดปรับปรุงค่าน้ำยอดที่ต้องออกใบลดหนี้ |  |  |  |  |  |  |  |  |  |  |  | Number |  |  |  |  |  | ยอดที่ต้องออกใบแจ้งหนี้ / ใบลดหนี้ เพิ่มเติม = Whichever Higher (Actual) - Whichever Higher (Revenue Sharing) |  |  |  |  |  |  |  |  |
|  | Invoice Owner | owner ตาม invoice |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Owner | owner ตามเรียกเก็บจริง |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |

---

## 20_Sales Transaction (Details)

| No. | SFDC Field Name (EN) | SFDC Field Name (TH) | Source Field API Name | Source Field Type | Source Field Length | VULLABLE (N=Required) | KP Table | KP Field Name | KP Field Type | KP Field Length | VULLABLE (N=Required).1 | Progress | Confirm | Type | Required | Sample Data | Description | Status | User/KP Feedback | Remark | Help Text | Track History | External ID | Track History.1 | Encrypted | Page Layout | Length | Source Field API Name.1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Commercial |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | BRANCH_CODE |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | SALE_NO |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | POS_NO |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | SALE_TYPE |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | SALE_DATE |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | SHIFT_NO |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | CREATE_DATE |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | TRANS_DATE |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | MEMBER_ID |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | SVC_ID |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | NAME |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | FLIGHT_NO |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | FLIGHT_DATE |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | NATION_CODE |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | PASSPORT_NO |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | BIRTH_DATE |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | SEX |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | VAT_TYPE |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | VAT_RATE |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | AMT_EXC_VAT |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | VAT_AMT |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | AMT_INC_VAT |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | PRO_CODE |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | EXTRA_DISC_VAT_AMT |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | EXTRA_DISC_AMT_EXC_VAT |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | EXTRA_DISC_AMT_INC_VAT |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | DISC_VAT_AMT |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | DISC_AMT_EXC_VAT |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | DISC_AMT_INC_VAT |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | DISC_AVG_PERCENTAGE |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | SERVICE_CHARGE_TYPE |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | SERVICE_CHARGE_EXC_VAT |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | SERVICE_CHARGE_VAT |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | SERVICE_CHARGE_INC_VAT |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | NET_EXC_VAT |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | NET_VAT |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | NET_INC_VAT |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | CANCEL_TAX_INVOICE_DATE |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | CANCEL_TAX_INVOICE |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | CANCEL_TAX_INVOICE_POS_NAME |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | VOID_REASON |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | RC_CODE |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |

---

## 20_Sales Transaction (Summary)

| No. | SFDC Field Name (EN) | SFDC Field Name (TH) | Source Field API Name | Source Field Type | Source Field Length | VULLABLE (N=Required) | KP Table | KP Field Name | KP Field Type | KP Field Length | VULLABLE (N=Required).1 | Progress | Confirm | Type | Required | Sample Data | Description | Status | User/KP Feedback | Remark | Help Text | Track History | External ID | Track History.1 | Encrypted | Page Layout | Length | Source Field API Name.1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | Revenue from Sales and Services | ยอดจำหน่ายสินค้าและบริการ |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Foreign Exchange and Securities Trading Volume | ปริมาณการแลกเปลี่ยนตราสารและเงินตราต่างประเทศ |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Total Amount | ยอดรวม |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Total Sales | ยอดขายรวม |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Gain (Loss) on Foreign Exchange | กำไรขาดทุนจากการแลกเปลี่ยน |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Revenue from Sales and Services | ยอดจำหน่ายสินค้าและบริการ |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Sum of Currency Brought | ยอดซื้อทั้งหมดของการแลกเปลี่ยนตราสารและเงินตรา |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Sum of  Currency Sold | ยอดขายทั้งหมดของการแลกเปลี่ยนตราสารและเงินตรา |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |

---

## 21_Supplier

| No. | SFDC Field Name (EN) | SFDC Field Name (TH) | Source Field API Name | Source Field Type | Source Field Length | VULLABLE (N=Required) | KP Table | KP Field Name | KP Field Type | KP Field Length | VULLABLE (N=Required).1 | Progress | Confirm | Type | Required | Sample Data | Description | Status | User/KP Feedback | Remark | Help Text | Track History | External ID | Track History.1 | Encrypted | Page Layout | Length | Source Field API Name.1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Information |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 1 |  |  |  |  |  |  |  |  |  |  |  | Not Ready |  |  |  |  |  | New |  |  |  |  |  |  |  |  |  |  |
| 2 |  |  |  |  |  |  |  |  |  |  |  | Not Ready |  |  |  |  |  | New |  |  |  |  |  |  |  |  |  |  |
| 3 |  |  |  |  |  |  |  |  |  |  |  | Not Ready |  |  |  |  |  | New |  |  |  |  |  |  |  |  |  |  |
| 4 |  |  |  |  |  |  |  |  |  |  |  | Not Ready |  |  |  |  |  | New |  |  |  |  |  |  |  |  |  |  |
| 5 |  |  |  |  |  |  |  |  |  |  |  | Not Ready |  |  |  |  |  | New |  |  |  |  |  |  |  |  |  |  |
| 6 |  |  |  |  |  |  |  |  |  |  |  | Not Ready |  |  |  |  |  | New |  |  |  |  |  |  |  |  |  |  |
| 7 |  |  |  |  |  |  |  |  |  |  |  | Not Ready |  |  |  |  |  | New |  |  |  |  |  |  |  |  |  |  |
| 8 |  |  |  |  |  |  |  |  |  |  |  | Not Ready |  |  |  |  |  | New |  |  |  |  |  |  |  |  |  |  |
| 9 |  |  |  |  |  |  |  |  |  |  |  | Not Ready |  |  |  |  |  | New |  |  |  |  |  |  |  |  |  |  |
| 10 |  |  |  |  |  |  |  |  |  |  |  | Not Ready |  |  |  |  |  | New |  |  |  |  |  |  |  |  |  |  |
|  |  |  | POS_SUPPLIER_CODE | VARCHAR2 | 3.0 | N | KPS_R_POS_SUPPLIER | POS_SUPPLIER_CODE | VARCHAR2 | 3.0 | N |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | NAME_E | VARCHAR2 | 100.0 | Y | KPS_R_POS_SUPPLIER | NAME_E | VARCHAR2 | 100.0 | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | SHORT_NAME | VARCHAR2 | 60.0 | Y | KPS_R_POS_SUPPLIER | SHORT_NAME | VARCHAR2 | 60.0 | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | ACTIVE | NUMBER | 22.0 | Y | KPS_R_POS_SUPPLIER | ACTIVE | NUMBER | 22.0 | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | TEL | VARCHAR2 | 60.0 | Y | KPS_R_POS_SUPPLIER | TEL | VARCHAR2 | 60.0 | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | FAX | VARCHAR2 | 60.0 | Y | KPS_R_POS_SUPPLIER | FAX | VARCHAR2 | 60.0 | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | ADDRESS1 | VARCHAR2 | 60.0 | Y | KPS_R_POS_SUPPLIER | ADDRESS1 | VARCHAR2 | 60.0 | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | ADDRESS2 | VARCHAR2 | 60.0 | Y | KPS_R_POS_SUPPLIER | ADDRESS2 | VARCHAR2 | 60.0 | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | CITY | VARCHAR2 | 60.0 | Y | KPS_R_POS_SUPPLIER | CITY | VARCHAR2 | 60.0 | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | ZIP_CODE | CHAR | 5.0 | Y | KPS_R_POS_SUPPLIER | ZIP_CODE | CHAR | 5.0 | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | POS_SUPPLIER_CODE | VARCHAR2 | 3.0 | N | KPS_R_EMAIL_SUPPLIER | POS_SUPPLIER_CODE | VARCHAR2 | 3.0 | N |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | SEQ | NUMBER | 22.0 | N | KPS_R_EMAIL_SUPPLIER | SEQ | NUMBER | 22.0 | N |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | NAMES | VARCHAR2 | 60.0 | N | KPS_R_EMAIL_SUPPLIER | NAMES | VARCHAR2 | 60.0 | N |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | EMAIL | VARCHAR2 | 100.0 | N | KPS_R_EMAIL_SUPPLIER | EMAIL | VARCHAR2 | 100.0 | N |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |

---

## 22_Invoice

| No. | SFDC Field Name (EN) | SFDC Field Name (TH) | Source Field API Name | Source Field Type | Source Field Length | VULLABLE (N=Required) | KP Table | KP Field Name | KP Field Type | KP Field Length | VULLABLE (N=Required).1 | Progress | Confirm | Type | Required | Sample Data | Description | Status | User/KP Feedback | Remark | Help Text | Track History | External ID | Track History.1 | Encrypted | Page Layout | Length | Source Field API Name.1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Information |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 1 |  |  |  |  |  |  |  |  |  |  |  | Not Ready |  |  |  |  |  | New |  |  |  |  |  |  |  |  |  |  |
| 2 |  |  |  |  |  |  |  |  |  |  |  | Not Ready |  |  |  |  |  | New |  |  |  |  |  |  |  |  |  |  |
| 3 |  |  |  |  |  |  |  |  |  |  |  | Not Ready |  |  |  |  |  | New |  |  |  |  |  |  |  |  |  |  |
| 4 |  |  |  |  |  |  |  |  |  |  |  | Not Ready |  |  |  |  |  | New |  |  |  |  |  |  |  |  |  |  |
| 5 |  |  |  |  |  |  |  |  |  |  |  | Not Ready |  |  |  |  |  | New |  |  |  |  |  |  |  |  |  |  |
| 6 |  |  |  |  |  |  |  |  |  |  |  | Not Ready |  |  |  |  |  | New |  |  |  |  |  |  |  |  |  |  |
| 7 |  |  |  |  |  |  |  |  |  |  |  | Not Ready |  |  |  |  |  | New |  |  |  |  |  |  |  |  |  |  |
| 8 |  |  |  |  |  |  |  |  |  |  |  | Not Ready |  |  |  |  |  | New |  |  |  |  |  |  |  |  |  |  |
| 9 |  |  |  |  |  |  |  |  |  |  |  | Not Ready |  |  |  |  |  | New |  |  |  |  |  |  |  |  |  |  |
| 10 |  |  |  |  |  |  |  |  |  |  |  | Not Ready |  |  |  |  |  | New |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | PREINV_NO | VARCHAR2 | 15.0 | N |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | CON_CODE | CHAR | 2.0 | N |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | TERM_CODE | VARCHAR2 | 10.0 | N |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | CREATEDBY | VARCHAR2 | 30.0 | N |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | CREATEDDATE | DATE | 7.0 | N |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | UPDATEDBY | VARCHAR2 | 30.0 | N |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | UPDATEDDATE | DATE | 7.0 | N |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | PREINV_NO | VARCHAR2 | 15.0 | N |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | PREINV_SEQ | NUMBER | 22.0 | N |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | CHARGE_CODE | VARCHAR2 | 5.0 | N |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | CREATEDBY | VARCHAR2 | 30.0 | N |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | CREATEDDATE | DATE | 7.0 | N |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | UPDATEDBY | VARCHAR2 | 30.0 | N |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | UPDATEDDATE | DATE | 7.0 | N |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |

---

## 23_Promotion

| No. | SFDC Field Name (EN) | SFDC Field Name (TH) | Source Field API Name | Source Field Type | Source Field Length | VULLABLE (N=Required) | KP Table | KP Field Name | KP Field Type | KP Field Length | VULLABLE (N=Required).1 | Progress | Confirm | Type | Required | Sample Data | Description | Status | User/KP Feedback | Remark | Help Text | Track History | External ID | Track History.1 | Encrypted | Page Layout | Length | Source Field API Name.1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Information |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 1 | Promo Code |  | PRO_CODE | VARCHAR2 | 10.0 | N | KPS_R_PROMOTION | PRO_CODE | VARCHAR2 | 10.0 | N | Ready |  | Yes |  |  | Individual Concession -> (CON Abbreviation)(3) + (Running No.)(4) SVB0009 DMK0007 HKT0007  2+ Concession -> "AXX" + (Running No.)(4) AXX0001 | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 2 | Promo Description |  | PRO_DESC | VARCHAR2 | 200.0 | Y | KPS_R_PROMOTION | PRO_DESC | VARCHAR2 | 200.0 | Y | Ready |  | Yes |  | Privileges for Bangkok International Flim Festival Participants |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 3 | Promo Start Date |  | PRO_SDATE | VARCHAR2 | 19.0 | Y | KPS_R_PROMOTION | PRO_SDATE | VARCHAR2 | 19.0 | Y | Ready |  | Yes |  | 23/09/2010 |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 4 | Promo End Date |  | PRO_EDATE | VARCHAR2 | 19.0 | Y | KPS_R_PROMOTION | PRO_EDATE | VARCHAR2 | 19.0 | Y | Ready |  | Yes |  | 23/09/2015 |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 5 | Promo Eligibility |  |  |  |  |  | KPS_R_PRO_SHOP.KPS_R_CONCESS | CON_CODE | CHAR | 2.0 | N | Ready |  | Yes |  | - SVB - DMK - HKT |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 6 | Promo Type |  | PROTYPE_CODE | VARCHAR2 | 5.0 | Y | KPS_R_PROMOTION | PROTYPE_CODE | VARCHAR2 | 5.0 | Y | Ready |  | Yes |  | 01. การใช้คูปอง 02. การใช้บัตร รับส่วนลด/ของสมนาคุณ 03. ซื้อชุดสินค้าหรือบริการราคาพิเศษ (Combo Set) 04. ใช้ส่วนลด จากการซื้อสินค้า หรือบริการครบตามจำนวนรายการหรือจำนวนเงินที่กำหนด 05. ซื้อสินค้า หรือบริการ ครบตามจำนวนรายการหรือจำนวนเงินที่กำหนด ได้รับ...ฟรีทันที 06. ซื้อสินค้า หรือบริการที่กำหนด ได้รับส่วนลดทันที 07. แสดงใบเสร็จที่มียอดการซื้อสินค้า หรือบริการ ครบตามที่กำหนด ได้รับ Discount 08. แสดงใบเสร็จที่มียอดการซื้อสินค้า หรือบริการ ครบตามที่กำหนด ได้รับ...ฟรีในครั้งต่อไป 09. ซื้อสินค้า หรือบริการ ครบตามที่กำหนดในราคาปกติรับสะสมแต้ม ได้รับ...ฟรี 10. ซื้อสินค้า หรือบริการ ครบตามที่กำหนดในราคาปกติรับสะสมแต้ม ครบตามกำหนดได้รับได้รับส่วนลดในครั้งต่อไป 11. On Top Promotion ได้รับ...ฟรีทันที 12. On Top Promotion ได้รับส่วนลดทันที 13. รับ...ฟรี (แบบไม่มีเงื่อนไข) 14. รายการส่งเสริมการขายของผู้ประกอบการ |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 7 | Promo Category |  | PROCATG_CODE | VARCHAR2 | 5.0 | Y | KPS_R_PROMOTION | PROCATG_CODE | VARCHAR2 | 5.0 | Y | Ready |  | Yes |  | 01. Tenant Promotion 02. Co-Promotion  03. Staff Benefits 04. Flight Delay 05. Partnership Promotion |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 8 | Created Date |  |  |  |  |  | KPS_R_PROMOTION | CREATEDDATE | DATE | 7.0 | Y | Ready |  | Yes |  |  |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 9 | Start Date |  | KPS_R_PRO_LAUNCH.START_DATE | DATE | 7.0 | Y | KPS_R_PRO_LAUNCH | START_DATE | DATE | 7.0 | Y | Ready |  | Yes |  |  | วันที่เริ่มจำหน่าย | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 10 | End Date |  | KPS_R_PRO_LAUNCHEND_DATE | DATE | 7.0 | Y | KPS_R_PRO_LAUNCH | END_DATE | DATE | 7.0 | Y | Ready |  | Yes |  |  | วันที่สิ้นสุดการจำหน่าย | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 11 | Promo Phase No. |  | . |  |  |  | KPS_R_PRO_LAUNCH | LAUNCHNO | VARCHAR2 | 10.0 | N | Ready |  | Yes |  | - 1 - 2 - 3 - 4 |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 12 | Target Description |  | TARGET_DESC | VARCHAR2 | 200.0 | Y | KPS_R_PROMOTION | TARGET_DESC | VARCHAR2 | 200.0 | Y | Ready |  |  |  | Burger king Booklet |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 13 | Sales Target Amount |  | TARGETAMT | NUMBER | 22.0 | Y | KPS_R_PROMOTION | TARGETAMT | NUMBER | 22.0 | Y | Ready |  |  |  | 100,000.00 |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 14 | Per |  |  |  |  |  | KPS_R_PROMOTION | TARGETPERTYPE | VARCHAR2 | 30.0 | Y | Ready |  |  |  | - Day - Month |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 15 | Budget Amount |  | BUTGETAMT | NUMBER | 22.0 | Y | KPS_R_PROMOTION | BUTGETAMT | NUMBER | 22.0 | Y | Ready |  |  |  | 100,000.00 |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 16 | Attach Memo |  |  |  |  |  | KPS_R_PRO_LAUNCH | MEMONO | VARCHAR2 | 30.0 | N | Ready |  |  |  |  |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 17 | Promotion Status |  |  |  |  |  | KPS_R_PROMOTION_TMSI | STATUS | NUMBER | 22.0 | Y | Ready |  | Yes |  |  |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | PRO_CODE | VARCHAR2 | 10.0 | N |  |  |  |  |  |  |  |  |  |  |  |  |  | KPS_R_PROMOTION |  |  |  |  |  |  |  |  |
|  |  |  | PROTYPE_CODE | VARCHAR2 | 5.0 | N |  |  |  |  |  |  |  |  |  |  |  |  |  | KPS_R_PROMOTION_TYPE |  |  |  |  |  |  |  |  |
|  |  |  | PROOWNER_CODE | VARCHAR2 | 30.0 | N |  |  |  |  |  |  |  |  |  |  |  |  |  | KPS_R_PROMOTION_OWNER |  |  |  |  |  |  |  |  |
|  |  |  | PROCATG_CODE | VARCHAR2 | 5.0 | N |  |  |  |  |  |  |  |  |  |  |  |  |  | KPS_R_PROMOTION_CATG |  |  |  |  |  |  |  |  |
|  |  |  | PRO_CODE | VARCHAR2 | 10.0 | N |  |  |  |  |  |  |  |  |  |  |  |  |  | KPS_R_PRO_LAUNCH |  |  |  |  |  |  |  |  |
|  |  |  | LAUNCHNO | VARCHAR2 | 10.0 | N |  |  |  |  |  |  |  |  |  |  |  |  |  | KPS_R_PRO_LAUNCH |  |  |  |  |  |  |  |  |
|  |  |  | MEMONO | VARCHAR2 | 30.0 | N |  |  |  |  |  |  |  |  |  |  |  |  |  | KPS_R_PRO_LAUNCH |  |  |  |  |  |  |  |  |
|  |  |  | PRO_CODE | VARCHAR2 | 10.0 | N |  |  |  |  |  |  |  |  |  |  |  |  |  | KPS_R_PRO_SHOP |  |  |  |  |  |  |  |  |
|  |  |  | LAUNCHNO | VARCHAR2 | 10.0 | N |  |  |  |  |  |  |  |  |  |  |  |  |  | KPS_R_PRO_SHOP |  |  |  |  |  |  |  |  |
|  |  |  | PROJOINSEQ | NUMBER | 22.0 | N |  |  |  |  |  |  |  |  |  |  |  |  |  | KPS_R_PRO_SHOP |  |  |  |  |  |  |  |  |
|  |  |  | CON_CODE | CHAR | 2.0 | N |  |  |  |  |  |  |  |  |  |  |  |  |  | KPS_R_PRO_SHOP |  |  |  |  |  |  |  |  |
|  |  |  | SHOP_CODE | VARCHAR2 | 20.0 | N |  |  |  |  |  |  |  |  |  |  |  |  |  | KPS_R_PRO_SHOP |  |  |  |  |  |  |  |  |
|  |  |  | PRO_CODE | VARCHAR2 | 10.0 | N |  |  |  |  |  |  |  |  |  |  |  |  |  | KPS_R_PRO_SHOPBRANCH |  |  |  |  |  |  |  |  |
|  |  |  | LAUNCHNO | VARCHAR2 | 10.0 | N |  |  |  |  |  |  |  |  |  |  |  |  |  | KPS_R_PRO_SHOPBRANCH |  |  |  |  |  |  |  |  |
|  |  |  | PROJOINSEQ | NUMBER | 22.0 | N |  |  |  |  |  |  |  |  |  |  |  |  |  | KPS_R_PRO_SHOPBRANCH |  |  |  |  |  |  |  |  |
|  |  |  | CON_CODE | CHAR | 2.0 | N |  |  |  |  |  |  |  |  |  |  |  |  |  | KPS_R_PRO_SHOPBRANCH |  |  |  |  |  |  |  |  |
|  |  |  | SHOP_CODE | VARCHAR2 | 20.0 | N |  |  |  |  |  |  |  |  |  |  |  |  |  | KPS_R_PRO_SHOPBRANCH |  |  |  |  |  |  |  |  |
|  |  |  | BRANCH_CODE | VARCHAR2 | 20.0 | N |  |  |  |  |  |  |  |  |  |  |  |  |  | KPS_R_PRO_SHOPBRANCH |  |  |  |  |  |  |  |  |
|  |  |  | SHOP_UNIT | VARCHAR2 | 15.0 | N |  |  |  |  |  |  |  |  |  |  |  |  |  | KPS_R_PRO_SHOPBRANCH |  |  |  |  |  |  |  |  |

---

## 24_Airline

| No. | SFDC Field Name (EN) | SFDC Field Name (TH) | Source Field API Name | Source Field Type | Source Field Length | VULLABLE (N=Required) | KP Table | KP Field Name | KP Field Type | KP Field Length | VULLABLE (N=Required).1 | Progress | Confirm | Type | Required | Sample Data | Description | Status | User/KP Feedback | Remark | Help Text | Track History | External ID | Track History.1 | Encrypted | Page Layout | Length | Source Field API Name.1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Header |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 1 | Airline Code |  | AIRLINE_CODE | VARCHAR2 | 20.0 | N | KPS_R_AIRLINE | AIRLINE_CODE | VARCHAR2 | 20.0 | N | Ready |  |  |  |  |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 2 | Airline Name |  | AIRLINE_NAME | VARCHAR2 | 100.0 | Y | KPS_R_AIRLINE | AIRLINE_NAME | VARCHAR2 | 100.0 | Y | Ready |  |  |  |  |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 3 | Airline Short Name |  | SHORTCODE | VARCHAR2 | 10.0 | Y | KPS_R_AIRLINE | SHORTCODE | VARCHAR2 | 10.0 | Y | Ready |  |  |  |  |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 4 | Airline Nationality |  | NATION_CODE | VARCHAR2 | 10.0 | N | KPS_R_AIRLINE | NATION_CODE | VARCHAR2 | 10.0 | N | Ready |  |  |  |  |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 5 | Airline Status |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  | - Active - Inactive - Expired - Suspended |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| Airline Office Address - Contract Address |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 6 | Building / Village |  | ADDRESS1 | VARCHAR2 | 100.0 | Y | KPS_R_AIRLINE | ADDRESS1 | VARCHAR2 | 100.0 | Y | Ready |  |  |  |  |  | Confirmed | อยากให้เพิ่มเลขประจำตัวผู้เสียภาษีสายการบิน |  |  |  |  |  |  |  |  |  |
| 7 | Address No. |  | ADDRESS2 | VARCHAR2 | 100.0 | Y | KPS_R_AIRLINE | ADDRESS2 | VARCHAR2 | 100.0 | Y | Ready |  |  |  | Thai Airways International Public Company Limited 333 Moo 1 |  | Confirmed | อยากให้เพิ่มระยะเวลาชำระเงิน (วัน) |  |  |  |  |  |  |  |  |  |
| 8 | Soi |  |  |  |  |  | ไม่มีบน Table |  |  |  |  | Ready |  |  |  |  |  | Confirmed | อยากให้เพิ่มระยะเวลาส่ง Invoice (วัน) |  |  |  |  |  |  |  |  |  |
| 9 | Street |  |  |  |  |  | ไม่มีบน Table |  |  |  |  | Ready |  |  |  |  |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 10 | Sub-District |  |  |  |  |  | ไม่มีบน Table |  |  |  |  | Ready |  |  |  | Nong Prue |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 11 | District |  | CITY | VARCHAR2 | 30.0 | Y | KPS_R_AIRLINE | ADDRESS2 | VARCHAR2 | 100.0 | Y |  |  |  |  | Bangphli |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 12 | Province |  | STATE | VARCHAR2 | 30.0 | Y | KPS_R_AIRLINE | CITY | VARCHAR3 | 30.0 | Y | Ready |  |  |  | Samut Prakarn |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 13 | Zip Code |  | ZIPCODE | VARCHAR2 | 10.0 | Y | KPS_R_AIRLINE | ZIPCODE | VARCHAR2 | 10.0 | Y | Ready |  |  |  | 10540 |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 14 | Country |  | TEL | VARCHAR2 | 30.0 | Y | KPS_R_AIRLINE | COUNTRY_CODE | VARCHAR2 | 3.0 | Y | Ready |  |  |  | Thailand |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 15 | Tel. |  | COUNTRY_CODE | VARCHAR2 | 3.0 | Y | KPS_R_AIRLINE | TEL | VARCHAR2 | 30.0 | Y | Ready |  |  |  | 02-134-5300 |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| Airline Contact Person |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 16 | Name-Surname |  | CONTACT | VARCHAR2 | 20.0 | Y | KPS_R_AIRLINE | CONTACT | VARCHAR2 | 20.0 | Y | Ready |  |  |  |  |  | Confirmed | อยากให้เพิ่ม Airline Operations Contact |  |  |  |  |  |  |  |  |  |
| 17 | Nickname |  |  |  |  |  | ไม่มีใน TMS |  |  |  |  | Ready |  |  |  |  |  | Confirmed | อยากให้เพิ่ม Airline Finance Contact Name |  |  |  |  |  |  |  |  |  |
| 18 | Mobile No. |  |  |  |  |  | ไม่มีใน TMS |  |  |  |  | Ready |  |  |  |  |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 19 | Email Address |  |  |  |  |  | ไม่มีใน TMS |  |  |  |  | Ready |  |  |  |  |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 20 | Status |  |  |  |  |  | ไม่มีใน TMS |  |  |  |  | Ready |  |  |  | - Active - Inactive |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| Penalty |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 21 | Penalty Type |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  | - Warning - Suspended |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 22 | Penalty Detail |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  | ค้างชำระติดต่อกัน 72 งวด |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 23 | Start Date |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  | 2021-01-04 00:00:00 |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 24 | End Date |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  | 31/03/2031 |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 25 | Penalty Remark |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  | แจ้งตักเตือน 3 ครั้ง |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 26 | Selected Promotion |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  | - All - Flight Delay - ... |  | Confirmed |  |  |  |  |  |  |  |  |  |  |

---

## 25_Flight Delay contract

| No. | SFDC Field Name (EN) | SFDC Field Name (TH) | Unnamed: 3 | Unnamed: 4 | Unnamed: 5 | Unnamed: 6 | KP Table | KP Field Name | KP Field Type | KP Field Length | VULLABLE (N=Required) | Progress | Confirm | Type | Required | Sample Data | Description | Status | User/KP Feedback | Remark | Help Text | Track History | External ID | Track History.1 | Encrypted | Page Layout | Length | Source Field API Name |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Record & Contract Information |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 1 | Created Date |  |  |  |  |  |  |  |  |  |  | Ready |  | Date |  | 2024-01-01 | วันที่สร้าง Record ใน Salesforce | New |  |  |  |  |  |  |  |  |  |  |
| 2 | Contract Number / Agreement Code |  |  |  |  |  |  |  |  |  |  | Ready |  | Text |  | BKP/PG | เลขที่สัญญา เช่น BKP/PG | New |  |  |  |  |  |  |  |  |  |  |
| 3 | Agreement Start Date |  |  |  |  |  |  |  |  |  |  | Ready |  | Date |  | 2024-01-01 | วันที่เริ่มต้นสัญญา | New |  |  |  |  |  |  |  |  |  |  |
| 4 | Agreement End Date |  |  |  |  |  |  |  |  |  |  | Ready |  | Date |  | 2026-12-31 | วันที่สิ้นสุดสัญญา | New |  |  |  |  |  |  |  |  |  |  |
| 5 | Agreement Effective Date |  |  |  |  |  |  |  |  |  |  | Ready |  | Date |  | 2024-01-01 | วันที่สัญญามีผลบังคับใช้ | New |  |  |  |  |  |  |  |  |  |  |
| 6 | Contract Status |  |  |  |  |  |  |  |  |  |  | Ready |  | Picklist |  | Active | สถานะสัญญา | New |  |  |  |  |  |  |  |  |  |  |
| Record & Contract Information |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 7 | Airline Name |  |  |  |  |  | KPS_R_AIRLINE | AIRLINE_NAME | VARCHAR2 | 100.0 | Y | Ready |  | Text |  | Bangkok Airways Public Company Limited | ชื่อสายการบิน | New |  |  |  |  |  |  |  |  |  |  |
| 8 | Airline Code |  |  |  |  |  | KPS_R_AIRLINE | AIRLINE_CODE | VARCHAR2 | 20.0 | N | Ready |  | Text |  | PG | รหัสสายการบิน | New |  |  |  |  |  |  |  |  |  |  |
| 9 | Airline Address |  |  |  |  |  | KPS_R_AIRLINE | ADDRESS1 | VARCHAR2 | 100.0 | Y | Ready |  | Long Text |  | 99 Moo 14 Vibhavadi Rangsit Road, Chomphon, Chatuchak, Bangkok 10900 | ที่อยู่สายการบิน | New |  |  |  |  |  |  |  |  |  |  |
| 10 | Airline Invoice Address |  |  |  |  |  |  |  |  |  |  | Ready |  | Long Text |  | Bangkok Airways Public Company Limited, 99 Moo 14 Vibhavadi Rangsit Road, Bangkok 10900 | ที่อยู่ออก Invoice | New |  |  |  |  |  |  |  |  |  |  |
| 11 | Airline Billing Address |  |  |  |  |  |  |  |  |  |  | Ready |  | Long Text |  | Suvarnabhumi Airport, Concourse A | ที่อยู่วางบิล | New |  |  |  |  |  |  |  |  |  |  |
| 12 | Airline Billing Process |  |  |  |  |  |  |  |  |  |  | Ready |  | Long Text |  | Submit vouchers with invoice to Bangkok Airways Suvarnabhumi Office | ขั้นตอนการวางบิล | New |  |  |  |  |  |  |  |  |  |  |
| Merchant Information |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 13 | Merchant Name |  |  |  |  |  |  |  |  |  |  | Ready |  | Text |  | AIM DHRAM CO., LTD. | ชื่อร้านค้า | New |  |  |  |  |  |  |  |  |  |  |
| 14 | Merchant Address |  |  |  |  |  |  |  |  |  |  | Ready |  | Long Text |  | 60/6-10 Rong Mueang Road, Pathumwan, Bangkok 10330 | ที่อยู่ร้านค้า | New |  |  |  |  |  |  |  |  |  |  |
| 15 | Merchant Payment Information |  |  |  |  |  |  |  |  |  |  | Ready |  | Long Text |  | Siam Commercial Bank PCL, Lat Krabang Branch, A/C No. 397-2-04547-7 | ข้อมูลบัญชีรับเงิน | New |  |  |  |  |  |  |  |  |  |  |
| 16 | Merchant Terms & Conditions |  |  |  |  |  |  |  |  |  |  | Ready |  | Long Text |  | Provide meals according to voucher value and agreement terms | เงื่อนไขร้านค้า | New |  |  |  |  |  |  |  |  |  |  |
| Outlet Information |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 17 | Outlet Name |  |  |  |  |  |  |  |  |  |  | Ready |  | Text |  | Thai Street Food / Kin Japanese Restaurant / Sensib Thai Massage | ชื่อสาขา | New |  |  |  |  |  |  |  |  |  |  |
| 18 | Outlet Location / Terminal |  |  |  |  |  |  |  |  |  |  | Ready |  | Text |  | Suvarnabhumi Airport | Terminal / Concourse | New |  |  |  |  |  |  |  |  |  |  |
| 19 | Outlet List (Addendum A) |  |  |  |  |  |  |  |  |  |  | Ready |  | File |  | See Addendum A | ไฟล์รายชื่อสาขา | New |  |  |  |  |  |  |  |  |  |  |
| Voucher & Pricing |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 20 | Voucher Type |  |  |  |  |  |  |  |  |  |  | Ready |  | Picklist |  | Delay Meal Voucher | ประเภท Voucher | New |  |  |  |  |  |  |  |  |  |  |
| 21 | Cabin Class |  |  |  |  |  |  |  |  |  |  | Ready |  | Picklist |  | First / Business / Economy | Class ผู้โดยสาร | New |  |  |  |  |  |  |  |  |  |  |
| 22 | Value per Cabin Class |  |  |  |  |  |  |  |  |  |  | Ready |  | Number |  | 250 THB | มูลค่า Voucher ต่อ Cabin | New |  |  |  |  |  |  |  |  |  |  |
| 23 | Max Voucher Value per Pax |  |  |  |  |  |  |  |  |  |  | Ready |  | Number |  | 250 | มูลค่าสูงสุดต่อผู้โดยสาร | New |  |  |  |  |  |  |  |  |  |  |
| 24 | Voucher Currency |  |  |  |  |  |  |  |  |  |  | Ready |  | Picklist |  | THB | สกุลเงิน | New |  |  |  |  |  |  |  |  |  |  |
| 25 | Airline Voucher Honoring Rules |  |  |  |  |  |  |  |  |  |  | Ready |  | Long Text |  | Voucher must be stamped and signed by authorized airline staff | เงื่อนไขการรับ Voucher | New |  |  |  |  |  |  |  |  |  |  |
| 26 | Voucher Issuance Method |  |  |  |  |  |  |  |  |  |  | Ready |  | Picklist |  | Company Stamp + Authorized Signature | วิธีออก Voucher | New |  |  |  |  |  |  |  |  |  |  |
| 27 | Voucher Usage Condition |  |  |  |  |  |  |  |  |  |  | Ready |  | Long Text |  | Passenger pays difference if exceeding voucher value | เงื่อนไขการใช้ | New |  |  |  |  |  |  |  |  |  |  |
| Billing & Invoice Conditions |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 28 | Invoice Submission Timeline (Days) |  |  |  |  |  |  |  |  |  |  | Ready |  | Number |  | 30 | จำนวนวันที่ต้องส่ง Invoice | New |  |  |  |  |  |  |  |  |  |  |
| 29 | Payment Term (Days) |  |  |  |  |  |  |  |  |  |  | Ready |  | Number |  | 30 | ระยะเวลาชำระเงิน | New |  |  |  |  |  |  |  |  |  |  |
| 30 | Late Payment Interest Rate |  |  |  |  |  |  |  |  |  |  | Ready |  | Percent |  | 1.25% per month | ดอกเบี้ยกรณีจ่ายช้า | New |  |  |  |  |  |  |  |  |  |  |
| 31 | Billing Office Hours |  |  |  |  |  |  |  |  |  |  | Ready |  | Text |  | Mon–Fri 08:00–17:00 | เวลาทำการ | New |  |  |  |  |  |  |  |  |  |  |
| 32 | Tax ID (Airline) |  |  |  |  |  |  |  |  |  |  | Ready |  | Text |  | 0107556000183 | เลขผู้เสียภาษีสายการบิน | New |  |  |  |  |  |  |  |  |  |  |
| Contact Information |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 33 | Airline Operations Contact |  |  |  |  |  |  |  |  |  |  | Ready |  | Text |  | Supapla Kluenbanglong, Tel. 02-134-8883 | ผู้ติดต่อสายการบิน (Operation) | New |  |  |  |  |  |  |  |  |  |  |
| 34 | Airline Finance Contact |  |  |  |  |  |  |  |  |  |  | Ready |  | Text |  | Anchalee Jaitert, Tel. 02-266-8760 | ผู้ติดต่อสายการบิน (Finance) | New |  |  |  |  |  |  |  |  |  |  |
| 35 | Merchant Operations Contact |  |  |  |  |  |  |  |  |  |  | Ready |  | Text |  | Prapapuss Mutthanawech, Tel. 089-921-3914 | ผู้ติดต่อร้านค้า (Operation) | New |  |  |  |  |  |  |  |  |  |  |
| 36 | Merchant Finance Contact |  |  |  |  |  |  |  |  |  |  | Ready |  | Text |  | Kannika Todok, Tel. 02-214-2779 | ผู้ติดต่อร้านค้า (Finance) | New |  |  |  |  |  |  |  |  |  |  |
| Legal & Supporting Documents |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 37 | Signed Agreement |  |  |  |  |  |  |  |  |  |  | Ready |  | File |  | Coupon Delay Meal Voucher Agreement.pdf | ไฟล์สัญญาที่ลงนามแล้ว | New |  |  |  |  |  |  |  |  |  |  |
| 38 | Company Registration Certificate |  |  |  |  |  |  |  |  |  |  | Ready |  | File |  | DBD Certificate.pdf | หนังสือรับรองบริษัท | New |  |  |  |  |  |  |  |  |  |  |
| 39 | VAT Registration Certificate (PP.20) |  |  |  |  |  |  |  |  |  |  | Ready |  | File |  | PP20.pdf | ใบ ภ.พ.20 | New |  |  |  |  |  |  |  |  |  |  |
| 40 | Airline Attached Documents |  |  |  |  |  |  |  |  |  |  | Ready |  | File |  | Voucher Spec, Addendum A | เอกสารแนบจากสายการบิน | New |  |  |  |  |  |  |  |  |  |  |
| 41 | Other Supporting Documents |  |  |  |  |  |  |  |  |  |  | Ready |  | File |  | Receipt Samples | เอกสารอื่น ๆ | New |  |  |  |  |  |  |  |  |  |  |
| Notes & Remarks |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 42 | Special Conditions / Remarks |  |  |  |  |  |  |  |  |  |  | Ready |  | Long Text |  | Outlets list subject to amendment | เงื่อนไขพิเศษ | New |  |  |  |  |  |  |  |  |  |  |
| 43 | Termination Summary |  |  |  |  |  |  |  |  |  |  | Ready |  | Long Text |  | Termination allowed upon breach or insolvency | สรุปเงื่อนไขยกเลิก | New |  |  |  |  |  |  |  |  |  |  |
| 44 | Internal Notes (SFDC Only) |  |  |  |  |  |  |  |  |  |  | Ready |  | Long Text |  | Sample data based on Bangkok Airways contract | หมายเหตุภายใน | New |  |  |  |  |  |  |  |  |  |  |

---

## 26_Act. Passenger

| No. | SFDC Field Name (EN) | SFDC Field Name (TH) | Unnamed: 3 | Unnamed: 4 | Unnamed: 5 | Unnamed: 6 | KP Table | KP Field Name | KP Field Type | KP Field Length | VULLABLE (N=Required) | Progress | Confirm | Type | Required | Sample Data | Source Field API Name | Description | Status | User/KP Feedback | Help Text | Track History | External ID | Encrypted | Page Layout |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Actual Passenger Information |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 1 | Source | แหล่งข้อมูล |  |  |  |  |  |  |  |  |  | Ready |  | text | Yes | AOT |  | แหล่งข้อมูลคือ AOT แต่อาจได้รับมาจาก mail จาก GL หรือจาก KPD ฯลฯ | Confirmed |  |  |  |  |  |  |
| 2 | Concession |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  | Cancelled |  |  |  |  |  |  |
| 3 | Fiscal Year |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  | Cancelled |  |  |  |  |  |  |
| 4 | Period (Month) |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  | Cancelled |  |  |  |  |  |  |
| 5 | Period (Year) |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  | Cancelled |  |  |  |  |  |  |
| 6 | Schedule Date | วันเดือนปี |  |  |  |  |  |  |  |  |  | Ready |  | date | Yes | 2025-12-01 00:00:00 |  | - | New |  |  |  |  |  |  |
| 7 | Airport_Code | สนามบิน |  |  |  |  |  |  |  |  |  | Ready |  | text | Yes | SVB |  | SVB , HKT , DMK | New |  |  |  |  |  |  |
| 8 | Flight_Int_Arr | จำนวนเที่ยวบินระหว่างประเทศขาเข้า |  |  |  |  |  |  |  |  |  | Ready |  | number | Yes | 390 |  |  | New |  |  |  |  |  |  |
| 9 | Flight_Int_Dep | จำนวนเที่ยวบินระหว่างประเทศขาออก |  |  |  |  |  |  |  |  |  | Ready |  | number | Yes | 391 |  |  | New |  |  |  |  |  |  |
| 10 | Flight_Int_Tot | จำนวนเที่ยวบินระหว่างประเทศทั้งหมด |  |  |  |  |  |  |  |  |  | Ready |  | number | Yes | 781 |  | สูตรผลบวก (ไม่ import เข้า แต่ระบบต้อง create ให้) | New |  |  |  |  |  |  |
| 11 | Flight_Dom_Arr | จำนวนเที่ยวบินภายในประเทศขาเข้า |  |  |  |  |  |  |  |  |  | Ready |  | number | Yes | 126 |  |  | New |  |  |  |  |  |  |
| 12 | Flight_Dom_Dep | จำนวนเที่ยวบินภายในประเทศขาออก |  |  |  |  |  |  |  |  |  | Ready |  | number | Yes | 127 |  |  | New |  |  |  |  |  |  |
| 13 | Flight_Dom_Tot | จำนวนเที่ยวบินภายในประเทศทั้งหมด |  |  |  |  |  |  |  |  |  | Ready |  | number | Yes | 253 |  | สูตรผลบวก (ไม่ import เข้า แต่ระบบต้อง create ให้) | New |  |  |  |  |  |  |
| 14 | Flight_Tot | จำนวนเที่ยวบินทั้งหมด |  |  |  |  |  |  |  |  |  | Ready |  | number | Yes | 1034 |  | สูตรผลบวก (ไม่ import เข้า แต่ระบบต้อง create ให้) | New |  |  |  |  |  |  |
| 15 | Pax_Int_Arr | จำนวนผู้โดยสารระหว่างประเทศขาเข้า |  |  |  |  |  |  |  |  |  | Ready |  | number | Yes | 108943 |  |  | New |  |  |  |  |  |  |
| 16 | Pax_Int_Dep | จำนวนผู้โดยสารระหว่างประเทศขาออก |  |  |  |  |  |  |  |  |  | Ready |  | number | Yes | 96408 |  |  | New |  |  |  |  |  |  |
| 17 | Pax_Int_Transfer | จำนวนผู้โดยสารระหว่างประเทศเปลี่ยนเครื่องบิน  |  |  |  |  |  |  |  |  |  | Ready |  | number | Yes | 13780 |  |  | New |  |  |  |  |  |  |
| 18 | Pax_Int_Tot_Dep | จำนวนผู้โดยสารระหว่างประเทศขาออกทั้งหมด |  |  |  |  |  |  |  |  |  | Ready |  | number | Yes | 110188 |  | สูตรผลบวก (ไม่ import เข้า แต่ระบบต้อง create ให้) | New |  |  |  |  |  |  |
| 19 | Pax_Int_Transit | จำนวนผู้โดยสารระหว่างประเทศพักเครื่อง |  |  |  |  |  |  |  |  |  | Ready |  | number | Yes | 657 |  |  | New |  |  |  |  |  |  |
| 20 | Pax_Int_Tot | จำนวนผู้โดยสารระหว่างประเทศทั้งหมด |  |  |  |  |  |  |  |  |  | Ready |  | number | Yes | 219788 |  | สูตรผลบวก (ไม่ import เข้า แต่ระบบต้อง create ให้) | New |  |  |  |  |  |  |
| 21 | Pax_Dom_Arr | จำนวนผู้โดยสารภายในประเทศขาเข้า |  |  |  |  |  |  |  |  |  | Ready |  | number | Yes | 22009 |  |  | New |  |  |  |  |  |  |
| 22 | Pax_Dom_Dep | จำนวนผู้โดยสารภายในประเทศขาออก |  |  |  |  |  |  |  |  |  | Ready |  | number | Yes | 21665 |  |  | New |  |  |  |  |  |  |
| 23 | Pax_Dom_Transfer | จำนวนผู้โดยสารภายในประเทศเปลี่ยนเครื่องบิน  |  |  |  |  |  |  |  |  |  | Ready |  | number | Yes | 3020 |  |  | New |  |  |  |  |  |  |
| 24 | Pax_Dom_Tot_Dep | จำนวนผู้โดยสารภายในประเทศขาออกทั้งหมด |  |  |  |  |  |  |  |  |  | Ready |  | number | Yes | 24685 |  | สูตรผลบวก (ไม่ import เข้า แต่ระบบต้อง create ให้) | New |  |  |  |  |  |  |
| 25 | Pax_Dom_Transit | จำนวนผู้โดยสารภายในประเทศพักเครื่อง |  |  |  |  |  |  |  |  |  | Ready |  | number | Yes | 0 |  |  | New |  |  |  |  |  |  |
| 26 | Pax_Dom_Tot | จำนวนผู้โดยสารภายในประเทศทั้งหมด |  |  |  |  |  |  |  |  |  | Ready |  | number | Yes | 46694 |  | สูตรผลบวก (ไม่ import เข้า แต่ระบบต้อง create ให้) | New |  |  |  |  |  |  |
| 27 | Pax_Tot_Arr | จำนวนผู้โดยสารขาเข้าทั้งหมด |  |  |  |  |  |  |  |  |  | Ready |  | number | Yes | 131609 |  | สูตรผลบวก (ไม่ import เข้า แต่ระบบต้อง create ให้) | New |  |  |  |  |  |  |
| 28 | Pax_Tot_Dep | จำนวนผู้โดยสารขาออกทั้งหมด |  |  |  |  |  |  |  |  |  | Ready |  | number | Yes | 134873 |  | สูตรผลบวก (ไม่ import เข้า แต่ระบบต้อง create ให้) | New |  |  |  |  |  |  |
| 29 | Pax_Tot | จำนวนผู้โดยสารทั้งหมด |  |  |  |  |  |  |  |  |  | Ready |  | number | Yes | 266482 |  | สูตรผลบวก (ไม่ import เข้า แต่ระบบต้อง create ให้) | New |  |  |  |  |  |  |
| 30 | No. of Passenger |  |  |  |  |  |  |  |  |  |  | Ready |  |  | Yes | 100 |  |  | Cancelled |  |  |  |  |  |  |
| 31 | Growth Amount |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  | 10 |  |  | To be discussed |  |  |  |  |  |  |
| 32 | Growth Rate |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  | 0.1 |  |  | To be discussed |  |  |  |  |  |  |
| 33 | Value Category |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  | - Actual - Estimate |  |  | To be discussed |  |  |  |  |  |  |
| Yearly Average |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 34 | Total Passenger |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  | To be discussed |  |  |  |  |  |  |
| 35 | Average Passenger per Month |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  | To be discussed |  |  |  |  |  |  |
| 36 | Average Growth Rate |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  | To be discussed |  |  |  |  |  |  |
| 37 | Base Year |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  | SVB = Year - 1 DMK and HKT = 2019 |  |  | To be discussed |  |  |  |  |  |  |
| 38 | Total Passenger |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  | To be discussed |  |  |  |  |  |  |
| 39 | Average Passenger per Month |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  | To be discussed |  |  |  |  |  |  |

---

## 27_Tar. Passenger

| No. | SFDC Field Name (EN) | SFDC Field Name (TH) | Unnamed: 3 | Unnamed: 4 | Unnamed: 5 | Unnamed: 6 | KP Table | KP Field Name | KP Field Type | KP Field Length | VULLABLE (N=Required) | Progress | Confirm | Type | Required | Sample Data | Source Field API Name | Description | Status | User/KP Feedback | Help Text | Track History | External ID | Encrypted | Page Layout |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Target Passenger Information |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 1 | Source | แหล่งข้อมูล |  |  |  |  |  |  |  |  |  | Ready |  | text | Yes | KPD |  | ผู้บริหาร KPD พิจารณาแล้วจึงส่ง mail ให้ผู้เกี่ยวข้อง เช่น KPS ปีละ 1 ครั้ง | New |  |  |  |  |  |  |
| 2 | Schedule Date | วันเดือนปี |  |  |  |  |  |  |  |  |  | Ready |  | date | Yes | 2025-12-01 00:00:00 |  | ข้อมูล import เป็นรายเดือน แต่ระบบต้องคำนวณกระจายรายวันให้ครบ | New |  |  |  |  |  |  |
| 3 | Airport_Code | สนามบิน |  |  |  |  | KPS_R_AIRPORT | IATA_CODE | VARCHAR2 | 10.0 | Y | Ready |  | text | Yes | SVB |  | SVB , HKT , DMK | New |  |  |  |  |  |  |
| 4 | Pax_Int_Arr | เป้าหมายจำนวนผู้โดยสารระหว่างประเทศขาเข้า |  |  |  |  |  |  |  |  |  | Ready |  | number | Yes | 77221.80661 |  | ระบบต้องคำนวณเป็นรายวันให้ จากที่ KPD ส่งมาเป็นรายเดือน | New |  |  |  |  |  |  |
| 5 | Pax_Int_Dep | เป้าหมายจำนวนผู้โดยสารระหว่างประเทศขาออก |  |  |  |  |  |  |  |  |  | Ready |  | number | Yes | 77183.6129 |  | ระบบต้องคำนวณเป็นรายวันให้ จากที่ KPD ส่งมาเป็นรายเดือน | New |  |  |  |  |  |  |
| 6 | Pax_Int_Transfer | เป้าหมายจำนวนผู้โดยสารระหว่างประเทศเปลี่ยนเครื่องบิน  |  |  |  |  |  |  |  |  |  | Ready |  | number | Yes | 0 |  | ระบบต้องคำนวณเป็นรายวันให้ จากที่ KPD ส่งมาเป็นรายเดือน | New |  |  |  |  |  |  |
| 7 | Pax_Int_Tot_Dep | เป้าหมายจำนวนผู้โดยสารระหว่างประเทศขาออกทั้งหมด |  |  |  |  |  |  |  |  |  | Ready |  | number | Yes | 77183.6129 |  | สูตรผลบวก (ไม่ import เข้า แต่ระบบต้อง create ให้) | New |  |  |  |  |  |  |
| 8 | Pax_Int_Transit | เป้าหมายจำนวนผู้โดยสารระหว่างประเทศพักเครื่อง |  |  |  |  |  |  |  |  |  | Ready |  | number | Yes | 637.5806452 |  | ระบบต้องคำนวณเป็นรายวันให้ จากที่ KPD ส่งมาเป็นรายเดือน | New |  |  |  |  |  |  |
| 9 | Pax_Int_Tot | เป้าหมายจำนวนผู้โดยสารระหว่างประเทศทั้งหมด |  |  |  |  |  |  |  |  |  | Ready |  | number | Yes | 155043.0002 |  | สูตรผลบวก (ไม่ import เข้า แต่ระบบต้อง create ให้) | New |  |  |  |  |  |  |
| 10 | Pax_Dom_Arr | เป้าหมายจำนวนผู้โดยสารภายในประเทศขาเข้า |  |  |  |  |  |  |  |  |  | Ready |  | number | Yes | 17834.33749 |  | ระบบต้องคำนวณเป็นรายวันให้ จากที่ KPD ส่งมาเป็นรายเดือน | New |  |  |  |  |  |  |
| 11 | Pax_Dom_Dep | เป้าหมายจำนวนผู้โดยสารภายในประเทศขาออก |  |  |  |  |  |  |  |  |  | Ready |  | number | Yes | 17765.14638 |  | ระบบต้องคำนวณเป็นรายวันให้ จากที่ KPD ส่งมาเป็นรายเดือน | New |  |  |  |  |  |  |
| 12 | Pax_Dom_Transfer | เป้าหมายจำนวนผู้โดยสารภายในประเทศเปลี่ยนเครื่องบิน  |  |  |  |  |  |  |  |  |  | Ready |  | number | Yes | 0 |  | ระบบต้องคำนวณเป็นรายวันให้ จากที่ KPD ส่งมาเป็นรายเดือน | New |  |  |  |  |  |  |
| 13 | Pax_Dom_Tot_Dep | เป้าหมายจำนวนผู้โดยสารภายในประเทศขาออกทั้งหมด |  |  |  |  |  |  |  |  |  | Ready |  | number | Yes | 17765.14638 |  | สูตรผลบวก (ไม่ import เข้า แต่ระบบต้อง create ให้) | New |  |  |  |  |  |  |
| 14 | Pax_Dom_Transit | เป้าหมายจำนวนผู้โดยสารภายในประเทศพักเครื่อง |  |  |  |  |  |  |  |  |  | Ready |  | number | Yes | 0 |  | ระบบต้องคำนวณเป็นรายวันให้ จากที่ KPD ส่งมาเป็นรายเดือน | New |  |  |  |  |  |  |
| 15 | Pax_Dom_Tot | เป้าหมายจำนวนผู้โดยสารภายในประเทศทั้งหมด |  |  |  |  |  |  |  |  |  | Ready |  | number | Yes | 35599.48387 |  | สูตรผลบวก (ไม่ import เข้า แต่ระบบต้อง create ให้) | New |  |  |  |  |  |  |
| 16 | Pax_Tot_Arr | เป้าหมายจำนวนผู้โดยสารขาเข้าทั้งหมด |  |  |  |  |  |  |  |  |  | Ready |  | number | Yes | 95693.72474 |  | สูตรผลบวก (ไม่ import เข้า แต่ระบบต้อง create ให้) | New |  |  |  |  |  |  |
| 17 | Pax_Tot_Dep | เป้าหมายจำนวนผู้โดยสารขาออกทั้งหมด |  |  |  |  |  |  |  |  |  | Ready |  | number | Yes | 94948.75928 |  | สูตรผลบวก (ไม่ import เข้า แต่ระบบต้อง create ให้) | New |  |  |  |  |  |  |
| 18 | Pax_Tot | เป้าหมายจำนวนผู้โดยสารทั้งหมด |  |  |  |  |  |  |  |  |  | Ready |  | number | Yes | 190642.484 |  | สูตรผลบวก (ไม่ import เข้า แต่ระบบต้อง create ให้) | New |  |  |  |  |  |  |

---

## 28_Act. Nationality

| No. | SFDC Field Name (EN) | SFDC Field Name (TH) | Unnamed: 3 | Unnamed: 4 | Unnamed: 5 | Unnamed: 6 | KP Table | KP Field Name | KP Field Type | KP Field Length | VULLABLE (N=Required) | Progress | Confirm | Type | Required | Sample Data | Source Field API Name | Description | Status | User/KP Feedback | Help Text | Track History | External ID | Encrypted | Page Layout |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Actual Nationality of Passenger Information |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 1 | Source | แหล่งข้อมูล |  |  |  |  |  |  |  |  |  | Ready |  | text | Yes | IMM |  | ตม. จะส่ง mail ให้ผู้เกี่ยวข้อง เช่น KPS เดือนละ 1 ครั้ง | New |  |  |  |  |  |  |
| 2 | Year | ปี |  |  |  |  |  |  |  |  |  | Ready |  | number | Yes | 2025 |  |  | New |  |  |  |  |  |  |
| 3 | Month | เดือน |  |  |  |  |  |  |  |  |  | Ready |  | number | Yes | 1 |  |  | New |  |  |  |  |  |  |
| 4 | Date | วันที่ |  |  |  |  |  |  |  |  |  | Ready |  | date | Yes | 31/01/2025 |  | เนื่องจากข้อมูลเป็นรายเดือน วันที่จะเป็นวันที่สุดท้ายของเดือน | New |  |  |  |  |  |  |
| 5 | Airport | สนามบิน |  |  |  |  | KPS_R_AIRPORT | IATA_CODE | VARCHAR2 | 10 | Y | Ready |  | text | Yes | SVB |  | ปัจจุบันมีเฉพาะ SVB แต่ต้องรองรับสำหรับเพิ่ม airport อื่นๆ | New |  |  |  |  |  |  |
| 6 | CountryCode | รหัสประเทศ |  |  |  |  | KPS_R_NATIONALITY | COUNTRY_CODE | VARCHAR2 | 3 | Y | Ready |  | text | Yes | A02 |  | ใช้ Lookup ข้อมูลกับ Master Table Nation | New |  |  |  |  |  |  |
| 7 | Nation | ชื่อประเทศ |  |  |  |  | KPS_R_NATION KPS_R_NATION | NATION_CODE NATION_DESC | VARCHAR2 VARCHAR2 | 10 50 | N Y | Ready |  | text | Yes | AFRICAN |  | ระบบต้องใช้ CountryCode ไป Lookup ดึงค่าจาก master table Nation | New |  |  |  |  |  |  |
| 8 | Continent | ทวีป |  |  |  |  |  |  |  |  |  | Ready |  | text | Yes | Africa |  | ระบบต้องใช้ CountryCode ไป Lookup ดึงค่าจาก master table Nation | New |  |  |  |  |  |  |
| 9 | Region | ภูมิภาค |  |  |  |  | KPS_R_NATION REGION_NAME | REGION_CODE REGION_NAME | VARCHAR2 VARCHAR2 | 10 100 | Y Y | Ready |  | text | Yes | Africa |  | ระบบต้องใช้ CountryCode ไป Lookup ดึงค่าจาก master table Nation | New |  |  |  |  |  |  |
| 10 | Direction | ประเภทผู้โดยสารตามลักษณะการเดินทาง |  |  |  |  |  |  |  |  |  | Ready |  | text | Yes | ARRIVAL |  | ผู้โดยสารขาเข้า , ขาออก , ฯลฯ ARRIVAL / DEPRATURE / TRANSIT / TRANSFER | New |  |  |  |  |  |  |
| 11 | Male | จำนวนผู้โดยสารที่เป็นเพศชาย |  |  |  |  |  |  |  |  |  | Ready |  | number | Yes | 2500 |  | ปัจจุบันยังไม่มีแยกชายหญิงจึงเก็บทั้งหมดเป็นเพศชายไว้ก่อน | New |  |  |  |  |  |  |
| 12 | Female | จำนวนผู้โดยสารที่เป็นเพศหญิง |  |  |  |  |  |  |  |  |  | Ready |  | number | Yes | 0 |  | ปัจจุบันยังไม่มีแยกชายหญิงจึงเก็บทั้งหมดเป็นเพศชายไว้ก่อน | New |  |  |  |  |  |  |
| 13 | Total | จำนวนผู้โดยสารทั้งหมด |  |  |  |  |  |  |  |  |  | Ready |  | number | Yes | 2500 |  | สูตรผลบวก (ไม่ import เข้า แต่ระบบต้อง create ให้) | New |  |  |  |  |  |  |
| 14 | Zone | ประเภทการแบ่งอาณาเขตพื้นที่ตามเส้นทางเครื่องบิน |  |  |  |  |  |  |  |  |  | Ready |  | text | Yes | INTERNATIONAL |  | เครื่องบินระหว่างประเทศ , ในประเทศ  INTERNATIONAL / DOMESTIC (ปัจจุบันมีแต่ INTERNATIONAL) | New |  |  |  |  |  |  |

---

## 29_By concourse

| No. | SFDC Field Name (EN) | SFDC Field Name (TH) | Unnamed: 3 | Unnamed: 4 | Unnamed: 5 | Unnamed: 6 | KP Table | KP Field Name | KP Field Type | KP Field Length | VULLABLE (N=Required) | Progress | Confirm | Type | Required | Sample Data | Source Field API Name | Description | Status | User/KP Feedback | Help Text | Track History | External ID | Encrypted | Page Layout |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| By concourse (Actual Passenger) Information |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 1 | Source | แหล่งข้อมูล |  |  |  |  |  |  |  |  |  | Ready |  | text | Yes | AOT |  | แหล่งข้อมูลคือ AOT แต่ได้รับมาจาก mail จาก GL เดือนละ 1 ครั้ง | New |  |  |  |  |  |  |
| 2 | Period (Year) | ปี |  |  |  |  |  |  |  |  |  | Ready |  | number | Yes | 2025-10-31 00:00:00 |  | - | New |  |  |  |  |  |  |
| 3 | Period (Month) | เดือน |  |  |  |  |  |  |  |  |  | Ready |  | number | Yes | 10 |  | - | New |  |  |  |  |  |  |
| 4 | Date | วันเดือนปี (วันที่สุดท้ายของเดือน) |  |  |  |  |  |  |  |  |  | Ready |  | date | Yes | 31/10/2025 |  | วันสุดท้ายของเดือนนั้นๆ | New |  |  |  |  |  |  |
| 5 | Airport_Code | สนามบิน |  |  |  |  | KPS_R_AIRPORT | IATA_CODE | VARCHAR2 | 10.0 | Y | Ready |  | text | Yes | SVB |  | ปัจจุบันมีเฉพาะ SVB แต่ต้องรองรับสำหรับเพิ่ม airport อื่นๆ | New |  |  |  |  |  |  |
| 6 | Position | ประเภทของจุดขึ้นเครื่อง  |  |  |  |  |  |  |  |  |  | Ready |  | text | Yes | Contact |  | เช่น Contact / Remote  (Remote : Shuttle bus ไปขึ้นระยะไกล) | New |  |  |  |  |  |  |
| 7 | Building | อาคารหรือจุดขึ้นเครื่อง  |  |  |  |  | KPS_R_BUILDING | B_DESC | VARCHAR2 | 30.0 | N | Ready |  | text | Yes | A |  | เช่น Gate A,B,C,... หรืออาคาร SAT1 ฯลฯ | New |  |  |  |  |  |  |
| 8 | SubBuilding | หมายเลขของจุดขึ้นเครื่อง  |  |  |  |  |  |  |  |  |  | Ready |  | text | Yes | A1 |  | เช่น A1 A2 A3 A4 A5 A6 ฯลฯ | New |  |  |  |  |  |  |
| 9 | Flight_Int_Arr | จำนวนเที่ยวบินระหว่างประเทศขาเข้า |  |  |  |  |  |  |  |  |  | Ready |  | number | Yes | 8 |  |  | New |  |  |  |  |  |  |
| 10 | Flight_Int_Dep | จำนวนเที่ยวบินระหว่างประเทศขาออก |  |  |  |  |  |  |  |  |  | Ready |  | number | Yes | 2 |  |  | New |  |  |  |  |  |  |
| 11 | Flight_Int_Tot | จำนวนเที่ยวบินระหว่างประเทศทั้งหมด |  |  |  |  |  |  |  |  |  | Ready |  | number | Yes | 10 |  | สูตรผลบวก (ไม่ import เข้า แต่ระบบต้อง create ให้) | New |  |  |  |  |  |  |
| 12 | Flight_Dom_Arr | จำนวนเที่ยวบินภายในประเทศขาเข้า |  |  |  |  |  |  |  |  |  | Ready |  | number | Yes | 240 |  |  | New |  |  |  |  |  |  |
| 13 | Flight_Dom_Dep | จำนวนเที่ยวบินภายในประเทศขาออก |  |  |  |  |  |  |  |  |  | Ready |  | number | Yes | 248 |  |  | New |  |  |  |  |  |  |
| 14 | Flight_Dom_Tot | จำนวนเที่ยวบินภายในประเทศทั้งหมด |  |  |  |  |  |  |  |  |  | Ready |  | number | Yes | 488 |  | สูตรผลบวก (ไม่ import เข้า แต่ระบบต้อง create ให้) | New |  |  |  |  |  |  |
| 15 | Flight_Tot | จำนวนเที่ยวบินทั้งหมด |  |  |  |  |  |  |  |  |  | Ready |  | number | Yes | 498 |  | สูตรผลบวก (ไม่ import เข้า แต่ระบบต้อง create ให้) | New |  |  |  |  |  |  |
| 16 | Pax_Int_Arr | จำนวนผู้โดยสารระหว่างประเทศขาเข้า |  |  |  |  |  |  |  |  |  | Ready |  | number | Yes | 829 |  |  | New |  |  |  |  |  |  |
| 17 | Pax_Int_Dep | จำนวนผู้โดยสารระหว่างประเทศขาออก |  |  |  |  |  |  |  |  |  | Ready |  | number | Yes | 325 |  |  | New |  |  |  |  |  |  |
| 18 | Pax_Int_Transfer | จำนวนผู้โดยสารระหว่างประเทศเปลี่ยนเครื่องบิน  |  |  |  |  |  |  |  |  |  | Ready |  | number | Yes | 0 |  |  | New |  |  |  |  |  |  |
| 19 | Pax_Int_Tot_Dep | จำนวนผู้โดยสารระหว่างประเทศขาออกทั้งหมด |  |  |  |  |  |  |  |  |  | Ready |  | number | Yes | 325 |  | สูตรผลบวก (ไม่ import เข้า แต่ระบบต้อง create ให้) | New |  |  |  |  |  |  |
| 20 | Pax_Int_Transit | จำนวนผู้โดยสารระหว่างประเทศพักเครื่อง |  |  |  |  |  |  |  |  |  | Ready |  | number | Yes | 0 |  |  | New |  |  |  |  |  |  |
| 21 | Pax_Int_Tot | จำนวนผู้โดยสารระหว่างประเทศทั้งหมด |  |  |  |  |  |  |  |  |  | Ready |  | number | Yes | 1154 |  | สูตรผลบวก (ไม่ import เข้า แต่ระบบต้อง create ให้) | New |  |  |  |  |  |  |
| 22 | Pax_Dom_Arr | จำนวนผู้โดยสารภายในประเทศขาเข้า |  |  |  |  |  |  |  |  |  | Ready |  | number | Yes | 33337 |  |  | New |  |  |  |  |  |  |
| 23 | Pax_Dom_Dep | จำนวนผู้โดยสารภายในประเทศขาออก |  |  |  |  |  |  |  |  |  | Ready |  | number | Yes | 30413 |  |  | New |  |  |  |  |  |  |
| 24 | Pax_Dom_Transfer | จำนวนผู้โดยสารภายในประเทศเปลี่ยนเครื่องบิน  |  |  |  |  |  |  |  |  |  | Ready |  | number | Yes | 3193 |  |  | New |  |  |  |  |  |  |
| 25 | Pax_Dom_Tot_Dep | จำนวนผู้โดยสารภายในประเทศขาออกทั้งหมด |  |  |  |  |  |  |  |  |  | Ready |  | number | Yes | 33606 |  | สูตรผลบวก (ไม่ import เข้า แต่ระบบต้อง create ให้) | New |  |  |  |  |  |  |
| 26 | Pax_Dom_Transit | จำนวนผู้โดยสารภายในประเทศพักเครื่อง |  |  |  |  |  |  |  |  |  | Ready |  | number | Yes | 0 |  |  | New |  |  |  |  |  |  |
| 27 | Pax_Dom_Tot | จำนวนผู้โดยสารภายในประเทศทั้งหมด |  |  |  |  |  |  |  |  |  | Ready |  | number | Yes | 66943 |  | สูตรผลบวก (ไม่ import เข้า แต่ระบบต้อง create ให้) | New |  |  |  |  |  |  |
| 28 | Pax_Tot_Arr | จำนวนผู้โดยสารขาเข้าทั้งหมด |  |  |  |  |  |  |  |  |  | Ready |  | number | Yes | 34166 |  | สูตรผลบวก (ไม่ import เข้า แต่ระบบต้อง create ให้) | New |  |  |  |  |  |  |
| 29 | Pax_Tot_Dep | จำนวนผู้โดยสารขาออกทั้งหมด |  |  |  |  |  |  |  |  |  | Ready |  | number | Yes | 33931 |  | สูตรผลบวก (ไม่ import เข้า แต่ระบบต้อง create ให้) | New |  |  |  |  |  |  |
| 30 | Pax_Tot | จำนวนผู้โดยสารทั้งหมด |  |  |  |  |  |  |  |  |  | Ready |  | number | Yes | 68097 |  | สูตรผลบวก (ไม่ import เข้า แต่ระบบต้อง create ให้) | New |  |  |  |  |  |  |
| 31 | Zone _by_con | ประเภทการแบ่งอาณาเขตพื้นที่ตาม concourse |  |  |  |  | KPS_R_WING | W_DESC | VARCHAR2 | 30.0 | N | Ready |  | text | Yes | EAST |  | ระบบต้องใช้ SubBuilding ไป Lookup ดึงค่าจาก master table by con.  (ปัจจุบันแบ่งเป็น E / W / NA) | New |  |  |  |  |  |  |

---

## 30_Holiday

| No. | SFDC Field Name (EN) | SFDC Field Name (TH) | Unnamed: 3 | Unnamed: 4 | Unnamed: 5 | Unnamed: 6 | KP Table | KP Field Name | KP Field Type | KP Field Length | VULLABLE (N=Required) | Progress | Confirm | Type | Required | Sample Data | Source Field API Name | Description | Status | User/KP Feedback | Help Text | Track History | External ID | Encrypted | Page Layout |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Passenger Information |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 1 | Source | แหล่งข้อมูล |  |  |  |  |  |  |  |  |  | Ready |  | text | Yes | KPG + AOT |  | ประกาศของคิงเพาเวอร์ และวันหยุดของ AOT ที่ไม่ตรงกับคิงเพาเวอร์เพราะมีผลต่อการนับวันในกระบวนการ shop renovation  | New |  |  |  |  |  |  |
| 2 | Holiday Date | วันเดือนปี |  |  |  |  |  |  |  |  |  | Ready |  | date | Yes | 2025-01-01 00:00:00 |  |  | New |  |  |  |  |  |  |
| 3 | Holiday name | ชื่อวันหยุด |  |  |  |  |  |  |  |  |  | Ready |  | text | Yes | วันขึ้นปีใหม่ |  |  | New |  |  |  |  |  |  |
| 4 | Refference | หน่วยงานที่มาของวันหยุด |  |  |  |  |  |  |  |  |  | Ready |  | text | Yes | KPG |  | KPG หรือ AOT | New |  |  |  |  |  |  |

---

## 31_Master Table Nation

| No. | SFDC Field Name (EN) | SFDC Field Name (TH) | Unnamed: 3 | Unnamed: 4 | Unnamed: 5 | Unnamed: 6 | KP Table | KP Field Name | KP Field Type | KP Field Length | VULLABLE (N=Required) | Progress | Confirm | Type | Required | Sample Data | Source Field API Name | Description | Status | User/KP Feedback | Help Text | Track History | External ID | Encrypted | Page Layout |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Nation Information |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 1 | Source | แหล่งข้อมูล |  |  |  |  |  |  |  |  |  | Ready |  | text | Yes | External data |  | DAS รวบรวมเองจากสื่อสาธารณะ website  | New |  |  |  |  |  |  |
| 2 | Code | รหัสประเทศ |  |  |  |  | KPS_R_NATION | NATION_CODE | VARCHAR2 | 10 | N | Ready |  | text | Yes | A02 |  |  | New |  |  |  |  |  |  |
| 3 | Nation | ชื่อประเทศ |  |  |  |  | KPS_R_NATION | NATION_DESC | VARCHAR2 | 50 | Y | Ready |  | text | Yes | AFRICAN |  |  | New |  |  |  |  |  |  |
| 4 | Continent | ทวีป |  |  |  |  |  |  |  |  |  | Ready |  | text | Yes | Africa |  |  | New |  |  |  |  |  |  |
| 5 | Region | ภูมิภาค |  |  |  |  | KPS_R_NATION KPS_R_REGION  | REGION_CODE REGION_NAME | VARCHAR2 VARCHAR2 | 10 100 | Y Y | Ready |  | text | Yes | Africa |  |  | New |  |  |  |  |  |  |

---

## 32_Master Table By Con.

| No. | SFDC Field Name (EN) | SFDC Field Name (TH) | Unnamed: 3 | Unnamed: 4 | Unnamed: 5 | Unnamed: 6 | KP Table | KP Field Name | KP Field Type | KP Field Length | VULLABLE (N=Required) | Progress | Confirm | Type | Required | Sample Data | Source Field API Name | Description | Status | User/KP Feedback | Help Text | Track History | External ID | Encrypted | Page Layout |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Nation Information |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 1 | Source | แหล่งข้อมูล |  |  |  |  |  |  |  |  |  | Ready |  | text | Yes | Internal Data |  | ผู้เกี่ยวข้อง KPS วางข้อตกลงในกการแบ่ง Zone | New |  |  |  |  |  |  |
| 2 | SubBuilding | หมายเลขของจุดขึ้นเครื่อง  |  |  |  |  |  |  |  |  |  | Ready |  | text | Yes | A1 |  |  | New |  |  |  |  |  |  |
| 3 | Zone _by_con | ประเภทการแบ่งอาณาเขตพื้นที่ตาม concourse |  |  |  |  | KPS_R_WING | W_DESC | VARCHAR2 | 30.0 | N | Ready |  | text | Yes | EAST |  | ฝั่ง East หรือ West หรือ Null | New |  |  |  |  |  |  |

---

