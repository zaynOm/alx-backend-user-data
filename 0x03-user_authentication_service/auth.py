#!/usr/bin/env python3
"""Auth stuff"""

import bcrypt


def _hash_password(password: str) -> bytes:
    """Hash password"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
