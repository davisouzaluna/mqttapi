import paho.mqtt.client as mqtt
import time
import random

BROKER="test.mosquitto.org"
PORT=1883
KEEPALIVE=60
TOPIC="dataSet"
time_sleep_pub=1

#Publisher
client = mqtt.Client()
client.connect(BROKER, PORT, KEEPALIVE)
client.loop_start()

def publish_data(data):
    client.publish(TOPIC, data)

try:
    while True:
        message=random.randint(0, 30)
        client.publish(TOPIC, message)
        time.sleep(time_sleep_pub)
        
except KeyboardInterrupt:
    print("\nSaindo")
    client.disconnect()
    client.loop_stop()
except Exception as e:
    print("Erro: ", e)
    client.disconnect()
    client.loop_stop()