## ADDED Requirements

### Requirement: Upsert file status record

The system SHALL upsert a `TMS_Daily_Sales_File__c` record via PATCH to the External ID endpoint, creating the record if it does not exist or updating it if it does.

#### Scenario: Create new status record (validation passed)

- **WHEN** `upsert_status(external_ref, status="New", **fields)` is called and no record exists for the given `external_ref`
- **THEN** the system SHALL PATCH to `/services/data/v66.0/sobjects/TMS_Daily_Sales_File__c/TMS_External_File_Ref__c/{external_ref}` with the status and fields
- **AND** Salesforce SHALL return HTTP 201 (created)

#### Scenario: Update existing status record

- **WHEN** `upsert_status(external_ref, status="Uploading", **fields)` is called and a record already exists
- **THEN** the system SHALL PATCH to the same endpoint
- **AND** Salesforce SHALL return HTTP 200 (updated)

#### Scenario: Upsert with validation failure status

- **WHEN** validation fails before upload
- **THEN** the system SHALL call `upsert_status(external_ref, status="Failed", TMS_Errors__c=errors)`

### Requirement: Update-only status change

The system SHALL support update-only mode (`?updateOnly=true`) to prevent accidental record creation when updating status after upload.

#### Scenario: Update status to "Uploaded" after successful upload

- **WHEN** `update_status(external_ref, status="Uploaded")` is called
- **THEN** the system SHALL PATCH to `/services/data/v66.0/sobjects/TMS_Daily_Sales_File__c/TMS_External_File_Ref__c/{external_ref}?updateOnly=true`
- **AND** the body SHALL contain `{"TMS_Status__c": "Uploaded"}`

#### Scenario: Update status to "In Progress" after failed upload (reset for retry)

- **WHEN** `update_status(external_ref, status="In Progress")` is called
- **THEN** the system SHALL PATCH with `?updateOnly=true` and body `{"TMS_Status__c": "In Progress"}`

#### Scenario: Record not found in update-only mode

- **WHEN** `update_status` is called with `updateOnly=true` and the record does not exist
- **THEN** Salesforce SHALL return HTTP 404
- **AND** the system SHALL raise an exception indicating the record was not found
