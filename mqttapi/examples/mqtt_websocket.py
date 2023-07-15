import json
import threading
from mqttapi import MQTTCommunicator,WebSocketServer
import signal
import sys

WEBSOCKET_SERVER = "ws://localhost:8769/"

mqtt_communicator = MQTTCommunicator(host='localhost', port=1883, keepalive=60, bind_address='')

mqtt_communicator.connect()

topic_qos_tuples = [
    ('topic1', 0),
    ('topic2', 1),
    ('topic3', 2)
]
mqtt_communicator.subscribe_to_topics(topic_qos_tuples)

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

def signal_handler(signal, frame):
    print("Programa encerrado.")
    bd_manipulator.disconnect()
    mqtt_communicator.disconnect()
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

def send_message_to_websocket(topic, payload):
    if websocket and websocket.sock and websocket.sock.connected:
        message = {
            'topic': topic,
            'payload': payload
        }
        websocket.send(json.dumps(message))


while True:
    mqtt_communicator.client.loop_start()
    def handle_message(client, userdata, msg):
        payload_str = msg.payload.decode()
        send_message_to_websocket(msg.topic, payload_str)
        #Opcionalmente pode-se implementar um : time.sleep(1)
    mqtt_communicator.client.on_message = handle_message
