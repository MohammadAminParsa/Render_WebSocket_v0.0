from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import uvicorn, os

app = FastAPI()

clients = set()
last_data = {"voltage": "0.000", "status": "ON"}

@app.get("/")
async def get_home():
    return HTMLResponse("""
    <html>
      <head><title>ESP32 Monitor</title></head>
      <body>
        <h1>ESP32 WebSocket Server</h1>
        <p>Status: <span id="status">Connecting...</span></p>
        <script>
          let ws = new WebSocket("ws://" + location.host + "/ws");
          ws.onopen = () => document.getElementById("status").innerText = "🟢 Connected!";
          ws.onmessage = (msg) => console.log("📥 Received: " + msg.data);
        </script>
      </body>
    </html>
    """)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.add(websocket)
    print("🟢 Client connected")

    try:
        while True:
            msg = await websocket.receive_text()
            print("📥 Received:", msg)

            # ذخیره آخرین داده (اختیاری برای ارسال به کلاینت‌های جدید)
            last_data.update(eval(msg))  # فرض بر JSON ساده {"voltage": "...", "status": "..."}
            
            # ارسال به همه کلاینت‌های دیگر
            for client in clients:
                if client != websocket:
                    await client.send_text(msg)
    except WebSocketDisconnect:
        print("🔴 Client disconnected")
        clients.remove(websocket)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # پیش‌فرض 8000 برای تست محلی
    uvicorn.run("main:app", host="0.0.0.0", port=port)
