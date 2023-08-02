import json
import time
import paho.mqtt.client as mqtt
from flask import Flask, Response

app = Flask(__name__)

# Configurações MQTT
MQTT_BROKER_HOST = 'broker.hivemq.com'
MQTT_BROKER_PORT = 1883
MQTT_TOPIC = 'dataSets'

# Armazenamento das mensagens MQTT
mqtt_messages = []

# Função para tratar mensagens MQTT recebidas
def on_message(client, userdata, message):
    payload = message.payload.decode('utf-8')
    mqtt_messages.append(payload)

# Configurar cliente MQTT
mqtt_client = mqtt.Client()
mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT, keepalive=60)
mqtt_client.subscribe(MQTT_TOPIC)
mqtt_client.loop_start()

def event_generator():
    while True:
        if mqtt_messages:
            data = mqtt_messages.pop(0)
            yield f"data: {data}\n\n"
        else:
            pass

@app.route('/events')
def events():
    return Response(event_generator(), content_type='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True)
