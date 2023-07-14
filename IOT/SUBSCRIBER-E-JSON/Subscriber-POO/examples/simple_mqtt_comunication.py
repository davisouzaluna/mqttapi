import time
import signal
import sys

#É preciso importar a classe(lugar do arquivo)
from mqtt_communicator import MQTTCommunicator

#Variáveis de controle do MQTT
BROKER = "test.mosquitto.org"
PORT = 1883
KEEPALIVE = 60
BIND = ""

#Variáveis de controle do banco(Mysql)
HOST = "localhost"
USER = "root"
PASSWORD = "root"
DATABASE = "Thingsafe"
PORT_DATABASE = 3306

# Instanciar objetos
mqtt_communicator = MQTTCommunicator(BROKER, PORT, KEEPALIVE, BIND)


# Conectar ao MQTT broker
mqtt_communicator.connect()

# Inscrever-se em vários tópicos/DEBUG
topics = [("topic1", 0), ("123456789123", 1), ("dataSet", 2)]
mqtt_communicator.subscribe_to_topics(topics)

# Função de tratamento de sinal para interromper o programa corretamente
def signal_handler(signal, frame):
    print("Programa encerrado.")
    mqtt_communicator.disconnect()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Loop principal
while True:
    mqtt_communicator.client.loop_start()
    
    #Sobrecarga de método(Para tratar a mensagem como quiser)
    def handle_message(client, userdata, msg):
        mensagem = str(msg.payload)
        topico = str(msg.topic)
        qos = msg.qos
           
    

    # Aguardar 1 segundo antes de executar novamente(O programa ficará sem fazer nada, portanto pode ser apagado para receber a mensagem a todo momento)
    time.sleep(1)
