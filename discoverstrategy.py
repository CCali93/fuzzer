from collections import deque

from fuzzerstrategy import FuzzerStrategy

class DiscoverStrategy(FuzzerStrategy):
    def __init__(self, args):
        super(FuzzerStrategy, self).__init__()
        self.acceptedOptions = ['--common-words']
        self.urlsQueue = deque()