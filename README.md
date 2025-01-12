# Python-API-Gateway

An API Gateway app for Backend development.

For postgresql auth use the following fields:
auth_method=database, database_type=postgresql, database_url, table_name, column_name

For mongodb auth use the following fields:
auth_method=database, database_type=mongodb, database_url, database_name, collection_name

For your own auth server use the following fields:
  "auth_method": "api",
  "auth_api_url": "authserverpath"