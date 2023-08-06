"""revtel fastapi package"""

from fastel.authorizers import (
    ClientIdAuth,
    ClientSecretAuth,
    Credential,
    JWBaseAuth,
    StaticClientAuth,
    StaticJWTAuth,
    StaticSecretAuth,
)
from fastel.cart.exceptions import CartException, cart_exception_handler
from fastel.collections import set_collections
from fastel.exceptions import APIException

__version__ = "1.5.0"
__all__ = [
    "APIException",
    "ClientIdAuth",
    "ClientSecretAuth",
    "Credential",
    "JWBaseAuth",
    "StaticClientAuth",
    "StaticSecretAuth",
    "StaticJWTAuth",
    "cart_exception_handler",
    "CartException",
    "set_collections",
]
