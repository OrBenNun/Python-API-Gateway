import json
from sqlalchemy import create_engine, Table, MetaData, select

# with open("config/auth_config.json", "r") as config_file:
#     config = json.load(config_file)
    
# AUTH_METHOD = config["auth_method"]

# # Database setup (if applicable)
# if AUTH_METHOD == "database" and config["database_type"] == "postgresql":
#     DB_URL = config["database_url"]
#     TABLE_NAME = config["table_name"]
#     COLUMN_NAME = config["column_name"]
#     engine = create_engine(DB_URL)

class PostgresAuth:
    def __init__(self, config):
        self.auth_method = config["auth_method"]
        if self.auth_method == "database" and config["database_type"] == "postgresql":
            self.db_url = config["database_url"]
            self.table_name = config["table_name"]
            self.column_name = config["column_name"]
            self.engine = create_engine(self.db_url)
        else:
            raise ValueError("Invalid authentication method or database type")

    def validate_token(self, token):
        # Implement token validation logic using self.engine, self.table_name, and self.column_name
        with self.engine.connect() as connection:
            metadata = MetaData()
            tokens_table = Table(self.table_name, metadata, autoload_with=self.engine)
            query = select(tokens_table).where(tokens_table.c[self.column_name] == token)
            result = connection.execute(query).fetchone()
            return result is not None
    
# # Validate token using database
# def validate_token_with_db(token):
#     with engine.connect() as connection:
#         metadata = MetaData()
#         tokens_table = Table(TABLE_NAME, metadata, autoload_with=engine)
#         query = select(tokens_table).where(tokens_table.c[COLUMN_NAME] == token)
#         result = connection.execute(query).fetchone()
#         return result is not None


# {
#     "auth_method": "database",
#     "database_type": "postgresql",
#     "database_url": "postgresql://postgres:postgres@localhost:5432/auth_server",
#     "table_name": "auth_tokens",
#     "column_name": "token"
#   }  