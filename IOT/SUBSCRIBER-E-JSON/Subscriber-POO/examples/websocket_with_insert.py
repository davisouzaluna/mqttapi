import paho.mqtt.client as mqtt
import time
import json
import pymysql
import datetime
import os
import signal
import sys
import re
import websocket
import threading

from bd_manipulator import BDManipulator
from json_manipulator import JSONManipulator
from mqtt_communicator import MQTTCommunicator

# Variáveis de controle do MQTT
BROKER = "test.mosquitto.org"
PORT = 1883
KEEPALIVE = 60
BIND = ""

# Instanciar objetos
bd_manipulator = BDManipulator("localhost", "root", "root", "thingsafe", 3306)
json_manipulator = JSONManipulator()
mqtt_communicator = MQTTCommunicator(BROKER, PORT, KEEPALIVE, BIND)


# Variáveis do WebSocket
WEBSOCKET_SERVER = "ws://localhost:8769/"

# Conectar ao banco de dados
bd_manipulator.connect()

# Conectar ao MQTT broker
mqtt_communicator.connect()

# Inscrever-se em vários tópicos/DEBUG
topics = [("topic1", 0), ("123456789123", 1), ("dataSet", 0)]
mqtt_communicator.subscribe_to_topics(topics)


# Função de tratamento de sinal para interromper o programa corretamente
def signal_handler(signal, frame):
    print("Programa encerrado.")
    bd_manipulator.disconnect()
    mqtt_communicator.disconnect()
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)


# Função para conectar ao WebSocket
def connect_to_websocket():
    global websocket
    websocket = websocket.WebSocketApp(WEBSOCKET_SERVER, on_message=on_message)
    websocket.run_forever()


# Função para receber mensagens do WebSocket
def on_message(ws, message):
    data = json.loads(message)
    topic = data['topic']
    payload = data['payload']
    # mqtt_client.publish(topic, payload)


# Iniciar a thread do WebSocket
websocket_thread = threading.Thread(target=connect_to_websocket)
websocket_thread.daemon = True
websocket_thread.start()


# Função para enviar mensagens MQTT para o cliente WebSocket
def send_message_to_websocket(topic, payload):
    if websocket and websocket.sock and websocket.sock.connected:
        message = {
            'topic': topic,
            'payload': payload
        }
        websocket.send(json.dumps(message))


# Loop principal
while True:
    mqtt_communicator.client.loop_start()

    # Sobrecarga de método
    def handle_message(client, userdata, v):
        
        payload_str = v.payload.decode()
        
        
        #Na mensagem comentada o formato da mensagem era: message = "{} ; {}".format(mac_address, value) por isso que há o split para dividir
        #payload_str = v.payload.decode()
        #mensagem = str(v.payload)
        #mac = str(mensagem.split(" ;")[0].strip().replace("'", ""))
        #value = int(mensagem.split(" ;")[1].strip().replace("'", ""))

        print("=============================")
        print("Topic: " + str(v.topic))
        print("Payload: " + str(v.payload))
        print("Mac: " + str(mac))
        print("value: " + str(value))
        print(
            "Hora: " + datetime.datetime.now(datetime.timezone.utc).strftime("%H:%M:%S")
        )

        mensagem = str(v.payload)
        topico = str(v.topic)
        qos = v.qos
        data_hora_medicao = datetime.datetime.now(datetime.timezone.utc)
        bd_manipulator.insert_data(mensagem, topico, qos, data_hora_medicao)
       
        send_message_to_websocket(v.topic, payload_str)

    # Aguardar 1 segundo antes de executar novamente(OPCIONAL)
    time.sleep(1)
    
    # execução da sobrecarga de método
    mqtt_communicator.client.on_message = handle_message
