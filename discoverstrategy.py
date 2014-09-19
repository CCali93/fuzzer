import requests
from requests.auth import HTTPDigestAuth

from collections import deque
from lxml import html
from urllib.parse import urlparse

import customauth
from fuzzerstrategy import FuzzerStrategy

class DiscoverStrategy(FuzzerStrategy):
    def __init__(self, args):
        super(DiscoverStrategy, self).__init__()
        self.authTuple = ()

        self.sourceUrl = args[0]

        self.urlQueue = deque()
        self.urlQueue.append(self.sourceUrl)

        self.discoveredUrls = {self.sourceUrl}

        self.systemInputs = {}

        for arg in args[1:]:
            argValuePair = arg.split('=')
            argName  = argValuePair[0]
            argValue = argValuePair[1]

            if argName == '--custom-auth':
                self.parseCustomAuth(argValue)
            elif argName == '--common-words':
                pass

    def execute(self):
        response = requests.get(
            self.sourceUrl,
            auth=HTTPDigestAuth(self.authTuple[0], self.authTuple[1])
        )

        parsedBody = html.fromstring(response.content)
        print(parsedBody.xpath("//title/text()")[0])

        print("\tForm Inputs:")

        self.systemInputs[self.sourceUrl] = parsedBody.xpath("//input")
        for inputElem in self.systemInputs[self.sourceUrl]:
            print("\t\t" + (str(inputElem)))

        print("\tCookies:")
        cookieList = response.cookies
        for (key, value) in cookieList:
            print("\t\t%s: %s" % (key, value))

        print(parsedBody.xpath('//a/@href'))

    def parseCommonWords(self, wordFile):
        pass
    
    def parseCustomAuth(self, authString):
        if authString in customauth.authConfig:
            self.authTuple = customauth.authConfig[authString]
        else:
            self.authTuple = ()
