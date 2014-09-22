import requests
from requests.auth import HTTPDigestAuth

from collections import deque
from lxml import html
from urllib.parse import urlparse, urljoin

from customauth import get_auth_info
from fuzzerstrategy import FuzzerStrategy
from helpers import get_url_domain, is_absolute_url, get_url_params,\
    trim_url_params

class DiscoverStrategy(FuzzerStrategy):
    #initialize everything necessary here
    def __init__(self, args):
        super(DiscoverStrategy, self).__init__()

        self.is_logged_in = False
        self.auth_tuple = ()

        self.source_url = args[0] #The first url to be requested

        #A Queue to be used to decide which order to visit pages for crawling
        self.urlqueue = deque()
        self.urlqueue.append(self.source_url)

        self.discovered_urls = {self.source_url}

        #stores all data discovered at each visited url
        self.url_data = dict()

        #Parse the command line arguments passed into the constructor
        for arg in args[1:]:
            arg_value_pair = arg.split('=')
            argname  = arg_value_pair[0]
            argvalue = arg_value_pair[1]

            if argname == '--custom-auth':
                self.auth_tuple = get_auth_info(argvalue)

    #Executes the fuzzing algorithm
    def execute(self):
        #Begin code for any necessary logging in.
        #This only needs to be executed once.
        session = requests.session()
        response = session.get(self.source_url)
        parsed_body = html.fromstring(response.content)

        if self._contains_login_form(parsed_body) and not self.is_logged_in:
            self._login(session, parsed_body)
        else:
            self.is_logged_in = True
        
        #We've logged in, so lets do another request and get actual page data
        response = session.get(self.source_url)
        parsed_body = html.fromstring(response.content)

        #get the title for the requested page and store it
        self.url_data[self.source_url] = dict()
        self.url_data[self.source_url]['title'] =\
            parsed_body.xpath("//title/text()")[0]
      
        #Get all form inputs on the page and store them
        self.url_data[self.source_url]['forminput'] =\
            parsed_body.xpath("//input")

        #store any cookies this page might have
        self.url_data[self.source_url]['cookies'] = response.cookies

        #Prepare to store any url parameters present in links on the page
        self.url_data[self.source_url]['urlparams'] = []
        #We're also storing unique links acessible from the given page
        self.url_data[self.source_url]['accessible_links'] = []
        all_links = set(
            filter(
                lambda url: self._is_valid_page_link(url),
                parsed_body.xpath("//a/@href")
            )
        )
        for link in all_links:
            #We want to create a link as an absolute url so we don't get
            #errors with our requests
            absolute_link = ''
            if self.source_url.endswith('/'):
                absolute_link = urljoin(self.source_url, link)
            else:
               absolute_link = urljoin(self.source_url + '/', link)

            #we want our accessible links to be links without url parameters=
            self.url_data[self.source_url]['accessible_links'].append(
                trim_url_params(absolute_link)
            )

            #get the url parameters from the url and store them in the data
            #structure
            urlparams = get_url_params(absolute_link)
            self.url_data[self.source_url]['urlparams'].extend(
                urlparams
            )
    
    #simply outputs the contents of the data structure
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

    #Parses the text file given for common words
    #Still needs implementation
    def _parse_common_words(self, word_file):
        print("Common words parsed")

    #Conducts the requests necessary to 'login'
    def _login(self, session, parsed_body):
        #perform authentication here
        if self.auth_tuple != ():
            #We use the form's action to generate the login url
            login_form = self._get_login_forms(parsed_body)[0]

            #Generate the login url
            login_url = ''
            if self.source_url.endswith('/'):
                login_url = urljoin(self.source_url, login_form.action)
            else:
               login_url = urljoin(self.source_url + '/', login_form.action)

            #Create the data payload used to log the user in            
            login_data = dict(
                username=self.auth_tuple[0],
                password=self.auth_tuple[1],
                Login='Login'
            )

            #Perform the login
            login_response = session.post(login_url, data=login_data)

            #Was the login successful
            self.is_logged_in = login_response.status_code == 200
        else:
            #No login was necessary
            self.is_logged_in = True

    #Gets any login forms present on an html page
    def _get_login_forms(self, html_body):
        return html_body.xpath("//form[descendant::input[@name='Login']]")

    #Tests if a page contains any login forms
    def _contains_login_form(self, html_body):
        login_forms = html_body.xpath("//form[descendant::input[@name='Login']]")

        return len(login_forms) >= 1

    #Validates a url to see if it can be accepted by the fuzzer
    def _is_valid_page_link(self, url):
        self_domain = self.source_url if\
            self.source_url.endswith('/') else self.source_url + '/'

        return (not is_absolute_url(url)) or get_url_domain(url) == self_domain

    #Finds all links on the current page
    def _find_links(self,url):
        links = []
        return links