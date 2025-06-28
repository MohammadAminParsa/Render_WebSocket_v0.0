```markdown
# ⚡ WebSocket Server for ESP32 (Node.js)

A simple and lightweight **Node.js** WebSocket server that receives **voltage** and **status** data from an ESP32 microcontroller and forwards it to all connected WebSocket clients in real time. 🔁📡

---

## 🚀 Overview

This project enables real-time communication between an ESP32 device and browser or desktop clients using WebSockets. The ESP32 sends structured messages (like voltage levels and device status), and this server efficiently relays that data to all connected clients.

Perfect for building dashboards, monitoring systems, or IoT applications. 🌐📈

---

## 🧰 Features

- 🔌 Real-time WebSocket communication
- 📶 Multi-client support
- ⚙️ Forwards voltage and status data from ESP32
- 💡 Lightweight and minimal dependencies
- 🌐 Easy integration with frontends or monitoring tools

---

## 📡 How It Works

1. ESP32 connects to the WebSocket server via Wi-Fi.
2. Sends JSON-formatted messages containing:
   - 📊 Voltage readings
   - ✅ Status indicators (e.g., "OK", "LOW", "ERROR")
3. The server receives the data and broadcasts it to all connected clients.

---

## 🛠️ Setup

### 📦 Requirements

- [Node.js](https://nodejs.org/) (v14 or higher recommended)
- ESP32 with WebSocket client firmware

### 🔧 Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/yourusername/esp32-websocket-server.git
cd esp32-websocket-server
npm install
```

---

## 🚀 Run the Server

Start the WebSocket server with:

```bash
node server.js
```

By default, the server listens on port `8080`.

---

## 🧪 Example ESP32 Payload

The ESP32 should send a JSON object like this:

```json
{
  "voltage": 3.72,
  "status": "ON"
}
```

> Ensure your ESP32 sends data to: `ws://<your-server-ip>:10000`

---

## 🖥️ Example Client Code (JavaScript)

Here's how a browser-based client can connect and receive data:

```javascript
const socket = new WebSocket("ws://localhost:8080");

socket.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log("Voltage:", data.voltage);
  console.log("Status:", data.status);
};
```

---

## 📁 File Structure

```
esp32-websocket-server/
├── server.js               # WebSocket server logic
├── package.json            # Project metadata and dependencies
├── .gitignore
└── README.md               # Project documentation
```

---

## 🔐 Security Notes

For production deployments:

- Use secure WebSockets (`wss://`) over HTTPS
- Add basic authentication or tokens
- Validate incoming ESP32 payloads

---

## 📌 Roadmap

- [ ] Add persistent logging (e.g., MongoDB, InfluxDB)
- [ ] Create a live frontend dashboard
- [ ] Add message validation & schema enforcement
- [ ] Support secure WebSocket connections

---

## 🤝 Contributing

Contributions are welcome! Feel free to fork the repo and submit a pull request. 💻✨

---

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## 📬 Contact

For support or collaboration:

- GitHub Issues
- mohammad.amin.parsa0082@gmail.com

---

Thanks for checking out this project! 🚀📡
```
