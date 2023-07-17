import asyncio
from mqttapi import MQTTCommunicator,WebSocketClient
import signal
import sys



mqtt_communicator = MQTTCommunicator(host='broker.hivemq.com', port=1883, keepalive=60, bind_address='')

mqtt_communicator.connect()

topic_qos_tuples = [
    ('dataSets', 0),
    ('topic2', 1),
    ('topic3', 2)
]
mqtt_communicator.subscribe_to_topics(topic_qos_tuples)


def on_messages(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode("utf-8")
    print(f"Received MQTT message. Topic: {topic}, Payload: {payload}")
    # Chame o método on_message do mqtt_communicator
    asyncio.run(send_data(topic,payload))


def signal_handler(signal, frame):
    print("\nPrograma encerrado.\n")
    mqtt_communicator.disconnect()
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)
async def send_data(topico,msg):
    websocket_client = WebSocketClient(websocket_server="ws://localhost:8769/")


    await websocket_client.connect()

    topic = f"{topico}"
    payload = f"{msg}"

    await websocket_client.send_message(topic, payload)

    await websocket_client.close()





while True:
    mqtt_communicator.client.loop_start()
    mqtt_communicator.client.on_message = on_messages

# Opcionalmente pode-se implementar um: time.sleep(1)
