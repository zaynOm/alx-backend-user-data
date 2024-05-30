#!/usr/bin/env python3
"""End-to-end integration test"""
import requests

BASE_URL = "http://localhost:5000"


def register_user(email: str, password: str) -> None:
    """Register a user"""
    res = requests.post(
        f"{BASE_URL}/users", {"email": email, "password": password}
    )
    assert res.status_code == 200
    assert res.json() == {"email": email, "message": "user created"}


def log_in_wrong_password(email: str, password: str) -> None:
    """Login using wrong password"""
    res = requests.post(
        f"{BASE_URL}/sessions", {"email": email, "password": password}
    )
    assert res.status_code == 401


def log_in(email: str, password: str) -> str:
    """Login the user"""
    res = requests.post(
        f"{BASE_URL}/sessions", {"email": email, "password": password}
    )
    assert res.status_code == 200
    assert res.json() == {"email": email, "message": "logged in"}
    return res.cookies.get("session_id")


def profile_unlogged() -> None:
    """unlogged profile"""
    res = requests.get(f"{BASE_URL}/profile")
    assert res.status_code == 403


def profile_logged(session_id: str) -> None:
    """logged profile"""
    res = requests.get(
        f"{BASE_URL}/profile", cookies={"session_id": session_id}
    )
    assert res.status_code == 200
    assert res.json() == {"email": EMAIL}


def log_out(session_id: str) -> None:
    """Logout"""
    res = requests.delete(
        f"{BASE_URL}/sessions", cookies={"session_id": session_id}
    )

    assert res.status_code == 200
    assert res.json() == {"message": "Bienvenue"}


def reset_password_token(email: str) -> str:
    """Reset user password"""
    res = requests.post(f"{BASE_URL}/reset_password", {"email": email})
    assert res.status_code == 200
    return res.json().get("reset_token")


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Update user password"""
    res = requests.put(
        f"{BASE_URL}/reset_password",
        {
            "email": email,
            "reset_token": reset_token,
            "new_password": new_password,
        },
    )

    assert res.status_code == 200
    assert res.json() == {"email": email, "message": "Password updated"}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
