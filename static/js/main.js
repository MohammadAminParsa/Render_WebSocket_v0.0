const socket = io(); // اتصال به Flask-SocketIO

// نمودار Chart.js
const ctx = document.getElementById('voltageChart').getContext('2d');
const voltageChart = new Chart(ctx, {
  type: 'line',
  data: {
    labels: [],
    datasets: [{
      label: 'Voltage (V)',
      data: [],
      borderColor: 'green',
      borderWidth: 2,
      fill: false
    }]
  },
  options: {
    responsive: true,
    animation: false,
    scales: {
      x: { display: false },
      y: { beginAtZero: true }
    }
  }
});

// دریافت داده جدید از سرور
socket.on('new_data', function(data) {
  const voltage = parseFloat(data.voltage);
  const time = new Date().toLocaleTimeString();

  voltageChart.data.labels.push(time);
  voltageChart.data.datasets[0].data.push(voltage);

  if (voltageChart.data.labels.length > 20) {
    voltageChart.data.labels.shift();
    voltageChart.data.datasets[0].data.shift();
  }

  voltageChart.update();
});

// ارسال دستور به سرور
function sendCommand(cmd) {
  socket.emit('command', { cmd: cmd });
}
