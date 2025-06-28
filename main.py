# main.py
from fastapi import FastAPI, Query
from fastapi import Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import controller, data

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"]
)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def index():
    with open("static/index.html") as f:
        return HTMLResponse(content=f.read())

@app.get("/data")
def get_data():
    return {
        "device_id": "esp32-001",
        "timestamp": datetime.utcnow().isoformat(),
        "data": {
            "voltage": data.get_voltage(),
            "status": controller.get_status()
        }
    }

@app.post("/data")
def post_data(v: str = Form(...)):  # توجه: تغییر از Query به Form
    data.set_voltage(v)
    return {
        "message": "Voltage updated",
        "voltage": v,
        "timestamp": datetime.utcnow().isoformat()
    }


@app.post("/status")
def post_status(status: str = Query(...)):
    if controller.set_status(status):
        return {
            "message": f"Status set to {status}",
            "timestamp": datetime.utcnow().isoformat()
        }
    return JSONResponse(status_code=400, content={"error": "Invalid status"})

@app.get("/status")
def get_status():
    return {"status": controller.get_status()}
