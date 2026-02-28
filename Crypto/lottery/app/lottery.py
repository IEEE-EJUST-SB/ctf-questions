from util.tickets import NUM_CROSSES, POSITIONS, TicketClient, TicketServer
from util.wire import Wire
from flag import FLAG

MAIN_MENU = '''
---=== LOTtery ===---
Your wallet contains {capital}€.
Each ticket for 6 from 49 is {ticket_price}€.
You can buy a ticket or wait for the draw.
'''.strip()


class Lottery:
    TICKET_PRICE: int = 20
    PRIZES: list[int] = [0, 0, 0, 10, 25, 100, 1_000]

    capital: int = 100

    def __init__(self, wire: Wire):
        self.wire = wire

    def run(self):
        while True:
            tickets = TicketServer(self.wire)
            tickets.start()
            while True:
                if self.capital >= max(self.PRIZES) * 10:
                    self.wire.send('flag')
                    self.wire.send(FLAG)
                self.wire.send('menu')
                self.wire.send(self.capital, self.TICKET_PRICE)
                match self.wire.receive(str):
                    case 'buy':
                        self.buy_ticket(tickets)
                    case 'draw':
                        if self.draw(tickets):
                            break
                        return
                    case 'exit':
                        return
                    case _ as command:
                        print(f'Unknown command {command}')

    def buy_ticket(self, ticket_server: TicketServer):
        if self.capital >= self.TICKET_PRICE:
            self.capital -= self.TICKET_PRICE
            self.wire.send('ok')
            ticket_server.sell_ticket()
        else:
            self.wire.send('You can\'t afford another ticket.')

    def draw(self, tickets: TicketServer):
        winning_positions = tickets.draw()
        self.wire.send(winning_positions)
        while True:
            match self.wire.receive(str):
                case 'submit':
                    positions = tickets.check_ticket()
                    correct = len(set(positions) & set(winning_positions))
                    prize = self.PRIZES[correct]
                    self.wire.send(prize)
                    self.capital += prize
                case 'next':
                    return True
                case 'exit':
                    return False


class Participant:
    ticket_client: TicketClient
    tickets: list

    def __init__(self, wire: Wire) -> None:
        self.wire = wire

    def main_menu(self, capital, ticket_price):
        print(MAIN_MENU.format(capital=capital, ticket_price=ticket_price))
        while True:
            match input('[B]uy, [d]raw or [e]xit? ').lower().strip()[:1]:
                case '' | 'b':
                    return 'buy'
                case 'd':
                    return 'draw'
                case 'e':
                    return 'exit'
                case other:
                    print(f'Invalid option "{other}"')

    def ticket_menu(self):
        selected = set()
        while len(selected) < NUM_CROSSES:
            print('┏' + '━'*21 + '┓')
            for pos in POSITIONS:
                if pos % 7 == 1:
                    print('┃', end='')
                if pos in selected:
                    print(' ✗ ', end='')
                else:
                    print(f'{pos:3}', end='')
                if pos % 7 == 0:
                    print('┃')
            print('┗' + '━'*21 + '┛')
            inp = input('Where to cross? ')
            try:
                position = int(inp)
                if position not in POSITIONS:
                    raise ValueError
                selected.add(position)
            except ValueError:
                print(f'Invalid position: {inp}')
        return list(selected)

    def buy_ticket(self):
        status = self.wire.receive(str)
        if status != 'ok':
            print(f'There was a problem: {status}')
        else:
            positions = self.ticket_menu()
            ticket = self.ticket_client.buy_ticket(positions)
            self.tickets.append(ticket)

    def draw(self):
        winning_positions = [int(pos) for pos in self.wire.receive(list)]
        winning_positions.sort()
        print(f'The winning positions are: {", ".join(f'{w}' for w in winning_positions)}')
        for ticket in self.tickets:
            self.wire.send('submit')
            self.ticket_client.submit_ticket(ticket)
            prize = self.wire.receive(int)
            positions = self.ticket_client.positions_on_ticket(ticket)
            positions.sort()
            print(f'You won {prize}€ with {", ".join(f'{p}' for p in positions)}')
        self.wire.send('next')

    def run(self):
        while True:
            self.ticket_client = TicketClient(self.wire)
            self.ticket_client.start()
            self.tickets = []
            while True:
                match self.wire.receive(str):
                    case 'flag':
                        flag = self.wire.receive(str)
                        print(f'FLAG: {flag}')
                        continue
                    case 'menu':
                        pass
                    case _:
                        assert False
                capital, ticket_price = self.wire.receive(int, int)
                option = self.main_menu(capital, ticket_price)
                self.wire.send(option)
                match option:
                    case 'buy':
                        self.buy_ticket()
                    case 'draw':
                        self.draw()
                        break
                    case 'exit':
                        print('Bye')
                        return
