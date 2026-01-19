-- Example SQL file in include/sql/
-- Use this for complex queries instead of embedding them in Python strings.
-- Usage in DAG:
-- sql = open("include/sql/sample_query.sql").read().format(table_name="my_table")

SELECT 
    id,
    name,
    created_at
FROM {{ table_name }}
WHERE created_at >= :start_date
  AND created_at < :end_date
ORDER BY created_at;
