from flask import Flask, jsonify

app = Flask(__name__)

VERSION = "v1"

@app.route("/")
def home():
    return jsonify({
        "service": "auth-service",
        "status": "running"
    })

@app.route("/health")
def health():
    return jsonify({
        "status": "healthy"
    })

@app.route("/version")
def version():
    return jsonify({
        "version": VERSION
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)