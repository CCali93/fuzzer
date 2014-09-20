import requests
from requests.auth import HTTPDigestAuth

from collections import deque
from lxml import html
from urllib.parse import urlparse, urljoin

import customauth
from fuzzerstrategy import FuzzerStrategy

class DiscoverStrategy(FuzzerStrategy):
    def __init__(self, args):
        super(DiscoverStrategy, self).__init__()
        self.auth_tuple = ()

        self.source_url = args[0]

        self.urlqueue = deque()
        self.urlqueue.append(self.source_url)

        self.discoveredUrls = {self.source_url}

        self.system_inputs = {}

        for arg in args[1:]:
            arg_value_pair = arg.split('=')
            argname  = arg_value_pair[0]
            argvalue = arg_value_pair[1]

            if argname == '--custom-auth':
                self._parse_custom_auth(argvalue)
            elif argname == '--common-words':
                self._parse_common_words(argvalue)

    def execute(self):
        session = requests.session()
        response = session.get(self.source_url)
        parsedBody = html.fromstring(response.content)

        if self._contains_login_form(parsedBody):
            self._login(session, parsedBody)
      
        response = session.get(self.source_url)

        print(parsedBody.xpath("//title/text()")[0])

        print("\tForm Inputs:")

        self.system_inputs[self.source_url] = parsedBody.xpath("//input")
        for inputElem in self.system_inputs[self.source_url]:
            print("\t\t" + (str(inputElem)))

        print("\tCookies:")
        cookieList = response.cookies
        for (key, value) in cookieList:
            print("\t\t%s: %s" % (key, value))

        print(parsedBody.xpath('//a/@href'))

    def _parse_common_words(self, wordFile):
        print("Common words parsed")
    
    def _parse_custom_auth(self, auth_string):
        if auth_string in customauth.authconfig:
            self.auth_tuple = customauth.authconfig[auth_string]
        else:
            self.auth_tuple = ()

    def _login(self, session, parsedBody):
        #perform authentication here
        login_form = self._get_login_forms(parsedBody)[0]

        login_url = ''
        if self.source_url.endswith('/'):
            login_url = urljoin(self.source_url, login_form.action)
        else:
           login_url = urljoin(self.source_url + '/', login_form.action)
        
        login_data = dict(username='', password='', Login='Login')
        session.post(login_url, data=login_data)

    def _get_login_forms(self, htmlBody):
        return htmlBody.xpath("//form[descendant::input[@name='Login']]")

    def _contains_login_form(self, htmlBody):
        login_forms = htmlBody.xpath("//form[descendant::input[@name='Login']]")

        return len(login_forms) >= 1
