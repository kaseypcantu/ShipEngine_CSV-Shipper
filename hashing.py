import hashlib
import os
from hmac import compare_digest

from dotenv import load_dotenv

load_dotenv()


def encrypt(pw: bytes) -> str:
    """Takes in a string to be encrypted.

    Args:
        pw (bytes): A string to be encrypted (must be bytes).

    Returns:
        An encrypted hashed string.
    """
    salt = bytes(os.getenv('APP_SALT'), encoding='utf-8')
    iterations = 300000
    dk = hashlib.pbkdf2_hmac('sha512', pw, salt=salt, iterations=iterations)
    return dk.hex()


def compare_hash(digest_a: str, digest_b: str) -> bool:
    """A utility to compare two password digests in a secure way that thwarts
    timing attacks.

    Args:
        digest_a (str): A given hashed value to be compared to another.
        digest_b (str): The hashed value to be compared against digest_a.

    Returns:
        A boolean indicating if digest_a == digest_b.
    """
    return compare_digest(digest_a, digest_b)
