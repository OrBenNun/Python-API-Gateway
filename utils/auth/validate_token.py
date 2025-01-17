from utils.auth.services.postgres_auth import PostgresAuth
from utils.auth.services.mongo_auth import MongoAuth
from utils.auth.services.api_auth import AuthServerAuth
from utils.auth.services.file_auth import FileAuth
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
    elif AUTH_METHOD == "api":
        return AuthServerAuth(config).validate_token(token)
    elif AUTH_METHOD == "file":
        return FileAuth(config).validate_token(token)