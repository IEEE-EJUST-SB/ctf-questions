from hashlib import shake_256
from secrets import token_bytes
from nacl.bindings import (crypto_scalarmult_ed25519_noclamp,
                           crypto_box_seed_keypair,
                           crypto_core_ed25519_sub,
                           crypto_core_ed25519_add,
                           crypto_core_ed25519_is_valid_point,
                           crypto_scalarmult_ed25519_SCALARBYTES,
                           crypto_box_SEEDBYTES
                           )


class EccGroup:
    representation: bytes

    def __init__(self, src) -> None:
        match src:
            case EccGroup(representation=_ as src):
                self.representation = src
            case bytes(rep):
                self.representation = rep
            case _:
                raise ValueError(src)
        assert crypto_core_ed25519_is_valid_point(self.representation)

    def __repr__(self) -> str:
        return f'ed25519({self.representation.hex()})'

    def __eq__(self, other: object) -> bool:
        if isinstance(other, EccGroup):
            return self.representation == other.representation
        return False

    def __hash__(self) -> int:
        return hash(('EccGroup', self.representation))

    def __pow__(self, other):
        return self.__class__(crypto_scalarmult_ed25519_noclamp(
            int(other).to_bytes(crypto_scalarmult_ed25519_SCALARBYTES, 'little'),
            self.representation))

    def __mul__(self, other):
        if isinstance(other, self.__class__):
            return self.__class__(crypto_core_ed25519_add(self.representation, other.representation))
        return NotImplemented

    def __truediv__(self, other):
        if isinstance(other, self.__class__):
            return self.__class__(crypto_core_ed25519_sub(self.representation, other.representation))
        return NotImplemented

    @classmethod
    def random(cls, seed: bytes | None = None):
        if seed is not None:
            h = shake_256(seed).digest(crypto_box_SEEDBYTES)
        else:
            h = token_bytes(crypto_box_SEEDBYTES)
        point, _ = crypto_box_seed_keypair(h)
        return cls(point)


EccGroup.G = EccGroup(bytes.fromhex('5866666666666666666666666666666666666666666666666666666666666666'))
EccGroup.Q = 2 ** 252 + 27742317777372353535851937790883648493
