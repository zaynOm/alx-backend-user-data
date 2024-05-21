#!/usr/bin/env python3
"""Authentication template"""
from flask import request


class Auth:
"""Auth class"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
       """Check if auth is required""" 
        return False

    def authorization_header(self, request=None) -> str:
        """Extract the authorization header"""
        return None


    def current_user(self, request=None) -> TypeVar("User"):
        """Get the current user"""
        return None
