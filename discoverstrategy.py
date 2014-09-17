import requests

from collections import deque
from lxml import html
import urlparse

from fuzzerstrategy import FuzzerStrategy

class DiscoverStrategy(FuzzerStrategy):
    def __init__(self, args):
        super(FuzzerStrategy, self).__init__()
        self.acceptedOptions = ['--common-words']
        self.sourceUrl = args[0]

        self.discoveredUrls = set()
        self.discoveredUrls.add(self.sourceUrl)

        self.urlsQueue = deque()
        self.urlsQueue.append(self.sourceUrl)

    def execute():
        while len(self.urlsQueue):
            url = self.urlsQueue.popleft()
            print(url)
