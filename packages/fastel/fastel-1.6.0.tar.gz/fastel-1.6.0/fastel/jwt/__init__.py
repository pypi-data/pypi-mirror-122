# jwt

from .decode_static import decode_static
from .kms_encode import kms_encode as encode

decode = decode_static

__all__ = ["decode", "decode_static", "encode"]
