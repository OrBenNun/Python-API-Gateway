from .config_loader import load_validation_rule

def validate_parameters(parameters, route):
    expected_parameters = load_validation_rule(route)
    
    unexpected_parameters = [param for param in parameters if param not in expected_parameters]
    if unexpected_parameters:
        raise Exception(f"Unexpected parameters: {', '.join(unexpected_parameters)}")
        
    for param, rules in expected_parameters.items():
        if param not in parameters and rules.get('required', False):
            raise Exception(f"Parameter {param} is required")
        
        value = parameters.get(param)
        
        if 'type' in rules:
            if rules['type'] == 'string' and not isinstance(value, str):
                raise Exception(f"Parameter {param} must be a string")
            elif rules['type'] == 'integer' and not isinstance(value, int):
                raise Exception(f"Parameter {param} must be an integer")
            
        if 'max_length' in rules and len(value) > rules['max_length']:
            raise Exception(f"Parameter {param} must not exceed {rules['max_length']} characters")
        
        if 'min_length' in rules and len(value) < rules['min_length']:
            raise Exception(f"Parameter {param} must have at least {rules['min_length']} characters")

        if 'min_value' in rules and value < rules['min_value']:
            raise Exception(f"Parameter {param} must be at least {rules['min_value']}")
        
        if 'max_value' in rules and value > rules['max_value']:
            raise Exception(f"Parameter {param} must not exceed {rules['max_value']}")
        
    return True