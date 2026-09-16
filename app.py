from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def health():
    return jsonify({"status": "VoxBridge is live", "mode": "maintenance"})

@app.route('/transcribe', methods=['POST'])
def transcribe():
    # TODO: replace with real Whisper + IndicTrans2 pipeline
    return jsonify({
        "status": "maintenance",
        "message": "Model pipeline is being finalized. Check back soon.",
        "hindi": None,
        "english": None
    }), 503

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
