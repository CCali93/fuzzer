import requests

from collections import deque
from lxml import html
from urllib.parse import urlparse

from fuzzerstrategy import FuzzerStrategy

class DiscoverStrategy(FuzzerStrategy):
    def __init__(self, args):
        super(DiscoverStrategy, self).__init__()
        optionCommands = {
            '--custom-auth': self.parseCommonWords,
            '--common-words': self.parseCustomAuth
        }

        self.sourceUrl = args[0]

        self.urlQueue = deque()
        self.urlQueue.append(self.sourceUrl)

        self.discoveredUrls = {self.sourceUrl}

        self.systemInputs = set()

        for arg in args[1:]:
            argValuePair = arg.split('=')
            argName  = argValuePair[0]
            argValue = argValuePair[1]

            if argName in optionCommands:
                optionCommands[argName](argValue)

    def execute(self):
        while len(self.urlQueue):
            url = self.urlQueue.popleft()
            response = requests.get(url)

            parsedBody = html.fromstring(response.content)
            print(parsedBody.xpath("//title/text()"))

            formInputs = parsedBody.xpath("//input")

            links = {
                urlparse.urljoin(response.url, url) for url in
                    parsedBody.xpath('//a/@href') if
                    urlparse.urljoin(response.url, url).startswith('http')
            }

            # Set difference to find new URLs
            for link in (links - self.discoveredUrls):
                self.discoveredUrls.add(link)
                self.urlQueue.append(link)

    def parseCommonWords(self, wordFile):
        pass
    
    def parseCustomAuth(self, authString):
        pass
