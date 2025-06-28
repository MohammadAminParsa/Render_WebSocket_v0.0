const express = require('express');
const http = require('http');
const WebSocket = require('ws');
const app = express();

const PORT = process.env.PORT || 80;
const server = http.createServer(app);

// مسیر /ws برای WebSocket
const wss = new WebSocket.Server({ server, path: "/ws" });

wss.on('connection', ws => {
  console.log('🟢 New WebSocket connected');
  ws.on('message', msg => {
    console.log('📥', msg);
    wss.clients.forEach(c => {
      if (c !== ws && c.readyState === WebSocket.OPEN) {
        c.send(msg);
      }
    });
  });
  ws.on('close', () => console.log('🔴 WebSocket disconnected'));
});

app.get('/', (_, res) => res.sendFile(__dirname + '/public/index.html'));

server.listen(PORT, () => {
  console.log(`🚀 Server listening on port ${PORT}`);
});
