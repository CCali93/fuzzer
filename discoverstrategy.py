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

        for arg in args[1:]:
            argValuePair = arg.split('=')
            argName  = argValuePair[0]
            argValue = argValuePair[1]

            if argName in optionCommands:
                optionCommands[argName](argValue)

    def execute(self):
        response = requests.get(self.sourceUrl)

    def parseCommonWords(self, wordFile):
        pass
    
    def parseCustomAuth(self, authString):
        pass
