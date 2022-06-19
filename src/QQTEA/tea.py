from ctypes import *
import struct
from typing import List, Tuple
from .Constance import magic_number_delta as delta


def encrypt(v, k: List[int], run_round: int = 32):
    v0 = c_uint32(v[0])
    v1 = c_uint32(v[1])
    sum1 = c_uint32(0)
    for i in range(run_round):
        sum1.value += delta
        v0.value += ((v1.value << 4) +
                     k[0]) ^ (v1.value+sum1.value) ^ ((v1.value >> 5)+k[1])
        v1.value += ((v0.value << 4) +
                     k[2]) ^ (v0.value+sum1.value) ^ ((v0.value >> 5)+k[3])
    return v0.value, v1.value


def decrypt(v, k: List[int], run_round: int = 32):
    v0 = c_uint32(v[0])
    v1 = c_uint32(v[1])
    sum1 = c_uint32(delta * run_round)
    for i in range(run_round):
        v1.value -= ((v0.value << 4) +
                     k[2]) ^ (v0.value+sum1.value) ^ ((v0.value >> 5)+k[3])
        v0.value -= ((v1.value << 4) +
                     k[0]) ^ (v1.value+sum1.value) ^ ((v1.value >> 5)+k[1])
        sum1.value -= delta
    return v0.value, v1.value


def custom_encode_or_decode(v: Tuple = [1, 2]) -> Tuple:
    run_round = 32
    delta = 0x61C88647

    v0 = c_uint32(v[0])
    v1 = c_uint32(v[1])
    sum1 = c_uint32(0)
    for i in range(run_round):
        v1.value -= ((v0.value << 3) + 86) ^ (v0.value +
                                              sum1.value) ^ ((v0.value >> 5)+120)
        v0.value -= ((v1.value << 3) + 18) ^ (v1.value +
                                              sum1.value) ^ ((v1.value >> 5)+52)
        sum1.value += delta
    return v0.value, v1.value


def test():
    k = [86, 120, 18, 52]

    test_data = b'12345678'
    test_data = [test_data[x*4:(x+1)*4] for x in range(int(len(test_data)/4))]
    test_data = [struct.unpack('<I', x)[0] for x in test_data]
    test_result = encrypt(test_data, k)
    test_result = [struct.pack('<I', x) for x in test_result]
    test_result = [x.hex() for x in test_result]
    print(test_result)

    raw_data = '2FCC78628950FE657C1C582B90BA604E'
    raw_data = bytes.fromhex(raw_data)
    raw_len = 8
    raw_data = [raw_data[x*raw_len:(x+1)*raw_len]
                for x in range(int(len(raw_data)/raw_len))]
    raw_data = [struct.unpack('>II', x) for x in raw_data]
    # data = encrypt(raw_data, k)
    de_data = [custom_encode_or_decode(raw_data[x]) for x in range(2)]
    pass
    de_data = [[struct.pack('<I', i) for i in x] for x in de_data]
    de_data = [b''.join(x) for x in de_data]
    de_data = b''.join(de_data)
    print(f'raw_data:{raw_data}')
    print(f'de_data:{de_data.hex()}')
    print(f'key:{k}')
    # print(f'data:{data}')
    print(f'de_data:{de_data}')
    pass
