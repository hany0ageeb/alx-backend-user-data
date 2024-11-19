#!/usr/bin/env python3
# auth.py
"""define a _hash_password method that takes in
a password string arguments and returns bytes.
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.exc import NoResultFound


def _generate_uuid() -> str:
    """generate_uuid"""
    return str(uuid.uuid4())


def _hash_password(password: str) -> bytes:
    """_hash_password
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """__init__
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """register_user
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                raise ValueError('User {} already exists'.format(email))
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))

    def valid_login(self, email: str, password: str) -> bool:
        """Expect email and password required arguments
        Returns a boolean
        """
        try:
            user = self._db.find_user_by(email=email)
            if bcrypt.checkpw(password.encode('utf-8'), user.hashed_password):
                return True
        except NoResultFound:
            return False
        return False
