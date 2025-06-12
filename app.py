from flask import Flask, request, jsonify

app = Flask(__name__)

latest_data = {
    "voltage": "0.00",
    "status": "OFF"
}

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>ESP32 Dashboard</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 20px;
                background: #f5f5f5;
                text-align: center;
            }
            h1 {
                color: #333;
            }
            canvas {
                max-width: 100%;
                height: 300px !important;
                margin-bottom: 30px;
                background: white;
                border: 1px solid #ccc;
            }
            #toggleBtn {
                padding: 12px 24px;
                font-size: 18px;
                border: none;
                cursor: pointer;
                border-radius: 6px;
            }
            .on {
                background: #28a745;
                color: white;
            }
            .off {
                background: #dc3545;
                color: white;
            }
        </style>
    </head>
    <body>
        <h1>🌡️ ESP32 Voltage Monitor</h1>
        <canvas id="chart"></canvas>
        <br>
        <button id="toggleBtn" class="off">OFF</button>

        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <script src="https://cdn.socket.io/4.7.2/socket.io.min.js"></script>
        <script>
            const ctx = document.getElementById('chart').getContext('2d');
            const chart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: [],
                    datasets: [{
                        label: 'Voltage (V)',
                        borderColor: 'blue',
                        backgroundColor: 'lightblue',
                        data: [],
                        tension: 0.2
                    }]
                },
                options: {
                    scales: {
                        y: { suggestedMin: 0, suggestedMax: 3.5 }
                    }
                }
            });

            const socket = io();
            socket.on('voltage', function(data) {
                const time = new Date().toLocaleTimeString();
                chart.data.labels.push(time);
                chart.data.datasets[0].data.push(data.voltage);
                if (chart.data.labels.length > 20) {
                    chart.data.labels.shift();
                    chart.data.datasets[0].data.shift();
                }
                chart.update();
            });

            const toggleBtn = document.getElementById('toggleBtn');
            toggleBtn.addEventListener('click', () => {
                const newState = toggleBtn.classList.contains('on') ? 'OFF' : 'ON';
                socket.emit('control', { status: newState });
            });

            socket.on('status', function(data) {
                if (data.status === 'ON') {
                    toggleBtn.classList.remove('off');
                    toggleBtn.classList.add('on');
                    toggleBtn.textContent = 'ON';
                } else {
                    toggleBtn.classList.remove('on');
                    toggleBtn.classList.add('off');
                    toggleBtn.textContent = 'OFF';
                }
            });
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

