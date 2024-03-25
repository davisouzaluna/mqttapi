import json
import os
import datetime

class JSONManipulator:
    def __init__(self):
        self.cache = {}

    def create_json_file(self, data, filename):
        if not os.path.exists(filename):
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

    # Função para criar o JSON a partir da mensagem MQTT
    def createMQTTjson(self, mqtt_message, filename):
        topic = mqtt_message.topic
        payload = mqtt_message.payload.decode("utf-8")
        timestamp = datetime.datetime.now(datetime.timezone.utc)

        json_data = {
            "topic": str(topic),
            "payload": str(payload),
            "timestamp": str(timestamp)
        }

        # Verificar se o arquivo já está sendo usado por outro programa
        if filename in self.cache:
            # Se o tamanho do cache ultrapassar 4 MB, limpar o cache
            if len(json.dumps(self.cache[filename])) > 4 * 1024 * 1024:# Esse tamanho eu escolhi arbitrariamente
                self.cache.pop(filename)
            else:
                # Adicionar dados ao cache
                if filename not in self.cache:
                    self.cache[filename] = []
                self.cache[filename].append(json_data)
                return

        # Se o arquivo não está sendo usado por outro programa ou o cache foi limpo, escrever diretamente no arquivo
        with open(filename, 'a') as file:
            json.dump(json_data, file)
            file.write('\n')
