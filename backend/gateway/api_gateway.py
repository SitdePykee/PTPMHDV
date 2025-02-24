from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Định nghĩa địa chỉ các microservices
SERVICE_URLS = {
    "production_planning": "http://localhost:5001",
    "material_management": "http://localhost:5002",
    "production_control": "http://localhost:5003",
    "quality_management": "http://localhost:5004"
}

def forward_request(service, endpoint):
    url = f"{SERVICE_URLS[service]}{endpoint}"
    response = requests.request(
        method=request.method,
        url=url,
        headers={key: value for key, value in request.headers if key != 'Host'},
        json=request.get_json()
    )
    return jsonify(response.json()), response.status_code

@app.route("/api/production_planning/<path:endpoint>", methods=["GET", "POST", "PUT", "DELETE"])
def production_planning_proxy(endpoint):
    return forward_request("production_planning", f"/{endpoint}")

@app.route("/api/material_management/<path:endpoint>", methods=["GET", "POST", "PUT", "DELETE"])
def material_management_proxy(endpoint):
    return forward_request("material_management", f"/{endpoint}")

@app.route("/api/production_control/<path:endpoint>", methods=["GET", "POST", "PUT", "DELETE"])
def production_control_proxy(endpoint):
    return forward_request("production_control", f"/{endpoint}")

@app.route("/api/quality_management/<path:endpoint>", methods=["GET", "POST", "PUT", "DELETE"])
def quality_management_proxy(endpoint):
    return forward_request("quality_management", f"/{endpoint}")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
