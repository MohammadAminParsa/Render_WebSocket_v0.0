from flask import Flask, request, jsonify

app = Flask(__name__)

latest_data = {}

@app.route('/upload', methods=['POST'])
def upload():
    global latest_data
    latest_data = request.json
    return '', 200

@app.route('/latest', methods=['GET'])
def latest():
    return jsonify(latest_data)

@app.route('/')
def root():
    return "<h3>ESP32 Server is Online ✅</h3>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
