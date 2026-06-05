from flask import Flask, jsonify, request
from prometheus_client import Counter, generate_latest
from prometheus_client import CONTENT_TYPE_LATEST

app = Flask(__name__)

VERSION = "v1"

REQUEST_COUNT = Counter(
    "auth_requests_total",
    "Total Auth Service Requests"
)


@app.route("/")
def home():
    REQUEST_COUNT.inc()

    return jsonify({
        "service": "auth-service",
        "status": "running"
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


@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {
        "Content-Type": CONTENT_TYPE_LATEST
    }

@app.route("/login", methods=["POST"])
def login():

    REQUEST_COUNT.inc()

    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    if username == "admin" and password == "password":
        return jsonify({
            "message": "login successful"
        })

    return jsonify({
        "message": "invalid credentials"
    }), 401


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )