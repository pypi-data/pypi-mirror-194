"""

CryptoHash utils

"""
from typing import Any

from Crypto.Hash import SHA3_256


def hash_sha3_256(data: Any) -> str:
    if isinstance(data, str):
        data = data.encode('utf-8')

    messageDigest = SHA3_256.new()
    messageDigest.update(data)
    return messageDigest.hexdigest()
