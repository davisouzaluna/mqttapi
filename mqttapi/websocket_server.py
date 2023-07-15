import asyncio
import json
import threading
import websockets


class WebSocketServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.connected_clients = set()
        self.server = None

    async def handle_websocket(self, client, path):
        # Adicionar o cliente à lista de clientes conectados
        self.connected_clients.add(client)

        try:
            # Aguardar mensagens do cliente
            async for message in client:
                # Aqui você pode processar a mensagem recebida do cliente WebSocket, se necessário
                print("Received message:", message)

                # Enviar mensagem para todos os clientes conectados
                for connected_client in self.connected_clients:
                    await connected_client.send(message)
        finally:
            # Remover o cliente da lista de clientes conectados
            self.connected_clients.remove(client)

    def run_server(self):
        # Iniciar o servidor WebSocket
        self.server = websockets.serve(self.handle_websocket, self.host, self.port)

        # Executar o servidor em um loop de eventos
        asyncio.get_event_loop().run_until_complete(self.server)
        asyncio.get_event_loop().run_forever()

    def stop_server(self):
        if self.server:
            self.server.close()
            
    def send_message_to_websocket(topic, payload):
        if websocket and websocket.sock and websocket.sock.connected:
            message = {
                'topic': topic,
                'payload': payload
            }
            websocket.send(json.dumps(message))
            
    def connect_to_websocket(WEBSOCKET_SERVER):
        global websocket
        websocket = websocket.WebSocketApp(WEBSOCKET_SERVER, on_message=on_message)
        websocket.run_forever()
        
    def on_message(ws, message):
        data = json.loads(message)
        topic = data['topic']
        payload = data['payload']

    def start_websocket_thread(self):
        websocket_thread = threading.Thread(target=self.connect_to_websocket)
        websocket_thread.daemon = True
        websocket_thread.start()



            
