from fastapi import FastAPI, Query, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

app = FastAPI()

# ───────────── Middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"]
)

# ───────────── درون‌سازی داده‌ها
voltage_value = "0.000"
status_value = "ON"

# ───────────── صفحات ساده برای تست در مرورگر
@app.get("/", response_class=HTMLResponse)
async def index():
    return f"""
    <h1>🌐 ESP32 Monitoring</h1>
    <p><b>Voltage:</b> {voltage_value} V</p>
    <p><b>Status:</b> {status_value}</p>
    <form action="/status" method="post">
      <button name="status" value="ON">🔋 Turn ON</button>
      <button name="status" value="OFF">⛔ Turn OFF</button>
    </form>
    """

# ───────────── API دریافت داده برای اپ یا مرورگر
@app.get("/data")
def get_data():
    return {
        "device_id": "esp32-001",
        "timestamp": datetime.utcnow().isoformat(),
        "voltage": voltage_value,
        "status": status_value
    }

# ───────────── API ارسال ولتاژ توسط ESP32
@app.post("/data")
def post_data(v: float = Form(...)):  # تغییر از Query به Form
    global voltage_value
    voltage_value = f"{v:.3f}"
    return {
        "message": "Voltage updated",
        "voltage": voltage_value,
        "timestamp": datetime.utcnow().isoformat()
    }

# ───────────── API دریافت وضعیت برای ESP32
@app.get("/status")
def get_status():
    return {"status": status_value}

# ───────────── API تغییر وضعیت از طریق UI یا اپلیکیشن
@app.post("/status")
def set_status(status: str = Query(...)):
    global status_value
    status = status.upper()
    if status in ["ON", "OFF"]:
        status_value = status
        return {
            "message": f"Status set to {status_value}",
            "timestamp": datetime.utcnow().isoformat()
        }
    return JSONResponse(status_code=400, content={"error": "Invalid status"})
