from mqttapi import MQTTCommunicator
from mqttapi import JSONManipulator    
import signal
import sys


#Por enquanto, nesse exemplo, o código do JSONManipulator ainda não foi adicionadoao MQTTapi
mqtt_communicator = MQTTCommunicator(host='localhost', port=1883, keepalive=60, bind_address='')
json_manipulator = JSONManipulator()

mqtt_communicator.connect()

topic_qos_tuples = [
    ('dataSets', 0),
    ('topic2', 1),
    ('topic3', 2),
]
mqtt_communicator.subscribe_to_topics(topic_qos_tuples)

#Callback 
def on_messages(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode("utf-8")
    print(f"Received MQTT message. Topic: {topic}, Payload: {payload}")
    json_manipulator.createMQTTjson(msg,"teste")
    
    # Chame o método on_message do mqtt_communicator
    

#Quando for clicar em ctrl+c, o programa irá chamar a função signal_handler
def signal_handler(signal, frame):
    print("\nPrograma encerrado.\n")
    mqtt_communicator.disconnect()
    sys.exit(0)

#chamada da função acima
signal.signal(signal.SIGINT, signal_handler)

#Loop para ficar escutando mensagens
while True:
    mqtt_communicator.client.loop_start()
    mqtt_communicator.client.on_message = on_messages

# Opcionalmente pode-se implementar um: time.sleep(1)
