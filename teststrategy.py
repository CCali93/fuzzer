from fuzzerstrategy import FuzzerStrategy

class TestStrategy(FuzzerStrategy):
    def __init__(self, args):
        super(TestStrategy, self).__init__()

        self.vector_list = []
        self.sensitive_info_list = []

        self.max_response_length = 500

        #Parse the command line arguments passed into the constructor
        for arg in args[1:]:
            arg_value_pair = arg.split('=')
            argname  = arg_value_pair[0]
            argvalue = arg_value_pair[1]

            if argname == '--vectors':
                self.vector_list = _parse_vectors_file(argvalue)
            elif argname == '--sensitive':
                self.sensitive_info_list = _parse_sensitive_info_file(argvalue)

    def execute(self):
        print("Testing")

    def _parse_vectors_file(self, vector_file):
        print("Vectors parsed")

    def _parse_sensitive_info_file(self, sensitive_info_file):
        print("Senstive Info Parsed")