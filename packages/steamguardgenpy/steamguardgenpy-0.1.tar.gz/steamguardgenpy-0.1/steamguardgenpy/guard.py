from time import time
from hashlib import sha1
from base64 import b64decode
from struct import pack, unpack
from hmac import new as hmac


def gen_two_factor_code(shared_secret: str, timestamp: int = None) -> str:
    """Generate steam twofactor (onetime/TOTP) code."""

    if timestamp is None:
        timestamp = int(time())
    _hmac = hmac(b64decode(shared_secret), pack(">Q", timestamp // 30), sha1).digest()
    start = ord(_hmac[19:20]) & 0xF
    full_code = unpack(">I", _hmac[start:start+4])[0] & 0x7FFFFFFF
    
    chars = "23456789BCDFGHJKMNPQRTVWXY"
    code = ""

    for _ in range(5):
        full_code, i = divmod(full_code, len(chars))
        code += chars[i]

    return code
