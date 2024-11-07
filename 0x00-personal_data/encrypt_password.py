#!/usr/bin/env python3
# encrypt_password.py
"""Implement a hash_password function that
expects one string argument name password
and returns a salted, hashed password,
which is a byte string.
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """returns a salted, hashed password
    """
    return bcrypt.hashpw(
        password=password.encode('utf-8'),
        salt=bcrypt.gensalt())
