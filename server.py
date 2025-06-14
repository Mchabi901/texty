# server.py
import asyncio
import websockets
import json

clients = {}  # websocket -> name

async def notify_users():
    names = list(clients.values())
    if clients:
        message = json.dumps({"type": "users", "list": names})
        await asyncio.wait([ws.send(message) for ws in clients])

async def handler(ws):
    try:
        async for message in ws:
            data = json.loads(message)

            if data["type"] == "join":
                clients[ws] = data["name"]
                await notify_users()

            elif data["type"] == "chat":
                full_msg = json.dumps({
                    "type": "chat",
                    "name": data["name"],
                    "text": data["text"]
                })
                await asyncio.wait([client.send(full_msg) for client in clients])

    except websockets.ConnectionClosed:
        print("Client disconnected")

    finally:
        if ws in clients:
            del clients[ws]
            await notify_users()

start_server = websockets.serve(handler, "0.0.0.0", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

