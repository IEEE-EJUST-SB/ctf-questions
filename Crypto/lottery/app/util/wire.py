from json import JSONEncoder, dumps, loads
from typing import Any
from base64 import b64encode, b64decode
import socket

from util.mod import IntegerMod
from util.ecc import EccGroup


class LotteryEncoder(JSONEncoder):
    def default(self, o: Any) -> Any:
        match o:
            case IntegerMod(representative=r):
                return {'__IntegerMod': True, 'rep': b64encode(r.to_bytes(r.bit_length() // 8 + 1)).decode()}
            case bytes(b):
                return {'__bytes': True, 'b64': b64encode(b).decode()}
            case EccGroup() as point:
                return {'__EccGroup': True, 'b64': b64encode(point.representation).decode()}
        return super().default(o)


def lottery_decode(dct: dict):
    match dct:
        case {'__IntegerMod': True, 'rep': str(representative)}:
            return int.from_bytes(b64decode(representative))
        case {'__bytes': True, 'b64': str(b64)}:
            return b64decode(b64)
        case {'__EccGroup': True, 'b64': str(b64)}:
            return EccGroup(b64decode(b64))
    return dct


class Wire:
    MSG_SEP = b'\n'
    s: socket.socket

    @classmethod
    def from_socket(Cls, socket: socket.socket):
        self = Cls()
        self.s = socket
        return self

    @classmethod
    def connect(Cls, ip: str, port: int, listen: False):
        self = Cls()
        self.s = None
        if listen:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
                listener.bind((ip, port))
                listener.listen(1)
                self.s, _ = listener.accept()
            listener.close()
        else:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.connect((ip, port))
        return self

    def recvmsg(self):
        buf = b''
        while not buf.endswith(self.MSG_SEP):
            c = self.s.recv(1)
            buf += c
        return buf[:-len(self.MSG_SEP)]

    def sendmsg(self, msg: bytes):
        assert self.MSG_SEP not in msg
        self.s.send(msg + self.MSG_SEP)

    def close(self):
        if self.s:
            self.s.close()

    def encode(self, *values) -> bytes:
        return dumps(values, cls=LotteryEncoder).encode()

    def decode(self, value: bytes, *types):
        raw = loads(value, object_hook=lottery_decode)
        assert isinstance(raw, list)
        assert len(raw) == len(types), f'Length mismatch: {raw, types}'
        if len(raw) == 1:
            return types[0](raw[0])
        return [t(v) for t, v in zip(types, raw)]

    def receive(self, *types):
        msg = self.recvmsg()
        return self.decode(msg, *types)

    def send(self, *values):
        payload = self.encode(*values)
        self.sendmsg(payload)
