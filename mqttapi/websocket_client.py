import asyncio
import threading
import json
import datetime
import websockets


# Variável do WebSocket Server
WEBSOCKET_SERVER = "ws://localhost:8769/"


class WebSocketClient:
    def __init__(self):
        self.websocket = None
        self.closed = asyncio.Event()

    async def connect(self):
        self.websocket = await websockets.connect(WEBSOCKET_SERVER)
        websocket_thread = threading.Thread(target=self.receive_message)
        websocket_thread.daemon = True
        websocket_thread.start()

    async def send_message(self, topic, payload):
        if self.websocket and self.websocket.open:
            message = {
                'topic': topic,
                'payload': payload
            }
            await self.websocket.send(json.dumps(message))

    def receive_message(self):
        asyncio.run(self._receive_message())

    async def _receive_message(self):
        while True:
            if self.websocket and self.websocket.open:
                message = await self.websocket.recv()
                self.on_message(message)

    def on_message(self, message):
        data = json.loads(message)
        topic = data['topic']
        payload = data['payload']
        print(f"WebSocket received message\nTopic: {topic}\nPayload: {payload}")

    async def close(self):
        if self.websocket and self.websocket.open:
            await self.websocket.close()
            self.closed.set()
            print("WebSocket connection closed")

