from flask import Flask, request, jsonify
import requests
from utils.parameter_validator import validate_parameters
from utils.ai_validation import ai_validate_parameters

app = Flask(__name__)

SERVICES = {
    
}

@app.route('/')
def home():
    return jsonify(message='API Gateway is running!')

@app.route('/login', methods=['POST'])
def login():
    try:
        # validate_parameters(request.json, 'login')
        ai_validate_parameters()
        return jsonify(message='Login successful'), 200
        
    except Exception as e:
        return jsonify(message=str(e)), 400


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)