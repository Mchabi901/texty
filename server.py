from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os

app = FastAPI()
clients = []

# Enable CORS so your frontend can connect from any domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["https://texty-production.up.railway.app"] for stricter policy
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    print("🔌 Client connected")
    try:
        while True:
            data = await websocket.receive_text()
            print("📨 Received:", data)
            for client in clients:
                if client != websocket:
                    await client.send_text(data)
    except WebSocketDisconnect:
        print("❌ Client disconnected")
    finally:
        if websocket in clients:
            clients.remove(websocket)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  # Railway provides PORT in env
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=False)
