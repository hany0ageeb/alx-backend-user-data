#!/usr/bin/env python3
# db.py
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """save the user to the database
        """
        session = self._session
        new_user = User(email=email, hashed_password=hashed_password)
        session.add(new_user)
        session.commit()
        return new_user

    def find_user_by(self, **kwargs):
        """fnd_by_user
        """
        if not kwargs:
            raise InvalidRequestError
        user_keys = ('id', 'email', 'hashed_password',
                     'session_id', 'reset_token')
        for key in kwargs.keys():
            if key not in user_keys:
                raise InvalidRequestError
        user = self._session.query(User).filter_by(**kwargs).first()
        if user is None:
            raise NoResultFound
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """update_user
        """
        user = self.find_user_by(id=user_id)
        user_keys = ('id', 'email', 'hashed_password',
                     'session_id', 'reset_token')
        column_names = User.__table__.columns.keys()
        for key, value in kwargs.items():
            if key not in user_keys:
                self._session.rollback()
                raise ValueError
            else:
                setattr(user, key, value)
        self._session.commit()
