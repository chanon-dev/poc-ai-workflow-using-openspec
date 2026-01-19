# Tasks: Add Oracle Connection Test DAG and Service

## 1. Oracle Connection Service

- [x] 1.1 Create `plugins/oracle_service.py` with connection helper class
- [x] 1.2 Implement health check method (ping database)
- [x] 1.3 Implement permission check for migration tables
- [x] 1.4 Add connection timeout handling

## 2. Test DAG Implementation

- [x] 2.1 Create `dags/test_oracle_connection_dag.py`
- [x] 2.2 Implement connection test task
- [x] 2.3 Implement table access verification task
- [x] 2.4 Implement sample query task

## 3. Verification

- [x] 3.1 Write unit tests for oracle_service
- [x] 3.2 Validate DAG syntax
- [ ] 3.3 Test with actual Oracle connection (manual)

## Dependencies

- Task 1.x must complete before Task 2.x
- Task 3.x depends on all previous tasks
