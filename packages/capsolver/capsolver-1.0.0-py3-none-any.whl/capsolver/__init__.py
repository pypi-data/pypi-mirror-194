import os

from capsolver.capsolver import (
    RecognitionTask,
    TokenTask,
    Balance,
)
from capsolver.error import CapsolverError, InvalidRequestError, IncompleteJobError, RateLimitError, AuthenticationError, InsufficientCreditError, UnknownError, Timeout, APIError, ServiceUnavailableError

api_base = os.environ.get("CAPSOLVER_API_BASE", "https://api.capsolver.com")
api_key = os.environ.get("CAPSOLVER_API_KEY")
proxy = None


__all__ = [
    "RecognitionTask",
    "TokenTask",
    "Balance",

    "CAPSOLVERError",
    "InvalidRequestError",
    "IncompleteJobError",
    "RateLimitError",
    "AuthenticationError",
    "InsufficientCreditError",
    "UnknownError",
    "Timeout",
    "APIError",
    "ServiceUnavailableError",

    "api_base",
    "api_key",
    "proxy",
]
