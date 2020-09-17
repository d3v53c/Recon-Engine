"""
Base Exception Class Handler.
"""


class BaseException(Exception):
    """
    Base Exception Class Handler for all raised exceptions.
    """
    class Meta:
        base = True