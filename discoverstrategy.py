import requests
from requests.auth import HTTPDigestAuth

from collections import deque
from lxml import html
from urllib.parse import urlparse, urljoin

import customauth
from fuzzerstrategy import FuzzerStrategy
from helpers import get_url_domain, is_absolute_url, get_url_params,\
    trim_url_params

class DiscoverStrategy(FuzzerStrategy):
    def __init__(self, args):
        super(DiscoverStrategy, self).__init__()

        self.is_logged_in = False
        self.auth_tuple = ()

        self.source_url = args[0]

        self.urlqueue = deque()
        self.urlqueue.append(self.source_url)

        self.discovered_urls = {self.source_url}

        self.url_data = dict()

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
        self.url_data[self.source_url] = dict()
        self.url_data[self.source_url]['title'] =\
            parsed_body.xpath("//title/text()")[0]

        response = session.get(self.source_url)
      
        self.url_data[self.source_url]['forminput'] =\
            parsed_body.xpath("//input")

        self.url_data[self.source_url]['cookies'] = response.cookies

        self.url_data[self.source_url]['urlparams'] = []
        self.url_data[self.source_url]['accessible_links'] = []
        all_links = set(
            filter(
                lambda url: self._is_valid_page_link(url),
                parsed_body.xpath("//a/@href")
            )
        )
        for link in all_links:
            absolute_link = ''
            if self.source_url.endswith('/'):
                absolute_link = urljoin(self.source_url, link)
            else:
               absolute_link = urljoin(self.source_url + '/', link)

            self.url_data[self.source_url]['accessible_links'].append(
                trim_url_params(absolute_link)
            )
            urlparams = get_url_params(absolute_link)
            self.url_data[self.source_url]['urlparams'].extend(
                urlparams
            )
        
    def output_discovered_data(self):
        for (url) in self.url_data:
            print(self.url_data[url]['title'])

            print("\tForm Inputs:")
            for input_elem in self.url_data[url]['forminput']:
                print("\t\t" + (str(input_elem)))

            print("\tURL Parameters:")
            for urlparam in self.url_data[url]['urlparams']:
                print("\t\t%s" % (urlparam))

            print("\tCookies:")
            for (key, value) in self.url_data[url]['cookies']:
                print("\t\t%s: %s" % (key, value))

            print("\tLinks:")
            for link in self.url_data[url]['accessible_links']:
                print("\t\t%s" % (link))


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
