import json

def read_config(path):
    with open(path, 'r') as file:
        config = json.load(file)
    return config