import requests
from flask import Flask, jsonify, request
from prometheus_client import Counter, generate_latest
from prometheus_client import CONTENT_TYPE_LATEST

app = Flask(__name__)

VERSION = "v1"

AUTH_SERVICE_URL = "http://auth-service:5000"
BALANCE_SERVICE_URL = "http://balance-service:5001"


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
    
    try:
        auth_response = requests.get(
            f"{AUTH_SERVICE_URL}/health",
            timeout=5
        )

        if auth_response.status_code != 200:
            return jsonify({
                "status": "failed",
                "message": "Auth service is unavailable"
            }), 503
        
        balance_response = requests.get(
            f"{BALANCE_SERVICE_URL}/balance",
            timeout=5
        )

        balance_data = balance_response.json()

        current_balance = balance_data["balance"]

        data = request.get_json() or {}

        amount = data.get("amount", 0)

        if amount > current_balance:
            return jsonify({
                "status": "failed",
                "message": "Insufficient funds"
            }), 400
        
        return jsonify({
            "status": "success",
            "message": "Transfer completed successfully",
            "remaining_balance": current_balance - amount
        })  

    except Exception as e:
        return jsonify({
            "status": "failed",
            "message": str(e)
        }), 500


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