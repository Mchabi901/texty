import asyncio
import websockets
import os

clients = set()

async def handler(websocket):
    print("New client connected")
    clients.add(websocket)
    try:
        async for message in websocket:
            print("Received:", message)
            for client in clients:
                if client != websocket:
                    await client.send(message)
    except:
        print("Client disconnected")
    finally:
        clients.remove(websocket)

async def main():
    port = int(os.environ.get("PORT", 8765))  # Use Railway's PORT or default to 8765
    async with websockets.serve(handler, "0.0.0.0", port):
        print(f"Server started at ws://0.0.0.0:{port}")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
