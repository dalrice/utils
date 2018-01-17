# get all table in all database

SELECT table_schema, table_name
FROM INFORMATION_SCHEMA.tables
ORDER BY table_schema, table_name ;
