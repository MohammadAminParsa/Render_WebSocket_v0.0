const ws = new WebSocket("wss://" + location.host + "/ws");

let chart = new Chart(document.getElementById("chart"), {
  type: "line",
  data: {
    labels: [],
    datasets: [{
      label: "Voltage (V)",
      borderColor: "blue",
      data: [],
      tension: 0.3
    }]
  },
  options: {
    responsive: true,
    animation: false,
    scales: {
      x: { display: false },
      y: {
        suggestedMin: 0,
        suggestedMax: 5
      }
    }
  }
});

ws.onopen = () => console.log("🟢 WebSocket connected!");
ws.onclose = () => console.log("🔴 WebSocket closed");
ws.onerror = (e) => console.error("❌ WebSocket error", e);

ws.onmessage = (event) => {
  try {
    const data = JSON.parse(event.data);
    if (data.voltage) {
      document.getElementById("voltage").textContent = `Voltage: ${data.voltage} V`;

      const now = new Date().toLocaleTimeString();
      chart.data.labels.push(now);
      chart.data.datasets[0].data.push(parseFloat(data.voltage));

      if (chart.data.labels.length > 30) {
        chart.data.labels.shift();
        chart.data.datasets[0].data.shift();
      }
      chart.update();
    }
  } catch (err) {
    console.error("Error parsing:", err);
  }
};

function sendCommand(cmd) {
  if (ws.readyState === WebSocket.OPEN) {
    ws.send(cmd);
    console.log("📤 Sent command:", cmd);
  }
}
