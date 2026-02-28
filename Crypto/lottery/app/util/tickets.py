from random import SystemRandom
from secrets import token_hex

from util.constants import G, BaseGroup, ExponentRing
from util.ot import ObliviousTransfer
from util.schnorr import Schnorr
from util.wire import Wire


_schnorr = Schnorr(G, ExponentRing)

# 6 out of 49
POSITIONS = list(range(1, 50))
NUM_CROSSES = 6


def _ticket_cross(position: int, token: str):
    assert position in POSITIONS, 'You are not supposed to put a cross there.'
    return f'{position}#{token}'.encode('utf-8')


class TicketServer:
    def __init__(self, wire: Wire):
        self._wire = wire
        self._pk, self._sk = _schnorr.keygen()
        self._invalid_tokens = set()

    def start(self):
        self._wire.send(self._pk)

    def sell_ticket(self):
        ticket_token = token_hex(64)
        signatures = [_schnorr.sign(self._sk, _ticket_cross(i, ticket_token)) for i in POSITIONS]
        ot = ObliviousTransfer(self._wire, G, BaseGroup, ExponentRing)
        ot.transfer(*[self._wire.encode(*s) for s in signatures], k=NUM_CROSSES)
        self._wire.send(ticket_token)

    def check_ticket(self):
        ticket_token = self._wire.receive(str)
        if ticket_token in self._invalid_tokens:
            return []
        self._invalid_tokens.add(ticket_token)
        positions = []
        valid = True
        for _ in range(NUM_CROSSES):
            position, *sig = self._wire.receive(int, *_schnorr.sig_type)
            if not _schnorr.verify(self._pk, _ticket_cross(position, ticket_token), sig):
                valid = False
            positions.append(position)
        return positions if valid else []

    def draw(self):
        return SystemRandom().sample(POSITIONS, k=NUM_CROSSES)


class TicketClient:

    def __init__(self, wire: Wire) -> None:
        self._wire = wire
        self.server_pk = None

    def start(self):
        self.server_pk = self._wire.receive(_schnorr.pk_type)

    def buy_ticket(self, positions: list[int]):
        assert len(positions) == NUM_CROSSES
        ot = ObliviousTransfer(self._wire, G, BaseGroup, ExponentRing)
        sigs = [self._wire.decode(sig, *_schnorr.sig_type)
                for sig in ot.receive(*[POSITIONS.index(p) for p in positions], n=len(POSITIONS))]
        ticket_token = self._wire.receive(str)
        for p, sig in zip(positions, sigs):
            assert _schnorr.verify(self.server_pk, _ticket_cross(p, ticket_token), sig)
        return ticket_token, list(zip(positions, sigs))

    def submit_ticket(self, ticket):
        token, crosses = ticket
        assert len(crosses) == NUM_CROSSES
        self._wire.send(token)
        for position, sig in crosses:
            self._wire.send(position, *sig)

    def positions_on_ticket(self, ticket):
        _, crosses = ticket
        return [pos for pos, _sig in crosses]
