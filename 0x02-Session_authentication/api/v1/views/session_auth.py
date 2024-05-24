#!/usr/bin/env python3
"""Module for session auth views"""


from os import getenv
from api.v1.views import app_views
from flask import abort, jsonify, request

from models.user import User


@app_views.route("/auth_session/login", methods=["POST"], strict_slashes=False)
def login():
    """Login using session auth"""
    email = request.form.get("email")
    password = request.form.get("password")

    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400
    try:
        users = User.search({"email": email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404
    if not users:
        return jsonify({"error": "no user found for this email"}), 404

    current_user = None
    for user in users:
        if user.is_valid_password(password):
            current_user = user
    if not current_user:
        return jsonify({"error": "wrong password"}), 401
    from api.v1.app import auth

    session_id = auth.create_session(current_user.id)
    session_name = getenv("SESSION_NAME")
    res = jsonify(current_user.to_json())
    res.set_cookie(session_name, session_id)
    return res
