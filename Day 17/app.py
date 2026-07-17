from flask import Flask, render_template, request, session, redirect, jsonify
from extensions import db, bcrypt, mail
from models.user import User
from models.prediction import Prediction
from routes.auth import auth_bp
from routes.prediction import prediction_bp
from routes.history import history_bp
import os

app = Flask(__name__)

# ----------------------------
# Configuration
# ----------------------------
app.config["SECRET_KEY"] = "signalsense_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///signalsense.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.environ.get(
    "MAIL_USERNAME",
    "shiningvibes07@gmail.com"
)
app.config["MAIL_PASSWORD"] = os.environ.get(
    "MAIL_PASSWORD",
    "123456"
)
app.config["MAIL_DEFAULT_SENDER"] = app.config["MAIL_USERNAME"]

# ----------------------------
# Initialize Extensions
# ----------------------------
db.init_app(app)
bcrypt.init_app(app)
mail.init_app(app)

# ----------------------------
# Register Blueprints
# ----------------------------
app.register_blueprint(auth_bp)
app.register_blueprint(prediction_bp)
app.register_blueprint(history_bp)

with app.app_context():
    db.create_all()

# ----------------------------
# Dashboard API
# ----------------------------
@app.route("/dashboard-data")
def dashboard_data():

    if "user_id" not in session:
        return jsonify({
            "success": False,
            "error": "Not logged in"
        })

    try:
        user_id = session["user_id"]

        total = Prediction.query.filter_by(
            user_id=user_id
        ).count()

        normal = Prediction.query.filter_by(
            user_id=user_id,
            prediction="Normal"
        ).count()

        anomalies = Prediction.query.filter_by(
            user_id=user_id,
            prediction="Anomaly"
        ).count()

        return jsonify({
            "success": True,
            "total": total,
            "normal": normal,
            "anomalies": anomalies
        })

    except Exception as e:
        print(e)
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# ----------------------------
# Pages
# ----------------------------
@app.route("/")
def home_page():
    return render_template("index.html")


@app.route("/login")
def login_page():
    return render_template("login.html")


@app.route("/register")
def register_page():
    return render_template("register.html")


@app.route("/forgot-password")
def forgot_password_page():
    return render_template("forgot_password.html")


@app.route("/dashboard")
def dashboard_page():

    if "user_id" not in session:
        return redirect("/login")

    return render_template("dashboard.html")


@app.route("/prediction")
def prediction_page():

    if "user_id" not in session:
        return redirect("/login")

    return render_template("prediction.html")


@app.route("/history")
def history_page():

    if "user_id" not in session:
        return redirect("/login")

    return render_template("history.html")


@app.route("/profile")
def profile():

    if "user_id" not in session:
        return redirect("/login")

    return render_template("profile.html")

# ----------------------------
# Update Profile
# ----------------------------
@app.route("/update-profile", methods=["POST"])
def update_profile():

    if "user_id" not in session:
        return jsonify(success=False)

    data = request.json

    user = User.query.get(session["user_id"])

    if not user:
        return jsonify(success=False)

    user.name = data["name"]

    from werkzeug.security import generate_password_hash

    if data["password"] != "":
        user.password = generate_password_hash(data["password"])

    db.session.commit()

    session["user_name"] = user.name

    return jsonify(success=True)

# ----------------------------
# Run
# ----------------------------
if __name__ == "__main__":
    app.run(debug=True)