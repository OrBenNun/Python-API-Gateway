# Python-API-Gateway

An API Gateway app for Backend development.

For postgresql auth use the following fields:
auth_method=database, database_type=postgresql, database_url, table_name, column_name

For mongodb auth use the following fields:
auth_method=database, database_type=mongodb, database_url, database_name, collection_name

For your own auth server use the following fields:
  "auth_method": "api",
  "auth_api_url": "auth_server_path"

For file auth use the following fields:
  "auth_method": "file",
    "tokens": [
      "valid_token_123",
    ]

You should add your .env file with the following params:
  GEMINI_API_KEY = Your Gemini API key
  API_RATE_LIMIT = Rate limit by Flask rate limit, for exmaple: 10 per minute

Dynamic routing:
  If you want to use urls for your microservices you can use static option on the config file for example:
        "backend": {
          "type": "static",
          "url": "http://localhost:3000"
        },
        "path": "/auth/login",
        "methods": ["POST"],
  
  If you want to use service discovery - Consul:
    Run consul docker command:
      docker run -d --name=consul -e CONSUL_BIND_INTERFACE=eth0 -p 8500:8500 hashicorp/consul:1.14
    Register your microservices to consul
    Adjust the config file option to "discovery" for example:
      "backend": {
          "type": "discovery",
          "service_name": "send-email"  
        },
        "path": "/send_email",
        "methods": ["POST"],
        "requires_auth": false

