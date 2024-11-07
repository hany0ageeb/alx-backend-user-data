#!/usr/bin/env python3
# filtered_logger.py
"""
Write a function called filter_datum that returns the log message obfuscated:
Arguments:
    - fields: a list of strings representing all fields to obfuscate
    - redaction: a string representing by what the field will be obfuscated
    - message: a string representing the log line
    - separator: a string representing by which
    character is separating all fields in the log line (message)
    - The function should use a regex to replace occurrences
    of certain field values.
    - filter_datum should be less than 5 lines long
    and use re.sub to perform the substitution with a single regex.
"""
from typing import List
import re
import logging
import os
import mysql.connector


PII_FIELDS = ("name", "email", "password", "ssn", "phone")


def filter_datum(
        fields: List[str],
        redaction: str,
        message: str,
        separator: str) -> str:
    """returns the log message obfuscated
    Args:
        fields: list of strings representing all fields to obfuscate
    """
    for field in fields:
        message = re.sub(r'{}=.+?{}'.format(field, separator),
                         f'{field}={redaction}{separator}', message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """format
        """
        record.msg = filter_datum(
            self.fields, self.REDACTION, record.msg, self.SEPARATOR)
        formatter = logging.Formatter(self.FORMAT)
        return formatter.format(record)


def get_logger() -> logging.Logger:
    """get_logger
    """
    logger = logging.getLogger('user_data')
    logger.propagate = False
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    logger.addHandler(handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ returns a connector to the database
    """
    cnx = mysql.connector.connect(
        user=os.getenv('PERSONAL_DATA_DB_USERNAME', 'root'),
        password=os.getenv('PERSONAL_DATA_DB_PASSWORD', ''),
        host=os.getenv('PERSONAL_DATA_DB_HOST', 'localhost'),
        database=os.getenv('PERSONAL_DATA_DB_NAME')
    )
    return cnx


def main() -> None:
    """entry point
    """
    logger = get_logger()
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        ('SELECT name,'
         ' email,'
         ' phone,'
         ' ssn,'
         ' password,'
         ' ip,'
         ' last_login,'
         ' user_agent'
         ' FROM users'))
    for (name,
         email,
         phone,
         ssn,
         password,
         ip,
         last_login,
         user_agent) in cursor:
        message = (f'name={name};'
                   f'email={email};'
                   f'phone={phone};'
                   f'ssn={ssn};'
                   f'password={password};'
                   f'ip={ip};'
                   f'last_login={last_login};'
                   f'user_agent={user_agent}')
        logger.log(logging.INFO, message)
    cursor.close()
    db.close()


if __name__ == '__main__':
    main()
