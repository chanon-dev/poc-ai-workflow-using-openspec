# Tasks: Add Oracle Connection Test DAG and Service

## 1. Oracle Connection Service

- [x] 1.1 Create `plugins/oracle_service.py` with connection helper class
- [x] 1.2 Implement health check method (ping database)
- [x] 1.3 Implement permission check for migration tables
- [x] 1.4 Add connection timeout handling

## 2. Service Interface Methods (NEW)

- [ ] 2.1 Add `get_pandas_df(query, params)` method
- [ ] 2.2 Add `get_table_columns(table_name)` method
- [ ] 2.3 Add `get_record_count(table_name, where_clause)` method

## 3. Test DAG Implementation

- [x] 3.1 Create `dags/test_oracle_connection_dag.py`
- [x] 3.2 Implement connection test task
- [x] 3.3 Implement table access verification task
- [x] 3.4 Implement sample query task

## 4. Refactor OracleExtractor (NEW)

- [ ] 4.1 Update `oracle_extractor.py` to use `OracleService` instead of `OracleHook`
- [ ] 4.2 Ensure dependency injection pattern for testing

## 5. Verification

- [x] 5.1 Write unit tests for oracle_service
- [x] 5.2 Validate DAG syntax
- [ ] 5.3 Test with actual Oracle connection (manual)
- [ ] 5.4 Add tests for new Service Interface Methods
- [ ] 5.5 Update tests for refactored OracleExtractor

## Dependencies

- Task 1.x must complete before Task 2.x and 3.x
- Task 4.x depends on Task 2.x (need service methods first)
- Task 5.x depends on all previous tasks
