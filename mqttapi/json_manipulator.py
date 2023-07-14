import json
import os

class JSONManipulator:
    def __init__(self):
        pass

    def create_json_file(self, data, filename):
        with open(filename, 'w') as file:
            json.dump(data, file)

    def update_json_file(self, data, filename):
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                existing_data = json.load(file)
            existing_data.update(data)
        else:
            existing_data = data
        with open(filename, 'w') as file:
            json.dump(existing_data, file)
