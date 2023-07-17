import datetime
from mqttapi import BDManipulator,MQTTCommunicator
import signal
import sys

mqtt_communicator = MQTTCommunicator(host='localhost', port=1883, keepalive=60, bind_address='')
bd_manipulator = BDManipulator(host='localhost', user='seu_usuario', password='sua_senha', database='seu_banco')

mqtt_communicator.connect()
bd_manipulator.connect()

topic_qos_tuples = [
    ('topic1', 0),
    ('topic2', 1),
    ('topic3', 2)
]
mqtt_communicator.subscribe_to_topics(topic_qos_tuples)

def signal_handler(signal, frame):
    print("Programa encerrado.")
    bd_manipulator.disconnect()
    mqtt_communicator.disconnect()
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

while True:
    mqtt_communicator.client.loop_start()
    def handle_message(client, userdata, msg):
        mensagem = str(msg.payload)
        topico = str(msg.topic)
        qos = msg.qos
        data_hora_medicao= datetime.datetime.now(datetime.timezone.utc)
        bd_manipulator.insert_data(mensagem, topico, qos, data_hora_medicao)

