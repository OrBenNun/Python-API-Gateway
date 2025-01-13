import json

def validate_api_request(endpoint, data, config):
    rules = config['rules']['endpoints'].get(endpoint)
    if not rules:
        raise ValueError(f"Endpoint '{endpoint}' not found in configuration.")

    parameters = rules.get('parameters', {})
    required_params = {k for k, v in parameters.items() if v.get('required')}

    missing_params = required_params - set(data.keys())
    if missing_params:
        raise ValueError(f"Missing required parameters: {', '.join(missing_params)}")

    unknown_params = set(data.keys()) - set(parameters.keys())
    if unknown_params:
        raise ValueError(f"Unknown parameters: {', '.join(unknown_params)}")
        
    for param_name, param_value in data.items():
        rules = parameters.get(param_name)
        if rules:
            param_type = rules.get('type')
            if param_type == 'string':
                if not isinstance(param_value, str):
                    raise TypeError(f"Parameter '{param_name}' must be a string.")
                max_length = rules.get('max_length')
                if max_length is not None and len(param_value) > max_length:
                    raise ValueError(f"Parameter '{param_name}' exceeds maximum length of {max_length}.")
                min_length = rules.get('min_length')
                if min_length is not None and len(param_value) < min_length:
                    raise ValueError(f"Parameter '{param_name}' is shorter than minimum length of {min_length}.")

            elif param_type == 'integer':
                if not isinstance(param_value, int):
                    raise TypeError(f"Parameter '{param_name}' must be an integer.")
                min_value = rules.get('min_value')
                if min_value is not None and param_value < min_value:
                    raise ValueError(f"Parameter '{param_name}' is less than minimum value of {min_value}.")

config_json = {'meta': {'version': '1.0', 'description': 'API configuration file for validation rules'}, 'rules': {'endpoints': {'login': {'_description': 'Handles user login by validating credentials.', 'parameters': {'username': {'type': 'string', 'max_length': 200, 'required': True}, 'password': {'type': 'string', 'max_length': 200, 'required': True}}, 'backend': {'type': 'static', 'url': 'http://localhost:3000'}, 'path': '/auth', 'methods': ['POST'], 'requires_auth': True}, 'send_email': {'_description': 'Send email to a user.', 'parameters': {'from_user': {'type': 'string', 'max_length': 200, 'required': True}, 'to_user': {'type': 'string', 'max_length': 200, 'required': True}}, 'backend': {'type': 'static', 'url': 'http://localhost:3000'}, 'path': '/send_email', 'methods': ['POST'], 'requires_auth': False}, 'create_order': {'_description': 'Creates a new order.', 'parameters': {'order_id': {'type': 'string', 'min_length': 1, 'max_length': 50, 'required': True}, 'item': {'type': 'string', 'max_length': 100, 'required': True}, 'quantity': {'type': 'integer', 'min_value': 1, 'required': True}}, 'backend': {'type': 'static', 'url': 'http://order-service.mycompany.com'}, 'path': '/orders/new', 'methods': ['POST'], 'requires_auth': True}}}}



import json

def validate_api_request(endpoint, data, config):
    rules = config['rules']['endpoints'].get(endpoint)
    if not rules:
        raise ValueError(f"Endpoint '{endpoint}' not found in configuration.")

    parameters = rules.get('parameters', {})
    required_params = {k for k, v in parameters.items() if v.get('required')}

    missing_params = required_params - set(data.keys())
    if missing_params:
        raise ValueError(f"Missing required parameters: {', '.join(missing_params)}")

    unknown_params = set(data.keys()) - set(parameters.keys())
    if unknown_params:
        raise ValueError(f"Unknown parameters: {', '.join(unknown_params)}")
        
    for param_name, param_value in data.items():
        rules = parameters.get(param_name)
        if rules:
            param_type = rules.get('type')
            if param_type == 'string':
                if not isinstance(param_value, str):
                    raise TypeError(f"Parameter '{param_name}' must be a string.")
                max_length = rules.get('max_length')
                if max_length is not None and len(param_value) > max_length:
                    raise ValueError(f"Parameter '{param_name}' exceeds maximum length of {max_length}.")
                min_length = rules.get('min_length')
                if min_length is not None and len(param_value) < min_length:
                    raise ValueError(f"Parameter '{param_name}' is shorter than minimum length of {min_length}.")

            elif param_type == 'integer':
                if not isinstance(param_value, int):
                    raise TypeError(f"Parameter '{param_name}' must be an integer.")
                min_value = rules.get('min_value')
                if min_value is not None and param_value < min_value:
                    raise ValueError(f"Parameter '{param_name}' is less than minimum value of {min_value}.")
