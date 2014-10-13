import requests
import os.path

from urllib.parse import urlparse, urljoin

from customauth import get_auth_info
from fuzzerstrategy import FuzzerStrategy
from discoverstrategy import DiscoverStrategy

class TestStrategy(FuzzerStrategy):
    def __init__(self, args):
        super(TestStrategy, self).__init__()

        self.source_url = args[0]

        self.custom_auth = ''

        self.vector_list = []
        self.sensitive_info_list = []

        self.max_response_length = 500

        #Parse the command line arguments passed into the constructor
        for arg in args[1:]:
            arg_value_pair = arg.split('=')
            argname  = arg_value_pair[0]
            argvalue = arg_value_pair[1]

            if argname == '--vectors':
                self._parse_vectors_file(argvalue)
            elif argname == '--custom-auth':
                self.custom_auth = argvalue
            elif argname == '--sensitive':
                self._parse_sensitive_info_file(argvalue)
            elif argname == '--slow':
                try:
                    self.max_response_length = int(argvalue)
                except ValueError:
                    raise Exception("--slow flag must be an integer")

        self.discovery_strategy = DiscoverStrategy(args)

    def execute(self):
        self.discovery_strategy.execute()

        session = requests.session()

        self._login(session)

        print("\n\nTest Results:")

        print((" " * 4) + "Potentially unlinked pages:")
        for url in self.discovery_strategy.common_words_urls:
            response = session.get(url)
            print((" " * 8) + url + ": ", end='')

            if response.status_code == 200:
                print("Exists")
            elif response.status_code == 404:
                print("Does not exist")

        #print all urls with non 200 status codes
        print((" " * 4) + "Requests with invalid status codes:")
        for url in self.discovery_strategy.url_data:
            urldata = self.discovery_strategy.url_data[url]

            if urldata['status_code'] != 200:
                print((" " * 8) + url)

        #print any urls with response times longer than the specified limit
        print((" " * 4) + "Potentially DOS Vulnerable URLs:")
        for url in self.discovery_strategy.url_data:
            urldata = self.discovery_strategy.url_data[url]

            if urldata['response_time'] >= self.max_response_length:
                print((" " * 8) + url)

        print((" " * 4) + "Lack of sanitization present for:")
        for url in self.discovery_strategy.url_data:
            for vector in self.vector_list:
                self._login(session)

                test_response = session.get(urljoin(url, vector))

                if test_response.status_code == 200:
                    print((" " * 8) + url)
                    break

        print((" " * 4) + "Undesired Information Disclosure in:")
        #For each URL:
        #check response text for any element of the sensitive list
        for url in self.discovery_strategy.url_data:
            for info in self.sensitive_info_list:
                self._login(session)

                info_check_response = session.get(url)                
                
                if info in info_check_response.text:
                    print((" " * 8) + url)
                    break


    def _generate_absolute_link(self, url):
        #We want to create a link as an absolute url so we don't get
        #errors with our requests
        absolute_link = ''
        if self.source_url.endswith('/'):
            absolute_link = urljoin(self.source_url, url)
        else:
           absolute_link = urljoin(self.source_url + '/', url)

        return absolute_link

    #Conducts the requests necessary to 'login'
    def _login(self, session):
        #perform authentication here
        auth_tuple = get_auth_info(self.custom_auth)

        if auth_tuple != ():
            #Generate the login url
            login_url = self._generate_absolute_link(
                self.discovery_strategy.login_action
            )

            #Create the data payload used to log the user in            
            login_data = dict(
                username=auth_tuple[0],
                password=auth_tuple[1],
                Login='Login'
            )

            #Perform the login
            login_response = session.post(login_url, data=login_data)

    def _parse_vectors_file(self, vector_file):
        if os.path.isfile(vector_file):
            print("Parsing vector file: %s" % (vector_file))
            for line in open(vector_file):
                self.vector_list.append(line.strip())
        else:
            raise Exception("%s: file not found" % (vector_file))

    def _parse_sensitive_info_file(self, sensitive_info_file):
        if os.path.isfile(sensitive_info_file):
            print(
                "Parsing sensitive information file: %s" % (sensitive_info_file)
            )
            for line in open(sensitive_info_file):
                self.sensitive_info_list.append(line.strip())
        else:
            raise Exception("%s: file not found" % sensitive_info_file)