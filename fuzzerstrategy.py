#An interface representing various "strategies" for fuzzing

class FuzzerStrategy:
    def execute(self):
        raise NotImplementedError("execute() needs to be implemented")