from flask import Blueprint, jsonify, session
from extensions import db
from models.prediction import Prediction

history_bp = Blueprint("history", __name__)

# ------------------------------------
# Get Prediction History
# ------------------------------------

@history_bp.route("/api/history", methods=["GET"])
def get_history():

    if "user_id" not in session:

        return jsonify({
            "success": False,
            "message": "Please login first."
        }), 401

    predictions = Prediction.query.filter_by(
        user_id=session["user_id"]
    ).order_by(
        Prediction.created_at.desc()
    ).all()

    history = []

    for item in predictions:

        history.append({

            "id": item.id,

            "device_id": item.device_id,

            "temperature": item.temperature,

            "humidity": item.humidity,

            "battery_level": item.battery_level,

            "prediction": item.prediction,

            "confidence": item.confidence,

            "created_at": item.created_at.strftime(
                "%d-%m-%Y %I:%M %p"
            )

        })

    return jsonify({
        "success": True,
        "history": history
    })


# ------------------------------------
# Delete Prediction
# ------------------------------------

@history_bp.route("/api/history/delete/<int:id>", methods=["DELETE"])
def delete_prediction(id):

    if "user_id" not in session:

        return jsonify({
            "success": False,
            "message": "Please login first."
        }), 401

    prediction = Prediction.query.filter_by(
        id=id,
        user_id=session["user_id"]
    ).first()

    if prediction is None:

        return jsonify({
            "success": False,
            "message": "Prediction not found."
        }), 404

    db.session.delete(prediction)

    db.session.commit()

    return jsonify({

        "success": True,

        "message": "Prediction deleted successfully."

    })


# ------------------------------------
# Delete All History
# ------------------------------------

@history_bp.route("/api/history/delete-all", methods=["DELETE"])
def delete_all_history():

    if "user_id" not in session:

        return jsonify({
            "success": False,
            "message": "Please login first."
        }), 401

    Prediction.query.filter_by(
        user_id=session["user_id"]
    ).delete()

    db.session.commit()

    return jsonify({

        "success": True,

        "message": "All history deleted."

    })