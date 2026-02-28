from hashlib import sha512
from typing import Type

from util.mod import IntegerMod


class Schnorr:
    def __init__(self, gen, exp: Type[IntegerMod]):
        self._gen = gen
        self._exp = exp
        self.sig_type = [exp, exp]
        self.pk_type = gen.__class__

    def _full_domain_hash(self, a, message: bytes):
        return self._exp.random(sha512(message + b'#' + str(a).encode()).digest())

    def keygen(self):
        sk = self._exp.random()
        pk = self._gen ** sk
        return pk, sk

    def sign(self, sk: IntegerMod, message: bytes):
        u = self._exp.random()
        a = self._gen ** u
        c = self._full_domain_hash(a, message)
        r = u + c * sk
        return (c, r)

    def verify(self, pk, message: bytes, sig: tuple[IntegerMod, IntegerMod]):
        c, r = sig
        a = (self._gen ** r) / (pk ** c)
        d = self._full_domain_hash(a, message)
        return c == d
