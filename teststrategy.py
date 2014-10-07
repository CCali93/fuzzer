from fuzzerstrategy import FuzzerStrategy

class TestStrategy(FuzzerStrategy):
    """docstring for TestStrategy"""
    def __init__(self, args):
        super(TestStrategy, self).__init__()
        self.args = args

    def execute(self):
        print("Testing")