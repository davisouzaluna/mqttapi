import signal
import sys
import datetime
import threading
import asyncio
import websockets

from mqtt_communicator import MQTTCommunicator
from websocket_client import WebSocketClient
from websocket_server import WebSocketServer

# Variáveis de controle do MQTT
BROKER = "test.mosquitto.org"
PORT = 1883
KEEPALIVE = 60
BIND = ""

# Variável para controlar a execução das threads
running = True

# Instanciar objetos
mqtt_communicator = MQTTCommunicator(BROKER, PORT, KEEPALIVE, BIND)

# Conectar ao MQTT broker
mqtt_communicator.connect()

# Iniciar o servidor WebSocket
server = WebSocketServer('localhost', 8769)

async def run_server():
    # Iniciar o servidor WebSocket
    start_server = websockets.serve(server.handle_websocket, server.host, server.port)

    # Executar o servidor em um loop de eventos
    await start_server


# Criar o loop de eventos
loop = asyncio.get_event_loop()

# Iniciar o cliente WebSocket
websocket_client = WebSocketClient()
loop.create_task(websocket_client.connect())

# Inscrever-se em vários tópicos/DEBUG
topics = [("topic1", 0), ("123456789123", 1), ("dataSet", 0)]
mqtt_communicator.subscribe_to_topics(topics)

# Função de tratamento de sinal para interromper o programa corretamente
def signal_handler(signal, frame):
    global running
    print("Programa encerrado.")
    running = False
    mqtt_communicator.disconnect()
    loop.stop()


signal.signal(signal.SIGINT, signal_handler)


# Sobrecarga de método
def handle_message(client, userdata, v):
    payload_str = v.payload.decode()  # Converter o payload em uma string
    mensagem = payload_str  # Usar a string convertida como mensagem

    print("=============================")
    print("Topic: " + str(v.topic))
    print("Payload: " + str(payload_str))  # Usar a string convertida aqui
    print("Hora: " + datetime.datetime.now(datetime.timezone.utc).strftime("%H:%M:%S"))
    print("Debug")
    websocket_client.send_message(v.topic, payload_str)
    print("==========================================")


async def main():
    # Iniciar o servidor WebSocket
    await run_server()

    loop = asyncio.get_event_loop()
    loop.create_task(websocket_client.connect())
    mqtt_communicator.client.loop_start()
    mqtt_communicator.client.on_message = handle_message
    # Aguardar o sinal de interrupção
    while running:
        await asyncio.sleep(1)
        
        

# Executar o loop principal
asyncio.run(main())
