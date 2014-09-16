from collections import deque
from lxml import html

from fuzzerstrategy import FuzzerStrategy

class DiscoverStrategy(FuzzerStrategy):
    def __init__(self, args):
        super(FuzzerStrategy, self).__init__()
        self.acceptedOptions = ['--common-words']

        self.discoveredUrls = set()
        self.discoveredUrls.add(args[0])

        self.urlsQueue = deque()
        self.urlsQueue.append(args[0])

    def execute():
        while len(self.urlsQueue):
            url = self.urlsQueue.popleft()
