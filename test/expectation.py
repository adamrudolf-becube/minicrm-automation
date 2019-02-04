class Expectation:
    def __init__(self, command_pattern, response_file, repeatedly = False):
        self.command_pattern = command_pattern
        self.response_file = response_file
        self.repeatedly = repeatedly
