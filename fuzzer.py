import requests
import sys

from discoverstrategy import DiscoverStrategy

#stub function as a placeholder for future code
def main(args):
    command = arg[0]
    strategy = None

    if command == "discover":
        strategy = DiscoverStrategy(args[1:])
    else:
        print("USAGE fuzz [discover | test] url OPTIONS")

if __name__ == '__main__':
    main(sys.argv[1:])