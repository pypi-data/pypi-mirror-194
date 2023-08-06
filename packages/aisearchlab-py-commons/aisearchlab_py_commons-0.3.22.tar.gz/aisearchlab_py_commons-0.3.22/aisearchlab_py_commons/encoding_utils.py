"""
Simple xor-based string encoder / decoder
"""
from base64 import b64encode, b64decode

from passlib.context import LazyCryptContext
from passlib.utils import sys_bits


def xor_crypt_encode(data: str) -> str:
    """
    XORs each input string character with it's position module 256
    :param data: input string
    :return: encoded data
    """
    base64 = b64encode(data.encode('utf-8')).decode('utf-8').strip('=')
    return ''.join(chr((i % 256) ^ ord(c))
                   for (i, c) in enumerate(base64))


def xor_crypt_decode(data: str) -> str:
    """
    XORs each input string character with it's position module 256,
    decodes result as base64
    :param data: input string
    :return: decoded data
    """
    return b64decode(''.join(chr((i % 256) ^ ord(c))
                             for (i, c) in enumerate(data)))


def xor_crypt_decode_reverse(data: str) -> str:
    """
    XORs each decoded input string character with it's
    position module 256
    :param data: input string in base64
    :return: decoded data
    """
    decoded = b64decode(data)
    return ''.join(chr((i % 256) ^ c) for (i, c) in enumerate(decoded))


pwd_context = LazyCryptContext(
    # choose some reasonbly strong schemes
    schemes=["sha512_crypt", "sha256_crypt"],

    # set some useful global options
    default="sha256_crypt" if sys_bits < 64 else "sha512_crypt",

    # Keep the number of rounds short, for a quicker-to-be-checked key
    sha512_crypt__max_rounds=1000,
    sha256_crypt__max_rounds=1000,
    sha512_crypt__min_rounds=1000,
    sha256_crypt__min_rounds=1000,
)


def encrypt_pass(passwd: str):
    """
    Securely hashes password
    :param passwd:
    :return:
    """
    return pwd_context.encrypt(passwd)
