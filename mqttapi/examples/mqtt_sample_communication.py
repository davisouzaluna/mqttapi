from mqttapi import MQTTCommunicator
import signal
import sys



mqtt_communicator = MQTTCommunicator(host='localhost', port=1883, keepalive=60, bind_address='')

mqtt_communicator.connect()

topic_qos_tuples = [
    ('topic1', 0),
    ('topic2', 1),
    ('topic3', 2),
]
mqtt_communicator.subscribe_to_topics(topic_qos_tuples)

#Callback 
def on_messages(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode("utf-8")
    print(f"Received MQTT message. Topic: {topic}, Payload: {payload}")
    # Chame o método on_message do mqtt_communicator
    


def signal_handler(signal, frame):
    print("\nPrograma encerrado.\n")
    mqtt_communicator.disconnect()
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)



while True:
    mqtt_communicator.client.loop_start()
    mqtt_communicator.client.on_message = on_messages

# Opcionalmente pode-se implementar um: time.sleep(1)
