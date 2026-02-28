from abc import ABCMeta
from secrets import randbelow
from hashlib import shake_256


def _binary_dispatch_representative(reverse_name):
    def wrapper(func):
        def f(self, other):
            res = getattr(self.representative, func.__name__)(other)
            if res != NotImplemented:
                return self.__class__(res)
            return getattr(other, reverse_name)(self.representative)

        f.__name__ = func.__name__
        f.__qualname__ = func.__qualname__
        return f
    return wrapper


class IntegerMod(metaclass=ABCMeta):
    representative: int
    mod: int

    def __init__(self, *args, **kwargs) -> None:
        match args:
            case [IntegerMod(mod=self.mod) as other]:
                self.representative = other.representative
                return
            case [IntegerMod() as other]:
                raise TypeError(f'Implicit conversion between IntegerMod instances of different moduli: '
                                f'Wanted {self.mod}, got {other.mod}')
        self.representative = int(*args, **kwargs) % self.mod

    def __repr__(self) -> str:
        return f'{self.representative} mod {self.mod}'

    def __int__(self):
        return self.representative

    def __eq__(self, other: object) -> bool:
        if isinstance(other, IntegerMod):
            return self.mod == other.mod and self.representative == other.representative
        return False

    def __hash__(self) -> int:
        return hash((self.representative, self.mod))

    def __neg__(self):
        return self.__class__(self.representative.__neg__())

    @_binary_dispatch_representative('__radd__')
    def __add__(self, other): pass
    @_binary_dispatch_representative('__rsub__')
    def __sub__(self, other): pass
    @_binary_dispatch_representative('__rmul__')
    def __mul__(self, other): pass

    @_binary_dispatch_representative('__add__')
    def __radd__(self, other): pass
    @_binary_dispatch_representative('__sub__')
    def __rsub__(self, other): pass
    @_binary_dispatch_representative('__mul__')
    def __rmul__(self, other): pass

    def __pow__(self, other):
        res = self.representative.__pow__(other, self.mod)
        if res == NotImplemented:
            res = other.__rpow__(self.representative, self.mod)
        return self.__class__(res)

    def __rpow__(self, other, mod=None):
        return self.representative.__rpow__(other, mod)

    def __truediv__(self, other):
        if isinstance(other, IntegerMod):
            return self * pow(other.representative, -1, self.mod)
        return self * pow(other, -1, self.mod)

    def __rtruediv__(self, other):
        return self.__class__(pow(self.representative, -1, self.mod)) * other

    @classmethod
    def random(cls, seed: bytes | None = None):
        if seed is not None:
            bl = (cls.mod-1).bit_length()
            while True:
                h = shake_256(seed).digest(64+(bl+7)//8)
                seed, val = h[:64], h[64:]
                val = int.from_bytes(val)
                val &= (1 << bl) - 1
                if val in range(cls.mod):
                    return cls(val)
        return cls(randbelow(cls.mod))


def Mod(m: int, name: str = None):
    name = f'IntegerMod_{name or str(m)}'

    class Cls(IntegerMod):
        mod = m
        __name__ = name
        __qualname__ = name
    return Cls
