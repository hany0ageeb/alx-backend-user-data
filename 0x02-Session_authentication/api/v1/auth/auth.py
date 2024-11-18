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
        if '*' in excluded_paths:
            return False
        if not path.endswith('/'):
            path = path + '/'
        if path in excluded_paths:
            return False
        for excluded_path in excluded_paths:
            if excluded_path.endswith('*'):
                if path.startswith(excluded_path[0:len(excluded_path)-1]):
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """that returns None
        Args:
            request: the flas request object
        """
        if not request:
            return None
        auth_header: str = request.headers.get('Authorization', None)
        if auth_header:
            return auth_header.lstrip(' ').rstrip(' ')
        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):  # type: ignore
        """returns None
        Args:
            request: the flas request object
        """
        return None
