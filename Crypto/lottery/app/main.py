#!/usr/bin/env python3
from argparse import ArgumentParser, Namespace
from socketserver import BaseRequestHandler, ThreadingTCPServer

from util.wire import Wire


DEFAULT_PORT = 1024


def host_lottery(args: Namespace):
    from lottery import Lottery

    class LotteryTcpHandler(BaseRequestHandler):
        def handle(self) -> None:
            wire = Wire.from_socket(self.request)
            lottery = Lottery(wire)
            lottery.run()

    with ThreadingTCPServer(
            (args.laddr, args.lport),
            LotteryTcpHandler,
            bind_and_activate=True) as server:
        server.serve_forever()


def play_lottery(args: Namespace):
    from lottery import Participant
    try:
        wire = Wire.connect(args.daddr, args.dport, listen=False)
        participant = Participant(wire)
        participant.run()
    finally:
        wire.close()


parser = ArgumentParser(
    description='LOTtery - OT-based, fair and secure 6-from-49 lottery\n\n'
    'Take part in a lottery where the host cannot screw you over without you noticing!\n'
    'They cannot know your tickets before announcing the winning combination.',
)

subparsers = parser.add_subparsers(required=True)
parser_host = subparsers.add_parser('host', description='Host a lottery over the network')
parser_host.add_argument('-a', '--address', dest='laddr', help='The ip address to listen on', default='127.0.0.1')
parser_host.add_argument('-p', '--port', dest='lport', help='The port to listen on', type=int, default=DEFAULT_PORT)
parser_host.set_defaults(func=host_lottery)
parser_host = subparsers.add_parser('play', description='Take part in a lottery over the network')
parser_host.add_argument('-a', '--address', dest='daddr', help='The ip address to connect to', default='127.0.0.1')
parser_host.add_argument('-p', '--port', dest='dport', help='The port to connect to', type=int, default=DEFAULT_PORT)
parser_host.set_defaults(func=play_lottery)

if __name__ == '__main__':
    args = parser.parse_args()
    args.func(args)
