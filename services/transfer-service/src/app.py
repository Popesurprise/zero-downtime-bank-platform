from flask import Flask, jsonify, request
from prometheus_client import Counter, generate_latest
from prometheus_client import CONTENT_TYPE_LATEST

app = Flask(__name__)

VERSION = "v1"

REQUEST_COUNT = Counter(
    "transfer_requests_total",
    "Total Transfer Requests"
)


@app.route("/")
def home():
    REQUEST_COUNT.inc()

    return jsonify({
        "service": "transfer-service"
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


@app.route("/transfer", methods=["POST"])
def transfer():

    REQUEST_COUNT.inc()

    data = request.get_json() or {}

    from_account = data.get("from_account")
    to_account = data.get("to_account")
    amount = data.get("amount")

    return jsonify({
        "status": "success",
        "from_account": from_account,
        "to_account": to_account,
        "amount": amount
    })


@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {
        "Content-Type": CONTENT_TYPE_LATEST
    }


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5002
    )