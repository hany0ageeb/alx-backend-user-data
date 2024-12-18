#!/usr/bin/env python3
# basic_auth.py
"""class BasicAuth that inherits from Auth
"""
import binascii
from .auth import Auth
from typing import TypeVar
import base64


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
        return authorization_header[len('Basic '):]

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str) -> str:
        """decode_base64_authorization_header
        """
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) is not str:
            return None
        try:
            return base64.b64decode(
                base64_authorization_header).decode('utf-8')
        except binascii.Error:
            return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str) -> (str, str):
        """extract_user_credentials
        """
        if decoded_base64_authorization_header is None:
            return (None, None)
        if type(decoded_base64_authorization_header) is not str:
            return (None, None)
        idx = decoded_base64_authorization_header.find(':')
        if idx == -1:
            return (None, None)
        return (decoded_base64_authorization_header[0:idx],
                decoded_base64_authorization_header[idx+1:])

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str) -> TypeVar('User'):  # type: ignore
        """user_object_from_credentials
        """
        from models.user import User
        if user_email is None or type(user_email) is not str:
            return None
        if user_pwd is None or type(user_pwd) is not str:
            return None
        users = User.search({"email": user_email})
        if users:
            for user in users:
                if user.is_valid_password(user_pwd):
                    return user
            return None
        return None

    def current_user(self, request=None) -> TypeVar('User'):  # type: ignore
        """current_user
        """
        auth_header = self.authorization_header(request)
        b64_auth_header = self.extract_base64_authorization_header(auth_header)
        dec_b64_auth_header = self.decode_base64_authorization_header(
            b64_auth_header)
        u_mal, u_pwd = self.extract_user_credentials(dec_b64_auth_header)
        return self.user_object_from_credentials(u_mal, u_pwd)
