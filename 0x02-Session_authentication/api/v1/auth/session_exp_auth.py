#!/usr/bin/env python3
# session_exp_auth.py
"""Create a class SessionExpAuth that inherits from SessionAuth
"""
from .session_auth import SessionAuth
from datetime import datetime, timedelta
from os import getenv


class SessionExpAuth(SessionAuth):
    """class SessionExpAuth
    """

    def __init__(self):
        super().__init__()
        SESSION_DURATION = getenv('SESSION_DURATION', '0')
        try:
            self.session_duration = int(SESSION_DURATION)
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """overload create_sesson
        """
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        self.user_id_by_session_id[session_id] = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """user_id_for_session_id
        """
        if session_id is None:
            return None
        if session_id not in self.user_id_by_session_id:
            return None
        session_dict: dict = self.user_id_by_session_id[session_id]
        if self.session_duration <= 0:
            return session_dict['user_id']
        if 'created_at' not in session_dict:
            return None
        created_at: datetime = session_dict['created_at']
        if datetime.now() > created_at\
                + timedelta(seconds=self.session_duration):
            return None
        return session_dict['user_id']
