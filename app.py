from flask import Flask, request, jsonify

app = Flask(__name__)

latest_data = {
    "voltage": "0.00",
    "status": "OFF"
}

@app.route('/')
def home():
    return '''
    <html>
    <head>
    <title>ESP32 Realtime</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
      body { text-align: center; font-family: sans-serif; }
      button { padding: 10px 20px; font-size: 16px; }
    </style>
    </head>
    <body>
      <h1>📡 Real-time Voltage Monitor</h1>
      <canvas id="chart" width="400" height="180"></canvas>
      <br>
      <button id="toggleBtn">Toggle</button>
      <p id="statusText">Status: OFF</p>

      <script>
        let chartCtx = document.getElementById('chart').getContext('2d');
        let chart = new Chart(chartCtx, {
          type: 'line',
          data: {
            labels: [],
            datasets: [{
              label: 'Voltage (V)',
              data: [],
              borderColor: 'blue',
              fill: false
            }]
          },
          options: {
            scales: {
              x: { display: false },
              y: { min: 0, max: 3.5 }
            }
          }
        });

        async function fetchData() {
          const res = await fetch('/latest');
          const data = await res.json();
          const voltage = parseFloat(data.voltage);
          const status = data.status;

          chart.data.labels.push('');
          chart.data.datasets[0].data.push(voltage);
          if (chart.data.labels.length > 20) {
            chart.data.labels.shift();
            chart.data.datasets[0].data.shift();
          }
          chart.update();

          document.getElementById("statusText").innerText = "Status: " + status;
        }

        setInterval(fetchData, 2000);

        document.getElementById("toggleBtn").onclick = async () => {
          let currentStatus = document.getElementById("statusText").innerText.includes("ON") ? "OFF" : "ON";
          await fetch("/control", {
            method: "POST",
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ "status": currentStatus })
          });
        }
      </script>
    </body>
    </html>
    '''


@app.route('/upload', methods=['POST'])
def upload():
    global latest_data
    latest_data = request.json
    return '', 200

@app.route('/latest', methods=['GET'])
def latest():
    return jsonify(latest_data)

@app.route('/control', methods=['GET', 'POST'])
def control():
    global latest_data
    if request.method == 'POST':
        latest_data['status'] = request.json.get('status', 'OFF')
        return '', 200
    else:
        return jsonify({"status": latest_data['status']})

import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))  # اگر PORT تعریف نشده بود، 10000 استفاده می‌کنه
    app.run(host='0.0.0.0', port=port)

