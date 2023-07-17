from websocket_server import WebSocketServer


def main():
    # Criar o servidor WebSocket
    server = WebSocketServer('localhost', 8769)

    try:
        # Iniciar o servidor WebSocket
        server.run_server()
    except KeyboardInterrupt:
        # Parar o servidor ao pressionar Ctrl+C
        server.stop_server()

# Executar o programa principal
if __name__ == "__main__":
    main()