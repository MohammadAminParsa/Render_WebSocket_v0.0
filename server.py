from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # فعال‌سازی CORS برای اتصال ESP32
socketio = SocketIO(app, cors_allowed_origins="*")

# داده‌ی ولتاژ از ESP32 دریافت و به مرورگر broadcast می‌شود
@socketio.on('esp_data')
def handle_esp_data(data):
    print("📥 ولتاژ دریافتی از ESP32:", data)
    emit('update_voltage', data, broadcast=True)

# دستور روشن/خاموش از مرورگر گرفته و برای ESP32 ارسال می‌شود
@socketio.on('switch_command')
def handle_switch_command(data):
    print("📤 ارسال دستور به ESP32:", data)
    emit('control_command', data, broadcast=True)

@app.route('/')
def index():
    return "سرور WebSocket برای مانیتورینگ اینورتر آماده است."

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
