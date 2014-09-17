import sys

from discoverstrategy import DiscoverStrategy

def main(args):
    command = arg[0]
    strategy = None

    if command == "discover":
        strategy = DiscoverStrategy(args[1:])
    else:
        print("USAGE fuzz [discover | test] url OPTIONS")

    strategy.execute()

if __name__ == '__main__':
    main(sys.argv[1:])
