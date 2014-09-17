#!/usr/bin/python3

import sys

from discoverstrategy import DiscoverStrategy

_USAGE_MESSAGE = "USAGE fuzz [discover | test] url OPTIONS"

def main(args):
    command = args[0]
    strategy = None

    if command == "discover":
        strategy = DiscoverStrategy(args[1:])
    else:
        print(_USAGE_MESSAGE)

    if strategy is not None:
        strategy.execute()

if __name__ == '__main__':
    if len(sys.argv) >= 2:
        main(sys.argv[1:])
    else:
        print(_USAGE_MESSAGE)
