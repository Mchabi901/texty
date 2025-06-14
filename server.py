import asyncio
import websockets

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
    async with websockets.serve(handler, "0.0.0.0", 8765):
        print("Server started at ws://0.0.0.0:8765")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
