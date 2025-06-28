# main.py
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

import controller, data
from jinja2 import Template

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"]
)

# ⬇️ مسیر استاتیک برای HTML
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def index():
    with open("static/index.html") as f:
        html = Template(f.read())
    return HTMLResponse(content=html.render(
        voltage=data.get_voltage(),
        status=controller.get_status()
    ))

@app.get("/data")
def get_data():
    return {
        "voltage": data.get_voltage(),
        "status": controller.get_status()
    }

@app.post("/data")
def post_data(v: str):
    data.set_voltage(v)
    return {"message": "Voltage updated", "voltage": v}

@app.post("/status")
def post_status(status: str):
    if controller.set_status(status):
        return {"message": f"Status set to {status}"}
    return JSONResponse(status_code=400, content={"error": "Invalid status"})

@app.get("/status")
def get_status():
    return {"status": controller.get_status()}
