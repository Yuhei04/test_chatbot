from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, this is a simple Flask app for testing!"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print("Received webhook event:", data)
    return jsonify({"status": "success"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
