from ctypes import *
from typing import List
from .Constance import magic_number_delta as delta


def encrypt(v, k: List[int], run_round: int = 32):
    v0 = c_uint32(v[0])
    v1 = c_uint32(v[1])
    v_sum = c_uint32(0)
    for i in range(run_round):
        v0.value += (((v1.value << 4) ^ (v1.value >> 5)) +
                     v1.value) ^ (v_sum.value+k[v_sum.value & 3])
        v_sum.value += delta
        v1.value += (((v0.value << 4) ^ (v0.value >> 5)) +
                     v0.value) ^ (v_sum.value+k[(v_sum.value >> 11) & 3])
    return v0.value, v1.value


def decrypt(v, k: List[int], run_round: int = 32):
    v0 = c_uint32(v[0])
    v1 = c_uint32(v[1])
    v_sum = c_uint32(delta * run_round)
    for i in range(run_round):
        v1.value -= (((v0.value << 4) ^ (v0.value >> 5)) +
                     v0.value) ^ (v_sum.value+k[(v_sum.value >> 11) & 3])
        v_sum.value -= delta
        v0.value -= (((v1.value << 4) ^ (v1.value >> 5)) +
                     v1.value) ^ (v_sum.value+k[v_sum.value & 3])

    return v0.value, v1.value


def test():
    raw_data = [1, 2]
    k = [2, 2, 3, 4]
    data = encrypt(raw_data, k)
    de_data = decrypt(data, k)
    print(f'raw_data:{raw_data}')
    print(f'key:{k}')
    print(f'data:{data}')
    print(f'de_data:{de_data}')

