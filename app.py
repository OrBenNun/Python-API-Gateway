from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

SERVICES = {
    
}

@app.route('/')
def home():
    return jsonify(message='API Gateway is running!')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)