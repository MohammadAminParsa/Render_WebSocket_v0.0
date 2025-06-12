from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# وضعیت دستگاه و ولتاژ آخر
latest_data = {
    "voltage": "0.00",
    "status": "OFF"
}

@app.route('/')
def home():
    # اینجا HTML کامل گذاشته شده بود (که قبلاً فرستادم)
    return render_template("index.html")  # یا جایگزین با return ''' ... '''

@app.route('/upload', methods=['POST'])
def upload():
    global latest_data
    data = request.json
    if data:
        latest_data['voltage'] = data.get('voltage', "0.00")
        latest_data['status'] = data.get('status', "OFF")
        # انتشار داده برای مرورگر
        socketio.emit('voltage', {"voltage": float(latest_data['voltage'])})
        socketio.emit('status', {"status": latest_data['status']})
    return '', 200

@app.route('/control', methods=['GET'])
def control():
    return latest_data['status'], 200

# WebSocket از مرورگر
@socketio.on('control')
def handle_control(data):
    latest_data['status'] = data['status']
    socketio.emit('status', {"status": data['status']})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host='0.0.0.0', port=port)
