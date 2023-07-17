import datetime
from mqttapi import MQTTCommunicator,MySQLManipulator
import signal
import sys

#altere esses parametros:
mqtt_communicator = MQTTCommunicator(host='localhost', port=1883, keepalive=60, bind_address='')
bd_manipulator = MySQLManipulator(host='localhost', user='your_username', password='your_password', database='your_database',port=3306)

mqtt_communicator.connect()
bd_manipulator.connect()

topic_qos_tuples = [
    ('topic1', 0),
    ('topic2', 1),
    ('topic3', 2)
]

mqtt_communicator.subscribe_to_topics(topic_qos_tuples)

def signal_handler(signal, frame):
    print("\nPrograma encerrado.\n")
    bd_manipulator.disconnect()
    mqtt_communicator.disconnect()
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

def handle_message(client, userdata, msg):
        mensagem = msg.payload.decode()#É feito isso pois a mensabem vem em bytes, entao ao invés de uma mensagem de: b'30 nós teremos: 30
        topico = str(msg.topic)
        qos = msg.qos
        data_hora_medicao= datetime.datetime.now(datetime.timezone.utc)
        print("message: "+mensagem)
        print("topic: "+topico)
        
        #caso queira que uma tabela já existente seja usada ou uma nova seja criada, altere o parametro 'tabela' do método
        #insert_data
        bd_manipulator.insert_data(mensagem, topico, qos, data_hora_medicao,tabela ='dados')
        #A ordem é: A mensagem(medição do sensor), o tópico(relacionado ao protocolo mqtt), o qos(relacionado ao protocolo mqtt)
        #e a data(nao obrigatorio, mas caso não for colocado, então irá aparecer em formato UTC)

while True:
    mqtt_communicator.client.loop_start()
    mqtt_communicator.client.on_message = handle_message
    
