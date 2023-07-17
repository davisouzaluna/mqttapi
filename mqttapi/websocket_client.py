import asyncio
import json
import websockets


class WebSocketClient:
    def __init__(self, websocket_server="ws://localhost:8769/"):
        self.websocket_server = websocket_server
        self.websocket = None
        self.is_running = False

    async def connect(self):
        self.websocket = await websockets.connect(self.websocket_server)

    async def send_message(self, topic, payload):
        if self.websocket and self.websocket.open:
            message = {
                'topic': topic,
                'payload': payload
            }
            await self.websocket.send(json.dumps(message))

    def on_mqtt_message(self, client, userdata, msg):
        topic = msg.topic
        payload = msg.payload.decode("utf-8")
        asyncio.create_task(self.send_message(topic, payload))

    async def run(self, mqtt_communicator):
        mqtt_communicator.on_message = self.on_mqtt_message
        mqtt_communicator.connect()
        await self.connect()
        self.is_running = True
        while self.is_running:
            mqtt_communicator.client.loop()
            await asyncio.sleep(1)

    async def close(self):
        if self.websocket and self.websocket.open:
            try:
                await self.websocket.close()
                print("WebSocket connection closed")
            except websockets.exceptions.ConnectionClosedError:
                print("WebSocket connection already closed")

    def stop(self):
        self.is_running = False
