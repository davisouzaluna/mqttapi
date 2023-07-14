import paho.mqtt.client as mqtt
import datetime

class MQTTCommunicator:
    def __init__(self, host, port, keepalive, bind_address):
        self.host = host
        self.port = port
        self.keepalive = keepalive
        self.bind_address = bind_address
        self.client = mqtt.Client("python3")
        self.connected = False

    def connect(self):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(self.host, self.port, self.keepalive, self.bind_address)
        self.client.loop_start()

    def disconnect(self):
        self.client.disconnect()
        self.client.loop_stop()
        self.connected = False

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected with result code " + str(rc))
            self.connected = True
        else:
            print("Connection failed")
            
    def subscribe_to_topics(self, topic_qos_tuples):
        for topic, qos in topic_qos_tuples:
            self.client.subscribe(topic, qos=qos)
            print("Subscribed to topic:", topic, "with QoS:", qos)

    def on_message(self, client, userdata, msg):
        print("=============================")
        print("Topic: " + str(msg.topic))
        print("Payload: " + str(msg.payload))
        print("Hora: " + datetime.datetime.now(datetime.timezone.utc).strftime("%H:%M:%S"))
        print("=============================")
