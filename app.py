from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return render_template('index.html')

# دریافت داده از ESP32
@socketio.on('esp_data')
def handle_esp_data(data):
    print("Data from ESP32:", data)
    socketio.emit('new_data', data)

# دریافت دستور از مرورگر و ارسال به ESP32
@socketio.on('command')
def handle_command(data):
    print("Command from browser:", data)
    socketio.emit('to_esp', data)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
