import requests

from collections import deque
from lxml import html

from fuzzerstrategy import FuzzerStrategy

class DiscoverStrategy(FuzzerStrategy):
    def __init__(self, args):
        acceptedOptions = ['--custom-auth', '--common-words'];
        self.sourceUrl = args[0]

        self.discoveredUrls = set()
        self.discoveredUrls.add(self.sourceUrl)

        self.urlsQueue = deque()
        self.urlsQueue.append(self.sourceUrl)

        for arg in args[1:]:
            argValuePair = arg.split('=')
            print("option: %s\tvalue:%s" % (argValuePair[0], argValuePair[1]))

    def execute(self):
        while len(self.urlsQueue):
            url = self.urlsQueue.popleft()
            print(url)
