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

#Variáveis de controle do MQTT
BROKER = "test.mosquitto.org"
PORT = 1883
KEEPALIVE = 60
BIND = ""

#Variáveis de controle do banco(Mysql)
HOST = "localhost"
USER = "root"
PASSWORD = "root"
DATABASE = "ReLUZ_API"
PORT_DATABASE = 3306

# Instanciar objetos
bd_manipulator = BDManipulator(HOST, USER, PASSWORD, DATABASE, PORT_DATABASE)
mqtt_communicator = MQTTCommunicator(BROKER, PORT, KEEPALIVE, BIND)

# Conectar ao banco de dados
bd_manipulator.connect()

# Conectar ao MQTT broker
mqtt_communicator.connect()

# Inscrever-se em vários tópicos/DEBUG
topics = [("topic1", 0), ("123456789123", 1), ("dataSet", 2)]
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
    mqtt_communicator.client.loop_start()
    def handle_message(client, userdata, msg):
        mensagem = str(msg.payload)
        topico = str(msg.topic)
        qos = msg.qos
        bd_manipulator.insert_data(mensagem, topico, qos, data_hora_medicao)    
    

    # Aguardar 1 segundo antes de executar novamente
    time.sleep(1)
#A criação do banco(tabelas e etc) é feita por fora, então caso seja feita a execução do código com um banco não criado
# irá ocorrer um erro. Posteriormente será criado a automação da criação da tabela.

#A query é: "INSERT INTO Dispositivo(mensagem, topico, qos, data_hora_medicao) VALUES(%s, %s, %s, %s)"