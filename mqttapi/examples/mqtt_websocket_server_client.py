import asyncio
import signal
import sys
import threading
from mqttapi import MQTTCommunicator,WebSocketServer,WebSocketClient


HOST_WS = 'localhost'
PORT_WS = 8769

MQTT_BROKER = 'localhost'
MQTT_PORT = 1883
MQTT_KEEPALIVE = 60
MQTT_BIND_ADDRESS = ''

topic_qos_tuples = [
    ('topic1', 0),
    ('topic2', 1),
    ('topic3', 2)
    ]

def run_websocket_server():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    server = WebSocketServer(HOST_WS, PORT_WS)
    try:
        loop.run_until_complete(server.run_server())
    except KeyboardInterrupt:
        server.stop_server()
        loop.stop()
    
    loop.close()

async def send_data(topico, msg):
    websocket_client = WebSocketClient(websocket_server=f"ws://{HOST_WS}:{PORT_WS}/")
    await websocket_client.connect()

    topic = f"{topico}"
    payload = f"{msg}"

    await websocket_client.send_message(topic, payload)

    await websocket_client.close()

def main():
    websocket_thread = threading.Thread(target=run_websocket_server)
    websocket_thread.start()
    
    try:
        def signal_handler(signal, frame):
            print("\nPrograma encerrado.\n")
            mqtt_communicator.disconnect()
            sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler)

        mqtt_communicator = MQTTCommunicator(host=MQTT_BROKER, port=MQTT_PORT, keepalive=MQTT_KEEPALIVE, bind_address=MQTT_KEEPALIVE)
        mqtt_communicator.connect()

        mqtt_communicator.subscribe_to_topics(topic_qos_tuples)

        def on_messages(client, userdata, msg):
            topic = msg.topic
            payload = msg.payload.decode("utf-8")
            print(f"Received MQTT message. Topic: {topic}, Payload: {payload}")
            
            
            asyncio.run(send_data(topic, payload))

        def signal_handler(signal, frame):
            print("\nPrograma encerrado.\n")
            mqtt_communicator.disconnect()
            sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler)
        mqtt_communicator.client.on_message = on_messages

        while True:
            mqtt_communicator.client.loop_start()
            
    except KeyboardInterrupt:
        pass

    # Parar a thread do servidor WebSocket ao finalizar o programa
    websocket_thread.join()

# Executar o programa principal
if __name__ == "__main__":
    main()
