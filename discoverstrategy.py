import requests
from requests.auth import HTTPDigestAuth

from collections import deque
from lxml import html
from urllib.parse import urlparse, urljoin

import customauth
from fuzzerstrategy import FuzzerStrategy
from helpers import get_url_domain, is_absolute_url

class DiscoverStrategy(FuzzerStrategy):
    def __init__(self, args):
        super(DiscoverStrategy, self).__init__()

        self.is_logged_in = False
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
        parsed_body = html.fromstring(response.content)

        if self._contains_login_form(parsed_body) and not self.is_logged_in:
            self._login(session, parsed_body)
        else:
            self.is_logged_in = True
        
        response = session.get(self.source_url)
        parsed_body = html.fromstring(response.content)
        print(parsed_body.xpath("//title/text()")[0])

        response = session.get(self.source_url)

        print("\tForm Inputs:")
        self.system_inputs[self.source_url] = parsed_body.xpath("//input")
        for input_elem in self.system_inputs[self.source_url]:
            print("\t\t" + (str(input_elem)))

        print("\tCookies:")
        cookie_list = response.cookies
        for (key, value) in cookie_list:
            print("\t\t%s: %s" % (key, value))

        print("\tLinks:")
        all_links = filter(
            lambda url: self._is_valid_page_link(url),
            parsed_body.xpath("//a/@href")
        )
        for link in all_links:
            absolute_link = ''
            if self.source_url.endswith('/'):
                absolute_link = urljoin(self.source_url, link)
            else:
               absolute_link = urljoin(self.source_url + '/', link)
            print("\t\t%s" % (absolute_link))

    def _parse_common_words(self, word_file):
        print("Common words parsed")
    
    def _parse_custom_auth(self, auth_string):
        if auth_string in customauth.authconfig:
            self.auth_tuple = customauth.authconfig[auth_string]
        else:
            self.auth_tuple = ()

    def _login(self, session, parsed_body):
        #perform authentication here
        if self.auth_tuple != ():
            login_form = self._get_login_forms(parsed_body)[0]

            login_url = ''
            if self.source_url.endswith('/'):
                login_url = urljoin(self.source_url, login_form.action)
            else:
               login_url = urljoin(self.source_url + '/', login_form.action)

            login_data = dict(
                username=self.auth_tuple[0],
                password=self.auth_tuple[1],
                Login='Login'
            )
            login_response = session.post(login_url, data=login_data)
            self.is_logged_in = login_response.status_code == 200
        else:
            self.is_logged_in = True


    def _get_login_forms(self, html_body):
        return html_body.xpath("//form[descendant::input[@name='Login']]")

    def _contains_login_form(self, html_body):
        login_forms = html_body.xpath("//form[descendant::input[@name='Login']]")

        return len(login_forms) >= 1

    def _is_valid_page_link(self, url):
        self_domain = self.source_url if\
            self.source_url.endswith('/') else self.source_url + '/'

        return (not is_absolute_url(url)) or get_url_domain(url) == self_domain
