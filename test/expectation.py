class Expectation:
    def __init__(self, command_pattern, response_identifier, repeatedly = False):
        self.command_pattern = command_pattern
        self.response_identifier = response_identifier
        self.repeatedly = repeatedly
