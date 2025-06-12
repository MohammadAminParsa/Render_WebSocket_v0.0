from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# داده‌ی ولتاژ از ESP32
@socketio.on('esp_data')
def handle_esp_data(data):
    print("📥 دریافت از ESP32:", data)
    emit('update_voltage', data, broadcast=True)

# دستور کنترل از مرورگر به ESP32
@socketio.on('switch_command')
def handle_switch_command(data):
    print("📤 فرمان به ESP32:", data)
    emit('control_command', data, broadcast=True)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=10000)
