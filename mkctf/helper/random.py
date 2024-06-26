"""Random helper
"""

from os import urandom


def randbytes(size: int) -> bytes:
    """Provide size random bytes"""
    return urandom(size)


def randhex(size: int) -> str:
    """Provide size random hex-encoded bytes"""
    return randbytes(size).hex()
