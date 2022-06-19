import struct
from typing import List
from QQTEA import xxtea
from .tea import encrypt as tea_encrypt
from .tea import decrypt as tea_decrypt

from .xtea import encrypt as xtea_encrypt
from .xtea import decrypt as xtea_decrypt


def bytes2ints(data: bytes, slice_len: int = 4) -> List[int]:
    data = [data[x*slice_len:(x+1)*slice_len]
            for x in range(int(len(data)/slice_len))]
    raw: List[int] = [struct.unpack('<I', i)[0] for i in data]
    return raw


def xxtea_encrypt(data: bytes, key: bytes, delta: int = 0x9e3779b9):
    return __xxtea(data, key, delta, True)


def xxtea_decrypt(data: bytes, key: bytes, delta: int = 0x9e3779b9):
    return __xxtea(data, key, delta, False)


def __xxtea(data: bytes, key: bytes, delta: int = 0x9e3779b9, is_encrypt=True) -> bytes:
    raw_data = bytes2ints(data)
    n: int = len(raw_data)
    if not is_encrypt:
        n = -n
    raw_key = bytes2ints(key)
    r = xxtea.btea(raw_data, raw_key, n, delta)
    r = [struct.pack('<I', x) for x in r]
    return b''.join(r)
