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
