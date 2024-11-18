#!/usr/bin/env python3
# session_db_auth.py
"""class SessionDBAuth nherits from SessionExpAuth
"""
from .session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from typing import List


class SessionDBAuth(SessionExpAuth):
    """class SessionDBAuth
    """

    def create_session(self, user_id=None):
        """creates and stores new instance of UserSession
        """
        session_id = super().create_session(user_id)
        if session_id:
            user_session = UserSession(user_id=user_id, session_id=session_id)
            user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """returns the User ID by requesting UserSession
        in the database based on session_id
        """
        if session_id is None:
            return None
        if type(session_id) is not str:
            return None
        u_sess = UserSession.search({"session_id": session_id})
        if u_sess:
            return u_sess[0].user_id
        return None

    def destroy_session(self, request=None):
        """destroy_session
        """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        u_sess: List[UserSession] = UserSession.search(
            {"session_id": session_id})
        if u_sess:
            u_sess[0].remove()
            return True
        return False
