#!/usr/bin/env python3
"""Flask app entry point"""


from flask import Flask, abort, jsonify, redirect, request
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route("/")
def index():
    """Welcome route"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def users():
    """Register a user"""
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400
    return jsonify({"email": email, "message": "user created"})


@app.route("/sessions", methods=["POST"])
def login():
    """Login a user"""
    email = request.form.get("email")
    password = request.form.get("password")
    if not AUTH.valid_login(email, password):
        abort(401)
    session_id = AUTH.create_session(email)
    res = jsonify({"email": email, "message": "logged in"})
    res.set_cookie("session_id", session_id)
    return res


@app.route("/sessions", methods=["DELETE"])
def logout():
    """Logout"""
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect("/")


@app.route("/profile")
def profile():
    """User profile"""
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    return jsonify({"email": user.email})


@app.route("/reset_password", methods=["POST"])
def get_reset_password_token():
    """Get reset password token"""
    email = request.form.get("email")
    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token})
    except ValueError:
        abort(403)


@app.route("/update_password", methods=["PUT"])
def update_password():
    """Update password end-point"""
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")
    try:
        AUTH.update_password(reset_token, new_password)
    except ValueError:
        abort(403)
    return jsonify({"email": email, "message": "Password updated"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
