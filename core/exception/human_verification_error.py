"""
Error handler for Human Verfication Exception.
"""

from .base import BaseException


class HumanVerificationFailure(BaseException):
    """
    Exception class for Human Verification Failure.
    """
    class Meta:
        base = False