#!/usr/bin/env python3
"""Password hashing and validation"""

import bcrypt
from typing import ByteString


def hash_password(password: str) -> ByteString:
    """Encrypting passwords"""
    return bcrypt.hashpw(str.encode(password), bcrypt.gensalt())
