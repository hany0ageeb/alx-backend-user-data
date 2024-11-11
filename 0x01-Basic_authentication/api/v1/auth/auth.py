#!/usr/bin/env python3
# auth.py
"""a class to manage the API authentication.
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """Auth class to manage
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """returns False
        """
        if path is None:
            return True
        if not excluded_paths:
            return True
        if not path.endswith('/'):
            path = path + '/'
        if path in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """that returns None
        Args:
            request: the flas request object
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):  # type: ignore
        """returns None
        Args:
            request: the flas request object
        """
        return None
