import json
import time
import paho.mqtt.client as mqtt
import mqtt_communicator as m
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

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response


def event_generator():
    while True:
        if mqtt_messages:
            data = mqtt_messages.pop(0)
            yield f"data: {data}\n\n"
        else:
            pass

@app.route('/')
def events():
    return Response(event_generator(), content_type='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True)
