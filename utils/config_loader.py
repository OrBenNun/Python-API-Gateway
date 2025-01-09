import json

def load_validation_rule(route):
    try:
        with open('config/validation_rules.json', 'r') as file:
            rules = json.load(file)
            
        return rules.get(route, {})
    except FileNotFoundError:
        raise Exception('Validation rule not found')
    except json.JSONDecodeError:
        raise Exception('Invalid JSON format')