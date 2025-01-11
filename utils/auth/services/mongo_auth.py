from pymongo import MongoClient
import json

# with open("config/auth_config.json", "r") as config_file:
#     config = json.load(config_file)

# AUTH_METHOD = config["auth_method"]

# # Set up MongoDB connection (if chosen by the developer)
# if AUTH_METHOD == "mongodb" and config["database_type"] == "mongodb":
#     DB_URL = config["database_url"]
#     DB_NAME = config["database_name"]
#     COLLECTION_NAME = config["collection_name"]

#     mongo_client = MongoClient(DB_URL)
#     db = mongo_client[DB_NAME]
#     tokens_collection = db[COLLECTION_NAME]
    
# # Function to validate token using MongoDB
# def validate_token_with_mongodb(token):
#     try:
#         token_doc = tokens_collection.find_one({"token": token})
#         return token_doc is not None
#     except Exception as e:
#         # app.logger.error(f"Error validating token: {e}")
#         raise Exception("Error validating token")
#         # return False
        
        
class MongoAuth:
    def __init__(self, config):
        self.auth_method = config["auth_method"]
        if self.auth_method == "database" and config["database_type"] == "mongodb":
            self.db_url = config["database_url"]
            self.database_name = config["database_name"]
            self.collection_name = config["collection_name"]
            self.mongo_client = MongoClient(self.db_url)
            self.db = self.mongo_client[self.database_name]
            self.tokens_collection = self.db[self.collection_name]
        else:
            raise ValueError("Invalid authentication method or database type")

    def validate_token(self, token):
        try:
            token_doc = self.tokens_collection.find_one({"token": token})
            return token_doc is not None
        except Exception as e:
            # app.logger.error(f"Error validating token: {e}")
            raise Exception("Error validating token")
            # return False
        
        
# {
#     "auth_method": "database",
#     "database_type": "mongodb",
#     "database_url": "mongodb://localhost:27017",
#     "database_name": "testserver",
#     "collection_name": "auth_server"
#   }  