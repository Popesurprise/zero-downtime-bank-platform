from flask import Flask, jsonify
from prometheus_client import Counter, generate_latest
from prometheus_client import CONTENT_TYPE_LATEST

app = Flask(__name__)

VERSION = "v1"

REQUEST_COUNT = Counter(
    "balance_requests_total",
    "Total Balance Requests"
)

@app.route("/")
def home():
    REQUEST_COUNT.inc()

    return jsonify({
        "service": "balance-service"
    })

@app.route("/health")
def health():
    REQUEST_COUNT.inc()

    return jsonify({
        "status": "healthy"
    })

@app.route("/version")
def version():
    REQUEST_COUNT.inc()

    return jsonify({
        "version": VERSION
    })

@app.route("/balance")
def balance():
    REQUEST_COUNT.inc()

    return jsonify({
        "account_id": "123456",
        "balance": 5000
    })

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {
        "Content-Type": CONTENT_TYPE_LATEST
    }

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5001
    )