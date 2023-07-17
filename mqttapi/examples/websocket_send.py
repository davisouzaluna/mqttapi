import asyncio
from websocket_client import WebSocketClient

async def send_data():
    websocket_client = WebSocketClient(websocket_server="ws://localhost:8769/")


    await websocket_client.connect()

    topic = "example_topic"
    payload = "example_payload"

    await websocket_client.send_message(topic, payload)

    await websocket_client.close()

asyncio.run(send_data())
