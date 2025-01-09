def validate_api_request(endpoint, data, config):
    rules = config.get('rules', {}).get('endpoints', {}).get(endpoint, {})
    if not rules:
        raise ValueError(f"Endpoint '{endpoint}' not found in configuration.")

    parameters = rules.get('parameters', {})
    required_params = {k for k, v in parameters.items() if v.get('required')}
    missing_params = required_params - set(data.keys())
    if missing_params:
        raise ValueError(f"Missing required parameters: {', '.join(missing_params)}")
    
    unknown_params = set(data.keys()) - set(parameters.keys())
    if unknown_params:
        raise ValueError(f"Unknown parameters provided: {', '.join(unknown_params)}")

    for param_name, param_value in data.items():
        rules = parameters.get(param_name)
        if not rules:
            continue  # Parameter not defined in rules, skip validation

        param_type = rules.get('type')
        if param_type == 'string':
            if not isinstance(param_value, str):
                raise TypeError(f"Parameter '{param_name}' must be a string.")
            max_length = rules.get('max_length')
            if max_length and len(param_value) > max_length:
                raise ValueError(f"Parameter '{param_name}' exceeds maximum length of {max_length}.")
            min_length = rules.get('min_length')
            if min_length and len(param_value) < min_length:
                raise ValueError(f"Parameter '{param_name}' is shorter than minimum length of {min_length}.")

        elif param_type == 'integer':
            if not isinstance(param_value, int):
                raise TypeError(f"Parameter '{param_name}' must be an integer.")
            min_value = rules.get('min_value')
            if min_value and param_value < min_value:
                raise ValueError(f"Parameter '{param_name}' is less than minimum value of {min_value}.")