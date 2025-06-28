from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import os
import uvicorn

app = FastAPI()

# ✅ فعال‌سازی CORS برای اجاره دسترسی همه کلاینت‌ها
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

clients = set()

@app.get("/")
async def read_root():
    return {"message": "WebSocket Server is running!"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.add(websocket)
    print("🟢 Client connected")

    try:
        while True:
            data = await websocket.receive_text()
            print("📥 Received from client:", data)
            for client in clients:
                if client != websocket:
                    await client.send_text(data)
    except WebSocketDisconnect:
        print("🔴 Client disconnected")
        clients.remove(websocket)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
