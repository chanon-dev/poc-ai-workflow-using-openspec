# KP Smart Tenant Data Migration Specification

> Data Migration Specification
>
> Source: KP Smart Tenant_Data Migration Specification_v0.2.xlsx
>
> Generated: 2026-02-04 14:19:18

---

## Summary Mapping

| Unnamed: 0 | Unnamed: 1 | 559 | 62 | 0 | 156 | 803 | 865 | Unnamed: 8 | Unnamed: 9 | Unnamed: 10 | 0.5723183338 | Unnamed: 12 | Unnamed: 13 | 0.1 | Unnamed: 15 | Unnamed: 16 | Unnamed: 17 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  |  | Ready | Not Ready | TBC | New | Initial | Total | Complete | Remark | ส่งวันที 30 ม.ค.  | 0.9538638897 |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  | ส่งวันที 06 ก.พ.  |  |  |  |  |  |  |  |
| No | Table | BE8 fields ready | BE8 fields not ready | BE8 fields TBC | BE8 fields New | BE8 fields ready | Total Fields | % BE8 fields ready | Remark | KP Confirm | % KP Complete | sheet_name | # KP mapping | %KP mapping  เมื่อเทียบกับ Total | PIC Mapping | PIC Query | Remark |
| 1 | Account (Tenant Profile) | 48 | 0 | 0 | 3 | 51 | 51 | 1 |  | 51 | 1 | 01_Account | 51 | 1 | Buay | SELECT  	krs.CON_CODE AS Concession,  	krs.SHOP_CODE AS "Tenant Code",  	krs.REGISTERED_NAME AS "Tenant Name",  	krs.SHOP_NAME_T AS "Tenant Name - TH", 	krs.SHOP_NAME_E AS "Tenant Name - EN", 	krs.SHORT_NAME AS "Short Name", 	krs.REG_DATE AS "Registration Date", 	krs.REG_COMM_NO AS "Registration No.", 	krs.REG_CAP_AMT AS "Registered Capital", 	krs.CURRENCY_CODE AS "Registered Currency", 	CASE  		WHEN krs.COMMERCIAL_FLAG = 1 THEN 'YES' 		ELSE 'NO' 	END AS Commercial, 	CASE  		WHEN krs.COMMERCIAL_FLAG = 0 THEN 'YES' 		ELSE 'NO' 	END AS Government, 	krs.REG_VAT_NO AS "Tax ID", 	krs.TEXT_BU_TYPE AS "Business Group", 	krs.BLL_SAP_CUSCODE AS "SAP Customer Code", 	CASE  		WHEN krs.CONTRACTOR_FLAG = 1 THEN 'Contractor' 		WHEN krs.TENANT_FLAG = 1 THEN 'Tenant' 		WHEN krs.KPG_FLAG = 1 THEN 'King Power Group' 		WHEN krs.HAS_SALES_FLAG = 1 THEN 'Sales/Revenue' 		WHEN krs.OTH_CUST_FLAG = 1 THEN 'Other Customer' 	END AS "Accounting Information", 	TRIM( 	    NVL(krs.LOC_BUILDING, '') \|\| ' ' \|\| NVL(krs.LOC_VILLAGE, '') 	) AS "Building / Village", 	krs.LOC_ADDRESS_NO AS "Address No.", 	krs.LOC_SOI AS "Soi", 	krs.LOC_STREET AS "Street", 	krs.LOC_SUB_DISTRICT AS "Sub-District", 	krs.LOC_DISTRICT_CODE AS "District", 	krs.LOC_PROV_CODE AS "Province", 	krs.LOC_ZIPCODE AS "Zip Code", 	krs.LOC_PHONE_NO AS "Contact No.", 	krs.LOC_COUNTRY_CODE AS "Country", 	CASE  		WHEN krs.LOC_WEBSITE IS NOT NULL THEN krs.LOC_WEBSITE 		WHEN krs.LOC_WEBSITE_2 IS NOT NULL THEN krs.LOC_WEBSITE_2 		ELSE NULL 	END AS "Website", 	REGEXP_REPLACE( 	    TRIM( 	        NVL(krs.BLL_ADDRESS1, '') \|\| ' ' 	      \|\| NVL(krs.BLL_ADDRESS2, '') \|\| ' ' 	      \|\| NVL(krs.BLL_CITY, '')    \|\| ' ' 	      \|\| NVL(krs.BLL_ZIP, '')     \|\| ' ' 	      \|\| NVL(krs.BLL_COUNTRY_CODE,'') \|\| ' ' 	      \|\| NVL(krs.BLL_TEL, '')     \|\| ' ' 	      \|\| NVL(krs.BLL_FAX, '') 	    ), 	    ' +', ' '   	) AS "Billing Address",   	TRIM(         REGEXP_REPLACE(             krs.REC_BUILDING \|\| ' ' \|\|             krs.REC_VILLAGE \|\| ' ' \|\|             krs.REC_ADDRESS_NO \|\| ' ' \|\|             krs.REC_SOI \|\| ' ' \|\|             krs.REC_STREET \|\| ' ' \|\|             krs.REC_SUB_DISTRICT \|\| ' ' \|\|             krs.REC_PROV_CODE \|\| ' ' \|\|             krs.REC_DISTRICT_CODE \|\| ' ' \|\|             krs.REC_ZIPCODE \|\| ' ' \|\|             krs.REC_PHONE_NO \|\| ' ' \|\|             krs.REC_FAX_NO \|\| ' ' \|\|             krs.REC_COUNTRY_CODE,             '\s+',             ' '         )     ) AS "Document Address",     krs.STATUS AS "Tenant Status",     krs.TEXT_BU_TYPE AS "KPT Shop Type (King Power Tax Fee)",     CASE      	WHEN UPPER(krs.SEND_SALES_TEXT_TYPE) = 'SUM' THEN 'Tenant Confirm'     	WHEN UPPER(krs.SEND_SALES_TEXT_TYPE) = 'DETAIL' THEN 'REV Confirm'     	WHEN UPPER(krs.SEND_SALES_TEXT_TYPE) = 'NONE' THEN 'No'     END AS "Require Sales Confirmation" FROM KPS_R_SHOP krs; | *** ยังไม่เสร็จ เดี๋ยวรอคุยเรื่อง field กับพี่โยเพิ่มเติม |
| 2 | Concession | 29 | 0 | 0 | 35 | 64 | 64 | 1 |  | 64 | 1 | 02_Concession | 64 | 1 | Buay | SELECT     c.CON_CODE AS "Concession No.",     'Airport' AS "Concession Type",     c.CON_DESC AS "Description",     c.CON_LNAME AS "ชื่อผู้ให้สัมปทาน",     c.CON_SNAME AS "ชื่อย่อผู้ให้สัมปทาน",     c.RCON_LNAME AS "ชื่อผู้รับสัมปทาน",     c.RCON_SNAME AS "ชื่อย่อผู้รับสัมปทาน",     c.LOCATION AS "Location",     c.BEGIN_DATE AS "Start Date",     c.END_DATE AS "End Date",     CASE WHEN c.ACTIVE_FLAG = 1 THEN 'Active' ELSE 'Inactive' END AS "Concession Status",     '' AS "รอบปีงบประมาณ (From)",     '' AS "รอบปีงบประมาณ (To)",     '' AS "การปรับส่วนแบ่งรายได้ตามมาตรการช่วยเหลือตามที่ ทอท. กำหนด (ผู้โดยสารจะมากกว่าปี 2562)",     c.CON_TOTAL_AREA AS "Total Area",     c.CON_COMM_AREA AS "Commercial Area",     c.CON_ME_AREA AS "M&E Area",     c.CON_STORE_AREA AS "Store Area",     '' AS "Other Area",     c.ACT_TOT_AREA AS "Total Area (Actual)",     c.ACT_COMM_AREA AS "Commercial Area (Actual)",     c.ACT_ME_AREA AS "M&E Area (Actual)",     c.ACT_STORE_AREA AS "Store Area (Actual)",     '' AS "Other Area (Actual)",     '' AS "Total Area (Occupied)",     '' AS "Commercial Area (Occupied)",     '' AS "M&E Area (Occupied)",     '' AS "Store Area (Occupied)",     '' AS "Other Area (Occupied)",     '' AS "Total Area (Vacant)",     '' AS "Commercial Area (Vacant)",     '' AS "M&E Area (Vacant)",     '' AS "Store Area (Vacant)",     '' AS "Other Area (Vacant)",     c.SAP_COMPANY_CODE AS "SAP Company Code",     c.SAP_BUSINESS_PLACE AS "SAP Business Place",     c.SAP_BUSINESS_AREA AS "SAP Business Area",     c.SAP_COST_CENTER AS "SAP Cost Center",     c.SAP_FUNDS_CENTER AS "SAP Funds Center",     c.SAP_TEXT_AIRPORT AS "SAP Airport",     '' AS "Concession Contract No.",     '' AS "Contract Date",     '' AS "Minimum Guarantee",     '' AS "Upfront Amount",     '' AS "Reference Year",     '' AS "- Number of Installment",     '' AS "- Total Revenue Sharing",     '' AS "- Due Date",     '' AS "- Amount",     '' AS "Revenue Sharing - % per month",     '' AS "- Contract Start Date",     '' AS "- Contract End Date",     '' AS "- No. of Day(s)",     '' AS "- Minimum Guarantee (per day)",     '' AS "- Total Area",     '' AS "- Commercial Area",     '' AS "- M&E Area",     '' AS "- Other Area",     '' AS "- Cost per SQM",     '' AS "- Passenger Growth (%)",     '' AS "- Inflation Rate (%)",     '' AS "- Remark" FROM KPS_R_CONCESS c; |  |
| 4 | Shop Brand | 6 | 0 | 0 | 0 | 6 | 6 | 1 | BE8 ตัดเหลือ 6 records | 6 | 1 | 04_Shop Brand | 6 | 1 | Buay | SELECT  	SHOP_CODE AS "Tenant Code", 	SHPBND_CODE, 	SHPBND_NAME_T, 	SHPBND_NAME_E, 	STATUS FROM  	KPS_R_SHOP_BRAND krsb  |  |
| 5 | Shop Branch | 14 | 0 | 0 | 9 | 23 | 23 | 1 |  | 19 | 0.8260869565 | 05_Shop Branch | 23 | 1 | Buay | SELECT     b.BRANCH_NO AS "Shop Branch No.",     b.BRANCH_CODE AS "Shop Branch Code",     b.BRANCH_NAME_T AS "Shop Branch Name - TH",     b.BRANCH_NAME_E AS "Shop Branch Name - EN",     b.BRANCH_SHOTNAME AS "Shop Branch Short Name",     c.AOT_CATE_DESC AS "Shop Category (AOT)",     '' AS "Service Time (Start)",     '' AS "Service Time (End)",     b.SHOP_UNIT AS "Unit No.",     u.AOTTOTAL_AREA AS "Total Area",     b.COMM_AREA AS "Commercial Area",     b.STORE_AREA AS "Store Area",     b.MNE_AREA AS "M&E Area",     b.OTH_AREA AS "Other Area",     p.POS_NO AS "POS No.",     CASE WHEN p.STATUS = 1 THEN 'Active' ELSE 'Inactive' END AS "POS Status",     '' AS "Date Period (From)",     '' AS "Date Period (To)",     '' AS "Shop Holiday/Event - Reason",     cp.CONT_NAME AS "Name-Surname",     cp.CONT_POST AS "Position",     cp.CONT_PHONE_NO AS "Mobile No.",     cp.CONT_EMAIL_ADDR AS "Email Address" FROM KPS_R_BRANCH b LEFT JOIN KPS_R_AOT_SHOP_CATE c ON b.AOT_CATE_CODE = c.AOT_CATE_CODE LEFT JOIN KPS_R_SHOPUNIT u ON b.CON_CODE = u.CON_CODE AND b.SHOP_UNIT = u.SHOP_UNIT LEFT JOIN KPS_R_POS p ON b.CON_CODE = p.CON_CODE AND b.SHOP_CODE = p.SHOP_CODE AND b.BRANCH_CODE = p.BRANCH_CODE LEFT JOIN KPS_R_SHOP_CONT_PER cp ON b.CON_CODE = cp.CON_CODE AND b.SHOP_CODE = cp.SHOP_CODE; |  |
| 6 | Contract | 79 | 0 | 0 | 64 | 143 | 143 | 1 |  | 103 | 0.7202797203 | 06_Contract | 110 | 0.7692307692 | Buay |  |  |
| 7 | Sub-Contract | 9 | 0 | 0 | 39 | 48 | 48 | 1 |  | 0 | 0 | 07_Sub Contract | 48 | 1 | Buay |  |  |
| 8 | Contact Point | 10 | 0 | 0 | 0 | 10 | 10 | 1 |  | 9 | 0.9 | 08_Contact | 10 | 1 | Buay | SELECT  	 krscp.CON_CODE \|\| ' : ' \|\| krc.CON_LNAME AS "Concession", 	 krs.SHOP_NAME_E AS "Company Name", 	 krs.SHORT_NAME AS "Shop Name", 	 krscp.CONT_NAME AS "Contact Person", 	 KRSCP.CONT_PHONE_NO AS "Mobile", 	 KRSCP.CONT_EMAIL_ADDR AS "E-mail", 	 KRSCP.CONT_POST AS "Job Title"	  FROM KPS_R_SHOP_CONT_PER krscp  JOIN KPS_R_CONCESS krc ON krscp.CON_CODE = krc.CON_CODE  JOIN KPS_R_SHOP krs ON krscp.SHOP_CODE = krs.SHOP_CODE | เหลือ Unit No., Created Date  Created Date Q: relationship ระหว่าง KPS_R_SHOP_CONT_PER  ไปหา KPS_CAC_INSPECTION_INFORM_SEND ยังไง |
| 10 | Reference Product | 24 | 0 | 0 | 0 | 24 | 24 | 1 |  | 0 | 0 | 10_Reference Products | 24 | 1 | Buay, P | SELECT     src.REF_SRC_NAME AS "Reference Product Source",     cat.STD_CATE_DESC AS "Product Type",     m.STD_CATE_CODE AS "Product Category Code",     sub1.PROD_SUBCAT1_DESC AS "Product Sub Type",     sub2.PROD_SUBCAT2_DESC_EN AS "Product Category Name - EN",     sub2.PROD_SUBCAT2_DESC AS "Product Category Name - TH",     sub2.STATUS AS "Product Status",     '' AS "Attachment/Reference",     '' AS "Product Name - TH",     m.PROD_SERV_NAME AS "Product Name - EN",     shop.SHORT_NAME AS "Reference Source",      m.REQ_PRICE_EXC_VAT AS "Sale Price (Exclude VAT)",     m.VAT_RATE AS "VAT",     m.REQ_PRICE_INC_VAT AS "Sale Price (Include VAT)",     '' AS "Survey Date",     m.REF_DATE AS "Reference Date for Approved Product" FROM KPS_T_REQPROD_MD_ORG m LEFT JOIN KPS_R_SHOP shop ON m.CON_CODE = shop.CON_CODE AND m.SHOP_CODE = shop.SHOP_CODE LEFT JOIN KPS_R_PROD_REF_SRC src ON 1=1 LEFT JOIN KPS_R_CATEGORY cat ON SUBSTR(m.STD_CATE_CODE, 1, 1) = cat.PROD_CATE_CODE LEFT JOIN KPS_R_PROD_SUBCATE1 sub1 ON      SUBSTR(m.STD_CATE_CODE, 1, 1) = sub1.PROD_CATE_CODE      AND SUBSTR(m.STD_CATE_CODE, 2, 1) = sub1.PROD_SUBCAT1_CODE LEFT JOIN KPS_R_PROD_SUBCATE2 sub2 ON      SUBSTR(m.STD_CATE_CODE, 1, 1) = sub2.PROD_CATE_CODE      AND SUBSTR(m.STD_CATE_CODE, 2, 1) = sub2.PROD_SUBCAT1_CODE      AND SUBSTR(m.STD_CATE_CODE, 3, 2) = sub2.PROD_SUBCAT2_CODE; |  |
| 11 | Product Category | 5 | 0 | 0 | 0 | 5 | 5 | 1 | ไม่พบฟิวด์ตั้งต้น BE8 เพิ่ม 20-Jan-26 | 0 | 0 | 11_Product Category | 5 | 1 | Got |  |  |
| 12 | Product & Price  - Category Product  - Unit Product | 41 | 0 | 0 | 5 | 46 | 46 | 1 | 2026-01-22 00:00:00 | 46 | 1 | 12_Product & Price | 46 | 1 | Got |  |  |
| 13 | Shop Inspection | 43 | 0 | 0 | 0 | 43 | 43 | 1 |  | 0 | 0 | 13_Shop Inspection | 36 | 0.8372093023 | Buay |  |  |
| 14 | Form Template  (การตรวจร้าน) | 5 | 0 | 0 | 0 | 5 | 5 | 1 |  | 5 | 1 | 14_Form Template(New) | 5 | 1 | Got |  |  |
| 17 | Unit (Space) | 54 | 0 | 0 | 1 | 55 | 55 | 1 |  | 55 | 1 | 17_Units | 55 | 1 | Got |  |  |
| 19 | POS | 22 | 0 | 0 | 0 | 22 | 22 | 1 |  | 22 | 1 | 19_POS | 22 | 1 | P | SELECT     con.CON_LNAME AS "Concession No",     pos.SHOP_CODE AS "Tenant",     shop.SHOP_NAME_E AS "Tenant Name",     pos.BRANCH_CODE AS "Shop",     shop.SHORT_NAME AS "Shop Name",     branch.SHOP_UNIT AS "Unit No",     unit.SHOP_UNIT_NAME AS "Unit Shop Description",     '' AS "Contact First Name and Last Name",     pos.POS_NO AS "POS Registration No.",     hist.REVENUE_ID AS "Revenue ID",     hist.CPU_SERIAL_NO AS "CPU Serial No. (Temporary)",     pos.SDATE AS "Start Date",     pos.EDATE AS "End Date",     CASE WHEN pos.STATUS = 1 THEN 'Use' ELSE 'Cancel' END AS "Status",     '' AS "IP Address",     '' AS "Mac Address",     pos.POS_SUPPLIER_CODE AS "Supplier Code",     sup.NAME_E AS "Supplier Name",     hist.REMARK AS "Remark",     hist.SEQ_NO AS "Action",     '' AS "Attachment - ภพ.06",     '' AS "Attachment - คก.2" FROM KPS_R_POS pos LEFT JOIN KPS_R_CONCESS con ON pos.CON_CODE = con.CON_CODE LEFT JOIN KPS_R_SHOP shop ON pos.CON_CODE = shop.CON_CODE AND pos.SHOP_CODE = shop.SHOP_CODE LEFT JOIN KPS_R_BRANCH branch ON pos.CON_CODE = branch.CON_CODE AND pos.SHOP_CODE = branch.SHOP_CODE AND pos.BRANCH_CODE = branch.BRANCH_CODE LEFT JOIN KPS_R_SHOPUNIT unit ON unit.CON_CODE = pos.CON_CODE LEFT JOIN KPS_T_POS_REGISTER_HISTORY hist ON pos.POS_NO = hist.POS_NO LEFT JOIN KPS_R_POS_SUPPLIER sup ON pos.POS_SUPPLIER_CODE = sup.POS_SUPPLIER_CODE; |  |
| 20 | Sales Transaction | 10 | 62 | 0 | 0 | 10 | 72 | 0.1388888889 |  | 0 | 0 | 20_Sales Transaction (Report) | 72 | 1 | Got |  |  |
| 21 | Supplier (Contact Point) | 4 | 0 | 0 | 0 | 4 | 4 | 1 | ไม่พบฟิวด์ตั้งต้น - BE8 เพิ่มฟิลล์ 23-Jan-26 | 4 | 1 | 21_Supplier Contact | 4 | 1 | P | SELECT         P.NAME_E AS "Supplier Name",         S.NAMES AS "Contact Person",         S.MOBILE AS "Mobile",         S.EMAIL AS "E-mail" FROM KPS_R_POS_SUPPLIER P JOIN KPS_R_EMAIL_SUPPLIER S ON P.POS_SUPPLIER_CODE = S.POS_SUPPLIER_CODE |  |
| 22 | Invoice | 138 | 0 | 0 | 0 | 138 | 138 | 1 | ไม่พบฟิวด์ตั้งต้น - BE8 เพิ่มฟิลล์ 22-Jan-26 | 0 | 0 | 22_Invoice | 45 | 0.3260869565 | Buay | SELECT     inv.PREINV_NO AS "Invoice Name",     '' AS "Status",     inv.PREINV_TYPE AS "Invoice Type",     inv.CON_CODE AS "Concession",     inv.CONT_NO AS "Contract",     inv.SAP_UNIT_NO AS "Unit No.",     inv.SAP_COMP_CODE AS "Company Code",     -- inv.CON_LNAME AS "Company Name",     -- inv.SHPBND_CODE AS "Brand Code",     -- inv.SHPBND_NAME_E AS "Shop Brand",     '' AS "Opportunity",     inv.ACCPERIOD_CODE \|\| '/' \|\| inv.PROCPERIOD_CODE AS "Monthly/Year",     rent.RENTAL_AMT AS "Monthly Rental Fee",     rent.MIN_MONTH_RATE AS "Minimum Guarantee",     rent.RATE_PER_MONTH AS "%Revenue Sharing",     rent.RENTAL_PER_AMT AS "Revenue Sharing",     inv.TOTAL_AMT AS "Amount",     inv.VAT_AMT AS "VAT Amount (Auto Cal.)",     '' AS "Total (Auto Cal.)",     inv.PREINV_DATE AS "Doc Date",     inv.DUE_DATE AS "Due Date",     rent.PROPERTYTAX_AMT AS "Property and Land Tax",     inv.REMARK AS "Remark",     rent.TOTAL_AMT AS "Total (excl. VAT)",     inv.SAP_UNIT_NO AS "Assignment",     rent.SERVICEFEE_AMT AS "Service Fee",     inv.TOTAL_AMT AS "Grand Total (excl. VAT)",     inv.VAT_RATE AS "Value Added Tax (VAT)",     inv.VAT_AMT AS "Total (VAT)",     inv.GRAND_TOTAL_AMT AS "Grand Total (VAT)",     rev.WT_RATE AS "Withholding Tax (W/T)",     rev.WT_AMT AS "Withholding Tax Amount (Auto Cal.)",     inv.NETTOTAL_AMT AS "Net Payment",     inv.NETTOTAL_AMT AS "Net Total (Auto Cal.)",     (SELECT SUM(CHARGE_NONE_VATAMT) FROM KPS_T_PREINV_DETAIL d WHERE d.PREINV_NO = inv.PREINV_NO AND d.CHARGE_CODE = 'REV001') AS "W/O VAT Collateral Deposit",     (SELECT SUM(CHARGE_VATAMT) FROM KPS_T_PREINV_DETAIL d WHERE d.PREINV_NO = inv.PREINV_NO AND d.CHARGE_CODE = 'REV001') AS "VAT Collateral Deposit",     rev.MIN_GUA_AMT AS "Collateral Deposit",     (SELECT SUM(CHARGE_NONE_VATAMT) FROM KPS_T_PREINV_DETAIL d WHERE d.PREINV_NO = inv.PREINV_NO AND d.CHARGE_CODE = '0006') AS "W/O VAT Building Usage Fee Deposit",     (SELECT SUM(CHARGE_VATAMT) FROM KPS_T_PREINV_DETAIL d WHERE d.PREINV_NO = inv.PREINV_NO AND d.CHARGE_CODE = '0006') AS "VAT Building Usage Fee Deposit",     (SELECT SUM(TOTAL_CHARGE_AMT) FROM KPS_T_PREINV_DETAIL d WHERE d.PREINV_NO = inv.PREINV_NO AND d.CHARGE_CODE = '0006') AS "Building Usage Fee Deposit",     '' AS "Rental Deposit",     (SELECT MAX(CHARGE_CODE) FROM KPS_T_PREINV_DETAIL d WHERE d.PREINV_NO = inv.PREINV_NO AND d.CHARGE_CODE = '0006') AS "Property Tax (One-Time)",     (SELECT SUM(CHARGE_NONE_VATAMT) FROM KPS_T_PREINV_DETAIL d WHERE d.PREINV_NO = inv.PREINV_NO) AS "W/O VAT One-Time Payment",     (SELECT SUM(CHARGE_VATAMT) FROM KPS_T_PREINV_DETAIL d WHERE d.PREINV_NO = inv.PREINV_NO) AS "VAT One-Time Payment",     (SELECT SUM(TOTAL_CHARGE_AMT) FROM KPS_T_PREINV_DETAIL d WHERE d.PREINV_NO = inv.PREINV_NO) AS "One-Time Payment",     inv.INVOICE_NO AS "Invoice No.",     inv.REF_DOC_NO AS "Reference No.",     inv.INVOICE_DATE AS "Issue Date",     inv.SAP_DOC_NO AS "Document Link" FROM KPS_T_PREINV inv LEFT JOIN KPS_T_PREINV_RENTAL rent ON inv.PREINV_NO = rent.PREINV_NO LEFT JOIN KPS_T_PREINV_REVGUA rev ON inv.PREINV_NO = rev.PREINV_NO; | Company Name, Brand Code, Shop Brand ยังไม่มี |
| 23 | Promotion - Target Sales | 18 | 0 | 0 | 0 | 18 | 18 | 1 |  | 18 | 1 | 23_Promotion | 18 | 1 | P | SELECT     p.PRO_CODE AS "Promo Code",     p.PRO_DESC AS "Promo Description",     p.PRO_SDATE AS "Promo Start Date",     p.PRO_EDATE AS "Promo End Date",     p.PROOWNER_CODE AS "Promo Eligibility",     t.PROTYPE_DESC AS "Promo Type",     c.PROCATG_DESC AS "Promo Category",     p.CREATEDDATE AS "Created Date",     l.START_DATE AS "Start Date",     l.END_DATE AS "End Date",     l.LAUNCHNO AS "Promo Phase No.",     p.TARGET_DESC AS "Target Description",     p.TARGETAMT AS "Sales Target Amount",     p.TARGETPERTYPE AS "Per",     p.BUTGETAMT AS "Budget Amount",     l.MEMONO AS "Attach Memo",     CASE WHEN p.CANCELFLAG = 1 THEN 'Void' ELSE 'Normal' END AS "Promotion Status",     p.OBJECTIVE AS "Promotion Criteria" FROM KPS_R_PROMOTION p LEFT JOIN KPS_R_PROMOTION_TYPE t ON p.PROTYPE_CODE = t.PROTYPE_CODE LEFT JOIN KPS_R_PROMOTION_CATG c ON p.PROCATG_CODE = c.PROCATG_CODE LEFT JOIN KPS_R_PRO_LAUNCH l ON p.PRO_CODE = l.PRO_CODE; |  |
| 20 | Sales Transaction (Summary) | 81 | 0 | 0 | 0 | 81 | 81 | 1 | BE8 เพิ่งเพิ่มเข้ามา 20/01/2026 | 0 | 0 | 20_Sales Transaction (Summary) | 0 | 0 | P |  |  |
| 20 | Sales Transaction (Daily Sale File) | 7 | 0 | 0 | 0 | 7 | 7 | 1 | BE8 เพิ่งเพิ่มเข้ามา 30/01/2026 | 0 | 0 | 20_Sales Transaction (Daily Sale File) | 0 | 0 | P |  |  |
| 20 | Sales Transaction (Details)_1 | 42 | 0 | 0 | 0 | 42 | 42 | 1 | BE8 เพิ่งเพิ่มเข้ามา 30/01/2026 | 0 | 0 | 20_Sales Transaction (Details)_1 | 42 | 1 | P |  |  |
| 20 | Sales Transaction (Details)_2 | 126 | 0 | 0 | 0 | 126 | 126 | 1 | BE8 เพิ่งเพิ่มเข้ามา 30/01/2026 | 0 | 0 | 20_Sales Transaction (Details)_2 | 99 | 0.7857142857 | P |  |  |

---

## Screen

*No data available*

## Overview

| # | Data Name | BU Owner | Source | Table API | Description | Migration Criteria | Total Amount | Target Total Amount | Estimated Amount
(2023-2024) | Growth Rate
(2023-2024) | Transaction Amount | User/KP Feedback |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ตัวอย่าง | Data Name 1 | CAD |  |  |  | All (Active) |  |  | 1,000 Records | 17-19% | 10 record per month |  |
| ตัวอย่าง | Data Name 2 | CAD |  |  |  | ย้อนหลัง 2 ปี  (1/2025) |  |  | 1,000 Records | 8-10% | 5 records per day | เพิ่ม Data Name 2 ใช้สำหรับแสดงข้อมูลที่เกี่ยวข้องกับ Data Name 1 |
| 1 | Account (Tenant Profile) | CAD | Oracle | KPS_R_SHOP |  | All SVB (2020-2026)   DMK/HKT(2016-2026) |  | 10-Feb'26 | 104 records per year | 0.2857 | 72 records per year | ข้อมูลตั้งแต่วันที่ 01/01/2023 – 31/12/2024 |
|  |  | CAD | External | KPS_R_SHOP_COMMITTEE | Committee by shop |  |  |  | 1040 (104*10) records per year |  | 0 records per year |  |
|  |  | CAD |  | KPS_R_SHOP_CONT_PER | Contact Person |  |  |  |  |  | 0 records per year |  |
| 2 | Concession | CAD | Oracle | KPS_R_CONCESS |  | All (00-11) |  |  |  |  | 0 records per year |  |
| 3 | Category | CAD | Oracle | KPS_R_AOT_SHOP_CATE |  | All (Active) |  |  |  |  | 0 records per year |  |
|  |  | CAD |  | KPS_R_AOT_RENTAL_CAT |  |  |  |  |  |  | 0 records per year |  |
|  |  | CAD |  | KPS_R_AOT_RENTAL_TYPE |  |  |  |  |  |  | 0 records per year |  |
| 4 | Shop Brand | CAD | Oracle | KPS_R_SHOP_BRAND |  | All (Active) |  |  | 81 records per year | 0.3721 | 51 records per year |  |
|  |  | CAD |  | KPS_T_PROD_COMPARE |  |  |  | 10-Feb'26 | 153061 records per year | -0.1354 | 190901 records per year |  |
| 5 | Shop Branch | CAD | Oracle | KPS_R_BRANCH |  | All (Active) |  |  | 188 records per year | 0.156 | 152 records per year |  |
|  |  | CAD |  | KPS_T_CONT_SHOP_UNIT |  |  |  |  | 338 records per year | -0.1793 | 457 records per year |  |
|  |  | CAD |  | KPS_R_SHOPUNIT |  |  |  |  | 78 records per year | -0.5372 | 266 records per year |  |
|  |  | CAD |  | KPS_R_POS |  |  |  | 10-Feb'26 | 1202 records per year | 1.0791 | 428 records per year |   |
|  |  | CAD |  | KPS_R_SHOP_CONT_PER |  |  |  |  |  |  | 0 records per year |  |
| 6 | Contract | CAD | Oracle | KPS_T_AOT_CONTRACT |  | All Active -  Attachment Inactive - No Attachment |  |  | 3 records per year | 0 | 0 records per year |  |
|  |  | CAD |  | KPS_T_CONTRACT |  |  |  |  | 80 records per year | -0.2353 | 120 records per year |  |
|  |  | CAD |  | KPS_T_CONTRACT_REVISE (เก็บ History Contract Change)  |  |  |  |  | 80 records per year | -0.2353 | 120 records per year |  |
|  |  | CAD |  | KPS_R_PERIOD_CONT |  |  |  |  | 0 records per year | -1 | 30 records per year |  |
|  |  | CAD |  | KPS_T_CONT_SHOP_UNIT |  |  |  |  | 338 records per year | -0.1793 | 457 records per year |  |
|  |  | CAD |  | KPS_R_SHOPUNIT |  |  |  |  | 78 records per year | -0.5372 | 266 records per year |  |
| 7 | Sub-Contract | CAD | Oracle | KPS_T_CONT_SUB_CONT (อยู่ภายใต้สัญญาแม่ Contract) |  | All (Active) |  |  | 0 records per year | -0.5 | 2 records per year |  |
| 8 | Contact Point | CAD | Oracle | KPS_R_SHOP_CONT_PER |  | All (Active) |  |  |  |  | 0 records per year |  |
|  | Contact Point  - ร้องเรียน  - ตรวจร้าน  - ราคา | CAC | Oracle | KPS_CAC_INSPECTION_INFORM_SEND |  | All |  | 10-Feb'26 | 3854 records per year | 0.0922 | 3380 records per year |  |
|  | Contact Point | FAM | ไม่มีข้อมูลในระบบ TMS | KPS_R_SHOP_CONT_PER |  | All (Active) |  |  | 0 records | 0 | 0 record per month |  |
|  | Contact Point - ผู้ติดตาม Text File - ผู้ติดตามยอดขายวัน - ฝ่ายบัญชีของผู้ประกอบการ | REV |  | KPS_R_EMAIL_SUPPLIER |  | All (Active) |  |  | 18 records per year | 2 | 4 records per year |  |
|  |  | REV |  | KPS_R_EMAIL_TENANT |  | All (Active) |  |  | 399 records per year | -0.0579 | 436 records per year |  |
|  | Contact Point | MKA |  |  |  | All (Active) |  |  |  |  |  |  |
| 9 | Case (ทะเบียนคุมประวัติ) | CAD | Manual Excel |  |  | All (Active) |  |  |  |  |  |  |
|  | Case (ทะเบียนคุมประวัติ) | MKA | Manual Excel |  |  | ย้อนหลัง 2 ปี (1/2025) |  |  |  |  |  |  |
| 10 | Reference Product | CAC | Manual Excel | KPS_T_REQPROD_MD_ORG |  | All (Active) |  | 10-Feb'26 | 82430 records per year | -0.1561 | 106707 records per year |  |
| 11 | Product Category |  |  |  |  |  |  |  |  |  |  |  |
| 12 | Product & Price  - Category Product  - Unit Product | CAC |  | KPS_T_REQPROD_MD |  | All |  | 10-Feb'26 | 163819 records per year | -0.1208 | 199139 records per year |  |
|  |  | CAC |  | KPS_T_APPRV_M |  |  |  | 10-Feb'26 | 164093 records per year | -0.1144 | 197251 records per year |  |
| 13 | Shop Inspection | CAC |  | KPS_CAC_INSPECTION_FORM |  | ย้อนหลัง 2 ปี  (1/2025: เฉพาะเชิงพาณิชย์) |  |  | 1721 records per year | 0.3939 | 1060 records per year |  |
|  |  | CAC |  | KPS_CAC_INSPECTION_TOPIC_M |  |  |  |  | 5 records per year | 0.3333 | 4 records per year |  |
|  |  | CAC |  | KPS_CAC_INSPECTION_TOPIC_MD |  |  |  |  | 228 records per year | 5.1667 | 22 records per year |  |
|  |  | CAC |  | KPS_CAC_INSP_DOC_DETAIL |  |  |  |  | 28272 records per year | -0.1059 | 33496 records per year |  |
|  |  | CAC |  | KPS_CAC_INSPECTION_DOCUMENT |  |  |  |  | 3066 records per year | 0.088 | 2704 records per year |  |
|  |  | CAC |  | KPS_CAC_INSP_FORM_UNIT_M |  |  |  |  | 95 records per year | -0.2558 | 150 records per year |  |
|  |  | CAC |  | KPS_CAC_INSP_FORM_UNIT_MD |  |  |  |  | 149 records per year | -0.1802 | 202 records per year |  |
|  |  | CAC |  | KPS_CAC_INSPECTOR |  |  |  |  | 0 records per year | -1 | 0 records per year |  |
|  |  | CAC |  | KPS_CAC_INSPECTION_PERIOD |  |  |  |  |  |  | 0 records per year |  |
|  |  | CAC |  | KPS_R_SHOP |  |  |  |  | 104 records per year | 0.2857 | 72 records per year |  |
| 14 | Form Template  (การตรวจร้าน) | CAC |  | KPS_CAC_INSPECTION_TEMPLATE |  | All  *Recheck email from 11-Dec |  |  | 3158 records per year | 7.3778 | 211 records per year |  |
| 15 | Location | FAM | Oracle | KPS_R_LOCATION |  | All (Active) |  |  |  |  | 0 records per year |  |
|  |  | FAM | Oracle | KPS_R_BUILDING |  |  |  |  |  |  | 0 records per year |  |
|  |  | FAM | Oracle | KPS_R_ZONE |  |  |  |  |  |  | 0 records per year |  |
|  |  | FAM | Oracle | KPS_R_WING |  |  |  |  |  |  | 0 records per year |  |
|  |  | FAM | Oracle | KPS_R_LEVEL |  |  |  |  |  |  | 0 records per year |  |
|  |  | FAM | Oracle | KPS_R_AREA >> ไม่ได้อยู่ใต้อะไรเลย |  |  |  |  |  |  | 0 records per year |  |
| 16 | Floor | FAM | Oracle | KPS_R_LEVEL |  | All (Active) |  |  |  |  | 0 records per year |  |
| 17 | Unit (Space) | FAM | Oracle | KPS_R_SHOPUNIT |  | All  (ย้อนหลัง 2 ปี) |  |  | 78 records per year | -0.5372 | 266 records per year |  |
| 18 | Technical Provisions and others | FAM | Manual Excel |  |  | All (Active) |  |  |  |  |  |  |
|  | - Meter Mapping Master | FAM | Manual Excel | KPS_R_ELECTRIC | TMS Parameter | All (Active) |  |  | -  | -  | - |  |
|  |  | FAM | Manual Excel | KPS_R_WATER_METER |  | All (Active) |  |  | 0 records | 0 | 0 record per month |  |
|  | - Source Electrical Meter Reading Record | FAM | Manual Excel | KPS_R_POWER_METER |  | All (Active) |  |  | 0 records | 0 | 0 record per month |  |
|  |  | FAM | Manual Excel | KPS_T_POWER_USAGE |  | All (Active) |  |  | 0 records | 0 | 0 record per month |  |
|  |  | FAM | Manual Excel | KPS_T_POWER_USAGE_SHOPUNIT |  | All (Active) |  |  | 0 records | 0 | 0 record per month |  |
|  | - Electrical Meter Reading Record | FAM | Manual Excel | KPS_R_POWER_METER |  | All (Active) |  |  | 0 records | 0 | 0 record per month |  |
|  |  | FAM | Manual Excel | KPS_T_POWER_USAGE |  | All (Active) |  |  | 0 records | 0 | 0 record per month |  |
|  |  | FAM | Manual Excel | KPS_T_POWER_USAGE_SHOPUNIT |  | All (Active) |  |  | 0 records | 0 | 0 record per month |  |
|  | - Source Water Meter Reading Record | FAM | Manual Excel | KPS_R_WATER_METER |  | All (Active) |  |  | 0 records | 0 | 0 record per month |  |
|  |  | FAM | Manual Excel | KPS_T_WATER_USAGE |  | All (Active) |  |  | 0 records | 0 | 0 record per month |  |
|  |  | FAM | Manual Excel | KPS_T_WATER_USAGE_SHOPUNIT |  | All (Active) |  |  | 0 records | 0 | 0 record per month |  |
|  | - Water Meter Reading Record | FAM | Manual Excel | KPS_R_WATER_METER |  | All (Active) |  |  | 0 records | 0 | 0 record per month |  |
|  |  | FAM | Manual Excel | KPS_T_WATER_USAGE |  | All (Active) |  |  | 0 records | 0 | 0 record per month |  |
|  |  | FAM | Manual Excel | KPS_T_WATER_USAGE_SHOPUNIT |  | All (Active) |  |  | 0 records | 0 | 0 record per month |  |
| 19 | POS | REV |  | KPS_R_POS |  | All (Active) |  |  | 1202 records per year | 1.0791 | 428 records per year |  |
|  |  | REV |  | KPS_T_CONT_SHOP_UNIT |  | All (Active) |  |  | 338 records per year | -0.1793 | 457 records per year |  |
|  |  | REV |  | KPS_R_SHOP |  | All (Active) |  |  | 104 records per year | 0.2857 | 72 records per year |  |
|  |  | REV |  | KPS_R_SHOPUNIT |  | All (Active) |  |  | 78 records per year | -0.5372 | 266 records per year |  |
|  |  | REV |  | KPS_T_POS_REGISTER_HISTORY |  | All (Active) |  |  | 2158 records per year | 1.438 | 624 records per year |  |
|  |  | REV |  | KPS_R_POS_SUPPLIER |  | All (Active) |  |  | 2 records per year | -0.25 | 4 records per year |  |
| 20 | Sales Transaction | REV | Oracle, TextFile | KPS_T_SALES_M | Sales Transaction Details  - Sales Master/Header | เริ่มปี 2569 (Jan-Jun) หรือ เริ่มปี 2568 |  |  | 51127576 records per year | 0.2655 | 36164974 records per year |  |
|  |  | REV | Oracle, TextFile | KPS_T_SALES_MD | Sales Transaction Details  - Sales Details/Line Items | เริ่มปี 2569 (Jan-Jun) หรือ เริ่มปี 2568 |  |  | 121722301 records per year | 0.2568 | 86957568 records per year |  |
|  |  | REV | Oracle, TextFile | KPS_T_SALESPAY_MD | Sales Transaction Details - Sales Payment | เริ่มปี 2569 (Jan-Jun) หรือ เริ่มปี 2568 |  |  | 51702195 records per year | 0.2681 | 36461318 records per year |  |
|  |  | REV | Oracle, TextFile | KPS_T_SALESBANK_MD | Sales Transaction Details  - Bank Detail | เริ่มปี 2569 (Jan-Jun) หรือ เริ่มปี 2568 |  |  | 163641 records per year | -0.0019 | 164120 records per year |  |
|  |  | REV | Oracle, TextFile | KPS_WEB_SALES | Sales Transaction Summary | เริ่มปี 2569 (Jan-Jun) หรือ เริ่มปี 2568 |  |  | 16656 records per year | 0.1305 | 13882 records per year |  |
|  |  | REV | Oracle, TextFile | KPS_T_SALES_APPRV | Sales Transaction Summary | เริ่มปี 2569 (Jan-Jun) หรือ เริ่มปี 2568 |  |  | 56491 records per year | 0.1739 | 44560 records per year |  |
|  |  | REV | Oracle, TextFile | KPS_T_SALES_APPRV_DETAIL | Sales Transaction Summary | เริ่มปี 2569 (Jan-Jun) หรือ เริ่มปี 2568 |  |  | 229433 records per year | 0.184 | 178716 records per year |  |
| 21 | Supplier (Contact Point) | REV |  | KPS_R_POS_SUPPLIER |  | All (Active) |  |  | 2 records per year | -0.25 | 4 records per year |  |
|  |  | REV |  | KPS_R_EMAIL_SUPPLIER |  | All (Active) |  |  | 18 records per year | 2 | 4 records per year |  |
| 22 | Invoice | ACC | Oracle | KPS_T_PREINV |  | เริ่มปี 2569 (Jan-Jun)  *รวมรายละเอียด เช่น ค่าน้ำ ค่าไฟ ใบลดหนี้ และ ทั้งหมด |  |  | 9391 records per year | 0.3403 | 6118 records per year |  |
|  |  | ACC | Oracle | KPS_T_PREINV_DETAIL |  | เริ่มปี 2569 (Jan-Jun)  *รวมรายละเอียด เช่น ค่าน้ำ ค่าไฟ ใบลดหนี้ และ ทั้งหมด |  |  | 9391 records per year | 0.3403 | 6118 records per year |  |
|  |  | ACC | Oracle | KPS_T_PREINV_MIN |  | เริ่มปี 2569 (Jan-Jun)  *รวมรายละเอียด เช่น ค่าน้ำ ค่าไฟ ใบลดหนี้ และ ทั้งหมด |  |  | 5018 records per year | 0.3919 | 3098 records per year |  |
|  |  | ACC | Oracle | KPS_T_PREINV_REVGUA |  | เริ่มปี 2569 (Jan-Jun)  *รวมรายละเอียด เช่น ค่าน้ำ ค่าไฟ ใบลดหนี้ และ ทั้งหมด |  |  | 4387 records per year | 0.2896 | 3020 records per year |  |
|  |  | ACC | Oracle | KPS_T_PREINV_REVSALES_D |  | เริ่มปี 2569 (Jan-Jun)  *รวมรายละเอียด เช่น ค่าน้ำ ค่าไฟ ใบลดหนี้ และ ทั้งหมด |  |  | 189097 records per year | 0.1393 | 155830 records per year |  |
|  |  | ACC | Oracle | KPS_T_PREINV_REVSALES_M |  | เริ่มปี 2569 (Jan-Jun)  *รวมรายละเอียด เช่น ค่าน้ำ ค่าไฟ ใบลดหนี้ และ ทั้งหมด |  |  | 4400 records per year | 0.2709 | 3093 records per year |  |
| 23 | Promotion - Target Sales | MKA |  | KPS_R_PROMOTION |  | All (Active) |  | 10-Feb'26 | 225 records per year | 0.1093 | 193 records per year |  |
|  |  |  |  | KPS_R_PROMOTION_TYPE |  |  |  | 10-Feb'26 |  |  | 0 records per year |  |
|  |  |  |  | KPS_R_PROMOTION_OWNER |  |  |  | 10-Feb'26 |  |  | 0 records per year |  |
|  |  |  |  | KPS_R_PROMOTION_CATG |  |  |  | 10-Feb'26 |  |  | 0 records per year |  |
|  |  |  |  | KPS_R_PRO_LAUNCH |  |  |  | 10-Feb'26 | 202 records per year | 0.0615 | 184 records per year |  |
|  |  |  |  | KPS_R_PRO_SHOP |  |  |  | 10-Feb'26 | 353 records per year | 0.0028 | 352 records per year |  |
|  |  |  |  | KPS_R_PRO_SHOPBRANCH |  |  |  | 10-Feb'26 | 4502 records per year | 0.5277 | 2438 records per year |  |
|  | Product & Price (Product Promotion) | MKA |  | KPS_T_APPRV_M |  | All  (Approved, Pending) |  | 10-Feb'26 | 164093 records per year | -0.1144 | 197251 records per year |  |
| 24 | Airline | MKA |  | KPS_R_AIRLINE |  | All  (Active, Inactive, Expired, Suspended) |  |  |  |  | 0 records per year |  |
| 25 | Flight Delay Contract | MKA |  | KPS_R_FLIGHT |  | All (Active) |  |  |  |  |  |  |
| 26 | Actual Passenger |  |  |  |  |  |  |  |  |  |  |  |
| 27 | Target Passenger |  |  |  |  |  |  |  |  |  |  |  |
| 28 | Actual Nationality |  |  |  |  |  |  |  |  |  |  |  |
| 29 | By Concourse |  |  |  |  |  |  |  |  |  |  |  |
| 30 | Holiday |  |  |  |  |  |  |  |  |  |  |  |
| 31 | Master Table Nation |  |  |  |  |  |  |  |  |  |  |  |
| 32 | Master Table By Con. |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  | KPS_T_REQPROD_MD |  |  | ? |  | 163819 records per year | -0.1208 | 199139 records per year |  |
|  |  |  |  | KPS_T_PROD_COMPARE |  |  | ? |  | 153061 records per year | -0.1354 | 190901 records per year |  |
|  |  |  |  | KPS_T_PROD_CATE_MPP |  |  | ? |  | 62691 records per year | -0.0532 | 68079 records per year |  |

---

## SUM

| # | Data Name | BU Owner | Source | Type | Is Ready for Mapping
(Yes/No) | Plan Target Date
(Ready for Mapping) 
ใส่เพื่อให้พี่เก่ง Priority Table ได้ | Target Date 
(Mapping Complete) | Target Date
(Delivery Template) | Status | Next Action | Note | BE8 Owner | Core System Info. | BU Owner.1 | Data Name.1 | SFDC Object | Sample Data | Note.1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1.0 | Account (Tenant Profile) | CAD | Oracle | Master | Yes | 23-Jan'26 | 6-Feb'26 |  | KP Complete |  |  |  | Concession | CAD | 2. Concession | TMS_Concession | DMK, SVB, HKT |  |
| 2.0 | Concession | CAD | Oracle | Master | Yes | 23-Jan'26 | 6-Feb'26 |  | KP Complete |  |  |  | Concession Contract | CAD | 6. Contract |  |  | Q: แตกต่างจาก Tenant Contract อย่างไร |
| 3.0 | Shop Category | CAD |  |  |  |  |  |  | Cancelled | - ย้ายไปอยู่ใน Account - BE8 Reconfirm field ที่เหลือ with K'Mue; Space Owner, AOT Rental Type, Space Usage Type |  |  | Tenant Profile | CAD | 1. Account | Account | After You Public Company Limited - SVB |  |
| 4.0 | Shop Brand | CAD | Oracle | Master | Yes | 23-Jan'26 | 30-Jan'26 |  | KP Complete |  |  |  | Shop Branch | CAD | 5. Shop Branch | TMS_Shop_Branch__c |  |  |
| 5.0 | Shop Branch | CAD | Oracle | Operational | Yes | 30-Jan'26 | 6-Feb'26 |  | Pending KP |  |  | Ton | Shop Brand | CAD | 4. Shop Brand | TMS_Shop_Brand__c | ลูกก๊อ (Luggaw), After You |  |
| 6.0 | Contract | CAD | Oracle | Operational | Yes | 30-Jan'26 | 6-Feb'26 |  | Pending KP |  | BE8 Recheck "Tenant Contract Protocol" | Ton | Tenant Service Records - ทะเบียนคุมประวัติ | CAD | 9. Case | TMS_Case__c |  |  |
| 7.0 | Sub-Contract | CAD | Oracle | Operational | Yes | 30-Jan'26 | 6-Feb'26 |  | Pending KP |  |  | Ton | Tenant Promotion | CAD | 23. Promotion | TMS_Promotion__c TMS_Promotion_Member__c |  | Q: แตกต่างจาก Promotion อย่างไร และมันคือ Product Promotion หรือไม่ |
| 8.0 | Contact | CAD | Oracle | Master | Yes | 23-Jan'26 | 6-Feb'26 |  | KP Complete |  | External ID = Concession+LName  |  | Tennant Daily Revenue | CAD |  | TMS_Daily_Sales_File__c |  | Q: Obj. อะไร |
| 9.0 | Case (ทะเบียนคุมประวัติ) | CAD | Manual Excel | Operational |  | 30-Jan'26 | 6-Feb'26 |  | Finalize with User |  |  | Ton | Tenant Contract | CAD | 6. Contract |  |  |  |
| 10.0 | Reference Product | CAC | Manual Excel | Master |  |  |  |  | Finalize with User |  | BE8 ทำ master แล้วต้องให้ทาง cac ช่วย map ให้ ตาม salesforce id ของ TMS เดิมมันฝังอยู่ใน Product เลยครับ มาพร้อมกับ Text File จาก ผปก. แต่ของใหม่ เราจะต้องทำให้ Maintain แยก เป็น Master Ref ไปเลย เพื่อให้เค้าดึงมาใช้ใหม่ได้ |  | Tenant Contract Protocol | CAD | 6. Contract |  |  |  |
| 11.0 | Product Category | CAC |  |  |  |  |  |  | Cancelled | ย้ายไปรวมอยู่ใน Product |  |  | Tenant Invoice | CAD | 22. Invoice | TMS_Invoice__c |  | แล้ว invocie ของ REV คืออะไร? |
| 12.0 | Product & Price  - Category Product  - Unit Product | CAC, MKA | Oracle | Master (for POC) | Yes | 23-Jan'26 | 6-Feb'26 |  | KP Complete |  |  |  | Sub Contract | CAD | 7. Sub-Contract |  |  |  |
| 13.0 | Shop Inspection | CAC | Oracle | Operational | Yes | 30-Jan'26 | 6-Feb'26 |  | Pending KP |  |  | Ta | Tenant Products | CAC | 12. Product & Price | Product2 |  |  |
| 14.0 | Form Template  (การตรวจร้าน) | CAC | Oracle | Master | Yes | 23-Jan'26 | 6-Feb'26 |  | KP Complete | BE8 Reconfirm with KP-IT สำหรับข้อมูลว่าครบหรือไม่ เช่น Group Reason, Reason |  | Ta | Reference Product Master | CAC | 10. Reference Product | TMS_Reference_Product__c |  |  |
| 15.0 | Location | FAM |  |  |  |  |  |  | Cancelled | ย้ายไปรวมอยู่ใน Units |  |  | Shop Inspection | CAC | 13. Shop Inspection |  |  |  |
| 16.0 | Floor | FAM |  |  |  |  |  |  | Cancelled | ย้ายไปรวมอยู่ใน Units |  |  | Form Template | CAC | 14. Form Template |  | F&B Stall |  |
| 17.0 | Unit (Space) | FAM | Oracle | Master | Yes | 23-Jan'26 | 6-Feb'26 |  | KP Complete |  |  |  | Unit (Merge/Swap/Split) | FAM | 17. Unit | TMS_Unit__c TMS_UnitJunction__c | T1ME2-24 (2) |  |
| 18.0 | Technical Provisions and others | FAM | Manual Excel | Master |  |  |  |  | Pending BE8 | BE8 Reconfirm with KP-FAM เพื่อสร้าง field ตั้งต้น |  | Ta | Technical Provision | FAM | 18. Technical Provision and others |  |  |  |
| 19.0 | POS | REV | Oracle | Master | Yes | 23-Jan'26 | 30-Jan'26 |  | KP Complete | BE8 Reconfirm to remove field with KP for Attachment - ภพ.06, Attachment - คก.2 |  | P'Poel | Meter Mapping Master | FAM |  | TMS_Meter_Usage__c |  | การคำนวณค่ําใช้จ่ํายสําธํารณูปโภค (Consumption) |
| 20.0 | Sales Transaction - Sales Transaction (Summary) - Sales Transaction (Daily Sale File) - Sales Transaction (Details)_1 - Sales Transaction (Details)_2 | REV | Oracle | Operational | Yes | 30-Jan'26 | 6-Feb'26 |  | Pending KP | BE8 สร้าง field ตั้งต้น |  | P'Poel | Source Electrical Meter Reading Record | FAM |  |  |  | การคำนวณค่ําไฟ |
| 21.0 | Supplier (Contact Point) | REV | Oracle | Master | Yes |  |  |  | KP Complete |  |  |  | Electrical Meter Reading Record | FAM |  |  |  | ข้อมูลการจดมิเตอร์หน่วยกํารใช้ไฟฟ้ํา จําก SMEE (SmartEE) |
| 22.0 | Invoice | REV | Oracle | Operational | Yes | 30-Jan'26 | 6-Feb'26 |  | Pending KP |  |  | P'Poel | Source Water Meter Reading Record | FAM |  |  |  | การคำนวณค่ําน้ำ (Electrical Consumption) |
| 23.0 | Promotion - Target Sales | MKA | Oracle | Master | Yes | 23-Jan'26 | 6-Feb'26 |  | KP Complete |  |  |  | Water Meter Reading Record | FAM |  |  |  | ข้อมูลการจดมิเตอร์หน่วยกํารใช้น ้ําประปํา KPS |
| 24.0 | Airline | MKA | Manual Excel | Master | Yes | 23-Jan'26 |  |  | Finalize with User |  |  |  | POS Registration | REV | 19. POS | TMS_POS__c TMS_Mock_DMO_Summary_POS_Transaction__c |  |  |
| 25.0 | Flight Delay Contract | MKA | Manual Excel | Master | Yes | 23-Jan'26 |  |  | Finalize with User |  |  |  | Supplier Master | REV | 8. Contact | Contact |  | <TBD with Ton> |
| 26.0 | Actual Passenger | DAS | Manual Excel | Operational |  | 30-Jan'26 | 6-Feb'26 |  | Pending BE8 | BE8 สร้าง field ตั้งต้น |  | Ta | Tenant Daily Sales Transaction Header | REV | 20. Sales Transaction | TMS_Temp_Sales_Transaction__c TMS_Company_Summary_Sales_Trn__c  TMS_DMO_Sales_Transaction__c TMS_DMO_Sales_Transaction_Item__c |  |  |
| 27.0 | Target Passenger | DAS | Manual Excel | Operational |  | 30-Jan'26 | 6-Feb'26 |  | Pending BE8 | BE8 สร้าง field ตั้งต้น |  | Ta | Tenant Daily Sales Transaction Detail | REV | 20. Sales Transaction |  |  |  |
| 28.0 | Actual Nationality | DAS | Manual Excel | Operational |  | 30-Jan'26 | 6-Feb'26 |  | Pending BE8 | BE8 สร้าง field ตั้งต้น |  | Ta | Promotion - Tenant Registration - Airport Registration - Product Inclusion & Exclusion - Mechanics  | MKA | 23. Promotion | TMS_Promotion__c TMS_Promotion_Member__c |  | ระบบจะแสดงข้อมูล Promotion ที่มีกํารขออนุมัติจํากผู้ประกอบกํารภํายใต้สัมปทํานที่ระบุโดยผู้ใช้งํานสํามํารถดูข้อมูล Promotion รํายผู้ประกอบกําร รวมถึง Promotionอื่นๆทั้งหมดที่มีกํารขออนุมัติจํากกํารท ําข้อมูลของผู้ใช้งํานจํากระบบ Workflow |
| 29.0 | By Concourse | DAS | Manual Excel | Operational |  | 30-Jan'26 | 6-Feb'26 |  | Pending BE8 | BE8 สร้าง field ตั้งต้น |  | Ta | Flight Delay Contract | MKA | 25. Flight Delay Contract |  |  | การบันทึกสัญญา Flight Delay เป็นส่วนที่เปิดให้ผู้ใช้งําน สํามํารถบันทึกข้อมูลสัญญํา Flight Delay ที่มีกํารท ําไว้กับทําง ผู้ประกอบกําร(Tenant)และทํางสํายกํารบิน(Airline) ให้สํามํารถไปใช้สิทธิตําม promotion flight delay ที่ร้ํานค้ําต่ํางๆ ได้ |
| 30.0 | Holiday | DAS | Manual Excel | Master |  |  |  |  | Cancelled | BE8 Reconfirm with KP  - Who/How to maintain, frequency - Used for? |  |  | Airline Master | MKA | 24. Airline | TMS_Airline__c |  | เพื่อใช้เป็น master ในกํารอ้ํางอิงข้อมูลต่อฟังก์ชันกํารท ํางํานต่ํางๆ เช่น กํารสร้ําง Promotion กํารบันทึกสัญญํา Flight Delay |
| 31.0 | Master Table Nation | DAS | Manual Excel | Operational |  | 30-Jan'26 | 6-Feb'26 |  | Pending BE8 | BE8 สร้าง field ตั้งต้น |  | Ta | Media Check | MKA |  |  |  | เพื่อใช้เก็บเป็นข้อมูล log กํารตรวจรํายกําร media ที่มีกํารใช้งํานแต่ละพื้นที่ ของผู้ประกอบกําร โดยจะมีส่วนเชื่อมโยงกับกํารคิดค่ําไฟจํากไฟป้ํายmedia ที่เกิดขึ้น ของผู้ประกอบกําร |
| 32.0 | Master Table By Con. | DAS | Manual Excel | Operational |  | 30-Jan'26 | 6-Feb'26 |  | Pending BE8 | BE8 สร้าง field ตั้งต้น |  | Ta |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  | 10 |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  | 0.3125 |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | มิเตอร์น้ำไฟ? (AOT Meter ID vs KP Meter ID) |  |  |  |  |  | <Any To Be Confirm> ? |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | COUNTA of Type | Source |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | Type |  | Manual Excel | Oracle | Grand Total |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  | 0 |  |  | 0 |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | Master |  | 5 | 9 | 14 |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | Master (for POC) |  |  | 1 | 1 |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | Operational |  | 7 | 6 | 13 |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | Grand Total | 0 | 12 | 16 | 28 |  |  |  |  |  |  |  |  |  |  |  |

---

## 01_Account

| No. | SFDC Field Name (EN) | SFDC Field Name (TH) | Source Field API Name | Source Field Type | Source Field Length | VULLABLE (N=Required) | KP Table | KP Field Name | KP Field Type | KP Field Length | VULLABLE (N=Required).1 | Progress | Confirm | Type | Required | Sample Data | Description | Status | User/KP Feedback | Remark | Help Text | Track History | External ID | Encrypted | Page Layout | Length | SFDC Table | SFDC API Name | SFDC Type | Type.1 | Required.1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Tenant Profile |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 1 | Concession |  | CON_CODE |  | 2 | N | KPS_R_SHOP | CON_CODE | CHAR | 2 | N | Ready | Y | Text (100) | Yes | 09 | เลขที่รหัสสัมปทาน | Confirmed |  | - เลือกข้อมูลตามตัวเลือกที่กำหนด โดยเป็นข้อมูลจาก “การบันทึกข้อมูลสัมปทาน” (Concession) |  |  |  |  |  |  |  |  |  | Text (100) | Yes |
| 2 | Tenant Code |  | SHOP_CODE | VARCHAR2 | 20 | N | KPS_R_SHOP | SHOP_CODE | VARCHAR2 | 20 | N | Ready | Y | Text (100) | Yes | 0902029 | รหัสบริษัทผู้ประกอบการ | Confirmed |  | - ระบบสร้างให้อัตโนมัติเมื่อได้รับการอนุมัติจัดทำสัญญาครั้งแรก จากระบบ Workflow Logic: (Concession Code)(2 หลัก) + (Business Type)(2 หลัก) + (Tenant Running No.)(3 หลัก) |  |  |  |  |  |  | Company Code | TMS_Company_Code__c | Text (100) | Text (100) | Yes |
| 3 | Tenant Name |  | REGISTERED_NAME | VARCHAR2 | 200 |  | KPS_R_SHOP | REGISTERED_NAME | VARCHAR2 | 200 | Y | Ready | Y | Text (100) | Yes |  |  | Confirmed |  | - ความยาวสูงสุด 100 ตัวอักษร |  |  |  |  |  |  | Company Name | TMS_Company_Name__c | Text (100) | Text (100) | Yes |
| 4 | Tenant Name - TH |  | SHOP_NAME_T | VARCHAR2 | 200 |  | KPS_R_SHOP | SHOP_NAME_T | VARCHAR2 | 200 | Y | Ready | Y | Text (100) | Yes | บริษัท อิมเพรสซีฟ สุวรรณภูมิ จำกัด | ชื่อผู้ประกอบการภาษาไทย | Confirmed |  | " |  |  |  |  |  |  | Tenant Name - TH |  | Text (100) | Text (100) | Yes |
| 5 | Tenant Name - EN |  | SHOP_NAME_E | VARCHAR2 | 200 |  | KPS_R_SHOP | SHOP_NAME_E | VARCHAR2 | 200 | Y | Ready | Y | Text (100) | Yes | Impressive Suvarnabhumi Co., Ltd. | ชื่อผู้ประกอบการภาษาอังกฤษ | Confirmed |  | " |  |  |  |  |  |  | Tenant Name - EN | TMS_Tenant_Name_EN__c | Text (100) | Text (100) | Yes |
| 6 | Short Name |  | SHORT_NAME | VARCHAR2 | 50 |  | KPS_R_SHOP | SHORT_NAME | VARCHAR2 | 50 | Y | Ready | Y | Text (100) | Yes | Impressive Suvarnabhumi | ชื่อย่อผู้ประกอบการ | Confirmed |  | " |  |  |  |  |  |  | Short Name | TMS_Short_Name__c | Text (100) | Text (100) | Yes |
| 7 | Business Type |  |  |  |  |  | KPS_R_SHOP KPS_R_BRANCH KPS_R_SHOPUNIT KPS_R_AOT_SHOP_CATE | SHOP_CODE SHOP_UNIT RNTCAT_CODE AOT_CATE_DESC | VARCHAR2 VARCHAR2 VARCHAR2 VARCHAR2 | 20 15 5 200 | N Y Y N | Ready | Y | Picklist (Multi-Select) | Yes | 01 - F&B 02 - Service 03 - Retails 04 - Bank | ประเภทธุรกิจ | Confirmed |  | - เลือกข้อมูลตามตัวเลือกที่กำหนด - เลือกได้ 1 ตัวเลือก  |  |  |  |  |  |  | Business Type | TMS_Business_Type__c | Picklist (Multi-Select) | Picklist (Multi-Select) | Yes |
| 8 | Registration Date |  | REG_DATE | DATE | 7 |  | KPS_R_SHOP | REG_DATE | DATE | 7 | Y | Ready | Y | Date | Yes |  | วันที่จดทะเบียนผู้ประกอบการ | Confirmed |  |  |  |  |  |  |  |  | Registration Date | TMS_Registration_Date__c | Date | Date | Yes |
| 9 | Registration No. |  |  |  |  |  | KPS_R_SHOP | REG_COMM_NO | VARCHAR2 | 30 | Y | Ready | Y | Text (100) | Yes |  | เลขจดทะเบียนผู้ประกอบการ | Confirmed |  |  |  |  |  |  |  |  | Registration No. | TMS_Registration_No__c | Text (100) | Text (100) | Yes |
| 10 | Registered Capital |  |  |  |  |  | KPS_R_SHOP | REG_CAP_AMT | NUMBER | 15,2 | Y | Ready | Y | Number(16,2) | No |  | ทุนจดทะเบียน | Confirmed |  | - กรอกได้เฉพาะตัวเลขเท่านั้น - รูปแบบ: #,###,###.## บาท |  |  |  |  |  |  | Registered Capital | TMS_Registered_Capital__c | Number(16,2) | Number(16,2) | No |
| 11 | Registered Currency |  |  |  |  |  | KPS_R_SHOP | CURRENCY_CODE | VARCHAR2 | 5 | Y | Ready | Y |  | No |  | หน่วย | Confirmed |  | - เลือกข้อมูลตามตัวเลือกจาก Currency Master |  |  |  |  |  |  | Registered Currency | TMS_Registered_Currency__c | Text (100) |  | No |
| 12 | Commercial |  | COMMERCIAL_FLAG | NUMBER | 22 |  | KPS_R_SHOP | COMMERCIAL_FLAG (1 = Commercial, 0 = Government) | NUMBER | 1,0 | Y | Ready | Y | Checkbox | Yes | - Yes - No  | เป็น commercial หรือไม่ | Confirmed |  |  |  |  |  |  |  |  | Commercial | TMS_Commercial__c | Checkbox | Checkbox | Yes |
| 13 | Government |  | <New> |  |  |  | KPS_R_SHOP | COMMERCIAL_FLAG (1 = Commercial, 0 = Government) | NUMBER | 1,0 | Y | New | Y | Checkbox | Yes | - Yes - No  | เป็น government หรือไม่ | Confirmed |  |  |  |  |  |  |  |  | Government | TMS_Government__c | Checkbox | Checkbox | Yes |
| 14 | Tax ID |  |  |  |  |  | KPS_R_SHOP | REG_VAT_NO | VARCHAR2 | 30 | Y | Ready | Y | Number(13,0) | Yes |  | เลขประจำตัวผู้เสียภาษีอากร | Confirmed |  | - กรอกได้เฉพาะตัวเลขเท่านั้น - กรอกข้อมูลได้สูงสุด 13 หลัก  |  |  |  |  |  |  | Tax ID | TMS_Tax_ID__c | Number(13,0) | Number(13,0) | Yes |
| 15 | Business Group |  | <New> |  |  |  | KPS_R_SHOP | TEXT_BU_TYPE | VARCHAR2 | 20 | Y | New | Y | Picklist | Yes | - KPS - KPT - BU | ประเภท text file business group | Confirmed |  | - เลือกข้อมูลตามตัวเลือกที่กำหนด - ตัวอย่าง KPS => “Primo Food and Beverage” KPT => “King Power Tax Free Co.,Ltd.” BU => “Boots”  |  |  |  |  |  |  | Business Group | TMS_Business_Group__c | Picklist | Picklist | Yes |
| 16 | SAP Customer Code |  | BLL_SAP_CUSCODE | VARCHAR2 | 30 |  | KPS_R_SHOP | BLL_SAP_CUSCODE | VARCHAR2 | 30 | Y | Ready | Y | Text (100) | No | 2070346 | เลข Customer Code จากระบบ SAP | Confirmed |  | - เลข Customer Code ที่ได้รับกลับมาจาก SAP |  |  |  |  |  |  | SAP Customer Code | TMS_SAP_Customer_Code__c | Text (100) | Text (100) | No |
| 17 | Accounting Information |  | <New> |  |  |  | KPS_R_SHOP KPS_R_SHOP KPS_R_SHOP KPS_R_SHOP KPS_R_SHOP | CONTRACTOR_FLAG TENANT_FLAG OTH_CUST_FLAG KPG_FLAG HAS_SALES_FLAG | NUMBER NUMBER NUMBER NUMBER NUMBER | 1,0 1,0 1,0 1,0 1,0 | Y Y Y Y Y | New | Y | Picklist (Multi-Select) | No | - Contractor - Tenant - Other Customer - King Power Group - Sales/Revenue  | ข้อมูลบัญชีผู้ใช้งาน | Confirmed |  | - เลือกข้อมูลตามตัวเลือกที่กำหนด - เลือกได้มากกว่า 1 ตัวเลือก  |  |  |  |  |  |  | Accounting Information | TMS_Accounting_Information__c | Picklist (Multi-Select) | Picklist (Multi-Select) | No |
| 18 | AOT Shop Category |  |  |  |  |  | KPS_R_SHOP KPS_R_BRANCH KPS_R_AOT_SHOP_CATE | SHOP_CODE AOT_CATE_CODE AOT_CATE_DESC | VARCHAR2 CHAR VARCHAR2 | 20 4 200 | N N N | Ready | Y |  |  |  |  |  |  |  |  |  |  |  |  |  | AOT Shop Category |  |  |  |  |
| 19 | AOT Shop Sub-Category |  |  |  |  |  | ไม่มี |  |  |  |  | Ready | Y |  |  | - Office, LWC, Store, etc. |  |  |  |  |  |  |  |  |  |  | AOT Shop Sub-Category |  |  |  |  |
| 20 | Shop Cateogry |  |  |  |  |  | KPS_R_SHOP KPS_R_BRANCH KPS_R_AOT_SHOP_CATE | SHOP_CODE AOT_CATE_CODE AOT_CATE_DESC | VARCHAR2 CHAR VARCHAR2 | 20 4 200 | N N N | Ready | Y |  |  | ประเภทร้ํานค้ําของ AOT เช่น - Bank - Communication - F&B - Restaurant - Healthy - Entertainment - Others - Lounge - Travel |  |  |  |  |  |  |  |  |  |  | Shop Cateogry |  |  |  |  |
| Authorized Committee |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 21 | Name-Surname |  | COMM_NAME | VARCHAR2 | 50 |  | KPS_R_SHOP_COMMITTEE | COMM_NAME | VARCHAR2 | 50 | Y | Ready | Y | Text (255) |  |  |  | Confirmed |  |  |  |  |  |  |  |  | Name-Surname | TMS_Name_Surname__c | Text (255) | Text (255) |  |
| 22 | Position |  | COMM_POSITION | VARCHAR2 | 30 |  | KPS_R_SHOP_COMMITTEE | COMM_POSITION | VARCHAR2 | 30 | Y | Ready | Y | Text (255) |  |  |  | Confirmed |  |  |  |  |  |  |  |  | Position | TMS_Position__c | Text (255) | Text (255) |  |
| 23 | ID Card No. |  |  |  |  |  | KPS_R_SHOP_COMMITTEE | COMM_ID_NO | VARCHAR2 | 40 | Y | Ready | Y | Text (255) |  |  |  | Confirmed |  |  |  |  |  |  |  |  | ID Card No. | TMS_ID_Card_No__c | Text (255) | Text (255) |  |
| 24 | Mobile No. |  |  |  |  |  | ไม่มี |  |  |  |  | Ready | Y | Phone |  |  |  | Confirmed |  |  |  |  |  |  |  |  | Mobile | PersonMobilePhone | Phone | Phone |  |
| 25 | Email Address |  |  |  |  |  | ไม่มี |  |  |  |  | Ready | Y | Email |  |  |  | Confirmed |  |  |  |  |  |  |  |  | Email | PersonEmail | Email | Email |  |
| Location Address |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 26 | Building / Village |  | LOC_BUILDING LOC_VILLAGE | VARCHAR2 VARCHAR2 | 60 60 |  | KPS_R_SHOP KPS_R_SHOP | LOC_BUILDING LOC_VILLAGE | VARCHAR2 VARCHAR2 | 60 60 | Y Y | Ready | Y | Text (255) | Yes |  |  | Confirmed |  |  |  |  |  |  |  |  |  |  |  | Text (255) | Yes |
| 27 | Address No. |  | LOC_ADDRESS_NO | VARCHAR2 | 50 |  | KPS_R_SHOP | LOC_ADDRESS_NO | VARCHAR2 | 50 | Y | Ready | Y | Text (255) | Yes |  |  | Confirmed |  |  |  |  |  |  |  |  |  |  |  | Text (255) | Yes |
| 28 | Soi |  | LOC_SOI | VARCHAR2 | 50 |  | KPS_R_SHOP | LOC_SOI | VARCHAR2 | 50 | Y | Ready | Y | Text (255) | Yes |  |  | Confirmed |  |  |  |  |  |  |  |  |  |  |  | Text (255) | Yes |
| 29 | Street |  | LOC_STREET | VARCHAR2 | 50 |  | KPS_R_SHOP | LOC_STREET | VARCHAR2 | 50 | Y | Ready | Y | Text (255) | Yes |  |  | Confirmed |  |  |  |  |  |  |  |  |  |  |  | Text (255) | Yes |
| 30 | Sub-District |  | LOC_SUB_DISTRICT | VARCHAR2 | 50 |  | KPS_R_SHOP | LOC_SUB_DISTRICT | VARCHAR2 | 50 | Y | Ready | Y | Text (255) | Yes |  |  | Confirmed |  |  |  |  |  |  |  |  |  |  |  | Text (255) | Yes |
| 31 | District |  | LOC_DISTRICT_CODE | VARCHAR2 | 3 |  | KPS_R_SHOP | LOC_DISTRICT_CODE | VARCHAR2 | 3 | Y | Ready | Y | Text (255) | Yes |  |  | Confirmed |  |  |  |  |  |  |  |  |  |  |  | Text (255) | Yes |
| 32 | Province |  | LOC_PROV_CODE | VARCHAR2 | 2 |  | KPS_R_SHOP | LOC_PROV_CODE | VARCHAR2 | 2 | Y | Ready | Y | Text (255) | Yes |  |  | Confirmed |  |  |  |  |  |  |  |  |  |  |  | Text (255) | Yes |
| 33 | Zip Code |  | LOC_ZIPCODE | CHAR | 5 |  | KPS_R_SHOP | LOC_ZIPCODE | CHAR | 5 | Y | Ready | Y | Number(5,0) | Yes |  |  | Confirmed |  |  |  |  |  |  |  |  |  |  |  | Number(5,0) | Yes |
| 34 | Contact Channel |  |  |  |  |  | ไม่มี |  |  |  |  | Ready | Y | Picklist | Yes | 1. Primary Contact No. 2. Secondary Contact No. 3. Fax No. |  | Confirmed |  |  |  |  |  |  |  |  | Contact Channel | TMS_Contact_Channel__c | Picklist | Picklist | Yes |
| 35 | Contact No. |  | LOC_PHONE_NO | VARCHAR2 | 100 |  | KPS_R_SHOP | LOC_PHONE_NO | VARCHAR2 | 100 | Y | Ready | Y | Phone | Yes |  |  | Confirmed |  |  |  |  |  |  |  |  |  |  |  | Phone | Yes |
| 36 | Email Address |  |  |  |  |  | ไม่มี |  |  |  |  | Ready | Y | Email | Yes |  |  | Confirmed |  |  |  |  |  |  |  |  |  |  |  | Email | Yes |
| 37 | Country |  | LOC_COUNTRY_CODE | VARCHAR2 | 3 |  | KPS_R_SHOP | LOC_COUNTRY_CODE | VARCHAR2 | 3 | Y | Ready | Y | Text (255) | Yes |  |  | Confirmed |  |  |  |  |  |  |  |  |  |  |  | Text (255) | Yes |
| 38 | Website |  | LOC_WEBSITE LOC_WEBSITE_2 | VARCHAR2 VARCHAR2 | 50 50 |  | KPS_R_SHOP KPS_R_SHOP | LOC_WEBSITE LOC_WEBSITE_2 | VARCHAR2 VARCHAR2 | 50 50 | Y Y | Ready | Y | Text (255) | Yes | 1. Primary 2. Secondary |  | Confirmed |  |  |  |  |  |  |  |  | Website | Website | URL(255) | Text (255) | Yes |
| 39 | Billing Address |  | BLL_ADDRESS1 BLL_ADDRESS2 BLL_CITY BLL_ZIP BLL_COUNTRY_CODE BLL_TEL BLL_FAX | VARCHAR2 VARCHAR2 VARCHAR2 VARCHAR2 VARCHAR2 VARCHAR2 VARCHAR2 | 120 120 60 10 3 100 30 |  | KPS_R_SHOP KPS_R_SHOP KPS_R_SHOP KPS_R_SHOP KPS_R_SHOP KPS_R_SHOP KPS_R_SHOP | BLL_ADDRESS1 BLL_ADDRESS2 BLL_CITY BLL_ZIP BLL_COUNTRY_CODE BLL_TEL BLL_FAX | VARCHAR2 VARCHAR2 VARCHAR2 VARCHAR2 VARCHAR2 VARCHAR2 VARCHAR2 | 120 120 60 10 3 100 30 | Y Y Y Y Y Y Y | Ready | Y | Picklist | Yes | 1. ที่อยู่เดียวกันกับที่อยู่ปัจจุบัน 2. ที่อยู่เดียวกันกับที่อยู่จัดส่งเอกสาร | ที่อยู่วางบิล  | Confirmed |  | - กรอกข้อมูลที่อยู่ หรือเลือกข้อมูลจากตัวเลือก |  |  |  |  |  |  |  |  |  | Picklist | Yes |
| 40 | Document Address |  |  |  |  |  | KPS_R_SHOP KPS_R_SHOP KPS_R_SHOP KPS_R_SHOP KPS_R_SHOP KPS_R_SHOP KPS_R_SHOP KPS_R_SHOP KPS_R_SHOP KPS_R_SHOP KPS_R_SHOP KPS_R_SHOP | REC_BUILDING REC_VILLAGE REC_ADDRESS_NO REC_SOI REC_STREET REC_SUB_DISTRICT REC_PROV_CODE REC_DISTRICT_CODE REC_ZIPCODE REC_PHONE_NO REC_FAX_NO REC_COUNTRY_CODE | VARCHAR2 VARCHAR2 VARCHAR2 VARCHAR2 VARCHAR2 VARCHAR2 VARCHAR2 VARCHAR2 CHAR VARCHAR2 VARCHAR2 VARCHAR2 | 60 60 50 50 50 50 3 3 5 100 30 3 | Y Y Y Y Y Y Y Y Y Y Y Y | Ready | Y | Picklist | Yes | 1. ที่อยู่เดียวกันกับที่อยู่ปัจจุบัน 2. ที่อยู่เดียวกันกับที่อยู่วางบิล | ที่อยู่จัดส่งเอกสาร | Confirmed |  | - กรอกข้อมูลที่อยู่ หรือเลือกข้อมูลจากตัวเลือก |  |  |  |  |  |  | Document Address | TMS_Document_Address__c | Picklist | Picklist | Yes |
| 41 | Tenant Grade/Assessment |  |  |  |  |  | ไม่มี |  |  |  |  | Ready | Y | Picklist |  | - A - B - C - D | ผลประเมินผู้ประกอบการ  | Confirmed |  |  |  |  |  |  |  |  | Tenant Grade/Assessment | TMS_Tenant_Grade_Assessment__c | Picklist | Picklist |  |
| 42 | Closure Opportunity |  |  |  |  |  | ไม่มี |  |  |  |  | Ready | Y | Picklist |  | - สูง - กลาง - ต่ำ | โอกาสในการปิดสัญญา | Confirmed |  |  |  |  |  |  |  |  | Closure Opportunity | TMS_Closure_Opportunity__c | Picklist | Picklist |  |
| 43 | Tenant Status |  | STATUS | NUMBER | 22 |  | KPS_R_SHOP | STATUS | NUMBER | 1,0 | Y | Ready | Y | Picklist | Yes | - New - Waiting list - Under discussion - Contracted - Inactive | สถานะผู้ประกอบการ | Confirmed |  |  |  |  |  |  |  |  | Tenant Status | TMS_Tenant_Status__c | Picklist | Picklist | Yes |
| 44 | KPT Shop Type (King Power Tax Fee) |  |  |  |  |  | KPS_R_SHOP | TEXT_BU_TYPE | VARCHAR2 | 20 | Y | Ready | Y | Picklist |  | BU Royal Local Product |  |  |  |  |  |  |  |  |  |  | KPT Shop Type (King Power Tax Fee) | TMS_KPT_Shop_Type_King_Power_Tax_Fee__c | Picklist | Picklist |  |
| 45 | Require Sales Confirmation |  |  |  |  |  | KPS_R_SHOP | SEND_SALES_TEXT_TYPE (SUM - ส่งข้อมูล Sales แบบสรุป DETAIL - ส่งข้อมูล Sales แบบละเอียด NONE - ไม่ส่งข้อมูล Sales) | VARCHAR2 | 6 | Y | Ready | Y | Picklist |  | No Tenant Confirm REV Confirm |  |  |  |  |  |  |  |  |  |  | Require Sales Confirmation | TMS_Require_Sales_Confirmation__c | Picklist | Picklist |  |
| Contact Person |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 46 | Name-Surname |  |  |  |  |  | KPS_R_SHOP_CONT_PER | CONT_NAME | VARCHAR2 | 50 | N | Ready | Y | Text (255) | Yes |  |  | Confirmed |  |  |  |  |  |  |  |  |  |  |  | Text (255) | Yes |
| 47 | Position |  |  |  |  |  | KPS_R_SHOP_CONT_PER | CONT_POST | VARCHAR2 | 50 | Y | Ready | Y | Text (255) | Yes |  |  | Confirmed |  |  |  |  |  |  |  |  |  |  |  | Text (255) | Yes |
| 48 | Mobile no. |  |  |  |  |  | KPS_R_SHOP_CONT_PER | CONT_PHONE_NO | VARCHAR2 | 30 | Y | Ready | Y | Phone | Yes |  |  | Confirmed |  |  |  |  |  |  |  |  |  |  |  | Phone | Yes |
| 49 | Email Address |  |  |  |  |  | KPS_R_SHOP_CONT_PER | CONT_EMAIL_ADDR | VARCHAR2 | 50 | Y | Ready | Y | Email | Yes |  |  | Confirmed |  |  |  |  |  |  |  |  |  |  |  | Email | Yes |
| 50 | Subject to Contact |   |  |  |  |  | KPS_R_SHOP_CONT_PER | SUBJECT | VARCHAR2 | 150 | Y | Ready | Y | Picklist | Yes | - สนใจพื้นที่ (Prospect) - สัญญา (Contract) - ออกแบบ (Design) - การตกแต่งร้านค้า (Onsite construction) - ระบบงานขาย POS และส่งยอดขาย (Revenue) - ราคาสินค้า (Price) - การส่งเสริมการขาย (Promotion) - Automated call | ส่วนงาน | Confirmed |  |  |  |  |  |  |  |  |  |  |  | Picklist | Yes |
| 51 | Preferred contact channel |  |  |  |  |  | ไม่มี |  |  |  |  | Ready | Y | Picklist | Yes | - Mobile - Email  | ช่องทางที่สะดวกให้ติดต่อ | Confirmed |  |  |  |  |  |  |  |  |  |  |  | Picklist | Yes |
|  | Is Migration |  |  |  |  |  |  |  |  |  |  |  |  |  |  | True False |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |

---

## Spec

| No. | SFDC Field Name (EN) | SFDC Field Name (TH) | Type | Required | Sample Data | Description | Status | Remark | Help Text | Track History | External ID | Track History.1 | Encrypted | Page Layout | Length | Source Field API Name |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Header |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 1 | Consession No. | Concession No. | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 2 | Unit No. | เลขที่ยูนิต | Text(XX) |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 3 | Start Date | วันที่เริ่ม | Date |  |  |  |  |  |  |  |  |  |  |  |  |  |

---

## 02_Concession

|   | SFDC Field Name (EN) | SFDC Field Name (TH) | Source Field API Name | Source Field Type | Source Field Length | VULLABLE (N=Required) | KP Table | KP Field Name | KP Field Type | KP Field Length | VULLABLE (N=Required).1 | Progress | Confirm | Type | Required | Sample Data | Description | Status | User/KP Feedback | Remark | Help Text | Track History | External ID | Track History.1 | Encrypted | Page Layout | Length |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Concession Information |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 1 | Concession No. |  | CON_CODE | CHAR | 2 | N | KPS_R_CONCESS | CON_CODE | CHAR | 2 | N | Ready | Y | Text | Yes | 09 | เลขที่รหัสสัมปทาน | Confirmed |  |  |  |  |  |  |  |  |  |
| 2 | Concession Type |  |  |  |  |  | Hard code - Airport |  |  |  |  | Ready | Y | Text | Yes | - Airport - Non-airport | ประเภทของสัมปทาน | Confirmed |  |  |  |  |  |  |  |  |  |
| 3 | Description |  | CON_DESC | VARCHAR2 | 100 | N | KPS_R_CONCESS | CON_DESC | VARCHAR2 | 100 | N | Ready | Y | Text | Yes |  | รายละเอียดสัมปทาน | Confirmed |  |  |  |  |  |  |  |  |  |
| 4 | ชื่อผู้ให้สัมปทาน |  | CON_SNAME CON_LNAME | VARCHAR2 VARCHAR2 | 10 100 | N N | KPS_R_CONCESS | CON_LNAME | VARCHAR2 | 100 | N | Ready | Y | Text | Yes | SVB - Terminal 1 |  | Confirmed |  | 09 : SVB 05 : DMK (Inter) 10 : DMK (Dom) 08 : HKT |  |  |  |  |  |  |  |
| 5 | ชื่อย่อผู้ให้สัมปทาน |  |  |  |  |  | KPS_R_CONCESS | CON_SNAME | VARCHAR2 | 10 | N | Ready | Y | Text | Yes | AOT |  | Confirmed |  |  |  |  |  |  |  |  |  |
| 6 | ชื่อผู้รับสัมปทาน |  | RCON_SNAME RCON_LNAME | VARCHAR2 VARCHAR2 | 10 100 | N N | KPS_R_CONCESS | RCON_LNAME | VARCHAR2 | 100 | N | Ready | Y | Text | Yes | บริษัท คิงเพาเวอร์ สุวรรณภูมิ จำกัด |  | Confirmed |  |  |  |  |  |  |  |  |  |
| 7 | ชื่อย่อผู้รับสัมปทาน |  |  |  |  |  | KPS_R_CONCESS | RCON_SNAME | VARCHAR2 | 10 | N | Ready | Y | Text | Yes | KPS |  | Confirmed |  |  |  |  |  |  |  |  |  |
| 8 | Location |  | LOCATION | VARCHAR2 | 60 | N | KPS_R_CONCESS | LOCATION | VARCHAR2 | 60 | N | Ready | Y | Text | Yes | ท่าอากาศยานสุวรรณภูมิ |  | Confirmed |  |  |  |  |  |  |  |  |  |
| 9 | Start Date |  | BEGIN_DATE | VARCHAR2 | 10 | Y | KPS_R_CONCESS | BEGIN_DATE | VARCHAR2 | 10 | Y | Ready | Y | Date | Yes |  |  | Confirmed |  | - Start Date ต้องไม่มากกว่า End Date - รูปแบบ: DD/MM/YYYY เป็น คริสต์ศักราช |  |  |  |  |  |  |  |
| 10 | End Date |  | END_DATE | VARCHAR2 | 10 | Y | KPS_R_CONCESS | END_DATE | VARCHAR2 | 10 | Y | Ready | Y | Date | Yes |  |  | Confirmed |  | - End Date ต้องไม่น้อยกว่า Start Date - รูปแบบ: DD/MM/YYYY เป็น คริสต์ศักราช |  |  |  |  |  |  |  |
| 11 | Concession Status |  |  |  |  |  | KPS_R_CONCESS | ACTIVE_FLAG (1 = Active, 0 = Inactive) | NUMBER | 1,0 | Y | Ready | Y | Picklist | Yes | - Active - Inactive | สถานะสัมปทาน | Confirmed |  | - เลือกข้อมูลตามตัวเลือกที่กำหนด - ข้อมูลจะถูกปรับอัตโนมัติหลังจากที่หมดอายุสัญญา  |  |  |  |  |  |  |  |
| 12 | รอบปีงบประมาณ (From) |  | ACT_DATE_AS_OF | DATE | 7 | Y | ไม่มี |  |  |  |  | Ready | Y | Date | Yes |  |  | Confirmed |  | SVB:               01/July - 30/June DMK & HKT:  01/October - 30/September |  |  |  |  |  |  |  |
| 13 | รอบปีงบประมาณ (To) |  |  |  |  |  | ไม่มี |  |  |  |  | Ready | Y | Date | Yes |  |  | Confirmed |  |  |  |  |  |  |  |  |  |
| 14 | การปรับส่วนแบ่งรายได้ตามมาตรการช่วยเหลือตามที่ ทอท. กำหนด (ผู้โดยสารจะมากกว่าปี 2562) |  | <New> |  |  |  | ไม่มี |  |  |  |  | New | Y |  |  | ปัจจุบันคือการปรับส่วนแบ่งรายได้ขั้นต่ำของ  - ใช่ = DMK, HKT - ไม่ใช่ = SVB |  |  |  |  |  |  |  |  |  |  |  |
| Concession Area |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 15 | Total Area |  | CON_TOTAL_AREA | NUMBER | 22 | Y | KPS_R_CONCESS | CON_TOTAL_AREA | NUMBER | 16, 3 | Y | Ready | Y | Number(1,3) | Yes | 5.000 |  | Confirmed |  | - กรอกได้เฉพาะตัวเลขเท่านั้น - รูปแบบ: #.### |  |  |  |  |  |  |  |
| 16 | Commercial Area |  | CON_COMM_AREA | NUMBER | 22 | Y | KPS_R_CONCESS | CON_COMM_AREA | NUMBER | 16, 3 | Y | Ready | Y | Number(1,3) | Yes | 5.000 |  | Confirmed |  | " |  |  |  |  |  |  |  |
| 17 | M&E Area |  | CON_ME_AREA | NUMBER | 22 | Y | KPS_R_CONCESS | CON_ME_AREA | NUMBER | 16, 3 | Y | Ready | Y | Number(1,3) | Yes | 0.000 |  | Confirmed |  | " |  |  |  |  |  |  |  |
| 18 | Store Area |  | CON_STORE_AREA | NUMBER | 22 | Y | KPS_R_CONCESS | CON_STORE_AREA | NUMBER | 16, 3 | Y | Ready | Y | Number(1,3) | Yes | 0.000 |  | Confirmed |  | " |  |  |  |  |  |  |  |
| 19 | Other Area |  |  |  |  |  | ไม่มี |  |  |  |  | Ready | Y | Number(1,3) | Yes | 0.000 |  | Confirmed |  | " |  |  |  |  |  |  |  |
| Actual Area |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 20 | Total Area |  | ACT_TOT_AREA | NUMBER | 22 | Y | KPS_R_CONCESS | ACT_TOT_AREA | NUMBER | 16, 3 | Y | Ready | Y | Number(1,3) | Yes | 5.000 |  | Confirmed |  | " |  |  |  |  |  |  |  |
| 21 | Commercial Area |  | ACT_COMM_AREA | NUMBER | 22 | Y | KPS_R_CONCESS | ACT_COMM_AREA | NUMBER | 16, 3 | Y | Ready | Y | Number(1,3) | Yes | 5.000 |  | Confirmed |  | " |  |  |  |  |  |  |  |
| 22 | M&E Area |  | ACT_ME_AREA | NUMBER | 22 | Y | KPS_R_CONCESS | ACT_ME_AREA | NUMBER | 16, 3 | Y | Ready | Y | Number(1,3) | Yes | 0.000 |  | Confirmed |  | " |  |  |  |  |  |  |  |
| 23 | Store Area |  | ACT_STORE_AREA | NUMBER | 22 | Y | KPS_R_CONCESS | ACT_STORE_AREA | NUMBER | 16, 3 | Y | Ready | Y | Number(1,3) | Yes | 0.000 |  | Confirmed |  | " |  |  |  |  |  |  |  |
| 24 | Other Area |  |  |  |  |  | ไม่มี |  |  |  |  | Ready | Y | Number(1,3) | Yes | 0.000 |  | Confirmed |  | " |  |  |  |  |  |  |  |
| Occupied Area |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 25 | Total Area |  | <New> |  |  |  | ไม่มี |  |  |  |  | New | Y | Number(1,3) | Yes | 5.000 |  | Confirmed |  | " |  |  |  |  |  |  |  |
| 26 | Commercial Area |  | <New> |  |  |  | ไม่มี |  |  |  |  | New | Y | Number(1,3) | Yes | 5.000 |  | Confirmed |  | " |  |  |  |  |  |  |  |
| 27 | M&E Area |  | <New> |  |  |  | ไม่มี |  |  |  |  | New | Y | Number(1,3) | Yes | 0.000 |  | Confirmed |  | " |  |  |  |  |  |  |  |
| 28 | Store Area |  | <New> |  |  |  | ไม่มี |  |  |  |  | New | Y | Number(1,3) | Yes | 0.000 |  | Confirmed |  | " |  |  |  |  |  |  |  |
| 29 | Other Area |  | <New> |  |  |  | ไม่มี |  |  |  |  | New | Y | Number(1,3) | Yes | 0.000 |  | Confirmed |  | " |  |  |  |  |  |  |  |
| Vacant Area |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 30 | Total Area |  | <New> |  |  |  | ไม่มี |  |  |  |  | New | Y | Number(1,3) | Yes | 5.000 |  | Connfirmed |  | " |  |  |  |  |  |  |  |
| 31 | Commercial Area |  | <New> |  |  |  | ไม่มี |  |  |  |  | New | Y | Number(1,3) | Yes | 5.000 |  | Connfirmed |  | " |  |  |  |  |  |  |  |
| 32 | M&E Area |  | <New> |  |  |  | ไม่มี |  |  |  |  | New | Y | Number(1,3) | Yes | 0.000 |  | Connfirmed |  | " |  |  |  |  |  |  |  |
| 33 | Store Area |  | <New> |  |  |  | ไม่มี |  |  |  |  | New | Y | Number(1,3) | Yes | 0.000 |  | Connfirmed |  | " |  |  |  |  |  |  |  |
| 34 | Other Area |  | <New> |  |  |  | ไม่มี |  |  |  |  | New | Y | Number(1,3) | Yes | 0.000 |  | Connfirmed |  | " |  |  |  |  |  |  |  |
| SAP Information |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 35 | SAP Company Code |  | SAP_COMPANY_CODE | VARCHAR2 | 4 | Y | KPS_R_CONCESS | SAP_COMPANY_CODE | VARCHAR2 | 4 | Y | Ready | Y | Number(4,0) | Yes | 6000 |  | Confirmed |  |  |  |  |  |  |  |  |  |
| 36 | SAP Business Place |  | SAP_BUSINESS_PLACE | VARCHAR2 | 4 | Y | KPS_R_CONCESS | SAP_BUSINESS_PLACE | VARCHAR2 | 4 | Y | Ready | Y | Number(4,0) | Yes | 0001 |  | Confirmed |  |  |  |  |  |  |  |  |  |
| 37 | SAP Business Area |  | SAP_BUSINESS_AREA | VARCHAR2 | 4 | Y | KPS_R_CONCESS | SAP_BUSINESS_AREA | VARCHAR2 | 4 | Y | Ready | Y | Number(4,0) | Yes | 2111 |  | Confirmed |  |  |  |  |  |  |  |  |  |
| 38 | SAP Cost Center |  | SAP_COST_CENTER | VARCHAR2 | 10 | Y | KPS_R_CONCESS | SAP_COST_CENTER | VARCHAR2 | 10 | Y | Ready | Y | Number(10,0) | Yes | 6211100000 |  | Confirmed |  |  |  |  |  |  |  |  |  |
| 39 | SAP Funds Center |  | SAP_FUNDS_CENTER | VARCHAR2 | 10 | Y | KPS_R_CONCESS | SAP_FUNDS_CENTER | VARCHAR2 | 10 | Y | Ready | Y | Number(10,0) | Yes | 6211100000 |  | Confirmed |  |  |  |  |  |  |  |  |  |
| 40 | SAP Airport |  | SAP_TEXT_AIRPORT | VARCHAR2 | 20 | Y | KPS_R_CONCESS | SAP_TEXT_AIRPORT | VARCHAR2 | 20 | Y | Ready | Y | Text | Yes | SVB |  | Confirmed |  |  |  |  |  |  |  |  |  |
| Concession Contract |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 41 | Concession Contract No. |  | <New> |  |  |  | ไม่มี |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 42 | Contract Date |  | <New> |  |  |  | ไม่มี |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 43 | Minimum Guarantee |  | <New> |  |  |  | ไม่มี |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 44 | Upfront Amount |  | <New> |  |  |  | ไม่มี |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 45 | Reference Year |  | <New> |  |  |  | ไม่มี |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Revenue Sharing Fixed Amount |  | <New> |  |  |  | ไม่มี |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 46 | - Number of Installment |  | <New> |  |  |  | ไม่มี |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 47 | - Total Revenue Sharing |  | <New> |  |  |  | ไม่มี |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 48 | - Due Date |  | <New> |  |  |  | ไม่มี |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 49 | - Amount |  | <New> |  |  |  | ไม่มี |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 50 | Revenue Sharing - % per month |  | <New> |  |  |  | ไม่มี |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Minimum Guarantee |  | <New> |  |  |  | ไม่มี |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 51 | - Contract Start Date |  | <New> |  |  |  | ไม่มี |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 52 | - Contract End Date |  | <New> |  |  |  | ไม่มี |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 53 | - No. of Day(s) |  | <New> |  |  |  | ไม่มี |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 54 | - Minimum Guarantee (per day) |  | <New> |  |  |  | ไม่มี |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 55 | - Total Area |  | <New> |  |  |  | ไม่มี |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 56 | - Commercial Area |  | <New> |  |  |  | ไม่มี |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 57 | - M&E Area |  | <New> |  |  |  | ไม่มี |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 58 | - Other Area |  | <New> |  |  |  | ไม่มี |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 59 | - Cost per SQM |  | <New> |  |  |  | ไม่มี |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 60 | - Passenger Growth (%) |  | <New> |  |  |  | ไม่มี |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 61 | - Inflation Rate (%) |  | <New> |  |  |  | ไม่มี |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 62 | - Remark |  | <New> |  |  |  | ไม่มี |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |

---

## 03_Shop Category

| No. | SFDC Field Name (EN) | SFDC Field Name (TH) | Source Field API Name | Source Field Type | Source Field Length | VULLABLE (N=Required) | KP Table | KP Field Name | KP Field Type | KP Field Length | VULLABLE (N=Required).1 | Progress | Confirm | Type | Required | Sample Data | Description | Status | User/KP Feedback | Remark | Help Text | Track History | External ID | Track History.1 | Encrypted | Page Layout | Length | Source Field API Name.1 | Source Field Type.1 | Source Field Length.1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Category |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 1 | Space Owner |  |  |  |  |  | KPS_R_OWNER | OWNER_CODE | VARCHAR2 | 30 | N | Ready |  |  |  |  |  | New |  |  |  |  |  |  |  |  |  | PROD_CATE_CODE | CHAR | 1.0 |
| 2 | AOT Rental Type |  |  |  |  |  | KPS_R_AOT_RENTAL_TYPE | RNT_CODE | VARCHAR2 | 5 | N | Ready |  |  |  |  |  | New |  |  |  |  |  |  |  |  |  | STD_CATE_ID | NUMBER | 22.0 |
| 3 | Space Usage Type |  |  |  |  |  | KPS_R_SPACE_USAGE KPS_R_SPACE_USAGE | USG_CODE USG_DESC | VARCHAR2 VARCHAR2 | 5 50 | N Y | Ready |  |  |  |  |  | New |  |  |  |  |  |  |  |  |  | STD_CATE_DESC | VARCHAR2 | 200.0 |
| 4 | AOT Shop Category |  |  |  |  |  | KPS_R_AOT_SHOP_CATE | AOT_CATE_CODE | CHAR | 4 | N | Ready |  |  |  |  |  | New |  |  |  |  |  |  |  |  |  | STATUS | NUMBER | 22.0 |
| 5 | AOT Shop Sub-Category |  |  |  |  |  | ไม่มี |  |  |  |  | Ready |  |  |  | - Office, LWC, Store, etc. |  | New |  |  |  |  |  |  |  |  |  | CREATEDBY | VARCHAR2 | 30.0 |
| 6 | Shop Cateogry |  | PROD_CATE_CODE | CHAR | 1.0 | N | KPS_R_AOT_SHOP_CATE | AOT_CATE_DESC | VARCHAR2 | 200 | N | Ready |  |  |  | ประเภทร้ํานค้ําของ AOT เช่น - Bank - Communication -F&B - Restaurant - Healthy - Entertainment - Others -Lounge -Travel |  | New |  | - เลือกข้อมูลตํามตัวเลือกที่ก ําหนด - เลือกได้มํากกว่ํา 1 ตัวเลือก |  |  |  |  |  |  |  | CREATEDDATE | DATE | 7.0 |

---

## 04_Shop Brand

| No. | SFDC Field Name (EN) | SFDC Field Name (TH) | Source Field API Name | Source Field Type | Source Field Length | VULLABLE (N=Required) | KP Table | KP Field Name | KP Field Type | KP Field Length | VULLABLE (N=Required).1 | Progress | Confirm | Type | Required | Sample Data | Description | Status | User/KP Feedback | Remark | Help Text | Track History | External ID | Track History.1 | Encrypted | Page Layout | Length | Source Field API Name.1 | SFDC Table | SFDC API Name | SFDC Type |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Information |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 1 | Tenant Code |  | SHOP_CODE | VARCHAR2 | 20 | N | KPS_R_SHOP_BRAND | SHOP_CODE | VARCHAR2 | 20 | N | Ready | Y | Text (100) | Yes | 0902029 | รหัสบริษัทผู้ประกอบการ | Confirmed |  | - ระบบสร้างให้อัตโนมัติเมื่อได้รับการอนุมัติจัดทำสัญญาครั้งแรก จากระบบ Workflow Logic: (Concession Code)(2 หลัก) + (Business Type)(2 หลัก) + (Tenant Running No.)(3 หลัก) |  |  |  |  |  |  |  |  | TMS_Shop_Brand__c |  |  |
| 2 | Shop Brand Code | SHPBND_CODE | VARCHAR2 | 4 | N |  | KPS_R_SHOP_BRAND | SHPBND_CODE | VARCHAR2 | 4 | N | Ready | Y | Number (4,0) | Yes |  0001 | รหัสแบรนด์ | Confirmed |  | - กรอกได้สูงสุด 4 หลัก - กรอกได้เฉพาะตัวเลขเท่านั้น |  |  |  |  |  |  |  |  |  |  |  |
| 3 | Brand Reputation | <New> |  |  |  |  | ไม่มี |  |  |  |  | Ready | Y | Picklist (Multi-Select) | Yes | - Inter - Local | ชื่อเสียงแบรนด์ | Confirmed |  | - เลือกข้อมูลตามตัวเลือกที่กำหนด - เลือกได้ 1 ตัวเลือก  |  |  |  |  |  |  |  |  |  |  |  |
| 4 | Shop Brand Name - TH | SHPBND_NAME_T | VARCHAR2 | 60 | Y |  | KPS_R_SHOP_BRAND | SHPBND_NAME_T | VARCHAR2 | 60 | Y | Ready | Y | Text | Yes | อิมเพรสซีฟ สุวรรณภูมิ | ชื่อแบรนด์ ภาษาไทย | Confirmed |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 5 | Shop Brand Name - EN | SHPBND_NAME_E | VARCHAR2 | 60 | Y |  | KPS_R_SHOP_BRAND | SHPBND_NAME_E | VARCHAR2 | 60 | Y | Ready | Y | Text | Yes | Impressive Suvarnabhumi | ชื่อแบรนด์ ภาษาอังกฤษ | Confirmed |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 6 | Shop Brand Status | STATUS | NUMBER | 22 | Y |  | KPS_R_SHOP_BRAND | STATUS (1 = active, 2 = inactive) | NUMBER | 1 | Y | Ready | Y | Picklist | Yes | - Active - Inactive |  | Confirmed |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Product |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 6 | Product Category Code |  |  |  |  |  | KPS_T_REQPROD_MD | STD_CATE_CODE | VARCHAR2 | 4 | N | Ready |  | Text |  | 5ABD | ประเภท product code   | Confirmed |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 7 | Product Category |  |  |  |  |  | KPS_T_REQPROD_MD KPS_R_PROD_SUBCATE1  | STD_CATE_CODE (ตัวที่ 1 = PROD_CATE_CODE  ตัวที่ 2 = PROD_SUBCAT1_CODE)  PROD_SUBCAT1_DESC | VARCHAR2 VARCHAR2 | 4 200 | N Y | Ready |  | Text |  | Halal food | ประเภท product   | Confirmed |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 8 | Product Code |  |  |  |  |  | KPS_T_PROD_COMPARE | PROD_SERV_CODE | VARCHAR2 | 100 | N | Ready |  | Text |  | 9781801081795 | รหัส product   | Confirmed |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 9 | Product Name |  |  |  |  |  | KPS_T_PROD_COMPARE | PROD_SERV_NAME | VARCHAR2 | 200 | Y | Ready |  | Text |  | ก๋วยเตี๋ยวแห้ง | ชื่อ product   | Confirmed |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 10 | Sub Product Code |  |  |  |  |  | ไม่มี |  |  |  |  | Ready |  | Text |  | 9781801081795 | รหัส product ย่อย สำหรับกรณี bundle product   | Confirmed |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 11 | Sub Product Name |  |  |  |  |  | ไม่มี |  |  |  |  | Ready |  | Text |  | ก๋วยเตี๋ยวแห้ง มินิ | ชื่อ product ย่อย สำหรับกรณี bundle product   | Confirmed |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 12 | Sell Price (include VAT) |  |  |  |  |  | KPS_T_PROD_COMPARE | REQ_PRICE_INC_VAT | NUMBER | 16,2 | Y | Ready |  | Number(16,2) |  | 1,070.00 | ราคาขาย รวม VAT   | Confirmed |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 13 | Previous Sell Price (include VAT) |  |  |  |  |  | KPS_T_PROD_COMPARE | OLD_PRICE_INC_VAT | NUMBER | 16,2 | Y | Ready |  | Number(16,2) |  | 1,000.00 | ราคาขายก่อนหน้า รวม VAT   | Confirmed |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 14 | Reference Price (include VAT) |  |  |  |  |  | KPS_T_PROD_COMPARE | REF_PRICE_INC_VAT | NUMBER | 16,2 | Y | Ready |  | Number(16,2) |  | 895.00 | ราคาเปรียบเทียบ รวม VAT   | Confirmed |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 15 | % Different |  |  |  |  |  | KPS_T_PROD_COMPARE | REF_PRICE_EXC_DIFF | NUMBER | 16,2 | Y | Ready |  | Number(16,2) |  | 19.55 | % ความแตกต่างของราคา   | Confirmed |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 16 | Reference Leading Hotel/Mall |  |  |  |  |  | KPS_T_PROD_COMPARE | REF_SHOP | VARCHAR2 | 100 | Y | Ready |  | Text |  | Central World | สถานที่ที่ใช้ในการเปรียบเทียบล่าสุด   | Confirmed |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 17 | Reference Shop |  |  |  |  |  | KPS_T_PROD_COMPARE | REF_SHOP | VARCHAR2 | 100 | Y | Ready |  | Text |  | Asia Books | ร้านค้าที่ใช้ในการเปรียบเทียบล่าสุด   | Confirmed |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 18 | Remark |  |  |  |  |  | KPS_T_PROD_COMPARE | REMARKS | VARCHAR2 | 200 | Y | Ready |  | Text (255) |  |  |  | Confirmed |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 19 | Related Request No. |  |  |  |  |  | KPS_T_PROD_COMPARE | APPRV_SEQ เอาค่า max | NUMBER | 5,0 | Y | Ready |  | Text |  |  | เลขที่การขออนุมัติ product ล่าสุด | Confirmed |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 20 | Related Request Type |  |  |  |  |  | KPS_T_PROD_COMPARE | TRANS_TYPE (1=New Product,  2=Price Increase/Decrease,  3=Cancel Product, 4=Promotion) | NUMBER | 1,0 | Y | Ready |  | Picklist |  | - New Product - Price Increase - Price Decrease - Cancel Product - Promotion | รูปแบบการขออนุมัติปรับปรุงข้อมูลผลิตภัณฑ์ล่าสุด | Confirmed |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 21 | Tenant Product Reference |  |  |  |  |  | ไม่มี |  |  |  |  | Ready |  |  |  |  | ภาพประกอบสินค้า ที่ใช้ในการเปรียบเทียบ | Confirmed |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 22 | Promotion Code |  |  |  |  |  | KPS_T_PROD_COMPARE KPS_T_APPRV_M | PROD_SERV_CODE PRO_CODE | VARCHAR2 VARCHAR2 | 100 10 | N Y | Ready |  | Text |  | 010009 | โปรโมชั่นโค้ดของผลิตภัณฑ์   | Confirmed |  |  |  |  |  |  |  |  |  |  |  |  |  |

---

## 05_Shop Branch

|   | SFDC Field Name (EN) | SFDC Field Name (TH) | Source Field API Name | Source Field Type | Source Field Length | VULLABLE (N=Required) | KP Table | KP Field Name | KP Field Type | KP Field Length | VULLABLE (N=Required).1 | Progress | Confirm | Type | Required | Sample Data | Description | Status | User/KP Feedback | Remark | Help Text | Track History | External ID | Track History.1 | Encrypted | Page Layout | Length | Source Field API Name.1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Information |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 1 | Shop Branch No. |  | BRANCH_NO | NUMBER | 22.0 | N | KPS_R_BRANCH | BRANCH_NO | NUMBER | 4,0 | N | Ready | Y | Text (255) | Yes |  |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 2 | Shop Branch Code |  | BRANCH_CODE | VARCHAR2 | 20.0 | N | KPS_R_BRANCH | BRANCH_CODE | VARCHAR2 | 20 | N | Ready | Y | Text (255) | Yes |  |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 3 | Shop Branch Name - TH |  | BRANCH_NAME_T | VARCHAR2 | 200.0 | Y | KPS_R_BRANCH | BRANCH_NAME_T | VARCHAR2 | 200 | Y | Ready | Y | Text (255) | Yes |  |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 4 | Shop Branch Name - EN |  | BRANCH_NAME_E | VARCHAR2 | 200.0 | Y | KPS_R_BRANCH | BRANCH_NAME_E | VARCHAR2 | 200 | Y | Ready | Y | Text (255) | Yes |  |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 5 | Shop Branch Short Name |  | BRANCH_SHOTNAME | VARCHAR2 | 100.0 | Y | KPS_R_BRANCH | BRANCH_SHOTNAME | VARCHAR2 | 100 | Y | Ready | Y | Text (255) | Yes |  |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 6 | Shop Category (AOT) |  | AOT_CATE_CODE | CHAR | 4.0 | N | KPS_R_BRANCH KPS_R_AOT_SHOP_CATE | AOT_CATE_CODE AOT_CATE_DESC | CHAR VARCHAR2 | 4 200 | N N | Ready | Y | Picklist (Multi-Select) | Yes | - Bank - Communication - F&B - Restaurant - Healthy - Entertainment - Others - Lounge - Travel | ประเภทร้านค้าของ AOT | Confirmed |  | - เลือกข้อมูลตามตัวเลือกที่กำหนด - เลือกได้มากกว่า 1 ตัวเลือก  |  |  |  |  |  |  |  |  |
| 7 | Service Time (Start) |  | <New> |  |  |  | ไม่มี |  |  |  |  | New | Y | Time | No |  | เวลาเปิด ปิด ร้าน เช่น 06:00 - 19:00 | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 8 | Service Time (End) |  | <New> |  |  |  | ไม่มี |  |  |  |  | New | Y | Time | No |  |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| Shop Unit |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 9 | Unit No. |  | SHOP_UNIT | VARCHAR2 | 15.0 | Y | KPS_R_BRANCH | SHOP_UNIT | VARCHAR2 | 15 | Y | Ready | Y | Text (255) | No |  |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 10 | Total Area |  | AREA | NUMBER | 22.0 | Y | KPS_R_BRANCH | AREA | NUMBER | 16,3 | Y | Ready | Y | Number (1,3) | No | 5.000 |  | Confirmed |  | - กรอกได้เฉพาะตัวเลขเท่านั้น - รูปแบบ: #.###  |  |  |  |  |  |  |  |  |
| 11 | Commercial Area |  | COMM_AREA | NUMBER | 22.0 | Y | KPS_R_BRANCH | COMM_AREA | NUMBER | 16,3 | Y | Ready | Y | Number (1,3) | No | 5.000 |  | Confirmed |  | " |  |  |  |  |  |  |  |  |
| 12 | Store Area |  | STORE_AREA | NUMBER | 22.0 | Y | KPS_R_BRANCH | STORE_AREA | NUMBER | 16,3 | Y | Ready | Y | Number (1,3) | No | 0.000 |  | Confirmed |  | " |  |  |  |  |  |  |  |  |
| 13 | M&E Area |  | MNE_AREA | NUMBER | 22.0 | Y | KPS_R_BRANCH | MNE_AREA | NUMBER | 16,3 | Y | Ready | Y | Number (1,3) | No | 0.000 |  | Confirmed |  | " |  |  |  |  |  |  |  |  |
| 14 | Other Area |  | OTH_AREA | NUMBER | 22.0 | Y | KPS_R_BRANCH | OTH_AREA | NUMBER | 16,3 | Y | Ready | Y | Number (1,3) | No | 0.000 |  | Confirmed |  | " |  |  |  |  |  |  |  |  |
| POS |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 15 | POS No. |  | <New> |  |  |  | KPS_R_BRANCH KPS_R_BRANCH KPS_R_BRANCH KPS_R_POS | CON_CODE SHOP_CODE BRANCH_CODE POS_NO | CHAR VARCHAR2 VARCHAR2 VARCHAR2 | 2 20 20 50  | N N N N | New | Y | Text (255) |  | E05112000200866 | หมายเลขเครื่อง POS | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 16 | POS Status |  | <New> |  |  |  | KPS_R_POS | STATUS (1 = active, 2 = Inactive) | NUMBER | 1,0 | Y | New | Y | Picklist | - Active - Inactive  |  | สถานะเครื่อง POS | Confirmed |  |  |  |  |  |  |  |  |  |  |
| Shop Holiday/Event  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 17 | Date Period (From) |  | <New> |  |  |  | ไม่มี |  |  |  |  | New | Y | Date |  |  | ช่วงวันที่ปิดร้าน (ปี คศ.) Format: DD/MM/YYYY | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 18 | Date Period (To) |  | <New> |  |  |  | ไม่มี |  |  |  |  | New | Y | Date |  |  |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 19 | Shop Holiday/Event - Reason |  | <New> |  |  |  | ไม่มี |  |  |  |  | New | Y | Text |  | งานเลี้ยงปีใหม่ | หมายเหตุ | Confirmed |  |  |  |  |  |  |  |  |  |  |
| Shop Contact Person |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 20 | Name-Surname |  | BLL_NAME | VARCHAR2 | 200.0 | Y | KPS_R_BRANCH KPS_R_SHOP_CONT_PER | SHOP_CODE CONT_NAME | VARCHAR2 VARCHAR2 | 20 50 | N N | Ready |  | Text |  |  |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 21 | Position |  | <New> |  |  |  | KPS_R_BRANCH KPS_R_SHOP_CONT_PER | SHOP_CODE CONT_POST | VARCHAR2 VARCHAR2 | 20 50 | N Y | New |  | Text |  |  |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 22 | Mobile No. |  | BLL_TEL | VARCHAR2 | 100.0 | Y | KPS_R_BRANCH KPS_R_SHOP_CONT_PER | SHOP_CODE CONT_PHONE_NO | VARCHAR2 VARCHAR2 | 20 30 | N Y | Ready |  | Phone |  |  |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 23 | Email Address |  | <New> |  |  |  | KPS_R_BRANCH KPS_R_SHOP_CONT_PER | SHOP_CODE CONT_EMAIL_ADDR | VARCHAR2 VARCHAR2 | 20 50 | N Y | New |  | Email |  |  |  | Confirmed |  |  |  |  |  |  |  |  |  |  |

---

## 06_Contract

| No. | SFDC Field Name (EN) | SFDC Field Name (TH) | Source Field API Name | Source Field Type | Source Field Length | VULLABLE (N=Required) | KP Table | KP Field Name | KP Field Type | KP Field Length | VULLABLE (N=Required).1 | Progress | Confirm | Type | Required | Sample Data | Description | Status | User/KP Feedback | Remark | Help Text | Track History | External ID | Track History.1 | Encrypted | Page Layout | Length | Source Field API Name.1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Information |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 1 | Account Name |  |  |  |  |  | KPS_T_CONTRACT KPS_R_SHOP | SHOP_CODE REGISTERED_NAME | VARCHAR2 VARCHAR2 | 20 200 | Y Y | Ready | Y | Lookup(Account) |  |  | ชื่อผู้ประกอบการ |  |  |  |  |  |  |  |  |  |  |  |
| 2 | Activated By |  |  |  |  |  | KPS_T_CONTRACT | CREATEDBY | VARCHAR2 | 30 | Y | Ready | Y | Lookup(User) |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 3 | Activated Date |  |  |  |  |  | KPS_T_CONTRACT | CONT_DATE | DATE | 7 | Y | Ready | Y | Date/Time |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 4 | Billing Address |  |  |  |  |  | KPS_T_CONTRACT KPS_R_SHOP KPS_R_SHOP KPS_R_SHOP KPS_R_SHOP KPS_R_SHOP KPS_R_SHOP KPS_R_SHOP | SHOP_CODE BLL_ADDRESS1 BLL_ADDRESS2 BLL_CITY BLL_ZIP BLL_COUNTRY_CODE BLL_TEL BLL_FAX | VARCHAR2 VARCHAR2 VARCHAR2 VARCHAR2 VARCHAR2 VARCHAR2 VARCHAR2 VARCHAR2 | 20 120 120 60 10 3 100 30 | Y Y Y Y Y Y Y Y | Ready | Y | Address |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 5 | Company Signed By |  |  |  |  |  | ไม่มี |  |  |  |  | Ready | Y | Lookup(User) |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 6 | Contract Name |  |  |  |  |  |  |  |  |  |  | Ready |  | Text(80) |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 7 | Contract Number |  |  |  |  |  | KPS_T_CONTRACT | CONT_NO | VARCHAR2 | 30 | N | Ready | Y | Auto Number | Yes | KPS 14/2564 | เลขที่สัญญา | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 8 | Contract Owner |  |  |  |  |  |  |  |  |  |  | Ready |  | Lookup(User) |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 9 | Contract Term (months) |  |  |  |  |  | KPS_T_CONTRACT | CONT_PERIOD_YEAR x 12 | NUMBER | 2,0 | N | Ready |  | Number(4, 0) |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 10 | Created By |  |  |  |  |  | KPS_T_CONTRACT | CREATEDBY | VARCHAR2 | 30 | Y | Ready |  | Lookup(User) |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 11 | Customer Signed By |  |  |  |  |  |  |  |  |  |  | Ready |  | Lookup(Contact) |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 12 | Customer Signed Date |  |  |  |  |  |  |  |  |  |  | Ready |  | Date |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 13 | Customer Signed Title |  |  |  |  |  |  |  |  |  |  | Ready |  | Text(40) |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 14 | Description |  |  |  |  |  | KPS_T_CONTRACT | CONT_REMARK | VARCHAR2 | 500 | Y | Ready |  | Long Text Area(32000) |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 15 | Last Modified By |  |  |  |  |  | KPS_T_CONTRACT | UPDATEDDATE | DATE | 7 | Y | Ready |  | Lookup(User) |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 16 | Owner Expiration Notice |  |  |  |  |  |  |  |  |  |  | Ready |  | Picklist |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 17 | Price Book |  |  |  |  |  |  |  |  |  |  | Ready |  | Lookup(Price Book) |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 18 | Shipping Address |  |  |  |  |  |  |  |  |  |  | Ready |  | Address |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 19 | Special Terms |  |  |  |  |  |  |  |  |  |  | Ready |  | Text Area(4000) |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 20 | Status |  |  |  |  |  | KPS_T_CONTRACT | ACTIVE_FLAG | NUMBER | 22 | Y | Ready |  | Picklist |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 21 | Requestor | ชื่อ-นามสกุลผู้ขอเปิดงาน |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  | ชื่อ-นามสกุลผู้ขอเปิดงาน (Requestor) |  |  | Ref: e-Contract |  |  |  |  |  |  |  |  |
| 22 | Requestor's Department | แผนกผู้ขอ |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  | แผนกผู้ขอ (Requestor's Department) |  |  | Ref: e-Contract |  |  |  |  |  |  |  |  |
| 23 | Requestor's Position | ตำแหน่งผู้ขอ |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  | ตำแหน่งผู้ขอ (Requestor's Position) |  |  | Ref: e-Contract |  |  |  |  |  |  |  |  |
| 24 | Contact Number | เบอร์โต๊ะผู้ขอ |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  | เบอร์โต๊ะผู้ขอ (Contact Number) |  |  | Ref: e-Contract |  |  |  |  |  |  |  |  |
| 25 | Emergency Contact |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  | Emergency Contact |  |  | Ref: e-Contract |  |  |  |  |  |  |  |  |
| 26 | Emergency Tel |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  | Emergency Tel |  |  | Ref: e-Contract |  |  |  |  |  |  |  |  |
| 27 | ชื่อนามสกุลหัวหน้าผู้ขอเปิดงาน | ชื่อนามสกุลหัวหน้าผู้ขอเปิดงาน |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  | ชื่อนามสกุลหัวหน้าผู้ขอเปิดงาน |  |  | Ref: e-Contract |  |  |  |  |  |  |  |  |
| 28 | LGC No. | เลขที่สัญญา |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  | เลขที่สัญญา (LGC No.) |  |  | Ref: e-Contract |  |  |  |  |  |  |  |  |
| 29 | LG No. | เลขที่งาน |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  | เลขที่งาน (LG No.) |  |  | Ref: e-Contract |  |  |  |  |  |  |  |  |
| 30 | Revision | เลขฉบับแก้ไข |  |  |  |  | KPS_T_CONTRACT KPS_T_CONTRACT_REVISE | CONT_NO REVISE_NO | VARCHAR2 VARCHAR2 | 30 10 | N N | Ready |  |  |  |  | เลขฉบับแก้ไข (Revision) |  |  | Ref: e-Contract |  |  |  |  |  |  |  |  |
| 31 | Contract Type | ประเภทสัญญา |  |  |  |  | KPS_T_CONTRACT | CONT_TYPE | VARCHAR2 | 10 | Y | Ready |  |  |  |  | ประเภทสัญญา (Contract Type) |  |  | Ref: e-Contract |  |  |  |  |  |  |  |  |
| 32 | Corporate Name | ชื่อกลุ่มบริษัท |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  | ชื่อกลุ่มบริษัท (Corporate Name) |  |  | Ref: e-Contract |  |  |  |  |  |  |  |  |
| 33 | Authorized signatory | ผู้มีอำนาจลงนาม |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  | ผู้มีอำนาจลงนาม (Authorized signatory) |  |  | Ref: e-Contract |  |  |  |  |  |  |  |  |
| 34 | Purpose | วัตถุประสงค์การทำสัญญา |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  | วัตถุประสงค์การทำสัญญา (Purpose)  |  |  | Ref: e-Contract |  |  |  |  |  |  |  |  |
| 35 | Contract Value | มูลค่าสัญญา |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  | มูลค่าสัญญา (Contract Value) |  |  | Ref: e-Contract |  |  |  |  |  |  |  |  |
| 36 | Supplier's Corporate Name (EN) | ชื่อเต็มบริษัทคู่สัญญาภาษาอังกฤษ |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  | ชื่อเต็มบริษัทคู่สัญญาภาษาอังกฤษ (Supplier's coporate name) |  |  | บริษัทที่ทำสัญญากับ KP |  |  |  |  |  |  |  |  |
| 37 | Supplier's Corporate Name (TH) | ชื่อเต็ทมบริษัทคู่สัญญาภาษาไทย |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  | ชื่อเต็ทมบริษัทคู่สัญญาภาษาไทย (Supplier's coporate name) |  |  | บริษัทที่ทำสัญญากับ KP |  |  |  |  |  |  |  |  |
| 38 | Supplier's Corporate Address | ที่อยู่บริษัท |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  | ที่อยู่บริษัท (Supplier's coporate address) |  |  | Ref: e-Contract |  |  |  |  |  |  |  |  |
| 39 | Supplier's Short Name (EN) | ชื่อย่อบริษัทคู่สัญญาภาษาอังกฤษ |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  | ชื่อย่อบริษัทคู่สัญญาภาษาอังกฤษ |  |  | Ref: e-Contract |  |  |  |  |  |  |  |  |
| 40 | Supplier's Short Name (TH) | ชื่อย่อบริษัทคู่สัญญาภาษาไทย |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  | ชื่อย่อบริษัทคู่สัญญาภาษาไทย |  |  | Ref: e-Contract |  |  |  |  |  |  |  |  |
| 41 | Comment | ข้อมูลเพิ่มเติม |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  | ข้อมูลเพิ่มเติม |  |  | Ref: e-Contract |  |  |  |  |  |  |  |  |
| 42 | Supplier's Email Contact | อีเมลผู้ติดต่อฝั่งคู่สัญญา |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  | อีเมลผู้ติดต่อฝั่งคู่สัญญา |  |  | Ref: e-Contract |  |  |  |  |  |  |  |  |
| 43 | Opportunity |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 44 | Submit to e-Contract Date |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 45 | Receive Contract Form Date |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 46 | Send Contract to Tenant Date |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Contract Period |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 47 | Period |  |  |  |  |  | Hard code  -Year |  |  |  |  | Ready | Y | Picklist | Yes | - Month - Year | ช่วงสัญญา | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 48 | Value |  |  |  |  |  | KPS_T_CONTRACT | CONT_PERIOD_YEAR | NUMBER | 2,0 | N | Ready | Y | Number | Yes | 10 เดือน | จำนวน | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 49 | Contract Sign Date |  |  |  |  |  | KPS_T_CONTRACT | CONT_DATE | DATE | 7 | Y | Ready | Y | Date | Yes | 28/09/2020 | วันที่เซ็นสัญญา เช่น  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 50 | Contract Start Date |  |  |  |  |  | KPS_T_CONTRACT | CONT_STR_DATE | DATE | 7 | N | Ready | Y | Date | Yes | 28/09/2020 | วันที่จดทะเบียนผู้ประกอบการ | Confirmed |  | - รูปแบบ: DD/MM/YYYY เป็น คริสต์ศักราช |  |  |  |  |  |  |  |  |
| 51 | Contract End Date |  |  |  |  |  | KPS_T_CONTRACT | CONT_END_DATE | DATE | 7 | N | Ready | Y | Date | Yes | 28/09/2020 | วันที่จดทะเบียนผู้ประกอบการ | Confirmed |  | - รูปแบบ: DD/MM/YYYY เป็น คริสต์ศักราช |  |  |  |  |  |  |  |  |
| Shop |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 52 | Shop Branch Code |  |  |  |  |  | KPS_T_CONT_SHOP_UNIT | BRANCH_CODE | VARCHAR2 | 20 | N | Ready | Y | Text | Yes |  | รหัสร้านค้าผู้ประกอบการ | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 53 | Shop Branch Name |  |  |  |  |  | KPS_R_BRANCH | BRANCH_NAME_T | VARCHAR2 | 200 | Y | Ready | Y | Text | Yes |  | ชื่อร้านค้าผู้ประกอบการ | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 54 | Open Date |  |  |  |  |  | KPS_T_CONT_SHOP_UNIT | SHOP_STR_DATE | DATE | 7 | Y | Ready | Y | Date | Yes |  | วันที่เปิดร้าน | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 55 | Closed |  |  |  |  |  | KPS_T_CONT_SHOP_UNIT | SHOP_END_DATE | DATE | 7 | Y | Ready | Y | Date | Yes |  | วันที่ปิดร้าน | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 56 | Shop Brand Code |  |  |  |  |  | KPS_T_CONT_TENT_SHOPBRAND | SHPBND_CODE | VARCHAR2 | 4 | N | Ready | Y | Text | Yes |  | รหัสแบรนด์ของผู้ประกอบการ | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 57 | Shop Brand Name - TH |  |  |  |  |  | KPS_T_CONT_TENT_SHOPBRAND.KPS_R_SHOP_BRAND | SHPBND_NAME_T | VARCHAR2 | 60 | Y | Ready | Y | Text | Yes |  | ชื่อแบรนด์ ภาษาไทย | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 58 | Shop Brand Name - EN |  |  |  |  |  | KPS_T_CONT_TENT_SHOPBRAND.KPS_R_SHOP_BRAND | SHPBND_NAME_E | VARCHAR2 | 60 | Y | Ready | Y | Text | Yes |  | ชื่อแบรนด์ ภาษาอังกฤษ | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 59 | Brand Status |  |  |  |  |  | KPS_T_CONT_TENT_SHOPBRAND.KPS_R_SHOP_BRAND | STATUS(1=Active,2=Inactive) | NUMBER | 1 | Y | Ready | Y | Text | Yes | - Active - Inactive |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 60 | Remark |  |  |  |  |  | KPS_T_CONTRACT | CONT_REMARK | VARCHAR2 | 500 | Y | Ready | Y | Text |  |  | หมายเหตุ | Confirmed |  |  |  |  |  |  |  |  |  |  |
| Contract Unit |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 61 | Original Unit No. |  |  |  |  |  | ไม่มีใน TMS  | SRC_UNIT | VARCHAR2 | 15 | N | Ready | Y | Text | Yes |  | เลขที่ Unit จากแหล่งข้อมูล | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 62 | KPS Unit No. |  |  |  |  |  | KPS_T_CONT_SHOP_UNIT | SHOP_UNIT | VARCHAR2 | 15 | N | Ready | Y | Text | Yes |  | เลขที่ Unit ของ KPS | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 63 | Floor |  |  |  |  |  | KPS_R_SHOPUNIT | LEVEL_CODE | VARCHAR2 | 3 | Y | Ready | Y | Text | Yes |  | ชั้น | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 64 | Building |  |  |  |  |  | KPS_R_SHOPUNIT | B_CODE | VARCHAR2 | 3 | Y | Ready | Y | Text | Yes |  | ตึก | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 65 | Wing |  |  |  |  |  | KPS_R_SHOPUNIT | W_CODE | VARCHAR2 | 3 | Y | Ready | Y | Text | Yes |  | วิง | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 66 | Zone |  |  |  |  |  | KPS_R_SHOPUNIT | ZONE_CODE | VARCHAR2 | 3 | Y | Ready | Y | Text | Yes |  | โซน | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 67 | Start Date |  |  |  |  |  | KPS_R_SHOPUNIT | START_DATE | DATE | 7 | Y | Ready | Y | Date | Yes |  |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 68 | Cancel Date |  |  |  |  |  | KPS_R_SHOPUNIT | END_DATE | DATE | 7 | Y | Ready | Y | Date | No |  |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 69 | Cancel Remark |  |  |  |  |  | KPS_R_SHOPUNIT | END_REASON | VARCHAR2 | 200 | Y | Ready | Y | Text | No |  |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| Actual Area |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 70 | Total Area |  |  |  |  |  | KPS_R_SHOPUNIT | ACT_TOT_AREA | NUMBER | 16,3 | Y | Ready | Y | Number(1,3) | Yes | 5.000 |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 71 | Commercial Area |  |  |  |  |  | KPS_R_SHOPUNIT | ACT_COMM_AREA | NUMBER | 16,3 | Y | Ready | Y | Number(1,3) | Yes | 5.000 |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 72 | M&E Area |  |  |  |  |  | KPS_R_SHOPUNIT | ACT_ME_AREA | NUMBER | 16,3 | Y | Ready | Y | Number(1,3) | Yes | 0.000 |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 73 | Store Area |  |  |  |  |  | KPS_R_SHOPUNIT | ACT_STORE_AREA | NUMBER | 16,3 | Y | Ready | Y | Number(1,3) | Yes | 0.000 |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 74 | Other Area |  |  |  |  |  | ไม่มีใน TMS |  |  |  |  | Ready | Y | Number(1,3) | Yes | 0.000 |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| Contract Area |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 75 | Total Area |  |  |  |  |  | KPS_R_BRANCH | AREA | NUMBER | 16,3 | Y | Ready | Y | Number(1,3) | Yes | 5.000 |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 76 | Commercial Area |  |  |  |  |  | KPS_R_BRANCH | COMM_AREA | NUMBER | 16,3 | Y | Ready | Y | Number(1,3) | Yes | 5.000 |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 77 | M&E Area |  |  |  |  |  | KPS_R_BRANCH | MNE_AREA | NUMBER | 16,3 | Y | Ready | Y | Number(1,3) | Yes | 0.000 |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 78 | Store Area |  |  |  |  |  | KPS_R_BRANCH | STORE_AREA | NUMBER | 16,3 | Y | Ready | Y | Number(1,3) | Yes | 0.000 |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 79 | Other Area |  |  |  |  |  | KPS_R_BRANCH | OTH_AREA | NUMBER | 16,3 | Y | Ready | Y | Number(1,3) | Yes | 0.000 |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| Information |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 80 | Shop Open Date Criteria |  | <New> |  |  |  | ไม่มีใน TMS  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 81 | Expected Open Date |  | <New> |  |  |  | ไม่มีใน TMS  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 82 | Deposit for reservation (inc. VAT) |  | <New> |  |  |  | ไม่มีใน TMS  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 83 | Minimum Guarantee Adjustment Condition |  | <New> |  |  |  | ไม่มีใน TMS  |  |  |  |  | New | Y |  |  | - % Passenger Growth - Fixed Rate - Fixed Amount | เงื่อนไขการปรับฐานส่วนแบ่งรายได้ขั้นต่ำ |  |  |  |  |  |  |  |  |  |  |  |
| 84 | Inflation Rate |  | <New> |  |  |  | ไม่มีใน TMS  |  |  |  |  | New | Y |  |  | อัตราเงินเฟ้อ |  |  |  |  |  |  |  |  |  |  |  |  |
| 85 | Criteria |  | <New> |  |  |  | ไม่มีใน TMS  |  |  |  |  | New | Y |  |  | วันที่เริ่มปรับส่วนแบ่งรายได้ขั้นต่ำ - วันที่เปิดร้านครบ 12 เดือน - วันที่ครบรอบปีงบประมาณ - วันที่ … (ระบุ) | วันที่เริ่มปรับฐานส่วนแบ่งรายได้ขั้นต่ำ |  |  |  |  |  |  |  |  |  |  |  |
| 86 | Upfront Criteria | เงื่อนไขการตัดชำระ of จำนวนเงินชำระล่วงหน้า (Upfront) | <New> |  |  |  | ไม่มีใน TMS  |  |  |  |  | New | Y |  |  | - ค่าเช่า - ส่วนแบ่งรายได้ |  |  |  |  |  |  |  |  |  |  |  |  |
| 87 | Upfront Period | ช่วงเวลาการตัดชำระ (from-to) of จำนวนเงินชำระล่วงหน้า (Upfront) | <New> |  |  |  | ไม่มีใน TMS  |  |  |  |  | New | Y |  |  | 07/25 - 12/25 |  |  |  |  |  |  |  |  |  |  |  |  |
| 88 | Upfront Amount | จำนวนเงิน of จำนวนเงินชำระล่วงหน้า (Upfront) | <New> |  |  |  | ไม่มีใน TMS  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 89 | Upfront Balance | จำนวนเงินคงเหลือ of จำนวนเงินชำระล่วงหน้า (Upfront) | <New> |  |  |  | ไม่มีใน TMS  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 90 | Discount Criteria | เงือนไข of Discount | <New> |  |  |  | ไม่มีใน TMS  |  |  |  |  | New | Y |  |  | - ค่าเช่า - ส่วนแบ่งรายได้ |  |  |  |  |  |  |  |  |  |  |  |  |
| 91 | Dicsount Amount | จำนวน (เงิน/%) of Discount | <New> |  |  |  | ไม่มีใน TMS  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 92 | Dicsount Period | ช่วงเวลาการให้ส่วนลด (from-to) of Discount | <New> |  |  |  | ไม่มีใน TMS  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 93 | หลักประกันสัญญาอนุญาติ |  | <New> |  |  |  | ไม่มีใน TMS  |  |  |  |  | New | Y |  |  | - Bank Guarantee - Cash  - Cheque |  |  |  |  |  |  |  |  |  |  |  |  |
| 94 | Collateral Agreement Period | Period of หลักประกันสัญญาอนุญาติ | <New> |  |  |  | ไม่มีใน TMS  |  |  |  |  | New | Y |  |  | - เดือน - ปี |  |  |  |  |  |  |  |  |  |  |  |  |
| 95 | Collateral Agreement No. | No. of หลักประกันสัญญาอนุญาติ | <New> |  |  |  | ไม่มีใน TMS  |  |  |  |  | New | Y |  |  | - 1 - 2 |  |  |  |  |  |  |  |  |  |  |  |  |
| 96 | Collateral Agreement Bank Name | Bank Name of หลักประกันสัญญาอนุญาติ | <New> |  |  |  | ไม่มีใน TMS  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 97 | Collateral Agreement Start Date | Start Date of หลักประกันสัญญาอนุญาติ | <New> |  |  |  | ไม่มีใน TMS  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 98 | Collateral Agreement End Date | End Date of หลักประกันสัญญาอนุญาติ | <New> |  |  |  | ไม่มีใน TMS  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 99 | Collateral Agreement Amount | Amount of หลักประกันสัญญาอนุญาติ | <New> |  |  |  | ไม่มีใน TMS  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 100 | Collateral Agreement Remark | Remark of หลักประกันสัญญาอนุญาติ | <New> |  |  |  | ไม่มีใน TMS  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 101 | Rent (THB/sq.m./month) | Rental Rate | <New> |  |  |  | ไม่มีใน TMS  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 102 | % Building Usage Fee | ค่าบริการการใช้อาคาร | <New> |  |  |  | ไม่มีใน TMS  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 103 | % Property Tax | ภาษีที่ดิน และสิ่งปลูกสร้าง | <New> |  |  |  | ไม่มีใน TMS  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 104 | W/O VAT Collateral Agreement |  หลักประกันสัญญาอนุญาติ - เงินสด (excl. VAT) | <New> |  |  |  | ไม่มีใน TMS  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 105 | VAT Collateral Agreement |  หลักประกันสัญญาอนุญาติ - เงินสด (incl. VAT) | <New> |  |  |  | ไม่มีใน TMS  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 106 | Collateral Agreement |  หลักประกันสัญญาอนุญาติ - เงินสด (incl. VAT) | <New> |  |  |  | ไม่มีใน TMS  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 107 | Rental Deposit | เงินประกันค่าเช่าพื้นที่ (excl. VAT) | <New> |  |  |  | ไม่มีใน TMS  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 108 | เงินประกันค่าเช่าพื้นที่  (incl. VAT) | เงินประกันค่าเช่าพื้นที่  (incl. VAT) | <New> |  |  |  | ไม่มีใน TMS  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 109 | เงินประกันค่าเช่าพื้นที่  (incl. VAT) | เงินประกันค่าเช่าพื้นที่  (incl. VAT) | <New> |  |  |  | ไม่มีใน TMS  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 110 | W/O VAT Building Usage Fee Deposit | เงินประกันค่าบริการใช้อาคาร (excl. VAT) | <New> |  |  |  | ไม่มีใน TMS  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 111 | VAT Building Usage Fee Deposit | เงินประกันค่าบริการใช้อาคาร (incl. VAT) | <New> |  |  |  | ไม่มีใน TMS  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 112 | Building Usage Fee Deposit | เงินประกันค่าบริการใช้อาคาร (incl. VAT) | <New> |  |  |  | ไม่มีใน TMS  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 113 | Property Tax (One-Time) | เงินประกันภาษีที่ดินและสิ่งปลูกสร้าง (excl. VAT) | <New> |  |  |  | ไม่มีใน TMS  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 114 | เงินประกันภาษีที่ดินและสิ่งปลูกสร้าง (excl. VAT) | เงินประกันภาษีที่ดินและสิ่งปลูกสร้าง (excl. VAT) | <New> |  |  |  | ไม่มีใน TMS  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 115 | เงินประกันภาษีที่ดินและสิ่งปลูกสร้าง (incl. VAT) | เงินประกันภาษีที่ดินและสิ่งปลูกสร้าง (incl. VAT) | <New> |  |  |  | ไม่มีใน TMS  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 116 | รวมหลักประกันสัญญาเช่า | รวมหลักประกันสัญญาเช่า | <New> |  |  |  | ไม่มีใน TMS  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 117 | รวมเงินทำสัญญา (excl. VAT) | รวมเงินทำสัญญา (excl. VAT) | <New> |  |  |  | ไม่มีใน TMS  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 118 | รวมเงินทำสัญญา (incl. VAT) | รวมเงินทำสัญญา (incl. VAT) | <New> |  |  |  | ไม่มีใน TMS  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 119 | รวมเงินทำสัญญา รวม VAT | รวมเงินทำสัญญา รวม VAT | <New> |  |  |  | ไม่มีใน TMS  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 120 | Minimum Guarantee (excl. VAT) |  | <New> |  |  |  | ไม่มีใน TMS  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 121 | Minimum Guarantee (incl. VAT) |  | <New> |  |  |  | ไม่มีใน TMS  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 122 | Minimum Guarantee (incl. VAT) |  | <New> |  |  |  | ไม่มีใน TMS  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 123 | Rental Fee (excl. VAT) |  | <New> |  |  |  | ไม่มีใน TMS  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 124 | Rental Fee (incl. VAT) |  | <New> |  |  |  | ไม่มีใน TMS  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 125 | Rental Fee (incl. VAT) |  | <New> |  |  |  | ไม่มีใน TMS  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 126 | Service Fee (exc. VAT) |  | <New> |  |  |  | ไม่มีใน TMS  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 127 | Service Fee (incl. VAT) |  | <New> |  |  |  | ไม่มีใน TMS  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 128 | Service Fee (incl. VAT) |  | <New> |  |  |  | ไม่มีใน TMS  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 129 | Total Monthly Fee (exc. VAT) |  | <New> |  |  |  | ไม่มีใน TMS  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 130 | Total Monthly Fee (incl. VAT) |  | <New> |  |  |  | ไม่มีใน TMS  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 131 | Total Monthly Fee (incl. VAT) |  | <New> |  |  |  | ไม่มีใน TMS  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 132 | Contract Status |  | <New> |  |  |  | ไม่มีใน TMS  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 133 | LG Contract No. |  | <New> |  |  |  | ไม่มีใน TMS  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 134 | Shop Layout |  | <New> |  |  |  | ไม่มีใน TMS  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 135 | Shop Image |  | <New> |  |  |  | ไม่มีใน TMS  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 136 | เงินประกันตกแต่ง |  | <New> |  |  |  | ไม่มีใน TMS  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 137 | Shop Handover Date |  | <New> |  |  |  | ไม่มีใน TMS  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 138 | Shop Open Date (Protocol) |  | <New> |  |  |  | ไม่มีใน TMS  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 139 | Shop Open Date (Actual) |  | <New> |  |  |  | ไม่มีใน TMS  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 140 | Last Revenue Sharing Date |  | <New> |  |  |  | ไม่มีใน TMS  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 141 | Shop Return Date |  | <New> |  |  |  | ไม่มีใน TMS  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 142 | Shop Closure Date |  | <New> |  |  |  | ไม่มีใน TMS  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 143 | Shop Closed Reason |  | <New> |  |  |  | ไม่มีใน TMS  |  |  |  |  | New | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |

---

## 07_Sub Contract

| No. | SFDC Field Name (EN) | SFDC Field Name (TH) | Source Field API Name | Source Field Type | Source Field Length | VULLABLE (N=Required) | KP Table | KP Field Name | KP Field Type | KP Field Length | VULLABLE (N=Required).1 | Progress | Confirm | Type | Required | Sample Data | Description | Status | User/KP Feedback | Remark | Help Text | Track History | External ID | Track History.1 | Encrypted | Page Layout | Length | Source Field API Name.1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Information |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 1 | Concession No. |  | CON_CODE | CHAR | 2.0 | N | KPS_T_CONT_SUB_CONT KPS_R_CONCESS | CON_CODE CON_LNAME | CHAR VARCHAR2 | 2 100 | N N | Ready |  |  | Yes | 09 – SVB Terminal 1 | เลขสัมปทาน  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 2 | Master Contract No. |  | CONT_NO | VARCHAR2 | 30.0 | N | KPS_T_CONT_SUB_CONT | CONT_NO | VARCHAR2 | 30 | N | Ready |  |  | Yes | KPS 14/2564 | เลขที่สัญญาหลัก | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 3 | Company Code |  | SHOP_CODE | CHAR | 18.0 | Y | KPS_T_CONT_SUB_CONT KPS_T_CONTRACT | CONT_NO SHOP_CODE | VARCHAR2 VARCHAR2 | 30 20 | N Y | Ready |  |  | Yes | 0903001 | รหัสบริษัทตามสัญญาหลัก | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 4 | Company Name |  | <New> |  |  |  | KPS_T_CONT_SUB_CONT KPS_T_CONTRACT KPS_R_SHOP | CONT_NO SHOP_CODE SHOP_NAME_T | VARCHAR2 VARCHAR2 VARCHAR2 | 30 20 200 | N Y Y | New |  |  | Yes | บริษัท คิง พาวเวอร์ แท็กซ์ฟรี จำกัด | ชื่อบริษัทตามสัญญาหลัก | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 5 | Sub-Contract No. |  | SUB_CONT_NO | CHAR | 18.0 | Y | KPS_T_CONT_SUB_CONT | SUBCONT_NO | VARCHAR2 | 30 | N | Ready |  |  | Yes | KPT-S-14/2564 | เลขที่สัญญา Sub Contract | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 6 | Sub-Contractor - Company Code |  | <New> |  |  |  | KPS_T_CONT_SUB_CONT | SHOP_CODE | VARCHAR2 | 20 | Y | New |  |  | Yes | 0903012 | เลขที่ผู้ประกอบการ | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 7 | Sub-Contractor - Company Name |  | <New> |  |  |  | KPS_T_CONT_SUB_CONT KPS_R_SHOP | SHOP_CODE SHOP_NAME_T | VARCHAR2 VARCHAR2 | 20 200 | Y Y | New |  |  | Yes | บริษัท ซีพี ออลล์ จำกัด (มหาชน) | ชื่อผู้ประกอบการ  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 8 | Contract Area |  | <New> |  |  |  | KPS_T_CONT_SUB_CONT | SUBCONT_AREA | NUMBER | 16,3 | Y | New |  |  |  |  |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 9 | Sub-Contract Status |  | <New> |  |  |  | ไม่มี |  |  |  |  | New |  |  |  |  | สถานะสัญญา Sub-Contract | Confirmed |  |  |  |  |  |  |  |  |  |  |
| Contract Period |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 10 | Period |  | CONT_DATE | CHAR | 10.0 | Y | Hard code  -Year |  |  |  |  | Ready |  | Picklist | Yes | - Month - Year | ช่วงสัญญา | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 11 | Value |  | NUM_YEAR | NUMBER | 22.0 | Y | KPS_T_CONT_SUB_CONT | SUBCONT_PERIOD | NUMBER | 2,0 | Y | Ready |  | Number | Yes | 10 เดือน | จำนวน | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 12 | Contract Sign Date |  | CONT_DATE | CHAR | 10.0 | Y | KPS_T_CONT_SUB_CONT | SUBCONT_SIGN_DATE | DATE | 7 | Y | Ready |  | Date | Yes | 28/09/2020 | วันที่เซ็นสัญญา เช่น  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 13 | Contract Start Date |  | CONT_STR_DATE | CHAR | 10.0 | Y | KPS_T_CONT_SUB_CONT | SUBCONT_STR_DATE | DATE | 7 | Y | Ready |  | Date | Yes | 28/09/2020 | วันที่จดทะเบียนผู้ประกอบการ | Confirmed |  | - รูปแบบ: DD/MM/YYYY เป็น คริสต์ศักราช |  |  |  |  |  |  |  |  |
| 14 | Contract End Date |  | CONT_END_DATE | CHAR | 10.0 | Y | KPS_T_CONT_SUB_CONT | SUBCONT_END_DATE | DATE | 7 | Y | Ready |  | Date | Yes | 28/09/2020 | วันที่จดทะเบียนผู้ประกอบการ | Confirmed |  | - รูปแบบ: DD/MM/YYYY เป็น คริสต์ศักราช |  |  |  |  |  |  |  |  |
| Shop |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 15 | Shop Branch Code |  | <New> |  |  |  | KPS_T_CONT_SUB_CONT KPS_T_CONT_SUB_CONT KPS_T_CONT_SHOP_UNIT | CONT_NO SUBCONT_NO BRANCH_CODE | VARCHAR2 VARCHAR2 VARCHAR2 | 30 30 20 | N N N | New |  | Text | Yes |  | รหัสร้านค้าผู้ประกอบการ | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 16 | Shop Branch Name |  | <New> |  |  |  | KPS_T_CONT_SUB_CONT KPS_T_CONT_SUB_CONT KPS_T_CONT_SHOP_UNIT KPS_R_BRANCH | CONT_NO SUBCONT_NO BRANCH_CODE BRANCH_NAME_T | VARCHAR2 VARCHAR2 VARCHAR2 VARCHAR2 | 30 30 20 200 | N N N Y | New |  | Text | Yes |  | ชื่อร้านค้าผู้ประกอบการ | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 17 | Open Date |  | <New> |  |  |  | KPS_T_CONT_SHOP_UNIT | SHOP_STR_DATE | DATE | 7 | Y | New |  | Date | Yes |  | วันที่เปิดร้าน | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 18 | Closed |  | <New> |  |  |  | KPS_T_CONT_SHOP_UNIT | SHOP_END_DATE | DATE | 7 | Y | New |  | Date | Yes |  | วันที่ปิดร้าน | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 19 | Shop Brand Code |  | <New> |  |  |  | KPS_T_CONT_SUB_CONT KPS_T_CONT_SUB_CONT KPS_T_CONT_SHOP_UNIT KPS_T_CONT_TENT_SHOPBRAND | CONT_NO SHOP_CODE BRANCH_CODE SHPBND_CODE | VARCHAR2 VARCHAR2 VARCHAR2 SHPBND_CODE | 30 20 20 4 | N Y N N | New |  | Text | Yes |  | รหัสแบรนด์ของผู้ประกอบการ | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 20 | Shop Brand Name - TH |  | <New> |  |  |  | KPS_R_SHOP_BRAND | SHPBND_NAME_T | VARCHAR2 | 60 | Y | New |  | Text | Yes |  | ชื่อแบรนด์ ภาษาไทย | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 21 | Shop Brand Name - EN |  | <New> |  |  |  | KPS_R_SHOP_BRAND | SHPBND_NAME_E | VARCHAR2 | 60 | Y | New |  | Text | Yes |  | ชื่อแบรนด์ ภาษาอังกฤษ | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 22 | Brand Status |  | <New> |  |  |  | KPS_R_SHOP_BRAND | STATUS (1=active, 2 =inactive) | NUMBER | 1 | Y | New |  | Text | Yes | - Active - Inactive |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 23 | Remark |  | <New> |  |  |  | KPS_T_CONT_SUB_CONT | REMARK_T | VARCHAR2 | 500 | Y | New |  | Text |  |  | หมายเหตุ | Confirmed |  |  |  |  |  |  |  |  |  |  |
| Contract Unit |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 24 | Original Unit No. |  | <New> |  |  |  | KPS_T_CONT_SHOP_UNIT | SHOP_UNIT | VARCHAR2 | 15 | N | New |  | Text | Yes |  | เลขที่ Unit จากแหล่งข้อมูล | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 25 | KPS Unit No. |  | <New> |  |  |  | KPS_T_SRC_UNIT | SRC_UNIT | VARCHAR2 | 15 | N | New |  | Text | Yes |  | เลขที่ Unit ของ KPS | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 26 | Floor |  | <New> |  |  |  | KPS_T_CONT_SHOP_UNIT KPS_R_SHOPUNIT | SHOP_UNIT LEVEL_CODE | VARCHAR2 VARCHAR2 | 15 3 | N Y | New |  | Text | Yes |  | ชั้น | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 27 | Building |  | <New> |  |  |  | KPS_T_CONT_SHOP_UNIT KPS_R_SHOPUNIT | SHOP_UNIT B_CODE | VARCHAR2 VARCHAR2 | 15 3 | N Y | New |  | Text | Yes |  | ตึก | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 28 | Wing |  | <New> |  |  |  | KPS_T_CONT_SHOP_UNIT KPS_R_SHOPUNIT | SHOP_UNIT W_CODE | VARCHAR2 VARCHAR2 | 15 3 | N Y | New |  | Text | Yes |  | วิง | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 29 | Zone |  | <New> |  |  |  | KPS_T_CONT_SHOP_UNIT KPS_R_SHOPUNIT | SHOP_UNIT ZONE_CODE | VARCHAR2 VARCHAR2 | 15 3 | N Y | New |  | Text | Yes |  | โซน | Confirmed |  |  |  |  |  |  |  |  |  |  |
| Address |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 30 | Building / Village |  | <New> |  |  |  | KPS_T_CONT_SUB_CONT KPS_R_SHOP KPS_R_SHOP | SHOP_CODE LOC_BUILDING LOC_VILLAGE | VARCHAR2 VARCHAR2 VARCHAR2 | 20 60 60 | Y Y Y | New |  |  | Yes |  | หมู่บ้าน | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 31 | Address No. |  | <New> |  |  |  | KPS_T_CONT_SUB_CONT KPS_R_SHOP | SHOP_CODE LOC_ADDRESS_NO | VARCHAR2 VARCHAR2 | 20 50 | Y Y | New |  |  | Yes |  | เลขที่ | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 32 | Soi |  | <New> |  |  |  | KPS_T_CONT_SUB_CONT KPS_R_SHOP | SHOP_CODE LOC_SOI | VARCHAR2 VARCHAR2 | 20 50 | Y Y | New |  |  | Yes |  | ซอย | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 33 | Street |  | <New> |  |  |  | KPS_T_CONT_SUB_CONT KPS_R_SHOP | SHOP_CODE LOC_STREET | VARCHAR2 VARCHAR2 | 20 50 | Y Y | New |  |  | Yes |  | ถนน | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 34 | Sub-District |  | <New> |  |  |  | KPS_T_CONT_SUB_CONT KPS_R_SHOP | SHOP_CODE LOC_SUB_DISTRICT | VARCHAR2 VARCHAR2 | 20 50 | Y Y | New |  |  | Yes |  | ตำบล | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 35 | District |  | <New> |  |  |  | KPS_T_CONT_SUB_CONT KPS_R_SHOP | SHOP_CODE LOC_DISTRICT_CODE | VARCHAR2 VARCHAR2 | 20 3 | Y Y | New |  |  | Yes |  | อำเภอ | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 36 | Province |  | <New> |  |  |  | KPS_T_CONT_SUB_CONT KPS_R_SHOP | SHOP_CODE LOC_PROV_CODE | VARCHAR2 VARCHAR2 | 20 2 | Y Y | New |  |  | Yes |  | จังหวัด | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 37 | Zip Code |  | <New> |  |  |  | KPS_T_CONT_SUB_CONT KPS_R_SHOP | SHOP_CODE LOC_ZIPCODE | VARCHAR2 CHAR | 20 5 | Y Y | New |  |  | Yes |  | รหัสไปรษณีย์ | Confirmed |  |  |  |  |  |  |  |  |  |  |
| Revenue Sharing |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 38 | Revenue Sharing |  | <New> |  |  |  | KPS_T_CONT_SUB_CONT KPS_T_CONT_REV_SHR | CONT_NO REV_SHARE_RATE | VARCHAR2 NUMBER | 30 5,2 | N N | New |  |  |  |  | ส่วนแบ่งรายได้จากการประกอบกิจการ | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 39 | Effective Start Date |  | <New> |  |  |  | KPS_T_CONT_SUB_CONT KPS_T_CONT_REV_SHR | CONT_NO STR_DATE | VARCHAR2 DATE | 30 7 | N N | New |  |  |  |  | วันที่เริ่มต้น | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 40 | Effective End Date |  | <New> |  |  |  | KPS_T_CONT_SUB_CONT KPS_T_CONT_REV_SHR | CONT_NO END_DATE | VARCHAR2 DATE | 30 7 | N N | New |  |  |  |  | วันที่สิ้นสุด | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 41 | Remark |  | <New> |  |  |  | KPS_T_CONT_SUB_CONT KPS_T_CONT_REV_SHR | CONT_NO REMARK_T | VARCHAR2 VARCHAR2 | 30 200 | N Y | New |  |  |  |  | หมายเหตุ | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 42 | Minimum Guarantee per SQM. |  | <New> |  |  |  | ไม่มี |  |  |  |  | New |  |  |  |  | ส่วนแบ่งรายได้ขั้นต่ำ ต่อ ตารางเมตร | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 43 | Contract Year Start |  | <New> |  |  |  | KPS_T_CONT_SUB_CONT | SUBCONT_STR_DATE | DATE | 7 | Y | New |  |  |  |  | วันที่เริ่มต้นปีงบประมาณ | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 44 | Contract Year End |  | <New> |  |  |  | KPS_T_CONT_SUB_CONT | SUBCONT_END_DATE | DATE | 7 | Y | New |  |  |  |  | วันที่สิ้นสุดปีงบประมาณ | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 45 | No. of Day |  | <New> |  |  |  | KPS_T_CONT_SUB_CONT KPS_T_CONT_MIN_GUA | CONT_NO NUM_DAY | VARCHAR2 NUMBER | 30 4,0 | N N | New |  |  |  |  | จำนวนวัน | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 46 | Minimum Guarantee per day |  | <New> |  |  |  | KPS_T_CONT_SUB_CONT KPS_T_CONT_MIN_GUA | CONT_NO MIN_GUAR_D_AMT | VARCHAR2 NUMBER | 30 16,2 | N N | New |  |  |  |  | ส่วนแบ่งรายได้ขั้นต่ำ ต่อ ตารางเมตร ต่อวัน | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 47 | Minimum Guarantee Month Rate |  | <New> |  |  |  | KPS_T_CONT_SUB_CONT KPS_T_CONT_MIN_GUA | CONT_NO MIN_MONTH_RATE | VARCHAR2 NUMBER | 30 5,2 | N Y | New |  |  |  |  | อัตราสัดส่วนวันที่ประกอบกิจการ | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 48 | Remark |  | <New> |  |  |  | KPS_T_CONT_SUB_CONT KPS_T_CONT_MIN_GUA | CONT_NO REMARK_T | VARCHAR2 VARCHAR2 | 30 200 | N Y | New |  |  |  |  | หมายเหตุ | Confirmed |  |  |  |  |  |  |  |  |  |  |
|  |  |  | SEQ | NUMBER | 22.0 | N |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |

---

## 08_Contact

| No. | SFDC Field Name (EN) | SFDC Field Name (TH) | Source Field API Name | Source Field Type | Source Field Length | VULLABLE (N=Required) | KP Table | KP Field Name | KP Field Type | KP Field Length | VULLABLE (N=Required).1 | Progress | Confirm | Type | Required | Sample Data | Description | Status | User/KP Feedback | Help Text | Track History | External ID | Track History.1 | Encrypted | Page Layout | Length |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Information |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 1 | Concession | สัมปทาน | CON_CODE | CHAR | 2.0 | N | KPS_R_SHOP_CONT_PER KPS_R_CONCESS | CON_CODE CON_LNAME | CHAR VARCHAR2 | 2 100 | N N | Ready | Y |  | Yes | 09 : SVB 05 : DMK (Inter) 10 : DMK (DOM) 08 : HKT |  | Confirmed |  |  |  |  |  |  |  |  |
| 2 | Company Name | ชื่อบริษัท |  |  |  |  | KPS_R_SHOP_CONT_PER KPS_R_SHOP | SHOP_CODE SHOP_NAME_E | VARCHAR2 VARCHAR2 | 20 200 | N Y | Ready | Y |  | Yes | After You Public Company Limited |  | Confirmed |  |  |  |  |  |  |  |  |
| 3 | Shop Name | ชื่อร้านค้า |  |  |  |  | KPS_R_SHOP | SHORT_NAME | VARCHAR2 | 50 | Y | Ready | Y |  | Yes | After You |  | Confirmed |  |  |  |  |  |  |  |  |
| 4 | Unit No. |  |  |  |  |  | KPS_R_SHOP_CONT_PER KPS_R_SHOPUNIT | SHOP_CODE SHOP_UNIT | VARCHAR2 VARCHAR2 | 20 15 | N N | Ready |  |  |  | T1ME2-24 |  |  |  |  |  |  |  |  |  |  |
| 5 | Type of Contact | ประเภทของเรื่องที่ต้องติดต่อ |  |  |  |  | ไม่มี |  |  |  |  | Ready | Y |  | Yes | - ข้อร้องเรียน (CAC) - การขออนุมัติราคาสินค้าและบริการ (CAC)  - การตรวจร้านค้า (CAC) - การเข้าก่อสร้าง/เงิน (FAM) - หน้าร้าน Operation (FAM) - F&B (CAD) - Service (CAD) - Bank (CAD) - Airline Operations Contact (MKA) - Airline Finance Contact (MKA) - Merchant Operations Contact (MKA) - Merchant Finance Contact (MKA) - Passengers Complaint - Product & Price  - Shop Inspection - Supplier |  | Confirmed |  |  |  |  |  |  |  |  |
| 6 | Contact Person | ข้อมูลผู้ติดต่อ |  |  |  |  | KPS_R_SHOP_CONT_PER | CONT_NAME | VARCHAR2 | 50 | N | Ready | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 7 | Mobile | เบอร์โทรศัพท์ |  |  |  |  | KPS_R_SHOP_CONT_PER | CONT_PHONE_NO | VARCHAR2 | 30 | Y | Ready | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 8 | E-mail | อีเมล |  |  |  |  | KPS_R_SHOP_CONT_PER | CONT_EMAIL_ADDR | VARCHAR2 | 50 | Y | Ready | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 9 | Job Title | ตำแหน่ง |  |  |  |  | KPS_R_SHOP_CONT_PER | CONT_POST | VARCHAR2 | 50 | Y | Ready | Y |  |  | - เจ้าของ - หุ้นส่วน |  |  |  |  |  |  |  |  |  |  |
| 13 | Created Date | วันที่บันทึกข้อมูล |  |  |  |  | KPS_CAC_INSPECTION_INFORM_SEND | CREATEDDATE | DATE | 11 | Y | Ready | Y |  | Yes | 2025-12-18 00:00:00 |  | Confirmed |  |  |  |  |  |  |  |  |

---

## 09_Case

| No. | SFDC Field Name (EN) | SFDC Field Name (TH) | Unnamed: 3 | Unnamed: 4 | Unnamed: 5 | Unnamed: 6 | KP Table | KP Field Name | KP Field Type | KP Field Length | VULLABLE (N=Required) | Progress | Confirm | Type | Required | Sample Data | Source Field API Name | Description | Status | User/KP Feedback | Help Text | Track History | External ID | Encrypted | Page Layout | Length |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Information |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 1 | Concession | สัมปทาน |  |  |  |  |  |  |  |  |  | Ready |  |  | Yes | 09 : SVB 05 : DMK (Inter) 10 : DMK (DOM) 08 : HKT |  |  | Confirmed |  |  |  |  |  |  |  |
| 2 | Company Name | ชื่อบริษัท |  |  |  |  |  |  |  |  |  | Ready |  |  | Yes | After You Public Company Limited |  |  | Confirmed |  |  |  |  |  |  |  |
| 3 | Shop Name | ชื่อร้านค้า |  |  |  |  |  |  |  |  |  | Ready |  |  | Yes | After You |  |  | Confirmed |  |  |  |  |  |  |  |
| 4 | Branch Code | เลขสาขาของร้านค้า |  |  |  |  |  |  |  |  |  | Ready |  |  | Yes | 001 - T1ME2-24 |  |  | Confirmed |  |  |  |  |  |  |  |
| 5 | Unit No. | เลขที่ยูนิต |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 6 | Level | ชั้น |  |  |  |  |  |  |  |  |  | Ready |  |  | Yes | 2 |  |  | Confirmed |  |  |  |  |  |  |  |
| 7 | Location | สถานที่ตั้งของร้าน |  |  |  |  |  |  |  |  |  | Ready |  |  | Yes | Terminal , Conocurse A (แสดงข้อมูลตามแต่ละ Location ของร้านค้า) |  |  | Confirmed |  |  |  |  |  |  |  |
| 8 | Issue Date | วันที่แจ้งเตือน |  |  |  |  |  |  |  |  |  | #REF! |  |  | Yes | 2025-06-05 00:00:00 |  |  | Confirmed |  |  |  |  |  |  |  |
| 9 | Case Type | ประเภทแจ้งเตือน |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 10 | Subject | หัวข้อการแจ้งเตือน |  |  |  |  |  |  |  |  |  | Ready |  |  | Yes | - ทำผิดข้อกำหนดด้านราคา - ทำผิดข้อกำหนดด้านสุขาภิบาล - ทำผิดข้อกำหนดด้านข้อร้องเรียน |  |  | Confirmed |  |  |  |  |  |  |  |
| 11 | Topic | เรื่องที่แจ้งเตือน |  |  |  |  |  |  |  |  |  | Ready |  |  | Yes | แจ้งผลการตรวจสุขาภิบาลร้านอาหารภายในอาคารผู้โดยสาร ท่าอากาศยานสุวรรณภูมิ |  |  | Confirmed |  |  |  |  |  |  |  |
| 12 | Detail | รายละเอียดการแจ้งเตือน |  |  |  |  |  |  |  |  |  | Ready |  |  | Yes | 1. พบการปนเปื้อนเชื้อ Coliforms และ Escherichia coli ในน้ำแข็งสำหรับบริโภคเกินเกณฑ์ที่กำหนด 2. พบการปนเปื้อนเชื้อ Coliforms ในอาหารเกินเกณฑ์ที่กำหนด |  |  | Confirmed |  |  |  |  |  |  |  |
| 13 | Cause of Problem | การวิเคราะห์สาเหตุของปัญหา |  |  |  |  |  |  |  |  |  | Ready |  |  | Yes | การจัดเก็บน้ำแข็งและอาหารไม่สะอาด |  |  | Confirmed |  |  |  |  |  |  |  |
| 14 | Problem Resolution | แนวทางการแก้ไขในระยะสั้นและระยะยาว |  |  |  |  |  |  |  |  |  | Ready |  |  | Yes | แจ้งเตือนเป็นลายลักษณ์อักษรผ่านอีเมล |  |  | Confirmed |  |  |  |  |  |  |  |
| 15 | Resolution Status | สถานะการแก้ไข |  |  |  |  |  |  |  |  |  | Ready |  |  | Yes | - อยู่ระหว่างดำเนินการ - แก้ไขแล้วเสร็จ |  |  | Confirmed |  |  |  |  |  |  |  |
| 16 | Completion Date | วันที่ที่แก้ไขแล้วเสร็จ |  |  |  |  |  |  |  |  |  | Ready |  |  | Yes | 2025-06-05 00:00:00 |  |  | Confirmed |  |  |  |  |  |  |  |
| 17 | BU Owner | ผู้ดำเนินการ |  |  |  |  |  |  |  |  |  | Ready |  |  | Yes | CAC |  |  | Confirmed |  |  |  |  |  |  |  |
| 18 | Remarks | หมายเหตุ |  |  |  |  |  |  |  |  |  | Ready |  |  | No | ร้านค้าปิดให้บริการในวันที่ 31/12/2025 |  |  | Confirmed |  |  |  |  |  |  |  |
| 19 | Last FollowUp Date |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 20 | Last FollowUp Result |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 21 | Close Date |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 22 | Operate by |  |  |  |  |  |  |  |  |  |  |  |  |  |  | - CAD - MKA - CAC -FAM |  | หน่วยงํานที่รับผิดชอบ  |  |  |  |  |  |  |  |  |
| 23 | Reference ID |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Case ID กรณีที่เปิด case จํากระบบ workflow |  |  |  |  |  |  |  |  |

---

## 10_Reference Products

| No. | SFDC Field Name (EN) | SFDC Field Name (TH) | Unnamed: 3 | Unnamed: 4 | Unnamed: 5 | Unnamed: 6 | KP Table | KP Field Name | KP Field Type | KP Field Length | VULLABLE (N=Required) | Progress | Confirm | Type | Required | Sample Data | Description | Status | User/KP Feedback | Remark | Help Text | Track History | External ID | Track History.1 | Encrypted | Page Layout | Length | Source Field API Name |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Header |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 1 | Reference Product Source | แหล่งที่มาของสินค้าอ้างอิง |  |  |  |  | KPS_R_PROD_REF_SRC | REF_SRC_NAME | VARCHAR2 | 150 | N | Ready |  |  | Yes | - Reference จาก Mall/Hotel - Under bundle/set | ประเภทของ reference product เช่น  ** “Under bundle/set” หมายถึง ข้อมูลที่เกิดจากการกรอกในกรณีที่ user เพิ่ม เพื่อใส่ใน set bundle หรือรายการที่ไม่ขายหน้าร้าน | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 2 | Product Type | ประเภทของสินค้า |  |  |  |  | KPS_T_REQPROD_MD_ORG KPS_R_CATEGORY | STD_CATE_CODE  STD_CATE_DESC  Note: STD_CATE_CODE  เลขตำแหน่ง 0 เป็น PROD_CATE_CODE | VARCHAR2 VARCHAR2 | 4 200 | N N | Ready |  |  | No | 2 - Services 3 - Retails 5 - Food & Beverages | ปัจจุบันฝ่าย CAC ใช้แค่เลข 2, 3 และ 5 เท่านั้น | Confirmed |  | ขอให้สามารถกรอกได้ภายหลัง |  |  |  |  |  |  |  |  |
| 3 | Product Category Code | รหัสประเภทสินค้า |  |  |  |  | KPS_T_REQPROD_MD_ORG | STD_CATE_CODE (STD_CATE_CODE = PROD_CATE_CODE + PROD_SUBCAT1_CODE + PROD_SUBCAT2_CODE (รวม 4 ตัวอักษร)) | VARCHAR2 | 4 | N | Ready |  |  | No | 5ACC |  | Confirmed |  | 1. ร้าน Starbucks มี Product Category Code ไม่เหมือนร้านค้าอื่นบางประเภท (โปรดดูชีท Product Cat_ Starbucks) 2. ขอให้สามารถกรอกได้ภายหลัง |  |  |  |  |  |  |  |  |
| 4 | Product Sub Type | ประเภทย่อยของสินค้า |  |  |  |  | KPS_T_REQPROD_MD_ORG KPS_R_PROD_SUBCATE1 | STD_CATE_CODE  (ตัวที่ 1 = PROD_CATE_CODE  ตัวที่ 2 = PROD_SUBCAT1_CODE) PROD_SUBCAT1_DESC | VARCHAR2 VARCHAR2 | 4 200 | N Y | Ready |  |  | No | Thai Food |  | Confirmed |  | ขอให้สามารถกรอกได้ภายหลัง |  |  |  |  |  |  |  |  |
| 5 | Product Category Name - EN | ชื่อหมวดหมู่สินค้าภาษาอังกฤษ |  |  |  |  | KPS_T_REQPROD_MD_ORG KPS_R_PROD_SUBCATE2 | STD_CATE_CODE  (ตัวที่ 3-4 = PROD_SUBCAT2_CODE) PROD_SUBCAT2_DESC_EN | VARCHAR2 VARCHAR2 | 4 200 | N Y | Ready |  |  | No | Noodle - Fried |  | Confirmed |  | ขอให้สามารถกรอกได้ภายหลัง |  |  |  |  |  |  |  |  |
| 6 | Product Category Name - TH | ชื่อหมวดหมู่สินค้าภาษาไทย |  |  |  |  | KPS_R_PROD_SUBCATE2 | PROD_SUBCAT2_DESC | VARCHAR2 | 200 | Y | Ready |  |  | No | ก๋วยเตี๋ยวผัด |  | Confirmed |  | ขอให้สามารถกรอกได้ภายหลัง |  |  |  |  |  |  |  |  |
| 7 | Product Status | สถานะของสินค้า |  |  |  |  | KPS_R_PROD_SUBCATE2 | STATUS | NUMBER | 1,0 | Y | Ready |  |  | Yes | - Active - Inactive |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 8 | Attachment/Reference | ไฟล์รูปภาพเมนูสินค้าและข้อมูลอ้างอิง |  |  |  |  | ไม่มี |  |  |  |  | Ready |  |  | No | - Menu and Price |  | Confirmed |  | ขอให้สามารถเพิ่มได้ภายหลัง |  |  |  |  |  |  |  |  |
| Source of Product - Leading Department Store |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 9 | Product Name - TH | ชื่อสินค้าภาษาไทย |  |  |  |  | ไม่มี |  |  |  |  | Ready |  |  | No | ผัดไทยกุ้งสด | ถ้ามีชื่อสินค้าภาษาไทย ไม่ต้องมีชื่อสินค้าภาษาอังกฤษก็ได้ | Confirmed |  | ขอให้สามารถกรอกได้ภายหลัง |  |  |  |  |  |  |  |  |
| 10 | Product Name - EN | ชื่อสินค้าภาษาอังกฤษ |  |  |  |  | KPS_T_REQPROD_MD_ORG | PROD_SERV_NAME | VARCHAR2 | 200 | N | Ready |  |  | No | Pad Thai Rice Noodle & Shrimp | ถ้ามีชื่อสินค้าภาษาอังกฤษ ไม่ต้องมีชื่อสินค้าภาษาไทยก็ได้ | Confirmed |  | ขอให้สามารถกรอกได้ภายหลัง |  |  |  |  |  |  |  |  |
| 11 | Reference Source | ชื่อร้านค้าและห้างสรรพสินค้าที่ใช้อ้างอิง |  |  |  |  | KPS_T_REQPROD_MD_ORG KPS_T_REQPROD_MD_ORG   KPS_T_REQPROD_MD_ORG | CON_CODE SHOP_CODE เอา 2 ค่าบนไปหาค่า SHORT_NAME ใน KPS_R_SHOP  REF_SOURCE | CHAR VARCHAR2   VARCHAR2 | 2 20   100 | N N   Y | Ready |  |  | Yes | Coffee Beans by Dao - Siam Paragon |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 12 | Sale Price (Exclude VAT) | ราคาขายไม่รวมภาษีมูลค่าเพิ่ม |  |  |  |  | KPS_T_REQPROD_MD_ORG | REQ_PRICE_EXC_VAT | NUMBER | 16,2 | N | Ready |  |  | Yes | 261.682243 | กรณีระบุ Sell Price (Exclude VAT) ให้ระบบคำนวณ Sell Price (Include VAT) อัตโนมัติ | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 13 | VAT | ภาษีมูลค่าเพิ่ม |  |  |  |  | KPS_T_REQPROD_MD_ORG | VAT_RATE | NUMBER | 5,2 | N | Ready |  |  | No |  |  | Cancelled |  |  |  |  |  |  |  |  |  |  |
| 14 | Sale Price (Include VAT) | ราคาขายรวมภาษีมูลค่าเพิ่ม |  |  |  |  | KPS_T_REQPROD_MD_ORG | REQ_PRICE_INC_VAT | NUMBER | 16,2 | N | Ready |  |  | Yes | 280 | กรณีระบุ Sell Price (Include VAT) ให้ระบบคำนวณ Sell Price (Exclude VAT) อัตโนมัติ | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 15 | Survey Date | วันที่สำรวจราคา |  |  |  |  | ไม่มี |  |  |  |  | Ready |  |  | Yes | 2025-12-18 00:00:00 |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 16 | Reference Date for Approved Product | วันที่อนุมัติราคาสินค้าในระบบ |  |  |  |  | KPS_T_REQPROD_MD_ORG | REF_DATE | VARCHAR2 | 10 | Y | Ready |  |  | Yes | 2025-12-20 00:00:00 | กรณีมีการพิมพ์ Reference Source เองในหน้าทำงาน ขอให้ระบบจัดเก็บข้อมูลใน Reference Product หลังจาก VP อนุมัติใบงานการขออนุมัติรายการสินค้า | Confirmed |  |  |  |  |  |  |  |  |  |  |
| Source of Product - Hotel |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 16 | Product Name - TH | ชื่อสินค้าภาษาไทย |  |  |  |  | ไม่มี |  |  |  |  | Ready |  |  | No |  | ถ้ามีชื่อสินค้าภาษาไทย ไม่ต้องมีชื่อสินค้าภาษาอังกฤษก็ได้ | Confirmed |  | ขอให้สามารถกรอกได้ภายหลัง |  |  |  |  |  |  |  |  |
| 17 | Product Name - EN | ชื่อสินค้าภาษาอังกฤษ |  |  |  |  | KPS_T_REQPROD_MD_ORG | PROD_SERV_NAME | VARCHAR2 | 200 | N | Ready |  |  | No | Pad Thai Prawn | ถ้ามีชื่อสินค้าภาษาอังกฤษ ไม่ต้องมีชื่อสินค้าภาษาไทยก็ได้ | Confirmed |  | ขอให้สามารถกรอกได้ภายหลัง |  |  |  |  |  |  |  |  |
| 18 | Reference Source | ชื่อร้านค้าและโรงแรมที่ใช้อ้างอิง |  |  |  |  | KPS_T_REQPROD_MD_ORG KPS_T_REQPROD_MD_ORG   KPS_T_REQPROD_MD_ORG | CON_CODE SHOP_CODE เอา 2 ค่าบนไปหาค่า SHORT_NAME ใน KPS_R_SHOP  REF_SOURCE | CHAR VARCHAR2   VARCHAR2 | 2 20   100 | N N   Y | Ready |  |  | Yes | Lakorn European Brasserie - The Rosewood Hotel Bangkok |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 19 | Sale Price (Exclude VAT) | ราคาขายไม่รวมภาษีมูลค่าเพิ่ม |  |  |  |  | KPS_T_REQPROD_MD_ORG | REQ_PRICE_EXC_VAT | NUMBER | 16,2 | N | Ready |  |  | Yes | 550 | กรณีระบุ Sell Price (Exclude VAT) ให้ระบบคำนวณ Sell Price (Include VAT) อัตโนมัติ | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 20 | VAT |  |  |  |  |  | KPS_T_REQPROD_MD_ORG | VAT_RATE | NUMBER | 5,2 | N | Ready |  |  | No |  |  | Cancelled |  |  |  |  |  |  |  |  |  |  |
| 21 | Sale Price (Include VAT) | ราคาขายรวมภาษีมูลค่าเพิ่ม |  |  |  |  | KPS_T_REQPROD_MD_ORG | REQ_PRICE_INC_VAT | NUMBER | 16,2 | N | Ready |  |  | Yes | 588.5 | กรณีระบุ Sell Price (Include VAT) ให้ระบบคำนวณ Sell Price (Exclude VAT) อัตโนมัติ | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 22 | Survey Date | วันที่สำรวจราคา |  |  |  |  | ไม่มี |  |  |  |  | Ready |  |  | Yes | 2025-12-18 00:00:00 |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 23 | Reference Date for Approved Product | วันที่อนุมัติราคาสินค้าในระบบ |  |  |  |  | KPS_T_REQPROD_MD_ORG | REF_DATE | VARCHAR2 | 10 |  | Ready |  |  | Yes | 2025-12-20 00:00:00 | กรณีมีการพิมพ์ Reference Source เองในหน้าทำงาน ขอให้ระบบจัดเก็บข้อมูลใน Reference Product หลังจาก VP อนุมัติใบงานการขออนุมัติรายการสินค้า | Confirmed |  |  |  |  |  |  |  |  |  |  |

---

## 11_Product Category

| No. | SFDC Field Name (EN) | SFDC Field Name (TH) | Source Field API Name | Source Field Type | Source Field Length | VULLABLE (N=Required) | KP Table | KP Field Name | KP Field Type | KP Field Length | VULLABLE (N=Required).1 | Progress | Confirm | Type | Required | Sample Data | Description | Status | User/KP Feedback | Remark | Help Text | Track History | External ID | Track History.1 | Encrypted | Page Layout | Length | Source Field API Name.1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 1.0 | Product  Category  Code |  |  |  |  |  | KPS_T_REQPROD_MD | STD_CATE_CODE  Note: STD_CATE_CODE = PROD_CATE_CODE + PROD_SUBCAT1_CODE + PROD_SUBCAT2_CODE (รวม 4 ตัวอักษร) | VARCHAR2 | 4 | N | Ready |  |  |  | 5B01 |  |  |  |  |  |  |  |  |  |  |  |  |
| 2.0 | ประเภท |  |  |  |  |  | KPS_R_CATEGORY | STD_CATE_DESC | VARCHAR2 | 200 | Y | Ready |  |  |  | Food & Beverages |  |  |  |  |  |  |  |  |  |  |  |  |
| 3.0 | Product Category |  |  |  |  |  | KPS_R_PRO_SUBCATE1 KPS_R_PRO_SUBCATE1 KPS_R_PRO_SUBCATE1 | PROD_CATE_CODE  PROD_SUBCAT1_CODE PROD_SUBCAT1_DESC  Note: (Product Category Code) ตำแหน่ง 1  = PROD_CATE_CODE, ตำแหน่งที่ 2 = PROD_SUBCAT1_CODE | CHAR CHAR VARCHAR2 | 1 1 200 | N N Y | Ready |  |  |  | Italian Food |  |  |  |  |  |  |  |  |  |  |  |  |
| 4.0 | Product Category |  |  |  |  |  | KPS_R_PRO_SUBCATE2 KPS_R_PRO_SUBCATE2 KPS_R_PRO_SUBCATE2 KPS_R_PRO_SUBCATE2 | PROD_CATE_CODE  PROD_SUBCAT1_CODE PROD_SUBCAT2_CODE PROD_SUBCAT2_DESC  Note: (Product Category Code) ตำแหน่ง 1  = PROD_CATE_CODE,  ตำแหน่งที่ 2 = PROD_SUBCAT1_CODE,ตำแหน่งที่ 34 = PROD_SUBCAT2_CODE  | CHAR CHAR CHAR VARCHAR2 | 1 1 2 200 | N N N Y | Ready |  |  |  | Prepared Food |  |  |  |  |  |  |  |  |  |  |  |  |
| 5.0 | ความหมาย |  |  |  |  |  | KPS_R_PRO_SUBCATE2 | PROD_SUBCAT2_DESC_EN | VARCHAR2 | 200 | Y | Ready |  |  |  | อาหารอิตาเลี่ยนสำเร็จรูป |  |  |  |  |  |  |  |  |  |  |  |  |

---

## 12_Product & Price

| No. | SFDC Field Name (EN) | SFDC Field Name (TH) | Source Field API Name | Source Field Type | Source Field Length | VULLABLE (N=Required) | KP Table | KP Field Name | KP Field Type | KP Field Length | VULLABLE (N=Required).1 | Progress | Confirm | Type | Required | Sample Data | Source Field API Name.1 | Description | Status | User/KP Feedback | Help Text | Track History | External ID | Encrypted | Page Layout | SFDC Table | SFDC API Name | SFDC Type | Unnamed: 29 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Product & Price |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 1 | Concession | สัมปทาน | CON_CODE | CHAR | 2.0 |  | KPS_T_APPRV_M KPS_R_CONCESS | CON_CODE CON_LNAME | CHAR VARCHAR2 | 2 100 | N N | Ready | Y |  | Yes | 09 : SVB 05 : DMK (Inter) 10 : DMK (Dom) 08 : HKT |  |  | Confirmed |  |  |  |  |  |  | Product2 | TMS_Concession__c | Lookup(Concession)	 |  |
| 2 | Company Code & Company Name | รหัสบริษัท และชื่อบริษัท | SHOP_CODE | VARCHAR2 | 20.0 | N | KPS_T_APPRV_M KPS_R_SHOP | SHOP_CODE SHOP_NAME_E | VARCHAR2 VARCHAR2 | 20 200 | N Y | Ready | Y |  | Yes | 0901075 APT FOODS CO., LTD.  |  |  | Confirmed |  |  |  |  |  |  | Product2 | TMS_Company_Code__c TMS_Company_Name__c | Formula (Text) Lookup(Account) | {tb.SHOP_CODE} - {tb.SHOP_NAME_E} |
| 3 | Shop Brand Code & Shop Name | รหัสร้านค้า และชื่อร้านค้า | SHPBND_CODE | VARCHAR2 | 4.0 | Y | KPS_T_APPRV_M KPS_R_SHOP_BRAND | SHPBND_CODE SHPBND_NAME_E | VARCHAR2 VARCHAR2 | 4 60 | N N | Ready | Y |  | Yes | 0001 - Burger King |  |  | Confirmed |  |  |  |  |  |  | Product2 | TMS_Shop_Brand_Code__c TMS_Shop_Brand_Name__c | Formula (Text) Lookup(Shop Brand) |  |
| 4 | Bar Code |  | KPS_T_REQPROD_MD.BARCODE | VARCHAR2 | 30.0 | Y | KPS_T_APPRV_M KPS_T_REQPROD_MD | CON_CODE SHOP_CODE PROD_SERV_CODE BARCODE FILE_NAME | VARCHAR2 | 30 | Y | Ready | Y |  | No | 12345678 |  |  | Confirmed |  |  |  |  |  |  | Product2 | TMS_Bar_Code__c | Text(100) |  |
| 5 | Unit Code | หน่วยนับสินค้า | UNIT_CODE | VARCHAR2 | 10.0 | Y | KPS_T_APPRV_M KPS_R_UNIT | UNIT_CODE UNIT_DESC | VARCHAR2 VARCHAR2 | 10 50 | N Y | Ready | Y |  | Yes | 0012 - Each |  |  | Confirmed |  |  |  |  |  |  | Product2 | TMS_Unit__c | Picklist |  |
| 6 | Start Date | วันที่ผู้ประกอบการต้องการเริ่มจำหน่ายสินค้า | KPS_EFF_SDATE | VARCHAR2 | 19.0 | Y | KPS_T_APPRV_M | KPS_EFF_SDATE | VARCHAR2 | 19 | Y | Ready | Y |  | Yes | 09/12/2025 00:00:00 |  |  | Confirmed |  |  |  |  |  |  | Product2 | TMS_Start_Date__c | Date/Time |  |
| 7 | End Date | วันที่สิ้นสุดสัญญา | KPS_EFF_EDATE | VARCHAR2 | 19.0 | Y | KPS_T_APPRV_M | KPS_EFF_EDATE | VARCHAR2 | 19 | Y | Ready | Y |  | Yes | 31/03/2028 23:59:59 |  |  | Confirmed |  |  |  |  |  |  | Product2 | TMS_End_Date__c | Date/Time |  |
| 8 | Document No. / Ticket No. | เลขที่เอกสาร | KPS_REASON | VARCHAR2 | 200.0 | Y | KPS_T_APPRV_M | KPS_REASON | VARCHAR2 | 200 | Y | Ready | Y |  | Yes | KPS/TEN 1058/2568  |  |  | Confirmed |  |  |  |  |  |  | Product2 | TMS_Document_No_Ticket_No__c | Text(100) |  |
| 9 | Created Date | วันที่ส่งใบงานขออนุมัติราคาสินค้ามายังฝ่าย CAC | CREATEDDATE | DATE | 7.0 | Y | KPS_T_REQPROD_MD | REQUEST_DATE | CHAR | 10 | N | Ready | Y |  | Yes | 2025-12-04 00:00:00 |  |  | Confirmed |  |  |  |  |  |  | Product2 | CreatedDate | Date/Time |  |
| Tenant Product comparison (KPS_T_REQPROD_MD) |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 10 | Product Category Code | รหัสหมวดหมู่สินค้า | STD_CATE_CODE | VARCHAR2 | 4.0 | Y | KPS_T_REQPROD_MD | STD_CATE_CODE | VARCHAR2 | 4 | N | Ready | Y |  | Yes | 5NKA |  |  | Confirmed |  |  |  |  |  |  | Product2 | TMS_Product_Category_Code__c | Text(100) |  |
| 11 | Product Code | รหัสสินค้า | PROD_SERV_CODE | VARCHAR2 | 100.0 | N | KPS_T_REQPROD_MD | PROD_SERV_CODE | VARCHAR2 | 100 | N | Ready | Y |  | Yes | BK 660000227 |  |  | Confirmed |  |  |  |  |  |  | Product2 | ProductCode | Text(255) |  |
| 12 | Product Name - EN | ชื่อสินค้าภาษาอังกฤษ | PROD_SERV_NAME | VARCHAR2 | 200.0 | Y | KPS_T_REQPROD_MD | PROD_SERV_NAME | VARCHAR2 | 200 | N | Ready | Y |  | Yes | Nestle Pure Life Water (Pet) |  |  | Confirmed |  |  |  |  |  |  | Product2 | Name | Text(255) |  |
| 13 | Product Name - TH | ชื่อสินค้าภาษาไทย | <New> |  |  |  | ไม่มี | ไม่มี |  |  |  | New | Y |  | No | น้ำดื่มเนสท์เล่ เพียวไลฟ์  |  |  | Confirmed |  |  |  |  |  |  | Product2 | TMS_Product_Name_TH__c | Text(255) |  |
| 14 | Product Weight (g. / ml. / oz.) | น้ำหนัก / ปริมาตรสินค้า (กรัม / มิลลิลิตร / ออนซ์) | <New> |  |  |  | ไม่มี | ไม่มี |  |  |  | New | Y |  | No | 600 ml. |  |  |  |  |  |  |  |  |  | Product2 | TMS_Product_Weight__c | Number(16, 2) |  |
| 15 | Transaction Type | ประเภทสินค้าที่ขออนุม้ติ | TRANS_TYPE | NUMBER | 22.0 | Y | KPS_T_REQPROD_MD | TRANS_TYPE (1 = New , 2 = Update , 3 = Cancel, 4 = Promotion) | NUMBER | (1,0) | N | Ready | Y |  | Yes | New, Update, Cancel |  |  | Confirmed |  |  |  |  |  |  | Product2 | TMS_Product_Type__c | Picklist |  |
| 16 | Sale Price (Exclude VAT) | ราคาขายไม่รวมภาษีมูลค่าเพิ่ม | KPS_PRICE_EXC_VAT | NUMBER | 22.0 | Y | KPS_T_REQPROD_MD | KPS_PRICE_EXC_VAT | NUMBER | (16,2) | Y | Ready | Y |  | Yes | 9.35 |  | 1. ขอให้มีจุดทศนิยม 2 ตำแหน่ง 2. สำหรับสินค้าที่ขออนุมัติใหม่ และสินค้าที่เกิดจากการกระทำผิดข้อกำหนดด้านราคาและต้องการยกเลิก | Confirmed |  |  |  |  |  |  | Product2 | TMS_Price_EXC_VAT__c | Number(16, 2) |  |
| 17 | Sale Price (Include VAT) | ราคาขายรวมภาษีมูลค่าเพิ่ม | KPS_PRICE_INC_VAT | NUMBER | 22.0 | Y | KPS_T_REQPROD_MD | KPS_PRICE_INC_VAT | NUMBER | (16,2) | Y | Ready | Y |  | Yes | 10 |  | 1. ขอให้มีจุดทศนิยม 2 ตำแหน่ง 2. สำหรับสินค้าที่ขออนุมัติใหม่ และสินค้าที่เกิดจากการกระทำผิดข้อกำหนดด้านราคา (ขายสินค้าก่อนได้รับการอนุมัติ) และต้องการยกเลิก | Confirmed |  |  |  |  |  |  | Product2 | TMS_Price_INC_VAT__c | Number(16, 2) |  |
| 18 | Previous Sale Price (Exclude VAT) | ราคาขายเดิมไม่รวมภาษีมูลค่าเพิ่ม | <New> |  |  |  | ไม่มี | ไม่มี |  |  |  | New | Y |  | Yes | 8.411214953 |  | 1. ขอให้มีจุดทศนิยม 2 ตำแหน่ง 2. สำหรับสินค้าที่ขออนุมัติปรับราคา และสินค้าที่มีในระบบ แต่ผู้ประกอบการต้องการยกเลิกจำหน่าย | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 19 | Previous Sale Price (Include VAT) | ราคาขายเดิมรวมภาษีมูลค่าเพิ่ม | <New> |  |  |  | ไม่มี | ไม่มี |  |  |  | New | Y |  | Yes | 9 |  | 1. ขอให้มีจุดทศนิยม 2 ตำแหน่ง 2. สำหรับสินค้าที่ขออนุมัติปรับราคา และสินค้าที่มีในระบบ แต่ผู้ประกอบการต้องการยกเลิกจำหน่าย | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 20 | Reference Source | ชื่อร้านค้า - สถานที่ที่ใช้อ้างอิง | KPS_T_REQPROD_MD.REF_SOURCE | VARCHAR2 | 100.0 | Y | KPS_T_REQPROD_MD | REF_SOURCE | VARCHAR2 | 100 | Y | Ready | Y |  | Yes | Burger King - Siam Paragon  |  |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 21 | Reference Price (Exclude VAT) | ราคาอ้างอิงไม่รวมภาษีมูลค่าเพิ่ม | KPS_T_REQPROD_MD.REQ_PRICE_EXC_VAT | NUMBER | 22.0 | N | ไม่มี | ไม่มี |  |  |  | Ready | Y |  | Yes | 18.69 |  | ขอให้มีจุดทศนิยม 2 ตำแหน่ง | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 22 | Reference Price (Include VAT) | ราคาอ้างอิงรวมภาษีมูลค่าเพิ่ม | KPS_T_REQPROD_MD.REQ_PRICE_INC_VAT | NUMBER | 22.0 | N | มีแต่ไม่ชัดเจนว่าเป็น In หรือ Ex (REF_PRICE) | มีแต่ไม่ชัดเจนว่าเป็น In หรือ Ex (REF_PRICE) |  |  |  | Ready | Y |  | Yes | 19.9983 |  | ขอให้มีจุดทศนิยม 2 ตำแหน่ง | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 23 | % Different | ส่วนต่างราคาสินค้า (Sale Price (Include VAT) - Reference Price (Include VAT)) / Reference Price (Include VAT) x 100 | KPS_T_PROD_COMPARE.REF_PRICE_EXC_DIFF | NUMBER | 22.0 | Y | KPS_T_PROD_COMPARE | REF_PRICE_EXC_DIFF |  |  |  | Ready | Y |  | Yes | -49.99574964 |  | ไม่เกิน 20.00% | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 24 | Remarks | หมายเหตุ | <New> |  |  |  | ไม่มี | ไม่มี |  |  |  | New | Y |  | No | เทียบกับ Bottle of Water  |  |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 25 | Request No. | เลขที่เอกสารขออนุมัติราคาสินค้า | KPS_REASON | VARCHAR2 | 200.0 | Y | KPS_T_REQPROD_MD | KPS_REASON | VARCHAR2 | 200 | Y | Ready | Y |  | Yes | 111-2568 |  |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| Internal Product comparison (KPS_T_PROD_COMPARE) |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 26 | Product Category Code | รหัสหมวดหมู่สินค้า |  |  |  |  | KPS_T_REQPROD_MD | STD_CATE_CODE | VARCHAR2 | 4 | N | Ready | Y |  | Yes | 5NKA |  |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 27 | Product Code | รหัสสินค้า |  |  |  |  | KPS_T_PROD_COMPARE | PROD_SERV_CODE | VARCHAR2 | 100 | N | Ready | Y |  | Yes | BK 660000227 |  |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 28 | Product Name - EN | ชื่อสินค้าภาษาอังกฤษ |  |  |  |  | KPS_T_PROD_COMPARE | PROD_SERV_NAME | VARCHAR2 | 200 | Y | Ready | Y |  | Yes | Nestle Pure Life Water (Pet) |  |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 29 | Product Name - TH | ชื่อสินค้าภาษาไทย |  |  |  |  | ไม่มี | ไม่มี |  |  |  | Ready | Y |  | No | น้ำดื่มเนสท์เล่ เพียวไลฟ์ |  |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 30 | Sub Product Name - EN / TH | ชื่อสินค้าย่อยใน Combo ภาษาอังกฤษ / ภาษาไทย |  |  |  |  | ไม่มี | ไม่มี |  |  |  | Ready | Y |  | Yes |  |  |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 31 | Product Weight (g. / ml. / oz.) | น้ำหนัก / ปริมาตรสินค้า / ขนาด (กรัม / มิลลิลิตร / ออนซ์ / S, M, L, XL) |  |  |  |  | ไม่มี | ไม่มี |  |  |  | Ready | Y |  | No | 600 ml. |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 32 | Transaction Type | ประเภทสินค้า |  |  |  |  | KPS_T_PROD_COMPARE | TRANS_TYPE (1 = New , 2 = Update , 3 = Cancel, 4 = Promotion) | NUMBER | (1,0) | Y | Ready | Y |  | Yes | New, Update, Cancel |  |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 33 | Sale Price (Exclude VAT) | ราคาขายรวมภาษีมูลค่าเพิ่ม |  |  |  |  | KPS_T_PROD_COMPARE | REQ_PRICE_EXC_VAT | NUMBER | (16,2) | Y | Ready | Y |  | Yes | 9.35 |  | 1. ขอให้มีจุดทศนิยม 2 ตำแหน่ง 2. สำหรับสินค้าที่ขออนุมัติใหม่ และสินค้าที่เกิดจากการกระทำผิดข้อกำหนดด้านราคาและต้องการยกเลิก | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 34 | Sale Price (Include VAT) | ราคาขายรวมภาษีมูลค่าเพิ่ม |  |  |  |  | KPS_T_PROD_COMPARE | REQ_PRICE_INC_VAT | NUMBER | (16,2) | Y | Ready | Y |  | Yes | 10 |  | 1. ขอให้มีจุดทศนิยม 2 ตำแหน่ง 2. สำหรับสินค้าที่ขออนุมัติใหม่ และสินค้าที่เกิดจากการกระทำผิดข้อกำหนดด้านราคา (ขายสินค้าก่อนได้รับการอนุมัติ) และต้องการยกเลิก | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 35 | Previous Sale Price (Exclude VAT) | ราคาขายเดิมรวมภาษีมูลค่าเพิ่ม |  |  |  |  | KPS_T_PROD_COMPARE | OLD_PRICE_EXC_VAT | NUMBER | (16,2) | Y | Ready | Y |  | Yes | 8.411214953 |  | 1. ขอให้มีจุดทศนิยม 2 ตำแหน่ง 2. สำหรับสินค้าที่ขออนุมัติปรับราคา และสินค้าที่มีในระบบ แต่ผู้ประกอบการต้องการยกเลิกจำหน่าย | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 36 | Previous Sale Price (Include VAT) | ราคาขายเดิมรวมภาษีมูลค่าเพิ่ม |  |  |  |  | KPS_T_PROD_COMPARE | OLD_PRICE_INC_VAT | NUMBER | (16,2) | Y | Ready | Y |  | Yes | 9 |  | 1. ขอให้มีจุดทศนิยม 2 ตำแหน่ง 2. สำหรับสินค้าที่ขออนุมัติปรับราคา และสินค้าที่มีในระบบ แต่ผู้ประกอบการต้องการยกเลิกจำหน่าย | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 37 | Reference Source | ชื่อร้านค้า - สถานที่ที่ใช้อ้างอิง |  |  |  |  | KPS_T_PROD_COMPARE | REF_SHOP | VARCHAR2 | 100 | Y | Ready | Y |  | Yes | Burger King - Siam Paragon  |  |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 38 | Reference Price (Exclude VAT) | ราคาอ้างอิงรวมภาษีมูลค่าเพิ่ม |  |  |  |  | KPS_T_PROD_COMPARE | REF_PRICE_EXC_VAT | NUMBER | (16,2) | Y | Ready | Y |  | Yes | 18.69 |  | ขอให้มีจุดทศนิยม 2 ตำแหน่ง | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 39 | Reference Price (Include VAT) | ราคาอ้างอิงรวมภาษีมูลค่าเพิ่ม |  |  |  |  | KPS_T_PROD_COMPARE | REF_PRICE_INC_VAT | NUMBER | (16,2) | Y | Ready | Y |  | Yes | 19.9983 |  | ขอให้มีจุดทศนิยม 2 ตำแหน่ง | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 40 | % Different | ส่วนต่างราคาสินค้า (Sale Price (Include VAT) - Reference Price (Include VAT)) / Reference Price (Include VAT) x 100 |  |  |  |  | KPS_T_PROD_COMPARE | REF_PRICE_EXC_DIFF | NUMBER | (5,0) | Y | Ready | Y |  | Yes | 11.11111111 |  | ไม่เกิน 20.00% | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 41 | Remarks | หมายเหตุ |  |  |  |  | KPS_T_PROD_COMPARE | REMARKS | VARCHAR2 | 200 | Y | Ready | Y |  | No | เทียบกับ Bottle of Water  |  |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 42 | Approved Date | วันที่อนุมัติราคาสินค้า |  |  |  |  | KPS_T_APPRV_M | KPS_APPROVE_DATE | CHAR | 10 | Y | Ready | Y |  | Yes | 2025-12-08 00:00:00 |  |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 43 | Start Date | วันที่ผู้ประกอบการต้องการเริ่มจำหน่ายสินค้า |  |  |  |  | KPS_T_PROD_COMPARE | START_DATE | CHAR | 10 | Y | Ready | Y |  | Yes | 09/12/2025 00:00:00 |  |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 44 | End Date | วันที่สิ้นสุดสัญญา |  |  |  |  | KPS_T_APPRV_M | KPS_EFF_EDATE | VARCHAR2 | 19 | Y | Ready | Y |  | Yes | 31/03/2028 23:59:59 |  |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 45 | Document No. / Ticket No. | เลขที่เอกสาร |  |  |  |  | KPS_T_APPRV_M | KPS_REASON | VARCHAR2 | 200 | Y | Ready | Y |  | Yes | KPS/TEN 1058/2568  |  |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 46 | Owner | ผู้รับผิดชอบ |  |  |  |  | KPS_T_PROD_COMPARE | CREATEDBY | VARCHAR2 | 30 | Y | Ready | Y |  | Yes | Woranuch |  |  |  |  |  |  |  |  |  |  |  |  |  |

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
| Inspection Period |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 1 | Year | ปี | PERIOD | NUMBER | 22.0 | N | KPS_CAC_INSPECTION_DOCUMENT | INS_YEAR | CHAR | 4 | Y | Ready |  |  | Yes | 2025 |  |  | Confirmed |  |  |  |  |  |  |
| 2 | Period | เดือนที่ตรวจ | S_MONTH_CODE | CHAR | 2.0 | N | KPS_CAC_INSPECTION_DOCUMENT KPS_CAC_INSPECTION_PERIOD DB_TABLE_ATTRIBUTE | PERIOD KEY_VALUE VALUE_DATA | NUMBER VARCHAR2 NVARCHAR2 | 2,0 30 4000 | Y N Y | Ready |  |  | Yes | November - December |  |  | Confirmed |  |  |  |  |  |  |
| 3 | Ad-hoc |  |  |  |  |  | KPS_CAC_INSPECTION_DOCUMENT | PERIOD (ถ้าเป็น null เป็น yes, otherwise no) | NUMBER | 2,0 | Y | Ready |  |  | Yes | - Yes - No |  |  |  |  |  |  |  |  |  |
| Information |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 4 | Concession | สัมปทาน |  |  |  |  | KPS_CAC_INSPECTION_DOCUMENT KPS_R_CONCESS | CON_CODE CON_LNAME | CHAR VARCHAR2 | 2 100 | N Y | Ready |  |  | Yes | 09 : SVB |  |  | Confirmed |  |  |  |  |  |  |
| 5 | Company Code | รหัสบริษัท |  |  |  |  | KPS_CAC_INSPECTION_DOCUMENT | SHOP_CODE | VARCHAR2 | 20 | Y | Ready |  |  | Yes | 0901049 - After You Public Company Limited |  |  | Confirmed |  |  |  |  |  |  |
| 6 | Company Name | ชื่อบริษัท |  |  |  |  | KPS_CAC_INSPECTION_DOCUMENT KPS_R_SHOP | SHOP_CODE SHOP_NAME_E | VARCHAR2 VARCHAR2 | 20 200 | Y Y | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 7 | Shop Code | รหัสร้านค้า |  |  |  |  | KPS_CAC_INSPECTION_DOCUMENT KPS_CAC_INSPECTION_DOCUMENT KPS_R_SHOP_BRAND | CON_CODE SHOP_CODE SHPBND_CODE | CHAR VARCHAR2 VARCHAR2 | 2 20 4 | Y Y N | Ready |  |  | Yes | 0002 - After You |  |  | Confirmed |  |  |  |  |  |  |
| 8 | Shop Name | ชื่อร้านค้า |  |  |  |  | KPS_CAC_INSPECTION_DOCUMENT KPS_CAC_INSPECTION_DOCUMENT KPS_R_SHOP_BRAND KPS_R_SHOP_BRAND | CON_CODE SHOP_CODE SHPBND_CODE SHPBND_NAME_E | CHAR VARCHAR2 VARCHAR2 VARCHAR2 | 2 20 4 60 | Y Y N Y | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 9 | Branch Code | เลขสาขาของร้านค้า |  |  |  |  | KPS_CAC_INSPECTION_DOCUMENT | BRANCH_CODE | VARCHAR2 | 20 | Y | Ready |  |  | Yes | 001 - T1ME2-24 |  |  | Confirmed |  |  |  |  |  |  |
| 10 | Unit No. | เลขที่ยูนิต |  |  |  |  | KPS_CAC_INSPECTION_DOCUMENT KPS_CAC_INSPECTION_DOCUMENT | BRANCH_CODE SHOP_UNIT | VARCHAR2 VARCHAR2 | 20 15 | Y Y | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 11 | Contract No. |  |  |  |  |  | ไม่มี |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 12 | Level | ชั้น |  |  |  |  | KPS_CAC_INSPECTION_DOCUMENT KPS_CAC_INSPECTION_DOCUMENT KPS_R_SHOPUNIT KPS_R_LEVEL | CON_CODE SHOP_UNIT LEVEL_CODE LEVEL_DESC | CHAR VARCHAR2 VARCHAR2 VARCHAR2 | 2 15 3 30 | N Y Y N | Ready |  |  | Yes | 2 |  |  | Confirmed |  |  |  |  |  |  |
| 13 | Location | สถานที่ตั้งของร้าน |  |  |  |  | KPS_CAC_INSPECTION_DOCUMENT KPS_CAC_INSPECTION_DOCUMENT KPS_R_SHOPUNIT KPS_R_BUILDING  | CON_CODE SHOP_UNIT B_CODE B_DESC | CHAR VARCHAR2 VARCHAR2 VARCHAR2 | 2 15 3 30 | N Y Y Y | Ready |  |  | Yes | Terminal , Concourse A (แสดงข้อมูลตามแต่ละ Location ของร้านค้า) |  |  | Confirmed |  |  |  |  |  |  |
| 14 | Inspection Type | ประเภทการตรวจร้านค้า |  |  |  |  | ไม่มี |  |  |  |  | Ready |  |  | Yes | การตรวจเมนูหน้าร้านค้า การตรวจร้านค้าเชิงพาณิชย์ การตรวจใบอนุญาต การตรวจสุขภาพพนักงาน |  |  | Confirmed |  |  |  |  |  |  |
| 15 | Inspection Category (Master Category) | ประเภทของร้านค้า |  |  |  |  | KPS_CAC_INSPECTION_DOCUMENT KPS_CAC_FORM_CATE DB_TABLE_ATTRIBUTE | FORM_CATE_CODE KEY_VALUE VALUE_DATA | VARCHAR2 VARCHAR2 NVARCHAR2 | 10 30 4000 | Y N Y | Ready |  |  | Yes | Restaurant |  |  | Confirmed |  |  |  |  |  |  |
| 16 | Institution | ผู้แจ้งปัญหาจากการตรวจ |  |  |  |  | KPS_CAC_INSPECTION_DOCUMENT KPS_CAC_INSP_DOC_DETAIL KPS_CAC_INSTITUTION DB_TABLE_ATTRIBUTE | DOC_NO INSTI_CODE KEY_VALUE VALUE_DATA | VARCHAR2 VARCHAR2 VARCHAR2 NVARCHAR2 | 10 4 30 4000 | N Y Y Y | Ready |  |  | Yes | KPS AOT DIPQ-SVB Phuket PPHO Nong Prue SAO DIPQ-DMK Don Mueang District Office DIPQ-HKT Phuket PPHO Mai Khao SAO |  |  | Confirmed |  |  |  |  |  |  |
| 17 | Inspector | ผู้เข้าตรวจ |  |  |  |  | KPS_CAC_INSPECTION_DOCUMENT KPS_CAC_INSPECTOR DB_TABLE_ATTRIBUTE | INS_YEAR KEY_VALUE VALUE_DATA | CHAR VARCHAR2 NVARCHAR2 | 4 30 4000 | Y Y Y | Ready |  |  | Yes | Panisa |  |  | Confirmed |  |  |  |  |  |  |
| 18 | Main Topic (Group Topic) | หัวข้อหลัก | KEY_VALUE | VARCHAR2 | 30.0 | N | KPS_CAC_INSPECTION_DOCUMENT KPS_CAC_INSP_DOC_DETAIL KPS_CAC_INSPECTION_TOPIC_M DB_TABLE_ATTRIBUTE | DOC_NO TOPIC_CODE KEY_VALUE VALUE_DATA | VARCHAR2 VARCHAR2 VARCHAR2 NVARCHAR2 | 10 4 30 2000 | N N N N | Ready |  |  | Yes | สถานที่ (F&B) |  |  | Confirmed |  |  |  |  |  |  |
| 19 | Sub Topic (Master Topic) | หัวข้อ |  |  |  |  | KPS_CAC_INSPECTION_DOCUMENT KPS_CAC_INSPECTION_TOPIC_MD KPS_CAC_INSPECTION_TOPIC_MD KPS_CAC_INSPECTION_TOPIC_MD DB_TABLE_ATTRIBUTE | DOC_NO TOPIC_CODE TOPIC_DTL_CODE KEY_VALUE VALUE_DATA | VARCHAR2 VARCHAR2 NUMBER VARCHAR2 NVARCHAR2 | 10 4 9,0 30 4000 | N N N N Y | Ready |  |  | Yes | สถานที่รับประทานอาหาร : โต๊ะหรือเก้าอี้ ที่จัดไว้สำหรับบริโภคอาหาร สะอาด มีสภาพดี ไม่ชำรุด และมีการทำความสะอาดเป็นประจำ |  |  | Confirmed |  |  |  |  |  |  |
| 20 | Main Reason (Mazter Group Reason) | ปัญหาหลัก |  |  |  |  | KPS_CAC_INSPECTION_DOCUMENT KPS_CAC_INSTITUTION_PROBLEM KPS_CAC_ITEM_RETAIL DB_TABLE_ATTRIBUTE | DOC_NO ITEM_CODE KEY_VALUE VALUE_DATA | VARCHAR2 VARCHAR2 VARCHAR2 NVARCHAR2 | 10 4 30 4000 | N N N Y | Ready |  |  | Yes | ความสะอาด |  |  | Confirmed |  |  |  |  |  |  |
| 21 | Sub Reason (Master Reason) | ปัญหา |  |  |  |  | KPS_CAC_INSPECTION_DOCUMENT KPS_CAC_INSTITUTION_PROBLEM KPS_CAC_INSTITUTION_PROBLEM KPS_CAC_REASON_RETAIL DB_TABLE_ATTRIBUTE | DOC_NO ITEM_CODE REASON_CODE KEY_VALUE VALUE_DATA | VARCHAR2 VARCHAR2 NUMBER VARCHAR2 NVARCHAR2 | 10 4 9,0 30 4000 | N N N N Y | Ready |  |  | Yes | พื้นไม่สะอาด |  |  | Confirmed |  |  |  |  |  |  |
| 22 | Form Template | แบบตรวจของร้านค้า | FORM_ID | VARCHAR2 | 10.0 | N | KPS_CAC_INSPECTION_DOCUMENT | FORM_ID | VARCHAR2 | 10 | N | Ready |  |  | Yes | Form Template ตามข้อมูล Master Data |  |  | Confirmed |  |  |  |  |  |  |
| 23 | Additional Problem from Government Sectors | ปัญหาการตรวจสุขาภิบาลโดยหน่วยงานราชการ / รัฐวิสาหกิจ |  |  |  |  | KPS_CAC_INSPECTION_DOCUMENT KPS_CAC_INSTITUTION_PROBLEM KPS_CAC_INSTITUTION_PROBLEM KPS_CAC_INSTITUTION_PROBLEM | DOC_NO ITEM_CODE REASON_CODE REMARK | VARCHAR2 VARCHAR2 NUMBER VARCHAR2 | 10 4 9,0 1000 | N N N Y | Ready |  |  | Yes | พื้นไม่สะอาด |  |  | Confirmed |  |  |  |  |  |  |
| 24 | Suggestion from Government Sectors | ข้อแนะนำเพิ่มเติมจากหน่วยงานราชการ / รัฐวิสาหกิจ |  |  |  |  | KPS_CAC_INSPECTION_DOCUMENT KPS_CAC_INSTITUTION_SUGGESTION | DOC_NO REMARK | VARCHAR2 VARCHAR2 | 10 2000 | N N | Ready |  |  | Yes | ข้อเสนอแนะจากการตรวจร้านค้า |  |  | Confirmed |  |  |  |  |  |  |
| 25 | Inspection Document  | ข้อมูลรายละเอียดผลตรวจ (ขั้นตอนการบันทึกผล) |  |  |  |  | KPS_CAC_INSPECTION_DOCUMENT | DOC_BIN | BLOB | 4000 | Y | Ready |  |  | Yes | แสดงข้อมูลรายละเอียดผลตรวจร้านค้า |  |  | Confirmed |  |  |  |  |  |  |
| 26 | KPS Inspection Checklist | หัวข้อการตรวจ |  |  |  |  | KPS_CAC_INSPECTION_DOCUMENT KPS_CAC_INSPECTION_TOPIC_MD KPS_CAC_INSPECTION_TOPIC_MD KPS_CAC_INSPECTION_TOPIC_MD DB_TABLE_ATTRIBUTE | DOC_NO TOPIC_CODE TOPIC_DTL_CODE KEY_VALUE VALUE_DATA | VARCHAR2 VARCHAR2 NUMBER VARCHAR2 NVARCHAR2 | 10 4 9,0 30 4000 | N N N N Y | Ready |  |  | Yes | สถานที่รับประทานอาหาร : โต๊ะหรือเก้าอี้ ที่จัดไว้สำหรับบริโภคอาหาร สะอาด มีสภาพดี ไม่ชำรุด และมีการทำความสะอาดเป็นประจำ |  |  | Confirmed |  |  |  |  |  |  |
| 27 | Result | ผลการตรวจ |  |  |  |  | KPS_CAC_INSPECTION_DOCUMENT KPS_CAC_INSP_DOC_DETAIL KPS_CAC_INSP_DOC_DETAIL | DOC_NO WEIGHT_PASS WEIGHT_RESULT (WEIGHT_RESULT < WEIGHT_PASS: not pass WEIGHT_RESULT >= WEIGHT_PASS: pass) | VARCHAR2 NUMBER NUMBER | 10 10,2 10,2 | N Y Y | Ready |  |  | Yes | - Pass - Not Pass  |  | ผลการตรวจแต่ละหัวข้อ | Confirmed |  |  |  |  |  |  |
| 28 | Final Result | สรุปผลการตรวจ |  |  |  |  |  |  |  |  |  | Ready |  |  | Yes | Pass |  | สรุปผลกาตรวจของร้านค้า | Confirmed |  |  |  |  |  |  |
| 29 | Summary Result (%) | สรุปผลการตรวจ (%) |  |  |  |  | KPS_CAC_INSPECTION_DOCUMENT | RESULT | NUMBER | (10,2) |  | Ready |  |  | Yes | 1 |  | แสดง % ผลการตรวจร้านค้า | Confirmed |  |  |  |  |  |  |
| 30 | Problem | ปัญหา |  |  |  |  |  |  |  |  |  | Ready |  |  | No | พื้นไม่สะอาด |  | เลือกจาก Reason | Confirmed |  |  |  |  |  |  |
| 31 | Picture | ภาพปัญหา |  |  |  |  |  |  |  |  |  | Ready |  |  | No | แสดงภาพปัญหาที่พบจากการตรวจร้านค้า |  | CAC แนบภาพปัญหาที่พบจากการตรวจร้านค้า และระบบแสดงภาพ | Confirmed |  |  |  |  |  |  |
| 32 | Suggestion | ข้อเสอนแนะ |  |  |  |  | KPS_CAC_INSPECTION_DOCUMENT KPS_CAC_INSTITUTION_SUGGESTION | DOC_NO REMARK | VARCHAR2 VARCHAR2 | 10 2000 | N N | Ready |  |  | No | ข้อเสนอแนะจากการตรวจร้านค้า |  |  | Confirmed |  |  |  |  |  |  |
| 33 | Approve Inspection Results | การอนุมัติผลตรวจร้าน |  |  |  |  | KPS_CAC_INSPECTION_DOCUMENT | ISCRITICAL (Critical = 1, Not Critical = null ) | NUMBER | 1 | Y | Ready |  |  | Yes | แสดงข้อมูลสำหรับอนุมัติผลการตรวจ |  | แสดงข้อมูลรายละเอียดผลการตรวจ,ข้อมูล Score (%) ของแต่ละร้านค้า ผลการตรวจร้านค้า (Preview) และเอกสารแนบ (Preview) โดยสามารถเลือกข้อมูลจากผลการตรวจได้  - ALL - Critical - Non Critical | Confirmed |  |  |  |  |  |  |
| 34 | Inspection Approval Status | สถานะการอนุมัติ |  |  |  |  | KPS_CAC_INSPECTION_DOCUMENT | APPROVE_STATUS | NUMBER | 1 |  | Ready |  |  | Yes | Approve Rejected Pending |  | แสดงหัวข้อสำหรับการอนุมัติผลตรวจ สถานะการอนุมัติกํารตรวจร้ํานค้ํา | Confirmed |  |  |  |  |  |  |
| 35 | Inspection Result (Preview) | ผลการตรวจร้าน (Preview) |  |  |  |  | KPS_CAC_INSPECTION_DOCUMENT KPS_CAC_INSPECTION_DOCUMENT | DOC_NO FORM_ID | VARCHAR2 VARCHAR2 | 10 10 | N N | Ready |  |  | Yes | แสดงข้อมูลรายละเอียดผลตรวจร้านค้า |  |  | Confirmed |  |  |  |  |  |  |
| 36 | Attachment | เอกสารแนบ |  |  |  |  |  |  |  |  |  | Ready |  |  | No | แสดงรายละเอียดของเอกสารแนบ |  | CAC แนบเอกสารที่เกี่ยวข้องกับตรวจร้านค้า Attached, KPS Document, AOT Result และเอกสารอื่นๆ และสามารถเปิดไฟล์เพื่อดูข้อมูลได้ | Confirmed |  |  |  |  |  |  |
| 37 | Contact Person | ข้อมูลผู้ติดต่อ |  |  |  |  | KPS_CAC_INSPECTION_INFORM KPS_CAC_INSPECTION_INFORM_SEND KPS_CAC_INSPECTION_INFORM_SEND | INFORM_NO MAIL_TYPE CONT_NAME | NUMBER VARCHAR2 VARCHAR2 | 22 10 50 | N N Y | Ready |  |  | No | ภาณิศา ชิณเครือ KPS |  | ข้อมูล ชื่อ - นามสกุล และตำแหน่งของผู้ติดต่อ | Confirmed |  |  |  |  |  |  |
| Inform Tenant Status |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 38 | Recipient Email | ข้อมูล Email สำหรับจัดส่งผลการตรวจร้านค้า (TO) |  |  |  |  | KPS_CAC_INSPECTION_INFORM KPS_CAC_INSPECTION_INFORM_SEND KPS_CAC_INSPECTION_INFORM_SEND | INFORM_NO MAIL_TYPE CONT_EMAIL | NUMBER VARCHAR2 VARCHAR2 | 22 10 200 | N N Y | Ready |  |  | Yes | panisa_ch@kingpower.com |  |  | Confirmed |  |  |  |  |  |  |
| 39 | CC/BCC | ข้อมูล Email สำหรับจัดส่งผลการตรวจร้านค้า (CC/BCC) |  |  |  |  | KPS_CAC_INSPECTION_INFORM KPS_CAC_INSPECTION_INFORM_SEND KPS_CAC_INSPECTION_INFORM_SEND | INFORM_NO MAIL_TYPE CONT_EMAIL | NUMBER VARCHAR2 VARCHAR2 | 22 10 200 | N N Y | Ready |  |  | No | panisa_ch@kingpower.com |  |  | Confirmed |  |  |  |  |  |  |
| 40 | Email Result Sending Status | สถานะการส่ง Email ถึงผู้ประกอบการ |  |  |  |  | KPS_CAC_INSPECTION_DOCUMENT | STATUS_MAIL | NUMBER | 1 |  | Ready |  |  | Yes | Yes/No |  |  | Confirmed |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 41 | Problem Solving Status | สถานะการแก้ไขของผู้ประกอบการ |  |  |  |  |  |  |  |  |  | Ready |  |  | Yes | ผู้ประกอบการส่งข้อมูลการแก้ไข ในวันที่ 18/12/2025 |  |  | Confirmed |  |  |  |  |  |  |
| 42 | ปัญหํากํารตรวจสุขําภิบําลโดยหน่วยงํานรําชกําร / รัฐวิสําหกิจ |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  | หลังคําไม่สะอําด |  |  |  |  |  |  |  |  |  |
| 43 | ข้อแนะนำเพิ่มเติมจํากหน่วยงํานรําชกําร / รัฐวิสําหกิจ |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  | หลังคําไม่สะอําด |  |  |  |  |  |  |  |  |  |

---

## 14_Form Template(New)

| No. | SFDC Field Name (EN) | SFDC Field Name (TH) | Unnamed: 3 | Unnamed: 4 | Unnamed: 5 | Unnamed: 6 | KP Table | KP Field Name | KP Field Type | KP Field Length | VULLABLE (N=Required) | Progress | Confirm | Type | Required | Sample Data | Source Field API Name | Description | Status | User/KP Feedback | Help Text | Track History | External ID | Encrypted | Page Layout |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Information |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 1 | Template Code | รหัสแบบฟอร์ม |  |  |  |  | KPS_CAC_INSPECTION_TEMPLATE | TEMP_ID | VARCHAR2 | 10 | N | Ready | Y |  | Yes |  |  |  | Confirmed |  |  |  |  |  |  |
| 2 | Shop Category | ประเภทของร้านค้า |  |  |  |  | จะสามารถระบุได้หลังจากสร้าง Documents เท่านั้น |  |  |  |  | Ready | Y |  | Yes | Restaurant |  | Master Category | Confirmed |  |  |  |  |  |  |
| 3 | Main Topic | หัวข้อหลัก |  |  |  |  | KPS_CAC_INSPECTION_TEMPLATE KPS_CAC_INSPECTION_TOPIC_M DB_TABLE_ATTRIBUTE (Localized via DB_TABLE_ATTRIBUTE (TABLE_ID='00001') ใช้ Code นี้เพื่อดูว่าจะต้องดึงข้อมูลมาจาก Table ใด โดยใช้  TABLE_ID ดูจาก DB_TABLE_CONFIG  ) | TOPIC_CODE KEY_VALUE VALUE_DATA | VARCHAR2 VARCHAR2 NVARCHAR2 | 4 30 2000 | N N Y | Ready | Y |  | Yes | สถานที่ (F&B) |  | Master Group Topic | Confirmed |  |  |  |  |  |  |
| 4 | Sub Topic | หัวข้อย่อย |  |  |  |  | KPS_CAC_INSPECTION_TEMPLATE KPS_CAC_INSPECTION_TEMPLATE KPS_CAC_INSPECTION_TOPIC_MD DB_TABLE_ATTRIBUTE (Localized via DB_TABLE_ATTRIBUTE (TABLE_ID='00002') ใช้ Code นี้เพื่อดูว่าจะต้องดึงข้อมูลมาจาก Table ใด โดยใช้  TABLE_ID ดูจาก DB_TABLE_CONFIG  )  | TOPIC_CODE TOPIC_DTL_CODE KEY_VALUE VALUE_DATA  | VARCHAR2 NUMBER VARCHAR2 NVARCHAR2  | 4 9,0 30 2000 | N N N Y | Ready | Y |  | Yes | สถานที่รับประทานอาหาร : โต๊ะหรือเก้าอี้ ที่จัดไว้สำหรับบริโภคอาหาร สะอาด มีสภาพดี ไม่ชำรุด และมีการทำความสะอาดเป็นประจำ |  | Master Topic | Confirmed |  |  |  |  |  |  |
| 5 | Status | สถานะ |  |  |  |  | KPS_CAC_INSPECTION_TEMPLATE | ACTIVE_FLAG | NUMBER | 1 | Y | Ready | Y |  | Yes | - Active  - Inactive |  | สถานะของแบบตรวจ,หัวข้อการตรวจ, ปัญหา | Confirmed |  |  |  |  |  |  |

---

## 15_Location

| No. | SFDC Field Name (EN) | SFDC Field Name (TH) | Source Field API Name | Source Field Type | Source Field Length | VULLABLE (N=Required) | KP Table | KP Field Name | KP Field Type | KP Field Length | VULLABLE (N=Required).1 | Progress | Confirm | Type | Required | Sample Data | Description | Status | User/KP Feedback | Remark | Help Text | Track History | External ID | Track History.1 | Encrypted | Page Layout | Length | Source Field API Name.1 | Source Field Type.1 | Source Field Length.1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Location |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 1 | Site |  |  |  |  |  | KPS_R_CONCESS | LOCATION | VARCHAR2 | 60.0 | N | Ready |  | Text | Yes | ท่าอากาศยานสุวรรณภูมิ | สถานที่ | New |  |  |  |  |  |  |  |  |  |  |  |  |
| 2 | Level |  |  |  |  |  | KPS_R_LEVEL | LEVEL_DESC | VARCHAR2 | 30.0 | N | Ready |  | Text | Yes | Level 4 | ชั้น | New |  |  |  |  |  |  |  |  |  |  |  |  |
| 3 | Building |  |  |  |  |  | KPS_R_BUILDING | B_DESC | VARCHAR2 | 30.0 | N | Ready |  | Text | Yes | Concourse | ตึก/อาคาร | New |  |  |  |  |  |  |  |  |  |  |  |  |
| 4 | Wing |  |  |  |  |  | KPS_R_WING | W_DESC | VARCHAR2 | 30.0 | N | Ready |  | Text | Yes | DE  | ปีกอาคาร | New |  |  |  |  |  |  |  |  |  |  |  |  |
| 5 | Zone |  |  |  |  |  | KPS_R_ZONE | ZONE_DESC | VARCHAR2 | 30.0 | N | Ready |  | Text | Yes | Junction East | โซน | New |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | LOC_CODE | VARCHAR2 | 3.0 | N |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | B_CODE | VARCHAR2 | 3.0 | N |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | B_DESC | VARCHAR2 | 30.0 | N |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | ZONE_CODE | VARCHAR2 | 3.0 | N |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | ZONE_DESC | VARCHAR2 | 30.0 | N |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | W_CODE | VARCHAR2 | 3.0 | N |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | W_DESC | VARCHAR2 | 30.0 | N |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | LEVEL_CODE | VARCHAR2 | 3.0 | N |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | LEVEL_DESC | VARCHAR2 | 30.0 | N |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | AREA_CODE | VARCHAR2 | 3.0 | N |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | AREA_NAME | VARCHAR2 | 40.0 | N |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |

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

---

## 17_Units

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
| 16 | Rental Rate |  |  |  |  |  | ไม่มี TMS KPS_R_AOT_RENTAL_RATE | RNTCAT_RATE | NUMBER | (10,2) | N | Ready | Y |  |  |  | เรทค่าเช่า | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 17 | Middle Rate |  |  |  |  |  | ไม่มีใน TMS |  |  |  |  | Ready | Y |  |  |  | เรทราคากลาง | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 18 | Unit Grade |  |  |  |  |  | ไม่มีใน TMS |  |  |  |  | Ready | Y |  |  | - A - B - C - D | ระดับพื้นที่ | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 19 | Unit Status |  |  |  |  |  | KPS_R_SHOPUNIT | STATUS | NUMBER | 1 | N | Ready | Y |  |  |  | สถานะ Unit | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 20 | Last Modified - Action |  |  |  |  |  | ต้องส่งให้ทาง BU เป็นคน Cleansing | ถ้าเจอ SHOPUNIT เดียวกันบน Table นี้ |  |  |  | Ready | Y |  |  | - Merge - Split - Sway | ปรับปรุงล่าสุดด้วยวิธีการ | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 21 | Last Modified By |  |  |  |  |  | KPS_R_SHOPUNIT | UPDATEDBY | VARCHAR2 | 30 |  | Ready | Y |  |  |  | ปรับปรุงล่าสุดโดย | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 22 | การแนบไฟล์ |  | <New> |  |  |  | ไม่มีใน TMS |  |  |  |  | New | Y |  |  | เอกสารรังวัดพื้นที่จาก AOT |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| Actual Area |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 23 | Total Area |  |  |  |  |  | KPS_R_SHOPUNIT | ACT_TOT_AREA | NUMBER | (16,3) |  | Ready | Y | Number(1,3) | Yes | 5.000 |  | Confirmed |  | " |  |  |  |  |  |  |  |  |
| 24 | Commercial Area |  |  |  |  |  | KPS_R_SHOPUNIT | ACT_COMM_AREA | NUMBER | (16,3) |  | Ready | Y | Number(1,3) | Yes | 5.000 |  | Confirmed |  | " |  |  |  |  |  |  |  |  |
| 25 | M&E Area |  |  |  |  |  | KPS_R_SHOPUNIT | ACT_ME_AREA | NUMBER | (16,3) |  | Ready | Y | Number(1,3) | Yes | 0.000 |  | Confirmed |  | " |  |  |  |  |  |  |  |  |
| 26 | Store Area |  |  |  |  |  | KPS_R_SHOPUNIT | ACT_STORE_AREA | NUMBER | (16,3) |  | Ready | Y | Number(1,3) | Yes | 0.000 |  | Confirmed |  | " |  |  |  |  |  |  |  |  |
| 27 | Other Area |  |  |  |  |  | ไม่มีใน TMS |  |  |  |  | Ready | Y | Number(1,3) | Yes | 0.000 |  | Confirmed |  | " |  |  |  |  |  |  |  |  |
| Unit Location |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 28 | Location |  |  |  |  |  | KPS_R_CONCESS KPS_R_CONCESS | CON_CODE CON_LNAME | CHAR VARCHAR2 | 2 100 | N | Ready | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 29 | Site |  |  |  |  |  | KPS_R_CONCESS | LOCATION | VARCHAR2 | 60 | N | Ready | Y |  | Yes | ท่าอากาศยานสุวรรณภูมิ | สถานที่ | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 30 | Level |  | LEVEL_CODE | VARCHAR2 | 3.0 | Y | KPS_R_SHOPUNIT | LEVEL_CODE | VARCHAR2 | 3 |  | Ready | Y |  | Yes | Level 4 | ชั้น | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 31 | Building |  | B_CODE | VARCHAR2 | 3.0 | Y | KPS_R_SHOPUNIT | B_CODE | VARCHAR2 | 3 |  | Ready | Y |  | Yes |  | ตึก/อาคาร | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 32 | Wing |  | W_CODE | VARCHAR2 | 3.0 | Y | KPS_R_SHOPUNIT | W_CODE | VARCHAR2 | 3 |  | Ready | Y |  | Yes |  | ปีกอาคาร | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 33 | Zone |  | ZONE_CODE | VARCHAR2 | 3.0 | Y | KPS_R_SHOPUNIT | ZONE_CODE | VARCHAR2 | 3 |  | Ready | Y |  | Yes |  | โซน | Confirmed |  |  |  |  |  |  |  |  |  |  |
| ข้อมูลการเช่าพื้นที่ |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 34 | ลำดับ |  |  |  |  |  | ไม่มีใน TMS (Running ASC) |  |  |  |  | Ready | Y |  | No |  | เลขลำดับที่ | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 35 | Tenant |  |  |  |  |  | KPS_T_CONT_SHOP_UNIT | SHOP_CODE | VARCHAR2 | 20 | N | Ready | Y |  | No |  | รหัสผู้ประกอบการ | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 36 | Tenant Name |  |  |  |  |  | KPS_R_SHOP | REGISTERED_NAME | VARCHAR2 |  |  | Ready | Y |  | No |  | ชื่อผู้ประกอบการ | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 37 | Shop |  |  |  |  |  | KPS_T_CONT_SHOP_UNIT | BRANCH_CODE | VARCHAR2 | 20 | N | Ready | Y |  | No |  | รหัส Shop | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 38 | Shop Name |  |  |  |  |  | KPS_R_BRANCH | BRANCH_NAME_T | VARCHAR2 | 200 |  | Ready | Y |  | No |  | ชื่อ Shop | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 39 | วันที่ส่งมอบพื้นที่ |  |  |  |  |  | KPS_T_CONTRACT | CONT_DATE |  |  |  | Ready | Y |  | No | 28/09/2020 |  | Confirmed |  | รูปแบบ: DD/MM/YYYY เป็น คริสต์ศักราช |  |  |  |  |  |  |  |  |
| 40 | วันที่เปิดร้าน |  |  |  |  |  | KPS_T_CONT_SHOP_UNIT | SHOP_STR_DATE | DATE | 7 | Y | Ready | Y |  | No | 28/09/2020 |  | Confirmed |  | รูปแบบ: DD/MM/YYYY เป็น คริสต์ศักราช |  |  |  |  |  |  |  |  |
| 41 | Contract No. |  |  |  |  |  | KPS_T_CONTRACT | CONT_NO | VARCHAR2 | 30 | N | Ready | Y |  | No |  | เลขที่สัญญา | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 42 | Contract Start Date |  |  |  |  |  | KPS_T_CONTRACT | CONT_STR_DATE | DATE | 7 | N | Ready | Y |  | No |  | วันที่สัญญาเริ่มต้น | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 43 | Contract End Date |  |  |  |  |  | KPS_T_CONTRACT | CONT_END_DATE | DATE | 7 | N | Ready | Y |  | No |  | วันที่สิ้นสุดสัญญา | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 44 | Total Area |  |  |  |  |  | KPS_R_BRANCH | AREA | NUMBER | (16,3) | Y | Ready | Y | Number(1,3) | Yes | 5.000 |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 45 | Commercial Area |  |  |  |  |  | KPS_R_BRANCH | COMM_AREA | NUMBER | (16,3) | Y | Ready | Y | Number(1,3) | Yes | 5.000 |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 46 | M&E Area |  |  |  |  |  | KPS_R_BRANCH | STORE_AREA | NUMBER | (16,3) | Y | Ready | Y | Number(1,3) | Yes | 0.000 |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 47 | Store Area |  |  |  |  |  | KPS_R_BRANCH | MNE_AREA | NUMBER | (16,3) | Y | Ready | Y | 3 | Yes | 0.000 |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 48 | Other Area |  |  |  |  |  | KPS_R_BRANCH | OTH_AREA | NUMBER | (16,3) | Y | Ready | Y | Number(1,3) | Yes | 0.000 |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| การปรับปรุง Unit |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 49 | ลำดับ |  |  |  |  |  | ไม่มีใน TMS (Running ASC) |  |  |  |  | Ready | Y |  |  |  | เลขลำดับที่ | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 50 | Action |  |  |  |  |  | Hardcode "Merge" |  |  |  |  | Ready | Y |  |  | - Merge - Swap - Split - Unit No. - วันที่เริ่มต้น - etc. |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 51 | Source Value |  |  |  |  |  | KPS_T_CONTRACT | CONT_AREA | NUMBER | (16,3) | Y | Ready | Y |  |  |  | ค่า ก่อนแก้ไข | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 52 | New Value |  |  |  |  |  | KPS_T_CONTRACT_REVISE | CONT_AREA | NUMBER | (16,3) | Y | Ready | Y |  |  |  | ค่าใหม่หลังแก้ไข | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 53 | Updated Date |  |  |  |  |  | KPS_T_CONTRACT_REVISE | REVISE_DATE | DATE |  |  | Ready | Y |  |  | 28/09/2020 |  | Confirmed |  | รูปแบบ: DD/MM/YYYY เป็น คริสต์ศักราช |  |  |  |  |  |  |  |  |
| 54 | Updated By |  |  |  |  |  | KPS_T_CONTRACT_REVISE | UPDATEDBY | VARCHAR2 | 30 |  | Ready | Y |  |  |  | ชื่อผู้ใช้ที่ update ข้อมูล | Confirmed |  |  |  |  |  |  |  |  |  |  |

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
| 6 | Activity |  | Text | Yes | F&B | ประเภทพื้นที่ | New |  |  |  |  |  |  |  |  |  |  |  |  |
| 7 | Floor |  | Text | Yes | 4 | ชั้น | New |  |  |  |  |  |  |  |  |  |  |  |  |
| 8 | Building |  | Text | Yes | Concourse/Main Terminal | อาคาร | New |  |  |  |  |  |  |  |  |  |  |  |  |
| 9 | Location |  | Text | Yes | DE, Domestic | พื้นที่อาคาร | New |  |  |  |  |  |  |  |  |  |  |  |  |
| 10 | Airport |  | Text | Yes | สุวรรณภูมิ | สนามบิน | New |  |  |  |  |  |  |  |  |  |  |  |  |
| 11 | Commercial Area (m2) |  | Text | Yes |  | พื้นที่ขาย | New |  |  |  |  |  |  |  |  |  |  |  |  |
| 12 | Storage Area (m2) |  | Text | Yes |  | พื้นที่สโตร์ | New |  |  |  |  |  |  |  |  |  |  |  |  |
| 13 | M&E Area (m2) |  | Text | Yes |  | พื้นที่ห้องเครื่อง | New |  |  |  |  |  |  |  |  |  |  |  |  |
| 14 | Total Area (m2) |  | Text | Yes |  | อื่นๆ | New |  |  |  |  |  |  |  |  |  |  |  |  |
| 15 | EE-Connect by |  | Text | Yes | AOT(1:1) /KP (1:M) | การเชื่อมต่อไฟ | New |  |  |  |  |  |  |  |  |  |  |  |  |
| 16 | EE-Power(Phase)/Main Breaker(AT) |  | Text | Yes | 3P/80AT | ขนาดเบรคเกอร์ | New |  |  |  |  |  |  |  |  |  |  |  |  |
| 17 | EE-Wire & Conduit |  | Text | Yes | 4x16 / 6 G.  IEC01. in Ø 1 1/2" IMC | ขนาดสายและท่อ | New |  |  |  |  |  |  |  |  |  |  |  |  |
| 18 | EE-Power Source |  | Text | Yes | SS5-4A-2DPM-A1 (NEW) in  LWC L2-A1/A2/8 | ตู้ที่เชื่อมต่อ | New |  |  |  |  |  |  |  |  |  |  |  |  |
| 19 | AC-Brand |  | Text | Yes | TARNE | ยี่ห้อแอร์ | New |  |  |  |  |  |  |  |  |  |  |  |  |
| 20 | AC-Model |  | Text | Yes | BDHA204RA1 | รุ่นของแอร์ | New |  |  |  |  |  |  |  |  |  |  |  |  |
| 21 | AC-Air Flow Rate (CFM) |  | Text | Yes | 1600 | แรงลม | New |  |  |  |  |  |  |  |  |  |  |  |  |
| 22 | AC-Capacity (BTU) |  | Text | Yes | 54000 | ขนาด | New |  |  |  |  |  |  |  |  |  |  |  |  |
| 23 | AC-Chilled Water Supply(inch) |  | Text | Yes | 1.1/4" | ขนาดท่อน้ำเย็นเข้า | New |  |  |  |  |  |  |  |  |  |  |  |  |
| 24 | AC-Chilled Water Return(inch) |  | Text | Yes | 1.1/4" | ขนาดท่อน้ำเย็นออก | New |  |  |  |  |  |  |  |  |  |  |  |  |
| 25 | AC-Drain Pipe(inch) |  | Text | Yes | 1.1/4" | ขนาดท่อน้ำทิ้งแอร์ | New |  |  |  |  |  |  |  |  |  |  |  |  |
| 26 | AC-Radiant Floor Cooling |  | Text | Yes | No. | ท่อแอร์แบบฝังพื้น | New |  |  |  |  |  |  |  |  |  |  |  |  |
| 27 | SN-Cold Water-Connect by |  | Text | Yes | By AOT | ประเภทการเชื่อมต่อน้ำประปา | New |  |  |  |  |  |  |  |  |  |  |  |  |
| 28 | SN-Cold Water-Main Pipe (inch) |  | Text | Yes | 1" | ขนาดท่อเมนประปา | New |  |  |  |  |  |  |  |  |  |  |  |  |
| 29 | SN-Cold Water-Meter (inch) |  | Text | Yes | 1" | ขนาดมิเตอร์น้ำ | New |  |  |  |  |  |  |  |  |  |  |  |  |
| 30 | SN-Waste Water-Drain Pipe (inch) |  | Text | Yes | 3" | ขนาดท่อน้ำทิ้งภายในร้าน | New |  |  |  |  |  |  |  |  |  |  |  |  |
| 31 | SN-Waste Water-Grease Trap (Set) |  | Text | Yes | By Tenant | ถังดักไขมัน | New |  |  |  |  |  |  |  |  |  |  |  |  |
| 32 | SN-Waste Water-Gravity (Yes/No.) |  | Text | Yes | Gravity | การต่อท่อน้ำทิ้งตรง(ไม่มีปั๊มน้ำ) | New |  |  |  |  |  |  |  |  |  |  |  |  |
| 33 | SN-Waste Water-Plumbing (Set) |  | Text | Yes | - | ปั๊มน้ำ | New |  |  |  |  |  |  |  |  |  |  |  |  |
| 34 | VN-Kitchen Exhaust Air Flow Rate (CFM) |  | Text | Yes | 1300 | แรงลมสำหรับ Hood ดูดควัน | New |  |  |  |  |  |  |  |  |  |  |  |  |
| 35 | VN-Electrostatic Precipitation (EP) |  | Text | Yes | Follow Tenant design | เครื่องขจัดละอองน้ำมัน | New |  |  |  |  |  |  |  |  |  |  |  |  |
| 36 | VN-Fire Suppression |  | Text | Yes | Must by Tenant | ระบบดับเพลิงใน Hood ดูดควัน | New |  |  |  |  |  |  |  |  |  |  |  |  |
| 37 | VN-KMA Flow |  | Text | Yes | 1000 | แรงลมระบบเติมอากาศดีของ Hood ดูดควัน | New |  |  |  |  |  |  |  |  |  |  |  |  |
| 38 | VN-Fresh Air (CFM) |  | Text | Yes | 150 | ระบบเติมอากาศดี | New |  |  |  |  |  |  |  |  |  |  |  |  |
| 39 | FP-Main Wet Pipe(inch) |  | Text | Yes | 21/2" | ท่อเมนระบบดับเพลิง | New |  |  |  |  |  |  |  |  |  |  |  |  |
| 40 | FP-Sprinkler head (Set) |  | Text | Yes | By Tenant | หัวฉีดน้ำดับเพลิงอัตโนมัติ | New |  |  |  |  |  |  |  |  |  |  |  |  |
| 41 | FP-Main Dry Pipe (Inch) |  | Text | Yes |  | ระบบเมนท่อแห้งของระบบดับเพลิง | New |  |  |  |  |  |  |  |  |  |  |  |  |
| 42 | FP-Deluge Valve(Set) |  | Text | Yes |  | ระบบดับเพลิงชนิด Deluge Valve | New |  |  |  |  |  |  |  |  |  |  |  |  |
| 43 | FP-Fire Extinguisher(Set) |  | Text | Yes |  | ถังดับเพลิง | New |  |  |  |  |  |  |  |  |  |  |  |  |
| 44 | FA-Fire Alarm Terminal(FA Box) |  | Text | Yes | 1 | กล่องเชื่อมต่อระบบสัญญาณแจ้งเหตุเพลิงไหม้ | New |  |  |  |  |  |  |  |  |  |  |  |  |
| 45 | FA-Smoke Detector(Set) |  | Text | Yes | 4 | อุปกรณ์ตรวจจับควัน | New |  |  |  |  |  |  |  |  |  |  |  |  |
| 46 | FA-Heat Detector(Set) |  | Text | Yes |  | อุปกรณ์ตรวจจับความร้อน | New |  |  |  |  |  |  |  |  |  |  |  |  |
| 47 | FA-Monitor Module(Set) |  | Text | Yes |  | อุปกรณ์ส่งสัญญาณระบบแจ้งเหตุเพลิงไหม้ | New |  |  |  |  |  |  |  |  |  |  |  |  |
| 48 | FA-Control Module(Set) |  | Text | Yes |  | อุปกรณ์ควบคุมระบบแจ้งเหตุเพลิงไหม้ | New |  |  |  |  |  |  |  |  |  |  |  |  |
| 49 | ICT-POS/COM/IP Phone(Point) |  | Text | Yes | 3 | จุดเชื่อมต่อระบบ POS,คอมพิวเตอร์,โทรศัพท์ | New |  |  |  |  |  |  |  |  |  |  |  |  |
| 50 | ICT-CCTV(Point) |  | Text | Yes | 1 | จุดเชื่อมต่อระบบกล้อง CCTV | New |  |  |  |  |  |  |  |  |  |  |  |  |
| 51 | ICT-CCTV(IP.Address) |  | Text | Yes | 176.12.2.123 | หมายเลข Address ของกล้อง | New |  |  |  |  |  |  |  |  |  |  |  |  |
| 52 | ICT-Access Point(Point) |  | Text | Yes |  | จุดเชื่อมต่อระบบ Access | New |  |  |  |  |  |  |  |  |  |  |  |  |
| 53 | ICT-Digital Signage(Point) |  | Text | Yes | 1 | จุดเชื่อมต่อป้าย | New |  |  |  |  |  |  |  |  |  |  |  |  |
| 54 | ST&AR-Shell&Core |  | Text | Yes | YES | โครงหน้าร้าน | New |  |  |  |  |  |  |  |  |  |  |  |  |
| 55 | ST&AR-Floor |  | Text | Yes | Terrazzo | พื้น | New |  |  |  |  |  |  |  |  |  |  |  |  |
| 56 | ST&AR-Wall |  | Text | Yes | Sandwich Panel | ผนัง | New |  |  |  |  |  |  |  |  |  |  |  |  |
| 57 | ST&AR-Ceiling |  | Text | Yes | Exposed | ฝ้า | New |  |  |  |  |  |  |  |  |  |  |  |  |
| 58 | EE Suggestion |  | Text | Yes |  |  | New |  |  |  |  |  |  |  |  |  |  |  |  |
| 59 | AC Suggestion |  | Text | Yes |  |  | New |  |  |  |  |  |  |  |  |  |  |  |  |
| 60 | SN Suggestion |  | Text | Yes |  |  | New |  |  |  |  |  |  |  |  |  |  |  |  |
| 61 | VN Suggestion |  | Text | Yes |  |  | New |  |  |  |  |  |  |  |  |  |  |  |  |
| 62 | FP Suggestion |  | Text | Yes |  |  | New |  |  |  |  |  |  |  |  |  |  |  |  |
| 63 | FA Suggestion |  | Text | Yes | กรณีที่มีการกั้นแบ่งพื้นที่ ต้องทำการติดตั้ง Smoke/Heat Detector |  | New |  |  |  |  |  |  |  |  |  |  |  |  |
| 64 | ICT Suggestion |  | Text | Yes |  |  | New |  |  |  |  |  |  |  |  |  |  |  |  |
| 65 | Shell&Core Suggestion |  | Text | Yes |  |  | New |  |  |  |  |  |  |  |  |  |  |  |  |
| 66 | Floor Suggestion |  | Text | Yes | Ritta รื้อพื้นเดิมออกส่งมอบให้ ID |  | New |  |  |  |  |  |  |  |  |  |  |  |  |
| 67 | Wall Suggestion |  | Text | Yes | Ritta กั้นผนังระหว่างร้าน |  | New |  |  |  |  |  |  |  |  |  |  |  |  |
| 68 | Ceiling Suggestion |  | Text | Yes | ออกแบบฝ้าเป็นลักษณะปิดทึบ ใช้วัสดุไม่ติดลามไฟ |  | New |  |  |  |  |  |  |  |  |  |  |  |  |
| 69 | Safety Suggestion |  | Text | Yes |  |  | New |  |  |  |  |  |  |  |  |  |  |  |  |
| 70 | Other Suggestion |  | Text | Yes |  |  | New |  |  |  |  |  |  |  |  |  |  |  |  |

---

## 18_Meter Master

| No. | SFDC Field Name (EN) | SFDC Field Name (TH) | Type | Required | Sample Data | Description | Status | User/KP Feedback | Remark | Help Text | Track History | External ID | Track History.1 | Encrypted | Page Layout | Length | Source Field API Name | Source Field Type | Source Field Length |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 1 | Conession |  |  | Yes | 09– SVB Terminal 1 | เลขที่รหัสสัมปทําน เ |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 2 | Unit No.KPS Unit No. |  |  | Yes | T1AE4-02 | เลขที่ Unit โดย KPS |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 3 | Source Unit No. |  |  |  | T1AE4-02 | เลขที่ Unit โดย AOT |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 4 | Tenant Code |  |  | Yes | 09001010 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 5 | Tenant Name |  |  | Yes |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 6 | Shop Code |  |  | Yes | 003 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 7 | Shop Name |  |  | Yes |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 8 | วันที่เปิดร้าน |  |  | Yes | 28/09/2020 |  |  |  | รูปแบบ: DD/MM/YYYY เป็นคริสต์ศักรําช |  |  |  |  |  |  |  |  |  |  |
| 9 | สถานะ |  |  | Yes | - ใช้งําน - ไม่ใช้งําน |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Electrical |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 10 | Meter No. |  |  | Yes |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 11 | Source Meter No. |  |  | Yes |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 12 | Owner |  |  | Yes | - KPC - KPD - KPDC - KPI.Ads - KPS - KPT |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 13 | Type of Power Energize |  |  | Yes | -1-M - AOT 1-1 - Flat Rate - พ่วง KBANK - พ่วง LWC - เหมําจ่ําย |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 14 | Source EE Room |  |  | Yes | A1-006 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 15 | Panel |  |  | Yes | SS5-4A-2DPM-A |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 16 | Feed No. |  |  | Yes | 19 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 17 | Phase |  |  | Yes | 3 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 18 | Handle by |  |  | Yes | - SMEE - Source System - Manual - Flat Rate |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 19 | ลำดับชั้น |  |  | Yes | - 2 - 3 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 20 | พ่วงจาก |  |  |  | กรณีลำดับชั้น 3 ระบุตัวพ่วงต้นทําง ที่ เกี่ยวข้อง เช่น 21134810682 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Water |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 21 | Meter No. |  |  | Yes |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 22 | Source Meter No. |  |  | Yes |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 23 | Type |  |  | Yes | - Main - Shop - Filter - เครื่องกรองน ้ํา - ห้องน ้ํา Office - ห้องน ้ํา Shop |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 24 | Source Unit No. |  |  | Yes | - A1-003 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 25 | Name |  |  | Yes | - MAIN_เสําL28 (Sorting ตะวันออก) |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 26 | ขนาดนิ้ว |  |  | Yes | -2 1/2 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |

---

## 18_Meter Usage

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
| 1 | Concession No. |  | CON_CODE | CHAR | 2.0 | N | KPS_R_POS KPS_R_CONCESS | CON_CODE CON_LNAME | CHAR VARCHAR2 | 2 100 | N N | Ready | Y | Text | Yes | 09 - SVB - Terminal 1 | เลขที่รหัสสัมปทาน | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 2 | Tenant |  |  |  |  |  | KPS_R_POS | SHOP_CODE | VARCHAR2 | 20 | N | Ready | Y |  | Yes | 0902101 | รหัสผู้ประกอบการ | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 3 | Tenant Name |  |  |  |  |  | KPS_R_POS KPS_R_SHOP | SHOP_CODE SHOP_NAME_E | VARCHAR2 VARCHAR2 | 20 200 | N N | Ready | Y |  | Yes |  | ชื่อผู้ประกอบการ | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 4 | Shop |  | SHOP_CODE | VARCHAR2 | 20.0 | N | KPS_R_POS | BRANCH_CODE | VARCHAR2 | 20 | N | Ready | Y |  | Yes |  | รหัสร้านค้าผู้ประกอบการ | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 5 | Shop Name |  |  |  |  |  | KPS_R_SHOP | SHORT_NAME | VARCHAR2 | 50 |  | Ready | Y |  | Yes |  | ชื่อร้านค้าผู้ประกอบการ | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 6 | Unit No. |  |  |  |  |  | KPS_R_POS KPS_R_BRANCH | BRANCH_CODE SHOP_UNIT | VARCHAR2 VARCHAR2 | 20 15 | N | Ready | Y |  | Yes |  | เลข unit ที่ตั้ง ของร้านค้า | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 7 | Unit Shop Description |  |  |  |  |  | KPS_R_SHOPUNIT | SHOP_UNIT_NAME | VARCHAR2 | 400 | Y | Ready | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 8 | Contact First Name and Last Name | ชื่อ นามสกุล ผู้ติดต่อ |  |  |  |  | ไม่มี |  |  |  |  | Ready | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| POS Registration |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 9 | POS Registration No. |  | POS_NO | VARCHAR2 | 50.0 | N | KPS_R_POS | POS_NO | VARCHAR2 | 50 | N | Ready | Y |  | No | E051120002A9144 | เลขที่จดทะเบียนเครื่อง POS เช่น  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 10 | Revenue ID |  |  |  |  |  | KPS_T_POS_REGISTER_HISTORY  | REVENUE_ID | VARCHAR2 | 20 |  | Ready | Y |  | No | E051120002A9144 | เลข Revenue ID เช่น  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 11 | CPU Serial No. (Temporary) |  |  |  |  |  | KPS_T_POS_REGISTER_HISTORY | CPU_SERIAL_NO | VARCHAR2 | 20 |  | Ready | Y |  | No | 4CE406B317 | เลขที่ CPU serial no. เช่น  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 12 | Start Date |  | SDATE | DATE | 7.0 | Y | KPS_R_POS | SDATE | DATE | 7 |  | Ready | Y |  | No | 28/09/2020 |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 13 | End Date |  | EDATE | DATE | 7.0 | Y | KPS_R_POS | EDATE | DATE | 7 |  | Ready | Y |  | No | 28/09/2020 |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 14 | Status |  | STATUS | NUMBER | 22.0 | Y | KPS_R_POS (1 : Use,2 : Cancel) | STATUS | NUMBER | 1 |  | Ready | Y |  | No | - Active - Inactive | สถานะการใช้งาน เครื่อง POS | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 15 | IP Address |  |  |  |  |  | ไม่มี |  |  |  |  | Ready | Y |  | No | 172.21.13.999 | เลข IP address ของเครื่อง POS | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 16 | Mac Address |  |  |  |  |  | ไม่มี |  |  |  |  | Ready | Y |  | No | 2C-58-B9-0F-1C-03 | เลข MAC address ของเครื่อง POS | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 17 | Supplier Code |  | POS_SUPPLIER_CODE | VARCHAR2 | 3.0 | Y | KPS_R_POS | POS_SUPPLIER_CODE | VARCHAR2 | 3 | Y | Ready | Y |  | No | 075 |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 18 | Supplier Name |  |  |  |  |  | KPS_R_POS KPS_R_POS_SUPPLIER | KPS_R_POS NAME_E | VARCHAR2 VARCHAR2 | 3 |  | Ready | Y |  | No | akksofttech |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 19 | Remark |  |  |  |  |  | KPS_T_POS_REGISTER_HISTORY | REMARK | VARCHAR2 | 50 |  | Ready | Y |  | No | ยกเลิก ตั้งแต่เวลา 23.30 น. |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 20 | Action |  |  |  |  |  | KPS_R_POS KPS_T_POS_REGISTER_HISTORY | STATUS (1 = Used, 2 = Cancel) SEQ_NO (Last Running number > 1 =  Update) | NUMBER | 22 | Y | Ready | Y |  | No | - Add - Update - Delete | การจัดการข้อมูลล่าสุด | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 21 | Attachment - ภพ.06 |  | FILE_NAME | VARCHAR2 | 60.0 | Y | ไม่มี |  |  |  |  | Ready | Y |  | No |  | เอกสาร ภพ.06 ที่แนบมา | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 22 | Attachment - คก.2 |  |  |  |  |  | ไม่มี |  |  |  |  | Ready | Y |  | No |  | เอกสาร คก.2 ที่แนบมา | Confirmed |  |  |  |  |  |  |  |  |  |  |

---

## 20_Sales Transaction (Report)

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

## 20_Sales Transaction (Summary)

| No. | SFDC Field Name (EN) | SFDC Field Name (TH) | Source Field API Name | Source Field Type | Source Field Length | VULLABLE (N=Required) | KP Table | KP Field Name | KP Field Type | KP Field Length | VULLABLE (N=Required).1 | Progress | Confirm | Type | Required | Sample Data | Description | Status | User/KP Feedback | Remark | Help Text | Track History | External ID | Track History.1 | Encrypted | Page Layout | Length | Source Field API Name.1 | Unnamed: 29 | Unnamed: 30 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | Company_Summary_Sales_Transaction__c Record Type: Concession |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Report รายรับเบื้องต้น |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 1.0 | Sales Date | รายวัน |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 2.0 | Sales and Service Amt | ยอดจำหน่ายสินค้าและบริการ |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 3.0 | Volume of Foreign Exchange Trading | ปริมาณการแลกเปลี่ยนตราสารและเงินตราต่างประเทศ = (SUM BROUGHT + SUM SOLD) |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 4.0 | Total Preliminary Income | รวม |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | รายงานสรุปปริมาณการแลกเปลี่ยนตราสารและเงินตราต่างประเทศ | Tenant_Summary_Sales_Transaction__c Record Type: Tenant |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 5.0 | Monthly Sales Date | 01/01/2024 - 31/01/2024  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 6.0 | Volumn Notes Bought |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 7.0 | Volumn Notes Sold |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 8.0 | Total Volumn | formula = Volumn Notes Bought + Volumn Notes Sold |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | รายงานสรุปยอดขาย (รวมทั้ง ปริมาณการแลกเปลี่ยนตราสารและเงินตราต่างประเทศ) เพื่อเป็นเอกสารประกอบการส่งหนังสือรายงานยอดขายประจำเดือนส่งให้แก่ ทอท. |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Source : คพส.06654-2568 รายงานยอดรายรับเบื้องต้นของผู้ประกอบการในบริเวณอาคารผู้โดยสารระหว่างประเทศ อาคาร 1 ท่าอากาศยานดอนเมือง พ.ย.68 - รายรับเบื้องต้น - รายละเอียดยอดจำหน่ายสินค้าและบริการและกำไรขั้นต้นจากการแลกเปลี่ยนตราสารและเงินตราค่างประเทศของผู้ประกอบการแต่ละรายเดือนพฤศจิกายน2568 |  |  |  |  |  |  |  |  |  |  |
|  | รายรับเบื้องต้น |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 9.0 | Sales Date | รายวัน |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 10.0 | Sales and Service Amt | ยอดจำหน่ายสินค้าและบริการ |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 11.0 | Volume of Foreign Exchange Trading | ปริมาณการแลกเปลี่ยนตราสารและเงินตราต่างประเทศ = (SUM BROUGHT + SUM SOLD) |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 12.0 | Total Preliminary Income | รวม |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | รายละเอียดยอดจำหน่ายสินค้าและบริการและกำไรขั้นต้นจากการแลกเปลี่ยนตราสารและเงินตราค่างประเทศของผู้ประกอบการ |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 13.0 | No |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 14.0 | Company Code |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 15.0 | Company Name |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 16.0 | Shop Brand |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 17.0 | Sales Amt (excl. VAT) |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 18.0 | Remark |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Company_Summary_Sales_Transaction__c Record Type: Concession |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 19.0 | Company Summary Sales Transaction Name |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Name |
| 20.0 | Sales Date |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Sales_Date__c |
| 21.0 | Concession |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Concession__c |
| 22.0 | Status |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Status__c |
| 23.0 | REV DM Confirmed Date/Time |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | TMS_REV_DM_Confirmed_Date_Time__c |
| 24.0 | REV DM Confirmed By |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | TMS_REV_DM_Confirmed_By__c |
| 25.0 | RecordTypeDevName |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | TMS_RecordTypeDevName__c |
|  | Sales Transaction Summary - Company_Summary_Sales_Transaction__c - Record Type: Company |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 26.0 | Company Code |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Company_Code__c |
| 27.0 | Company Name |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Company_Name__c |
| 28.0 | Require Sales Confirmation |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Require_Sales_Confirmation__c |
| 29.0 | KPT? |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | TMS_KPT__c |
| 30.0 | Branch Code |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Branch_Code__c |
| 31.0 | Shop Branch |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Shop_Branch__c |
| 32.0 | Shop Brand |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Shop_Brand__c |
| 33.0 | Sales Transaction Status |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Sales_Transaction_Status__c |
| 34.0 | Sales Amt (VAT) |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Sales_Amt_VAT__c |
| 35.0 | VAT |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | VAT__c |
| 36.0 | Sales Amt (excl. VAT) |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Sales_Amt_excl_VAT__c |
| 37.0 | Error Log |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Error_Log__c |
| 38.0 | Tenant Confirmed Date/Time |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Tenant_Confirmed_Date_Time__c |
| 39.0 | REV Admin/ KPT ACC Confirmed Date/Time |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | TMS_REV_Admin_Confirmed_Date_Time__c |
| 40.0 | REV Admin/ KPT ACC Confirmed By |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | TMS_REV_Admin_Confirmed_By__c |
| 41.0 | Confirm Billing |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Confirm_Billing__c |
| 42.0 | Confirm AOT |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Confirm_AOT__c |
| 43.0 | %AOT Revenue Share |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 44.0 | Revenue Share |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 45.0 | Remark |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Remark__c |
| 46.0 | Concession Sales Date | อ้างอิงถึง Concession และ Sales Date ของรายได้นี้ |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Concession_Sales_Date__c |
|  | Sales by Tenant Report สำหรับให้ DM REV Confirm จุดประสงค์เพื่อยืนยันกับ Audit  (As-is: AOT Approve Sales Report By Tenant) |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 47.0 | Company Code |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 48.0 | Company Name |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 49.0 | Sales Date |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 50.0 | Sales Amt (excl. VAT) |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 51.0 | Confirm AOT |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | ตรวจใบเสร็จรับเงิน Sales_Transaction + Sales_Transaction_Item |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Sales_Transaction |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 52.0 | Sales No. |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Sales_No__c |
| 53.0 | Sales Date |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Sales_Date__c |
| 54.0 | POS No |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | TMS_POS_No__c |
| 55.0 | RC Code |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 56.0 | Sales Time |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Sales_Time__c |
| 57.0 | Void Status |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Void_Status__c |
| 58.0 | Promotion Code |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Promotion_Code__c |
| 59.0 | Sales Amt (excl. VAT) |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Sales_Amt_excl_VAT__c |
| 60.0 | Service Amt (excl. VAT) |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Service_Amt_excl_VAT__c |
| 61.0 | Discount Amt (excl. VAT) |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Discount_Amt_excl_VAT__c |
| 62.0 | Total (excl. VAT) |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Total_excl_VAT__c |
| 63.0 | Total (incl. VAT) |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Total_VAT__c |
| 64.0 | Document Link |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 65.0 | Remark |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Sales_Transaction_Item |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 66.0 | Seq |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 67.0 | Product |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 68.0 | Product Name |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 69.0 | Promotion |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 70.0 | QTY. |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 71.0 | Unit |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 72.0 | Price (excl. VAT) |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 73.0 | Pricel (incl. VAT) |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 74.0 | Exc. VAT Amt |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 75.0 | Inc. VAT Amt |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 76.0 | Disc Exc. VAT Amt |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 77.0 | Disc Inc. VAT Amt |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 78.0 | Service Charge Exc. VAT |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 79.0 | Service Charge Inc. VAT |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 80.0 | Total Net Exc. VAT |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 81.0 | Total Net Inc. VAT |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |

---

## 20_Sales Transaction (Daily Sal

| No. | SFDC Field Name (EN) | SFDC Field Name (TH) | Source Field API Name | Source Field Type | Source Field Length | VULLABLE (N=Required) | KP Table | KP Field Name | KP Field Type | KP Field Length | VULLABLE (N=Required).1 | Progress | Confirm | Type | Required | Sample Data | Description | Status | User/KP Feedback | Remark | Help Text | Track History | External ID | Track History.1 | Encrypted | Page Layout | Length | Source Field API Name.1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 1.0 | File Name |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | TMS_File_Name__c |
| 2.0 | Business Type |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  | bank, bu, local_product |  |  |  |  |  |  |  |  |  |  |  | TMS_Business_Type__c |
| 3.0 | Shop Code |  | KPS_R_SHOP | SHOP_CODE |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Shop_Code__c |
| 4.0 | Branch Code |  | KPS_R_SHOP | BRANCH_CODE |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Branch_Code__c |
| 5.0 | Sales Date |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Sales_Date__c |
| 6.0 | Status |  | KPS_R_SHOP | STATUS |  |  |  |  |  |  |  | Ready |  |  |  | Uploading, Uploaded, Validation, Completed, Failed, Reset |  |  |  |  |  |  |  |  |  |  |  | TMS_Status__c |
| 7.0 | AOT Status |  | KPS_R_SHOP | SEND_SALES_TEXT_TYPE |  |  |  |  |  |  |  | Ready |  |  |  | Confirm, Unconfirm |  |  |  |  |  |  |  |  |  |  |  | TMS_AOT_Status__c |

---

## 20_Sales Transaction (Details)_

| No. | SFDC Field Name (EN) | SFDC Field Name (TH) | Source Field API Name | Source Field Type | Source Field Length | VULLABLE (N=Required) | KP Table | KP Field Name | KP Field Type | KP Field Length | VULLABLE (N=Required).1 | Progress | Confirm | Type | Required | Sample Data | Description | Status | User/KP Feedback | Remark | Help Text | Track History | External ID | Track History.1 | Encrypted | Page Layout | Length | Source Field API Name.1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Commercial |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 1 | BRANCH_CODE |  |  |  |  |  | KPS_T_SALES_M | BRANCH_CODE | VARCHAR2 | 20.0 | N | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 2 | SALE_NO |  |  |  |  |  | KPS_T_SALES_M | SALE_NO | VARCHAR2 | 50.0 | N | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 3 | POS_NO |  |  |  |  |  | KPS_T_SALES_M | POS_NO | VARCHAR2 | 50.0 | N | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 4 | SALE_TYPE |  |  |  |  |  | KPS_T_SALES_M (1: Sales    2: Return) | SALE_TYPE | NUMBER | 22.0 | N | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 5 | SALE_DATE |  |  |  |  |  | KPS_T_SALES_M | SALE_DATE | CHAR | 10.0 | N | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 6 | SHIFT_NO |  |  |  |  |  | KPS_T_SALES_M | SHIFT_NO | NUMBER | 22.0 | N | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 7 | CREATE_DATE |  |  |  |  |  | KPS_T_SALES_M | CREATE_DATE | CHAR | 19.0 | N | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 8 | TRANS_DATE |  |  |  |  |  | KPS_T_SALES_M | TRANS_DATE | CHAR | 19.0 | N | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 9 | MEMBER_ID |  |  |  |  |  | KPS_T_SALES_M | MEMBER_ID | VARCHAR2 | 20.0 | Y | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 10 | SVC_ID |  |  |  |  |  | KPS_T_SALES_M | SVC_ID | VARCHAR2 | 20.0 | Y | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 11 | NAME |  |  |  |  |  | KPS_T_SALES_M | NAME | VARCHAR2 | 200.0 | Y | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 12 | FLIGHT_NO |  |  |  |  |  | KPS_T_SALES_M | FLIGHT_NO | VARCHAR2 | 10.0 | Y | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 13 | FLIGHT_DATE |  |  |  |  |  | KPS_T_SALES_M | FLIGHT_DATE | VARCHAR2 | 19.0 | Y | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 14 | NATION_CODE |  |  |  |  |  | KPS_T_SALES_M | NATION_CODE | VARCHAR2 | 10.0 | Y | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 15 | PASSPORT_NO |  |  |  |  |  | KPS_T_SALES_M | PASSPORT_NO | VARCHAR2 | 50.0 | Y | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 16 | BIRTH_DATE |  |  |  |  |  | KPS_T_SALES_M | BIRTH_DATE | VARCHAR2 | 10.0 | Y | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 17 | SEX |  |  |  |  |  | KPS_T_SALES_M (M : Male F :  Female) | SEX | VARCHAR2 | 1.0 | Y | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 18 | VAT_TYPE |  |  |  |  |  | KPS_T_SALES_M (1: Include VAT 2: Exclude VAT) | VAT_TYPE | NUMBER | 22.0 | N | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 19 | VAT_RATE |  |  |  |  |  | KPS_T_SALES_M F_GetVatRate() | VAT_RATE | NUMBER | 22.0 | Y | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 20 | AMT_EXC_VAT |  |  |  |  |  | KPS_T_SALES_M | AMT_EXC_VAT | NUMBER | 22.0 | N | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 21 | VAT_AMT |  |  |  |  |  | KPS_T_SALES_M | VAT_AMT | NUMBER | 22.0 | N | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 22 | AMT_INC_VAT |  |  |  |  |  | KPS_T_SALES_M | AMT_EXC_VAT | NUMBER | 22.0 | N | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 23 | PRO_CODE |  |  |  |  |  | KPS_T_SALES_M | PRO_CODE | VARCHAR2 | 10.0 | Y | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 24 | EXTRA_DISC_VAT_AMT |  |  |  |  |  | KPS_T_SALES_M | EXTRA_DISC_VAT_AMT | NUMBER | 22.0 | N | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 25 | EXTRA_DISC_AMT_EXC_VAT |  |  |  |  |  | KPS_T_SALES_M | EXTRA_DISC_AMT_EXC_VAT | NUMBER | 22.0 | N | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 26 | EXTRA_DISC_AMT_INC_VAT |  |  |  |  |  | KPS_T_SALES_M | EXTRA_DISC_AMT_INC_VAT | NUMBER | 22.0 | N | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 27 | DISC_VAT_AMT |  |  |  |  |  | KPS_T_SALES_M | DISC_VAT_AMT | NUMBER | 22.0 | Y | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 28 | DISC_AMT_EXC_VAT |  |  |  |  |  | KPS_T_SALES_M | DISC_AMT_EXC_VAT | NUMBER | 22.0 | Y | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 29 | DISC_AMT_INC_VAT |  |  |  |  |  | KPS_T_SALES_M | DISC_AMT_INC_VAT | NUMBER | 22.0 | Y | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 30 | DISC_AVG_PERCENTAGE |  |  |  |  |  | KPS_T_SALES_M | DISC_AVG_PERCENTAGE | NUMBER | 22.0 | N | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 31 | SERVICE_CHARGE_TYPE |  |  |  |  |  | KPS_T_SALES_M | SERVICE_CHARGE_TYPE | NUMBER | 22.0 | N | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 32 | SERVICE_CHARGE_EXC_VAT |  |  |  |  |  | KPS_T_SALES_M | SERVICE_CHARGE_EXC_VAT | NUMBER | 22.0 | N | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 33 | SERVICE_CHARGE_VAT |  |  |  |  |  | KPS_T_SALES_M | SERVICE_CHARGE_VAT | NUMBER | 22.0 | N | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 34 | SERVICE_CHARGE_INC_VAT |  |  |  |  |  | KPS_T_SALES_M | SERVICE_CHARGE_INC_VAT | NUMBER | 22.0 | N | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 35 | NET_EXC_VAT |  |  |  |  |  | KPS_T_SALES_M | NET_EXC_VAT | NUMBER | 22.0 | N | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 36 | NET_VAT |  |  |  |  |  | KPS_T_SALES_M | NET_VAT | NUMBER | 22.0 | N | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 37 | NET_INC_VAT |  |  |  |  |  | KPS_T_SALES_M | NET_INC_VAT | NUMBER | 22.0 | N | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 38 | CANCEL_TAX_INVOICE_DATE |  |  |  |  |  | KPS_T_SALES_M | VOID_DATE | VARCHAR2 | 19.0 | Y | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 39 | CANCEL_TAX_INVOICE |  |  |  |  |  | KPS_T_SALES_M | CANCEL_TAX_INVOICE | VARCHAR2 | 50.0 | Y | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 40 | CANCEL_TAX_INVOICE_POS_NAME |  |  |  |  |  | KPS_T_SALES_M | CANCEL_TAX_INVOICE_POS_NAME | VARCHAR2 | 50.0 | Y | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 41 | VOID_REASON |  |  |  |  |  | KPS_T_SALES_M | VOID_REASON | VARCHAR2 | 200.0 | Y | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 42 | RC_CODE |  |  |  |  |  | KPS_T_SALES_M | RC_CODE | VARCHAR2 | 60.0 | Y | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |

---

## Sheet10

| No. | SFDC Field Name (EN) | SFDC Field Name (TH) | Source Field API Name | Source Field Type | Source Field Length | VULLABLE (N=Required) | KP Table | KP Field Name | KP Field Type | KP Field Length | VULLABLE (N=Required).1 | Progress | Confirm | Type | Required | Sample Data | Description | Status | User/KP Feedback | Remark | Help Text | Track History | External ID | Track History.1 | Encrypted | Page Layout | Length | Source Field API Name.1 | Unnamed: 29 | Unnamed: 30 | Unnamed: 31 | Unnamed: 32 | Unnamed: 33 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | File_Name |  |  |  |  |  |  |  |  |  |  | Ready |  | Text(255) | Y | 0904002_bank_20251127001001.txt | Daily Sales File Id + Sales No |  |  |  |  |  |  |  |  |  |  |  | TMS_File_Name__c | Text(255) | Y | 0904002_bank_20251127001001.txt | Daily Sales File Id + Sales No |
| 2 | External_File_Ref |  |  |  |  |  |  |  |  |  |  | Ready |  | Text(255) | Y | 0904002_bank_20251127001001.txt_20251127070000 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_External_File_Ref__c | Text(255) | Y | 0904002_bank_20251127001001.txt_20251127070000 |  |
| 3 | Daily_Sales_File |  |  |  |  |  |  |  |  |  |  | Ready |  | Lookup(TMS_Daily_Sales_File__c) | Y | a1kfc000002wq6jAAA |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Daily_Sales_File__c | Lookup(TMS_Daily_Sales_File__c) | Y | a1kfc000002wq6jAAA |  |
| 4 | Header_Business_Type |  |  |  |  |  | ไม่มี |  |  |  |  | Ready |  | picklist | N | bank, bu |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Header_Business_Type__c | picklist | N | 904002_1_E051120002B0239_2025112701_2025-11-27 | Shop Code + Branch Code + POS No + Sales No + Sales Date |
| 5 | Header_Shop_Code |  |  |  |  |  | KPS_T_SALES_M | SHOP_CODE | VARCHAR2 | 20 |  | Ready |  | Text(255) | N | 904002 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Header_Shop_Code__c | Text(255) | N |  |  |
| 6 | Header_Branch_Code |  |  |  |  |  | KPS_T_SALES_M | BRANCH_CODE | VARCHAR2 | 20 |  | Ready |  | Text(255) | N | 1 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Header_Branch_Code__c | Text(255) | N |  |  |
| 7 | Header_Sales_No |  |  |  |  |  | KPS_T_SALES_M | SALE_NO | CHAR | 50 |  | Ready |  | Text(255) | N | 2025112701 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Header_Sales_No__c | Text(255) | N |  |  |
| 8 | Header_Pos_No |  |  |  |  |  | KPS_T_SALES_M | POS_NO | VARCHAR2 | 50 |  | Ready |  | Text(255) | N | E051120002B0239 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Header_Pos_No__c | Text(255) | N |  |  |
| 9 | Header_Sales_Type |  |  |  |  |  | KPS_T_SALES_M | SALE_TYPE | NUMBER | 1,0 |  | Ready |  | Text(255) | N | 1 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Header_Sales_Type__c | Text(255) | N |  |  |
| 10 | Header_Sales_Date |  |  |  |  |  | KPS_T_SALES_M | SALE_DATE | CHAR | 10 |  | Ready |  | Date | N | 2025-11-27 00:00:00 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Header_Sales_Date__c | Date | N |  |  |
| 11 | Header_Shift_No |  |  |  |  |  | KPS_T_SALES_M | SHIFT_NO | NUMBER | 2,0 |  | Ready |  | Text(255) | N | 1 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Header_Shift_No__c | Text(255) | N |  |  |
| 12 | Header_Create_Date |  |  |  |  |  | KPS_T_SALES_M | CREATE_DATE | CHAR | 19 |  | Ready |  | DateTime | N | 2025-01-27T10:30:00.000Z	 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Header_Create_Date__c | DateTime | N |  |  |
| 13 | Header_Trans_Date |  |  |  |  |  | KPS_T_SALES_M | TRANS_DATE | CHAR | 19 |  | Ready |  | DateTime | N | 2025-01-27T10:30:00.000Z	 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Header_Trans_Date__c | DateTime | N |  |  |
| 14 | Header_Member_Id |  |  |  |  |  | KPS_T_SALES_M | MEMBER_ID | VARCHAR2 | 20 |  | Ready |  | Text(255) | N |  |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Header_Member_Id__c | Text(255) | N |  |  |
| 15 | Header_Svc_Id |  |  |  |  |  | KPS_T_SALES_M | SVC_ID | VARCHAR2 | 20 |  | Ready |  | Text(255) | N |  |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Header_Svc_Id__c | Text(255) | N |  |  |
| 16 | Header_Name |  |  |  |  |  | KPS_T_SALES_M | NAME | VARCHAR2 | 200 |  | Ready |  | Text(255) | N | D.Whopper Jr Pork RVM |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Header_Name__c | Text(255) | N |  |  |
| 17 | Header_Flight_No |  |  |  |  |  | KPS_T_SALES_M | FLIGHT_NO | VARCHAR2 | 10 |  | Ready |  | Text(255) | N | BK 660013540 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Header_Flight_No__c | Text(255) | N |  |  |
| 18 | Header_Flight_Date |  |  |  |  |  | KPS_T_SALES_M | FLIGHT_DATE | VARCHAR2 | 19 |  | Ready |  | Date | N | 2025-11-27 00:00:00 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Header_Flight_Date__c | Date | N |  |  |
| 19 | Header_Nation_Code |  |  |  |  |  | KPS_T_SALES_M | NATION_CODE | VARCHAR2 | 10 |  | Ready |  | Text(255) | N |  |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Header_Nation_Code__c | Text(255) | N |  |  |
| 20 | Header_Passport_No |  |  |  |  |  | KPS_T_SALES_M | PASSPORT_NO | VARCHAR2 | 50 |  | Ready |  | Text(255) | N | A123456 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Header_Passport_No__c | Text(255) | N |  |  |
| 21 | Header_Birth_Date |  |  |  |  |  | KPS_T_SALES_M | BIRTH_DATE | VARCHAR2 | 10 |  | Ready |  | Date | N | 2025-11-27 00:00:00 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Header_Birth_Date__c | Date | N |  |  |
| 22 | Header_Sex |  |  |  |  |  | KPS_T_SALES_M | SEX | VARCHAR2 | 1 |  | Ready |  | picklist | N | Male, Female |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Header_Sex__c | picklist | N |  |  |
| 23 | Header_Vat_Type |  |  |  |  |  | KPS_T_SALES_M | VAT_TYPE | NUMBER | 1,0 |  | Ready |  | picklist / Text(255) | N |  |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Header_Vat_Type__c | picklist / Text(255) | N |  |  |
| 24 | Header_Vat_Rate |  |  |  |  |  | KPS_T_SALES_M | VAT_RATE | NUMBER | 6,2 |  | Ready |  | Number(18,2) | N | 0.00 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Header_Vat_Rate__c | Number(18,2) | N |  |  |
| 25 | Header_Amt_Exc_Vat |  |  |  |  |  | KPS_T_SALES_M | AMT_EXC_VAT | NUMBER | 16,2 |  | Ready |  | Number(18,2) | N | 0.00 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Header_Amt_Exc_Vat__c | Number(18,2) | N |  |  |
| 26 | Header_Vat_Amt |  |  |  |  |  | KPS_T_SALES_M | VAT_AMT | NUMBER | 16,2 |  | Ready |  | Number(18,2) | N | 0.00 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Header_Vat_Amt__c | Number(18,2) | N |  |  |
| 27 | Header_Amt_Inc_Vat |  |  |  |  |  | KPS_T_SALES_M | AMT_INC_VAT | NUMBER | 16,2 |  | Ready |  | Number(18,2) | N | 0.00 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Header_Amt_Inc_Vat__c | Number(18,2) | N |  |  |
| 28 | Header_Pro_Code |  |  |  |  |  | KPS_T_SALES_M | PRO_CODE | VARCHAR2 | 10 |  | Ready |  | Text(255) | N |  |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Header_Pro_Code__c | Text(255) | N |  |  |
| 29 | Header_Extra_Disc_Vat_Amt |  |  |  |  |  | KPS_T_SALES_M | EXTRA_DISC_VAT_AMT | NUMBER | 12,2 |  | Ready |  | Number(18,2) | N | 0.00 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Header_Extra_Disc_Vat_Amt__c | Number(18,2) | N |  |  |
| 30 | Header_Extra_Disc_Amt_Exc_Vat |  |  |  |  |  | KPS_T_SALES_M | EXTRA_DISC_AMT_EXC_VAT | NUMBER | 12,2 |  | Ready |  | Number(18,2) | N | 0.00 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Header_Extra_Disc_Amt_Exc_Vat__c | Number(18,2) | N |  |  |
| 31 | Header_Extra_Disc_Amt_Inc_Vat |  |  |  |  |  | KPS_T_SALES_M | EXTRA_DISC_AMT_INC_VAT | NUMBER | 12,2 |  | Ready |  | Number(18,2) | N | 0.00 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Header_Extra_Disc_Amt_Inc_Vat__c | Number(18,2) | N |  |  |
| 32 | Header_Disc_Vat_Amt |  |  |  |  |  | KPS_T_SALES_M | DISC_VAT_AMT | NUMBER | 16,2 |  | Ready |  | Number(18,2) | N | 0.00 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Header_Disc_Vat_Amt__c | Number(18,2) | N |  |  |
| 33 | Header_Disc_Amt_Exc_Vat |  |  |  |  |  | KPS_T_SALES_M | DISC_AMT_EXC_VAT | NUMBER | 16,2 |  | Ready |  | Number(18,2) | N | 0.00 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Header_Disc_Amt_Exc_Vat__c | Number(18,2) | N |  |  |
| 34 | Header_Disc_Amt_Inc_Vat |  |  |  |  |  | KPS_T_SALES_M | DISC_AMT_INC_VAT | NUMBER | 16,2 |  | Ready |  | Number(18,2) | N | 0.00 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Header_Disc_Amt_Inc_Vat__c | Number(18,2) | N |  |  |
| 35 | Header_Disc_Avg_Percentage |  |  |  |  |  | KPS_T_SALES_M | DISC_AVG_PERCENTAGE | NUMBER | 12,2 |  | Ready |  | Number(3,2) / percent | N | 50 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Header_Disc_Avg_Percentage__c | Number(3,2) / percent | N |  |  |
| 36 | Header_Service_Charge_Type |  |  |  |  |  | KPS_T_SALES_M | SERVICE_CHARGE_TYPE | NUMBER | 1,0 |  | Ready |  | picklist | N |  |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Header_Service_Charge_Type__c | picklist | N |  |  |
| 37 | Header_Service_Charge_Exc_Vat |  |  |  |  |  | KPS_T_SALES_M | SERVICE_CHARGE_EXC_VAT | NUMBER | 12,2 |  | Ready |  | Number(18,2) | N | 0.00 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Header_Service_Charge_Exc_Vat__c | Number(18,2) | N |  |  |
| 38 | Header_Service_Charge_Vat |  |  |  |  |  | KPS_T_SALES_M | SERVICE_CHARGE_VAT | NUMBER | 12,2 |  | Ready |  | Number(18,2) | N | 0.00 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Header_Service_Charge_Vat__c | Number(18,2) | N |  |  |
| 39 | Header_Service_Charge_Inc_Vat |  |  |  |  |  | KPS_T_SALES_M | SERVICE_CHARGE_INC_VAT | NUMBER | 12,2 |  | Ready |  | Number(18,2) | N | 0.00 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Header_Service_Charge_Inc_Vat__c | Number(18,2) | N |  |  |
| 40 | Header_Net_Exc_Vat |  |  |  |  |  | KPS_T_SALES_M | NET_EXC_VAT | NUMBER | 12,2 |  | Ready |  | Number(18,2) | N | 0.00 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Header_Net_Exc_Vat__c | Number(18,2) | N |  |  |
| 41 | Header_Net_Vat |  |  |  |  |  | KPS_T_SALES_M | NET_VAT | NUMBER | 12,2 |  | Ready |  | Number(18,2) | N | 0.00 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Header_Net_Vat__c | Number(18,2) | N |  |  |
| 42 | Header_Net_Inc_Vat |  |  |  |  |  | KPS_T_SALES_M | NET_INC_VAT | NUMBER | 12,2 |  | Ready |  | Number(18,2) | N | 0.00 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Header_Net_Inc_Vat__c | Number(18,2) | N |  |  |
| 43 | Header_Void_Date |  |  |  |  |  | KPS_T_SALES_M | VOID_DATE | CHAR | 19 |  | Ready |  | Date | N | 2025-11-27 00:00:00 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Header_Void_Date__c | Date | N |  |  |
| 44 | Header_Cancel_Tax_Invoice |  |  |  |  |  | KPS_T_SALES_M | CANCEL_TAX_INVOICE | VARCHAR2 | 50 |  | Ready |  | Text(255) | N |  |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Header_Cancel_Tax_Invoice__c | Text(255) | N |  |  |
| 45 | Header_Cancel_Tax_Invoice_Pos_Name |  |  |  |  |  | KPS_T_SALES_M | CANCEL_TAX_INVOICE_POS_NAME | VARCHAR2 | 50 |  | Ready |  | Text(255) | N |  |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Header_Cancel_Tax_Invoice_Pos_Name__c | Text(255) | N |  |  |
| 46 | Header_Void_Reason |  |  |  |  |  | KPS_T_SALES_M | VOID_REASON | VARCHAR2 | 200 |  | Ready |  | Text(255) | N |  |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Header_Void_Reason__c | Text(255) | N |  |  |
| 47 | Header_RC_Code |  |  |  |  |  | KPS_T_SALES_M | RC_CODE | VARCHAR2 | 60 |  | Ready |  | Text(255) | N | 252363230082146 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Header_RC_Code__c | Text(255) | N |  |  |
| 48 | Header_Doc_Date |  |  |  |  |  | KPS_T_SALES_M | DOC_DATE | VARCHAR2 | 19 |  | Ready |  | Date | N | 2025-11-27 00:00:00 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Header_Doc_Date__c | Date | N |  |  |
| 49 | Header_Amt |  |  |  |  |  | ไม่มี |  |  |  |  | Ready |  | Number(18,2) | N | 0.00 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Header_Amt__c | Number(18,2) | N |  |  |
| 50 | Detail_Business_Type |  |  |  |  |  | ไม่มี |  |  |  |  | Ready |  | picklist | N | bank, bu, local_product |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Detail_Business_Type__c | picklist | N |  |  |
| 51 | Detail_Shop_Code |  |  |  |  |  | KPS_T_SALES_MD | SHOP_CODE | VARCHAR2 | 20 |  | Ready |  | Text(255) | N | 904002 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Detail_Shop_Code__c | Text(255) | N |  |  |
| 52 | Detail_Branch_Code |  |  |  |  |  | KPS_T_SALES_MD | BRANCH_CODE | VARCHAR2 | 20 |  | Ready |  | Text(255) | N | 1 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Detail_Branch_Code__c | Text(255) | N |  |  |
| 53 | Detail_Sales_No |  |  |  |  |  | KPS_T_SALES_MD | SALE_NO | VARCHAR2 | 50 |  | Ready |  | Text(255) | N | 2025112701 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Detail_Sales_No__c | Text(255) | N |  |  |
| 54 | Detail_Pos_No |  |  |  |  |  | KPS_T_SALES_MD | POS_NO | VARCHAR2 | 50 |  | Ready |  | Text(255) | N | E051120002B0239 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Detail_Pos_No__c | Text(255) | N |  |  |
| 55 | Detail_Sales_Type |  |  |  |  |  | KPS_T_SALES_MD | SALE_TYPE | NUMBER | 1,0 |  | Ready |  | Text(255) | N | 1 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Detail_Sales_Type__c | Text(255) | N |  |  |
| 56 | Detail_Sales_Date |  |  |  |  |  | KPS_T_SALES_MD | SALE_DATE | CHAR | 10 |  | Ready |  | Date | N | 2025-11-27 00:00:00 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Detail_Sales_Date__c | Date | N |  |  |
| 57 | Detail_Seq |  |  |  |  |  | KPS_T_SALES_MD | SEQ | NUMBER | 9,0 |  | Ready |  | Text(255) | N | 1 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Detail_Seq__c | Text(255) | N |  |  |
| 58 | Detail_Aot_Product_Cate_Code |  |  |  |  |  | KPS_T_SALES_MD | AOT_PRODUCT_CATE_CODE | VARCHAR2 | 50 |  | Ready |  | Text(255) | N |  |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Detail_Aot_Product_Cate_Code__c | Text(255) | N |  |  |
| 59 | Detail_Aot_Product_Cate_Name |  |  |  |  |  | KPS_T_SALES_MD | AOT_PRODUCT_CATE_NAME | VARCHAR2 | 100 |  | Ready |  | Text(255) | N |  |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Detail_Aot_Product_Cate_Name__c | Text(255) | N |  |  |
| 60 | Detail_Std_Cate_Code |  |  |  |  |  |  |  |  |  |  | Ready |  | Text(255) | N | 5FIB, 5FAA |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Detail_Std_Cate_Code__c | Text(255) | N |  |  |
| 61 | Detail_Prod_Serv_Code |  |  |  |  |  | KPS_T_SALES_MD | PROD_SERV_CODE | VARCHAR2 | 100 |  | Ready |  | Text(255) | N |  |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Detail_Prod_Serv_Code__c | Text(255) | N |  |  |
| 62 | Detail_Prod_Serv_Name |  |  |  |  |  |  |  |  |  |  | Ready |  | Text(255) | N |  |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Detail_Prod_Serv_Name__c | Text(255) | N |  |  |
| 63 | Detail_Vat_Type |  |  |  |  |  |  |  |  |  |  | Ready |  | picklist | N |  |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Detail_Vat_Type__c | picklist | N |  |  |
| 64 | Detail_Vat_Rate |  |  |  |  |  | KPS_T_SALES_MD | VAT_RATE | NUMBER | 5,2 |  | Ready |  | Number(18,2) | N | 0.00 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Detail_Vat_Rate__c | Number(18,2) | N |  |  |
| 65 | Detail_Prod_Serv_Qty |  |  |  |  |  | KPS_T_SALES_MD | PROD_SERV_QTY | NUMBER | 16,2 |  | Ready |  | Number(18,0) | N | 0.00 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Detail_Prod_Serv_Qty__c | Number(18,0) | N |  |  |
| 66 | Detail_Unit_Disc_Percentage |  |  |  |  |  | KPS_T_SALES_MD | UNIT_DISC_PERCENTAGE | NUMBER | 12,2 |  | Ready |  | Number(3,2) / percent | N | 50 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Detail_Unit_Disc_Percentage__c | Number(3,2) / percent | N |  |  |
| 67 | Detail_Unit_Code |  |  |  |  |  | KPS_T_SALES_MD | UNIT_CODE | VARCHAR2 | 10 |  | Ready |  | Text(255) | N |  |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Detail_Unit_Code__c | Text(255) | N |  |  |
| 68 | Detail_Aot_Price_Exc_Vat |  |  |  |  |  | KPS_T_SALES_MD | AOT_PRICE_EXC_VAT | NUMBER | 16,2 |  | Ready |  | Number(18,2) | N | 0.00 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Detail_Aot_Price_Exc_Vat__c | Number(18,2) | N |  |  |
| 69 | Detail_Aot_Price_Inc_Vat |  |  |  |  |  | KPS_T_SALES_MD | AOT_PRICE_INC_VAT | NUMBER | 16,2 |  | Ready |  | Number(18,2) | N | 0.00 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Detail_Aot_Price_Inc_Vat__c | Number(18,2) | N |  |  |
| 70 | Detail_Unit_Amt_Exc_Vat |  |  |  |  |  | KPS_T_SALES_MD | UNIT_AMT_EXC_VAT | NUMBER | 12,2 |  | Ready |  | Number(18,2) | N | 0.00 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Detail_Unit_Amt_Exc_Vat__c | Number(18,2) | N |  |  |
| 71 | Detail_Unit_Amt_Vat |  |  |  |  |  | KPS_T_SALES_MD | UNIT_AMT_VAT | NUMBER | 12,2 |  | Ready |  | Number(18,2) | N | 0.00 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Detail_Unit_Amt_Vat__c | Number(18,2) | N |  |  |
| 72 | Detail_Unit_Amt_Inc_Vat |  |  |  |  |  | KPS_T_SALES_MD | UNIT_AMT_INC_VAT | NUMBER | 12,2 |  | Ready |  | Number(18,2) | N | 0.00 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Detail_Unit_Amt_Inc_Vat__c | Number(18,2) | N |  |  |
| 73 | Detail_Unit_Disc_Amt_Exc_Vat |  |  |  |  |  | KPS_T_SALES_MD | UNIT_DISC_AMT_EXC_VAT | NUMBER | 12,2 |  | Ready |  | Number(18,2) | N | 0.00 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Detail_Unit_Disc_Amt_Exc_Vat__c | Number(18,2) | N |  |  |
| 74 | Detail_Unit_Disc_Vat_Amt |  |  |  |  |  | KPS_T_SALES_MD | UNIT_DISC_VAT_AMT | NUMBER | 12,2 |  | Ready |  | Number(18,2) | N | 0.00 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Detail_Unit_Disc_Vat_Amt__c | Number(18,2) | N |  |  |
| 75 | Detail_Unit_Disc_Inc_Vat_Amt |  |  |  |  |  | KPS_T_SALES_MD | UNIT_DISC_INC_VAT_AMT | NUMBER | 12,2 |  | Ready |  | Number(18,2) | N | 0.00 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Detail_Unit_Disc_Inc_Vat_Amt__c | Number(18,2) | N |  |  |
| 76 | Detail_Unit_Net_Amt_Exc_Vat |  |  |  |  |  | KPS_T_SALES_MD | UNIT_NET_AMT_EXC_VAT | NUMBER | 12,2 |  | Ready |  | Number(18,2) | N | 0.00 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Detail_Unit_Net_Amt_Exc_Vat__c | Number(18,2) | N |  |  |
| 77 | Detail_Unit_Net_Amt_Vat |  |  |  |  |  | KPS_T_SALES_MD | UNIT_NET_AMT_VAT | NUMBER | 12,2 |  | Ready |  | Number(18,2) | N | 0.00 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Detail_Unit_Net_Amt_Vat__c | Number(18,2) | N |  |  |
| 78 | Detail_Unit_Net_Amt_Inc_Vat |  |  |  |  |  | KPS_T_SALES_MD | UNIT_NET_AMT_INC_VAT | NUMBER | 12,2 |  | Ready |  | Number(18,2) | N | 0.00 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Detail_Unit_Net_Amt_Inc_Vat__c | Number(18,2) | N |  |  |
| 79 | Detail_Total_Amt_Exc_Vat |  |  |  |  |  | KPS_T_SALES_MD | TOTAL_AMT_EXC_VAT | NUMBER | 12,2 |  | Ready |  | Number(18,2) | N | 0.00 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Detail_Total_Amt_Exc_Vat__c | Number(18,2) | N |  |  |
| 80 | Detail_Total_Amt_Vat |  |  |  |  |  | KPS_T_SALES_MD | TOTAL_AMT_VAT | NUMBER | 12,2 |  | Ready |  | Number(18,2) | N | 0.00 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Detail_Total_Amt_Vat__c | Number(18,2) | N |  |  |
| 81 | Detail_Total_Amt_Inc_Vat |  |  |  |  |  | KPS_T_SALES_MD | TOTAL_AMT_INC_VAT | NUMBER | 12,2 |  | Ready |  | Number(18,2) | N | 0.00 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Detail_Total_Amt_Inc_Vat__c | Number(18,2) | N |  |  |
| 82 | Detail_Total_Disc_Amt_Exc_Vat |  |  |  |  |  | KPS_T_SALES_MD | TOTAL_DISC_AMT_EXC_VAT | NUMBER | 12,2 |  | Ready |  | Number(18,2) | N | 0.00 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Detail_Total_Disc_Amt_Exc_Vat__c | Number(18,2) | N |  |  |
| 83 | Detail_Total_Disc_Vat_Amt |  |  |  |  |  | KPS_T_SALES_MD | TOTAL_DISC_VAT_AMT | NUMBER | 12,2 |  | Ready |  | Number(18,2) | N | 0.00 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Detail_Total_Disc_Vat_Amt__c | Number(18,2) | N |  |  |
| 84 | Detail_Total_Disc_Amt_Inc_Vat |  |  |  |  |  | KPS_T_SALES_MD | TOTAL_DISC_AMT_INC_VAT | NUMBER | 12,2 |  | Ready |  | Number(18,2) | N | 0.00 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Detail_Total_Disc_Amt_Inc_Vat__c | Number(18,2) | N |  |  |
| 85 | Detail_Total_Net_Amt_Exc_Vat |  |  |  |  |  | KPS_T_SALES_MD | TOTAL_NET_AMT_EXC_VAT | NUMBER | 12,2 |  | Ready |  | Number(18,2) | N | 0.00 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Detail_Total_Net_Amt_Exc_Vat__c | Number(18,2) | N |  |  |
| 86 | Detail_Total_Net_Amt_Vat |  |  |  |  |  | KPS_T_SALES_MD | TOTAL_NET_AMT_VAT | NUMBER | 12,2 |  | Ready |  | Number(18,2) | N | 0.00 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Detail_Total_Net_Amt_Vat__c | Number(18,2) | N |  |  |
| 87 | Detail_Total_Net_Amt_Inc_Vat |  |  |  |  |  | KPS_T_SALES_MD | TOTAL_NET_AMT_INC_VAT | NUMBER | 12,2 |  | Ready |  | Number(18,2) | N | 0.00 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Detail_Total_Net_Amt_Inc_Vat__c | Number(18,2) | N |  |  |
| 88 | Detail_Total_Display_Amt |  |  |  |  |  | KPS_T_SALES_MD | TOTAL_DISPLAY_AMT | NUMBER | 12,2 |  | Ready |  | Number(18,2) | N | 0.00 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Detail_Total_Display_Amt__c | Number(18,2) | N |  |  |
| 89 | Detail_Amt_Exc_Vat |  |  |  |  |  |  |  |  |  |  | Ready |  | Number(18,2) | N | 0.00 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Detail_Amt_Exc_Vat__c | Number(18,2) | N |  |  |
| 90 | Detail_Vat_Amt |  |  |  |  |  |  |  |  |  |  | Ready |  | Number(18,2) | N | 0.00 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Detail_Vat_Amt__c | Number(18,2) | N |  |  |
| 91 | Detail_Amt_Inc_Vat |  |  |  |  |  |  |  |  |  |  | Ready |  | Number(18,2) | N | 0.00 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Detail_Amt_Inc_Vat__c | Number(18,2) | N |  |  |
| 92 | Detail_Pro_Code |  |  |  |  |  | KPS_T_SALES_MD | PRO_CODE | VARCHAR2 | 10 |  | Ready |  | Number(18,2) | N | 0.00 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Detail_Pro_Code__c | Number(18,2) | N |  |  |
| 93 | Detail_Disc_Price_Exc_Vat |  |  |  |  |  | KPS_T_SALES_MD | DISC_PRICE_EXC_VAT | NUMBER | 16,2 |  | Ready |  | Number(18,2) | N | 0.00 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Detail_Disc_Price_Exc_Vat__c | Number(18,2) | N |  |  |
| 94 | Detail_Disc_Price_Inc_Vat |  |  |  |  |  | KPS_T_SALES_MD | DISC_PRICE_INC_VAT | NUMBER | 16,2 |  | Ready |  | Number(18,2) | N | 0.00 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Detail_Disc_Price_Inc_Vat__c | Number(18,2) | N |  |  |
| 95 | Detail_Service_Charge |  |  |  |  |  | KPS_T_SALES_MD | SERVICE_CHARGE | NUMBER | 16,2 |  | Ready |  | Text(255) | N |  |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Detail_Service_Charge__c | Text(255) | N |  |  |
| 96 | Detail_Currency_Code |  |  |  |  |  |  |  |  |  |  | Ready |  | Text(255) | N | THB, AED, USD |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Detail_Currency_Code__c | Text(255) | N |  |  |
| 97 | Detail_Old_Balance |  |  |  |  |  |  |  |  |  |  | Ready |  | Number(18,2) | N | 0.00 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Detail_Old_Balance__c | Number(18,2) | N |  |  |
| 98 | Detail_Rcv_Frm_Ho |  |  |  |  |  |  |  |  |  |  | Ready |  | Number(18,2) | N | 0.00 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Detail_Rcv_Frm_Ho__c | Number(18,2) | N |  |  |
| 99 | Detail_Bought |  |  |  |  |  |  |  |  |  |  | Ready |  | Number(18,2) | N | 0.00 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Detail_Bought__c | Number(18,2) | N |  |  |
| 100 | Detail_Sold |  |  |  |  |  |  |  |  |  |  | Ready |  | Number(18,2) | N | 0.00 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Detail_Sold__c | Number(18,2) | N |  |  |
| 101 | Detail_Sent_To_Ho |  |  |  |  |  |  |  |  |  |  | Ready |  | Number(18,2) | N | 0.00 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Detail_Sent_To_Ho__c | Number(18,2) | N |  |  |
| 102 | Detail_New_Balance |  |  |  |  |  |  |  |  |  |  | Ready |  | Number(18,2) | N | 0.00 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Detail_New_Balance__c | Number(18,2) | N |  |  |
| 103 | Detail_Old_Balance_Thb |  |  |  |  |  |  |  |  |  |  | Ready |  | Number(18,2) | N | 0.00 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Detail_Old_Balance_Thb__c | Number(18,2) | N |  |  |
| 104 | Detail_Rcv_Frm_Ho_Thb |  |  |  |  |  |  |  |  |  |  | Ready |  | Number(18,2) | N | 0.00 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Detail_Rcv_Frm_Ho_Thb__c | Number(18,2) | N |  |  |
| 105 | Detail_Bought_Thb |  |  |  |  |  |  |  |  |  |  | Ready |  | Number(18,2) | N | 0.00 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Detail_Bought_Thb__c | Number(18,2) | N |  |  |
| 106 | Detail_Sold_Thb |  |  |  |  |  |  |  |  |  |  | Ready |  | Number(18,2) | N | 0.00 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Detail_Sold_Thb__c | Number(18,2) | N |  |  |
| 107 | Detail_Sent_To_Ho_Thb |  |  |  |  |  |  |  |  |  |  | Ready |  | Number(18,2) | N | 0.00 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Detail_Sent_To_Ho_Thb__c | Number(18,2) | N |  |  |
| 108 | Detail_New_Balance_Thb |  |  |  |  |  |  |  |  |  |  | Ready |  | Number(18,2) | N | 0.00 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Detail_New_Balance_Thb__c | Number(18,2) | N |  |  |
| 109 | Detail_Avg_Buy_Rate |  |  |  |  |  |  |  |  |  |  | Ready |  | Number(18,2) | N | 0.00 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Detail_Avg_Buy_Rate__c | Number(18,2) | N |  |  |
| 110 | Detail_Baht_Eef_Rate |  |  |  |  |  |  |  |  |  |  | Ready |  | Number(18,2) | N | 0.00 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Detail_Baht_Eef_Rate__c | Number(18,2) | N |  |  |
| 111 | Detail_Gain_Loss_Amount |  |  |  |  |  |  |  |  |  |  | Ready |  | Number(18,2) | N | 0.00 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Detail_Gain_Loss_Amount__c | Number(18,2) | N |  |  |
| 112 | Detail_Avg_Sell_Rate |  |  |  |  |  |  |  |  |  |  | Ready |  | Number(18,2) | N | 0.00 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Detail_Avg_Sell_Rate__c | Number(18,2) | N |  |  |
| 113 | Detail_Nom_Rate |  |  |  |  |  |  |  |  |  |  | Ready |  | Number(18,2) | N | 0.00 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Detail_Nom_Rate__c | Number(18,2) | N |  |  |
| 114 | Payment_Business_Type |  |  |  |  |  |  |  |  |  |  | Ready |  | picklist | N | bank, bu |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Payment_Business_Type__c | picklist | N |  |  |
| 115 | Payment_Shop_Code |  |  |  |  |  | KPS_T_SALESPAY_MD | SHOP_CODE | VARCHAR2 | 20 |  | Ready |  | Text(255) | N | 904002 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Payment_Shop_Code__c | Text(255) | N |  |  |
| 116 | Payment_Branch_Code |  |  |  |  |  | KPS_T_SALESPAY_MD | BRANCH_CODE | VARCHAR2 | 20 |  | Ready |  | Text(255) | N | 1 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Payment_Branch_Code__c | Text(255) | N |  |  |
| 117 | Payment_Sale_No |  |  |  |  |  | KPS_T_SALESPAY_MD | SALE_NO | VARCHAR2 | 50 |  | Ready |  | Text(255) | N | 2025112701 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Payment_Sale_No__c | Text(255) | N |  |  |
| 118 | Payment_Pos_No |  |  |  |  |  | KPS_T_SALESPAY_MD | POS_NO | VARCHAR2 | 50 |  | Ready |  | Text(255) | N | E051120002B0239 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Payment_Pos_No__c | Text(255) | N |  |  |
| 119 | Payment_Sale_Type |  |  |  |  |  | KPS_T_SALESPAY_MD | SALE_TYPE | NUMBER | 1,0 |  | Ready |  | Text(255) | N | 1 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Payment_Sale_Type__c | Text(255) | N |  |  |
| 120 | Payment_Sale_Date |  |  |  |  |  | KPS_T_SALESPAY_MD | SALE_DATE | CHAR | 10 |  | Ready |  | Date | N | 2025-11-27 00:00:00 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Payment_Sale_Date__c | Date | N |  |  |
| 121 | Payment_Pay_Type |  |  |  |  |  | KPS_T_SALESPAY_MD | PAY_TYPE | NUMBER | 1,0 |  | Ready |  | picklist | N |  |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Payment_Pay_Type__c | picklist | N |  |  |
| 122 | Payment_Currency_Code |  |  |  |  |  | KPS_T_SALESPAY_MD | CURRENCY_CODE | VARCHAR2 | 5 |  | Ready |  | Text(255) | N | THB, AED, USD |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Payment_Currency_Code__c | Text(255) | N |  |  |
| 123 | Payment_Rate |  |  |  |  |  | KPS_T_SALESPAY_MD | RATE | NUMBER | 16,6 |  | Ready |  | Number(18,2) | N | 0.00 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Payment_Rate__c | Number(18,2) | N |  |  |
| 124 | Payment_Amount |  |  |  |  |  | KPS_T_SALESPAY_MD | AMOUNT | NUMBER | 16,2 |  | Ready |  | Number(18,2) | N | 0.00 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Payment_Amount__c | Number(18,2) | N |  |  |
| 125 | Payment_Baht_Amt |  |  |  |  |  | KPS_T_SALESPAY_MD | BAHT_AMT | NUMBER | 16,2 |  | Ready |  | Number(18,2) | N | 0.00 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Payment_Baht_Amt__c | Number(18,2) | N |  |  |
| 126 | Payment_Sum_Header_Amt |  |  |  |  |  | ไม่มี |  |  |  |  | Ready |  | Number(18,2) | N | 0.00 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Payment_Sum_Header_Amt__c | Number(18,2) | N |  |  |
| 127 | Payment_Sum_Dtl_Amt |  |  |  |  |  | ไม่มี |  |  |  |  | Ready |  | Number(18,2) | N | 0.00 |  |  |  |  |  |  |  |  |  |  |  |  | TMS_Payment_Sum_Dtl_Amt__c | Number(18,2) | N |  |  |

---

## 20_Financial Transaction (Detai

| No. | SFDC Field Name (EN) | SFDC Field Name (TH) | Source Field API Name | Source Field Type | Source Field Length | VULLABLE (N=Required) | KP Table | KP Field Name | KP Field Type | KP Field Length | VULLABLE (N=Required).1 | Progress | Confirm | Type | Required | Sample Data | Description | Status | User/KP Feedback | Remark | Help Text | Track History | External ID | Track History.1 | Encrypted | Page Layout | Length | Source Field API Name.1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Rental |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Rental Fee Per Month | ค่าเช่าต่อเดือน |  |  |  |  |  |  |  |  |  | Ready |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Days Per Month | จำนวนวันที่คำนวณค่าเช่า |  |  |  |  |  |  |  |  |  | Ready |  | Number |  |  |  |  |  | จำนวนวันที่คำนวณค่าเช่า = (จำนวนวันในเดือน – จำนวนวันที่นับจำกวันส่งมอบพื้นที่ + 1) |  |  |  |  |  |  |  |  |
|  | Day Since Handover | จำนวนวันที่นับจากวันส่งมอบพื้นที่ |  |  |  |  |  |  |  |  |  | Ready |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Building Land Tax | ค่าภาษีโรงเรือน และที่ดิน |  |  |  |  |  |  |  |  |  | Ready |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Service Fee | ค่าธรรมเนียมการใช้บริการ |  |  |  |  |  |  |  |  |  | Ready |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Amount charge | จำนวนเงินที่เรียกเก็บ |  |  |  |  |  |  |  |  |  | Ready |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Monthly Rental Fee Charge | ค่าเช่าพื้นที่รายเดือนที่เรียกเก็บ |  |  |  |  |  |  |  |  |  | Ready |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Monthly Rental Fee Charge If Discount | ค่าเช่าพื้นที่รายเดือนที่เรียกเก็บทั้งหมด ถ้ามีส่วนลด |  |  |  |  |  |  |  |  |  | Ready |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Minimum Guarantee |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Concession | สนามบิน |  |  |  |  |  |  |  |  |  | Ready |  | Text |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Contract No. | เลขสัญญาเช่า |  |  |  |  |  |  |  |  |  | Ready |  | Text |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Minimum Guarantee | ส่วนแบ่งรายได้ขั้นต่ำ |  |  |  |  |  |  |  |  |  | Ready |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Days Per Month | จำนวนวันที่คำนวณค่าเช่า |  |  |  |  |  |  |  |  |  | Ready |  | Number |  |  |  |  |  | จำนวนวันที่คำนวณค่าเช่า = (จำนวนวันในเดือน – จำนวนวันที่นับจำกวันส่งมอบพื้นที่ + 1) |  |  |  |  |  |  |  |  |
|  | Day Since Handover | จำนวนวันที่นับจากวันส่งมอบพื้นที่ |  |  |  |  |  |  |  |  |  | Ready |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Amount charge | จำนวนเงินออกใบแจ้งหนี้ |  |  |  |  |  |  |  |  |  | Ready |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Invoice Amount |  |  |  |  |  |  |  |  |  |  | Ready |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | New Minimum Guarantee | ส่วนแบ่งรายได้ขั้นต่ำ ใหม่ |  |  |  |  |  |  |  |  |  | Ready |  | Number |  |  |  |  |  | มีการคำนวณได้ 3 ประเภทขึ้นอยู่กับสัญญา |  |  |  |  |  |  |  |  |
|  | Whichever Higher Minimum Guarantee Estimate | ยอดที่สูงกว่าสำหรับกรณีคำนวณ Minimum Guarantee Estimate |  |  |  |  |  |  |  |  |  | Ready |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Whichever Higher Minimum Guarantee Actual | ยอดที่สูงกว่าสำหรับกรณีคำนวณ Minimum Guarantee Actual |  |  |  |  |  |  |  |  |  | Ready |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Estimate Month End Adjust Amount | ยอดที่ปรับปรุงตอนสิ้นเดือน |  |  |  |  |  |  |  |  |  | Ready |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Monthly Accounting Adjustment | ยอดที่ต้องปรับปรุงทางบัญชีเพิ่มเติมในเดือนประกอบการนั้นๆ |  |  |  |  |  |  |  |  |  | Ready |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Adjusted Invoice Amount | ยอดที่ต้องออกใบแจ้งหนี้ |  |  |  |  |  |  |  |  |  | Ready |  | Number |  |  |  |  |  | ยอดที่ต้องปรับปรุงทางบัญชีเพิ่มเติมในเดือนประกอบการนั้นๆ = Whichever Higher (Actual) - Whichever Higher (Estimate) |  |  |  |  |  |  |  |  |
|  | Adjusted Credit Amount | ยอดที่ต้องออกใบลดหนี้ |  |  |  |  |  |  |  |  |  | Ready |  | Number |  |  |  |  |  | ยอดที่ต้องออกใบแจ้งหนี้ / ใบลดหนี้ เพิ่มเติม = Whichever Higher (Actual) - Whichever Higher (Revenue Sharing) |  |  |  |  |  |  |  |  |
|  | Final Adjusted Invoice Amount | ยอดสุทธิที่ต้องออกใบแจ้งหนี้ เพิ่มเติม |  |  |  |  |  |  |  |  |  | Ready |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Final Adjusted Credit Amount | ยอดสุทธิที่ต้องออกใบลดหนี้ เพิ่มเติม |  |  |  |  |  |  |  |  |  | Ready |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | New Minimum Guarantee Fixed Amount | ส่วนแบ่งรายได้ขั้นต่ำรายปี กรณี Fixed Amount |  |  |  |  |  |  |  |  |  | Ready |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | New Minimum Guarantee PG | ส่วนแบ่งรายได้ขั้นต่ำรายปี กรณีปรับตาม PG |  |  |  |  |  |  |  |  |  | Ready |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | New Minimum Guarantee Fixed Rate | ส่วนแบ่งรายได้ขั้นต่ำรายปี กรณี Fixed Rate |  |  |  |  |  |  |  |  |  | Ready |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | New Minimum Guarantee MAGi | ส่วนแบ่งรายได้ขั้นต่ำรายปี กรณี MAG(i) |  |  |  |  |  |  |  |  |  | Ready |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Passenger Growth |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Estimate Passenger Growth Rate Per Month | อัตราการเติบโตผู้โดยสารต่อเดือนโดยประมาณ |  |  |  |  |  |  |  |  |  | Ready |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Estimate Passenger Growth Rate Per Year | อัตราการเติบโตผู้โดยสารต่อปีโดยประมาณ |  |  |  |  |  |  |  |  |  | Ready |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Actual Passenger Growth Rate Per Month | อัตราการเติบโตผู้โดยสารต่อเดือน |  |  |  |  |  |  |  |  |  | Ready |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Actual Passenger Growth Rate Per Year | อัตราการเติบโตผู้โดยสารต่อปี |  |  |  |  |  |  |  |  |  | Ready |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Estimate Current Passenger Amount | จำนวนผู้โดยสารรอบปัจจุบันโดยประมาณ |  |  |  |  |  |  |  |  |  | Ready |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Estimate Previous Passenger Amount | จำนวนผู้โดยสารรอบก่อนหน้าโดยประมาณ |  |  |  |  |  |  |  |  |  | Ready |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Concession | สนามบิน |  |  |  |  |  |  |  |  |  | Ready |  | Text |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Whichever Higher Estimate | ยอดที่สูงกว่าโดยประมาณ |  |  |  |  |  |  |  |  |  | Ready |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Whichever Higher Actual | ยอดที่สูงกว่า |  |  |  |  |  |  |  |  |  | Ready |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Avg Passenger | จำนวนผู้โดยสารโดยเฉลี่ย |  |  |  |  |  |  |  |  |  | Ready |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Passenger Growth Rate | อัตราการเติบโตผู้โดยสาร |  |  |  |  |  |  |  |  |  | Ready |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Revenue Sharing |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Whichever Higher Revenue Sharing | ยอดที่สูงกว่าสำหรับกรณีคำนวณ Revenue Sharing |  |  |  |  |  |  |  |  |  | Ready |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Charged_Revenue_Sharing_Amount__c | ยอดที่เรียกเก็บส่วนแบ่งรายได้จากการประกอบกิจการ |  |  |  |  |  |  |  |  |  | Ready |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Invoice_Charged_Amount__c | ยอดที่เรียกเก็บตามใบแจ้งหนี้ |  |  |  |  |  |  |  |  |  | Ready |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Electric |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Concession | สนามบิน |  |  |  |  |  |  |  |  |  | Ready |  | Text |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Usage Unit | จำนวนหน่วยที่ใช้จริง |  |  |  |  |  |  |  |  |  | Ready |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Current Meter Reading | หน่วยมิเตอร์ปัจจุบัน |  |  |  |  |  |  |  |  |  | Ready |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Last Meter Reading | หน่วยมิเตอร์ครั้งก่อนหน้า |  |  |  |  |  |  |  |  |  | Ready |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | TOU Current Meter Reading | หน่วยมิเตอร์ปัจจุบัน TOU |  |  |  |  |  |  |  |  |  | Ready |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | TOU Last Meter Reading | หน่วยมิเตอร์ครั้งก่อนหน้า TOU |  |  |  |  |  |  |  |  |  | Ready |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Electrical Charge Per Unit | ค่าไฟต่อหน่วย |  |  |  |  |  |  |  |  |  | Ready |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Service Meter | ค่ารักษามิเตอร์ |  |  |  |  |  |  |  |  |  | Ready |  | Number |  |  | Service Meter SVB & DMK = 33.29 บาท Service Meter HKT = 46.16 บาท |  |  |  |  |  |  |  |  |  |  |  |
|  | FT Charge | ค่า FT |  |  |  |  |  |  |  |  |  | Ready |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Service Charge | ค่าบริการ |  |  |  |  |  |  |  |  |  | Ready |  | Number |  |  | Service Charge = (รวมค่ำพลังงำนไฟฟ้ำ) + Service Meter + FT  * 0.1 ปัดทศนิยม 2 ตำแหน่ง |  |  |  |  |  |  |  |  |  |  |  |
|  | Total Electrical Bill | ค่าไฟทั้งสิ้น |  |  |  |  |  |  |  |  |  | Ready |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Total Electrical AOT | ค่าไฟทั้งสิ้นจาก AOT |  |  |  |  |  |  |  |  |  | Ready |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Electrical Charge Variance | ส่วนต่างของค่าไฟ |  |  |  |  |  |  |  |  |  | Ready |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Difference Ratio | สัดส่วนส่วนต่าง |  |  |  |  |  |  |  |  |  | Ready |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Electrical Bill Adjustment Amount | ยอดปรับปรุงค่าไฟ |  |  |  |  |  |  |  |  |  | Ready |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Electrical Monthly Adjusted Invoice Amount | ยอดปรับปรุงค่าไฟที่ต้องออกใบแจ้งหนี้ |  |  |  |  |  |  |  |  |  | Ready |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Electrical Monthly Adjusted Credit Amount | ยอดปรับปรุงค่าไฟที่ต้องออกใบลดหนี้ |  |  |  |  |  |  |  |  |  | Ready |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Invoice Owner | owner ตาม invoice |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Owner | owner ตามเรียกเก็บจริง |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Water |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Concession | สนามบิน |  |  |  |  |  |  |  |  |  | Ready |  | Text |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Usage Unit | จำนวนหน่วยที่ใช้จริง |  |  |  |  |  |  |  |  |  | Ready |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Current Meter Reading Value | หน่วยมิเตอร์ปัจจุบัน |  |  |  |  |  |  |  |  |  | Ready |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Last Meter Reading Value | หน่วยมิเตอร์ครั้งก่อนหน้า |  |  |  |  |  |  |  |  |  | Ready |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Water Charge Per Unit | ค่าน้ําต่อหน่วย |  |  |  |  |  |  |  |  |  | Ready |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Wastewater Treatment Fee | ค่าบำบัดน้ำ |  |  |  |  |  |  |  |  |  | Ready |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Maintenance Fee | ค่าบำรุงรักษามาตร |  |  |  |  |  |  |  |  |  | Ready |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Total Water Bill | ค่าน้ํ้ำทั้งสิ้น |  |  |  |  |  |  |  |  |  | Ready |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Total Water AOT | ค่าน้ํ้ำทั้งสิ้นจาก AOT |  |  |  |  |  |  |  |  |  | Ready |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Water Charge Variance | ส่วนต่างของค่าน้ำ |  |  |  |  |  |  |  |  |  | Ready |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Difference Ratio | สัดส่วนส่วนต่าง |  |  |  |  |  |  |  |  |  | Ready |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Water Bill Adjustment Amount | ยอดปรับปรุงค่าน้ำ |  |  |  |  |  |  |  |  |  | Ready |  | Number |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Water Monthly Adjusted Invoice Amount | ยอดปรับปรุงค่าน้ำยอดที่ต้องออกใบแจ้งหนี้ |  |  |  |  |  |  |  |  |  | Ready |  | Number |  |  |  |  |  | ยอดที่ต้องปรับปรุงทางบัญชีเพิ่มเติมในเดือนประกอบการนั้นๆ = Whichever Higher (Actual) - Whichever Higher (Estimate) |  |  |  |  |  |  |  |  |
|  | Water Monthly Adjusted Credit Amount | ยอดปรับปรุงค่าน้ำยอดที่ต้องออกใบลดหนี้ |  |  |  |  |  |  |  |  |  | Ready |  | Number |  |  |  |  |  | ยอดที่ต้องออกใบแจ้งหนี้ / ใบลดหนี้ เพิ่มเติม = Whichever Higher (Actual) - Whichever Higher (Revenue Sharing) |  |  |  |  |  |  |  |  |
|  | Invoice Owner | owner ตาม invoice |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Owner | owner ตามเรียกเก็บจริง |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |

---

## 21_Supplier Contact

| No. | SFDC Field Name (EN) | SFDC Field Name (TH) | Source Field API Name | Source Field Type | Source Field Length | VULLABLE (N=Required) | KP Table | KP Field Name | KP Field Type | KP Field Length | VULLABLE (N=Required).1 | Progress | Confirm | Type | Required | Sample Data | Description | Status | User/KP Feedback | Remark | Help Text | Track History | External ID | Track History.1 | Encrypted | Page Layout | Length | Source Field API Name.1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Information |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 1 | Suppplier Name |  |  |  |  |  | KPS_R_POS_SUPPLIER | NAME_E | VARCHAR2 | 100 | Y | Ready | Y |  |  |  |  | New |  |  |  |  |  |  |  |  |  |  |
| 2 | Contact Person |  |  |  |  |  | KPS_R_POS_SUPPLIER KPS_R_EMAIL_SUPPLIER | POS_SUPPLIER_CODE NAMES | VARCHAR2 VARCHAR2 | 3 60 | N N | Ready | Y |  |  |  |  | New |  |  |  |  |  |  |  |  |  |  |
| 3 | Mobile |  |  |  |  |  | KPS_R_POS_SUPPLIER KPS_R_EMAIL_SUPPLIER | POS_SUPPLIER_CODE MOBILE | VARCHAR2 VARCHAR2 | 3 60 | N Y | Ready | Y |  |  |  |  | New |  |  |  |  |  |  |  |  |  |  |
| 4 | E-mail |  |  |  |  |  | KPS_R_POS_SUPPLIER KPS_R_EMAIL_SUPPLIER | POS_SUPPLIER_CODE EMAIL | VARCHAR2 VARCHAR2 | 3 100 | N N | Ready | Y |  |  |  |  | New |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | New |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | New |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | New |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | New |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | New |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | New |  |  |  |  |  |  |  |  |  |  |

---

## 22_Invoice

| No. | SFDC Field Name (EN) | SFDC Field Name (TH) | Source Field API Name | Source Field Type | Source Field Length | VULLABLE (N=Required) | KP Table | KP Field Name | KP Field Type | KP Field Length | VULLABLE (N=Required).1 | Progress | Confirm | Type | Required | Sample Data | Description | Status | User/KP Feedback | Remark | Help Text | Track History | External ID | Track History.1 | Encrypted | Page Layout | Length | Source Field API Name.1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ข้อมูลผู้ประกอบการ |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 1 | Invoice Name |  |  |  |  |  | KPS_T_PREINV | PREINV_NO | VARCHAR2 | 15 | N | Ready |  |  |  | IV01/2569-00001 |  |  |  |  |  |  |  |  |  |  |  |  |
| 2 | Status |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  | Draft ACC Admin Review Returned to ACC Admin Waiting for ACC SM Approve Waiting for ACC DM Approve Submit to SAP Closed |  |  |  |  |  |  |  |  |  |  |  |  |
| 3 | Invoice Type |  |  |  |  |  | KPS_T_PREINV | PREINV_TYPE | VARCHAR2 | 3 |  | Ready |  |  |  | Reservation Fee Collateral Deposit Rental Deposit Decoration Insurance Water Insurance Electric Insurance Water Meter Installation Fee Electric Meter Installation Fee Rental Fee Monthly Water Bill Monthly Electric Bill Minimum Guarantee Revenue Sharing Revenue Sharing (Actual PG) |  |  |  |  |  |  |  |  |  |  |  |  |
| 4 | Concession |  |  |  |  |  | KPS_T_PREINV | CON_CODE | CHAR | 2 |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 5 | Contract |  |  |  |  |  | KPS_T_PREINV | CONT_NO | VARCHAR2 | 30 |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 6 | Unit No. |  |  |  |  |  | KPS_T_PREINV | SAP_UNIT_NO | VARCHAR2 | 400 |  | Ready |  |  |  | T1FW4-02 |  |  |  |  |  |  |  |  |  |  |  |  |
| 7 | Company Code |  |  |  |  |  | KPS_T_PREINV | SAP_COMP_CODE | VARCHAR2 | 4 |  | Ready |  |  |  | 0901097 |  |  |  |  |  |  |  |  |  |  |  |  |
| 8 | Company Name |  |  |  |  |  | KPS_T_PREINV | CON_LNAME | VARCHAR2 | 100 |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 9 | Brand Code |  |  |  |  |  | KPS_T_PREINV | SHPBND_CODE | VARCHAR2 | 4 |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 10 | Shop Brand |  |  |  |  |  | KPS_T_PREINV | SHPBND_NAME_E | VARCHAR2 | 60 |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 11 | Opportunity |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Sync Data from SAP |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 46 | Invoice No. |  |  |  |  |  | KPS_T_PREINV | INVOICE_NO | VARCHAR2 | 30 | Y | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 47 | Reference No. |  |  |  |  |  | KPS_T_PREINV | REF_DOC_NO | VARCHAR2 | 30 | Y | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 48 | Issue Date |  |  |  |  |  | KPS_T_PREINV | INVOICE_DATE | DATE | 7 | Y | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 49 | Document Link |  |  |  |  |  | KPS_T_PREINV | SAP_DOC_NO | VARCHAR2 | 20 | Y | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| จำนวนเงิน |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 12 | Monthly/Year |  |  |  |  |  | KPS_T_PREINV | ACCPERIOD_CODE/PROCPERIOD_CODE | VARCHAR2/VARCHAR2 | 2026-10-10 00:00:00 |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 13 | Monthly Rental Fee |  |  |  |  |  | KPS_T_PREINV_RENTAL | RENTAL_AMT | NUMBER | 16,2 |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 14 | Minimum Guarantee |  |  |  |  |  | KPS_T_PREINV_RENTAL | MIN_MONTH_RATE | NUMBER | 16,2 |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 15 | %Revenue Sharing |  |  |  |  |  | KPS_T_PREINV_RENTAL | RATE_PER_MONTH | NUMBER | 16,10 |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 16 | Revenue Sharing |  |  |  |  |  | KPS_T_PREINV_RENTAL | RENTAL_PER_AMT | NUMBER | 16,2 |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 17 | Amount |  |  |  |  |  | KPS_T_PREINV | TOTAL_AMT | NUMBER | 22 | Y | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 18 | VAT Amount (Auto Cal.) |  |  |  |  |  | KPS_T_PREINV | VAT_AMT | NUMBER | 22 | Y | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 19 | Total (Auto Cal.) |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 20 | Doc Date |  |  |  |  |  | KPS_T_PREINV | PREINV_DATE | DATE |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 21 | Due Date |  |  |  |  |  | KPS_T_PREINV | DUE_DATE | DATE |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 22 | Property and Land Tax |  |  |  |  |  | KPS_T_PREINV_RENTAL | PROPERTYTAX_AMT | NUMBER | 10,2 |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 23 | Remark |  |  |  |  |  | KPS_T_PREINV | REMARK | VARCHAR2 | 400 |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 24 | Total (excl. VAT) |  |  |  |  |  | KPS_T_PREINV_RENTAL | TOTAL_AMT | NUMBER | 10,2 |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 25 | Assignment |  |  |  |  |  | KPS_T_PREINV | SAP_UNIT_NO | VARCHAR2 | 400 |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 26 | Service Fee |  |  |  |  |  | KPS_T_PREINV_RENTAL | SERVICEFEE_AMT | NUMBER | 16,2 |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 27 | Grand Total (excl. VAT) |  |  |  |  |  | KPS_T_PREINV | TOTAL_AMT | NUMBER | 22 | Y | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 28 | Value Added Tax (VAT) |  |  |  |  |  | KPS_T_PREINV | VAT_RATE | NUMBER | 22 | Y | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 29 | Total (VAT) |  |  |  |  |  | KPS_T_PREINV | VAT_AMT | NUMBER | 22 | Y | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 30 | Grand Total (VAT) |  |  |  |  |  | KPS_T_PREINV | GRAND_TOTAL_AMT | NUMBER | 6,2 |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 31 | Withholding Tax (W/T) |  |  |  |  |  | KPS_T_PREINV_REVGUA | WT_RATE | NUMBER | 22 | Y | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 32 | Withholding Tax Amount (Auto Cal.) |  |  |  |  |  | KPS_T_PREINV_REVGUA | WT_AMT | NUMBER | 22 | Y | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 33 | Net Payment |  |  |  |  |  | KPS_T_PREINV | NETTOTAL_AMT | NUMBER | 16,2 |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 34 | Net Total (Auto Cal.) |  |  |  |  |  | KPS_T_PREINV | NETTOTAL_AMT | NUMBER | 16,2 |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 35 | W/O VAT Collateral Deposit |  |  |  |  |  | KPS_T_PREINV_DETAIL | CHARGE_NONE_VATAMT (CHARGE = 'REV001') | NUMBER | 22 | Y | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 36 | VAT Collateral Deposit |  |  |  |  |  | KPS_T_PREINV_DETAIL | CHARGE_VATAMT (CHARGE = 'REV001') | NUMBER | 22 | Y | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 37 | Collateral Deposit |  |  |  |  |  | KPS_T_PREINV_REVGUA | MIN_GUA_AMT | NUMBER | 22 | Y | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 38 | W/O VAT Building Usage Fee Deposit |  |  |  |  |  | KPS_T_PREINV_DETAIL | CHARGE_NONE_VATAMT (CHARGE_CODE='0006') | NUMBER | 22 | Y | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 39 | VAT Building Usage Fee Deposit |  |  |  |  |  | KPS_T_PREINV_DETAIL | CHARGE_VATAMT (CHARGE_CODE='0006') | NUMBER | 22 | Y | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 40 | Building Usage Fee Deposit |  |  |  |  |  | KPS_T_PREINV_DETAIL | TOTAL_CHARGE_AMT (CHARGE_CODE='0006') | NUMBER | 22 | Y | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 41 | Rental Deposit |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 42 | Property Tax (One-Time) |  |  |  |  |  | KPS_T_PREINV_DETAIL | CHARGE_CODE (CHARGE_CODE='0006') | VARCHAR2 | 5 | N | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 43 | W/O VAT One-Time Payment |  |  |  |  |  | KPS_T_PREINV_DETAIL | CHARGE_NONE_VATAMT | NUMBER | 22 |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 44 | VAT One-Time Payment |  |  |  |  |  | KPS_T_PREINV_DETAIL | CHARGE_VATAMT | NUMBER | 22 |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 45 | One-Time Payment |  |  |  |  |  | KPS_T_PREINV_DETAIL | TOTAL_CHARGE_AMT | NUMBER | 22 |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 46 | Start Date |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 47 | End Date |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 48 | Sales Amount |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| ค่าไฟ |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Contract |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Meter Usage |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Meter No. | รหัสมิเตอร์ |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Unit No. |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Meter Owner |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Shop Brand |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Last Meter Reading | หน่วยมิเตอร์ครั้งก่อนหน้า |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Current Meter Reading | หน่วยมิเตอร์ปัจจุบัน |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Unit Usage | หน่วยที่ใช้ |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Charge |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Service Meter |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | FT |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Service Charge |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Electricity Exp. |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Additional Electricity Charge (Average) | ค่าไฟส่วนเพิ่ม (หารเฉลี่ย) (บาท) |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Total (excl. VAT) |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Vat >> Invoice at Contract |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Net Total >> Invoice at Contract |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Sum เหลือ Record เดียว |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| ค่าน้ำ |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | External Id |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Contract |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Meter Usage |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | ประเภท |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Company |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Rec.Meter AOT  (by item) |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | เปิดร้าน |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Unit No. |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Shop name |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Meter No. | รหัสมิเตอร์ |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | ขนาด นิ้ว |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Last Meter Reading | หน่วยมิเตอร์ครั้งก่อนหน้า |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Current Meter Reading | หน่วยมิเตอร์ปัจจุบัน |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Unit Usage | หน่วยที่ใช้ |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | ค่าน้ำประปา (17.55 บาท) |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  ค่าบำบัด  (6 บาท)  |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | ค่าบำรุงรักษามาตร |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Total (excl. VAT) |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  ค่าเฉลี่ย ส่วนกลาง  |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Net Total (excl. VAT) |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Vat >> Invoice at Contract |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Net Total >> Invoice at Contract |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Revenue Sharing |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Tenant / Sub Tenant |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Shop Name |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Unit No. |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Shop Type |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | ขนาดพื้นที่ตามสัญญา |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | ยอดขาย |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | % Rev. Sharing |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | ส่วนแบ่งรายได้ ตาม % ยอดขาย |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Min. Guarartee |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Whichever Higher |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | % to Sale |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | ยอดเรียกเก็บเพิ่มเติมแล้ว |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | VAT Amount |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Total |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Withholding Tax Amount |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Net Total |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Estimate PG |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | ยอดขาย |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | % Rev. Sharing |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | ส่วนแบ่งรายได้ ตาม % ยอดขาย |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Min. Guarantee ตามสัญญาเดิม |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Min. Guarantee ส่วนเพื่ม |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Min. Guarantee 1-31ม.ค. |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Whichever Higher 1-31ม.ค. |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | % to Sales |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | ส่วนแบ่งรายได้ รอเรียกเก็บเพิ่ม |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | VAT Amount |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Total |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Withholding Tax Amount |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Net Total |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| Actual PG |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | ยอดขาย |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | % Rev. Sharing |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | ส่วนแบ่งรายได้ ตาม % ยอดขาย |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Min. Guarantee ตามสัญญาเดิม |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Min. Guarantee ส่วนเพื่ม |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Min. Guarantee ส่วนลด 20% |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Min. Guarantee 1-31ม.ค. |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Min. Gua. ต่อ ตรม./เดือน |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Whichever Higher 1-31ม.ค. |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | % to Sales |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Per Pax |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | ส่วนแบ่งรายได้ ปรับปรุงเพิ่มเติม |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | ส่วนแบ่งรายได้ รับรู้เพิ่มเติม |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| ค่าเช่า |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Customer Code SAP |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | บริษัท |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | หมายเลขพื้นที่ (Unit No.) |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | ชื่อร้านค้า |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Assignment |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | ประเภทธุรกิจ |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | หมายเหตุ |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | วันที่ทอท. อนุมัติแบบ |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | วันที่ส่งมอบพื้นที่ |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | ขนาดพื้นที่ตามสัญญา(ตรม.) |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | ค่าเช่าต่อเดือน |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | ค่าภาษีโรงเรือน และที่ดิน (12.5 % ของค่าเช่า) |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | ยอดรวม (ไม่มี VAT) |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | ค่าธรรมเนียมการใช้บริการ (15 % ของค่าเช่า) |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | ยอดรวมทั้งสิ้น (ไม่รวม VAT) |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | ภาษีมูลค่าเพิ่ม VAT 7% |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | ยอดรวม (มี VAT) |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | ยอดรวมทั้งสิ้น (รวม VAT) |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | ภาษีหัก ณ ที่จ่าย (W/T) |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | ยอดชำระสุทธิ |  |  |  |  |  |  |  |  |  |  | Ready |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |

---

## 23_Promotion

| No. | SFDC Field Name (EN) | SFDC Field Name (TH) | Source Field API Name | Source Field Type | Source Field Length | VULLABLE (N=Required) | KP Table | KP Field Name | KP Field Type | KP Field Length | VULLABLE (N=Required).1 | Progress | Confirm | Type | Required | Sample Data | Description | Status | User/KP Feedback | Remark | Help Text | Track History | External ID | Track History.1 | Encrypted | Page Layout | Length | Source Field API Name.1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Information |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 1 | Promo Code |  | PRO_CODE | VARCHAR2 | 10.0 | N | KPS_R_PROMOTION | PRO_CODE | VARCHAR2 | 10 | N | Ready | Y | Yes |  |  | Individual Concession -> (CON Abbreviation)(3) + (Running No.)(4) SVB0009 DMK0007 HKT0007  2+ Concession -> "AXX" + (Running No.)(4) AXX0001 | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 2 | Promo Description |  | PRO_DESC | VARCHAR2 | 200.0 | Y | KPS_R_PROMOTION | PRO_DESC | VARCHAR2 | 200 | Y | Ready | Y | Yes |  | Privileges for Bangkok International Flim Festival Participants |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 3 | Promo Start Date |  | PRO_SDATE | VARCHAR2 | 19.0 | Y | KPS_R_PROMOTION | PRO_SDATE | VARCHAR2 | 19 | Y | Ready | Y | Yes |  | 23/09/2010 |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 4 | Promo End Date |  | PRO_EDATE | VARCHAR2 | 19.0 | Y | KPS_R_PROMOTION | PRO_EDATE | VARCHAR2 | 19 | Y | Ready | Y | Yes |  | 23/09/2015 |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 5 | Promo Eligibility |  |  |  |  |  | KPS_R_PROMOTION | PROOWNER_CODE | VARCHAR2 | 30 |  | Ready | Y | Yes |  | - SVB - DMK - HKT |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 6 | Promo Type |  | PROTYPE_CODE | VARCHAR2 | 5.0 | Y | KPS_R_PROMOTION KPS_R_PROMOTION_TYPE | PROTYPE_CODE PROTYPE_DESC | VARCHAR2 VARCHAR2 | 5 100 | N Y | Ready | Y | Yes |  | 01. การใช้คูปอง 02. การใช้บัตร รับส่วนลด/ของสมนาคุณ 03. ซื้อชุดสินค้าหรือบริการราคาพิเศษ (Combo Set) 04. ใช้ส่วนลด จากการซื้อสินค้า หรือบริการครบตามจำนวนรายการหรือจำนวนเงินที่กำหนด 05. ซื้อสินค้า หรือบริการ ครบตามจำนวนรายการหรือจำนวนเงินที่กำหนด ได้รับ...ฟรีทันที 06. ซื้อสินค้า หรือบริการที่กำหนด ได้รับส่วนลดทันที 07. แสดงใบเสร็จที่มียอดการซื้อสินค้า หรือบริการ ครบตามที่กำหนด ได้รับ Discount 08. แสดงใบเสร็จที่มียอดการซื้อสินค้า หรือบริการ ครบตามที่กำหนด ได้รับ...ฟรีในครั้งต่อไป 09. ซื้อสินค้า หรือบริการ ครบตามที่กำหนดในราคาปกติรับสะสมแต้ม ได้รับ...ฟรี 10. ซื้อสินค้า หรือบริการ ครบตามที่กำหนดในราคาปกติรับสะสมแต้ม ครบตามกำหนดได้รับได้รับส่วนลดในครั้งต่อไป 11. On Top Promotion ได้รับ...ฟรีทันที 12. On Top Promotion ได้รับส่วนลดทันที 13. รับ...ฟรี (แบบไม่มีเงื่อนไข) 14. รายการส่งเสริมการขายของผู้ประกอบการ |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 7 | Promo Category |  | PROCATG_CODE | VARCHAR2 | 5.0 | Y | KPS_R_PROMOTION KPS_R_PROMOTION_CATG | PROCATG_CODE PROCATG_DESC | VARCHAR2 VARCHAR2 | 5 100 | Y Y | Ready | Y | Yes |  | 01. Tenant Promotion 02. Co-Promotion  03. Staff Benefits 04. Flight Delay 05. Partnership Promotion |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 8 | Created Date |  |  |  |  |  | KPS_R_PROMOTION | CREATEDDATE | DATE | 7 | Y | Ready | Y | Yes |  |  |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 9 | Start Date |  | KPS_R_PRO_LAUNCH.START_DATE | DATE | 7.0 | Y | KPS_R_PRO_LAUNCH | START_DATE | DATE | 7 | Y | Ready | Y | Yes |  |  | วันที่เริ่มจำหน่าย | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 10 | End Date |  | KPS_R_PRO_LAUNCHEND_DATE | DATE | 7.0 | Y | KPS_R_PRO_LAUNCH | END_DATE | DATE | 7 | Y | Ready | Y | Yes |  |  | วันที่สิ้นสุดการจำหน่าย | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 11 | Promo Phase No. |  | . |  |  |  | KPS_R_PRO_LAUNCH | LAUNCHNO | VARCHAR2 | 10 | N | Ready | Y | Yes |  | - 1 - 2 - 3 - 4 |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 12 | Target Description |  | TARGET_DESC | VARCHAR2 | 200.0 | Y | KPS_R_PROMOTION | TARGET_DESC | VARCHAR2 | 200 | Y | Ready | Y |  |  | Burger king Booklet |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 13 | Sales Target Amount |  | TARGETAMT | NUMBER | 22.0 | Y | KPS_R_PROMOTION | TARGETAMT | NUMBER | 16,2 | Y | Ready | Y |  |  | 100,000.00 |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 14 | Per |  |  |  |  |  | KPS_R_PROMOTION | TARGETPERTYPE | VARCHAR2 | 30 | Y | Ready | Y |  |  | - Day - Month |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 15 | Budget Amount |  | BUTGETAMT | NUMBER | 22.0 | Y | KPS_R_PROMOTION | BUTGETAMT | NUMBER | 16,2 | Y | Ready | Y |  |  | 100,000.00 |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 16 | Attach Memo |  |  |  |  |  | KPS_R_PRO_LAUNCH | MEMONO | VARCHAR2 | 30 | N | Ready | Y |  |  |  |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 17 | Promotion Status |  |  |  |  |  | KPS_R_PROMOTION (Void flag : 0 = Normal , 1 = Void) | STATUS | NUMBER | 1,0 | Y | Ready | Y | Yes |  | - Active - Inactive |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 18 | Promotion Criteria |  |  |  |  |  | KPS_R_PROMOTION | OBJECTIVE | VARCHAR2 | 4000 | Y | Ready | Y |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  | Text |  |  |  |  |  |  |  |  |  |  |  |  |  |  |

---

## 24_Airline

| No. | SFDC Field Name (EN) | SFDC Field Name (TH) | Source Field API Name | Source Field Type | Source Field Length | VULLABLE (N=Required) | KP Table | KP Field Name | KP Field Type | KP Field Length | VULLABLE (N=Required).1 | Progress | Confirm | Type | Required | Sample Data | Description | Status | User/KP Feedback | Remark | Help Text | Track History | External ID | Track History.1 | Encrypted | Page Layout | Length | Source Field API Name.1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 1 | Airline Code |  | AIRLINE_CODE | VARCHAR2 | 20.0 | N | KPS_R_AIRLINE | AIRLINE_CODE | VARCHAR2 | 20 | N | Ready |  | Text(100) |  |  |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 2 | Airline Name |  | AIRLINE_NAME | VARCHAR2 | 100.0 | Y | KPS_R_AIRLINE | AIRLINE_NAME | VARCHAR2 | 100 | Y | Ready |  | Text(100) |  |  |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 3 | Airline Short Name |  | SHORTCODE | VARCHAR2 | 10.0 | Y | KPS_R_AIRLINE | SHORTCODE | VARCHAR2 | 10 | Y | Ready |  | Text(100) |  |  |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 4 | Airline Nationality |  | NATION_CODE | VARCHAR2 | 10.0 | N | KPS_R_AIRLINE | NATION_CODE | VARCHAR2 | 10 | N | Ready |  | Text(100) |  |  |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 5 | Airline Status |  |  |  |  |  | ไม่มีใน TMS |  |  |  |  | Ready |  | Picklist |  | - Active - Inactive - Expired - Suspended |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| Airline Office Address - Contract Address |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 6 | Building / Village |  | ADDRESS1 | VARCHAR2 | 100.0 | Y | KPS_R_AIRLINE | ADDRESS1 | VARCHAR2 | 100 | Y | Ready |  |  |  |  |  | Confirmed | อยากให้เพิ่มเลขประจำตัวผู้เสียภาษีสายการบิน |  |  |  |  |  |  |  |  |  |
| 7 | Address No. |  | ADDRESS2 | VARCHAR2 | 100.0 | Y | KPS_R_AIRLINE KPS_R_AIRLINE | ADDRESS1 ADDRESS2 | VARCHAR2 VARCHAR2 | 100 100 | Y Y | Ready |  |  |  | Thai Airways International Public Company Limited 333 Moo 1 |  | Confirmed | อยากให้เพิ่มระยะเวลาชำระเงิน (วัน) |  |  |  |  |  |  |  |  |  |
| 8 | Soi |  |  |  |  |  | KPS_R_AIRLINE | ADDRESS1 | VARCHAR2 | 100 | Y | Ready |  |  |  |  |  | Confirmed | อยากให้เพิ่มระยะเวลาส่ง Invoice (วัน) |  |  |  |  |  |  |  |  |  |
| 9 | Street |  |  |  |  |  | KPS_R_AIRLINE KPS_R_AIRLINE | ADDRESS1 ADDRESS2 | VARCHAR2 VARCHAR2 | 100 100 | Y Y | Ready |  |  |  |  |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 10 | Sub-District |  |  |  |  |  | KPS_R_AIRLINE KPS_R_AIRLINE | ADDRESS1 ADDRESS2 | VARCHAR2 VARCHAR2 | 100 100 | Y Y | Ready |  |  |  | Nong Prue |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 11 | District |  | CITY | VARCHAR2 | 30.0 | Y | KPS_R_AIRLINE KPS_R_AIRLINE | ADDRESS1 ADDRESS2 | VARCHAR2 VARCHAR2 | 100 100 | Y Y | Ready |  |  |  | Bangphli |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 12 | Province |  | STATE | VARCHAR2 | 30.0 | Y | KPS_R_AIRLINE | CITY | VARCHAR2 | 30 | Y | Ready |  |  |  | Samut Prakarn |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 13 | Zip Code |  | ZIPCODE | VARCHAR2 | 10.0 | Y | KPS_R_AIRLINE | ZIPCODE | VARCHAR2 | 10 | Y | Ready |  |  |  | 10540 |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 14 | Country |  | TEL | VARCHAR2 | 30.0 | Y | KPS_R_AIRLINE | COUNTRY_CODE | VARCHAR2 | 3 | Y | Ready |  |  |  | Thailand |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 15 | Tel. |  | COUNTRY_CODE | VARCHAR2 | 3.0 | Y | KPS_R_AIRLINE | TEL | VARCHAR2 | 30 | Y | Ready |  |  |  | 02-134-5300 |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| Airline Contact Person |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 16 | Name-Surname |  | CONTACT | VARCHAR2 | 20.0 | Y | KPS_R_AIRLINE | CONTACT | VARCHAR2 | 20 | Y | Ready |  |  |  |  |  | Confirmed | อยากให้เพิ่ม Airline Operations Contact |  |  |  |  |  |  |  |  |  |
| 17 | Nickname |  |  |  |  |  | ไม่มีใน TMS |  |  |  |  | Ready |  |  |  |  |  | Confirmed | อยากให้เพิ่ม Airline Finance Contact Name |  |  |  |  |  |  |  |  |  |
| 18 | Mobile No. |  |  |  |  |  | ไม่มีใน TMS |  |  |  |  | Ready |  |  |  |  |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 19 | Email Address |  |  |  |  |  | ไม่มีใน TMS |  |  |  |  | Ready |  |  |  |  |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 20 | Status |  |  |  |  |  | ไม่มีใน TMS |  |  |  |  | Ready |  |  |  | - Active - Inactive |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| Penalty |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 21 | Penalty Type |  |  |  |  |  | ไม่มีใน TMS |  |  |  |  | Ready |  |  |  | - Warning - Suspended |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 22 | Penalty Detail |  |  |  |  |  | ไม่มีใน TMS |  |  |  |  | Ready |  |  |  | ค้างชำระติดต่อกัน 72 งวด |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 23 | Start Date |  |  |  |  |  | ไม่มีใน TMS |  |  |  |  | Ready |  |  |  | 2021-01-04 00:00:00 |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 24 | End Date |  |  |  |  |  | ไม่มีใน TMS |  |  |  |  | Ready |  |  |  | 31/03/2031 |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 25 | Penalty Remark |  |  |  |  |  | ไม่มีใน TMS |  |  |  |  | Ready |  |  |  | แจ้งตักเตือน 3 ครั้ง |  | Confirmed |  |  |  |  |  |  |  |  |  |  |
| 26 | Selected Promotion |  |  |  |  |  | ไม่มีใน TMS |  |  |  |  | Ready |  |  |  | - All - Flight Delay - ... |  | Confirmed |  |  |  |  |  |  |  |  |  |  |

---

## 25_Flight Delay contract

| No. | SFDC Field Name (EN) | SFDC Field Name (TH) | Unnamed: 3 | Unnamed: 4 | Unnamed: 5 | Unnamed: 6 | KP Table | KP Field Name | KP Field Type | KP Field Length | VULLABLE (N=Required) | Progress | Confirm | Type | Required | Sample Data | Description | Status | User/KP Feedback | Remark | Help Text | Track History | External ID | Track History.1 | Encrypted | Page Layout | Length | Source Field API Name |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Record & Contract Information |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 1 | Created Date |  |  |  |  |  | <Manual Excel> |  |  |  |  | Ready |  | Date |  | 2024-01-01 | วันที่สร้าง Record ใน Salesforce | New |  |  |  |  |  |  |  |  |  |  |
| 2 | Contract Number / Agreement Code |  |  |  |  |  | <Manual Excel> |  |  |  |  | Ready |  | Text |  | BKP/PG | เลขที่สัญญา เช่น BKP/PG | New |  |  |  |  |  |  |  |  |  |  |
| 3 | Agreement Start Date |  |  |  |  |  | <Manual Excel> |  |  |  |  | Ready |  | Date |  | 2024-01-01 | วันที่เริ่มต้นสัญญา | New |  |  |  |  |  |  |  |  |  |  |
| 4 | Agreement End Date |  |  |  |  |  | <Manual Excel> |  |  |  |  | Ready |  | Date |  | 2026-12-31 | วันที่สิ้นสุดสัญญา | New |  |  |  |  |  |  |  |  |  |  |
| 5 | Agreement Effective Date |  |  |  |  |  | <Manual Excel> |  |  |  |  | Ready |  | Date |  | 2024-01-01 | วันที่สัญญามีผลบังคับใช้ | New |  |  |  |  |  |  |  |  |  |  |
| 6 | Contract Status |  |  |  |  |  | <Manual Excel> |  |  |  |  | Ready |  | Picklist |  | Active | สถานะสัญญา | New |  |  |  |  |  |  |  |  |  |  |
| Record & Contract Information |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 7 | Airline Name |  |  |  |  |  | KPS_R_AIRLINE | AIRLINE_NAME | VARCHAR2 | 100 | Y | Ready |  | Text |  | Bangkok Airways Public Company Limited | ชื่อสายการบิน | New |  |  |  |  |  |  |  |  |  |  |
| 8 | Airline Code |  |  |  |  |  | KPS_R_AIRLINE | SHORTCODE | VARCHAR2 | 10 | Y | Ready |  | Text |  | PG | รหัสสายการบิน | New |  |  |  |  |  |  |  |  |  |  |
| 9 | Airline Address |  |  |  |  |  | KPS_R_AIRLINE KPS_R_AIRLINE KPS_R_AIRLINE KPS_R_AIRLINE | ADDRESS1 ADDRESS2 CITY ZIPCODE | VARCHAR2 VARCHAR2 VARCHAR2 VARCHAR2 | 100 100 30 10 | Y Y Y Y | Ready |  | Long Text |  | 99 Moo 14 Vibhavadi Rangsit Road, Chomphon, Chatuchak, Bangkok 10900 | ที่อยู่สายการบิน | New |  |  |  |  |  |  |  |  |  |  |
| 10 | Airline Invoice Address |  |  |  |  |  | <Manual Excel> |  |  |  |  | Ready |  | Long Text |  | Bangkok Airways Public Company Limited, 99 Moo 14 Vibhavadi Rangsit Road, Bangkok 10900 | ที่อยู่ออก Invoice | New |  |  |  |  |  |  |  |  |  |  |
| 11 | Airline Billing Address |  |  |  |  |  | <Manual Excel> |  |  |  |  | Ready |  | Long Text |  | Suvarnabhumi Airport, Concourse A | ที่อยู่วางบิล | New |  |  |  |  |  |  |  |  |  |  |
| 12 | Airline Billing Process |  |  |  |  |  | <Manual Excel> |  |  |  |  | Ready |  | Long Text |  | Submit vouchers with invoice to Bangkok Airways Suvarnabhumi Office | ขั้นตอนการวางบิล | New |  |  |  |  |  |  |  |  |  |  |
| Merchant Information |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 13 | Merchant Name |  |  |  |  |  | KPS_R_SHOP | SHOP_NAME_E | VARCHAR2 | 200 | Y | Ready |  | Text |  | AIM DHRAM CO., LTD. | ชื่อร้านค้า | New |  |  |  |  |  |  |  |  |  |  |
| 14 | Merchant Address |  |  |  |  |  | KPS_R_SHOP KPS_R_SHOP KPS_R_SHOP KPS_R_SHOP KPS_R_SHOP ADR_DISTRICT KPS_R_SHOP ADR_PROVINCE KPS_R_SHOP | LOC_ADDRESS_NO LOC_SOI LOC_STREET LOC_SUB_DISTRICT LOC_DISTRICT_CODE DISTRICT_NAME_T LOC_PROV_CODE PROV_NAME_T LOC_ZIPCODE | VARCHAR2 VARCHAR2 VARCHAR2 VARCHAR2 VARCHAR2 VARCHAR2 VARCHAR2 VARCHAR2 CHAR | 50 50 50 50 3 50 2 30 5 | Y Y Y Y Y Y Y Y Y | Ready |  | Long Text |  | 60/6-10 Rong Mueang Road, Pathumwan, Bangkok 10330 | ที่อยู่ร้านค้า | New |  |  |  |  |  |  |  |  |  |  |
| 15 | Merchant Payment Information |  |  |  |  |  |  |  |  |  |  | Ready |  | Long Text |  | Siam Commercial Bank PCL, Lat Krabang Branch, A/C No. 397-2-04547-7 | ข้อมูลบัญชีรับเงิน | New |  |  |  |  |  |  |  |  |  |  |
| 16 | Merchant Terms & Conditions |  |  |  |  |  | KPS_R_SHOP KPS_R_TERMSPAYMENT | BLL_TERM_CODE TERM_DESC | VARCHAR2 VARCHAR2 | 10 100 | Y Y | Ready |  | Long Text |  | Provide meals according to voucher value and agreement terms | เงื่อนไขร้านค้า | New |  |  |  |  |  |  |  |  |  |  |
| Outlet Information |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 17 | Outlet Name |  |  |  |  |  | KPS_R_SHOP | SHOP_NAME_E | VARCHAR2 | 200 | Y | Ready |  | Text |  | Thai Street Food / Kin Japanese Restaurant / Sensib Thai Massage | ชื่อสาขา | New |  |  |  |  |  |  |  |  |  |  |
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
| 29 | Payment Term (Days) |  |  |  |  |  | KPS_R_TERMSPAYMENT | TERM_DAY | NUMBER | 22 | Y | Ready |  | Number |  | 30 | ระยะเวลาชำระเงิน | New |  |  |  |  |  |  |  |  |  |  |
| 30 | Late Payment Interest Rate |  |  |  |  |  | KPS_T_CONTRACT_REVISE | LATE_PAY_RATE | NUMBER | 22 | Y | Ready |  | Percent |  | 1.25% per month | ดอกเบี้ยกรณีจ่ายช้า | New |  |  |  |  |  |  |  |  |  |  |
| 31 | Billing Office Hours |  |  |  |  |  |  |  |  |  |  | Ready |  | Text |  | Mon–Fri 08:00–17:00 | เวลาทำการ | New |  |  |  |  |  |  |  |  |  |  |
| 32 | Tax ID (Airline) |  |  |  |  |  |  |  |  |  |  | Ready |  | Text |  | 0107556000183 | เลขผู้เสียภาษีสายการบิน | New |  |  |  |  |  |  |  |  |  |  |
| Contact Information |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 33 | Airline Operations Contact |  |  |  |  |  | KPS_R_EMAIL_SUPPLIER KPS_R_EMAIL_SUPPLIER | NAMES MOBILE | VARCHAR2 VARCHAR2 | 60 30 | N Y | Ready |  | Text |  | Supapla Kluenbanglong, Tel. 02-134-8883 | ผู้ติดต่อสายการบิน (Operation) | New |  |  |  |  |  |  |  |  |  |  |
| 34 | Airline Finance Contact |  |  |  |  |  |  |  |  |  |  | Ready |  | Text |  | Anchalee Jaitert, Tel. 02-266-8760 | ผู้ติดต่อสายการบิน (Finance) | New |  |  |  |  |  |  |  |  |  |  |
| 35 | Merchant Operations Contact |  |  |  |  |  | KPS_R_SHOP_CONT_PER KPS_R_SHOP_CONT_PER | CONT_NAME CONT_PHONE_NO | VARCHAR2 VARCHAR2 | 50 30 | N Y | Ready |  | Text |  | Prapapuss Mutthanawech, Tel. 089-921-3914 | ผู้ติดต่อร้านค้า (Operation) | New |  |  |  |  |  |  |  |  |  |  |
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
| 1 | Source | แหล่งข้อมูล |  |  |  |  | ไม่มี |  |  |  |  | Ready |  | text | Yes | KPG + AOT |  | ประกาศของคิงเพาเวอร์ และวันหยุดของ AOT ที่ไม่ตรงกับคิงเพาเวอร์เพราะมีผลต่อการนับวันในกระบวนการ shop renovation | New |  |  |  |  |  |  |
| 2 | Holiday Date | วันเดือนปี |  |  |  |  | ไม่มี |  |  |  |  | Ready |  | date | Yes | 2025-01-01 00:00:00 |  |  | New |  |  |  |  |  |  |
| 3 | Holiday name | ชื่อวันหยุด |  |  |  |  | ไม่มี |  |  |  |  | Ready |  | text | Yes | วันขึ้นปีใหม่ |  |  | New |  |  |  |  |  |  |
| 4 | Refference | หน่วยงานที่มาของวันหยุด |  |  |  |  | ไม่มี |  |  |  |  | Ready |  | text | Yes | KPG |  | KPG หรือ AOT | New |  |  |  |  |  |  |

---

## 31_Master Table Nation

| No. | SFDC Field Name (EN) | SFDC Field Name (TH) | Unnamed: 3 | Unnamed: 4 | Unnamed: 5 | Unnamed: 6 | KP Table | KP Field Name | KP Field Type | KP Field Length | VULLABLE (N=Required) | Progress | Confirm | Type | Required | Sample Data | Source Field API Name | Description | Status | User/KP Feedback | Help Text | Track History | External ID | Encrypted | Page Layout |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Nation Information |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 1 | Source | แหล่งข้อมูล |  |  |  |  | ไม่มี |  |  |  |  | Ready |  | text | Yes | External data |  | DAS รวบรวมเองจากสื่อสาธารณะ website  | New |  |  |  |  |  |  |
| 2 | Code | รหัสประเทศ |  |  |  |  | KPS_R_NATION | NATION_CODE | VARCHAR2 | 10 | N | Ready |  | text | Yes | A02 |  |  | New |  |  |  |  |  |  |
| 3 | Nation | ชื่อประเทศ |  |  |  |  | KPS_R_NATION | NATION_DESC | VARCHAR2 | 50 | Y | Ready |  | text | Yes | AFRICAN |  |  | New |  |  |  |  |  |  |
| 4 | Continent | ทวีป |  |  |  |  | ไม่มี |  |  |  |  | Ready |  | text | Yes | Africa |  |  | New |  |  |  |  |  |  |
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

