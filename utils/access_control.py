import json

def load_access_list(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

access_list = load_access_list('config/access_list.json')

def is_request_allowed(ip):
    if ip in access_list['deny']:
        print('Access denied for IP:', ip)
        return False
    if ip in access_list['allow']:
        print('Access granted for IP:', ip)
        return True
    return False