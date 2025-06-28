```markdown
# 🔌 IoT Remote Monitoring System

A professional IoT system for **remote monitoring and control** of an embedded device using an **STM32**, **ESP32**, and a **FastAPI backend**. This project enables **real-time voltage monitoring** and **remote LED control** via a dashboard and RESTful API.

---

## 📦 Overview

This system enables:

- 📈 Real-time voltage data reading from an STM32 microcontroller.
- 🔁 Data transmission over UART from STM32 to ESP32.
- 🌐 HTTP communication from ESP32 to a FastAPI backend server.
- 💻 A web dashboard to visualize live voltage readings.
- 🟢 Remote ON/OFF control of an LED on STM32's `PC13` pin.
- 🧠 Designed for **embedded systems diagnostics**, **IoT education**, and **remote device monitoring**.

---

## 🧩 Architecture

```
[STM32] --UART--> [ESP32] --HTTP--> [FastAPI Server] --> [Web Dashboard]
                     ^                                         |
                     |------------<-- ON/OFF Commands ---------|
```

- **STM32**: Measures voltage, listens for control commands (ON/OFF) for LED on PC13.
- **ESP32**: Bridges UART data to the cloud via HTTP and relays server commands to STM32.
- **FastAPI Server**: Hosts the REST API and dashboard, processes data and sends commands.

---

## 🚀 Features

- 📤 **Voltage Streaming**: Voltage data pushed periodically to backend.
- 📊 **Dashboard**: Live plot of incoming voltage data.
- 💡 **Remote LED Control**: Toggle PC13 pin via UI or API.
- 📱 **API-first Design**: Fully documented and testable via Swagger UI.
- ☁️ **Deployable on Render.com** or local server.

---

## 🛠️ Setup Instructions

### 1. STM32 Firmware

- Write firmware for STM32 (e.g., STM32F103C8T6) that:
  - Reads voltage data (ADC).
  - Sends data over UART (e.g., `USART1`).
  - Listens for "ON" / "OFF" string commands to toggle `PC13`.

Example data format (sent every 1s):
```
VOLTAGE:3.30\n
```

Incoming commands:
```
ON\n / OFF\n
```

> You can use STM32CubeMX to set up peripherals and generate code for Keil or PlatformIO.

---

### 2. ESP32 Firmware

#### Requirements:

- PlatformIO (recommended) or Arduino IDE
- Libraries:
  - `WiFi.h`
  - `HTTPClient.h`
  - `HardwareSerial.h`

#### Responsibilities:

- Connect to Wi-Fi.
- Read voltage from UART.
- POST voltage to FastAPI endpoint.
- GET command state (ON/OFF) from FastAPI every few seconds and relay it to STM32.

#### Flashing ESP32:

```bash
# Navigate to the ESP32 firmware directory
cd firmware/esp32

# Compile and upload
pio run --target upload
```

Make sure to configure:
```cpp
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";
const char* serverUrl = "http://<your-api-server>/api/voltage";
```

---

### 3. FastAPI Backend

#### 📋 Features:

- `/api/voltage` (POST): Receive voltage from ESP32.
- `/api/voltage` (GET): Return recent voltage readings.
- `/api/control` (GET/POST): Get or set LED status.
- `/dashboard`: View live dashboard.

#### 🔧 Setup Locally:

```bash
# Clone the repo
git clone https://github.com/yourusername/iot-monitoring-system.git
cd iot-monitoring-system/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn main:app --reload
```

#### 🌐 Deploy on Render.com:

1. Push to a public GitHub repo.
2. Go to [Render.com](https://render.com).
3. Create new **Web Service**:
   - Environment: Python
   - Start command: `uvicorn main:app --host 0.0.0.0 --port 10000`
4. Set environment variables if needed (e.g., `PORT=10000`).

---

## 🖥️ Web Dashboard

Visit `/dashboard` on your FastAPI server to view:

- 📉 Live voltage graph (updated in real-time).
- 💡 LED ON/OFF toggle with current state.
  
Accessible at:
```
http://localhost:8000/dashboard
```
or on Render:
```
https://your-render-app-name.onrender.com/dashboard
```

---

## 📡 API Documentation

FastAPI provides built-in API docs at:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### 🔌 API Endpoints

#### `POST /api/voltage`

Send voltage from ESP32.

```json
{
  "value": 3.3
}
```

#### `GET /api/voltage`

Returns list of recent readings.

```json
[
  { "timestamp": "2025-06-29T12:00:00Z", "value": 3.3 },
  ...
]
```

#### `GET /api/control`

Returns current LED state.

```json
{ "state": "ON" }
```

#### `POST /api/control`

Set LED state.

```json
{ "state": "OFF" }
```

---

## 🧪 Testing the System

- Ensure STM32 is running and connected to ESP32 via UART.
- Flash ESP32 with correct Wi-Fi and server URL.
- Start the FastAPI server.
- Navigate to `/dashboard` to monitor and control.
- Use `/docs` to manually test API endpoints.

---

## 🧰 Tech Stack

- 👾 STM32 (HAL-based firmware via STM32CubeMX)
- 📡 ESP32 (PlatformIO, Wi-Fi + UART)
- 🐍 Python 3.10+
- 🚀 FastAPI + Uvicorn
- 📊 Chart.js + HTML for dashboard

---

## 🤝 Contributions

Contributions, issues, and suggestions are welcome! Please fork the repo and submit a pull request.

---

## 📄 License

This project is licensed under the MIT License. See `LICENSE` for more info.

---

## 🌟 Acknowledgments

- Thanks to the communities behind STM32, ESP32, FastAPI, and Open Source tools!

---

Happy Monitoring! 📶💡📊
```
