from flask import Blueprint, request, jsonify, session
from extensions import db
from models.prediction import Prediction

import joblib
import numpy as np
import os

prediction_bp = Blueprint("prediction", __name__)

# -----------------------------
# Load ML Model Lazily
# -----------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "ml",
    "signalsense_logistic_randomsearch_model.pkl"
)

SCALER_PATH = os.path.join(
    BASE_DIR,
    "ml",
    "signalsense_scaler.pkl"
)

model = None
scaler = None


def load_model():
    global model, scaler

    if model is not None and scaler is not None:
        return True

    if not os.path.exists(MODEL_PATH) or not os.path.exists(SCALER_PATH):
        return False

    if os.path.getsize(MODEL_PATH) == 0 or os.path.getsize(SCALER_PATH) == 0:
        return False

    try:
        model = joblib.load(MODEL_PATH)
        scaler = joblib.load(SCALER_PATH)
        return True
    except Exception:
        model = None
        scaler = None
        return False


# -----------------------------
# Prediction Route
# -----------------------------

@prediction_bp.route("/predict", methods=["POST"])
def predict():

    if "user_id" not in session:

        return jsonify({
            "success": False,
            "message": "Please login first."
        }), 401

    if not load_model():
        return jsonify({
            "success": False,
            "message": "Prediction model not available."
        }), 500

    data = request.get_json()

    device_id = data["device_id"]

    temperature = float(data["temperature"])

    humidity = float(data["humidity"])

    battery = float(data["battery_level"])

    features = np.array([
        [
            temperature,
            humidity,
            battery
        ]
    ])

    scaled = scaler.transform(features)

    prediction = model.predict(scaled)[0]

    probabilities = model.predict_proba(scaled)[0]

    confidence = round(
        float(np.max(probabilities) * 100),
        2
    )

    # Convert prediction to text
    if prediction == 1:
        prediction_text = "Anomaly"
    else:
        prediction_text = "Normal"

    # Save to SQLite

    history = Prediction(

        user_id=session["user_id"],

        device_id=device_id,

        temperature=temperature,

        humidity=humidity,

        battery_level=battery,

        prediction=prediction_text,

        confidence=confidence

    )

    db.session.add(history)

    db.session.commit()

    return jsonify({

        "success": True,

        "device_id": device_id,

        "prediction": prediction_text,

        "confidence": confidence

    })