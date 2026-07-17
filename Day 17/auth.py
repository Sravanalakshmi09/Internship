from flask import Blueprint, request, jsonify, session, current_app, redirect
from extensions import db, bcrypt, mail
from models.user import User
from flask_mail import Message
import random

auth_bp = Blueprint("auth", __name__)

# ------------------------
# Register
# ------------------------

@auth_bp.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    fullname = data["fullname"]
    email = data["email"]
    password = data["password"]

    user = User.query.filter_by(email=email).first()

    if user:
        return jsonify({
            "success": False,
            "message": "Email already exists."
        })

    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

    new_user = User(
        fullname=fullname,
        email=email,
        password=hashed_password
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Registration Successful"
    })

# ------------------------
# Login
# ------------------------

@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    email = data["email"]
    password = data["password"]

    user = User.query.filter_by(email=email).first()

    if user and bcrypt.check_password_hash(user.password, password):

        session["user_id"] = user.id
        session["user_name"] = user.fullname

        return jsonify({
            "success": True,
            "message": "Login Successful"
        })

    return jsonify({
        "success": False,
        "message": "Invalid Email or Password"
    })

# ------------------------
# Logout
# ------------------------

@auth_bp.route("/logout")
def logout():
    session.clear()

    return redirect('/login')

# ------------------------
# Forgot Password
# ------------------------

@auth_bp.route("/forgot-password", methods=["POST"])
def forgot_password():

    data = request.get_json()

    email = data["email"]

    user = User.query.filter_by(email=email).first()

    if not user:

        return jsonify({
            "success": False,
            "message": "Email not found"
        })

    otp = str(random.randint(100000,999999))

    user.otp = otp

    db.session.commit()

    msg = Message(
        "SignalSense Password Reset OTP",
        sender=current_app.config["MAIL_USERNAME"],
        recipients=[email]
    )

    msg.body = f"Your OTP is {otp}"

    try:
        mail.send(msg)
    except Exception as error:
        return jsonify({
            "success": False,
            "message": "Failed to send OTP. Check email configuration and app permissions."
        }), 500

    return jsonify({
        "success": True,
        "message": "OTP Sent"
    })

# ------------------------
# Reset Password
# ------------------------

@auth_bp.route("/reset-password", methods=["POST"])
def reset_password():

    data = request.get_json()

    email = data["email"]

    otp = data["otp"]

    password = data["password"]

    user = User.query.filter_by(

        email=email,

        otp=otp

    ).first()

    if not user:

        return jsonify({

            "success": False,

            "message": "Invalid OTP"

        })

    user.password = bcrypt.generate_password_hash(password).decode("utf-8")

    user.otp = None

    db.session.commit()

    return jsonify({

        "success": True,

        "message": "Password Updated"

    })
    