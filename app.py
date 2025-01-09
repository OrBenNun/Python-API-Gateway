from flask import Flask, request, jsonify
import requests
from utils.parameter_validator import validate_parameters
from utils.ai_validation import ai_validation_func
from llm_validation import validate_api_request
from utils.ai_validation import read_validation_rules
from utils.access_control import is_request_allowed

app = Flask(__name__)

SERVICES = {
    
}

@app.before_request
def check_ip():
    client_ip = request.remote_addr
    if not is_request_allowed(client_ip):
        return jsonify(message='Access denied'), 403

@app.route('/')
def home():
    return jsonify(message='API Gateway is running!')

@app.route('/login', methods=['POST'])
def login():
    try:

        try:
            file_path = 'config/validation_rules.json'
            validation_rules = read_validation_rules(file_path)
            validate_api_request('login',request.json,validation_rules)
        except Exception as e:
            return jsonify(message=str(e)), 400
        return jsonify(message='Login successful'), 200
        
    except Exception as e:
        return jsonify(message=str(e)), 400


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)