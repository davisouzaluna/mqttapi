import paho.mqtt.client as mqtt
import time
import json
import pymysql
import datetime
import os
import signal
import sys

from bd_manipulator import BDManipulator
from json_manipulator import JSONManipulator
from mqtt_communicator import MQTTCommunicator

# Instanciar objetos
bd_manipulator = BDManipulator("localhost", "root", "root", "ReLuZ", 3306)
json_manipulator = JSONManipulator()
mqtt_communicator = MQTTCommunicator("localhost", 1883, 60, "")

# Conectar ao banco de dados
bd_manipulator.connect()

# Conectar ao MQTT broker
mqtt_communicator.connect()

# Inscrever-se em vários tópicos
topics = [("topic1", 0), ("topic2", 1), ("topic3", 2)]
mqtt_communicator.subscribe_to_topics(topics)

# Função de tratamento de sinal para interromper o programa corretamente
def signal_handler(signal, frame):
    print("Programa encerrado.")
    bd_manipulator.disconnect()
    mqtt_communicator.disconnect()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Loop principal
while True:
    # Executar tarefas do programa

    # Aguardar 1 segundo antes de executar novamente
    time.sleep(1)
