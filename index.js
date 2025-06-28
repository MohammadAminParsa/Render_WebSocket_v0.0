const express = require('express');
const http = require('http');
const WebSocket = require('ws');

const app = express();
app.use(express.static('public'));

const server = http.createServer(app);
const wss = new WebSocket.Server({ server });

let clientSocket = null;

wss.on('connection', ws => {
  console.log('Client connected');
  clientSocket = ws;
  ws.on('message', message => {
    console.log('Received:', message);
    // ارسال فرمان به ESP32 اگر JSON با فرمان باشد
    try {
      const data = JSON.parse(message);
      if (data.command && clientSocket) {
        clientSocket.send(data.command);
      }
    } catch (e) {}
  });
  ws.on('close', () => {
    console.log('Client disconnected');
    clientSocket = null;
  });
});

server.listen(5000, () => {
  console.log('Server listening on http://localhost:5000');
});
