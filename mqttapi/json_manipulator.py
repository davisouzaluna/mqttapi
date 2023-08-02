import json
import os
import mqtt_communicator
import datetime

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

    #Coloque essa função dentro do callback
    def createMQTTjson(self,mqtt_message):
        topic = mqtt_message.topic
        payload = mqtt_message.payload.decode("utf-8")
        timestamp = datetime.datetime.now(datetime.timezone.utc)
        
        json_data = {
        "topic": topic,
        "payload": payload,
        "timestamp": timestamp
        }
        
        json_string = json.dumps(json_data)
        return json_string