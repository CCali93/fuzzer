#!/usr/bin/python3

import sys

from discoverstrategy import DiscoverStrategy

_USAGE_MESSAGE = "USAGE fuzz [discover | test] url OPTIONS"

#the main function
def main(args):
    command = args[0]
    strategy = None

    #based on the command entered we create the appropriate strategy to do the
    #work we need
    if command == "discover":
        strategy = DiscoverStrategy(args[1:])
    else:
        print(_USAGE_MESSAGE)

    #Basically if the user entered a valid command
    if strategy is not None:
        strategy.execute()

        #output the discovered stuff if we're doing discovery
        if command == 'discover':
            strategy.output_discovered_data()

if __name__ == '__main__':
    #If the user entered the right amount of command line arguments
    if len(sys.argv) >= 2:
        main(sys.argv[1:])
    else:
        print(_USAGE_MESSAGE)
