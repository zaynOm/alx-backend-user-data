#!/usr/bin/env python3
"""Basic auth"""
import base64
from typing import TypeVar

from models.user import User
from .auth import Auth


class BasicAuth(Auth):
    """BasicAuth class"""

    def extract_base64_authorization_header(
        self, authorization_header: str
    ) -> str:
        """Extract the base64 part of the Authorization header"""
        if (
            authorization_header is None
            or not isinstance(authorization_header, str)
            or not authorization_header.startswith("Basic ")
        ):
            return None
        return authorization_header.lstrip("Basic ")

    def decode_base64_authorization_header(
        self, base64_authorization_header: str
    ) -> str:
        """Decode the value of base64 in the Authorization header"""
        if base64_authorization_header is None or not isinstance(
            base64_authorization_header, str
        ):
            return None
        try:
            decoded_header = base64.b64decode(base64_authorization_header)
        except Exception:
            return None
        return decoded_header.decode(errors="ignore")

    def extract_user_credentials(
        self, decoded_base64_authorization_header: str
    ) -> (str, str):
        """Extract credencials from base64"""
        if (
            decoded_base64_authorization_header is None
            or not isinstance(decoded_base64_authorization_header, str)
            or ":" not in decoded_base64_authorization_header
        ):
            return None, None
        return tuple(decoded_base64_authorization_header.split(":", 1))

    def user_object_from_credentials(
        self, user_email: str, user_pwd: str
    ) -> TypeVar("User"):
        """Get the user with the credentials"""
        if user_email is None or type(user_email) is not str:
            return None
        if user_pwd is None or type(user_pwd) is not str:
            return None
        users = User.search({"email": user_email})
        if not users:
            return None
        if User.count() == 0:
            return User(**{"email": user_email, "_password": user_pwd})
        for user in users:
            if user.is_valid_password(user_pwd):
                return user
        return None

    def current_user(self, request=None) -> TypeVar("User"):
        """Overloads the current user"""
        auth_header = self.authorization_header(request)
        decoded_auth_header = self.decode_base64_authorization_header(
            self.extract_base64_authorization_header(auth_header)
        )
        email, pwd = self.extract_user_credentials(decoded_auth_header)
        return self.user_object_from_credentials(email, pwd)
