import os.path

from fuzzerstrategy import FuzzerStrategy
from discoverstrategy import DiscoverStrategy

class TestStrategy(FuzzerStrategy):
    def __init__(self, args):
        super(TestStrategy, self).__init__()

        self.discovery_strategy = DiscoverStrategy(args)

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
            elif argname == '--sensitive':
                self._parse_sensitive_info_file(argvalue)
            elif argname == '--slow':
                self.max_response_length = int(argvalue)

    def execute(self):
        self.discovery_strategy.execute()

        print("\n\nTest Results:")

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

        """
        test forms for information disclosure
        submit forms and scan response for any information in the provided file
        """

        """
        Using given inputs, somehow check for properly escaped values upon
        submission
        """

    def _parse_vectors_file(self, vector_file):
        if os.path.isfile(vector_file):
            for line in open(vector_file):
                self.vector_list.append(line.strip())
        else:
            raise Exception("%s: file not found" % (vector_file))

    def _parse_sensitive_info_file(self, sensitive_info_file):
        if os.path.isfile(sensitive_info_file):
            for line in open(sensitive_info_file):
                self.sensitive_info_list.append(line.strip())
        else:
            raise Exception("%s: file not found" % sensitive_info_file)