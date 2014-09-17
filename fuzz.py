import sys

from discoverstrategy import DiscoverStrategy

def main(args):
    command = args[0]
    strategy = None

    if command == "discover":
        strategy = DiscoverStrategy(args[1:])
    else:
        print("USAGE fuzz [discover | test] url OPTIONS")

    if strategy is not None:
        strategy.execute()

if __name__ == '__main__':
    main(sys.argv[1:])
