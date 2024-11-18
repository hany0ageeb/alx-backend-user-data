#!/usr/bin/env python3
# user_session.py
"""user_sesson
"""
from models.base import Base


class UserSession(Base):
    """class UserSession
    """

    def __init__(self, *args: list, **kwargs: dict):
        """__nt__
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
