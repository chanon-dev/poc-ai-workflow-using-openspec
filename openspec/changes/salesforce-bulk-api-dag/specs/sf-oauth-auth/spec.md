## ADDED Requirements

### Requirement: Authenticate via OAuth 2.0 Client Credentials

The system SHALL authenticate to Salesforce using the OAuth 2.0 Client Credentials flow, obtaining an `access_token` and `instance_url` for subsequent API calls.

#### Scenario: Successful authentication

- **WHEN** `get_salesforce_token(conn_id)` is called with a valid Airflow Connection ID
- **THEN** the system SHALL POST to `{host}/services/oauth2/token` with `grant_type=client_credentials`, `client_id`, and `client_secret` from the connection
- **AND** return a dict containing `access_token`, `instance_url`, and `token_type`

#### Scenario: Authentication failure — invalid credentials

- **WHEN** the Salesforce token endpoint returns HTTP 401 (`invalid_client`)
- **THEN** the system SHALL raise an exception with the error description from the response body

#### Scenario: Authentication failure — bad request

- **WHEN** the Salesforce token endpoint returns HTTP 400 (`invalid_grant`)
- **THEN** the system SHALL raise an exception with the error description from the response body

### Requirement: Read credentials from Airflow Connection

The system SHALL read `client_id`, `client_secret`, and `host` (base URL) from an Airflow Connection, not from hardcoded values or environment variables.

#### Scenario: Connection provides all required fields

- **WHEN** an Airflow Connection exists with `conn_id="salesforce_api"` containing `login` (client_id), `password` (client_secret), and `host` (base URL)
- **THEN** the system SHALL use these values for the OAuth request

#### Scenario: Connection missing required fields

- **WHEN** the Airflow Connection is missing `login`, `password`, or `host`
- **THEN** the system SHALL raise a descriptive error indicating which field is missing
