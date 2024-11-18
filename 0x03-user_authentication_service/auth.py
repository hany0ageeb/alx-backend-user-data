#!/usr/bin/env python3
# auth.py
"""define a _hash_password method that takes in
a password string arguments and returns bytes.
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """_hash_password
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
