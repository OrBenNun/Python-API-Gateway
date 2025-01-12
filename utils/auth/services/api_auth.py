import json
import requests

class AuthServerAuth:
    def __init__(self, config):
        self.auth_method = config["auth_method"]
        if self.auth_method == "api":
            self.auth_api_url = config["auth_api_url"]
        else:
            raise ValueError("Invalid authentication method or database type")

    def validate_token(self, token):
        try:
            # Send a POST request to the external API with the token
            response = requests.post(
                self.auth_api_url,
                json={"token": token},
                timeout=5  # Set a timeout to avoid long waits
            )
            # Check if the response indicates the token is valid
            if response.status_code == 200:
                data = response.json()
                return data.get("is_valid", False)  # Assuming the API returns {"is_valid": true/false}
            return False
        except requests.RequestException as e:
            raise Exception("Error validating token")
            # return False