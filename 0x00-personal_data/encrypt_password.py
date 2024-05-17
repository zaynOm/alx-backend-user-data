#!/usr/bin/env python3
"""Password hashing and validation"""

import bcrypt


def hash_password(password: str) -> bytes:
    """Encrypting passwords"""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Check valid password"""
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password)
