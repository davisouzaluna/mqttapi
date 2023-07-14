import asyncio
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
            
