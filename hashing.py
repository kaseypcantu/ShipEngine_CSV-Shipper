import hashlib
import os
from hmac import compare_digest

from dotenv import load_dotenv

load_dotenv()


def encrypt(pw: bytes) -> str:
    """
    Takes in a string to be encrypted.

    :param pw: A string to be encrypted (must be bytes).
    :return: An encrypted hashed string.
    """
    salt = bytes(os.getenv('APP_SALT'), encoding='utf-8')
    iterations = 300000
    dk = hashlib.pbkdf2_hmac('sha512', pw, salt=salt, iterations=iterations)
    return dk.hex()


# enc = encrypt(b'test')
# print(enc)
# print(type(enc))


def compare_hash(digest_a: str, digest_b: str) -> bool:
    """
    A utility to compare two password digests in a secure way that
    thwarts timing attacks.

    :param digest_a: A given hashed value to be compared to another.
    :param digest_b: The hashed value to be compared against digest_a.
    :return: A boolean indicating if digest_a == digest_b.
    """
    return compare_digest(digest_a, digest_b)
