from flask import Flask, request, jsonify

app = Flask(__name__)

latest_data = {
    "voltage": "0.00",
    "status": "OFF"
}

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
