#!/usr/bin/env python3
# basic_auth.py
"""class BasicAuth that inherits from Auth
"""
from .auth import Auth


class BasicAuth(Auth):
    """class BasicAuth
    """

    def extract_base64_authorization_header(
            self,
            authorization_header: str) -> str:
        """extract_base64_authorization_header
        """
        if authorization_header is None:
            return None
        if type(authorization_header) is not str:
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header.removeprefix('Basic ')
