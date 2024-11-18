#!/usr/bin/env python3
# session_auth.py
"""class SessionAuth that inherits from Auth
Create a class attribute user_id_by_session_id
initialized by an empty dictionary
"""
from .auth import Auth
import uuid


class SessionAuth(Auth):
    """class SessionAuth
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """creates a Session ID for a user_id
        """
        if user_id is None:
            return None
        if type(user_id) is not str:
            return None
        session_id: str = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id
