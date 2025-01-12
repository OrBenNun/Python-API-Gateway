from flask import Flask, request, jsonify
import requests
from utils.parameter_validator import validate_parameters
from utils.ai_validation import ai_validation_func
from llm_validation import validate_api_request
from utils.ai_validation import read_validation_rules
from utils.access_control import is_request_allowed
from functools import wraps
# from utils.auth.postgres_auth import validate_token_with_db
from utils.auth.validate_token import validate_token

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_limiter.errors import RateLimitExceeded
import os

app = Flask(__name__)

API_RATE_LIMIT = os.getenv("API_RATE_LIMIT", "100 per hour")

# Initialize Flask-Limiter
limiter = Limiter(
    get_remote_address,  # Use client's IP address for rate limiting
    app=app,
    default_limits=[API_RATE_LIMIT]  # Default rate limit for all routes
)

# Custom error handler for rate limiting
@app.errorhandler(RateLimitExceeded)
def handle_rate_limit_exceeded(e):
    response = {
        "error": "Rate limit exceeded",
        "message": "You have exceeded the allowed number of requests. Please wait before trying again.",
        "details": str(e.description)  # Optional, includes information about the limit
    }
    # Return a 429 Too Many Requests response
    return jsonify(response), 429

SERVICES = {
    
}

@app.before_request
def check_ip():
    client_ip = request.remote_addr
    if not is_request_allowed(client_ip):
        return jsonify(message='Access denied'), 403

# @app.route('/')
# def home():
#     return jsonify(message='API Gateway is running!')

# @app.route('/login', methods=['POST'])
# def login():
#     try:

#         try:
#             file_path = 'config/validation_rules.json'
#             validation_rules = read_validation_rules(file_path)
#             # validate_api_request('login',request.json,validation_rules)
#         except Exception as e:
#             return jsonify(message=str(e)), 400
#         return jsonify(message='Login successful'), 200
        
#     except Exception as e:
#         return jsonify(message=str(e)), 400


file_path = 'config/validation_rules.json'
validation_rules = read_validation_rules(file_path)

# Mock user token for simplicity (replace with a database or other mechanism in production)
VALID_TOKENS = {"valid_token_123"}

def authenticate(f):
    """
    Decorator to protect routes with token-based authentication.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        # if not auth_header or auth_header.split(" ")[1] not in VALID_TOKENS:
        #     return jsonify({"error": "Unauthorized access"}), 401
        # is_valid = validate_token_with_db(auth_header.split(" ")[1])
        is_valid = validate_token(auth_header.split(" ")[1])
        if not is_valid:
            return jsonify({"error": "Unauthorized access"}), 401
        return f(*args, **kwargs)
    return decorated_function

def create_route_function(endpoint, validation_rules):
    """
    Factory function to create unique route functions.
    """
    @limiter.limit(API_RATE_LIMIT)  # Apply rate limit from .env to dynamic routes
    def route_function():
        """
        Function to handle requests for dynamically generated routes.
        """
        if request.method == 'POST':
            request_data = request.get_json()
            if not request_data:
                return jsonify({"error": "Request body must be JSON"}), 400
            
            try:
                validate_api_request(endpoint, request_data, validation_rules)
            except Exception as e:
                return jsonify({"error": str(e)}), 400
            
            # Placeholder response (extend as needed)
            return jsonify({"message": f"Request to {endpoint} processed successfully."})
    # Apply authentication if required
    if validation_rules["rules"]["endpoints"][endpoint]["requires_auth"]:
        return authenticate(route_function)
    
    return route_function

# Generate routes dynamically
for endpoint, details in validation_rules["rules"]["endpoints"].items():
    route_function = create_route_function(endpoint, validation_rules)
    app.route(f'/{endpoint}', methods=['POST'], endpoint=endpoint)(route_function)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)