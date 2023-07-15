import json
import threading
from mqttapi import MQTTCommunicator,WebSocketServer
import signal
import sys

#Atributos do websocket
HOST_WEBSOCKET= "localhost"
PORT_WEBSOCKET="8769"

mqtt_communicator = MQTTCommunicator(host='localhost', port=1883, keepalive=60, bind_address='')
websocket_server = WebSocketServer(HOST_WEBSOCKET, PORT_WEBSOCKET)

mqtt_communicator.connect()

topic_qos_tuples = [
    ('topic1', 0),
    ('topic2', 1),
    ('topic3', 2)
]
mqtt_communicator.subscribe_to_topics(topic_qos_tuples)

#Se conecta ao websocket(como cliente)
websocket_server.connect_to_websocket()

# Iniciar a thread do WebSocket
websocket_server.start_websocket_thread()

def signal_handler(signal, frame):
    print("Programa encerrado.")
    mqtt_communicator.disconnect()
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)




while True:
    mqtt_communicator.client.loop_start()
    def handle_message(client, userdata, msg):
        payload_str = msg.payload.decode()
        websocket_server.send_message_to_websocket(msg.topic, payload_str)
        #Opcionalmente pode-se implementar um : time.sleep(1)
    mqtt_communicator.client.on_message = handle_message
