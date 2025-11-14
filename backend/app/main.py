from flask import Flask, request, jsonify
from flask_cors import CORS
from app.utils.predict import predict_fraud

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Fraud Detection API is Running!"})

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json
        result = predict_fraud(data)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
