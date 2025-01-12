import requests

class FileAuth:
    def __init__(self, config):
        self.auth_method = config["auth_method"]
        if self.auth_method == "file":
            self.valid_tokens = set(config.get("tokens", []))
        else:
            raise ValueError("Invalid authentication method or database type")

    def validate_token(self, token):
        try:
            if token in self.valid_tokens:
                return True
            else:
                return False
        except requests.RequestException as e:
            raise Exception("Error validating token")
            # return False




# {
#   "auth_method": "file",
#   "tokens": [
#     "valid_token_123",
#     "valid_token_456",
#     "valid_token_789"
#   ]
# }
