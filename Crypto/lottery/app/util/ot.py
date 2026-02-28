from hashlib import shake_256
from typing import Type
from itertools import batched, chain

from util.wire import Wire
from util.mod import IntegerMod


class ObliviousTransfer:
    def __init__(self, wire: Wire, generator, group, exp: Type[IntegerMod]):
        self._wire = wire
        self._gen = generator
        self._group = group
        self._exp = exp

    def _encrypt_with_keys(self, pt: bytes, bit_keys: list):
        hash = shake_256(b'#'.join(str(k).encode('utf-8') for k in bit_keys))
        keystream = hash.digest(len(pt))
        return bytes((p ^ k for p, k in zip(pt, keystream)))

    def _decrypt_with_keys(self, ct: bytes, bit_keys: list):
        return self._encrypt_with_keys(ct, bit_keys)

    def transfer(self, *values: bytes, k: int = 1):
        n = len(values)
        logn = n.bit_length()
        bit_keys = [[self._gen ** self._exp.random() for _ in [0, 1]] for _ in range(logn)]
        keys = [[bit_keys[bi][(index >> bi) & 1] for bi in range(logn)] for index in range(n)]
        ciphertexts = [self._encrypt_with_keys(pt, k) for pt, k in zip(values, keys)]
        for _get_index in range(k):
            w = [self._gen ** self._exp.random() for _bit_index in range(logn)]
            self._wire.send(*w)
            h = list(batched(self._wire.receive(*([self._group]*2*logn)), 2))
            for (h_0, h_1), w in zip(h, w):
                assert h_0 * h_1 == w, 'Keys for OT do not conform to protocol'
            r = [self._exp.random() for _bit_index in range(logn)]
            u = [self._gen ** rr for rr in r]
            v = [[(h__ ** r_) * bit_key for bit_key, h__ in zip(bit_keys_, h_)] for bit_keys_, h_, r_ in zip(bit_keys, h, r)]
            self._wire.send(*chain(u, *v))
        self._wire.send(*ciphertexts)

    def receive(self, *indices: int, n: int):
        logn = n.bit_length()
        keys = []
        for index in indices:
            bits = [(index >> i) & 1 for i in range(logn)]
            w = self._wire.receive(*[self._group]*logn)
            alpha = [self._exp.random() for _ in range(logn)]
            h_b = [self._gen ** alpha_ for alpha_ in alpha]
            h = [[w_/h_b_, h_b_] if bit else [h_b_, w_/h_b_] for h_b_, w_, bit in zip(h_b, w, bits)]
            for (h_0, h_1), w in zip(h, w):
                if h_0 * h_1 != w:
                    print(f'Something went wrong in calculation: {h_0=}, {h_1=}, {h_0*h_1=}, {w=}')
            self._wire.send(*chain(*h))
            resp = self._wire.receive(*[self._group]*logn, *[self._group]*2*logn)
            u, v = resp[:logn], resp[logn:]
            v = batched(v, 2)
            keys.append([v_[bit] / (u_ ** alpha_) for v_, u_, alpha_, bit in zip(v, u, alpha, bits)])
        ciphertexts = self._wire.receive(*[bytes]*n)
        values = [self._decrypt_with_keys(ciphertexts[i], k) for i, k in zip(indices, keys)]
        return values
