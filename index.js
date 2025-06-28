const express = require('express');
const http = require('http');
const WebSocket = require('ws');
const app = express();

// پورت ۵۰۰۰ پیش‌فرض Render است
const PORT = process.env.PORT || 5000;
const server = http.createServer(app);

const wss = new WebSocket.Server({ server, path: "/ws" });

let latestVoltage = "0.000";
let deviceStatus = "ON";

wss.on('connection', (ws) => {
  console.log("🔗 New client connected");

  // ارسال اطلاعات اولیه به کلاینت (مثلاً مرورگر)
  ws.send(JSON.stringify({
    voltage: latestVoltage,
    status: deviceStatus,
    source: "server"
  }));

  ws.on('message', (message) => {
    console.log("📥 Received:", message.toString());

    // پردازش پیام JSON از ESP32
    try {
      const data = JSON.parse(message.toString());
      if (data.voltage) latestVoltage = data.voltage;
      if (data.status) deviceStatus = data.status;

      // در صورت نیاز به پخش برای همه:
      wss.clients.forEach((client) => {
        if (client !== ws && client.readyState === WebSocket.OPEN) {
          client.send(JSON.stringify(data));
        }
      });
    } catch (err) {
      console.log("❌ Invalid message format");
    }
  });

  ws.on('close', () => {
    console.log("❌ Client disconnected");
  });
});

app.get("/", (req, res) => {
  res.send("🟢 WebSocket Server is Running!");
});

server.listen(PORT, () => {
  console.log(`🚀 Server running on port ${PORT}`);
});
