from utils.auth.services.postgres_auth import PostgresAuth
from utils.auth.services.mongo_auth import MongoAuth
import json

with open("config/auth_config.json", "r") as config_file:
    config = json.load(config_file)
    
AUTH_METHOD = config["auth_method"]


def validate_token(token):
    if AUTH_METHOD == "database":
        if config["database_type"] == "mongodb":
            return MongoAuth(config).validate_token(token)
        if config["database_type"] == "postgresql":
            return PostgresAuth(config).validate_token(token)