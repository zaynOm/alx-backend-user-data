#!/usr/bin/env python3
"""Authentication template"""
from typing import List, TypeVar
from flask import request


class Auth:
    """Auth class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Check if auth is required"""
        if path is None or not excluded_paths:
            return True
        path = path if path.endswith("/") else path + "/"
        for ep in excluded_paths:
            if ep.endswith("*") and ep[:-1] in path:
                return False

        return path not in excluded_paths

    def authorization_header(self, request=None) -> str:
        """Extract the authorization header"""
        if request is None:
            return None
        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar("User"):
        """Get the current user"""
        return None
