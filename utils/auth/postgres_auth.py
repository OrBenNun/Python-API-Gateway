import json
from sqlalchemy import create_engine, Table, MetaData, select
import requests

with open("config/auth_config.json", "r") as config_file:
    config = json.load(config_file)
    
AUTH_METHOD = config["auth_method"]

# Database setup (if applicable)
if AUTH_METHOD == "database" and config["database_type"] == "postgresql":
    DB_URL = config["database_url"]
    TABLE_NAME = config["table_name"]
    COLUMN_NAME = config["column_name"]
    engine = create_engine(DB_URL)
    
# Validate token using database
def validate_token_with_db(token):
    with engine.connect() as connection:
        metadata = MetaData()
        tokens_table = Table(TABLE_NAME, metadata, autoload_with=engine)
        query = select(tokens_table).where(tokens_table.c[COLUMN_NAME] == token)
        result = connection.execute(query).fetchone()
        return result is not None